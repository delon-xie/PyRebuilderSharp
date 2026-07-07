# CFG 问题深度分析与解决方案

> 本文档分析 PyRebuilderSharp 中 3 个 CFG 相关核心问题的根因，
> 评估修复方案和风险，决定是否推进。

---

## 前置知识：PyRebuilderSharp 的 CFG 架构

```
源码 .pyc → PycReader → 指令列表
  → BlockScanner → 基本块（BasicBlock）
    → ControlFlowScanner → 支配树 + 自然循环检测 → LoopStructure
      → AstBuilder → 结构体解析（if/while/for/try）
        → PythonCodeGenerator → 输出
```

**关键模块职责**：

| 模块 | 输入 | 输出 | 算法 |
|:-----|:------|:------|:------|
| `BlockScanner` | 指令列表 | 基本块 + CFG 边 | 领导指令检测 |
| `ControlFlowScanner` | 基本块 | `LoopStructure` 列表 | 支配树 + 回边分析 |
| `AstBuilder` | 基本块 + LoopStructure | AST (If/While/For/Try) | 块级结构体解析 |

**支配树 - 回边分析的核心**：

Block A 支配 Block B 当且仅当所有从 CFG 入口到 B 的路径都经过 A。当 pred 的回边从高偏移跳转到低偏移的 header 时，如果 header 支配 pred，则这条边是循环回边。

---

## 问题 1：`while True` + `break` → 嵌套 `while`（l1_7）

### 现象

```python
# 原始
while True:
    i += 1
    if i > 10: break     # ← 语义为：条件成立时退出循环
    if i % 2 == 0: continue
    total += i
return total

# 当前反编译
while True:
    while True:           # ← 错误：if-break 被识别为嵌套 while
        i += 1
        return total      # ← 错误：break 被改写为 return
    total += i            # ← i % 2 == 0 的 continue 逻辑丢失
```

### 字节码布局 (l1_7 @ 3.10)

```
offset  │ 指令
────────┼──────────────────────────────────
0x0000  │ LOAD_CONST 0; STORE_FAST i; LOAD_CONST 0; STORE_FAST total
0x0008  │ NOP                            ← outer while True 入口
0x000A  │ LOAD_FAST i; LOAD_CONST 1; INPLACE_ADD; STORE_FAST i  ← i += 1
0x0014  │ LOAD_FAST i; LOAD_CONST 10; COMPARE_OP 4  ← i > 10
0x0018  │ POP_JUMP_IF_FALSE → 0x0020     ← if i > 10: break else continue
0x001C  │ NOP; LOAD_FAST total; RETURN_VALUE  ← break: return total
0x0020  │ LOAD_FAST i; ... COMPARE_OP 2  ← i % 2 == 0
0x0028  │ POP_JUMP_IF_FALSE → 0x002E     ← if i % 2 == 0: continue
0x002A  │ JUMP_ABSOLUTE → 0x0008         ← continue: 回跳 outer header
0x002C  │ LOAD_FAST total; LOAD_FAST i; INPLACE_ADD; STORE_FAST total  ← total += i
0x0034  │ JUMP_ABSOLUTE → 0x000A         ← 循环体回跳
```

### CFG 块划分

| 块 | 偏移 | 指令 | 后继 |
|:---|:-----|:-----|:-----|
| A | 0x0000 | i=0, total=0 | → B |
| **B** | **0x0008** | **NOP** | **→ C, C'** |
| **C** | **0x000A** | **i+=1, i>10, POP_JUMP_IF_FALSE** | **→ D(ft), E(jmp)** |
| D | 0x001C | NOP, RETURN_VALUE | → exit |
| **E** | **0x0020** | **i%2==0, POP_JUMP_IF_FALSE** | **→ F(ft), B(jmp)** |
| F | 0x002C | total+=i | → C |
| G | 0x002A | JUMP_ABSOLUTE | → B |
| exit | synthetic | — | — |

### 支配树分析

```
入口 (0x0000)
 │
 ├── B (0x0008) 支配：A, B, C, D, E, F
 │    │
 │    └── C (0x000A) 支配：D(部分)
 │         │
 │         └── E (0x0020) 支配：F
 │              │
 │              ├── F (0x002C) 支配：C(部分)
 │              │
 │              └── G (0x002A) 支配：B(部分)
```

**关键支配关系**：
- B (0x0008) 支配 C (0x000A) ✓ → B 可以成为循环头
- C (0x000A) 支配 E (0x0020) ✓ → C 可以成为循环头
- C (0x000A) 支配 F (0x002C) ✓
- **C (0x000A) 不支配 G (0x002A)** ❌ （G → B 的回边不经过 C）

