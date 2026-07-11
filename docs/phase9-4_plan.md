# Phase 9-4 详细方案: 控制流重建 — if-else 分支分裂修复

> 目标: 修复 abc/enum/functools 等大文件中的控制流分裂问题
> 预期: 白盒 339→360+ (BARE_EXPR 58→35, SYNTAX 14→10)
> 难度: 🔴 困难 — 涉及 CFG 级 seq-block 结构重建

---

## 1. 问题精确定义

### 1.1 症状

```python
# abc.py update_abstractmethods 当前输出:
def update_abstractmethods(cls):
    if hasattr(cls, '__abstractmethods__'):
        return cls
        abstracts = set()                    # ← BARE: 应为 if-false 分支
        all_abstract_methods = ...           # ← BARE
        return cls                           # ← BARE
```

### 1.2 字节码结构

```asm
# abc.py update_abstractmethods (3.10 字节码示意)
LOAD_GLOBAL  hasattr
LOAD_FAST    cls
LOAD_ATTR    __abstractmethods__
CALL_FUNCTION 2
POP_JUMP_IF_FALSE  → L1          # if not hasattr → skip return
  LOAD_FAST  cls
  RETURN_VALUE                     # return cls (true branch)
L1:                                # false branch 起点
  ...                              # 设置 abstracts set
  ...
  LOAD_FAST  cls
  RETURN_VALUE                     # return cls (函数末尾)
```

### 1.3 当前处理路径

1. `BlockScanner` 将 `POP_JUMP_IF_FALSE` 后的 **fallthrough** (L1) 标记为独立 block
2. `SequentialBlockBuilder.MergeLinearChain` 会将 L1 与其后继块合并
3. `ParseIfElseStructure` 在 seq-block 层检测 if-else 结构
4. **关键问题**: 当 If 的 true-branch 以 `RETURN_VALUE` 结束时，false-branch 的 blocks 在 CFG 中形成独立链，seq-block 处理将其作为**函数体尾部**而非 if-else 分支

### 1.4 根因定位

`ParseIfElseStructure` 中 (AstBuilder.cs ~11260-11350):

```csharp
// 收集 true-branch body
var visited = new HashSet<int> { header.Id };
var worklist = new Queue<SequentialBlock>();
visited.Add(trueBranch.Id);
worklist.Enqueue(trueBranch);

while (worklist.Count > 0)
{
    var current = worklist.Dequeue();
    if (current == mergePoint) continue;
    bodyBlocks.Add(current);
    // ...
}
```

当 true-branch 以 `RETURN_VALUE` 终止时：
- `mergePoint` 是 true-branch 和 false-branch 的汇聚点
- 如果 true-branch 以 RETURN 结束，不存在汇聚点 → `mergePoint` 为 null
- bodyBlocks 收集了整个 true-branch 链（含 **false-branch 的 blocks**）
- **false-branch blocks 被错误纳入 true-branch body**

---

## 2. 修复方案

### 2.1 方案 A: 终端指令感知的 If 解析（推荐）

**原理**: 当 true-branch 以终端指令（RETURN_VALUE/RAISE_VARARGS）结束时，不再收集 false-branch 块为 body，而是建立完整的 if-else 结构。

**代码修改**: `ParseIfElseStructure` 方法 (AstBuilder.cs)

```csharp
// 修改前: 收集 trueBranch 的所有后继直到 mergePoint
while (worklist.Count > 0)
{
    var current = worklist.Dequeue();
    if (current == mergePoint) continue;
    bodyBlocks.Add(current);
    ...
}

// 修改后: 终端指令感知 — 如果 true-branch 以 RETURN/RAISE 结束，停止收集
while (worklist.Count > 0)
{
    var current = worklist.Dequeue();
    if (current == mergePoint) continue;
    
    // Phase 9-4: 检测 true-branch 是否以终端指令终止
    // 如果是，该分支不包含 false-branch 的 blocks
    if (IsTerminalBlock(current) && bodyBlocks.Count > 0)
    {
        // 已经收集了足够多的 true-branch blocks
        // 剩余的 worklist 条目是 false-branch 
        break;
    }
    
    bodyBlocks.Add(current);
    ...
}
```

同时新增 `IsTerminalBlock`:

