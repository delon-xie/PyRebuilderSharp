# Step 3 总结文档

> 日期: 2026-07-10
> Phase 8 实施方案第三步完成
> 实现: CleanupBareExpr + 集成到 3 条后处理路径

---

## 成果清单

```
Step 3 → ✅
├── CleanupBareExpr pass ────────────────────────────────── ✅
│   ├── B4/B6: FunctionRef(`<...>`) 删除
│   ├── B8: 孤立 Name 删除 (x, cls, method, it, result...)
│   ├── B5: 类体属性/方法删除 (cls.__x__, self.x()...)
│   ├── B1/B2/B3: comprehension .append/.add/.__setitem__ 删除 (带上下文检测)
│   └── B7: match type pattern 删除 (int, str...)
│
├── FoldDecoratorCalls ──────────────────────────────────── 🔄
│   ├── IsDecoratorExpression() 保留为预备代码
│   └── 已注释：FunctionRef→FunctionDef 映射需要更仔细的设计
│
└── 集成到 3 条后处理路径 ────────────────────────────────── ✅
    ├── Build() — 非 seq-blocks 回退路径
    ├── BuildWithSequentialBlocks() — seq-blocks 主路径
    └── BuildFallback() — 降级回退路径
```

## 变更文件

| 文件 | 改动 |
|------|------|
| `src/.../Builders/AstBuilder.cs` | +9 个方法 (CleanupBareExpr + 6 个 helper + IsDecoratorExpression) |
| | +`using AstAttribute` 别名避免与 System.Attribute 冲突 |
| | +3 处 `CleanupBareExpr(stmts)` 调用（3 条路径各一） |

## 回归验证

| 检查项 | Step 1 基线 | Step 3 结果 | 变化 |
|--------|:----------:|:----------:|:----:|
| `dotnet build` | 0 errors | 0 errors | → |
| 白盒通过 (PASS) | 298 | **299** | **+1** ✅ |
| BARE_EXPR | 83 | **82** | **-1** ✅ |
| 其他指标 (EMPTY_TRY, SYNTAX_ERROR 等) | 不变 | 不变 | → |

## 技术难点记录

### 1. 3 条后处理路径都需要单独添加

`AstBuilder` 有 3 条不同的构建路径：
- `Build()` — 非 seq-blocks 路径
- `BuildWithSequentialBlocks()` — seq-blocks 主路径（默认）
- `BuildFallback()` — 降级回退路径

每条路径有**独立的** `PostProcessFunctionDefs → ConvertAugAssign → CollapseRedundantPasses` 管道。
新 pass 必须 3 处都加，否则 seq-blocks 默认路径不生效。

### 2. Attribute 命名冲突

`Models.AST.Attribute` 与 `System.Attribute` 冲突。
解决方案：`using AstAttribute = PyRebuilderSharp.Core.Models.AST.Attribute;`

### 3. Decorator 折叠被推迟

`FoldDecoratorCalls` 的设计难点：
- `Call.Args` 类型是 `List<Expr>`，但 `FunctionDef` 是 `Stmt`（不在 `Expr` 层次结构中）
- 实际上 `PostProcessFunctionDefs` 已经将 `FunctionRef` 从 stmts 中提取出来，但嵌套在 `Call.Args` 中的 `FunctionRef` 仍在原位置
- 需要 stmts 级别的 `FunctionRef` → `FunctionDef` 映射关系来正确折叠

## 下一步

Step 4 可直接开始：后支配树 + COME_FROM 结构验证（3天）。
或者在此 Step 基础上增强 CleanupBareExpr（更多的 BARE_EXPR 模式 + complete decorator folding）。

推荐：先进行 Step 4（结构验证），回来再增强 Step 3。
