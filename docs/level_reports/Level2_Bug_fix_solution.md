# Level 2 问题分析与修改方案

> Level 2：异常与上下文管理（try/except/finally, with）
> Baseline: 45 tests (5 files × 9 versions), 0 A/B/C across most versions

---

## 问题总览

| # | 问题 | 严重度 | 影响范围 | 修复难度 |
|:-:|:-----|:------:|:--------:|:--------:|
| 1 | **try/except 体完全塌陷为顺序代码** | **P0** | l2_2, l2_3, l2_4, l2_10, l2_11, l2_13, l2_14 在 3.8-3.14 | 🔴 |
| 2 | 嵌套 try/except 的 handler 体错误 | P1 | l2_6, l2_12 | 🟡 |
| 3 | `finally` 体注入多余的 `raise` | P1 | l2_1, l2_8 (3.10) | 🟢 |
| 4 | `def` → `class` 误判 | P1 | test_try_complex test3 (3.10) | 🟢 |
| 5 | with 语句体出现在 `return` 之后（死代码） | P1 | l2_9 | 🟢 |
| 6 | with 语句 `lock` 独立表达式 | P2 | test_with.py, l2_9 | 🟢 |
| 7 | 3.14 中 `pass` 前缀 | P2 | 所有函数 | 🟢 |
| 8 | with 语句在 3.14 中完全崩溃 | P2 | l2_9_3.14, test_with_3.14 | 🟡 |

---

## 问题 1：try/except 体完全塌陷（P0 — 最严重）

### 现象

```python
# 原始
def l2_2_try_except_single():
    try:
        x = 1 / 0
    except ValueError:
        x = 0
    return x

# 反编译（所有版本）
def l2_2_try_except_single():
    x = 1 / 0
    return x
```

try/except 的两个分支都塌陷为顺序代码——视为 PlainCode 而非控制结构。

### 根因

`IsTrySetupOpcode`（~L2910）对 `SETUP_FINALLY` 的检测是跨版本有效的（opcode 122 从 2.7 保留到 3.10），但对 `BUILD_EXCEPTION_HANDLER`（3.11+ 的 try 设置指令）和其他异常设置指令的覆盖不全。

具体路径：
1. `BuildStatementsInternal` / `GetStructuredBlockStmts` 调用 `BuildTryFromBlock`
2. `BuildTryFromBlock` 查找 `SETUP_FINALLY` / `SETUP_EXCEPT`
3. 对于 3.8-3.10：找到 `SETUP_FINALLY`，但 handler 识别失败（因为 handler 块以 `JUMP_IF_NOT_EXC_MATCH` 开头，不是旧式的异常匹配模式）
4. 对于 3.11+：`BuildTryFromExceptionTable` 被调用，但如果 handler 块无法通过 `GetStructuredBlockStmts` 正确处理，仍会返回 null

`BuildTryFromBlock` 的 handler 提取逻辑（~L3700-3774）依赖于：
- handler 块以 `JUMP_IF_NOT_EXC_MATCH` + `handler_offset` 或以 `DUP_TOP` + `LOAD_GLOBAL ValueError` 模式开始
- 对于 3.10 wordcode，handler 块的跳转偏移计算与 2-字节指令版本不同

### 修改方案

需要重构 `BuildTryFromBlock` 的 handler 识别逻辑：

```
1. 扩大 IsTrySetupOpcode 的覆盖范围（新增 3.8-3.10 的兼容路径）
2. 修复 handler 块识别：从 SETUP_FINALLY 的异常处理跳转目标回溯
3. 对于 3.11+：确保 BuildTryFromExceptionTable 正确处理函数级 try
```

修改点：
- `AstBuilder.cs` `BuildTryFromBlock`（~L3786-3780）
- `IsTrySetupOpcode`（~L2910-2925）
- 可能需要新增 `PycReader` 中对 3.8-3.10 异常块的预处理

---

## 问题 2：finally 体注入多余的 `raise`（P1 — 可快速修复）

### 现象

```python
# 反编译（3.10）
def l2_1_try_finally():
    try:
        x = 1
    finally:
        x = 2
        raise       # ← 多余的 raise
    x = 2
    return x
```

### 根因

`BuildTryFromBlock` 在处理完 finally 体后，从 `POP_BLOCK` 的后继块提取了 `RAISE_VARARGS` / `RERAISE` 指令作为 finally 体的一部分。`RERAISE` 是运行时 finally 块的正常结束方式（CPython 在 finally 块尾部插入 `RERAISE` 以保证异常继续传播）。

在 `BuildTryFromBlock` ~L3748-3774 的 handler 构建中，`handlerBody` 的提取包括了 `RERAISE` 指令。从 `BlockDecompiler` 的角度，`RERAISE` 可能是作为一个 `Raise()` 语句产生。

### 修改方案

在 finally 构建的最后一步，过滤掉 `Raise()` 无参数的语句（`RERAISE` / `RAISE_VARARGS 0` 对应的 AST 节点）：

```csharp
// BuildTryFromBlock 中，在构建 Handler 前：
handlerBody = handlerBody
    .Where(s => !(s is Raise r && r.Exc == null && r.Cause == null))
    .ToList();
```

---

