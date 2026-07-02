# Phase 34 Execution Plan: Baseline Diff Reduction

**Date**: 2026-06-26
**Baseline**: 997/997 ✅ 0 crashes, diff lines = **65,306**

## Current State vs Previous

| Metric | Phase 32 | Phase 33 | Δ |
|--------|:--------:|:--------:|:-:|
| Diff lines | 70,408 | 65,306 | **−5,102** |
| A-class | 9 (1%) | 33 (3%) | +24 |
| B-class | 22 (2%) | 40 (4%) | +18 |
| A+B acceptable | 31 (3%) | 73 (7%) | +42 |
| C-class | 82 (9%) | 180 (18%) | +98 |
| D-class | 893 (90%) | 744 (75%) | −149 |
| Orphans | 0 | 0 | 0 |

### Fixes in Phase 33 (this session)
| Fix | Impact |
|-----|:------:|
| LOAD_METHOD call fragmentation | −442 |
| CALL_FUNCTION_EX + LIST_EXTEND + INTRINSIC handlers | −434 |
| Keyword arg order (insert at 0) | −30 |
| `__all__` list preservation | cosmetic |
| Kwdefaults via SET_FUNCTION_ATTRIBUTE | functional |
| EmitBlankLineIfNeeded improvements | −228 |
| **Total** | **−1,134** |

---

## Diff Category Breakdown

Based on analysis of 20 D-class files across 5 versions:

| Rank | Category | Prevalence | Est. Δ | Nature | 
|:----:|:---------|:----------:|:------:|:------|
| 1 | **BLANK_LINES** | 87% | −8,000 | Cosmetic — partially fixed |
| 2 | **SIG_WRAPPING** (multi-line→single line) | 65% | −5,000 | Cosmetic |
| 3 | **IMPORT_FORMAT** | 81% | −3,000 | Cosmetic |
| 4 | **KWARG_SPACES** (`=` vs ` = `) | 60% | −1,500 | Cosmetic |
| 5 | **DICT_FORMAT** (multi-line→inline) | 55% | −2,000 | Cosmetic |
| 6 | **HEADER** | 100% | −1,000 | Cosmetic |
| 7 | **DOCSTRING_QUOTES** | 10% | −500 | Cosmetic |
| 8 | **TRY_BLOCK** (try/finally missing) | 70% | −5,000 | **Semantic** |
| 9 | **CALL_SYNTAX** (*args/**kwargs) | 35% | −1,000 | **Semantic** |
| 10 | **BOOL_EXPR** (logic simplified) | 30% | −500 | **Semantic** |
| 11 | **ASSIGN_FORMAT** (tuple parens) | 20% | −200 | Cosmetic |
| 12 | **CONTROL_FLOW** (if/else restructured) | 15% | −300 | **Semantic** |

---

## Prioritized Execution Plan

### P0 — Semantic Errors (functional correctness)

**Phase 34a: ExceptionTable → try/finally recovery** (−5,000 est., 4h)
- `recursive_repr` loses `try: result = user_function(self) finally: repr_running.discard(key)`
- Root cause: ET handler blocks without CHECK_EXC_MATCH are skipped entirely
- Fix requires restructuring block boundaries at ET entry boundaries
- Target files: reprlib.py, functools.py, enum.py, contextlib.py

**Phase 34b: CALL_FUNCTION_EX *args/**kwargs syntax** (−1,000 est., 3h)  
- `[object](**kwargs)` pattern — already partially fixed (call target correct now)
- Remaining: `*args` not rendered as `*args` (appears as positional arg)
- Need: `Starred` expression in AST model + `*` prefix in code generator

### P1 — High-Impact Formatting (cosmetic but most diff lines)

**Phase 34c: Multi-line function signatures** (−5,000 est., 2h)
- `def __init__(self, *, maxlevel=6, ...)` → one line instead of 5 lines
- Fix: Add parameter for max line length, wrap at commas
- Target: All files with long signatures

**Phase 34d: Dict literal formatting** (−2,000 est., 2h)
- `_lookup = {'a': 'b', ...}` inline vs multi-line
- Fix: Detect dicts with > threshold entries, format as multi-line
- Target: reprlib.py, functools.py, abc.py, enum.py

### P2 — Lower-Impact Cleanup

**Phase 34e: Import format normalization** (−3,000 est., 2h)
- Multi-line imports collapsed to one line
- `import math, sys` vs `import math\nimport sys`
- Fix: Match original import grouping style

**Phase 34f: Keyword arg spacing** (−1,500 est., 1h)
- `stream=None` vs `stream = None`
- Fix: Remove spaces around `=` in keyword args

**Phase 34g: Assignment formatting** (−200 est., 1h)
- `key = id(self), get_ident()` → `key = (id(self), get_ident())`
- Tuple unpacking without parens being parenthesized
- Fix: Detect multiple-assignment comma patterns

### P3 — Final Polish

**Phase 34h: Header format** (−1,000 est., 1h)
- `# Decompiled from: <module>` instead of copyright
- Fix: Emit `# Decompiled from: filename` matching original format

---

## Summary

| Phase | Priority | Description | Effort | Est. Δ | Status |
|-------|:--------:|:------------|:------:|:------:|:------:|
| 34a | P0 | try/finally via ET | 4h | −5,000 | 🔲 |
| 34b | P0 | *args/**kwargs syntax | 3h | −1,000 | 🔲 |
| 34c | P1 | Multi-line signatures | 2h | −5,000 | 🔲 |
| 34d | P1 | Dict literal wrapping | 2h | −2,000 | 🔲 |
| 34e | P2 | Import format | 2h | −3,000 | 🔲 |
| 34f | P2 | KW arg spacing | 1h | −1,500 | 🔲 |
| 34g | P3 | Assignment formatting | 1h | −200 | 🔲 |
| 34h | P3 | Header format | 1h | −1,000 | 🔲 |
| **Total** | | | **16h** | **−18,700** | |

**Target after all phases**: ~46,606 diff lines (A+B ~25%)
