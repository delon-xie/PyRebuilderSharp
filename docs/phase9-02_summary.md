# Phase 9-02 总结文档

> 日期: 2026-07-10
> 修复: BARE_EXPR 增强清理（递归 + 更广覆盖）

---

## 变更文件

| 文件 | 改动 |
|------|------|
| `src/.../Builders/AstBuilder.cs` | CleanupBareExpr 重写：递归 + ProcessChildBareExpr + 扩展 Name 集合 |

## 指标变化

| 指标 | 修复前 | 修复后 | 变化 |
|:-----|:------:|:------:|:----:|
| 全量基线 | 1325/1325 | 1325/1325 | → ✅ |
| 孤儿块 | 0 | 0 | → ✅ |
| A+B 可接受 | 52 (4%) | 52 (4%) | → |
| **Diff lines** | **146007** | **140207** | **↓5800** ✅ |
| 白盒通过 | 299 | **305** | **+6** ✅ |
| BARE_EXPR | 82 | **74** | **-8** ✅ |
| `dotnet build` | 0 err | 0 err | → ✅ |

## 改动要点

1. **递归子结构处理** — 新增 `ProcessChildBareExpr()` 递归进入 If/For/While/Try/With/FunctionDef/ClassDef 的 body，对每个子 body 调用 `CleanupBareExpr()`。这是最关键的变化——之前的清理只处理顶级语句，嵌套在控制结构内的 BARE_EXPR 全部漏过。
2. **Name 关键字残留清理** — `Name { Id: "return" }`, `"raise"`, `"yield"` 删除
3. **IsBareNameSafeToRemove 扩展** — 增加 `name`、`return`、`yield`、`raise`
4. **模式合并** — `Constant { Value: null }` 单行处理

## 待处理（Phase 9-02+）

| 问题 | 数量 | 说明 |
|:-----|:----:|:------|
| SYNTAX_ERROR | 14 | 需逐例分析（3.5 兼容、大文件边界、yield 作用域） |
| BARE_EXPR 残余 | 74 | 需更深层分析（handler cleanup None、f-string 片段） |
