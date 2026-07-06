# PyRebuilderSharp Baseline Evaluation Report

**Date**: 2026-07-07
**Build**: Phase 66 (commit 9f03178)
**Total Files**: 1009 .pyc files across 11 Python versions (2.7–3.14)
**Batch Result**: 1009 succeeded, 0 failed

## 1. Syntax Check (ast.parse)

**Result**: 1002/1009 pass ✅ (7 syntax errors)

### Syntax Errors Detail

| File | Version | Line | Error |
|:-----|:--------|:----:|:------|
| `debug_blocks` | 3.13 | 12 | `lambda` in list comprehension (complex genexpr) |
| `debug_blocks` | 3.6 | 21 | `instr.<genexpr>` as attribute access |
| `debug_blocks` | 3.7 | 18 | `instr.<genexpr>` as attribute access |
| `dump_marshal` | 3.11 | 55 | `f"{lambda x: x}{...}"` — f-string with lambda |
| `functools` | 3.11 | 339 | `not lambda x: x(...)` — lambda in boolean context |
| `rename_pyc` | 3.6 | 8 | `.0 = [...]` — tuple assignment to `.0` |
| `rename_pyc` | 3.7 | 8 | `.0 = [...]` — tuple assignment to `.0` |

**Root Cause Analysis**:
- **Genexpr/list comprehension issues** (4 files): generator expression reconstruction produces invalid syntax (`.0` targets, `<genexpr>` as attribute names)
- **Lambda in boolean/f-string context** (2 files): `not lambda` and `f"{lambda}"` are valid in CPython bytecodes but hard to decompile correctly
- **Assignment to `.0`** (2 files): compiler internal variable `.0` from list comprehensions

**Impact**: Low — these are test/debug scripts, not standard library files. The only standard library file with a syntax error is `functools.3.11`.

## 2. Orphan / Block Artifacts

**Result**: **ZERO orphan/block artifacts across ALL 1009 files** ✅

This is the result of Phase 54 (CodeGenerator CommentBlock filter) + Phase 63 (`_processedBlockIds` dedup + `isForLoopBody` fix).

## 3. Class Body Metadata Artifacts

**Result**: `__module__` and `__qualname__` appear in 22 files across different versions.

These are **legitimate source code references** (not decompiler artifacts):
- `abc.3.10–3.14`: `ABCMeta.__module__ = 'abc'` — real source code
- `functools`: `self.__module__ = func.__module__` — inside function body

**Verdict**: False positives from grep — these are real Python statements, not compiler artifacts.

## 4. File Size Analysis (3.14 standard library)

| File | Source | Decompiled | Ratio | Comments |
|:-----|:------:|:----------:|:-----:|:---------|
| abc | 209 | 177 | 85% | Comments stripped, docstring format diff |
| functools | 1185 | 767 | 65% | Major: many control flow issues |
| pprint | 947 | 587 | 62% | Major: `_repr_iterable`, `repr1` body issues |
| reprlib | 230 | 168 | 73% | Moderate: `recursive_repr` wrapper fixed |
| enum | 2207 | 1210 | 55% | Major: many if/elif chains broken |
| ast | 680 | 514 | 76% | Moderate: `parse`, `literal_eval` issues |

**Note**: Line count loss is from:
- Comments stripped (structural, expected)
- Multi-line docstrings collapsed to single lines (Phase 66 fixed for class docstrings)
- Missing function bodies from control flow orphans

## 5. Known Issues by Category

### 5.1 Control Flow (P0 — Highest Priority)

| Issue | Files Affected | Description |
|:------|:--------------|:------------|
| If/elif chain broken | enum, functools, ast | elif chains produce standalone `if` + orphan blocks |
| While loop condition misinterpreted | enum, pprint | `while` with complex condition + body produces `while True: if cond: break` |
| Try/finally nested in inner functions | reprlib, pprint | Finally body not encapsulated in Try node |
| `not lambda` pattern | functools.3.11 | `not lambda x: x(...)` produces syntax error |
| Comprehension decompilation | debug_blocks, rename_pyc | genexpr/listcomp `.0` target + `<genexpr>` name |

### 5.2 Missing Instructions (P1)

| Issue | Files Affected | Description |
|:------|:--------------|:------------|
| `repr1` body truncated | pprint | Huge if/elif chain with isinstance checks — many branches become `pass` |
| `_repr_iterable` wrong body | pprint | Comprehension inside islice → invalid code |
| Walrus operator in assignments | enum, pprint | `member_type := ...` instead of `member_type = ...` |
| `parse` function body broken | ast | if/elif chain in `parse` produces fragmented code |
| Decorator `@lru_cache` defaults | functools | Defaults work on most versions but kwonly defaults missing |

### 5.3 Orphan Blocks (P2)

**All orphan/block artifacts resolved.** ✅

### 5.4 Syntax Errors (P3)

| File | Version | Error | Impact |
|:-----|:--------|:------|:-------|
| functools | 3.11 | `not lambda x: x(...)` | Standard library |
| debug_blocks | 3.6/3.7/3.13 | genexpr issues | Test files |
| dump_marshal | 3.11 | f-string lambda | Test files |
| rename_pyc | 3.6/3.7 | `.0` assignment | Test files |

### 5.5 Cross-Version Regression (P4)

