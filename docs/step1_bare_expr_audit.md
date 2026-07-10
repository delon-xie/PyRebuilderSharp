# Step 1 产出物: BARE_EXPR 分类审计报告

> 日期: 2026-07-10
> 基线: 白盒 298/405 (73.6%)，BARE_EXPR=83, SYNTAX_ERROR=14
> 来源: `test_data/whitebox_report_20260710_075900.md`

---

## 1. 总体统计

| 指标 | 数值 |
|------|------|
| 白盒总用例 | 405 |
| 通过 | 298 (73.6%) |
| BARE_EXPR 总数 | **83** |
| 涉及测试文件 | 21 个 |
| 涉及 Python 版本 | 2.7, 3.5~3.14 |

## 2. 分类汇总

| 分类 | 规则 | 约数量 | 安全度 | 说明 |
|------|------|--------|--------|------|
| **A: comprehension 变量泄漏** | B1/B2/B3 | ~30 | 🟡 中 | LIST_APPEND/MAP_ADD 残留，可在 `ConvertComprehensionCalls` 后清除 |
| **B: 类体属性/方法泄漏** | B5 | ~15 | 🟢 高 | `cls.__bases__`、`self.connect()` 等，可安全删除 |
| **C: match pattern 中间值** | B7 | ~8 | 🟡 中 | `int`、`str` 等类型名在 guard 中残留 |
| **D: None/return/yield 残留** | B4/B8 | ~12 | 🟢 高 | 编译器生成的隐式 None 泄漏 |
| **E: 裸名称泄漏** | B8 | ~10 | 🟢 高 | 孤立变量名 `x`、`method`、`it` 等 |
| **F: 裸函数/方法调用泄漏** | — | ~5 | 🔴 低 | `os.unlink(x)`、`gen.reset(10)` — 可能影响语义，谨慎 |
| **G: 裸表达式泄漏** | — | ~3 | 🔴 低 | `x < 0`、`functools.WRAPPER...` 等 |

## 3. 逐例分类表

| # | 测试文件 | 版本 | 裸表达式 | 分类 | 处理规则 |
|---|---------|------|---------|------|---------|
| 1 | abc | 2.7,3.10~3.14 | `abstracts.add(name)` | A — comprehension .add | B1 |
| 2 | abc | 3.5 | `inheritance.` | D — docstring 残留 | H1 |
| 3 | abc | 3.5~3.14 | `instead.` | D — docstring 残留 | H1 |
| 4 | abc | 3.10~3.14 | `cls.__bases__` | B — 类体属性 | B5 |
| 5 | abc | 3.10~3.14 | `cls._abc_registry` / `cls._abc_cache` | B — 类体属性 | B5 |
| 6 | abc | 3.11+ | `cls` | E — 裸名称 | B8 |
| 7 | abc | 3.11+ | `cls.__dict__` | B — 类体属性 | B5 |
| 8 | enum | 3.6~3.10 | `return` | D — return 在函数体外残留 | H2 |
| 9 | enum | 3.11~3.14 | `name.startswith(pattern)` | F — 方法调用 | H3 |
| 10 | enum | 3.11~3.14 | `name` | E — 裸名称 | B8 |
| 11 | enum | 3.13~3.14 | `num` | E — 裸名称 | B8 |
| 12 | enum | 3.13~3.14 | `getattr(self, name, ...)` | F — 方法调用 | H3 |
| 13 | functools | 3.8~3.10 | `functools.WRAPPER_ASSIGNMENTS)` | G — 表达式 | H4 |
| 14 | functools | 3.11~3.14 | `StopIteration` | E — 裸名称 | B8 |
| 15 | functools | 3.12 | `order.append(j)` | A — comprehension .append | B1 |
| 16 | functools | 3.13~3.14 | `it` | E — 裸名称 | B8 |
| 17 | l2_exception | 3.12 | `ZeroDivisionError` | E — 裸异常类型名 | B8 |
| 18 | l5_class | 3.12 | `abc.abstractmethod` | B — decorator 残留 | B5 |
| 19 | l6_advanced | 3.12,3.14 | `x` | E — 裸名称 | B8 |
| 20 | l6_advanced | 3.12,3.14 | `raise` | D — raise 在 comprehension 外 | H2 |
| 21 | l6_advanced | 3.12,3.14 | `v` | E — 裸名称 | B8 |
| 22 | l8_complex | 3.12,3.14 | `result.append('zero')` | A — comprehension .append | B1 |
| 23 | l8_complex | 3.12,3.14 | `results.extend(...)` | A — comprehension .extend | B1 |
| 24 | l9_ultimate | 3.12,3.14 | `gen.reset(10)` | F — 方法调用 | H3 |
| 25 | l9_ultimate | 3.12,3.14 | `self.connect()` | B — 类体方法调用 | B5 |
| 26 | l9_ultimate | 3.12,3.14 | `self.disconnect()` | B — 类体方法调用 | B5 |
| 27 | l9_ultimate | 3.12,3.14 | `result` | E — 裸名称 | B8 |
| 28 | loop_else | 3.11 | `return` | D — return 残留 | H2 |
| 29 | loop_else | 3.11 | `total` | E — 裸名称 | B8 |
| 30 | match_full | 3.10,3.11 | `int` | C — match type pattern | B7 |
| 31 | match_full | 3.10,3.11 | `str` | C — match type pattern | B7 |
| 32 | match_simple | 3.10,3.11 | `int` | C — match type pattern | B7 |
| 33 | match_simple | 3.10,3.11 | `str` | C — match type pattern | B7 |
| 34 | reprlib | 3.6~3.14 | `repr_running.add(key)` | A — set .add | B1 |
| 35 | reprlib | 3.6 | `None` | D — None 残留 | B4 |
| 36 | reprlib | 3.11~3.14 | `method` | E — 裸名称 | B8 |
| 37 | reprlib | 3.11~3.14 | `(n, ...)` | G — 表达式 | H4 |
| 38 | test_comp | 2.7~3.14 | `x` (行 4, 9, 12) | A — comprehension 变量 | B1/B8 |
| 39 | test_comp | 3.12~3.14 | `raise` | D — raise 残留 | H2 |
| 40 | test_nested_comp | 2.7~3.14 | `x`, `row` | A — comprehension 变量 | B1/B8 |
| 41 | test_nested_comp | 3.5~3.7 | `test_nested_comp.py > 0` | G — 异常表达式 | H4 |
| 42 | test_simple_comp | 2.7~3.14 | `x` (行 4, 9, 12) | A — comprehension 变量 | B1/B8 |
| 43 | test_minimal_if | 2.7 | `os.unlink(py_path + 'c')` | F — 方法调用 | H3 |
| 44 | test_minimal_if | 3.9~3.13 | `os.unlink(py_path)` | F — 方法调用 | H3 |
| 45 | test_minimal_if | 3.11~3.13 | `f.write(src)` | F — 方法调用 | H3 |
| 46 | test_minimal_if | 3.11~3.13 | `None` | D — None 残留 | B4 |
| 47 | test_continue_for | 3.11 | `None` | D — None 残留 | B4 |
| 48 | test_just_for | 3.11 | `None` | D — None 残留 | B4 |
| 49 | test_try_complex | 3.12,3.13 | `ValueError` | E — 裸异常类型名 | B8 |
| 50 | test_with | 3.11~3.13 | `None` | D — None 残留 | B4 |
| 51 | test_yield_gen | 3.11~3.14 | `None`, `yield` | D — None/yield 残留 | B4 |
| 52 | try_else | 3.12,3.13 | `ZeroDivisionError` | E — 裸异常类型名 | B8 |
| 53 | if_else | 3.14 | `x < 0` | G — 条件表达式泄漏 | H4 |
| 54 | if_else | 3.14 | `y > 0` | G — 条件表达式泄漏 | H4 |

