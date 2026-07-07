# Level 1 P0 修复完成状态

## 已修复（4/4 P0，本轮完成）

| P0# | 问题 | 改动文件 | 关键代码 | 影响范围 |
|:---:|:-----|:---------|:---------|:--------:|
| 1 | if-else → `and`/`or` 短路误判 | `AstBuilder.cs` | `isSimpleAndExpr`/`isSimpleOrExpr` 增加 `!bodyHasAssign && !hasStoresInBody` | l1_1~l1_3, l1_10, l1_11, if_else.py 全部 |
| 2 | for/while else 子句丢失 | `AstBuilder.cs` | `elseOffset = offset + 2 + arg + (Py312?2:0)` | l1_8, loop_else.py 全部, l1_5, l1_6 for-else |
| 3 | while True + break 嵌套 | `AstBuilder.cs` | 检测 header 中 POP_JUMP 前有 STORE/INPLACE → 条件=True | l1_7 `while True` 条件正确 |
| 4 | for-else 过拟合 + try-except | `AstBuilder.cs` | 无 break/condJump 的 for 循环 `return false` | test_control_flow for-else 消除 |

## 附加修复

| 问题 | 改动 | 效果 |
|:-----|:-----|:------|
| 孤立表达式 `range(10)` / `lst` / 字面量 | `GetStructuredBlockStmts` + `BuildStatementsInternal` 中 GET_ITER 前导块委派 | 6 个文件消除冗语，`l1_5_for_range` 达到正确输出 |
| 丢失初始化语句 | GET_ITER 块中提取 Assign 等初始化语句 | `total = 0` 等保留 |

## 待修复（需更深层改动）

| 问题 | 模块 | 原因 | 难度 |
|:-----|:-----|:-----|:----:|
| l1_6 `def`→`class` | `AstBuilder.PostProcessFunctionDefs` + `TryDetectInlinedComprehension` | 函数体被误判为列表推导式 | 🟡 |
| l1_7 while True 内层 if `i>10:break`→嵌套 while | `ControlFlowScanner` 循环/条件块分类 | POP_JUMP 被重复嵌套为 while | 🔴 |
| l1_9, loop_else while-else 条件 `i==10`→`not i<5` | `AstBuilder.BuildWhileLoop` | else 体条件来源判断错误 | 🟡 |
| 死代码 after return | `AstBuilder.BuildBlockOnly` / `CollectBodyBlocks` | 后继块未及时终止 | 🟢 |
| 模块级 try-except 丢失 | `AstBuilder.BuildStatementsInternal` / `BuildTryFromBlock` | FOR_ITER→else 块在后续 path 中未被重处理 | 🔴 |
| set 字面量 `{1,2,3}`→`{[1,2,3]}` | `AstBuilder.BlockDecompiler` | 3.10+ BUILD_SET CACHE 条目 | 🟢 |
