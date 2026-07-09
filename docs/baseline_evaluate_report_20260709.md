# PyRebuilderSharp 基线评估与修复计划（2026-07-09）

---

## 1. 总体状态

| 测试类型 | 指标 | 数值 |
|----------|------|------|
| **全量基线** | 反编译成功率 | **1325/1325 (100%)** ✅ |
| | 运行时崩溃 | **0** ✅ |
| | 孤儿块 | **0** ✅ |
| | A+B 可接受 | 52 (4%) |
| | 总 diff 行 | 153,130 |
| **白盒测试** | 通过率 | **287/405 (70%)** |
| | 失败 | 118 (29%) |

---

## 2. 问题分类 — 按优先级排序

| 优先级 | 问题 | 数量 | 占比 | 影响文件 | 核心根因 |
|--------|------|------|------|---------|---------|
| **P0** | EMPTY_TRY | **51** | 16% | enum, functools, reprlib, try_else, test_try_complex | ParseTryStructure 的 body block 收集范围不正确; header 含 try 前代码时 body 为空 |
| **P0** | TRY_NO_HANDLER | **45** | 14% | abc, functools, reprlib | ExceptionTable handler 解析失败，产生无 except/finally 的 try |
| **P1** | BARE_EXPR | **83** | 26% | abc, enum, functools, reprlib, comp, match | 中间表达式（comprehension 变量、class 属性、handler 变量）泄漏 |
| **P2** | SYNTAX_ERROR | **14** | 4% | enum, test_nested_comp, test_simple_comp, l5_class, l7_edge | 3.5-3.7 comprehension 差异、大文件边界、yield from 标记 |
| **P2** | ELSE_CONTAINS_FINALLY | **11** | 3% | test_try_simple（全版本） | 测试脚本伪阳性（else 块代码被判定含 finally） |
| **P3** | REDUNDANT_PASS | **35** | 11% | enum, functools, reprlib | 空函数体 pass 堆积（多为合法的空抽象方法） |
| **P3** | REDUNDANT_RETURN | **21** | 7% | enum, functools, l7_edge, l8 | return None 去重不完全 |
| **P3** | REDUNDANT_RAISE | **14** | 4% | enum, functools, l6, l8, test_comp | handler 的 RERAISE 未完全过滤 |
| **P3** | CLEANUP_LEAK | **8** | 3% | abc, enum, functools, l9 | `e = None` 清理语句泄漏 |
| **P4** | FORMAT_ERROR | **3** | 1% | reprlib 3.11/3.12/3.14 | f-string 双花括号转义 |

---

## 3. 优先级排序说明

### 影响面 > 控制块异常 > 指令缺失 > 孤儿块 > 语法错误

### P0: 影响面最大 + 控制块异常

**EMPTY_TRY (51)** 是当前最核心的结构性问题。直接影响 enum、functools、reprlib、try_else 等 4+ 目标文件，跨越 3.6~3.14 版本。try 体为空 ⇒ 缺失整个 try/except 逻辑 ⇒ 控制流错误。

**TRY_NO_HANDLER (45)** 是 EMPTY_TRY 的孪生问题。try 解析到了 header 和 body 但 handler（except/finally）没找到。两个问题合起来 **96 个**基本影响同一个根因：`ParseTryStructure` 的 handler 范围计算和 body 收集。

### P1: BARE_EXPR

虽然数量最大（83），但很多是 comprehension/class 类的模式问题，修复影响面广泛但预期提升幅度不高（每个模式只影响 2-3 个文件）。

### P2: SYNTAX_ERROR + ELSE_CONTAINS

语法错误直接导致生成的 Python 不可用，但数量少（14）。ELSE_CONTAINS 主要是测试脚本的伪阳性。

### P3: 后处理过滤

REDUNDANT/CLEANUP 系列已大幅改进（从初始的 91+27+7+23 → 35+14+21+8），剩余多为合法空体或边界 case。

---

## 4. 建议修复顺序

### Batch A: try/except 深度修复（预期 +30 通过）

| 批次 | 问题 | 方法 | 预期 |
|------|------|------|------|
| A1 | EMPTY_TRY body 范围 | 修正 `BuildTryStructureStatements` body 收集: header 合入 body, overlap 检查 | -15 |
| A2 | TRY_NO_HANDLER handler 解析 | `ParseTryStructure` 中 handler 块识别: PUSH_EXC_INFO→CHECK_EXC_MATCH→POP_EXCEPT 链追踪 | -20 |
| A3 | ELSE_CONTAINS_FINALLY 伪阳性 | 检查 test_try_simple 的 else body 归属 | -11 |

### Batch B: BARE_EXPR 子模式修复（预期 +15 通过）

| 子模式 | 文件 | 方法 |
|--------|------|------|
| Comprehension `x`/`row` | test_comp, test_nested_comp, test_simple_comp | `IsForIterBody`/`ForIterExitTarget` 标注 → 后处理过滤 |
| Class body `cls.__bases__` | abc | ClassDef 后检查漏网表达式 |
| Match `int`/`str` | match_full, match_simple | match pattern 变量清理 |

### Batch C: SYNTAX_ERROR（预期 +8 通过）

| 文件 | 原因 | 方法 |
|------|------|------|
| test_nested_comp 3.5-3.7 | Comprehension 编译差异 | 检查 pyc 编译路径 |
| enum 3.11-3.14 | 大文件 seq-block 边界 | 修正 body range |
| l5_class 3.12 | `yield from` outside function | comprehension 标记传递 |

---

## 5. 预期路线图

```
当前: 287 (70%), A+B=52 (4%)
  │
  ├─ A1: EMPTY_TRY body → 302 (74%), A+B ~60 (~5%)
  ├─ A2: TRY_NO_HANDLER → 322 (79%)
  ├─ A3: ELSE_CONTAINS → 323 (79%) 
  ├─ B: BARE_EXPR → 338 (83%)
  ├─ C: SYNTAX_ERROR → 346 (85%)
  └─ P3 后处理 → 350 (86%)
```

**建议下一步**: **Batch A1 — EMPTY_TRY body 范围修复**。这是 51 个问题的核心瓶颈，修复后直接辐射 A2（TRY_NO_HANDLER）和 A3，合计预期 +30 通过。
