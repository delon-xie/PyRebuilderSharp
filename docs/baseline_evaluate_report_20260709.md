# PyRebuilderSharp 基线评估报告

**日期**: 2026-07-09  
**测试工具**: `test_data/whitebox_test.py`  
**反编译模式**: `--seq-blocks`  
**测试套件**: 45 个测试文件 × 11 版本 = 495 用例（123 跳过无 pyc，实际 405）  

---

## 1. 总体统计

| 指标 | 数值 |
|------|------|
| 测试用例总数 | 405 |
| 跳过(无 pyc) | 123 |
| **通过** | **286 (70%)** |
| **失败** | **119 (29%)** |

---

## 2. 各版本通过率

| 版本 | 通过 | 失败 | 通过率 |
|------|------|------|--------|
| 2.7 | 21 | 9 | 70% |
| 3.5 | 24 | 8 | 75% |
| 3.6 | 25 | 9 | 73% |
| 3.7 | 25 | 9 | 73% |
| 3.8 | 29 | 6 | **82%** |
| 3.9 | 29 | 6 | **82%** |
| 3.10 | 29 | 8 | 78% |
| 3.11 | 21 | 16 | 56% |
| 3.12 | 28 | 19 | 59% |
| 3.13 | 24 | 13 | 64% |
| 3.14 | 31 | 16 | 65% |

**趋势**: 2.7-3.10 稳定在 70-82%，3.11+ 下降到 56-65%。3.11 的 ExceptionTable + 新操作码是主要瓶颈。

---

## 3. 问题分类统计

| 问题类型 | 数量 | 占比 |
|----------|------|------|
| BARE_EXPR | 92 | 28.7% |
| REDUNDANT_PASS | 31 | 9.7% |
| CLEANUP_LEAK | 23 | 7.2% |
| REDUNDANT_RETURN | 22 | 6.9% |
| EMPTY_TRY | 14 | 4.4% |
| REDUNDANT_RAISE | 14 | 4.4% |
| SYNTAX_ERROR | 14 | 4.4% |
| ELSE_CONTAINS_FINALLY | 11 | 3.4% |
| FORMAT_ERROR | 3 | 0.9% |

---

## 4. 问题优先级分析

### P0 — 影响面大（BARE_EXPR + CLEANUP_LEAK）

#### BARE_EXPR (92, 占失败 28%)

| 子模式 | 次数 | 受影响文件 | 根因 |
|--------|------|-----------|------|
| `cls.__bases__` / `cls.__dict__` 等 | ~20 | abc (2.7-3.14) | 类装饰器/基类操作中间表达式泄漏 |
| `abstracts.add(name)` | ~10 | abc | 抽象方法注册表达式泄漏 |
| `repr_running.add(key)` / `.discard(key)` | ~10 | reprlib (3.6-3.14) | 递归检测装饰器 body 泄漏 |
| `x` / `row` | ~15 | test_comp, test_nested_comp, test_simple_comp | Comprehension 生成器变量泄漏 |
| `return` / `raise` / `None` | ~15 | enum, functools, test_comp | 后终端 handler 泄漏 |
| `int` / `str` | ~8 | match_full, match_simple | Match pattern 变量泄漏 |
| `StopIteration` | ~5 | functools | Iterator 停止表达式泄漏 |
| `name.startswith(pattern)` / `number` | ~5 | enum | 成员检查表达式泄漏 |
| `functools.WRAPPER_ASSIGNMENTS` | ~5 | functools | wrapper 属性表达式泄漏 |

**根因**: StackMachine 输出中间表达式（如 `LOAD_ATTR cls.__bases__`）作为 `ExprStmt`，seq-blocks 在 Phase 1 缓存了这些语句，Phase 3c 直接输出无法被上层控制结构消费。

#### CLEANUP_LEAK (23, 占失败 7%)

| 次数 | 受影响文件 | 详情 |
|------|-----------|------|
| 3-30 | enum | `e = None` 清理语句 |
| 4-19 | functools | `e = None` 清理语句 |
| 2 | reprlib | `e = None` 清理语句 |
| 3-8 | l9_ultimate | `e = None` 清理语句 |

**根因**: Exception handler 的异常变量清理（`STORE_FAST e; LOAD_CONST None; STORE_FAST e`）在 handler 结束后未正确过滤。

---

### P1 — 控制块异常（EMPTY_TRY + ELSE_CONTAINS_FINALLY + REDUNDANT_RAISE）

#### EMPTY_TRY (14)

| 文件 | 版本 | 详情 |
|------|------|------|
| enum | 3.11-3.14 | try 体为空(行388-951) |
| reprlib | 3.11-3.14 | try 体为空(行191-229) |
| test_try_complex | 3.11-3.14 | try 体为空(行11) |
| l9_ultimate | 3.12, 3.14 | try 体为空(行32, 86) |

**根因**: seq-blocks 中 `BuildTryStructureStatements` 的 body 指令处理可能在 try body 为空时跳过正确内容。

#### ELSE_CONTAINS_FINALLY (11)

所有版本（2.7-3.14）的 `test_try_simple` 均触发。测试脚本伪阳性——`print('finally')` 在 `finally:` 块内部但测试不检查缩进。**可忽略**。

