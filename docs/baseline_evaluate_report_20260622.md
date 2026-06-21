# PyRebuilderSharp Baseline Test Evaluation Report

**Date**: 2026-06-22 06:40
**Scope**: 942 decompiled outputs across 11 Python versions (2.7 -> 3.14)
**Engine**: PyRebuilderSharp (.NET 10 + Avalonia, block-level CFG reconstruction)
**Commit**: `c67fcb6`

---

## 1. Executive Summary

| Metric | Value | Status |
|:-------|:------|:------:|
| Unique source files | 95 | |
| Total decompilation attempts | 942 | |
| **Decompilation success (no crashes)** | **942 (100.0%)** | :white_check_mark: |
| **Decompilation failures** | **0** | :x: |
| **A class (near-perfect, <=3% diff)** | **29 (3%)** | :white_check_mark: |
| **B class (minor cosmetic, <=15%)** | **42 (4%)** | :white_check_mark: |
| C class (notable formatting diff, <=40%) | 161 (17%) | :warning: |
| D class (high diff ratio, >40%) | 710 (75%) | :warning: |
| **A+B (acceptable output)** | **71 (8%)** | :white_check_mark: |
| Total orphan blocks | 3967 | :warning: |
| Total diff lines (added+removed) | 72756 | |
| Total diff lines per file (avg) | 77.2 | |

**Key metric**: 0% crash rate across all decompilation attempts.

### Quality Trends

| Metric | Before Phase 8 | After Phase 10 | Change |
|:-------|:--------------:|:--------------:|:------:|
| A+B acceptable | 50 (5%) | 71 (8%) | +21 files |
| Total orphans | 4989 | 3967 | -1022 |
| Diff lines | 77071 | 72756 | -4315 |
| # [WARN] | 312 | 0 | Eliminated |
| # Unknown node | 36 | 0 | Eliminated |

---

## 2. Per-Version Quality Breakdown

| Version | Files | A (<=3%) | B (<=15%) | C (<=40%) | D (>40%) | A+B% | Orphans |
|:-------:|:-----:|:-------:|:--------:|:--------:|:--------:|:----:|:------:|
| 2.7 | 51 | 3 | 4 | 15 | 29 | 14% | 30 |
| 3.10 | 93 | 3 | 5 | 16 | 69 | 9% | 183 |
| 3.11 | 93 | 1 | 2 | 10 | 80 | 3% | 167 |
| 3.12 | 93 | 1 | 3 | 13 | 76 | 4% | 111 |
| 3.13 | 93 | 3 | 3 | 10 | 77 | 6% | 110 |
| 3.14 | 94 | 3 | 4 | 11 | 76 | 7% | 90 |
| 3.5 | 57 | 3 | 5 | 17 | 32 | 14% | 18 |
| 3.6 | 91 | 3 | 4 | 14 | 70 | 8% | 347 |
| 3.7 | 91 | 3 | 4 | 17 | 67 | 8% | 817 |
| 3.8 | 93 | 3 | 4 | 19 | 67 | 8% | 993 |
| 3.9 | 93 | 3 | 4 | 19 | 67 | 8% | 1101 |

---

## 3. Key File Diff Deep Dive

| File | Ver | Ratio | Cat | Orphans | Diff Lines |
|:----|:---:|:-----:|:---:|:------:|:----------:|
| abc.py | 2.7 | 95.7% | D | 0 | 200 |
| abc.py | 3.10 | 68.4% | D | 0 | 143 |
| abc.py | 3.11 | 82.8% | D | 9 | 173 |
| abc.py | 3.12 | 74.2% | D | 1 | 155 |
| abc.py | 3.13 | 140.7% | D | 1 | 294 |
| abc.py | 3.14 | 142.1% | D | 1 | 297 |
| abc.py | 3.5 | 124.4% | D | 3 | 260 |
| abc.py | 3.6 | 133.5% | D | 11 | 279 |
| abc.py | 3.7 | 106.2% | D | 0 | 222 |
| abc.py | 3.8 | 72.2% | D | 12 | 151 |
| abc.py | 3.9 | 72.2% | D | 12 | 151 |
| enum.py | 3.10 | 94.2% | D | 79 | 2081 |
| enum.py | 3.11 | 127.1% | D | 66 | 2807 |
| enum.py | 3.12 | 123.9% | D | 59 | 2736 |
| enum.py | 3.13 | 148.8% | D | 56 | 3285 |
| enum.py | 3.14 | 150.5% | D | 51 | 3322 |
| enum.py | 3.6 | 113.5% | D | 263 | 2506 |
| enum.py | 3.7 | 113.9% | D | 652 | 2516 |
| enum.py | 3.8 | 114.6% | D | 653 | 2531 |
| enum.py | 3.9 | 115.1% | D | 652 | 2542 |
| functools.py | 3.10 | 87.4% | D | 4 | 1036 |
| functools.py | 3.11 | 121.8% | D | 44 | 1444 |
| functools.py | 3.12 | 118.7% | D | 18 | 1408 |
| functools.py | 3.13 | 138.8% | D | 19 | 1646 |
| functools.py | 3.14 | 139.6% | D | 15 | 1656 |
| functools.py | 3.8 | 90.7% | D | 160 | 1076 |
| functools.py | 3.9 | 91.9% | D | 149 | 1090 |
| pprint.py | 3.14 | 105.0% | D | 6 | 995 |
| reprlib.py | 3.10 | 87.0% | D | 3 | 201 |
| reprlib.py | 3.11 | 138.5% | D | 17 | 320 |
| reprlib.py | 3.12 | 117.7% | D | 3 | 272 |
| reprlib.py | 3.13 | 121.6% | D | 3 | 281 |
| reprlib.py | 3.14 | 123.4% | D | 3 | 285 |
| reprlib.py | 3.6 | 94.8% | D | 13 | 219 |
| reprlib.py | 3.7 | 101.3% | D | 41 | 234 |
| reprlib.py | 3.8 | 101.3% | D | 40 | 234 |
| reprlib.py | 3.9 | 103.0% | D | 43 | 238 |

