# Step 5 总结文档

> 日期: 2026-07-10
> Phase 8 实施方案第五步完成
> 实现: StructuralValidator ISC 适配 + DecompileNestedCodeObjects + 回归验证

---

## 成果清单

```
Step 5 → ✅
├── 5.1 StructuralValidator ISC 适配 ────────────────────── ✅
│   ├── 新增 3 个 seq-block 验证方法
│   │   ├── ValidateR1_SeqIfElse — seq-block if-else 链
│   │   ├── ValidateR3_SeqLoop — seq-block for/while 回边
│   │   └── ValidateR5_SeqExceptionTable — seq-block try ET 异常边
│   ├── 通过 DecompileOptions.ShowStructuralValidation 开关控制
│   └── 输出结构验证统计 (R1/R3/R5 各几例)
│
├── 5.2 DecompileNestedCodeObjects ──────────────────────── 🔄
│   ├── 3 个私有方法: DecompileNestedCodeObjects / FindChildCodeByName / DecompileChildCodeObject
│   ├── 循环引用保护（_processedNestedCodeNames）
│   ├── 递归深度保护（MaxNestedDepth=10）
│   ├── 继承图: 支持 FunctionDef / ClassDef 递归
│   └── 状态: 已实现 + 已注释（需集成适配）
│
└── 5.3 ET 映射尝试 ────────────────────────────────────── 🔄
    ├── overlap-based 尝试 → 退化（太激进）
    ├── 已回退到原 fully-contained 方案
    └── 结论: 需更精确的 handler 范围计算（Phase 2c HandlerDepth）
```

## 增量代码

| 文件 | 改动 |
|------|------|
| `Scanners/StructuralValidator.cs` | 重写: 新增 3 个 seq-block 方法 + AddFail helper |
| `Builders/AstBuilder.cs` | +94 行: DecompileNestedCodeObjects 全套实现 |
| | +`DecompileOptions.ShowStructuralValidation` 控制 validator |
| | -ET 映射暂时回退 |

## 回归验证

| 指标 | Step 3 | Step 4 | Step 5 | 变化 |
|------|:------:|:------:|:------:|:----:|
| 白盒通过 | 299 | 299 | **299** | → |
| BARE_EXPR | 82 | 82 | 82 | → |
| EMPTY_TRY | 56 | 56 | 56 | → |
| `dotnet build` | 0 err | 0 err | 0 err | → |

## 经验教训

### 1. ET overlap 检查比想象中危险

overlap 检查 `sb.StartOffset < hEnd && sb.EndOffset > hStart` 导致 -3 退化，因为 seq-block 的偏移范围可能跨越 handler 边界。正确的做法需要结合 `HandlerDepth`（Phase 2c 标注）来做精确匹配。

### 2. DecompileNestedCodeObjects 需要集成到 seq-blocks 路径

当前实现够用但被禁用，因为：
- `BuildWithSequentialBlocks` 的 stmts 来自 `GenerateAstStatementsHybrid`，其结构不同
- `ConvertChildCodesToFunctionDefs` 已在 seq-blocks 路径中处理大部分情况
- 需要先跑通非 seq 路径确认实现正确

### 3. StructuralValidator 可用但默认关闭

通过 `--show-structural-validation` 可启用。启用后输出：
```
[STRUCT_VALIDATE] FAIL R1 @0x...: seq-if-else: ...
[STRUCT_VALIDATE] FAIL R3 @0x...: seq-loop: ...
[STRUCT_VALIDATE] 5 structural issues: R1=2, R3=0, R5=3
```

## 后续（Phase 9+）

| 待办 | 优先级 | 说明 |
|------|--------|------|
| ET 严格映射修正 | P1 | 需结合 HandlerDepth + overlap 逐步验证 |
| DecompileNestedCodeObjects 激活 | P1 | 先在非 seq-blocks 路径启用，验证无误后启用 seq 路径 |
| COME_FROM 自动修复 | P2 | 基于 StructuralValidator 诊断实现 R1/R5 自动修复 |
