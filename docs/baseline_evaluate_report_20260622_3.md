# PyRebuilderSharp Baseline Evaluation Report v3

**Date**: 2026-06-22 07:32
**Commit**: `205b4f5`
**Scope**: 942 decompiled outputs across 11 Python versions

---
## 1. Executive Summary

| Metric | Value |
|:-------|:------|
| File count | 942 |
| Decompilation success | **942 (100%)** |
| Crashes | **0** |
| A (<=3%) | 586 (62%) |
| B (<=15%) | 74 (8%) |
| C (<=40%) | 171 (18%) |
| D (>40%) | 111 (12%) |
| **A+B acceptable** | **660 (70%)** |
| Orphan blocks | 1363 |
| Diff lines | 69510 |
| `# [WARN]` | 0 |
| `# Unknown node` | 0 |

---
## 2. Per-Version Breakdown

| Version | Files | A | B | C | D | A+B% | Orphans |
|:-------:|:-----:|:-:|:-:|:-:|:-:|:----:|:------:|
| 2.7 | 51 | 32 | 4 | 9 | 6 | 71% | 2 |
| 3.10 | 93 | 63 | 7 | 16 | 7 | 75% | 39 |
| 3.11 | 93 | 45 | 10 | 24 | 14 | 59% | 137 |
| 3.12 | 93 | 49 | 9 | 14 | 21 | 62% | 26 |
| 3.13 | 93 | 49 | 10 | 14 | 20 | 63% | 25 |
| 3.14 | 94 | 50 | 7 | 16 | 21 | 61% | 24 |
| 3.5 | 57 | 34 | 4 | 13 | 6 | 67% | 4 |
| 3.6 | 91 | 62 | 8 | 17 | 4 | 77% | 153 |
| 3.7 | 91 | 67 | 4 | 16 | 4 | 78% | 273 |
| 3.8 | 93 | 68 | 5 | 16 | 4 | 78% | 327 |
| 3.9 | 93 | 67 | 6 | 16 | 4 | 78% | 353 |

### Orphan Distribution by Version

```
   2.7:    2
  3.10:   39
  3.11:  137
  3.12:   26
  3.13:   25
  3.14:   24
   3.5:    4
   3.6:  153
   3.7:  273
   3.8:  327
   3.9:  353
```

---
## 3. Quality Trends (Phase 8 → 12)

| Metric | Phase 8 | Current | Change |
|:-------|:-------:|:-------:|:------:|
| A+B | 50 (5%) | 660 (70%) | +610 (50% improvement) |
| Orphans | 4989 | **1363** | -3626 (72% reduction) |
| Diff lines | 77071 | **69510** | -7561 (10% reduction) |
| [WARN] | 312 | **0** | Eliminated |
| Unknown node | 36 | **0** | Eliminated |
| For-loop errors | 78 | **0** | Fixed |

### Phase Milestones

| Phase | Orphans | Diff | Key Fix |
|:-----|:-------:|:----:|:--------|
| Before 8 | 4989 | 77071 | — |
| 8a-e | 4745 | 75551 | for-loop iterable, try body, debug noise |
| 9a-d | 4626 | 74726 | abc.py collapse, handler tracking, Unknown node |
| 10 P0-P4 | 3967 | 72756 | tuple unpack, handler-preamble filter, defaults, docstring |
| 11 P0,P2 | 3967 | 72698 | STORE/LOAD combined-opcode encoding, arg order |
| **12 A1** | **1363** | **69510** | **terminal-jump orphan filter** |

---
## 4. Key File Quality

