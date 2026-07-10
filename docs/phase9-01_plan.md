# Phase 9-01 方案设计: CFG handler→class edge 误分类修复

> 基线报告: `docs/baseline_evaluate_report_20260710_085636.md` 第 6.4 节
> 影响范围: 约 50 个文件（含 abc.py 等关键标准库）

---

## 1. 问题分类

### 1.1 问题级别

| 维度 | 评级 | 说明 |
|------|:----:|------|
| 影响面 | 🔴 大 | ~50 文件受影响（abc.py、pprint.py 等关键库） |
| 严重程度 | 🟡 中 | 反编译成功但结构错位（不是崩溃） |
| 优先级 | **P0** | 控制块异常 + 影响面大 = 最高优先级 |

### 1.2 现象

反编译输出中，try-except 块结束后紧邻的 class/function 定义被错误地嵌套在 handler 块内：

```python
# ✅ 正确输出:
def test():
    try:
        ...
    except:
        ...
    class Foo:     # ← 应在 try 结构外，与 def test() 同级
        pass
    def bar():     # ← 同样应在 try 结构外
        pass

# ❌ 错误输出（当前）:
def test():
    try:
        ...
    except:
        ...
        class Foo:     # ← 被错误缩进在 except 块内
            pass
        def bar():     # ← 也被嵌套在 except 内
            pass
```

### 1.3 根因

BlockScanner 的 `LinkBlocks()` 方法对于 handler/RAISE_VARARGS 之后的 fallthrough 块，会将后续的 blocks 不加区分地链接为 handler 的后继。当后续 block 包含 `LOAD_BUILD_CLASS`（class 定义）或 `MAKE_FUNCTION`（函数定义）时，它们被错误地添加到 handler 的 `Successors` 中。

具体涉及两处代码：

**位置 A — RAISE_VARARGS fallthrough**（`BlockScanner.cs:222-228`）
```csharp
case Opcode.RAISE_VARARGS:
    block.Flags |= BlockFlags.Exit;
    ResolveIntermediateJumps(block, blocks, codeObj);
    // RAISE_VARARGS 仍需要顺序后继
    if (i + 1 < blocks.Count)
        AddSuccessor(block, blocks[i + 1]);  // ← 将下一个 block（可能是 class/func）链接为 handler 后继
    break;
```

**位置 B — ExceptionTable handler 边**（`BlockScanner.cs:308-327`）
```csharp
// 3.11+: ExceptionTable handler 边
for (int j = 0; j < blocks.Count; j++)
{
    if (blocks[j].StartOffset >= entry.StartOffset && blocks[j].EndOffset <= entry.EndOffset)
    {
        AddSuccessor(blocks[j], handlerBlock);  // ← 将 try 体内的所有 block 都链接 handler
    }
}
```

位置 A 是 3.10- 版本的主要问题源，位置 B 是 3.11+ 版本的问题源。

---

## 2. 解决方案

### 2.1 修复策略

不修改 CFG 结构本身（保持完整 CFG 供下游使用），而是在 **CFG 构建完成后、AST 构建前**，清理 handler 块的错误后继边。

#### 2.1.1 新增 `CleanHandlerSuccessors()` 方法

