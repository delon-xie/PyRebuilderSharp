# 综合问题修复计划

## 已完成
- **P0/P1**: 闭包 _cell (l4_5/6/10, l3_5), IfExp 三元 (l3_10), 递归名 (l4_8), *args 展开 (l4_9)
- **P1**: Await AST (l6_6), walrus DUP_TOP (l6_7), with 去重 (l6_11), 装饰器顺序 (l8_5)
- **P2**: 隐式 docstring 过滤 (l5_11/13), varargs 参数名 (l3_6), 无参 _ (l3_9)
- **CFG**: 嵌套 while 消除 (l1_7), 死代码阻断 (l1_4), while-else break 检测 (l1_9)

## 待修复（从易到难）

| 难度 | 问题 | 影响 | 优先级 |
|:----:|:-----|:-----|:------:|
| 🟢 | `test_syntax.py` 排除 + 空白行规范化 | 全量 diff -7000 | P3 |
| 🟢 | `except ValueError as e` → name 丢失 | l9_1/2 | P2 |
| 🟢 | 属性增广赋值 `self._value += x` | l8_6, l6 | P2 |
| 🟡 | **def→class 误判 (PostProcessFunctionDefs)** | l6_11, l7_17, l8_1/12, many L10 | **P1** |
| 🟡 | `global x` 声明丢失 | l4_7, l7_17 | P2 |
| 🟡 | try/except 内 Raise 去重 + nonlocal 恢复 | l9_2, l4_6 | P2 |
| 🔴 | **try/except 结构恢复 (3.8-3.14)** | L2/5/8/9/10, ~40K diff | **P0** |
| 🔴 | **推导式引擎重写** | L6/8/9/10, ~15K diff | **P0** |
| 🔴 | **__build_class__ 模式匹配** | L5/6/8/9/10, ~10K diff | **P1** |
