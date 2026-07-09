# Batch A — EMPTY_TRY body 范围修复方案规划

---

## 1. 现状分析

### 1.1 问题定义

白盒测试报告显示 **EMPTY_TRY = 51**，**TRY_NO_HANDLER = 45**，合计 **96** 个 try 结构异常。核心表现：

```
# 反编译输出:
try:
    pass                    ← ❌ body 应该是实际的函数语句
except ValueError as e:
    print(e)                ← ✅ handler 正确
```

以及：

```
# 多出一个空的 try:
try:
    x = 1
except:
    ...                      ← handler 包含了 try body 语句
try:
    pass                     ← ❌ 多余的 try
except:
    pass
```

### 1.2 三个独立但耦合的根因

| # | 根因 | 影响数量 | 影响版本 | 代码位置 |
|---|------|---------|---------|---------|
| A | 2 个 try 结构（源文件 1 个 try） — **Phase 2/5 过度链接** | ~30 | 3.10-  | `SequentialBlockBuilder.AnnotateExceptionTableBlocks` + `ParseControlStructures` |
| B | handler body 范围包含 try body 语句 — **preamble 检测缺失** | ~25 | 3.10-（SETUP_FINALLY） | `BuildTryStructureStatements` 行 12207-12231 |
| C | ET 路径 body range 边界不匹配 — **overlap 检查不精准** | ~20 | 3.11+（ExceptionTable） | `ParseTryStructure` 行 11148-11170 |

### 1.3 根因 A: 过度链接

**现象**：`try_else.3.10` 中，每个 def 函数生成 2 个 try 结构但源文件只有 1 个。

**根因**：`AnnotateExceptionTableBlocks`（Phase 2）为每个 `ExceptionTableEntries` 中 Depth==0 的条目设置 `IsTryHeader = true`。然后 Phase 5 遍历所有 `IsTryHeader` 的 seqBlock 并调用 `ParseTryStructure`。但有些 ET 条目对应的 seqBlock 是**前一个 try 的 handler 内部**的嵌套结构——它应该被前一个 try 的 visited 集排除掉，而不是被独立链接。

**具体问题**：
- Handler 的 seqBlock 也被标注了 `IsTryHeader = true`（因为 handler 内部也有 ET 条目）
- 前一个 try 的 `visited` 集排除了 handler 内部的块，但第 2 个 Try 结构被创建时这些块已在 visited 中 → 空 body + 空 handler

**修复方向**：
- Phase 2c 中，`IsFinallyBlock`/`IsTryElseBlock` 标注应反向清除 `IsTryHeader`（handler 内的块不是 try header）
- 或 Phase 5 中，跳过已在 visited 中的块（已实现，但 visited 没有包括 handler 内部的嵌套结构）

### 1.4 根因 B: 3.10- 缺乏 POP_TOP preamble 检测

**现象**：`try_else.3.10` 中 handler 体包含 try body 的语句（`handler_body = [try_body_stmt, handler_body_stmt]`）。

**根因**：`BuildTryStructureStatements` 的 handler preamble 检测只处理 `CHECK_EXC_MATCH`（3.11+）。对于 3.10- SETUP_FINALLY 模式，handler 前导码是 `POP_TOP × 3` 序列：

```
# 3.10- handler preamble (SETUP_FINALLY):
POP_TOP        ← exception class
POP_TOP        ← exception instance
POP_TOP        ← traceback
[POP_TOP]      ← bare except 多一个（跳过匹配类型）
[STORE_FAST e] ← named except: e = exc_value

# 3.11+ handler preamble (ExceptionTable):
PUSH_EXC_INFO / PUSH_EXC_INFO_312
CHECK_EXC_MATCH / CHECK_EG_MATCH
POP_JUMP_IF_FALSE → next handler
COPY / STORE_FAST e (if named)
```

旧的 preamble 检测代码只看了 3.11+ 的 `CHECK_EXC_MATCH`。没有它时 `bodyStartIdx = 0`，整个 seqBlock 的指令都被当成了 handler body。

**修复方向**：添加 POP_TOP-based preamble 检测。

### 1.5 根因 C: 3.11+ body range 边界

**现象**：3.11+ 的 try 结构创建了空 body。

**根因**：`ParseTryStructure` 行 11148-11170 的 body block 收集使用 overlap 检查：
```csharp
if (seqBlock.EndOffset > tryStartOffset && seqBlock.StartOffset < tryEndOffset)
```

但 `tryEndOffset` 来自 `primaryExceptEntry.EndOffset`（ExceptionTable 条目的 body 范围结束）。对于嵌套 try，内部 try 的 EndOffset 可能小于外部 try 的 body 范围，导致 body blocks 收集覆盖不足或超出。

**修复方向**：
- body 范围限制为 `tryStartOffset` 到第一个 handler 的 StartOffset
- 使用 overlap 检查 + body 范围限制

---

## 2. 修复方案

### 2.1 方案 A: 防止过度链接（影响~30个问题）

**文件**: `SequentialBlockBuilder.cs` — `AnnotateExceptionTableBlocks`
**改动**: 标记 handler seqBlock 时，清除其内部的 `IsTryHeader`

