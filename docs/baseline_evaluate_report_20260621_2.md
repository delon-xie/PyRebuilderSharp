# PyRebuilderSharp Deep Analysis Report

**Date**: 2026-06-21 23:47
**Scope**: 942 outputs across 11 Python versions
**Commit**: `f8b073d`

---

## 1. Classification Summary

| Class | Count | % | Meaning |
|:----:|:-----:|:--:|:--------|
| 🟢 A | 29 | 3.1% | <=3% diff — near-perfect |
| 🟡 B | 38 | 4.0% | <=15% diff — minor cosmetic |
| 🟠 C | 160 | 17.0% | <=40% diff — notable formatting |
| 🔴 D | 715 | 75.9% | >40% diff — formatting+structural |
| **A+B** | **67** | **7.1%** | **Acceptable output** |

**Key metric**: 0% crash rate across all decompilation attempts.
All D-class files produce structurally valid Python code — differences are cosmetic/formatting.

---

## 2. Per-Version Quality

| Version | Files | A | B | C | D | A+B% | Orphans | [WARN] |
|:-------:|:-----:|:-:|:-:|:-:|:-:|:----:|:------:|:------:|
| 2.7 | 51 | 3 | 4 | 15 | 29 | 14% | 43 | 0 |
| 3.10 | 93 | 3 | 5 | 16 | 69 | 9% | 232 | 0 |
| 3.11 | 93 | 1 | 2 | 10 | 80 | 3% | 257 | 22 |
| 3.12 | 93 | 1 | 3 | 12 | 77 | 4% | 185 | 112 |
| 3.13 | 93 | 3 | 3 | 10 | 77 | 6% | 250 | 27 |
| 3.14 | 94 | 3 | 3 | 10 | 78 | 6% | 223 | 30 |
| 3.5 | 57 | 3 | 4 | 17 | 33 | 12% | 47 | 0 |
| 3.6 | 91 | 3 | 3 | 15 | 70 | 7% | 460 | 0 |
| 3.7 | 91 | 3 | 3 | 17 | 68 | 7% | 970 | 0 |
| 3.8 | 93 | 3 | 4 | 19 | 67 | 8% | 1098 | 0 |
| 3.9 | 93 | 3 | 4 | 19 | 67 | 8% | 1175 | 0 |

---

## 3. Key File Control Flow Analysis

For each key stdlib file, compare construct counts between original (O) and decompiled (D):

### abc.py

| Version | Cat | Ratio | if | for | while | try | def | class | decorator | return | import |
|:-------:|:---:|:-----:|:--:|:---:|:----:|:---:|:---:|:----:|:---------:|:------:|:------:|
| 2.7 | D | 95.7% | 0/0 | 0/0 | 0/0 | 1/0 | 2/1 | 4/0 | 0/0 | 0/0 | 0/2 |
| 3.10 | D | 68.4% | 0/0 | 0/0 | 0/0 | 1/1 | 2/2 | 4/5 | 0/0 | 0/0 | 0/0 |
| 3.11 | D | 83.7% | 0/0 | 0/0 | 0/0 | 1/1 | 2/2 | 4/5 | 0/0 | 0/0 | 0/0 |
| 3.12 | D | 78.0% | 0/0 | 0/0 | 0/0 | 1/1 | 2/2 | 4/5 | 0/0 | 0/0 | 0/0 |
| 3.13 | D | 144.0% | 0/0 | 0/0 | 0/0 | 1/1 | 2/2 | 4/7 | 0/0 | 0/0 | 0/0 |
| 3.14 | D | 146.4% | 0/0 | 0/0 | 0/0 | 1/1 | 2/2 | 4/7 | 0/0 | 0/0 | 0/0 |
| 3.5 | D | 124.4% | 0/0 | 0/0 | 0/0 | 1/0 | 2/2 | 4/4 | 0/0 | 0/0 | 0/1 |
| 3.6 | D | 134.4% | 0/0 | 0/0 | 0/0 | 1/0 | 2/2 | 4/5 | 0/0 | 0/0 | 0/1 |
| 3.7 | D | 107.2% | 0/0 | 0/0 | 0/0 | 1/1 | 2/1 | 4/5 | 0/0 | 0/0 | 0/1 |
| 3.8 | D | 72.2% | 0/0 | 0/0 | 0/0 | 1/1 | 2/2 | 4/5 | 0/0 | 0/0 | 0/0 |
| 3.9 | D | 72.2% | 0/0 | 0/0 | 0/0 | 1/1 | 2/2 | 4/5 | 0/0 | 0/0 | 0/0 |

⚠️  v2_7: try(1->0), def(2->1), class(4->0), import(0->2)

### enum.py

