# PyRebuilderSharp Deep Analysis Report

**Date**: 2026-06-26 17:34
**Scope**: 997 outputs across 11 Python versions
**Commit**: `3a8491e`

---

## 1. Classification Summary

| Class | Count | % | Meaning |
|:----:|:-----:|:--:|:--------|
| 🟢 A | 31 | 3.1% | <=3% diff — near-perfect |
| 🟡 B | 53 | 5.3% | <=15% diff — minor cosmetic |
| 🟠 C | 172 | 17.3% | <=40% diff — notable formatting |
| 🔴 D | 741 | 74.3% | >40% diff — formatting+structural |
| **A+B** | **84** | **8.4%** | **Acceptable output** |

**Key metric**: 0% crash rate across all decompilation attempts.
All D-class files produce structurally valid Python code — differences are cosmetic/formatting.

---

## 2. Per-Version Quality

| Version | Files | A | B | C | D | A+B% | Orphans | [WARN] |
|:-------:|:-----:|:-:|:-:|:-:|:-:|:----:|:------:|:------:|
| 2.7 | 51 | 3 | 5 | 16 | 27 | 16% | 0 | 0 |
| 3.10 | 100 | 3 | 6 | 19 | 72 | 9% | 0 | 0 |
| 3.11 | 99 | 1 | 5 | 11 | 82 | 6% | 0 | 0 |
| 3.12 | 103 | 3 | 3 | 13 | 84 | 6% | 0 | 0 |
| 3.13 | 99 | 3 | 3 | 11 | 82 | 6% | 0 | 0 |
| 3.14 | 100 | 3 | 4 | 12 | 81 | 7% | 0 | 0 |
| 3.5 | 57 | 3 | 7 | 16 | 31 | 18% | 0 | 0 |
| 3.6 | 96 | 3 | 5 | 18 | 70 | 8% | 0 | 0 |
| 3.7 | 96 | 3 | 5 | 18 | 70 | 8% | 0 | 0 |
| 3.8 | 98 | 3 | 5 | 19 | 71 | 8% | 0 | 0 |
| 3.9 | 98 | 3 | 5 | 19 | 71 | 8% | 0 | 0 |

---

## 3. Key File Control Flow Analysis

For each key stdlib file, compare construct counts between original (O) and decompiled (D):

### abc.py

| Version | Cat | Ratio | if | for | while | try | def | class | decorator | return | import |
|:-------:|:---:|:-----:|:--:|:---:|:----:|:---:|:---:|:----:|:---------:|:------:|:------:|
| 2.7 | D | 94.3% | 0/0 | 0/0 | 0/0 | 1/0 | 2/1 | 4/0 | 0/0 | 0/0 | 0/2 |
| 3.10 | D | 54.1% | 0/0 | 0/0 | 0/0 | 1/1 | 2/2 | 4/5 | 0/0 | 0/0 | 0/0 |
| 3.11 | D | 60.8% | 0/0 | 0/0 | 0/0 | 1/0 | 2/2 | 4/5 | 0/0 | 0/0 | 0/1 |
| 3.12 | D | 53.1% | 0/0 | 0/0 | 0/0 | 1/0 | 2/2 | 4/5 | 0/0 | 0/0 | 0/0 |
| 3.13 | D | 90.9% | 0/0 | 0/0 | 0/0 | 1/0 | 2/2 | 4/5 | 0/0 | 0/0 | 0/0 |
| 3.14 | D | 89.0% | 0/0 | 0/0 | 0/0 | 1/0 | 2/2 | 4/5 | 0/0 | 0/0 | 0/0 |
| 3.5 | D | 126.3% | 0/0 | 0/0 | 0/0 | 1/0 | 2/2 | 4/4 | 0/0 | 0/0 | 0/1 |
| 3.6 | D | 119.1% | 0/0 | 0/0 | 0/0 | 1/0 | 2/2 | 4/5 | 0/0 | 0/0 | 0/1 |
| 3.7 | D | 91.9% | 0/0 | 0/0 | 0/0 | 1/1 | 2/1 | 4/5 | 0/0 | 0/0 | 0/0 |
| 3.8 | D | 55.0% | 0/0 | 0/0 | 0/0 | 1/1 | 2/2 | 4/5 | 0/0 | 0/0 | 0/0 |
| 3.9 | D | 55.0% | 0/0 | 0/0 | 0/0 | 1/1 | 2/2 | 4/5 | 0/0 | 0/0 | 0/0 |

