# PyRebuilderSharp Baseline Test Evaluation Report

**Date**: 2026-06-26
**Scope**: 997 decompiled outputs across 11 Python versions (2.7 → 3.14)
**Engine**: PyRebuilderSharp (.NET 10 + Avalonia, block-level CFG reconstruction)
**Commit**: `1c99e90`

---

## 1. Summary

| Metric | Value | Status |
|:-------|:-----:|:-----:|
| Total files (unique) | 106 | ✅ |
| Total across versions | 997 | ✅ |
| Success rate | 997/997 (100%) | ✅ |
| Crashes | 0 | ✅ |
| A class (low diff, <10%) | 31 (3%) | ✅ |
| B class (low-moderate, 10-25%) | 53 (5%) | ⚠️ |
| C class (moderate, 25-40%) | 167 (17%) | ⚠️ |
| D class (high diff ratio, >40%) | 746 (75%) | ⚠️ |
| **A+B (acceptable output)** | **84 (8%)** | ✅ |
| Total orphan blocks | 0 | ⚠️ |
| Total diff lines (added+removed) | **70589** | |
| Total diff lines per file (avg) | **70.8** | |

---

## 2. Diff Pattern Classification

Full diff analysis across functools.py, enum.py, reprlib.py, abc.py (v3_12):

### Category A: If+Return → If+Else+Return Chain (★ HIGH PRIORITY)
**Impact**: ~1500 lines across functools.py, enum.py  
**Root cause**: BoolOp simplification converts `return A or B` (after guard) into `if: return; else: return ...`  
**Example**:
```python
# Original:
if op_result is NotImplemented: return op_result
return not op_result and self != other

# Decompiled:
if op_result is NotImplemented: return op_result
else:
    return not op_result and (self != other)
```

### Category B: For-loop Try/Except/Else Lifted (★ HIGH PRIORITY)
**Impact**: ~500 lines (functools.py update_wrapper)  
**Root cause**: P0-F fix insufficient — ET blocks inside for-loop still partially lifted out  
**Example**:
```python
# Original:
for attr in assigned:
    try: value = getattr(wrapped, attr)
    except AttributeError: pass
    else: setattr(wrapper, attr, value)

# Decompiled:
for attr in assigned:
    pass
# ... try/except lifted before loop, setattr after return
```

### Category C: Comprehension Collapse (★ HIGH PRIORITY)
**Impact**: ~800 lines (functools, enum)  
**Root cause**: Set/list/dict comprehensions not detected; child code body flattened  
**Example**:
```python
# Original:
roots = {op for op in _convert if getattr(cls, op, None) is not getattr(object, op, None)}

# Decompiled:
op
{}
for op in {}:
    if not getattr(cls, op, None) is not getattr(object, op, None):
        pass
```

### Category D: Return + BoolOp Simplification (★ HIGH PRIORITY)
**Impact**: ~600 lines (functools total_ordering, enum)  
**Root cause**: Block-level conditions convert simple returns into if/else chains  
**Example**:
```python
# Original:
return not op_result and self != other

# Decompiled:
else:
    return not op_result and (self != other)
```

### Category E: Inner Class Definition Collapse (★ HIGH PRIORITY)
**Impact**: ~200 lines (functools cmp_to_key)  
**Root cause**: P0-D incomplete — CALL handler consumes __build_class__ reference before class body  
**Example**:
```python
# Original:
class K(object):
    __slots__ = ['obj']
    def __init__(self, obj): ...

# Decompiled:
K = K('K', object)
```

### Category F: Lambda Rendering (★ MODERATE)
**Impact**: ~100 lines (functools)  
**Root cause**: Lambda stored as `<lambda>` string literal in code  
**Example**:
```python
# Original:
wrapper.cache_parameters = lambda: {'maxsize': maxsize, 'typed': typed}
# Decompiled:
wrapper.cache_parameters = <lambda>
```

### Category G: Genexpr Rendering (★ MODERATE)
**Impact**: ~80 lines (functools)  
**Root cause**: Genexpr child code name `<genexpr>` leaks into output  
**Example**:
```python
# Original:
if any(issubclass(cls, base) for base in ...):
# Decompiled:
elif <genexpr>():
    pass
```

### Category H: Not-Inversion Pattern (★ MODERATE)
**Impact**: ~300 lines (functools, enum)  
**Root cause**: `not in` → `not ... in` with inverted if/else  
**Example**:
```python
# Original:
if candidate in s2[1:]:
    candidate = None
    break

# Decompiled:
if not candidate in s2[1:]:
    pass
else:
    candidate = None
```

