# 反编译器控制流架构分析与解耦方案

## 一、整体数据流图

```
源码(.py) → 编译(.pyc) → PycReader
    ↓
BlockScanner.Scan()
    ├── MarkLeaders()     → Leader 集合
    ├── SplitAtLeaders()  → [Block₀, Block₁, ...]
    ├── LinkBlocks()      → block.Successors 填充
    ├── MergeOrphanBlocks() → 合并 RETURN_VALUE 后孤儿
    └── MarkBlockProperties() → Entry/Exit 标志
    ↓
ControlFlowScanner.Analyze()
    ├── BuildCFG()       → CFG(Entry, Blocks[...])
    ├── CreateSyntheticExit() → Exit 添加到无后继的块
    ├── ComputeImmediateDominators()
    ├── DetectNaturalLoops()
    └── BuildStructuredCFG()
    ↓
BlockDecompiler.DecompileBlocks()
    └── 每块 → StackMachine.Execute() → flat statements
    ↓
AstBuilder.Build(cfg)
    ├── BuildStatements(cfg.Entry, visited)  ─── 主路径
    │   └── BuildStatementsInternal(block)    ─── 每块的入口
    │       ├── [A] LoopHeader?  → BuildLoop()
    │       ├── [B] FOR_ITER?    → BuildForLoop()
    │       ├── [C] SETUP_WITH?  → BuildWithFromBlock()
    │       ├── [D] ET覆盖?      → BuildTryFromExceptionTable()
    │       │                     → BuildMatchFromExceptionTable()
    │       │                     → visited.Contains(block)? → return [BUG!]
    │       ├── [E] 条件分支?     → BuildIfElse()
    │       ├── [F] match/case?  → BuildMatchFromInline()
    │       └── [G] 平坦语句     → flat stmts + 后继递归
    │
    ├── 孤儿块恢复 (orphan recovery)
    │   ├── handler_pre    → 跳过 [语句丢失!]
    │   ├── for_iter      → BuildForLoop()
    │   ├── jump_cond     → 提取前缀语句
    │   ├── isTerminalJump → 跳过
    │   ├── LooksLikeClassBody → ClassDef
    │   └── 其他          → CommentBlock(# orphan)
    │
    ├── PostProcessFunctionDefs()  → Assign→FunctionDef/ClassDef
    ├── ConvertChildCodesToFunctionDefs() → orphan 子代码→FunctionDef
    └── ConvertComprehensionCalls() → genexpr→ListComp
```

## 二、BuildIfElse 流程图

```
BuildIfElse(header, visited)
  ├── 提取 headerInitStmts (条件前的初始化语句)
  ├── ExtractCondition(header) → testExpr
  ├── bodyBranch = FindFallthrough(header)
  ├── afterBranch = FindBlockByOffset(targetOffset)
  │
  ├── OR短接链检测 (isOrChain)
  │   ├── → 交换 bodyBranch/afterBranch
  │   └── 进入 OR 合并逻辑
  │
  ├── 简单OR表达式检测 (isSimpleOrExpr)
  │   └── return BooleanOp(Or, ...)
  │
  ├── 简单AND表达式检测 (isSimpleAndExpr)
  │   └── return BooleanOp(And, ...)
  │
  ├── While循环检测 (isWhileLoop)
  │   └── return While(...)
  │
  ├── bodyStmts = GetStructuredBlockStmts(bodyBranch, visited)
  │
  ├── else 子句检测 (isElseClause)
  │   ├── afterBranch → BuildBlockOnly → orelse (else体)
  │   └── afterBranch后继 → tailCode
  │
  ├── elif 链检测
  │   └── afterStmts首条为 If → orelse = elif链
  │
  ├── result.AddRange(headerInitStmts)
  ├── result.Add(If(testExpr, bodyStmts, orelse))
  ├── result.AddRange(tailCode)
  └── return result
```

## 三、BuildStatementsInternal 完整流程