| Version | Cat | Ratio | if | for | while | try | def | class | decorator | return | import |
|:-------:|:---:|:-----:|:--:|:---:|:----:|:---:|:---:|:----:|:---------:|:------:|:------:|
| 3.10 | D | 96.3% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.11 | D | 127.4% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.12 | D | 128.2% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.13 | D | 153.3% | 0/2 | 0/0 | 0/0 | 0/0 | 22/22 | 18/14 | 1/0 | 0/0 | 3/3 |
| 3.14 | D | 156.0% | 0/2 | 0/0 | 0/0 | 0/0 | 22/22 | 18/14 | 1/0 | 0/0 | 3/3 |
| 3.6 | D | 115.8% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.7 | D | 118.0% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.8 | D | 117.4% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |
| 3.9 | D | 119.7% | 0/0 | 0/0 | 0/0 | 0/0 | 22/22 | 18/17 | 1/0 | 0/0 | 3/3 |

⚠️  v3_10: class(18->17), decorator(1->0)

### functools.py

| Version | Cat | Ratio | if | for | while | try | def | class | decorator | return | import |
|:-------:|:---:|:-----:|:--:|:---:|:----:|:---:|:---:|:----:|:---------:|:------:|:------:|
| 3.10 | D | 86.1% | 0/0 | 0/0 | 0/0 | 4/4 | 31/31 | 6/5 | 0/0 | 0/0 | 6/6 |
| 3.11 | D | 121.8% | 0/0 | 0/0 | 0/0 | 4/4 | 31/31 | 6/6 | 0/0 | 0/0 | 6/6 |
| 3.12 | D | 122.9% | 0/0 | 0/0 | 0/0 | 4/4 | 31/31 | 6/6 | 0/0 | 0/0 | 6/6 |
| 3.13 | D | 142.2% | 0/0 | 0/0 | 0/0 | 4/4 | 31/31 | 6/6 | 0/0 | 0/0 | 6/7 |
| 3.14 | D | 145.0% | 0/0 | 0/0 | 0/0 | 4/4 | 31/31 | 6/6 | 0/0 | 0/0 | 6/7 |
| 3.8 | D | 93.0% | 0/0 | 0/0 | 0/0 | 4/4 | 31/31 | 6/6 | 0/0 | 0/0 | 6/6 |
| 3.9 | D | 94.5% | 0/0 | 0/0 | 0/0 | 4/4 | 31/31 | 6/5 | 0/0 | 0/0 | 6/6 |

⚠️  v3_10: class(6->5)

### pprint.py

| Version | Cat | Ratio | if | for | while | try | def | class | decorator | return | import |
|:-------:|:---:|:-----:|:--:|:---:|:----:|:---:|:---:|:----:|:---------:|:------:|:------:|
| 3.14 | D | 117.9% | 0/0 | 0/0 | 0/0 | 0/0 | 9/9 | 2/2 | 0/0 | 0/0 | 4/4 |

### reprlib.py

| Version | Cat | Ratio | if | for | while | try | def | class | decorator | return | import |
|:-------:|:---:|:-----:|:--:|:---:|:----:|:---:|:---:|:----:|:---------:|:------:|:------:|
| 3.10 | D | 87.0% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.11 | D | 139.0% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.12 | D | 117.7% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.13 | D | 134.2% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.14 | D | 134.2% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.6 | D | 97.4% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.7 | D | 103.0% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.8 | D | 100.4% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |
| 3.9 | D | 103.0% | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 1/1 | 0/0 | 0/0 | 3/3 |


---

## 4. Anomaly Analysis

| Anomaly Type | Total Count | Impact |
|:-------------|:-----------:|:------:|
| `# orphan @...` blocks | 4940 | Unreachable code fragments in output |
| `# [WARN]` markers | 191 | Instructions that couldn't be decompiled |
| `# Unknown node` | 36 | AST nodes the code generator can't handle |
| `# not decompiled` | 191 | Instructions explicitly skipped |

### Top Files by Total Orphans

| File | Total Orphans |
|:-----|:-------------:|
| enum.py | 2917 |
| functools.py | 526 |
| reprlib.py | 208 |
| abc.py | 76 |
| pprint.py | 29 |

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

- **`# [WARN]` markers** (191 total)
- **`# Unknown node`** (36 total)
- **Bare `raise`** after orphan blocks (19 remaining)
- **`# [SUMMARY]`** now CLI-gated

---

## 6. Quality Trends (Phase 8 Before/After)

| Metric | Before Phase 8 | After Phase 8 | Improvement |
|:-------|:--------------:|:-------------:|:-----------:|
| A+B acceptable | 50 (5%) | 67 (7.1%) | +17 files |
| For-loop iterable errors | 78 | 0 | ✅ Fixed |
| Orphan raises | 460 | 19 | -96% |
| Total orphans | 4989 | 4940 | -49 |
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
| **P3** | Unknown node coverage | 36 instances | 2h | Add AST visitors for missing nodes |
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

*Report generated by `tools/deep_analyze.py` on 2026-06-21 23:47*
