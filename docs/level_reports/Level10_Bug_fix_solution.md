# Level 10 诊断结果 + 全局总结

> Level 10：剩余根目录全部 .py 文件
> 130+ 文件 × 9 版本，76,759 diff lines
> **A=18 B=31** — 首次出现完美反编译 🎉

---

## 成绩亮点

- **18 个 A 类文件**（零 diff）在不同版本中完美反编译
- **31 个 B 类文件**（微小差异）分布在 3.8-3.14 版本
- 简单文件如 `test_just_for.py`（除头部注释外零 diff）
- 标准库模块如 `abc.py` 部分版本完全正确

## 全局反编译状态

```
                    基线    当前  ↓降幅   A+B 率
═══════════════════════════════════════════════════
Level  1 (控制流):   2151 → 2020 ↓131   6%+  ❌ 全 D
Level  2 (异常):     1889 → 1881   ↓8   1%+  ❌ 全 D
Level  3 (lambda):    243 →  227  ↓16   7%+  ❌ 全 D
Level  4 (函数):      336 →  302  ↓34  10%+  ❌ 全 D
Level  5 (类):        576 →  557  ↓19   3%+  ❌ 部分 C
Level  6 (推导式):   1196 → 1180  ↓16   1%+  ❌ 3 B
Level  7 (边界):     7011 → 7011   ↓0   —   ❌ 全 D
Level  8 (复杂):     1543 → 1533  ↓10   1%+  ❌ 全 D
Level  9 (终极):     1757 → 1757   ↓0   —   ❌ 全 D
Level 10 (全量):      —    76759    —   5%   ✅ A=18 B=31
═══════════════════════════════════════════════════
总计 diff:           18702→18468 ↓234      17-level ≅ 95K diff
                             +76759
                            ───────
                            ~95,000
A+B 率: 4-5%（130 文件中约 5-6 个 A+B）
```

## 核心待解决问题

| # | 问题 | 估计 diff | 优先级 |
|:-:|:-----|:---------:|:------:|
| 1 | **try/except 结构恢复失败** (3.8-3.14) | ~40,000 | P0 |
| 2 | **推导式元素/过滤/迭代器丢失** | ~15,000 | P0 |
| 3 | **类 body/`__build_class__` 模式失败** | ~10,000 | P1 |
| 4 | **def→class 误判** (PostProcessFunctionDefs) | ~5,000 | P1 |
| 5 | **闭包捕获变量名 `_cell` / 非局部变量** | ~3,000 | P1 |
| 6 | **函数注释/默认值/varargs 损失** | ~5,000 | P2 |
| 7 | **装饰器重构失败** | ~3,000 | P2 |
| 8 | **常量折叠/引号/元组括号** (cosmetic) | ~8,000 | P3 |
| 9 | **重复空白行/头部注释** (cosmetic) | ~6,000 | P3 |

## 所有修复文件索引

| 文件 | 修复内容 |
|:-----|:---------|
| `ControlFlowScanner.cs` | 跳过体内回边 (l1_7) |
| `BlockScanner.cs` | RETURN_VALUE 不添加后继 (l1_4) |
| `AstBuilder.cs` | if-else 三元表达式 → IfExp (l3_10) |
| `AstBuilder.cs` | while-else break 检测 (l1_9) |
| `AstBuilder.cs` | 死代码终端语句阻断 (l1_4) |
| `AstBuilder.cs` | BuildLambda varargs 参数名 (l3_6) |
| `AstBuilder.cs` | 无参 lambda `_` 消除 (l3_9) |
| `AstBuilder.cs` | TryDetectInlinedComprehension 非推导式拒绝 (l1_6) |
| `AstBuilder.cs` | 装饰器顺序外→内 (l8_5) |
| `AstBuilder.cs` | 隐式 docstring 过滤 `<locals>` (l5) |
| `AstBuilder.cs` | StripTrailingReturnNone 保护唯一 return (l4_13) |
| `AstBuilder.cs` | with 语句去重 (l6_11) |
| `AstBuilder.cs` | GetStructuredBlockStmts `_processedBlockIds` (l1_4) |
| `StackMachine.cs` | GetDerefVarname 3.10- 布局分离 (l4_5/6/10) |
| `StackMachine.cs` | LOAD_CLOSURE 3.10- 布局 (l4_5/6/10) |
| `StackMachine.cs` | CALL_FUNCTION_EX `*args` 展开 (l4_9) |
| `StackMachine.cs` | YIELD_FROM async→Await (l6_6) |
| `StackMachine.cs` | DUP_TOP walrus 检测 (l6_7) |
| `Expr.cs` | 新增 `IfExp`, `Await` 记录类型 |
| `PythonCodeGenerator.cs` | 新增 VisitIfExp, VisitAwait |
