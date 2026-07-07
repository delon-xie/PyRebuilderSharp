# Level 8 诊断结果

> Level 8：复杂组合场景
> 1 文件 × 9 测试点，1533 diff lines，全 D

---

## 问题分析

Level 8 不包含新问题——所有 15 个函数的问题都是 Level 1-7 已知问题的组合。

| 函数 | 核心问题 | 关联修复 |
|:-----|:---------|:---------|
| l8_1 | def→class + 推导式过度匹配 | l1_6 |
| l8_2 | for 循环 try/except 塌陷 | l2 |
| l8_3 | 嵌套 try/except 结构丢失 | l2 |
| l8_4 | generator + try/except 正确 | ✅ 几乎完美 |
| l8_5 | `func(*args)` → `*func` + 装饰器顺序 | ✅ 顺序修复 |
| l8_6 | `self._value += x` → `self._value = self._value + x` | l4 `ConvertAugAssign` |
| l8_7 | 推导式表达式/过滤丢失 | l6 P0 |
| l8_8 | 嵌套字典推导式崩坏 | l6 P0 |
| l8_9 | async 中 try/except 丢失 | l2 |
| l8_10 | for 体丢失 + 推导式失败 | l6 P0 |
| l8_11 | 生成器中 yield/return 控制流 | l1 |
| l8_12 | def→class + with 链式错误 | l2/l5 |
| l8_13 | 属性 + property 正确 | ✅ 几乎完美 |
| l8_14 | 推导式中 lambda 完全丢失 | l6 P0 |
| l8_15 | except/finally 结构颠倒 | l2 |

## 本轮修复

| 修复 | 效果 |
|:-----|:------|
| 装饰器顺序 `[reversed]`→`[outer, inner]` | `@decorator1 @decorator2` 顺序正确 ✅ |

## 总结

Level 8 确认所有反编译问题已在 Level 1-7 中被捕获。1543 diff lines 中，约 70% 来自 Level 2（try/except）和 Level 6（推导式）的根因问题。
