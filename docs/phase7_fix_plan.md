# Seq-Blocks Phase 7 修复执行计划

**目标**: 将白盒测试通过率从 251/405 (61%) 提升到 340/405 (85%)+

---

## 修复路线图

### Batch 1: P0 — RUNTIME_ERROR 崩溃修复

**目标**: 消除 55 个 RUNTIME_ERROR，解锁 enum/functools/reprlib/l8/l9

**步骤**:

- **1a**: 定位 `[SEQ_BUILD_HYBRID]` 崩溃根因
  - 方法: 在 `GenerateStatementsFromSeqBlockHybrid` 中输出 `seqBlock.ParentStructure.Type` 和 `structureHeaders.Contains`
  - 出问题的 seqBlock 的 SourceBlocks 是否跨越了控制结构边界？
  - 检查 `BuildSequentialBlockGraph` 中 succ 映射是否正确

- **1b**: 修复 `[SEQ_BUILD_FOR]` 崩溃
  - `BuildForLoopStructureStatements` 中 `ExtractIterExpression`/`ExtractLoopVariable` 失败
  - 在 seq-blocks 模式下，这些方法从 `forLoop.Header.SourceBlocks[0]` 提取 — 但 seqBlock 的 SourceBlocks 可能包含多个基本块，选择第一个不一定正确
  - 修复: 改为从 forLoop.Header.Instructions 中直接解析 iter/loopVar

- **1c**: 验证: `enum`.`3.10`、`functools`.`3.10` 从 RUNTIME_ERROR 变为具体问题

### Batch 2: P0 — BARE_EXPR 消除

**目标**: 将 BARE_EXPR 从 113 降到 <30

**步骤**:

- **2a**: 控制结构 body 结束后的 `return None` / `raise` 泄漏
  - 根因: StackMachine 的 ExprStack 在主遍历未清空，控制结构结束后栈上剩余表达式被输出
  - 修复: 在 `GenerateStatementsFromSeqBlockHybrid` 中，对 `ParentStructure != null` 且 `structureHeaders.Contains(sb.Id)` 的块，返回前清空栈

- **2b**: 裸 `name` / `cls.__bases__` 等表达式
  - 根因: StackMachine 输出 Load 指令作为 ExprStmt，应被下一指令消费
  - 修复: 在 `DecompileSequentialBlocks` 后，对每个 seqBlock 的 Statements 做死代码消除（去掉孤立 Load 表达式）

- **2c**: 验证: `abc`.`3.10`、`reprlib`.`3.10`、`test_minimal_if`.`3.10` 的 BARE_EXPR 消除

### Batch 3: P1 — REDUNDANT_PASS/RAISE 清理

**目标**: REDUNDANT_PASS 从 91 降到 <10，REDUNDANT_RAISE 从 27 降到 <5

**步骤**:

- **3a**: 冗余 pass 消除
  - 方法: 在每个 BuildStructureStatements 方法中，合并连续 pass
  - 特别处理: for/while 的 else 空 body → 仅最后一个 pass（而非 body 每个块一个）

- **3b**: 冗余 raise 消除
  - handler 块 raise 泄漏: handler 的 `raise` 在被 `LinkControlStructures` 标记后仍在主遍历中输出
  - 修复: `GenerateStatementsFromSeqBlockHybrid` 中，对 `ParentStructure == tryStruct` 的 seqBlock 先跳过，由 `BuildTryStructureStatements` 统一处理

### Batch 4: P2 — Try/Except 结构准确性修复

**目标**: ELSE_CONTAINS_FINALLY (11) → 0，EMPTY_TRY (5) → 0，CLEANUP_LEAK (5) → 0

**步骤**:

- **4a**: `MarkStructureBlocksProcessed` 区域覆盖修复
  - 目前 finally 块的 seqBlock 未全部标记为已处理 → handler 块残留
  - 修复: 在 `LinkControlStructures` 中，对 try 的 exceptHandlers 范围内的所有 seqBlock 设置 ParentStructure

- **4b**: finally vs else 边界修复
  - 检查 `ParseTryStructure` 对 ExceptionTable 的 IsFinally 判定
  - 对 3.10- 版本检查 SETUP_FINALLY → POP_BLOCK → END_FINALLY 序列

### Batch 5: P2 — SYNTAX_ERROR 修复

**目标**: SYNTAX_ERROR (12) → 0

**步骤**:

- **5a**: async generator vs async function
  - `ConvertChildCodesToFunctionDefs` 中 `co_flags & CO_ASYNC_GENERATOR` 判定
  - seq-blocks 模式下 `_codeObject.Version` / `_codeObject.Flags` 是否正确传递到嵌套函数的 `FunctionDef` 节点

- **5b**: comprehension 中 yield
  - `ConvertComprehensionCalls` 在 seq-blocks 中未正确处理 generator 表达式的 yield

---

## 验证策略

### 增量验证（per-batch）

```
dotnet build -c Release
python3 test_data/whitebox_test.py   # 自动生成新报告
diff 新旧报告                          # 检查每个 batch 的改进
```

### 关键里程碑

| 批次 | 预期通过 | 主要改善 | 验收标准 |
|------|---------|---------|---------|
| Batch 1 | 306 (76%) | RUNTIME_ERROR 消除 | enum/functools/reprlib 可从 RUNTIME_ERROR 变为其他问题 |
| Batch 2 | 330 (81%) | BARE_EXPR 大幅减少 | abc/reprlib/try_simple 的裸表达式消除 |
| Batch 3 | 370 (91%) | PASS/RAISE 清理 | loop_else/l2_exception 的 pass 降 <5 |
| Batch 4 | 385 (95%) | Try 结构准确 | test_try_simple 无 ELSE_CONTAINS_FINALLY |
| Batch 5 | 395 (97%) | Syntax 正确 | 所有用例通过 ast.parse |

---

## 核心风险

1. **Fallback 降级** — 如果 `VerifyNoOrphanBlocks` 失败，整个 seq-blocks 降级到 `BuildFallback`。这可能导致通过率**下降**而非上升。需确保 MergeLinearChain 的边界条件（with/try/if 头检测）正确。

2. **回归** — 修复一个结构可能破坏另一个。每批次后需全量回归验证。

3. **3.14 特有操作码** — LOAD_FAST_BORROW_314 / LOAD_SPECIAL 等新指令在 StackMachine 中可能未正确处理，导致 seqBlock 反编译失败。