### 回边分析（DetectNaturalLoops）

```
回边 1：G(0x002A) → B(0x0008)  ✓ B 支配 G(0x002A)
         创建循环 L1：header=B, body={B, C, D, E, F, G}

回边 2：F(0x002C) → C(0x000A)  ✓ C 支配 F(0x002C)
         创建循环 L2：header=C, body={C, D, E, F}
           DetermineLoopType(C) → 有 POP_JUMP_IF_FALSE → LoopType.While
```

**问题根因**：`DetectNaturalLoops` 为每个回边创建独立的循环结构。回边 F → C 创建了 L2，其 header C 含有 `POP_JUMP_IF_FALSE`，`DetermineLoopType` 返回 `While`。但实际上 L2 是 L1 的子集（嵌套），且 C 的 `POP_JUMP_IF_FALSE` 是内层的 `if-break`，不是 while 条件。

### 修复方案：4 种选项

#### 方案 A：跳过已存在的循环体内的回边（推荐 — 最小改动）

在 `DetectNaturalLoops` 中，创建循环 L1 后，标记 L1 的 body 块。当处理新回边时，如果 header 已经在 L1 的 body 中，且 L1 是 outer 循环，则跳过此回边（不创建新循环）：

```csharp
// DetectNaturalLoops 中，for each (block, pred):
// 在创建 loopBody 后：
if (type != LoopType.For) // for 循环需要独立检测（嵌套推导式）
{
    // 检查 header 是否已在更外层循环的 body 中
    var outerLoop = loops.FirstOrDefault(l => l.BodyBlocks.Contains(block) && l.Header != block);
    if (outerLoop != null)
        continue; // header 已在外部循环体内 → 不创建新循环
}
```

**优点**：1 行改动，不影响 for-loop（嵌套推导式需要独立循环）
**风险**：可能丢失合法的嵌套循环（如 while 内嵌 while）
**适用场景**：l1_7 的模式（`while True` 内嵌 `if-break`）被正确识别为单层循环

#### 方案 B：修正 DetermineLoopType（中等改动）

在 `DetermineLoopType` 中，当 header 有 `POP_JUMP_IF_FALSE` 时，检查其跳转目标是否**仍在循环体内**。如果目标在体内，则此条件不是循环条件，而是内部 if-break：

```csharp
private LoopType DetermineLoopType(BasicBlock header, List<BasicBlock> loopBody)
{
    if (hasForPattern) return LoopType.For;
    
    // 检查 header 的条件跳转是否跳出循环体
    var lastInstr = header.Instructions.LastOrDefault();
    if (lastInstr != null && JumpHelper.IsConditionalJump(lastInstr.Opcode))
    {
        var jumpTarget = ResolveJumpTarget(lastInstr, ...);
        var targetBlock = loopBody.FirstOrDefault(b => b.StartOffset <= jumpTarget && jumpTarget < b.EndOffset + 2);
        if (targetBlock != null && targetBlock != header)
        {
            // 跳转目标仍在循环体内 → 不是 while 条件，是内部 if
            return LoopType.Infinite;
        }
    }
    
    return hasCondition ? LoopType.While : LoopType.Infinite;
}
```

**优点**：增强语义准确性，还可以识别其他 `while True` + `if-break` 模式
**风险**：需要访问指令跳转解析（BlockScanner 的私有方法需提取）

#### 方案 C：循环嵌套消减（较大改动）

在 `BuildStructuredCFG` 中或 `AstBuilder.Build` 中，对所有检测到的循环做后处理：如果一个循环的 header 在另一个循环的 body 中，且不是 for 循环，则将此内层循环标记为 infinite（内部 if-break）而非 while：

```csharp
// 在 loops 按 body 大小排序后：
foreach (var inner in loops)
{
    var outer = loops.FirstOrDefault(l => 
        l.BodyBlocks.Contains(inner.Header) && l.Header != inner.Header);
    if (outer != null && inner.Type == LoopType.While && outer.Type != LoopType.For)
    {
        // 内层 while 实际上是 outer 的内部 if-break
        inner.Type = LoopType.Infinite;
    }
}
```

#### 方案 D：BuildWhileLoop 内部修复（当前方案 — 不彻底）

在 `BuildWhileLoop` 中检测 header 含有 `INPLACE_ADD/STORE_FAST` 等 body 操作 → `testExpr = True`，再通过 body/exit 块交换和 header body 合并来处理。

**已实现**，但仍有嵌套 while 输出（因为 `ControlFlowScanner` 创建了两个 LoopStructure，AstBuilder 按结构列表逐个处理）。