| File | Ver | Ratio | Cat | Orphans | Diff |
|:----|:---:|:-----:|:---:|:------:|:----:|
| abc.py | 2.7 | -88.0% | A | 0 | -184 |
| abc.py | 3.10 | -16.7% | A | 0 | -35 |
| abc.py | 3.11 | -17.2% | A | 4 | -36 |
| abc.py | 3.12 | -16.7% | A | 0 | -35 |
| abc.py | 3.13 | -17.2% | A | 0 | -36 |
| abc.py | 3.14 | -14.8% | A | 0 | -31 |
| abc.py | 3.5 | -29.2% | A | 2 | -61 |
| abc.py | 3.6 | -14.4% | A | 8 | -30 |
| abc.py | 3.7 | -29.7% | A | 0 | -62 |
| abc.py | 3.8 | -23.0% | A | 1 | -48 |
| abc.py | 3.9 | -22.0% | A | 1 | -46 |
| enum.py | 3.10 | -39.0% | A | 13 | -862 |
| enum.py | 3.11 | -36.5% | A | 54 | -807 |
| enum.py | 3.12 | -29.2% | A | 23 | -644 |
| enum.py | 3.13 | -42.6% | A | 20 | -941 |
| enum.py | 3.14 | -40.4% | A | 18 | -891 |
| enum.py | 3.6 | -30.3% | A | 111 | -669 |
| enum.py | 3.7 | -54.6% | A | 203 | -1206 |
| enum.py | 3.8 | -54.5% | A | 191 | -1203 |
| enum.py | 3.9 | -54.2% | A | 193 | -1197 |
| functools.py | 3.10 | -51.1% | A | 2 | -606 |
| functools.py | 3.11 | -35.6% | A | 37 | -422 |
| functools.py | 3.12 | -29.2% | A | 1 | -346 |
| functools.py | 3.13 | -28.0% | A | 1 | -332 |
| functools.py | 3.14 | -25.6% | A | 2 | -304 |
| functools.py | 3.8 | -50.8% | A | 72 | -602 |
| functools.py | 3.9 | -52.7% | A | 68 | -625 |
| pprint.py | 3.14 | -66.5% | A | 1 | -630 |
| reprlib.py | 3.10 | -38.5% | A | 2 | -89 |
| reprlib.py | 3.11 | -20.3% | A | 13 | -47 |
| reprlib.py | 3.12 | -13.0% | A | 0 | -30 |
| reprlib.py | 3.13 | -27.3% | A | 0 | -63 |
| reprlib.py | 3.14 | -16.0% | A | 0 | -37 |
| reprlib.py | 3.6 | -32.5% | A | 9 | -75 |
| reprlib.py | 3.7 | -44.2% | A | 25 | -102 |
| reprlib.py | 3.8 | -46.8% | A | 23 | -108 |
| reprlib.py | 3.9 | -42.4% | A | 25 | -98 |

---
## 5. Remaining Issues & Root Causes

### 5.1 Orphan Blocks (1363)

The remaining 1363 orphans cluster into two groups:

- **Type `other` (~700)**: Blocks with CALL/COMPARE_OP/etc that don't match any terminal-jump category
- **Type `flat_expr_*` (~260)**: Pure load/store expression blocks in small helper functions
- **Type `handler_pre` (0)**: All eliminated by Phase 10 P1 + 12 A1
- **Type `jump_cond` (0)**: All eliminated by Phase 12 A1
- **Primary concentration**: enum.py small helper funcs (`_is_dunder`, `_is_sunder`, `_is_internal_class`, `bin`)

### 5.2 abc.py 3.13/14 Residual
- `for (value, name)` vs original `for name, value` — variable order swapped (cosmetic)
- `cls.__bases__` iterable duplicate before for-loop (cosmetic)
- `value = getattr(name, cls, None)` argument swap — already fixed in Phase 11 P2

### 5.3 Formatting Fidelity
- **Blank line preservation**: No lnotab/linetable gap tracking
- **Import grouping**: Multi-line imports merged into single lines
- **Docstrings**: Module-level `"""..."""` correct; function-level single-line docstrings use `'...'` in some versions

---
## 6. Phase 13 Recommendations

| Priority | Issue | Impact | Effort |
|:--------:|:------|:------:|:------:|
| **P0** | Remaining orphan blocks (~1363) | 14% of files have orphans | 6h |
| **P1** | abc.py iterable duplication & variable order | abc.py cosmetic clarity | 3h |
| **P2** | Blank line preservation | Readability, all files | 3h |
| **P3** | Dark/deep: `BuildTryFromBlock` nested try restructuring | ~700 'other' orphans | 1-2w |

### Proposed Order

1. **P1 (3h)**: Fix iterable duplication and variable order in abc.py — mark predecessor blocks consumed
2. **P0 (6h)**: Target remaining 1363 orphans — classify and handle the 'other' and 'flat_expr' types
3. **P2 (3h)**: Implement lnotab/linetable blank-line tracking for readability

---
*Generated 2026-06-22 07:32*
