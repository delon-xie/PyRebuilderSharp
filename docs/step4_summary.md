# Step 4 总结文档

> 日期: 2026-07-10
> Phase 8 实施方案第四步完成
> 实现: PostDominatorScanner + StructuralValidator + AstBuilder 集成

---

## 成果清单

```
Step 4 → ✅
├── PostDominatorScanner.cs ──────────────────────────────── ✅
│   ├── ComputePostDominators() — 反转 CFG → 后支配树
│   ├── BuildComeFromMap() — 跳转 target→source 映射
│   ├── IsPostDominatedBy() — 后支配查询 API
│   ├── ShouldGenerateComeFrom(→ ClassifyJump) — 跳转分类
│   │   ├── POP_JUMP_IF_* → Conditional
│   │   ├── FOR_ITER → ForLoopEnd
│   │   └── JUMP_FORWARD/ABSOLUTE/BACKWARD → 跳过
│   └── BuildReverseCFG() — 边反向 + 入口/出口对调
│
├── StructuralValidator.cs ────────────────────────────────── ✅
│   ├── R1: if-elif 链验证（ConditionHeader 后支配检查）
│   ├── R2: try-except handler 归属验证
│   ├── R3: loop-body vs break 验证
│   ├── R4: else-body 归属验证
│   └── R5: ExceptionTable 异常边验证
│
└── 集成 ──────────────────────────────────────────────────── ✅
    ├── AstBuilder.Build() — 每个文件反编译都跑后支配树
    ├── BuildWithSequentialBlocks() — 通过 ShowStructuralValidation 开关控制
    ├── DecompileOptions.ShowStructuralValidation — 配置选项
    └── 默认关闭，向下兼容
```

## 技术难点

### 1. `ControlFlowGraph.Entry/Exit` 是 `init` 属性

不能在方法中赋值 `cfg.Entry = xxx`。解决：在 `new ControlFlowGraph { Entry = ..., Exit = ... }` 初始化器中设置。

### 2. `ISequentialControlStructure` vs `ControlStructure` 是两套独立类型层次

- `ControlStructure` — ControlFlowScanner 的输出（IfElseStructure、LoopStructure、TryStructure）
- `ISequentialControlStructure` — SequentialBlockBuilder 的输出（IfElseControlStructure 等）

StructuralValidator 设计为验证 `ControlStructure`，但 seq-blocks 路径产生 `ISequentialControlStructure`。
**解决方案**：验证器保留完整代码但暂不激活针对 ISequentialControlStructure 的验证，在 Step 5 中适配。

### 3. 后支配树不修改 AST，无回归风险

所有指标与 Step 3 完全一致，验证了零回归。

## 增量文件

| 文件 | 行数 | 说明 |
|------|------|------|
| `src/.../Scanners/PostDominatorScanner.cs` | ~280 | 后支配树 + COME_FROM |
| `src/.../Scanners/StructuralValidator.cs` | ~260 | R1-R5 验证规则 |
| `src/.../Core/DecompileOptions.cs` | +3 | `ShowStructuralValidation` 属性 |

## Step 4+ 待办

1. **Step 5 适配**：让 StructuralValidator 也处理 `ISequentialControlStructure` 类型
2. **COME_FROM 自动修复**：基于高频 FAIL 实现 R1-R5 自动修复逻辑
3. **SeqBlock.ComeFromSources** 标注字段：在 SequentialBlock 上挂接 COME_FROM 信息