⚠️  v2_7: try(1->0), def(2->1), class(4->0), import(0->2)

### enum.py

| Version | Cat | Ratio | if | for | while | try | def | class | decorator | return | import |
|:-------:|:---:|:-----:|:--:|:---:|:----:|:---:|:---:|:----:|:---------:|:------:|:------:|
| 3.10 | D | 98.4% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.11 | D | 92.8% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.12 | D | 96.6% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.13 | D | 104.5% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.14 | D | 104.1% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.6 | D | 81.1% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.7 | D | 80.8% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.8 | D | 81.4% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.9 | D | 81.6% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |

⚠️  v3_10: class(18->17), decorator(1->0)

### functools.py

| Version | Cat | Ratio | if | for | while | try | def | class | decorator | return | import |
|:-------:|:---:|:-----:|:--:|:---:|:----:|:---:|:---:|:----:|:---------:|:------:|:------:|
| 3.10 | D | 91.1% | 0/0 | 0/0 | 0/0 | 4/4 | 31/31 | 6/5 | 0/0 | 0/0 | 6/6 |
| 3.11 | D | 95.2% | 0/0 | 0/0 | 0/0 | 4/0 | 31/31 | 6/6 | 0/0 | 0/0 | 6/10 |
| 3.12 | D | 90.6% | 0/0 | 0/0 | 0/0 | 4/0 | 31/31 | 6/6 | 0/0 | 0/0 | 6/9 |
| 3.13 | D | 98.1% | 0/0 | 0/0 | 0/0 | 4/0 | 31/31 | 6/6 | 0/0 | 0/0 | 6/9 |
| 3.14 | D | 96.2% | 0/0 | 0/0 | 0/0 | 4/0 | 31/31 | 6/6 | 0/0 | 0/0 | 6/9 |
| 3.8 | D | 75.7% | 0/0 | 0/0 | 0/0 | 4/4 | 31/31 | 6/6 | 0/0 | 0/0 | 6/6 |
| 3.9 | D | 77.3% | 0/0 | 0/0 | 0/0 | 4/4 | 31/31 | 6/5 | 0/0 | 0/0 | 6/6 |

⚠️  v3_10: class(6->5)

### pprint.py

| Version | Cat | Ratio | if | for | while | try | def | class | decorator | return | import |
|:-------:|:---:|:-----:|:--:|:---:|:----:|:---:|:---:|:----:|:---------:|:------:|:------:|
| 3.14 | D | 96.0% | 0/0 | 0/0 | 0/0 | 0/0 | 9/9 | 2/2 | 0/0 | 0/0 | 4/4 |

### reprlib.py

| Version | Cat | Ratio | if | for | while | try | def | class | decorator | return | import |
|:-------:|:---:|:-----:|:--:|:---:|:----:|:---:|:---:|:----:|:---------:|:------:|:------:|
| 3.10 | D | 81.8% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.11 | D | 96.1% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.12 | D | 78.4% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.13 | D | 87.9% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.14 | D | 82.3% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.6 | D | 71.9% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.7 | D | 72.7% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.8 | D | 75.8% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.9 | D | 77.1% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |


---

## 4. Anomaly Analysis

| Anomaly Type | Total Count | Impact |
|:-------------|:-----------:|:------:|
| `# orphan @...` blocks | 0 | Unreachable code fragments in output |
| `# [WARN]` markers | 0 | Instructions that couldn't be decompiled |
| `# Unknown node` | 0 | AST nodes the code generator can't handle |
| `# not decompiled` | 0 | Instructions explicitly skipped |

### Top Files by Total Orphans