## 问题 3：`def` → `class` 误判（P1 — 已在 Level1 修复，Level2 遗漏）

### 现象

```python
# 3.10 反编译
class test3:        # ← def test3()
    pass
```

### 根因

与 Level1 的 l1_6 相同：`PostProcessFunctionDefs` 中将带有内联推导式模式（`LIST_APPEND_313`）的 `Assign` 序列误判为类定义。Level1 已通过 `TryDetectInlinedComprehension` 约束修复，但 Level2 的 `test_try_complex.py` 中 test2 的 for 循环体 `pass` 触发了不同的推导式误判路径。

### 修改方案

同 Level1 修复方案（`docs/Level1_Bug_fix_solution.md` 问题 1），扩展约束条件：body 中不含 `INPLACE_*` / `CALL_FUNCTION` 等非推导式指令。

---

## 问题 4：with 语句体出现在 return 之后（P1 — 死代码模式）

### 现象

```python
# 反编译（3.6/3.10）
def l2_9_with_statement():
    ...
    fp = ContextManager()
    result = fp
    return result
    with ContextManager() as fp:    # ← 死代码，不可达
        result = fp
```

### 根因

`BuildTryFromBlock` 或 `GetStructuredBlockStmts` 在处理 `SETUP_WITH` 块时，with 体的提取失败。`SETUP_WITH` 在 3.6-3.10 中是独立的 try-setup 指令，`BuildWithFromBlock`（~L4515）需要找到 `WITH_EXCEPT_START` / `POP_BLOCK` 的范围。

当 `BuildWithFromBlock` 返回 null（识别失败）时，块退化到 `BuildStatementsInternal` 的平坦路径。`SETUP_WITH` 指令不被识别，其后的代码包括 with 体和 __exit__ 设置代码被混在一起。

### 修改方案

增强 `BuildWithFromBlock` 对 3.10 wordcode 的兼容性：检查 `SETUP_WITH` 跳转参数后使用 `ResolveJumpTarget` 计算 handler 地址（而非硬编码偏移）。

---

## 问题 5：with 语句 `lock` 独立表达式（P2）

### 现象

```python
# 反编译（3.6/3.10）
lock = object()
lock                    # ← 独立表达式
print('hello')
with lock:
    print('hello')
```

### 根因

`BuildWithFromBlock` 中，`SETUP_WITH` 前的 `LOAD_GLOBAL lock` 或 `LOAD_FAST lock` 被 `BlockDecompiler` 处理为独立的 `ExprStmt(lock)`。与 Level1 的 `range(10)` 孤立表达式属于同一类问题。

`MarkForLoopPredecessors` 在 for 循环中已有修复，但 with 语句中没有等价机制来标记前导表达式为已消费。

### 修改方案

与 Level1 的 GET_ITER 前导块修复类似：在处理 `SETUP_WITH` 块时，提取 `SETUP_WITH` 之前的 LOAD 指令（with 上下文管理器表达式），将其标记为已消费（visited），避免产生独立表达式。

---

## 问题 6：3.14 中 `pass` 前缀（P2）

### 现象

```python
# 反编译（3.14）
def l2_2_try_except_single():
    pass              # ← 每个函数前都有 pass
    x = 1 / 0
    return x
    x = 0             # ← handler 体残留
```

### 根因

3.14 的 `RESUME` (opcode 151) 指令在函数入口生成。`RESUME` 被 `BlockDecompiler` 跳过不做处理，但产生了空的头块（起始偏移=函数入口）。`BuildBlockOnly` 处理空块时产生了 `Pass()` 语句。

`x = 0` 残留在 return 之后（问题 1 + 问题 4 的叠加——handler 体未被 Try 结构包裹，作为顺序代码出现在 return 之后）。

### 修改方案

在 `BlockDecompiler` 或 `BuildBlockOnly` 中，跳过 `RESUME` 指令产生的空指令块：

```csharp
// BuildBlockOnly 中，如果块只有 RESUME 指令，返回空列表
if (block.Instructions.Count == 1 && block.Instructions[0].Opcode == Opcode.RESUME)
    return new List<Stmt>();
```

---

## 可立即修复的问题（截止今日）

| 优先级 | 问题 | 预计收益 | 工时 | 文件/行号 |
|:------:|:-----|:---------|:----:|:---------|
| P1 | 问题 2：finally 多余 `raise` | 2 个文件提升 | 0.5h | `AstBuilder.cs` BuildTryFromBlock handler |
| P1 | 问题 4：with 体死代码（简化版） | 1 个文件修复 | 1h | `BuildWithFromBlock` or with-after-return filter |
| P1 | 问题 3：def→class（复用 Level1 修复） | 1 个文件修复 | 0.5h | 与 Level1 相同约束 |
| P2 | 问题 5：with `lock` 独立表达式 | 2 个文件改进 | 1h | `BuildWithFromBlock` 前导表达式消费 |
| P2 | 问题 6：3.14 `pass` 前缀 | 所有 3.14 文件 | 0.5h | `BuildBlockOnly` RESUME 过滤 |
| 🔴 | **问题 1：try/except 塌陷** | **6 个文件核心修复** | **4h+** | `BuildTryFromBlock` + handler 识别 |
