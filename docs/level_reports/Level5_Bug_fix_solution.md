# Level 5 问题分析与修复方案

> Level 5：类定义与继承
> 3 文件 × 27 测试点，576 diff lines

---

## 问题总览

| # | 问题 | 影响 | 根因 | 难度 |
|:-:|:-----|:-----|:-----|:----:|
| 1 | `__build_class__` 模式未识别 | l5_13/14 类体完全消失 | `PostProcessFunctionDefs` 中 `LOAD_BUILD_CLASS` → `__build_class__` 检测失败 | 🔴 |
| 2 | 类变量赋值丢失 `x=1` | l5_2, l5_11 | `STORE_NAME` 在类体中未被识别为类属性 | 🟡 |
| 3 | 类文档字串覆盖方法体 | l5_11, l5_13 | co_consts[0] 中的 `<locals>.ClassName` 被插入为 `ExprStmt` | 🟢 |
| 4 | 装饰器丢失 `@classmethod`/`@staticmethod`/`@property` | l5_5, l5_14, 3.14 更多 | `MAKE_FUNCTION` + `STORE_NAME` 后 `__qualname__` 模式匹配失败 | 🔴 |
| 5 | `__slots__` tuple→list | l5_12 | 元组常量 `('x', 'y')` 被反编译为列表 `['x', 'y']` | 🟢 |
| 6 | 返回元组括号 `(a.x, a.y)` vs `a.x, a.y` | 多函数 | 元组返回值统一带有括号 | 🟢 |
| 7 | 双引号→单引号 | 全文件 | 字符串常量反编译为单引号 | 🟢 |
| 8 | `A.count += 1` → `A.count = A.count + 1` | l5_11 | 属性增广赋值未识别 | 🟡 |
| 9 | `from abc import ABC, abstractmethod` 分解 | l5_14 | `IMPORT_FROM` + `STORE_NAME` 解析丢失顺序 | 🟢 |

---

## 可快速修复的问题

| 问题 | 修复 | 预计行数 | 收益 |
|:-----|:-----|:--------:|:----:|
| 类文档字串覆盖 (3) | 过滤 `<locals>.` 开头的常量 | 3 | l5_11, l5_13 |
| `__slots__` list→tuple (5) | 在 `__slots__` 赋值时转换 ListLiteral 为元组 | 5 | l5_12 |
| `A.count += 1` (8) | 属性增广赋值 `A.x = A.x + 1` → `A.x += 1` | 3 | l5_11 |
| 导入语句顺序 (9) | `IMPORT_FROM` → `STORE_NAME` 恢复导入链 | 3 | l5_14 |

---

## 建议

Level 5 的核心问题（`__build_class__` 识别失败、装饰器丢失）涉及 `PostProcessFunctionDefs` 中 `LOAD_BUILD_CLASS` 模式匹配，需要 4-6 小时深入修复。类文档字串覆盖和元组→列表修复可以在 15 分钟内完成。