```csharp
/// <summary>
/// 清理 handler 块中错误连接到 class/func 定义的后继边。
/// 
/// 原理：
///   - class 定义以 LOAD_BUILD_CLASS 开头
///   - 函数定义以 MAKE_FUNCTION/MAKE_CLOSURE 开头（在栈上）
///   - 如果 handler 块的后继块是 class/func 定义 → 从 Successors 中移除
///   - 这些 class/func 定义应由模块级/函数级的 fallthrough 链路连接
/// 
/// 触发条件：
///   - handler 块的 successors 包含以 LOAD_BUILD_CLASS 开头的 block
///   - handler 块的 successors 包含以 MAKE_FUNCTION 开头的 block
///   - 被移除的 block 无其他 predecessor 时，连接到最近的公共前驱
/// </summary>
private static void CleanHandlerSuccessors(List<BasicBlock> blocks)
{
    // Step 1: 收集所有 handler 块（有 ExceptionHandler 标记或通过 ET 链接的块）
    var handlerSuccessors = new HashSet<BasicBlock>();
    
    foreach (var block in blocks)
    {
        // 检查 block 是否是 handler（被 ExceptionHandlers 引用 或 标记了 ExceptionHandler flag）
        bool isHandler = block.Flags.HasFlag(BlockFlags.ExceptionHandler);
        
        if (!isHandler) continue;
        
        // Step 2: 检查 handler 的后继块是否以 class/func 定义开头
        var successorsToRemove = new List<BasicBlock>();
        foreach (var succ in block.Successors)
        {
            if (IsClassOrFuncDefinition(succ))
            {
                successorsToRemove.Add(succ);
            }
        }
        
        // Step 3: 从 handler 中移除错误的后继边
        foreach (var succ in successorsToRemove)
        {
            block.Successors.Remove(succ);
            succ.Predecessors.Remove(block);
        }
    }
    
    // Step 4: 确保被移除的 class/func block 仍有连接（连接到相邻的前驱）
    // 如果 block 有 0 个 predecessor，连接到序号上前一个 block
    for (int i = 0; i < blocks.Count; i++)
    {
        if (blocks[i].Predecessors.Count == 0 && i > 0)
        {
            // 找到最近的有 successors 的 block
            for (int j = i - 1; j >= 0; j--)
            {
                if (blocks[j].Successors.Count > 0)
                {
                    AddSuccessor(blocks[j], blocks[i]);
                    break;
                }
            }
        }
    }
}

/// <summary>检测 block 是否为 class 或 function 定义的开头。</summary>
private static bool IsClassOrFuncDefinition(BasicBlock block)
{
    if (block.Instructions.Count == 0) return false;
    
    var firstOp = block.Instructions[0].Opcode;
    
    // class 定义: LOAD_BUILD_CLASS
    if (firstOp == Opcode.LOAD_BUILD_CLASS)
        return true;
    
    // 函数定义: 块以 LOAD_CONST(code_object) 开头后跟 MAKE_FUNCTION
    if (firstOp == Opcode.LOAD_CONST || firstOp == Opcode.LOAD_CLOSURE_313)
    {
        // 检查块中是否有 MAKE_FUNCTION / MAKE_CLOSURE
        return block.Instructions.Any(i =>
            i.Opcode == Opcode.MAKE_FUNCTION ||
            i.Opcode == Opcode.MAKE_CLOSURE_312 ||
            i.Opcode == Opcode.MAKE_CLOSURE_313);
    }
    
    return false;
}
```

### 2.2 集成点

在 `BlockScanner.Scan()` 的 `LinkBlocks` 之后、`MergeOrphanBlocks` 之前插入：

```csharp
public List<BasicBlock> Scan(CodeObject codeObj)
{
    var instructions = codeObj.Instructions;
    var leaders = MarkLeaders(instructions, codeObj.ExceptionTable, codeObj);
    var blocks = SplitAtLeaders(instructions, leaders);
    LinkBlocks(blocks, codeObj.ExceptionTable, codeObj);
    
    // Phase 9-01: 清理 handler 块错误连接的 class/func 定义
    CleanHandlerSuccessors(blocks);
    
    MergeOrphanBlocks(blocks);
    MarkBlockProperties(blocks);
    return blocks;
}
```

### 2.3 ExceptionTable 边修复（3.11+ 补充）

对于 3.11+ ExceptionTable，位置 B 的修复不同——不是移除 handler 边的 successors，而是限制 ET handler 边只连接到 try 体内具备**终端指令之前**的块：