#### REDUNDANT_RAISE (14)

| 文件 | 版本 | 次数 |
|------|------|------|
| enum | 3.10/3.12-3.14 | 5-14 |
| functools | 3.12-3.14 | 5 |
| l6_advanced | 3.12/3.14 | 4 |
| l8_complex | 3.12/3.14 | 5-6 |
| test_comp | 3.12-3.14 | 3 |

**根因**: Exception handler 的 `RERAISE` 操作码产生的 `raise` 语句在 seq-blocks 的 handler 构建后未完全过滤。

---

### P2 — 语法错误（SYNTAX_ERROR + FORMAT_ERROR）

#### SYNTAX_ERROR (14)

| 错误 | 文件 | 原因 |
|------|------|------|
| `invalid syntax` (line 4) | test_nested_comp 3.5/3.6/3.7 | Comprehension 编译问题 |
| `invalid syntax` (line 4) | test_simple_comp 3.5/3.6/3.7 | Comprehension 编译问题 |
| `invalid syntax` | abc 3.5, test_cls2 3.5 | 老版本兼容 |
| `invalid syntax (line 116)` | l7_edge 3.12 | 边缘 case |
| `invalid syntax (line 1456-2159)` | enum 3.11-3.14 | 大文件复杂 case |
| `'yield from' outside function` | l5_class 3.12 | Comprehension 中的 yield |

**根因**: 3.5/3.6/3.7 的 comprehension 编译差异；大文件的 seq-blocks 遍历边界问题。

#### FORMAT_ERROR (3)

| 文件 | 行 | 问题 |
|------|-----|------|
| reprlib 3.11 | 行173 | `return f"{{s!s}}"` |
| reprlib 3.12 | 行178 | `return f"{{s!s}}"` |
| reprlib 3.14 | 行183 | `return f"{{s}}"` |

**根因**: F-string 中双花括号 `{{`、`}}` 的转义处理不完全。

---

## 5. 版本瓶颈分析

| 版本 | 通过率 | 瓶颈 |
|------|--------|------|
| 2.7 | 70% | 老版本特有操作码 |
| 3.5-3.7 | 73-75% | Comprehension 语法差异 |
| 3.8-3.9 | **82%** | 最稳定版本 |
| 3.10 | 78% | match 模式匹配 |
| 3.11 | **56%** | ⚠️ ExceptionTable + 新操作码 |
| 3.12 | 59% | ⚠️ 大文件边界问题 |
| 3.13 | 64% | ⚠️ comprehension 差异 |
| 3.14 | 65% | ⚠️ 新操作码 + CACHE 格式 |

---

## 6. 修复行动计划

### Batch X1: CLEANUP_LEAK 消除（预期 +5 通过）

**难度**: 低  
**目标**: 23 → 0

修复 `TrimPostTerminalDeadCode` 增加 handler cleanup 模式识别：
- `STORE_FAST e` 紧随 `LOAD_CONST None` 的自赋值模式
- 在 AST 层面将 `e = None` 删除

### Batch X2: REDUNDANT_RAISE 消除（预期 +10 通过）

**难度**: 中  
**目标**: 14 → 0

在 `BuildTryStructureStatements` 中，handler body 构建后对残余 `raise` 做后过滤：
- 非 try 结构体内的裸 `raise` 去掉
- handler 末尾的 `RERAISE` 转化产生的 `raise` 去掉

### Batch X3: EMPTY_TRY 修复（预期 +8 通过）

**难度**: 高  
**目标**: 14 → 0

修复 `BuildTryStructureStatements` 的 try body 范围计算：
- ExceptionTable 的 try body 范围可能遗漏或错位
- 对 3.11+ ExceptionTable 的 body 范围做更精确的映射

### Batch X4: BARE_EXPR 子模式修复（预期 +15 通过）

**难度**: 中-高  
**目标**: 92 → 60

逐个子模式修复：
1. Comprehension 变量 `x`/`row` 泄漏：在 comprehension 反编译后清理 generator variables
2. Match pattern `int`/`str` 泄漏：在 match 结构构建后清理 pattern subjects
3. Class body expression 泄漏：在 class 构建后检查漏网表达式

### Batch X5: SYNTAX_ERROR 修复（预期 +8 通过）

**难度**: 中  
**目标**: 14 → 0

1. 3.5-3.7 comprehension 差异：检查 `test_nested_comp` 和 `test_simple_comp` 的编译输出
2. Enum 大文件语法错误：检查 seq-blocks 的边界遍历
3. `'yield from' outside function`：comprehension yield 标记处理

---

## 7. 预期路线图

| 批次 | 预期通过 | 累计通过 | 通过率 | 
|------|---------|---------|--------|
| 当前 | 286 | 286 | 70% |
| X1 (CLEANUP) | +5 | 291 | 71% |
| X2 (RAISE) | +10 | 301 | 74% |
| X3 (EMPTY_TRY) | +8 | 309 | 76% |
| X4 (BARE_EXPR) | +15 | 324 | 80% |
| X5 (SYNTAX) | +8 | 332 | 82% |

**终极目标**: 372/405 (92%)，保留约 33 个深层次问题（enum/functools/reprlib 的结构修复需要更复杂的 CFG 级改动）。
