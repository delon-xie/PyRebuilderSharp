# Phase 33 Execution Plan: Baseline Diff Reduction

**Date**: 2026-06-26  
**Baseline**: 997/997 ✅ 0 crashes, diff lines = 65,998  

---

## Current State

| Metric | Value |
|--------|-------|
| Total files × versions | 997 |
| A-class (≤3%) | 33 |
| B-class (≤15%) | 51 |
| A+B acceptable | 84 (8%) |
| D-class (>40%) | 741 (74%) |
| Orphans | 0 |
| Diff lines | 65,998 |

---

## Diff Category Breakdown (Manual Survey of 20 D-class files)

### P0 — Semantic Errors (produce functionally WRONG code)
| Category | Files Affected | Root Cause |
|----------|---------------|------------|
| **1. Try/except/finally blocks lost** | reprlib, pprint, functools, enum, contextlib | ExceptionTable successor collection incomplete; handler blocks not linked to normal-flow predecessors |
| **2. CALL_FUNCTION_EX with *args/**kwargs broken** | pprint, functools, dataclasses | `pp(object, *args, **kwargs)` → `[object](**kwargs)`. KW_NAMES + argpack interaction |
| **3. `__all__ = [...]` → tuple** | All files (cosmetic, but affects eval) | AST builder converts all list constants to tuples |
| **4. `__lt__` body lost** | pprint, enum | try/except in comparison methods not recovered |
| **5. Double return/fallthrough** | reprlib, abc, functools | CFG fallthrough to handler entry produces duplicate `return self.repr_instance` |

### P1 — Structural Recovery Bugs
| Category | Files Affected | Root Cause |
|----------|---------------|------------|
| **6. `{k: v for k,v in ...}`→set({k: v …})** | abc.py | 3.13+ ET + block boundary conflict for comprehension init |
| **7. Missing `repr_running = set()`** | reprlib | `BUILD_SET` before comprehension — detected as inline comprehension init |
| **8. `key = id(self), get_ident()` → `(id(self), get_ident())`** | reprlib | Tuple without parens normalized to tuple-with-parens |
| **9. `if method:\n  if typename not in …` merged** | reprlib, functools | OR-chained conditions collapsed |

### P2 — Formatting Fidelity
| Category | Files Affected | Root Cause |
|----------|---------------|------------|
| **10. Docstring `'text'` vs `"""text"""`** | All files | No docstring detection in code generator |
| **11. Missing blank lines between defs** | All files | No lnotab line-gap preservation |
| **12. Keyword arg order reversed** | All files | CALL arg pop order = LIFO → reversed |
| **13. Default params lost (`compact=False` → `compact`)** | pprint, abc, functools | `LOAD_CONST default` before `MAKE_FUNCTION` not tracked |
| **14. Single-line import → multi-line** | All files | Import grouping logic merges adjacent imports |

### P3 — Cleanup
| Category | Files Affected | Root Cause |
|----------|---------------|------------|
| **15. `# Decompiled from:` header** | All files | Replaces original copyright |
| **16. `.cell` for unresolved cellvars** | Pre-3.11 closure files | Cellvar name resolution fallback |
| **17. COPY_FREE_VARS placeholders** | Closure files | Placeholder names from COPY_FREE_VARS |

---

## Prioritized Execution Plan

### Phase 33a: LOAD_METHOD Fix (DONE ✅)
**Impact**: −442 diff lines, `repr1` method call fragmentation fixed  
**Files fixed**: reprlib.py, abc.py, functools.py, pprint.py method calls  
**Status**: ✅ Implemented, verified, baseline 997/997

### Phase 33b: ExceptionTable → try/finally Recovery (P0, est. 4h)
**Problem**: ExceptionTable handler blocks for try/finally are collected but NOT linked to the normal-flow predecessor. `recursive_repr`'s `try: … finally: …` block is lost entirely — cleanup code appears as unreachable statements after `return`.

**Approach**:
1. Read CPython 3.12+ `Python/compile.c` exception table generation for try/finally
2. In `BuildTryFromExceptionTable`: after collecting handler blocks, trace backward from each handler's **start offset** to find the normal-flow predecessor
3. Insert the predecessor's instructions as the try body, handler instructions as the finally block
4. Verify with `recursive_repr` (reprlib), `_safe_key.__lt__` (pprint), and `enum.py` metaclass

**Success criteria**: reprlib.py recursive_repr shows `try: … finally: …`, pprint.py __lt__ shows try/except body.

### Phase 33c: CALL_FUNCTION_EX with *args/**kwargs (P0, est. 3h)
**Problem**: `pp(object, *args, **kwargs)` → `[object](**kwargs)`. The `CALL_FUNCTION_EX` handler doesn't properly expand `*args` and `**kwargs` into the call signature.

**Approach**:
1. Examine `CALL_FUNCTION_EX` handler in `StackMachine.cs` (line 713+)
2. When `flags & 1` (kwargs dict) and `flags & 2` (args tuple), reconstruct the call as `func(*args, **kwargs)` 
3. Handle the case where args is a Name expression (not just a tuple constant)
4. Test with `pprint.py` `pp()` function

**Success criteria**: `def pp(object, *args, **kwargs)` decompiles correctly, `[object](**kwargs)` eliminated.

### Phase 33d: List Constant → Tuple Conversion (P1, est. 2h)
**Problem**: `__all__ = ["a", "b"]` → `__all__ = ('a', 'b')`. All list constants in constants table are stored as tuples by marshal. The AST builder needs to track which constants should be lists.

**Approach**:
1. In `CodeObject`, add `ListConstantIndices: HashSet<int>` tracking which constant indices hold list literals (from `BUILD_LIST` instructions)
2. During code generation, for constants referenced by `BUILD_LIST`, emit actual list literals
3. Test with `__all__` in abc.py, reprlib.py, pprint.py

**Success criteria**: `__all__ = ["Repr", "repr", …]` preserved as list.

### Phase 33e: Default Parameter Value Recovery (P2, est. 3h)
**Problem**: `def __init__(self, *, compact=False, …)` → `def __init__(self, *, compact, …)` — default values lost.

**Approach**:
1. In `StackMachine.MAKE_FUNCTION` handler, collect the `LOAD_CONST` values that precede `MAKE_FUNCTION` (they define default values)
2. Match defaults to parameters by position
3. Store in `CodeObject.DefaultValues` dict
4. Emit in code generator

**Success criteria**: `compact=False`, `fillvalue='...'` etc. preserved in decompiled signatures.

### Phase 33f: Formatting Fidelity (P3, est. 4h)
**Problem**: Docstrings, blank lines, keyword arg order — cosmetic but affects 100% of files.

**Approach**:
1. **Docstring**: In `AstBuilder/Generator`, detect `Constant(str)` as first statement in function → emit `"""…"""` instead of `'…'`
2. **Blank lines**: Track `LineNumberTable` gaps between consecutive function/class defs → emit `\n` 
3. **KW order**: Reverse keyword list in `Call` code generation (args are LIFO-popped)

**Success criteria**: ~70% of cosmetic diffs eliminated (est. −20,000 diff lines).

---

## Summary Timeline

| Phase | Priority | Description | Est. Effort | Target Diff Reduction |
|-------|----------|-------------|-------------|----------------------|
| 33a | P0 | LOAD_METHOD call fix | ✅ Done | −442 |
| 33b | P0 | ExceptionTable try/finally | 4h | −5,000 |
| 33c | P0 | CALL_FUNCTION_EX *args | 3h | −1,000 |
| 33d | P1 | List constant preservation | 2h | −200 |
| 33e | P2 | Default param values | 3h | −3,000 |
| 33f | P3 | Formatting fidelity | 4h | −20,000 |
| **Total** | | | **16h** | **−29,642** |

**Target after all phases**: ~36,356 diff lines (A+B ~30%)
