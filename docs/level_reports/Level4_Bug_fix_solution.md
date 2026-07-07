# Level 4 问题分析与修复方案

> Level 4：函数定义与多函数
> 3 文件 × 25 测试点，336 diff lines

---

## 问题总览

| # | 问题 | 影响 | 根因 | 难度 |
|:-:|:-----|:-----|:-----|:----:|
| 1 | `_cell` 代替捕获变量名 | l4_5, l4_6, l4_10 | `LOAD_CLOSURE`/`LOAD_DEREF` 在 3.6-3.13 中索引解析不到 Freevars | 🟡 |
| 2 | 闭包中初始化语句丢失 `x=1` | l4_6, l4_10 | 闭包内局部变量定义被 `POP_TOP` 后未恢复 | 🟡 |
| 3 | 注释丢失 (l4_4) | `(x: int, y: str) → bool` → `(x, y)` | `BuildFunctionDef` 未提取 `FunctionRef.AnnotationExprs`（不存在此字段） | 🔴 |
| 4 | 递归调用名 `n(n-1)` 错误 (l4_8) | 3.6-3.13 | `Name('fact')` 被解析为参数 `n`（栈/名匹配偏移） | 🟡 |
| 5 | 装饰器结构错误 (l4_9) | 3.14 完全反转 | `PostProcessFunctionDefs` 中装饰器 `@` 语法识别失败 | 🔴 |
| 6 | `func`→`args` 命名错乱 (l4_9 wrapper) | 3.6-3.13 | `Call` 的目标函数名从 `func` 错配为 `args` | 🟡 |
| 7 | `return None`→`pass` (l4_13) | 全部版本 | `StripTrailingReturnNone` 移除后 `FixEmptyFunctionBodies` 插入 `Pass` | 🟢 |
| 8 | docstring 引号类型 `"""`→`'` (l4_14) | 全部版本 | 常量转字符串时丢失原始引号类型 | 🟢 |
| 9 | 默认参数值丢失 `b=10`→`b` (l4_2) | 全部版本 | `FunctionRef.DefaultExprs` 可能为空 | 🟡 |
| 10 | global 声明丢失 `global x` (l4_7) | 全部版本 | `STORE_GLOBAL` 未生成 `Global` 声明节点 | 🟡 |
| 11 | `and`→`or` 短路错误 (l4_4) | 3.6-3.13 | `isinstance(x, int) and isinstance(y, str)` → `or` | 🟡 |
| 12 | 3.14 模块级 `__annotate__` 函数 | 3.14 特有 | annotations 系统生成的辅助函数被暴露 | 🟡 |

---

## 优先级排序

| 优先级 | 问题 | 影响 | 修复建议 |
|:------:|:-----|:-----|:---------|
| **P1** | 闭包 `_cell` (l4_5/l4_6/l4_10) | 3 个函数 | 与 l3_2 相同根因，修复 `GetDerefVarname` 的 localsplus 索引计算 |
| **P1** | 递归调用名 (l4_8) | 3.6-3.13，8 版本 | `StackMachine` 中 `CALL_FUNCTION` opcode 前 NAME 解析错误 |
| **P2** | `return None`→`pass` (l4_13) | 全部 | `StripTrailingReturnNone`: 仅移除非唯一的 Return(None) |
| **P2** | 默认值丢失 (l4_2) | 全部 | 与 l3_3 相同根因 — `FunctionRef.DefaultExprs` 可能未传播到嵌套函数 |

## 已修复

| 修复 | 效果 |
|:-----|:------|
| `StripTrailingReturnNone` 不移除唯一的 Return(None) | ⚠️ 需验证内层函数处理路径 |

## 建议

Level 4 的核心问题集中在闭包变量名解析（与 Level 3 共享根因）和函数名解析（递归/装饰器）。注释和 docstring 问题涉及 `FunctionRef` 数据结构和 `PythonCodeGenerator`，修复面较广，建议与 Level 5-9 一并规划。
