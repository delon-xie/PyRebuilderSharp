# Phase 9-2 迭代方案: 结构级问题修复

> 基线: 白盒 328/405 (81%), EMPTY_TRY=14, BARE_EXPR=68, SYNTAX=10, TNH=10, CLEANUP=7
> 目标: 白盒 350+ (86%)
> 地位: Phase 9 表达式级清理完成 → Phase 9-2 结构级修复

---

## 1. 剩余问题分类

```
白盒 328/405 — 剩余 77 个失败
═══════════════════════════════
BARE_EXPR      68  ─┬─ abc 控制流分裂       25
                    ├─ enum 大文件边界        15
                    ├─ reprlib try→class     15
                    ├─ comprehension 变量泄漏   8
                    └─ match 类型 + 其他       5

EMPTY_TRY       14  ─┬─ enum + else/finally    8
                     ├─ test_try_complex        2
                     └─ reprlib + 其他          4

SYNTAX_ERROR    10  ─┬─ enum 大文件截断        4
                     ├─ comprehension 3.5-3.7   3
                     ├─ l7_edge + test_cls2     2
                     └─ abc 3.5                 1

TRY_NO_HANDLER  10  ─┬─ abc 3.7-3.10           5
                     ├─ reprlib 3.11-3.12       2
                     └─ 其他                    3

CLEANUP_LEAK     7  ─┬─ abc 3.13-3.14          2
                     └─ enum/其他               5
```

## 2. 迭代路线图

| 迭代 | 内容 | 目标 | 影响场景 | 难度 | 白盒预期 |
|:----:|:-----|:----|:---------|:----:|:--------:|
| **9-2-01** | abc 控制流分裂修复 | BARE 68→45 | abc.py 各版本 | 🔴 难 | 328→335 |
| **9-2-02** | enum 大文件边界 | SYNTAX 10→6, EMPTY 14→10 | enum.py | 🔴 难 | 335→340 |
| **9-2-03** | handler preamble + TRY_NO 检测 | TNH 10→3 | abc+reprlib | 🟡 中 | 340→345 |
| **9-2-04** | comprehension 变量泄漏 | BARE 45→40 | test_comp 等 | 🟢 易 | 345→347 |
| **9-2-05** | reprlib try→class + 清理 | BARE 40→35 | reprlib | 🟡 中 | 347→350 |

## 3. 各迭代详情

### 9-2-01: abc 控制流分裂修复

**问题**：`abc.py` 中 `update_abstractmethods` 和 `_dump_registry` 函数在字节码级别包含 `if ...: return cls` 后的代码。Seq-block 构建时未将 return 后的代码分离为独立分支，导致：
```python
def update_abstractmethods(cls):
    if hasattr(cls, '__abstractmethods__'):
        return cls
        getattr(scls, ...)    # ← return 后不可达代码
        cls.__abstractmethods__ = frozenset(abstracts)
```

**修复**：在 `BuildWithSequentialBlocks()` 的 `PostProcessFunctionDefs` 中添加 `return` 后的**死代码消除**。检测 `return`/`raise` 后的不可达语句，移至新的 else 分支或删除。

**文件**：`AstBuilder.cs` — `PostProcessFunctionDefs` 或新增 `CleanDeadCodeAfterReturn`

### 9-2-02: enum 大文件边界修复

**问题**：`enum.py` (1500+ 行) 的 SYTNAX_ERROR 出现于行 1400-2000，EMPYY_TRY 出现于行 168-1330。大文件中 ExceptionTable Entry 的 EndOffset 可能在 block 边界处截断。

**修复**：在 `LinkBlocks` 或 `AnnotateExceptionTableBlocks` 中，对 enum-like 大文件（超过 200 块）的 ET 边界做放宽处理——如果 try body 的最后一个 block 位于 handler 入口之前，视为截断边界。

**文件**：`SequentialBlockBuilder.cs` — `AnnotateExceptionTableBlocks` 大文件处理

### 9-2-03: Handler preamble + TRY_NO_HANDLER

**问题**：10 例 TRY_NO_HANDLER 中 5 例是 abc 3.7-3.10 的 `try 块(行3)后缺少 except/finally`。这是因为 3.10- SETUP_FINALLY handler 的 POP_TOP×3 preamble 未被 `ParseTryStructure` 正确识别。

**修复**：在 `ParseTryStructure` 的 3.10- path 中，对 SETUP_FINALLY 目标块检测 preamble 指令（POP_TOP×3）+ `JUMP_FORWARD` 模式，正确分离 handler body。

**文件**：`AstBuilder.cs` — `ParseTryStructure` SETUP_FINALLY path

### 9-2-04: Comprehension 变量泄漏

**问题**：8 例 BARE_EXPR `x` 出现在 `test_comp` 2.7 和 3.12-3.14。3.12+ 中 `raise` 也出现。这些是 for-else 结构的 ELSE 分支中 comprehension 变量 `x` 泄漏。

**修复**：在 `CleanupBareExpr` 中，当检测到 `For` 语句的 Orelse 中包含 Name `x` 且 `x` 是 for-else 的 iter 变量时，删除该 Name。

**文件**：`AstBuilder.cs` — `CleanupBareExpr` 增强

### 9-2-05: reprlib try→class

**问题**：reprlib 各版本在 try/except 后的 class/function 定义中生成了 `pieces`、`trail` 等 BARE_EXPR。这可能是 9-01 handler→class edge 修复未覆盖的场景。

**修复**：检查 reprlib 输出的具体结构，确定是 handler→class edge 问题还是控制流分裂。如为前者，增强 `CleanHandlerSuccessors`。

**文件**：`BlockScanner.cs` / `AstBuilder.cs`

## 4. 风险登记

| 风险 | 迭代 | 概率 | 缓解 |
|:-----|:----:|:----:|:------|
| return 后死代码消除删除真实代码 | 9-2-01 | 🟡 中 | 只删 ExprStmt/Pass，不删 Assign/FunctionDef |
| 大文件 ET 边界放宽引入新 EMPTY_TRY | 9-2-02 | 🟢 低 | 逐例回归检查 |
| preamble 检测过于宽松 | 9-2-03 | 🟡 中 | 仅对 handler 入口块检测 |
| for-else 变量名误删 | 9-2-04 | 🟢 低 | 只删与 for target 同名的 Name |