## 4. 分类占比

```
A (comprehension):  █████████████████████████░░░░  ~30 (36%)
B (class body):     █████████████░░░░░░░░░░░░░░░░  ~15 (18%)
C (match pattern):  ██████░░░░░░░░░░░░░░░░░░░░░░░  ~8 (10%)
D (None/return):    █████████░░░░░░░░░░░░░░░░░░░░  ~12 (14%)
E (bare name):      ████████░░░░░░░░░░░░░░░░░░░░░  ~10 (12%)
F (func call):      ████░░░░░░░░░░░░░░░░░░░░░░░░░  ~5  (6%)
G (expr):           ██░░░░░░░░░░░░░░░░░░░░░░░░░░░  ~3  (4%)
```

## 5. Step 3 处理优先级

| 优先级 | 规则 | 安全度 | 涉及条目 | 预期减量 |
|--------|------|--------|---------|---------|
| **立即处理** | B4: None/FunctionRef(`<...>`) 删除 | 🟢 | #35, #46~51 | -12 |
| **立即处理** | B8: 孤立 Name 删除 | 🟢 | #6, #10~11, #17, #19, #21, #27, #29, #36, #49, #52 | -10 |
| **立即处理** | B5: 类体 `cls.__xxx__` / `self.xxx()` 删除 | 🟢 | #4~7, #18, #25~26 | -8 |
| **可处理** | B1: comprehension `.append/.add` 删除 | 🟡 | #1, #15, #22~23, #34 | -7 |
| **可处理** | B7: match type pattern 删除 | 🟡 | #30~33 | -7 |
| **需研读** | 函数调用泄漏 (`os.unlink`, `gen.reset`, `f.write`) | 🔴 | #43~46 | -5 |
| **需研读** | 表达式泄漏 (`x < 0`, `WRAPPER_ASSIGNMENTS)`) | 🔴 | #13, #41, #53~54 | -4 |
| **需研读** | comprehension 裸变量 (`x`) 与真实 for-else 歧义 | 🔴 | #38, #40, #42 | — |
| **安全合计** | | | | **-30~-35** |

## 6. 关键发现

### 6.1 comprehension 相关的 BARE_EXPR 最难处理

**问题**：`test_comp` 的输出中，裸 `x` 和 `raise` 与 comprehension 变量共享同一个作用域。3.12+ 的输出为：

```python
def test_comp1():
    x              ← BARE_EXPR (comprehension iter variable leaked)
    range(10)      ← BARE_EXPR (GET_ITER + FOR_ITER leaked)
    for x in range(10):
        pass
    else:
        raise      ← BARE_EXPR (loop else raise leaked)
```

这里的 `x` 可能是 for-else 循环头部的 iter 变量泄漏，而不是 comprehension 变量。需要通过 `IsInComprehensionContext()` 启发式来区分。

### 6.2 `None` 在 3.11+ 高频出现

`None` BARE_EXPR 在 3.11+ 版本的多个测试中出现（test_with, test_yield_gen, test_continue_for, test_just_for）。这是 `RETURN_VALUE` / `RETURN_CONST` 的栈上 None 值泄漏，可以通过在 `StackMachine.Execute()` 中消化 `None` 常量来解决。

### 6.3 match type pattern 是新的分类

`int` 和 `str` 在 match_simple/match_full 中出现，是 match case 的 guard 表达式泄漏。这些应该由 `AnnotateMatchBlocks` 消化。

---

> **文档版本**: v1.0
> **下一步**: 将此分类表作为 Step 3 (BARE_EXPR 清理) 的直接输入