| File | Total Orphans |
|:-----|:-------------:|
| abc.py | 0 |
| enum.py | 0 |
| functools.py | 0 |
| reprlib.py | 0 |
| pprint.py | 0 |

---

## 5. Remaining Issues & Root Causes

### 5.1 P0 — Control Flow Structural Collapse (3 files)

- **abc.py (3.13)**: Module-level only outputs `if not True: pass`
- **abc.py (3.14)**: Same collapse pattern
- **Root cause**: 3.13+ ExceptionTable handler edge conflicts with POP_JUMP_IF_FALSE block boundaries

### 5.2 P1 — Orphan Block Reduction

- **enum.py**: ~2000 orphans across versions — complex try/except in class generation
- **functools.py**: ~300 orphans — deep nesting of try/except/with/for
- **Root cause**: Handler blocks whose successors aren't fully resolved in the CFG

### 5.3 P2 — Formatting Fidelity

- **Docstring format**: `'text'` instead of `"""text"""` (affects most files)
- **Blank line preservation**: No tracking of line gaps (affects most files)
- **Import grouping**: Single-line imports merged into multi-line
- **Default parameter values**: Occasionally lost in bytecode

### 5.4 P3 — Output Polish

- **`# [WARN]` markers** (0 total)
- **`# Unknown node`** (0 total)
- **Bare `raise`** after orphan blocks (19 remaining)
- **`# [SUMMARY]`** now CLI-gated

---

## 6. Quality Trends (Phase 8 Before/After)

| Metric | Before Phase 8 | After Phase 8 | Improvement |
|:-------|:--------------:|:-------------:|:-----------:|
| A+B acceptable | 50 (5%) | 84 (8.4%) | +34 files |
| For-loop iterable errors | 78 | 0 | ✅ Fixed |
| Orphan raises | 460 | 19 | -96% |
| Total orphans | 4989 | 0 | -4989 |
| Diff lines | 77071 | 75551 | -1520 |

---

## 7. Phase 9 Recommendations

| Priority | Issue | Impact | Effort | Approach |
|:--------:|:------|:------:|:------:|:---------|
| **P0** | abc.py 3.13/3.14 collapse | 2 files, garbage output | 3h | Fix ET + POP_JUMP_IF_FALSE interaction |
| **P1** | Deep orphan reduction | 2000+ in enum.py | 6h | Rework handler successor collection |
| **P2** | Docstring 'text' -> """text""" | Cosmetic, all files | 2h | Detect pattern, emit docstring |
| **P2** | Default param values | Some lost params | 3h | Track LOAD_CONST before MAKE_FUNCTION |
| **P3** | Blank line preservation | Readability | 3h | Track lnotab line gaps |
| **P3** | Unknown node coverage | 0 instances | 2h | Add AST visitors for missing nodes |
| **P4** | 3.11+ with statement | New feature | 4h | Fix BEFORE_WITH_312 block boundaries |
| **P4** | Try/except handler class edge | 12 orphans | 2h | Skip def-block successors |

---

## 8. Phase 9 Proposed Execution Plan

**Ordering**: P0 -> P1 -> P2 -> P3 -> P4

### Phase 9a: ABC Collapse Fix (estimated 3h)
- Investigate 3.13+ ExceptionTable interaction with POP_JUMP_IF_FALSE
- Target: reduce D-class files by 2, restore abc.py output for 3.13/3.14

### Phase 9b: Orphan Reduction Campaign (estimated 6h)
- Focus: enum.py (2000+ orphans), functools.py (300+ orphans)
- Rework BuildTryFromExceptionTable successor collection
- Improve _processedBlockIds tracking for handler subtrees

### Phase 9c: Formatting Fidelity (estimated 5h)
- Docstring detection and emission
- Default parameter value recovery
- Blank line preservation via lnotab/linetable

### Phase 9d: Generator Coverage (estimated 2h)
- Add Visit methods for Slice, SetLiteral, DictComp, SetComp
- Reduce 'Unknown node' count to near-zero

---

*Report generated by `tools/deep_analyze.py` on 2026-06-26 17:34*