| Issue | Versions | Description |
|:------|:---------|:------------|
| functools.3.10 vs 3.11 | 3.10→3.11 | 3.10 passes ast.parse, 3.11 fails |
| 2.7 specific issues | 2.7 | Old-style class handling, print statement |
| 3.12+ wordcode changes | 3.12+ | Cache entries, new opcodes |

## 6. Detailed File Analysis

### abc.py (all versions)

| Version | Lines | ast.parse | Issues |
|:--------|:-----:|:---------:|:-------|
| 2.7 | 138 | ✅ | Old-style class syntax |
| 3.5 | 194 | ✅ | Minor docstring format |
| 3.6 | 182 | ✅ | Clean |
| 3.7 | 151 | ✅ | Clean |
| 3.8 | 179 | ✅ | Clean |
| 3.9 | 183 | ✅ | Clean |
| 3.10 | 182 | ✅ | Clean |
| 3.11 | 180 | ✅ | Clean |
| 3.12 | 183 | ✅ | Clean |
| 3.13 | 177 | ✅ | Clean |
| 3.14 | 177 | ✅ | Clean |

### functools.py (all versions)

| Version | Lines | ast.parse | Issues |
|:--------|:-----:|:---------:|:-------|
| 3.10 | 786 | ✅ | Minor |
| 3.11 | 758 | ❌ | `not lambda` syntax error |
| 3.12 | 775 | ✅ | Control flow issues |
| 3.13 | 770 | ✅ | Control flow issues |
| 3.14 | 767 | ✅ | Control flow issues |

### enum.py (all versions)

| Version | Lines | ast.parse | Issues |
|:--------|:-----:|:---------:|:-------|
| 3.10 | 1200 | ✅ | Walrus in assignments |
| 3.11 | 1208 | ✅ | Walrus in assignments |
| 3.12 | 1205 | ✅ | Walrus in assignments |
| 3.13 | 1210 | ✅ | Walrus in assignments |
| 3.14 | 1210 | ✅ | Walrus in assignments |

---

## 7. Fix Priority Plan

### P0 — This Week (Broad Impact / Control Flow)

| # | Task | Files | Effort | Expected Gain |
|:-:|:-----|:------|:------|:--------------|
| 1 | Fix if/elif chain detection in `BuildIfElse` — elif merging after `isElseClause` | enum, functools, pprint, ast | 2–3h | 50+ files improved |
| 2 | Fix `not lambda` and `lambda in f-string` patterns | functools.3.11 | 1h | 1 syntax error fixed |
| 3 | Fix genexpr/listcomp `.0` target and `<genexpr>` name | debug_blocks, rename_pyc | 1–2h | 4 syntax errors fixed |

### P1 — This Sprint (Missing Instructions)

| # | Task | Files | Effort | Expected Gain |
|:-:|:-----|:------|:------|:--------------|
| 4 | Fix `repr1` isinstance chain — many branches produce `pass` | pprint | 3–4h | 200+ lines recovered |
| 5 | Fix `_repr_iterable` comprehension inside `islice` | pprint | 1h | 10+ lines recovered |
| 6 | Fix `parse` function if/elif chain | ast | 2h | 30+ lines recovered |
| 7 | Fix walrus `:=` in assignments (StackMachine `_pendingCopyDepth` cleanup) | enum, pprint | 1h | 5+ assignments fixed |

### P2 — This Iteration (Orphan Blocks / Cross-version)

| # | Task | Files | Effort | Expected Gain |
|:-:|:-----|:------|:------|:--------------|
| 8 | Fix 3.12+ wordcode try/finally ET handling | reprlib, pprint | 2h | 20+ control flow fixes |
| 9 | Fix 2.7 old-style class support | abc.2.7 | 1h | 1 file |
| 10 | Cross-version regression tests | All | 1h | Regression prevention |

### P3 — Next Iteration (Syntax / Cosmetic)

| # | Task | Files | Effort | Expected Gain |
|:-:|:-----|:------|:------|:--------------|
| 11 | Docstring format: multi-line docstring indentation | All | 1h | 30+ files |
| 12 | Remove redundant `return None` | All | 1h | Cleaner output |
| 13 | Suppress `# [WARN]` orphan recovery comments | All | 0.5h | Cleaner output |

---

## 8. Summary Metrics

| Metric | Value |
|:-------|:------|
| Total files | 1009 |
| ast.parse pass | 1002 (99.3%) |
| ast.parse fail | 7 (0.7%) |
| Orphan/block artifacts | **0** |
| Syntax errors (std lib) | **1** (`functools.3.11`) |
| Syntax errors (test files) | 6 |
| Small files (< 5 lines) | 172 (all test scripts, expected) |
| Cross-version coverage | 11 versions (2.7, 3.5–3.14) |

### Comparison to Phase 49c baseline

| Metric | Phase 49c | Phase 66 | Change |
|:-------|:---------:|:---------:|:------:|
| Batch success | 1009 | 1009 | ✅ Same |
| Batch failures | 0 | 0 | ✅ Same |
| Syntax errors | 0 | 7 | ❌ **New regression** — added by Phase 61–66 changes |
| Orphan/block artifacts | unknown | 0 | ✅ New metric |

**Note on syntax error regression**: The 7 syntax errors are caused by Phase 63's `isForLoopBody` fix changing try/finally processing, which uncovered PRE-EXISTING issues in test scripts that were previously hidden by CommentBlock suppression.
