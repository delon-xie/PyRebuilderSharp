# PyRebuilderSharp Baseline Test Evaluation Report
**Date**: 2026-06-16 (v5 — for-loop iterable + POP_TOP false Break fixes)
**Scope**: 938 decompiled files x 11 Python versions (2.7 → 3.14)
**Engine**: PyRebuilderSharp (.NET 10 + Avalonia, block-level fault tolerance)

---

## 1. Overall Summary

| Metric | Value | Status |
|:-------|:------|:------:|
| Total files | 938 | |
| **Fatal crashes** (tool exit) | **0 (0.0%)** | ✅ |
| **CrashCollector events** (block-level) | **0** | ✅ Cleared |
| Unique crash types | — | No active crashes |

**Fatal crash rate**: 0.0% (all exceptions caught by fault-tolerant framework)
**Block-level fault tolerance**: 100% (every crash generates `CommentBlock` + fallback)

### vs v4 (2026-06-16 baseline)

| Metric | v4 | v5 | Δ |
|:-------|:---|:---|:--|
| Fatal crashes | 0 | **0** | ✅ |
| CrashCollector files | 1,604 | **0** | ✅ **CLEARED** |
| abc.3.10 orphans | 0 | **0** | ✅ Stable |
| Unique crash types | 2 | **0** | ✅ **FIXED** |

---

## 2. abc.py Orphan Recovery (Key Quality Indicator)

| Version | v4 Orphans | v5 Orphans | Status |
|:-------:|:----------:|:----------:|:------:|
| 2.7 | — | — | ⬜ No .pyc |
| 3.5 | — | — | ⬜ No .pyc |
| 3.6 | — | — | ⬜ No .pyc |
| 3.7 | — | — | ⬜ No .pyc |
| 3.8 | 2 | **1** | ✅ **-50%** |
| 3.9 | 2 | **1** | ✅ **-50%** |
| **3.10** | **0** | **0** | ✅ **FIXED** 🎉 |
| 3.11 | 1 | **1** | — |
| 3.12 | 3 | **2** | ✅ **-33%** |
| 3.13 | 0 | **0** | ✅ |
| 3.14 | — | **2** | ⬜ New measurement |

### Notable Improvements (v4 → v5)

**abc.3.8.pyc**: 2 orphans → **1 orphan**
- for-loop body `break` → `abstracts.add(name)` no longer orphaned

**abc.3.9.pyc**: 2 orphans → **1 orphan**
- Same fix as 3.8

**abc.3.10.pyc**: 0 orphans → **0 orphans** (stable)
- `for scls in cls.__bases__:` and `abstracts.add(name)` both correct ✅
- All three for-loops fully decompiled

**abc.3.12.pyc**: 3 orphans → **2 orphans**
- for-loop body no longer orphaned

---

## 3. Crash Analysis (CrashCollector)

| Crash Type | Count | Status |
|:-----------|:------|:-------|
| `NullReferenceException` | 0 | ✅ Fixed (68fc56d) |
| `InvalidCastException` | 0 | ✅ Fixed |

All historical crashes (1,604 from pre-fix runs) have been cleaned.
**0 active crash files** in `~/.pyrebuilder/crashes/`.

---

## 4. Regression Status

| Test | Result |
|:-----|:------:|
| `--stats` batch (938 files) | ✅ 938 succeeded, 0 failed |
| `dotnet build` | ✅ 0 errors |
| Crash files | ✅ 0 files |

---

## 5. Key Fixes in this Cycle

| Commit | Fix | Impact |
|:-------|:----|:-------|
| `68fc56d` | 3.6-3.9 wordcode jump target *2 + AddSuccessor null guard | Fixed 4 fatal crashes |
| `f47ece0` | try/except handler→post-handler successor chain + _processedBlockIds | abc orphans: 3.10 4→0 |
| `81193c0` | Orphan block position-aware insertion (early-offset heuristic) | `abstracts = set()` at correct position |
| `dd667a6` | Version case switch/case pattern + CPython source annotations | Code quality |
| **`ee2f464`** | **for-loop iterable via fallthrough predecessor chain (DFS)** | `iterable` → **`cls.__bases__`** ✅ |
| **`df2e297`** | **POP_TOP false Break — only Break when stack empty** | `break` → **`abstracts.add(name)`** ✅ |

---

## 6. Remaining Issues

### B-class (Semantic errors) — Cleared ✅

All B-class semantic errors from v4 are now **resolved**:
1. ~~`for scls in iterable:` → `cls.__bases__:`~~ ✅ `ee2f464`
2. ~~Inner for-loop `break` → `abstracts.add(name)`~~ ✅ `df2e297`
3. ~~Second for-loop `break` → `abstracts.add(name)`~~ ✅ `df2e297`

### C-class (Known limitations)

| Issue | Count | Status |
|:------|:-----:|:-------|
| Pre-3.8 files not compiled | 4 versions | ⬜ Need pyenv setup |
| CFG handler→class edge | ~50 files | 🔴 Requires BlockScanner rework |
| BuildTryFromExceptionTable O(n²) | 3.11+ | 🔴 Performance optimization |
| Remaining orphans (3.8/3.9/3.11/3.12/3.14) | 1-2 per version | 🟡 Needs successor chain analysis |
| 2.7/3.5/3.6/3.7 abc.pyc unavailable | 4 versions | ⬜ Compile with pyenv |

---

## 7. File Distribution by Python Version

_(Exact count per version would require re-count; the test suite contains 938 .pyc files across 11 Python versions)_

---

## 8. Next Steps

| Priority | Task | Effort |
|:--------:|:-----|:------:|
| P1 | Compile missing .pyc for 2.7, 3.5, 3.6, 3.7 | ~30m |
| P1 | Optimize BuildTryFromExceptionTable O(n²) | ~2h |
| P2 | Fix remaining orphans via successor chain analysis | ~3h |
| P2 | Fix CFG handler→class edge misclassification | ~4h |
