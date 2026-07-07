# Level 6 问题分析与修复方案

> Level 6：推导式、async、yield、generator、match/case、walrus
> 7 文件 × 59 测试点，1196 diff lines

---

## 问题总览

| # | 问题 | 影响 | 根因 | 难度 |
|:-:|:-----|:-----|:-----|:----:|
| **P0** | 推导式元素表达式丢失 `x*x`→`x` | l6_2/3, test_comp, test_nested_comp | `TryDetectInlinedComprehension` 中 `LIST_APPEND_313` 之后的指令未正确模拟 | 🔴 |
| **P0** | 推导式迭代器丢失 `range(10)`→`iterable` | 全 comprehension | `GET_ITER` → `FOR_ITER` 链中迭代表达式提取失败，fallback 到 `Name('iterable')` | 🔴 |
| **P0** | 推导式过滤条件丢失 `if x%2==0` | 含条件的推导式 | `hasIf` 检测到但不含过滤条件的表达式 | 🟡 |
| **P1** | `await f()`→`yield from f()` | l6_6 | `GET_AWAITABLE` + `YIELD_FROM` 被识别为 yield from | 🟡 |
| **P1** | walrus `n := len(items)`→`n = len(items)` | l6_7 | `COPY` + `STORE_FAST` + `DUP_TOP` 未组合为 NamedExpr | 🟢 |
| **P1** | match/case → if/elif | l6_8 | `MATCH_KEYS`/`MATCH_CLASS` 等 3.10+ 模式匹配被 BuildIfElse 捕获 | 🔴 |
| **P1** | dataclass 类体 `pass` + 装饰器错位 | l6_9 | `@dataclass` 装饰器 + `x: int` 注释在类体中丢失 | 🟡 |
| **P1** | enum 值丢失 | l6_10 | 类体中 `RED = 1` 未识别 | 🟡 |
| **P1** | with 语句重复 | l6_11 | `SETUP_WITH` + 异常表路径都生成 with | 🟡 |
| **P2** | 装饰器 with args 体丢失 | l6_12 | `for _ in range(times): results.append(...)` 变成 `pass` | 🟡 |
| **P2** | lambda 在推导式中 | l6_15 | `lambda x, i=i: x + i` 中的默认值 `i=i` 未正确渲染 | 🟢 |

---

## 可快速修复（P1-P2）

| 问题 | 修复 | 行数 | 收益 |
|:-----|:-----|:----:|:----:|
| walrus `n:=x` | `COPY(1)` + `STORE_FAST n` + `... POP` 模式 → `NamedExpr` | 5 | l6_7 |
| `await f()`→`yield from` | `GET_AWAITABLE` + `YIELD_FROM` 改为 `Await` | 3 | l6_6 |
| with 语句重复 | `BuildWithFromBlock` 标记已处理块 | 3 | l6_11 |
| enum 值/注解丢失 | `__build_class__` 同 l5 P0 问题 | shared | l6_9/10 |

---

## 建议

Level 6 的推导式问题是最大工程项（占 60%+ diff lines），与 `TryDetectInlinedComprehension` 的指令模拟引擎相关。walrus 和 `await` 修复可在 15 分钟内完成。
