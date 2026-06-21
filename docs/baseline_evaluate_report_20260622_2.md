# PyRebuilderSharp Final Baseline Assessment

**Date**: 2026-06-22 07:03
**Scope**: 942 outputs across 11 Python versions (2.7 -> 3.14)
**Commit**: `a72b000`

---

## 1. Executive Summary

| Metric | Value | Status |
|:-------|:------|:------:|
| Total files | 942 | |
| Decompilation success | **942 (100%)** | :white_check_mark: |
| Failures | **0** | |
| A (near-perfect, <=3%) | 29 (3%) | :white_check_mark: |
| B (minor cosmetic, <=15%) | 42 (4%) | :white_check_mark: |
| C (notable, <=40%) | 161 (17%) | :warning: |
| D (high diff, >40%) | 710 (75%) | :warning: |
| **A+B acceptable** | **71 (8%)** | :white_check_mark: |
| Orphan blocks | 3967 | :warning: |
| Diff lines | 72698 | |
| Diff lines/file avg | 77.2 | |
| `# [WARN]` | 0 | :white_check_mark: |
| `# Unknown node` | 0 | :white_check_mark: |

---

## 2. Per-Version Quality

| Version | Files | A | B | C | D | A+B% | Orphans |
|:-------:|:-----:|:-:|:-:|:-:|:-:|:----:|:------:|
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

## 3. Key File Deep Dive

| File | Ver | Ratio | Cat | Orphans | Diff |
|:----|:---:|:-----:|:---:|:------:|:----:|
| abc.py | 2.7 | 95.7% | D | 0 | 200 |
| abc.py | 3.10 | 68.4% | D | 0 | 143 |
| abc.py | 3.11 | 82.8% | D | 9 | 173 |
| abc.py | 3.12 | 74.2% | D | 1 | 155 |
| abc.py | 3.13 | 140.7% | D | 1 | 294 |
| abc.py | 3.14 | 141.1% | D | 1 | 295 |
| abc.py | 3.5 | 124.4% | D | 3 | 260 |
| abc.py | 3.6 | 133.5% | D | 11 | 279 |
| abc.py | 3.7 | 106.2% | D | 0 | 222 |
| abc.py | 3.8 | 72.2% | D | 12 | 151 |
| abc.py | 3.9 | 72.2% | D | 12 | 151 |
| enum.py | 3.10 | 94.2% | D | 79 | 2081 |
| enum.py | 3.11 | 127.1% | D | 66 | 2807 |
| enum.py | 3.12 | 123.9% | D | 59 | 2736 |
| enum.py | 3.13 | 148.8% | D | 56 | 3285 |
| enum.py | 3.14 | 151.0% | D | 51 | 3334 |
| enum.py | 3.6 | 113.5% | D | 263 | 2506 |
| enum.py | 3.7 | 113.9% | D | 652 | 2516 |
| enum.py | 3.8 | 114.6% | D | 653 | 2531 |
| enum.py | 3.9 | 115.1% | D | 652 | 2542 |
| functools.py | 3.10 | 87.4% | D | 4 | 1036 |
| functools.py | 3.11 | 121.8% | D | 44 | 1444 |
| functools.py | 3.12 | 118.7% | D | 18 | 1408 |
| functools.py | 3.13 | 138.8% | D | 19 | 1646 |
| functools.py | 3.14 | 136.3% | D | 15 | 1616 |
| functools.py | 3.8 | 90.7% | D | 160 | 1076 |
| functools.py | 3.9 | 91.9% | D | 149 | 1090 |
| pprint.py | 3.14 | 103.7% | D | 6 | 983 |
| reprlib.py | 3.10 | 87.0% | D | 3 | 201 |
| reprlib.py | 3.11 | 138.5% | D | 17 | 320 |
| reprlib.py | 3.12 | 117.7% | D | 3 | 272 |
| reprlib.py | 3.13 | 121.6% | D | 3 | 281 |
| reprlib.py | 3.14 | 128.6% | D | 3 | 297 |
| reprlib.py | 3.6 | 94.8% | D | 13 | 219 |
| reprlib.py | 3.7 | 101.3% | D | 41 | 234 |
| reprlib.py | 3.8 | 101.3% | D | 40 | 234 |
| reprlib.py | 3.9 | 103.0% | D | 43 | 238 |

---

## 4. Quality Trends (Phase 8 -> 11)

| Metric | Phase 8 Before | Current | Change |
|:-------|:--------------:|:-------:|:------:|
| A+B | 50 (5%) | **71 (7.5%)** | +21 |
| Orphans | 4989 | **3967** | -1022 (20%) |
| Diff lines | 77071 | **72698** | -4373 (6%) |
| [WARN] | 312 | **0** | Eliminated |
| Unknown node | 36 | **0** | Eliminated |
| For-loop errors | 78 | **0** | Fixed |

### Phase-by-Phase Improvements

| Phase | Task | Orphans | Diff |
|:----:|:-----|:-------:|:----:|
| **8a** | For-loop iterable fix | -78 sem | -200 |
| **8b** | Orphan raise suppression | -441 | -100 |
| **8e** | Debug noise cleanup | 0 | -1444 |
| **9a** | abc.py 3.13/14 collapse | -185 | -701 |
| **9b** | Handler block tracking | -129 | -124 |
| **9d** | Unknown node elimination | 0 | -4 |
| **10 P1** | Handler preamble filter | -659 | -553 |
| **10 P2** | [WARN] elimination | 0 | -1350 |
| **10 P3** | Default parameter values | 0 | -31 |
| **10 P4** | Docstring format | 0 | 0 |
| **11 P0** | STORE_FAST_STORE_FAST encoding | 0 | 0 |
| **11 P2** | LOAD combined arg order | 0 | -58 |

---

## 5. Remaining Issues

### 5.1 Orphan Blocks (3967)
- **enum.py**: ~2800 across versions -- complex nested try/except in class generation
- **functools.py**: ~503 -- 3.11+ for-loop body boundary detection
- **Root cause**: Handler blocks in deeply nested structures not fully resolved

### 5.2 Cosmetic / Formatting
- **Iterable duplication**: `cls.__bases__` / `cls.__dict__.items()` printed as flat statement AND for-loop iterable (P4)
- **Blank line preservation**: No lnotab tracking between blocks
- **Import grouping**: Multi-line imports merged into single lines
- **Function docstring**: Single-line `'text'` still used in some function bodies

### 5.3 abc.py 3.13/14 Residual
- `for (value, name)` vs original `for name, value` -- variable order swapped (cosmetic)
- `cls.__bases__` iterable duplicate before for-loop

---

## 6. Phase 12 Recommendations

| Priority | Issue | Impact | Effort |
|:--------:|:------|:------:|:------:|
| **P0** | Deep orphan reduction (enum.py ~2800) | Largest remaining orphan source | 6h |
| **P1** | Iterable duplication (cls.__bases__) | 3+ files affected, cosmetic | 3h |
| **P2** | Blank line preservation (lnotab) | All files, readability | 3h |
| **P3** | Import grouping preservation | All files, formatting | 2h |
| **P4** | Deep orphan: functools.py ~500 | Second largest orphan source | 3h |

### Proposed Order

1. **P1**: Fix iterable duplication -- mark predecessor blocks consumed in ExtractIterExpression
2. **P0+P4**: Orphan reduction -- refactor handler chain detection in BuildTryFromBlock
3. **P2**: Blank line preservation -- implement lnotab/linetable gap tracking
4. **P3**: Import grouping -- preserve multi-line import structure

---

*Generated by baseline_evaluate_all.py + deep analysis on 2026-06-22 07:03*