### 推荐方案：组合 A + B

**方案 A** 解决「为内部 if-break 创建错误循环」的检测问题。**方案 B** 作为语义增强，确保即使循环被创建，也被正确识别为 `Infinite` 而非 `While`。

**实现量**：方案 A 约 5 行代码，方案 B 约 15 行代码

---

## 问题 2：死代码出现在 return 之后（l1_4）

### 现象

```python
def l1_4_while_simple():
    i = total = 0
    while i < 10:
        total += i
        i += 1
    return total
    total += i    # ← 死代码，不可达
    i += 1        # ← 死代码，不可达
```

### 根因分析

在 `l1_4` 的 while 循环中，CFG 结构为：

```
  while 头 (POP_JUMP_IF_FALSE → exit)
    │
    ├── body: total+=i; i+=1; JUMP → while 头
    │
    └── exit block: return total → (后继: 代码继续)
```

在 `BuildWhileLoop` 中，`CollectBodyBlocks(bodyEntry, header, bodyBlocks, visited, elseOffset)` 收集 body 块。`bodyEntry` 是 body 的第一个块（total+=i），`elseOffset` 是 exit 块（return total）的偏移。

`CollectBodyBlocks` 遍历 body 块的前驱和后继，包含了 `total+=i; i+=1` 块，但不包含 exit block（被 elseOffset 过滤）。然后 `visited.Remove(bb)` 把这些 body 块从 visited 中移出，让 `GetStructuredBlockStmts` 后续重新处理。

死代码的来源：
1. `BuildWhileLoop` 返回 `[While(cond, body)]` 后，`BuildStatementsInternal` 中调用此 while 的入口会继续处理 while 的**后继块**
2. while 的后继块包括 exit block（return total）和... 循环体块！
3. 体块被 `visited.Remove(bb)` 恢复后，成为未访问的 successor -> 被重新处理

**关键路径**：

```
BuildStatementsInternal(while_header)
  → GetStructuredBlockStmts → BuildLoop → BuildWhileLoop
    → CollectBodyBlocks → visited.Remove(bb)  # 体块被释放
    → 返回 While(...)
  → 继续处理 while_header 的后继
    → 后继包括 exit block + 体块（被释放后再次可见）
    → exit block 输出 Return(total)
    → 体块被重新处理为死代码
```

### 修复方案

在 `BuildWhileLoop` 返回后，由调用方重新检查 while_body 的后继块是否已被正确消费。如果体块已经被构建到 While 节点中，不应再通过 successor 链路处理。

**方案 A：在 BuildWhileLoop 中标记 body 块为 permanent visited（推荐）**

`BuildWhileLoop` 调用 `CollectBodyBlocks` 后，体块被加入 `bodyBlocks`，然后通过 `visited.Remove(bb)` 释放以便嵌套处理。但在返回前，应**重新标记体块为 `_processedBlockIds`**，确保外层不重复处理：

```csharp
// BuildWhileLoop 返回前：
foreach (var bb in bodyBlocks)
    _processedBlockIds.Add(bb.Id);
```

这可以防止 `BuildStatementsInternal` 在处理 while 后继块时重复遍历体块。

**方案 B：在 GetStructuredBlockStmts 中增加死代码检测**

当 while 的 exit block 包含 `RETURN_VALUE` 时，其后继（死代码）不应被消费。但目前的终端检测（`stmts[^1] is Return → return`）未涵盖 `GetStructuredBlockStmts` 返回的 flat path 路径。

---

## 问题 3：while-else 条件检测错误（l1_9 / loop_else）

### 现象

```python
# 原始
def l1_9_while_else():
    i = 0
    while i < 5:
        if i == 10:
            break
        i += 1
    else:
        return "completed"    # ← else 子句
    return "broke"

# 反编译
def l1_9_while_else():
    i = 0
    while i < 5:
        if not i < 5:         # ← i==10 被改写为 not i<5
            pass
    return 'completed'         # ← else 体未关联到 while
    i += 1                     # ← 死代码
```

### 根因分析

while-else 的 bytecode 结构：
```
while 头 (0x0000): i=0
  ├─ 条件头 (0x0008): i<5 → POP_JUMP_IF_FALSE → else_block(0x002C)
  │   ├─ i==10 → POP_JUMP_IF_FALSE → (i+=1 block)
  │   │   └─ NOP, return "broke" (break: 跳过 else)
  │   └─ i+=1 → JUMP → 条件头
  └─ else_block (0x002C): return "completed"
```