```csharp
private static bool IsTerminalBlock(SequentialBlock block)
{
    if (block.Instructions.Count == 0) return false;
    var lastInstr = block.Instructions[^1];
    return lastInstr.Opcode == Opcode.RETURN_VALUE ||
           lastInstr.Opcode == Opcode.RETURN_GENERATOR_313 ||
           lastInstr.Opcode == Opcode.RETURN_CONST ||
           lastInstr.Opcode == Opcode.RETURN_CONST_313 ||
           lastInstr.Opcode == Opcode.RAISE_VARARGS ||
           JumpHelper.IsUnconditionalJump(lastInstr.Opcode);
}
```

### 2.2 方案 B: 后处理 — 死代码后恢复 If-Else（备选）

**原理**: 在 `CleanDeadCodeAfterReturn` 之后，扫描函数体检测 `Return`/`Raise` 后跟随非跳转语句的模式，将这些语句重构为 `If` 的 else 分支。

**代码**: 新增 `RecoverIfElseStructure` pass

```csharp
// 检测: Return(Raise) + ExprStmt/Assign → 用 If(not condition) 包裹
private static List<Stmt> RecoverIfElseStructure(List<Stmt> stmts)
{
    for (int i = 0; i < stmts.Count - 1; i++)
    {
        if ((stmts[i] is Return || stmts[i] is Raise) && 
            stmts[i + 1] is not Return and not Raise and not FunctionDef)
        {
            // 重构为 if-else
            // return → if not (previous condition):
            // 需要回溯找到决定这个 return/raise 的 if 条件
        }
    }
}
```

**缺点**: 需要回溯查找 if 条件，实现复杂且脆弱。

### 2.3 方案选择

**选择方案 A** — 从根源修复 `ParseIfElseStructure`，避免 false-branch blocks 被错误收集。

**原因**:
1. 修复点在控制流解析的核心路径，修改一次影响所有文件
2. 方案 A 比方案 B 更健壮（在 seq-block 层修复而非后处理层猜测）
3. 方案 B 需要回溯条件，在复杂控制流中可能误判

---

## 3. 实施步骤

### Step 1: 添加 `IsTerminalBlock` 工具方法

```csharp
// AstBuilder.cs, 工具方法区
private static bool IsTerminalBlock(SequentialBlock block) { ... }
private static bool IsSeqBlockTerminatedByJump(SequentialBlock block) { ... }
```

### Step 2: 修改 `ParseIfElseStructure` 的 true-branch BFS

```csharp
// lines ~11331-11350
// 在 BFS 循环中添加终端指令检测
if (IsTerminalBlock(current) && bodyBlocks.Count > 0)
    break; // 停止收集 false-branch 的 blocks
```

### Step 3: 验证 false-branch 的收集

```csharp
// 在终端指令检测后，剩余的 worklist 条目应作为 false-branch
if (mergePoint == null && bodyBlocks.Count > 0 && worklist.Count == 0)
{
    // 没有合并点 → 尝试从 CFG 中找 false-branch
    var falseBranchStart = FindSequenceBlockAfter(headers[0], seqBlocks);
    if (falseBranchStart != null)
        falseBranch = falseBranchStart;
}
```

### Step 4: 集成 `AnnotateConditionChains` 识别连续 if-elif

在 `ParseControlStructures` 前，对所有 IsConditionHeader 的 seqBlock 标注连续链，使 `ParseIfElseStructure` 能够正确识别 elif 链。

---

## 4. 风险评估

| 风险 | 概率 | 影响 | 缓解 |
|:-----|:----:|:----:|:------|
| 终端指令检测误判（非 if-else 的 RETURN） | 🟡 中 | 高 | 只在 true-branch 路径上检查 |
| false-branch block 错误排除 | 🟡 中 | 中 | 逐例回归检查 |
| 嵌套 if-else 处理复杂 | 🔴 高 | 高 | 先从简单情况开始（abc 单层 if） |
| elif 链处理 | 🟡 中 | 低 | 3.10+ 用 JUMP_IF_NOT_EXC_MATCH 区分 |

## 5. 验收指标

| 指标 | 修复前 | 预期 | 验证方式 |
|:-----|:------:|:----:|:---------|
| abc.py 各版本 BARE_EXPR | 15 | 5-8 | 白盒 BARE 计数 |
| enum.py BARE_EXPR | 15 | 8-10 | 白盒 BARE 计数 |
| functools.py BARE_EXPR | 12 | 6-8 | 白盒 BARE 计数 |
| 全量基线 | 1325/1325 | 1325/1325 | 基线脚本 |
| 孤儿块 | 0 | 0 | 基线脚本 |

## 6. 回退条件

1. 全量基线 <1325
2. 孤儿块 >5
3. 白盒通过率下降 >3%
