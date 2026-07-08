# Phase 7 Seq-Blocks 白盒测试评估报告

**日期**: 2026-07-09
**测试文件**: `test_data/whitebox_report_20260709_021000.md`
**测试套件**: `test_data/whitebox_test.py` — 405 用例 × 45 文件 × 11 版本

---

## 1. 总体评估

| 指标 | 数值 |
|------|------|
| 测试总数 | 405 |
| 跳过（无 pyc） | 123 |
| 通过 | **251 (61%)** |
| 失败 | **154 (38%)** |
| 问题类型数 | 10 种 |

### 版本通过率热力图

```
2.7     ████████████████████████░░░░ 66%  ← 较老版本表现好
3.5     ███████████████████████████░ 78%  ← 最佳
3.6     ████████████████████████░░░░ 73%
3.7     ████████████████████████░░░░ 73%
3.8     █████████████████████████░░░ 77%
3.9     █████████████████████████░░░ 77%
3.10    ████████████████████████░░░░ 70%
3.11    ████████████████████░░░░░░░░ 51%  ← 拐点（3.11+ 差异大）
3.12    █████████████████░░░░░░░░░░░ 44%
3.13    █████████████████░░░░░░░░░░░ 43%  ← 最差
3.14    █████████████████░░░░░░░░░░░ 42%  ← 最差
```

**趋势**: 2.7 到 3.10 稳定在 66-78%，3.11+ 急剧下降到 42-51%。这是 seq-blocks 对 3.11+ 的 ExceptionTable/新操作码处理不足的表现。

---

## 2. 问题分类深析

### P0 — RUNTIME_ERROR（55 次，致命）

**模式**: 所有 RUNTIME_ERROR 均出现在 `[SEQ_BUILD_HYBRID]` 或 `[SEQ_BUILD_FOR]` 日志上下文。

| 受影响文件 | 版本范围 | 错误上下文 |
|-----------|---------|-----------|
| `enum` | 3.6–3.14 | 17 次: SEQ_BUILD_HYBRID(11) + SEQ_BUILD_FOR(6) |
| `functools` | 3.8–3.14 | 14 次: SEQ_BUILD_HYBRID(10) + SEQ_BUILD_FOR(4) |
| `reprlib` | 3.11–3.13 | 5 次: SEQ_BUILD_HYBRID |
| `l8_complex` | 3.12, 3.14 | 2 次: SEQ_BUILD_FOR |
| `l9_ultimate` | 3.14 | 1 次: SEQ_BUILD_FOR |

**代表错误**:
```
[SEQ_BUILD_HYBRID] Stmt: Raise { Location = , Exc = Call { ... }, Cause =  }
[SEQ_BUILD_HYBRID] Stmt: ExprStmt { Location = , Value = ... }
```

**根因**: StackMachine 在处理 Raise/ExprStmt 语句时 Location 为空/异常。
- 在 `GenerateStatementsFromSeqBlockHybrid` 中，对有 ParentStructure 的 seqBlock，其 Statements 直接从缓存输出，但 Raise 语句的指令上下文（如异常类型/原因）在合并为 SequentialBlock 时跨块了
- SEQ_BUILD_FOR 错误：`BuildForLoopStructureStatements` 中 iterExpr 或 loopVar 提取失败导致 Raise 无法构建

### P0 — BARE_EXPR（113 次，最多发）

**模式**: 裸表达式，包括 `cls.__bases__`, `raise`, `return None`, `x` 等。

**根因**: 
1. StackMachine 输出中间表达式（如 Name 引用）但后继指令未消费
2. seq-blocks 模式缓存 Statements 后，在 `GenerateAstStatementsHybrid` 中这些未消费表达式直接进入输出
3. 控制结构 body 结束后，块的指令残留（如 `return None` / `raise`）作为独立表达式泄漏

**典型输出**（test_try_simple 3.14）:
```python
def test(flag):
    ...
    return None         # ✅ 正确
    e = None            # ❌ 清理代码泄漏
    raise               # ❌ 3 次裸 raise
    raise
    raise
```

### P1 — REDUNDANT_PASS（91 次）

**模式**: `pass` 语句过多（>3 次）。

**根因**:
1. 空控制结构 body 自动生成 pass，但 seqBlock 合并后 body 关系未正确识别 → 多余 pass
2. StackMachine 在无指令时生成 Pass() 且未被过滤
3. for/while 循环的 else body 在为空时也生成了 pass

**分布**:
- `l2_exception.3.12`: 28 pass（最严重）
- `l6_advanced`: 29-33 pass
- `loop_else`: 4-10 pass（各版本）
- `test_nested_comp`: 22-30 pass

### P1 — REDUNDANT_RAISE（27 次）

**模式**: 裸 raise 语句过多（>2）。

**根因**: handler 块的 `raise` 语句在 seq-blocks 中从 handler 区域泄漏到主 body。

**受影响**: test_try_simple(3), try_else(5), l2_exception(7), l6_advanced(10) 等。

### P2 — SYNTAX_ERROR（12 次）

| 错误 | 次数 | 根因 |
|------|------|------|
| `'yield from' outside function` | 3 | test_nested_comp 3.5/3.6/3.7 |
| `'return' with value in async generator` | 4 | test_async 3.11/3.13/3.14, l5_class 3.12 |
| `invalid syntax` | 2 | test_nested_comp 3.5/3.6/3.7, l7_edge 3.12 |

**根因**: comprehension 的 yield 未被识别为 generator；async generator vs async function 的 co_flags 分类在 seq-blocks 中丢失。

### P2 — ELSE_CONTAINS_FINALLY（11 次）

try 的 else 块包含了 finally 的代码（`print('finally')`）。

### P3 — CLEANUP_LEAK（5 次）

`e = None` 清理代码泄漏到输出中。

---

## 3. 问题优先级矩阵

| 优先级 | 问题 | 次数 | 影响面 | 修复难度 | 目标版本 |
|--------|------|------|--------|----------|---------|
| **P0** | RUNTIME_ERROR | 55 | 阻断 enum/functools/reprlib 等 5 个标准库 | ⚠️ 中 | 3.11+ seq-blocks |
| **P0** | BARE_EXPR | 113 | 几乎所有文件的质量 | ⚠️ 中 | 全版本 |
| **P1** | REDUNDANT_PASS | 91 | 美观 + ast.parse 通过 | ✅ 低 | 全版本 |
| **P1** | REDUNDANT_RAISE | 27 | 结构完整性 | ⚠️ 中 | 全版本 |
| **P2** | SYNTAX_ERROR | 12 | ast.parse 失败 | ⚠️ 中 | 特定版本 |
| **P2** | ELSE_CONTAINS_FINALLY | 11 | try 结构准确性 | ⚠️ 高 | 全版本 |
| **P3** | CLEANUP_LEAK | 5 | 代码质量 | ✅ 低 | 全版本 |
| **P3** | EMPTY_TRY | 5 | try 结构准确性 | ⚠️ 高 | 全版本 |