**`IsLoopElseTarget` 的判定**（~L5269-5404）：

```csharp
// while 循环的 else 判定（~L5397-5401）:
bool isExitOnlyBlock = IsExitOnlyBlock(afterBranch);
return !isExitOnlyBlock;
```

`afterBranch` 是 while 循环的 else 候选块（`return "completed"`）。`IsExitOnlyBlock` 检查块是否仅含 `return None`/`return value`。对于 `LOAD_CONST 'completed'; RETURN_VALUE`，`IsExitOnlyBlock` 在行 5451-5454 返回 `true`：

```csharp
if (instrs.Count == 2 &&
    (instrs[0].Opcode == Opcode.LOAD_FAST || instrs[0].Opcode == Opcode.LOAD_NAME) &&
    instrs[1].Opcode == Opcode.RETURN_VALUE)
    return true;
```

所以 `isExitOnlyBlock = true`，导致 `!isExitOnlyBlock = false` → else 子句被丢弃。

**同时**，内部 `if i == 10: break` 被 `BuildIfElse` 处理。`BuildIfElse` 的目标块（`afterBranch`）是 else 候选块（`return "completed"`），被识别为 else 子句。`isExitOnlyBlock` 返回 true 但 `BuildIfElse` 的 else 检测逻辑（`IsElseTarget`）有不同的判定标准，结果为 `isElseClause = true`。条件表达式 `i == 10` 被取反 → `not i < 5`。

### 修复方案

**方案 A：修改 while-else 的 IsExitOnlyBlock 判定**（推荐 — 最小改动）

在 `IsLoopElseTarget` 的 while 分支中，改用更精确的判定：else 候选块应同时满足：
1. 不是单纯的 `return None`（过滤 void return）
2. 循环体内有跳过 else 的 break

```csharp
else if (isWhileLoop)
{
    // 检查循环体内是否有 break 跳过 else 块
    bool hasBreak = false;
    if (bodyBranch != null)
    {
        var visitedBlocks = new HashSet<BasicBlock>();
        var blockQueue = new Queue<BasicBlock>();
        blockQueue.Enqueue(bodyBranch);
        visitedBlocks.Add(bodyBranch);
        while (blockQueue.Count > 0 && !hasBreak)
        {
            var cur = blockQueue.Dequeue();
            foreach (var instr in cur.Instructions)
            {
                if (instr.Opcode == Opcode.POP_TOP && cur.Successors.Any(s => 
                    s.StartOffset > afterBranch.EndOffset))  // break: POP_TOP + JUMP 跳过 else
                { hasBreak = true; break; }
            }
            foreach (var succ in cur.Successors)
                if (succ.StartOffset < afterBranch.StartOffset && !visitedBlocks.Contains(succ))
                { visitedBlocks.Add(succ); blockQueue.Enqueue(succ); }
        }
    }
    return hasBreak;  // 有 break → else 是真实的 else 子句
}
```

**方案 B：分离 while-else 的 else 识别与 exit-only 判定**

不再用 `IsExitOnlyBlock` 做单点判定，而是检查 else 候选块的 predecessors 是否**只有**循环头的跳出路径（没有其他入口）：

```csharp
// 正确的 while-else 判定：
// else 块的 predecessors 应包含循环头（正常退出），可能也包含 body 块（条件失败退出）
// 但不应包含 body 外的其他块
bool isElse = afterBranch.Predecessors.Count <= 2 
    && afterBranch.Predecessors.Any(p => p == header || bodyBlocks.Contains(p))
    && !IsExitOnlyBlock(afterBranch);
```

---

## 综合风险评估

| 问题 | 影响范围 | 修复方案 | 代码行数 | 风险 | 优先级 |
|:-----|:--------|:---------|:--------:|:----:|:-----:|
| **L1: while True break 嵌套** | 1 文件 | A: 跳过体内回边 | ~5 | 低 | P1 |
| **L2: 死代码 after return** | 3 文件 | A: body块重新标记 processed | ~3 | 低 | P1 |
| **L3: while-else 条件** | 4 文件 | A: break 检测 | ~15 | 中 | P2 |

### 建议

3 个 CFG 问题中有 2 个（死代码、while-else）可以通过 3-5 行改动解决。while True break 嵌套问题需要 5 行（方案 A）但需要验证不影响合法的嵌套循环。

**建议推进**：先修复死代码和 while-else（约 10 行，低风险），再评估 while True break 修复对 for 循环嵌套的影响。

而 Level 2 的 try/except 塌陷（`BuildTryFromBlock` handler 识别）是独立的非 CFG 问题，可与 CFG 修复并行进行。