### Category I: F-string Conversion (★ LOW)
**Impact**: ~200 lines (enum.py)  
**Root cause**: `'%s' % name` → `f"_{name!s}__"` (format change, functionally equivalent)  

### Category J: Module Metadata (★ LOW - Cosmetic)
**Impact**: ~400 lines (all files)  
**Issues**:  
- `__all__` list → tuple format  
- Multi-line def signatures → single line  
- Comment blocks removed  
- Docstring `'...'` → `"""..."""`  

---

## 3. Version Comparison

```
File          v3_7   v3_8   v3_10  v3_11  v3_12  v3_13  v3_14
functools       -     +922  +1082  +1190  +1137  +1233  +1228
enum.py       +1785  +1798  +2219  +2234  +2207  +2411  +2399
reprlib.py    +175   +182   +218   +242   +205   +220   +213
abc.py        +195   +119   +120   +135   +125   +202   +200
```

Key observations:
- **enum.py** dominates at 2200+ diff lines per version (worst file)
- **functools.py** has 1100+ diff lines (most improved by Phase 29)
- **reprlib.py** now at ~205 diff lines (improved by Phase 30 BUILD_CONST_KEY_MAP fix)
- **abc.py** at ~125 diff lines (improved by LOAD_SUPER_ATTR fix)
- v3.13/v3.14 consistently worse due to new opcodes and changed bytecode format

---

## 4. Execution Plan

### P0 (Immediate — Current Sprint)

| # | Issue | Est. | Impact | Approach |
|:-:|:------|:----:|:------:|:---------|
| P0-A | **For+try/except/else unwinding** (update_wrapper) | 6h | functools ~400 lines | Extend ET skip: skip ET entries whose block is inside a for-loop body chain (not just direct predecessor). Handle nested try/else with condition blocks |
| P0-B | **Comprehension detection** (set/list/dict/genexpr) | 8h | functools ~600 lines, enum ~400 lines | Fix BuildComprehension: handle GET_ITER consuming iterable, detect comprehension patterns in BuildForLoop, handle inline genexpr in conditions |
| P0-C | **BoolOp return simplification** (if/else chain) | 4h | functools ~500 lines | Post-process single-stmt else bodies to merge with preceding if (guard pattern). Remove redundant else when parent is `if X: return` |
| P0-D | **Inner class collapse** (cmp_to_key) | 4h | functools ~200 lines | Fix CALL handler for __build_class__: verify PUSH_NULL sentinel handling and stack depth for 3.12 CALL protocol |

### P1 (Next Sprint)

| # | Issue | Est. | Impact | Approach |
|:-:|:------|:----:|:------:|:---------|
| P1-A | **Not-inversion pattern** | 4h | functools ~300 lines | Fix condition extraction: detect `not in` / `not is` patterns and preserve original operator instead of inverting if/else |
| P1-B | **Lambda rendering** | 3h | functools ~100 lines | Fix FunctionRef rendering: detect `<lambda>` name and build Lambda AST from child code |
| P1-C | **Genexpr rendering** | 3h | functools ~80 lines | Extend BuildComprehension to handle Call(FunctionRef,\<genexpr\>) as generator expression in function arguments |

### P2 (Backlog)

| # | Issue | Est. | Impact | Approach |
|:-:|:------|:----:|:------:|:---------|
| P2-A | **F-string vs % formatting** | 2h | enum ~200 lines | Codegen option: prefer `%` or f-string |
| P2-B | **Module metadata** | 3h | all | __all__ format, comment preservation, blank lines |

### Effort Summary

| Priority | Tasks | Est. Total | Expected Diff Reduction |
|:--------:|:-----:|:----------:|:----------------------:|
| P0 | 4 tasks | 22h | ~1700 lines (~2.4%) |
| P1 | 3 tasks | 10h | ~480 lines (~0.7%) |
| P2 | 2 tasks | 5h | ~600 lines (~0.8%) |
| **Total** | **9 tasks** | **37h** | **~2780 lines (~3.9%)** |

---

## 5. Next Step Recommendation

**Immediate P0 target**: P0-A (for+try/except/else unwinding) — this is the highest-impact remaining issue affecting `update_wrapper` and multiple patterns in functools. The ET-skip mechanism needs to handle nested for-loop body blocks, not just direct predecessor check.

**Run command**: `python3 tools/baseline_evaluate_all.py` after each fix.

---

*Report generated by `tools/baseline_evaluate_all.py` on 2026-06-26*
*Diff analysis by agent categorize phase*