```python
def BuildStatementsInternal(block, visited):
    stmts = []
    result = _blockResults[block.Id]
    
    # ============ Phase A: 块类型检测 ============
    
    # A1: 循环头
    if block.Flags.LoopHeader:
        return BuildLoop(block, visited)
    
    # A2: FOR_ITER / 列表推导式
    hasForIter = any(instr.Opcode == FOR_ITER)
    hasListAppend313 = any(instr.Opcode == LIST_APPEND_313)
    if (hasForIter or hasListAppend313) and not LoopHeader:
        # 检测 FOR_ITER 前驱 → BuildForLoop
        # 如果没找到 → 列表字面量（fall through）
    
    # A3: With语句
    if SETUP_WITH in block.Instructions:
        return BuildWithFromBlock(block, visited)
    
    # ============ Phase B: 平坦语句获取 ============
    
    stmts.AddRange(result.Statements)  # BlockDecompiler 的平坦语句
    visited.Add(block)
    
    # ============ Phase C: ET 异常表匹配 ============
    
    # C1: 旧式 try 体 (POP_BLOCK 模式)
    if tryBodyStmts := BuildTryFromExceptionTable(block, visited):
        stmts.AddRange(tryBodyStmts)
        # 标记 handler 块为 visited
        # 处理 handler 后继（类定义等）
        return stmts
    
    # C2: 3.11+ ExceptionTable 匹配
    if ET.Count > 0 and _buildTryDepth == 0:
        matchingEntry = ET 匹配块范围
        if matchingEntry != None:
            # 多条目 try/except
            # C2a: 连续条目 → 分别处理 + 合并 visited
            # C2b: 单一条目 → BuildTryFromExceptionTable
            # C2c: handler 后继处理
            # C2d: try/except 后的 else 体（JumpTarget 间未访问块）
            return stmts  # ← [BUG] 短路条件分支检测!
    
    # ============ Phase D: 条件分支检测 ============
    
    # D1: match/case
    if matchStmts := BuildMatchFromExceptionTable(block, visited):
        return matchStmts
    
    # D2: 已处理标记检查
    if visited.Contains(block):  # ← [BUG] 应该用 _processedBlockIds
        # 处理后继 → return
    
    # D3: 条件分支
    if IsConditionBranch(block):
        return BuildIfElse(block, visited)
    
    # D4: match/case 内联
    if COPY + MATCH_CLASS pattern:
        if matchStmts := BuildMatchFromInline(block, visited):
            return matchStmts
    
    # ============ Phase E: 兜底 ============
    
    # E1: 平坦语句（如果之前没加过）
    if result == null or !result.IsSuccess:
        stmts.Add(CommentBlock)
    else:
        stmts.AddRange(result.Statements)
    
    # E2: 后继块递归
    for succ in block.Successors:
        if not visited.Contains(succ):
            stmts.AddRange(BuildStatements(succ, visited))
    
    return stmts
```

## 四、可解耦的独立问题

### 🔧 P0: `visited.Contains(block)` 短路 `IsConditionBranch`

- **位置**: AstBuilder.cs:1079-1088
- **症状**: wrapper 函数体只有 `key=(id(self),42)`，if/try/finally/return 全部丢失
- **根因**: `visited.Add(block)` 先在 line ~1034 执行，然后 `visited.Contains(block)` 在 line 1079 检查 → 总是 true → 在到达 `IsConditionBranch` 之前就 return 了
- **修改**: `visited.Contains(block)` → `_processedBlockIds.Contains(block.Id)`

### 🔧 P1: `handler_pre` 块跳过导致语句丢失

- **位置**: AstBuilder.cs:152-156
- **症状**: 内层函数中 try/finally/return 块被分类为 handler_pre → 跳过
- **修改**: handler_pre 块的语句应该被添加到当前函数体，而不是跳过

### 🔧 P2: `ExtractCondition` 丢弃 STORE_FAST 产生的赋值语句

- **位置**: AstBuilder.cs:5642-5643
- **症状**: 条件分支前的初始化语句在条件提取时丢失
- **修改**: 收集 `stackMachine.Execute()` 的返回值并返回给调用者

### 🔧 P3: 孤儿块恢复中 `isTerminalJump` 跳过条件块

- **位置**: AstBuilder.cs:177-187
- **症状**: POP_JUMP_IF_TRUE/FALSE 的 orphan 块被跳过
- **修改**: `jump_cond` 分支已提取前缀，但仅当 `Count > 1` 时触发。减小阈值或移除 count 检查

## 五、深度耦合问题（需顶层设计）

### 🔗 问题5: `visited` 集和 `stmts` 列表在 ET 处理和条件分支处理间共享

- **本质**: 一块一次处理模式。一个块要么被当作 try/except，要么被当作 if/else
- **方案B（推荐）**: 块类型标记 — 在 BlockScanner 阶段为每块打类型标签

### 🔗 问题6: 孤儿块恢复是后处理，不是内联处理

- **本质**: 孤儿块语句被 APPEND 到末尾，位置错误
- **方案**: 确定性块遍历 — 用显式队列代替递归 visited

### 🔗 问题7: `BuildIfElse` 的 else 子句检测多次出现且逻辑重复

- **本质**: 3 处独立的 else 检测逻辑，行为不一致
- **方案**: 统一 `IsElseTarget` 函数

---

## 六、改造计划

### Phase A: P0-P3 立即修复（当前执行）

| 步骤 | 文件 | 修改 |
|:-----|:-----|:-----|
| P0 | `AstBuilder.cs:1079` | `visited.Contains(block)` → `_processedBlockIds.Contains(block.Id)` |
| P1 | `AstBuilder.cs:152-156` | handler_pre 不跳过，恢复语句 |
| P2 | `AstBuilder.cs:5642-5643` | ExtractCondition 收集赋值语句 |
| P3 | `AstBuilder.cs:203-223` | jump_cond 前缀提取阈值降低 |

### Phase B: 架构级重构（后续）

| 步骤 | 说明 |
|:-----|:------|
| B1 | 块类型标记系统 |
| B2 | 确定性块遍历队列 |
| B3 | 统一 else 子句检测 |
| B4 | 异常表与条件分支解耦（两阶段 pass） |