```csharp
// 在 ExceptionTable handler 边的链接中加入 class/func 过滤
// 仅限 3.11+:
for (int j = 0; j < blocks.Count; j++)
{
    if (blocks[j].StartOffset >= entry.StartOffset
        && blocks[j].EndOffset <= entry.EndOffset
        && !IsClassOrFuncDefinition(blocks[j]))  // ← 新增过滤
    {
        // 只对非 class/func 定义的块添加 handler 边
        AddSuccessor(blocks[j], handlerBlock);
    }
    if (blocks[j].StartOffset > entry.EndOffset) break;
}
```

---

## 3. 预期效果

### 3.1 量化预期

| 指标 | 修复前 | 修复后 | 改善 |
|------|:------:|:------:|:----:|
| A+B 可接受输出 | 52 (4%) | **~72 (~5%)** | +20 文件 |
| abc.py D 类(count) | 11/11 | **~8/11**（3 个版本升级到 C） | 改善 |
| pprint.py | D | **C 或 B** | 改善 |
| 受影响的 handler 结构 | ~50 文件 | **~10 文件** | -40 文件 |
| 白盒通过率 | 299 | **300~302** | +1~3 |
| 总 diff lines | 146007 | **~144500** | -1500 |

### 3.2 具体文件改善

预计以下文件会明显改善：

| 文件 | 版本 | 当前 D 类原因 |
|:-----|:----:|:-------------|
| abc.py | 2.7~3.14 | class/def 在 try/except 后缩进错误 |
| pprint.py | 3.14 | 同 |
| functools.py | 3.8~3.14 | handler→class edge + decorator 链 |
| reprlib.py | 3.6~3.14 | try/except 后的 class 定义错位 |
| contextlib.py | 所有 | 同 |

---

## 4. 风险评估

### 4.1 退化风险

| # | 风险 | 概率 | 影响 | 缓解措施 |
|---|------|:----:|:----:|---------|
| 1 | 移除 handler 后继边后，被移除的 class/func block 成为孤儿块 | 🟡 中 | 中 | `MarkLeaders` 确保 class/func 有前驱，`MergeOrphanBlocks` 兜底 |
| 2 | false negative：将非 class/func 的 block 也清理了 | 🟢 低 | 高 | `IsClassOrFuncDefinition` 检查仅限 `LOAD_BUILD_CLASS` + `MAKE_FUNCTION` 组合 |
| 3 | false positive：真正的 handler→class 边被保留 | 🟢 低 | 低 | 影响有限，最多少改善几个文件 |
| 4 | 3.11+ ET 过滤影响正常的 handler 跳转 | 🟡 中 | 中 | 仅在非 class/func 块上添加 ET 边 |

### 4.2 回退条件

如果以下任一条件成立，立即回退该次改动：

1. 全量基线 `1325/1325` 被破坏（任一文件崩溃）
2. 白盒通过率下降超过 1%（≥3 个测试点）
3. 孤儿块从 0 增加到 >5

### 4.3 验收严苛要求

```
✅ dotnet build -c Release → 0 errors
✅ 全量基线 1325/1325 (100%)
✅ 白盒通过率 ≥ 299 (74%)
✅ 孤儿块 = 0
✅ abc.py + pprint.py + functools.py 的 handler→class 结构正确
✅ diff lines 减少至少 500（即结构改善可量化）
```

---

## 5. 实施步骤

1. 在 `BlockScanner.cs` 中新增 `CleanHandlerSuccessors()` + `IsClassOrFuncDefinition()` 方法
2. 修改 `Scan()` 调用流程，在 `LinkBlocks` 之后插入清理
3. 修改 `LinkBlocks()` 中 ExceptionTable 边添加过滤
4. `dotnet build` 验证编译
5. 运行全量基线 `python3 tools/baseline_evaluate_all.py` 对比退化
6. 运行白盒 `python3 test_data/whitebox_test.py` 对比通过率
7. 手动检查 abc.py 输出验证 handler→class 结构正确
8. 根据结果决定提交或回退
