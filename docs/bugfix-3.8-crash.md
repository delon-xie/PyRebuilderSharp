# Bugfix: 3.8 Crash — BlockScanner AddSuccessor NRE

**Date**: 2026-06-16
**Author**: Hermes Agent
**Commit**: `68fc56d` (part of)

## Symptom

Python 3.8 `.pyc` files cause a `NullReferenceException` when `BlockScanner.AddSuccessor` is called with a null `to` parameter.

```
Unhandled exception. System.NullReferenceException: Object reference not set to an instance of an object.
   at PyRebuilderSharp.Core.Scanners.BlockScanner.AddSuccessor(BasicBlock from, BasicBlock to)
```

## Root Cause

`BlockScanner.ResolveJumpTarget` returned incorrect targets for 3.6-3.9 wordcode bytecode, causing `FindBlockByOffset` to return null. The null block was then passed to `AddSuccessor(from, to)` which called `to.Predecessors.Add(from)` — NRE.

### Deeper Cause

**3.6-3.9 wordcode jump args are instruction indices, not byte offsets.**

In CPython 3.6, the wordcode format was introduced (Include/opcode.h, PEP 527). Each instruction is exactly 2 bytes: `[opcode, arg]`. Jump targets in 3.6-3.9 are stored as **instruction indices** (which instruction number to jump to), not byte offsets.

- CPython 3.6: `Python/compile.c` `assembler()` emits jump args as instruction counts
- CPython 3.10: Changed to byte offsets (`Python/compile.c` ~line 785, "jumps are absolute byte offsets")

The `*2` conversion (instruction index × 2 = byte offset) was missing for 3.6-3.9 wordcode.

## Fix Applied

### 1. `BlockScanner.AddSuccessor` null guard
Added null check before accessing `to.Predecessors`:
```csharp
private void AddSuccessor(BasicBlock from, BasicBlock? to)
{
    if (to == null) return;
    to.Predecessors.Add(from);
}
```

### 2. `BlockScanner.ResolveJumpTarget` wordcode *2
Added `is36To39Wordcode` detection and `*2` for all jump types in 3.6-3.9:
- `JUMP_ABSOLUTE`: `is36To39Wordcode ? arg * 2 : arg`
- `JUMP_FORWARD`/`FOR_ITER`: `offset + 2 + (is36To39Wordcode ? arg * 2 : arg)`
- `POP_JUMP_IF_*` (wordcode): `offset + 2 + (is36To39Wordcode ? arg * 2 : arg)`

### 3. Version detection
Detection: wordcode (all offsets even) + `IsWordOffset==false` → 3.6-3.9

### 4. `CodeObject.IsWordOffset` property
Added property to distinguish 3.10+ (arg already *2 in parser) from 3.6-3.9 (needs *2 in resolver).

## Version-Specific Affected Code

- `src/PyRebuilderSharp.Core/Scanners/BlockScanner.cs` — `ResolveJumpTarget()` (lines ~85-127)
- `src/PyRebuilderSharp.Core/Scanners/BlockScanner.cs` — `AddSuccessor()` (null guard)
- `src/PyRebuilderSharp.Core/Models/Bytecode/CodeObject.cs` — `IsWordOffset` property

## Regression Coverage

Before fix: 938 files, **1 crash** (3.8 abc.py)
After fix: 938 files, **0 crashes**, 938 succeeded