```csharp
foreach (var tryHeader in seqBlocks.Where(b => b.IsTryHeader))
{
    // 找到此 try 的所有 handler seqBlock
    foreach (var et in tryHeader.ExceptionTableEntries)
    {
        if (!et.IsExcept && !et.IsFinally) continue;
        var handlerBlock = FindSeqBlockByOffset(seqBlocks, et.TargetOffset);
        if (handlerBlock == null) continue;
        
        // 清除 handler 块本身的 IsTryHeader（防止被当做新的 try）
        handlerBlock.IsTryHeader = false;
        
        // 清除 handler 块内所有嵌套的 IsTryHeader
        foreach (var nestedBlock in seqBlocks)
        {
            if (nestedBlock.StartOffset >= handlerBlock.StartOffset &&
                nestedBlock.EndOffset <= handlerBlock.EndOffset)
            {
                nestedBlock.IsTryHeader = false;
            }
        }
    }
}
```

**负影响分析**:
- ⚠️ 如果 handler 内部确实有嵌套 try（例如 `except: try: ... except: ...`），会错误清除内层 try 的标注
- ⚠️ 但 Phase 5 的 visited 集会在外层的 handler 被标记后跳过内层 try
- ✅ 实际影响小，因为嵌套 try 在 handler 内的场景会通过 body 反编译自动处理

### 2.2 方案 B: 3.10- POP_TOP preamble 检测（影响~25个问题）

**文件**: `AstBuilder.cs` — `BuildTryStructureStatements`
**改动**: 在现有 `CHECK_EXC_MATCH` 检测之前，添加 POP_TOP 序列检测

```csharp
int bodyStartIdx = 0;
bool seenCheckExcMatch = false;
// 先检查是否是 SETUP_FINALLY 模式（3.10-）的 POP_TOP preamble
bool isPopBasedPreamble = handlerInstrs.Count >= 3 &&
    handlerInstrs[0].Opcode == Opcode.POP_TOP &&
    handlerInstrs[1].Opcode == Opcode.POP_TOP &&
    handlerInstrs[2].Opcode == Opcode.POP_TOP;

if (isPopBasedPreamble)
{
    // POP_TOP×3 (exc_class, exc_value, traceback)
    // 可选: POP_TOP (bare except)
    // 可选: STORE_FAST (named except)
    bodyStartIdx = 3; // 跳过 POP_TOP×3
    if (bodyStartIdx < handlerInstrs.Count && 
        handlerInstrs[bodyStartIdx].Opcode == Opcode.POP_TOP)
        bodyStartIdx++; // bare except
    if (bodyStartIdx < handlerInstrs.Count &&
        handlerInstrs[bodyStartIdx].Opcode == Opcode.STORE_FAST)
        bodyStartIdx++; // named except
}
else
{
    // 3.11+ CHECK_EXC_MATCH 检测（原有逻辑）
    for (int i = 0; i < handlerInstrs.Count; i++)
    {
        // ... 原有代码 ...
    }
}
```

**负影响分析**:
- ⚠️ POP_TOP 序列的判断可能误判（恰好 3 个连续 POP_TOP 的非 preamble 场景）
- ✅ 但 SETUP_FINALLY 的 handler 入口是固定的进入点，3 个 POP_TOP 一定是 exception 对象/值/traceback 的清理
- ✅ 如果误判导致 bodyStartIdx 跳过实际 body 语句，测试会立即发现（丢失语句 vs 当前多包含语句）
- ✅ 当前问题更严重（多包含语句）

### 2.3 方案 C: 3.11+ body range 边界（影响~20个问题）

**文件**: `AstBuilder.cs` — `ParseTryStructure`
**改动**: 在 ET 路径 body 收集后，验证 body blocks 是否都在 `tryStartOffset` 和第一个 handler 之间，超出的裁剪。

```csharp
// ET 路径 body 收集后添加验证
if (bodyBlocks.Count > 0 && exceptHandlers.Count > 0)
{
    int firstHandlerStart = exceptHandlers.Min(h => h.Handler.StartOffset);
    bodyBlocks.RemoveAll(b => b.StartOffset >= firstHandlerStart);
}
```

**负影响分析**:
- ⚠️ 如果 handler 在 try body 中插入了一些指令（如异常传播跳板），会被错误移除
- ✅ 异常传播代码不会生成实际的 AST 语句，移除后不影响
- ✅ 结合方案 A 可大幅减少空 body

---

## 3. 执行顺序与预期收益

| 步骤 | 方案 | 文件 | 预期降幅 | 风险 |
|------|------|------|---------|------|
| 1 | A: 防止过度链接 | `SequentialBlockBuilder.cs` | EMPTY_TRY -15, TRY_NO_HANDLER -10 | 低 |
| 2 | B: POP_TOP preamble | `AstBuilder.cs` | EMPTY_TRY -10, TRY_NO_HANDLER -15 | 中 |
| 3 | C: body range 边界 | `AstBuilder.cs` | EMPTY_TRY -10 | 低 |
| **合计** | | | **EMPTY_TRY 51→16, TRY_NO_HANDLER 45→20** | |

### 总体预期

通过率: **287/405 (70%) → ~317/405 (78%)** (+30)

### 回滚条件

如果在任意步骤后测试通过率下降超过 3%，立即 revert 该步骤的修改：
- `git diff` 查看改了什么
- `git checkout -- <file>` 回滚指定文件
- 重新 `dotnet build -c Release` 验证

---

## 4. 关键检查点

每个步骤完成后必须验证：

1. **`dotnet build -c Release`** — 0 错误
2. **`python3 test_data/whitebox_test.py`** — 通过率不下降超过 3%
3. **检查 `test_try_simple.3.10` 和 `test_try_complex.3.10` 的输出** — try body 非空
4. **检查 `try_else.3.10`** — 每个函数只有 1 个 try，handler body 不含 try body 语句
5. **检查 `enum.3.10`** — 没有批量上空 try