---

## 4. Remaining Issues & Root Causes

### 4.1 Orphan Blocks (3967)

- **enum.py**: ~2800 orphans across all versions -- complex try/except/with/for nesting in class generation
- **functools.py**: ~500 orphans -- 3.11+ for-loop body boundary detection
- **Root cause**: Handler blocks whose successors aren't fully resolved in the CFG; Phase 10 P1 suppressed handler-preamble blocks but some orphan-producing blocks remain

### 4.2 Formatting Fidelity

- **Docstring format**: single-line function docstrings now `"""..."""` (Phase 10 P4)
- **Blank line preservation**: No tracking of line gaps between blocks
- **Import grouping**: Single-line imports merged into multi-line
- **Default parameter values**: `file = None` working for `_dump_registry` but not all cases

### 4.3 abc.py 3.13/14 Issues

- **`for _ in cls.__dict__.items()`**: Tuple unpacking `name, value` not reconstructed
- **`cls.__bases__`** flat statement before `for scls in cls.__bases__` -- iterable duplication
- **`value = getattr(name, cls, None)`** argument order swapped (should be `cls, name`)

---

## 5. Phase 11 Recommendations

| Priority | Issue | Impact | Effort | Approach |
|:--------:|:------|:------:|:------:|:---------|
| **P0** | abc.py 3.13/14 `for _ in cls.__dict__.items()` unpack | Nested for-loop without tuple unpack, 3.13-14 only | 4h | Trace 3.13 body block layout to find UNPACK_SEQUENCE in for-loop bodies |
| **P1** | Deep orphan reduction (enum.py ~2000) | Remaining 3967 orphans, 70% from enum/functools | 6h | Rework `BuildTryFromBlock` handler chain tracking for nested try/except inside loops |
| **P2** | abc.py `value = getattr(name, cls, None)` arg swap | Function argument order error, 3.10+ | 2h | Fix StackMachine CALL arg order when arguments come from tuple unpack |
| **P3** | Default param values for class-body functions | Class method defaults like `fget=None` not restored | 3h | Investigate class-body function default handling (SET_FUNCTION_ATTRIBUTE path) |
| **P4** | abc.py `cls.__bases__` iterable duplication | Flat statement before for-loop, all versions | 2h | Fix ExtractIterExpression to not leave iterable expression as flat statement |
| **P5** | Blank line preservation | Cosmetic, all files | 3h | Track lnotab/linetable line gaps between blocks |

---

## 6. Phase 11 Proposed Execution Plan

**Ordering**: P0 -> P1 -> P2 -> P3 -> P4 -> P5

### Phase 11a: abc.py 3.13 for-loop unpack (4h)
- Investigate why `UNPACK_SEQUENCE` is not found in for-loop body blocks for 3.13+
- Fix `ExtractLoopVariable` or body block collection to locate UNPACK_SEQUENCE
- Target: `for name, value in cls.__dict__.items()` correct

### Phase 11b: Deep orphan reduction (6h)
- Focus: enum.py (~2000 orphans), functools.py (~500)
- Rework handler chain tracking in `BuildTryFromBlock` for nested try/except
- May require revisiting `FindBlocksFromOffset` to handle nested handler chains

### Phase 11c: abc.py arg order + iterable duplication (4h)
- Fix `value = getattr(name, cls, None)` to `value = getattr(cls, name, None)`
- Fix `cls.__bases__` flat statement before for-loop

---

*Report generated by `tools/baseline_evaluate_all.py` + deep analysis on 2026-06-22 06:40*
