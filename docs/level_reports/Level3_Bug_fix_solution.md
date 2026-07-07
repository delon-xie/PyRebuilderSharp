# Level 3 分析与修复记录

> Level 3：Lambda 表达式
> Diff lines: 243 → 227（本轮修复）

## 本轮修复

| 修复 | 文件 | 效果 |
|:-----|:-----|:------|
| 三元表达式 (l3_10) | `AstBuilder.BuildIfElse`, `Expr.cs`, `PythonCodeGenerator.cs` | `(x>0) and x` → `x if x > 0 else 0` ✅ |
| 空 lambda 伪参数 (l3_9) | `AstBuilder.BuildLambda` | `lambda _: 42` → `lambda : 42` ✅ |
| varargs 参数名 (l3_6) | `AstBuilder.BuildLambda` | `_` → `args, kwargs` ✅（`*` 前缀仍缺失）|
| `IfExp` AST 节点 | `Expr.cs`, `PythonCodeGenerator.cs` | 新增三元表达式支持 |

## 新增 AST 模型

```csharp
public record IfExp(Expr Test, Expr Body, Expr Orelse) : Expr;
```
输出格式：`body if test else orelse`

## 剩余问题

| 问题 | 影响 | 根因 | 难度 |
|:-----|:-----|:-----|:-----|
| `_cell` → `outer_var` | l3_2, l3_5 | `LOAD_CLOSURE` cellIdx 在 3.10 localsplus 布局中解析不到捕获变量名 | 🟡 |
| 默认参数值丢失 `y=10`→`y` | l3_3 | 默认值存储在外层 `MAKE_FUNCTION` 指令中，`BuildLambda` 无访问路径 | 🟡 |
| 字典字面量 lambda 体丢失 | l3_8 | `PostProcessFunctionDefs` 未匹配字典内嵌的 `FunctionRef` | 🔴 |
| varargs `*`/`**` 前缀 | l3_6 | `Lambda` 的 `Parameter` 无 vararg/kwarg 标记 | 🟢 |
