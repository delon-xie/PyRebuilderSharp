# Bugfix: CFG for-loop / orphan / backward-jump fixes

**Commits**: `c0e75fd`, `08f8db0`, `c5a6a82`, `68fc56d`

## Scope

Four related fixes for CFG reconstruction issues in for-loops, orphan block tracking, and backward-jump detection.

---

### 1. FOR_ITER exit successor not processed (`c0e75fd`)

**Symptom**: For-loops swallow next block after loop body. The block immediately following the loop body is not decompiled, causing data loss.

**Root Cause**: `AstBuilder.BuildStatementsInternal` processes FOR_ITER by decompiling the loop body, but does not then process the successor/exit block of the loop. The exit block remains in the visited set and is excluded from further BuildStatements calls.

**Fix**: After processing the FOR_ITER loop body, remove the exit block from visited and call BuildStatements on it:
```csharp
// After for-loop processing, handle the exit block
var exitBlock = forIterBlock.GetSuccOrNext();
if (exitBlock != null && _processedBlockIds.Add(exitBlock.Id))
{
    visited.Remove(exitBlock);
    var exitStmts = BuildStatements(exitBlock, visited);
    if (exitStmts.Count > 0)
        stmts.AddRange(exitStmts);
}
```

---

### 2. Orphan tracking — GetStructuredBlockStmts / BuildBlockOnly not tracking (`08f8db0`)

**Symptom**: Blocks processed via `GetStructuredBlockStmts` or `BuildBlockOnly` are not registered in `_processedBlockIds`, causing them to appear as orphans in the crash collector.

**Fix**: Add `_processedBlockIds.Add()` calls in both methods.

---

### 3. For-loop body over-collection (`08f8db0`)

**Symptom**: `CollectBodyBlocks` for for-loops collects blocks that are not part of the loop body (code after the for-loop).

**Root Cause**: When a for-loop body contains a jump back to the loop header, `CollectBodyBlocks` follows the jump target and collects all blocks up to the end of the function, including code that should be after the loop.

**Fix**: Added `exitBlock` parameter to `CollectBodyBlocks` — stop collecting when the exit block is reached:
```csharp
private List<BasicBlock> CollectBodyBlocks(BasicBlock entry, BasicBlock? exitBlock)
{
    var body = new List<BasicBlock>();
    var workList = new Queue<BasicBlock>();
    var visited = new HashSet<int>();
    workList.Enqueue(entry);
    while (workList.Count > 0) {
        var block = workList.Dequeue();
        if (!visited.Add(block.Id)) continue;
        if (exitBlock != null && block.Id == exitBlock.Id) continue;
        body.Add(block);
        foreach (var succ in block.Successors)
            if (!visited.Contains(succ.Id) && succ.Id != entry.Id)
                workList.Enqueue(succ);
    }
    return body;
}
```

---

### 4. Backward-jump false positive in wordcode (`08f8db0`)

**Symptom**: Wordcode for-loops pre-3.10 thought every for-loop body was a true loop-re-entry, because raw jump args are always < the block's own offset in wordcode, triggering false positive loop-continue detection.

**Root Cause**: In wordcode (3.6-3.14), raw jump args are 2-byte values or offsets that happen to be numerically smaller than the current block's offset, falsely triggering `IsBackwardJump` detection.

**Fix**: Compare resolved (byte-offset) jump targets instead of raw args. Use `ResolveJumpTarget` output for comparison.

---

### 5. JUMP_BACKWARD continue detection in 3.12+ (`c5a6a82`)

**Symptom**: `if not X: pass else: break` patterns in 3.12+ produce incorrect output with redundant continue statement.

**Root Cause**: `BuildRestrictedIfElse` didn't handle `JUMP_BACKWARD` (the 3.12+ replacement for `JUMP_ABSOLUTE` used in continue patterns).

**Fix**: Added `JUMP_BACKWARD` support and body/else swap logic:
```csharp
case Opcode.JUMP_BACKWARD:
    // `if not X: pass else: break` → `if X: body`
    break;
```
Plus conditional swap: when body is empty and else has `pass`, swap body and else content.

## Affected Code

- `src/PyRebuilderSharp.Core/Builders/AstBuilder.cs` — FOR_ITER, orphan tracking, body collection, backward jump, continue detection

## Regression

938/938 succeeded, 0 failed, 0 crashes ✅
