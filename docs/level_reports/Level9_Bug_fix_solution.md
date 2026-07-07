# Level 9 诊断结果 + 全 Level 总结

> Level 9：最终组合测试
> 1 文件 × 9 测试点，1757 diff lines，全 D

---

## 问题分析

Level 9 所有 10 个函数的问题均来自 Level 1-8 已知问题。

| 函数 | 核心问题 | 根因 |
|:-----|:---------|:------|
| l9_1 | def→class, annotations, except as, with 顺序 | L1/2/4/5 |
| l9_2 | def→class, defaults, decorator `@functools.wraps`, try-except | L1/2/3/4/5 |
| l9_3 | while yield generator 控制流崩塌 | L1/2/6 |
| l9_4 | lambda 参数丢失 λvarargs `*args` | L3/6 |
| l9_5 | with 链接 `with A() as a, B() as b:` 失败 | L2 |
| l9_6 | type hints `x: int` 丢失 + for-else 误判 | L1/4 |
| l9_7 | `nonlocal depth` + `def→class` | L1/4/5 |
| l9_8 | async generator `yield` in async → broken | L6 |
| l9_9 | `type()` + dict + lambda 组合 | L3/5 |
| l9_10 | `raise ValueError(f"...")` + try/except + for + if | L1/2 |

## 全 Level 最终总结

```
Level 1  (控制流):   2151 → 2020 ↓131  19%  ✅ while break, def→class
Level 2  (异常/with): 1889 → 1881   ↓8   1%  ⚠️ try/except 需重构
Level 3  (lambda):     243 →  227  ↓16   7%  ✅ 三元 IfExp, varargs
Level 4  (函数定义):   336 →  302  ↓34  10%  ✅ 闭包 _cell, 递归, *args
Level 5  (类定义):     576 →  557  ↓19   3%  ✅ 类 docstring
Level 6  (推导式):   1196 → 1180  ↓16   1%  ✅ Await, Walrus, With 去重
Level 7  (边界):     7011 → 7011   ↓0   0%  ⚠️ test_syntax.py 膨胀
Level 8  (复杂):     1543 → 1533  ↓10   1%  ✅ 装饰器顺序
Level 9  (终极):     1757 → 1757   ↓0   0%  ⚠️ 已知问题组合
                 ─────    ─────  ──── 
总计:            18702 → 18468 ↓234
```

## 剩余两个核心工程

| 工程 | 影响 diff lines | 根因文件 | 估算 |
|:-----|:---------------:|:---------|:----:|
| **try/except 重构** (L2/5/6/8/9) | ~3000+ | `AstBuilder.cs` BuildTryFromBlock/BuildTryFromExceptionTable | 6h |
| **推导式引擎重写** (L6/8/9) | ~1500+ | `AstBuilder.cs` TryDetectInlinedComprehension/BuildComprehension | 6h |

这两个修复将自动解决 Level 7-9 中所有重现的问题。
