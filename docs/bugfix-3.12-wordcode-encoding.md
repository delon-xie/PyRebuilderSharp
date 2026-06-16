# Bugfix: 3.12 Wordcode Name Encoding Issues

**Commits**: `bcec82b`, `72b6143`, `68fc56d`
**Date**: 2026-06-16

## Summary

Three related fixes for Python 3.12+ wordcode instruction encoding.

In Python 3.12, certain instruction arguments encode additional flags in the low bit:
- `LOAD_GLOBAL`: `(name_idx << 1) | push_null_flag`
- `LOAD_ATTR`: `(name_idx << 1) | self_or_null_flag`

Without decoding the `>>1` shift, the wrong name is loaded, producing semantically incorrect output.

## Details

### 1. LOAD_GLOBAL name encoding (commit `72b6143`)

**Symptom**: `set(cls, '__abstractmethods__')` instead of `hasattr(cls, '__abstractmethods__')` — wrong name loaded.

**Root Cause**: CPython 3.12 `LOAD_GLOBAL` encodes `(name_idx << 1) | push_null_flag` in the argument. The low bit `&1` indicates whether a null sentinel should be pushed (PEP 669 / new call protocol). When the push_null bit is set, `arg >>= 1` is needed to get the correct name table index.

**Reference**: CPython 3.12 `Python/ceval.c` LOAD_GLOBAL (or `Python/generated_cases.c.h` for 3.12+):
```c
// LOAD_GLOBAL
name_idx = oparg >> 1;
if (oparg & 1) {
    // push null sentinel for call protocol
    PUSH(null);
}
```

**Fix** (`src/PyRebuilderSharp.Core/Readers/PycReader.cs`):
```csharp
// Python 3.12+: LOAD_GLOBAL arg = (name_idx << 1) | push_null
if (hasPushNull && (arg & 1) != 0)
    arg >>= 1;
```

### 2. LOAD_ATTR name encoding (commit `bcec82b`)

**Symptom**: `cls.add` instead of `cls.__bases__` — wrong attribute name loaded.

**Root Cause**: CPython 3.12 `LOAD_ATTR` encodes `(name_idx << 1) | self_or_null_flag` in the argument. Similar to LOAD_GLOBAL, the low bit needs to be removed to get the correct name index.

**Reference**: CPython 3.12 `Python/generated_cases.c.h` LOAD_ATTR:
```c
name_idx = oparg >> 1;
```

**Fix** (`src/PyRebuilderSharp.Core/Readers/PycReader.cs`):
```csharp
// Python 3.12+: LOAD_ATTR arg = (name_idx << 1) | self_or_null
if (isPy312Plus && (arg & 1) != 0)
    arg >>= 1;
```

### 3. while→if root cause: LinkBlocks not passing codeObj (commit `bcec82b`)

**Symptom**: `while hasattr()` instead of `if not hasattr()` — infinite loop instead of conditional.

**Root Cause**: `BlockScanner.LinkBlocks` called `ResolveJumpTarget` without passing `codeObj`. Without `codeObj`, `codeObj?.IsWordOffset` was null → false → `is36To39Wordcode` was false → wordcode POP_JUMP_IF_TRUE's raw arg (which in 3.12+ wordcode is `offset + 2 + arg`) was incorrectly treated as an absolute offset 4 → pointed to offset 4 which is inside block `B@0000` (0-0x19) → self-loop → CycleException → treated as LoopHeader → `while` loop generated.

**Fix**: Pass `codeObj` to all `ResolveJumpTarget` calls in `LinkBlocks`:
```csharp
var jumpTarget = ResolveJumpTarget(instr, codeObj);
```

## Version-Specific Affected Code

- `src/PyRebuilderSharp.Core/Readers/PycReader.cs` — LOAD_GLOBAL arg decoding (3.12+)
- `src/PyRebuilderSharp.Core/Readers/PycReader.cs` — LOAD_ATTR arg decoding (3.12+)
- `src/PyRebuilderSharp.Core/Scanners/BlockScanner.cs` — `LinkBlocks` codeObj passing

## Regression

938/938 succeeded, 0 failed, 0 crashes ✅
