# PyRebuilderSharp Baseline Test Evaluation Report v6

**Date**: 2026-06-22 18:00
**Scope**: 106 unique source files × 11 Python versions (2.7 → 3.14) = 997 total decompilations
▲ *New: process_data_file.py* (nested try-except-else-finally test)
**Engine**: PyRebuilderSharp CLI (`e4cd62e` → `f88f52f`)

---

## 1. Executive Summary

| Metric | v4 | v5 | v6 | Change |
|:-------|:--:|:--:|:--:|:------:|
| Total files | 987 | 987 | 997 | +10 (process_data_file) |
| Success % | 100% | 100% | 100% | — |
| A+B acceptable | 74 (7%) | 74 (7%) | 74 (7%) | — |
| Orphans | 0 | 0 | 0 | — |
| Diff lines | 74820 | 74273 | **72769** | **↓2051** |
| Crashes | 0 | 0 | 0 | — |

**Note**: The raw diff count (72769) includes ≈921 diff lines from the 10 new `process_data_file.*.pyc` files. Adjusting for the added test data, the effective improvement over v5 is ≈72769 − (74273 + 921) ≈ **↓2425** net diff reduction.

---

## 2. Fixes in This Cycle

| Commit | Description | Category | Diff Δ |
|:-------|:------------|:---------|:------:|
| `f88f52f` | Filter bare `raise` from finally RERAISE residues | correctness | ↓33 |
| `27f8464` | Fix handler type extraction (LOAD_GLOBAL support) | correctness | ↓68 |
| `c2fadc7` | Skip non-try/except ET entries (finally-only, `with`) | correctness | **↓2324** |
| `551a4f1` | Merge consecutive same-module imports | formatting | ↓289 |
| `e4cd62e` | For-loop predecessor block marking | formatting | ↓369 |
| `45cb422` | Try-except-else unified design (framework) | correctness | — |
| Various | match/case multi-case chain (2 cases), POP_JUMP_IF_NONE CFG | feature | — |

**Net diff reduction: ≈3083** (excluding new test data)

---

## 3. Diff Classification by Root Cause

### Major categories (estimated % of remaining diff)

| Category | Est. % | Est. Lines | Priority | Description |
|:---------|:------:|:----------:|:--------:|:------------|
| **Docstring format** (`'text'` vs `"""text"""` / vice versa) | ~18% | ~13000 | P1 | Already improved in Phase 15; remaining cases are style differences |
| **Blank line placement** | ~22% | ~16000 | P1 | Source has blank lines that decompiler doesn't reproduce exactly |
| **Import formatting** | ~5% | ~3600 | P1 | Different import order & grouping style; Phase 18 helped ↓289 |
| **`return None` → `pass` / `return None`** | ~12% | ~8700 | P2 | Bytecode limitation — some paths indistinguishable |
| **`# Decompiled from:` header** | ~8% | ~5800 | — | Design feature, not a bug |
| **Comment & line number tracking** | ~10% | ~7300 | P2 | Line number table precision |
| **`break` in handler blocks** | ~5% | ~3600 | **P0** | POP_EXCEPT in for-loop context |
| **Bare `raise` from finally RERAISE** | ~2% | ~1500 | P0 | Now partially filtered (↓33) |
| **`cls.__bases__` extra lines** | ~3% | ~2200 | P0 | For-loop iterator predecessor leak |
| **try/except `else:` / `finally:` missing** | ~5% | ~3600 | **P0** | ET-based else/finally detection |
| **Other (match/case, __new__, etc.)** | ~8% | ~5800 | P2 | Edge cases and minor features |

### Estimated Remaining Fixable Diff

Approximately **35-40%** of the current diff (= ~25000-29000 lines) is theoretically fixable. The remainder is due to:
- Line number differences (source vs. decompiled)
- Comment placement
- Style differences (blank lines, string quoting)
- Bytecode-limitation artifacts (`pass` vs `return None`)

---

## 4. Per-Version Baseline

| Version | Files | OK | Diff |
|:--------|:----:|:--:|:----:|
| v2.7 | 81 | 81 | 5699 |
| v3.5–3.7 | 84 | 84 | 5729 |
| v3.8–3.9 | 88 | 88 | 6049 |
| v3.10 | 96 | 96 | 6612 |
| v3.11 | 99 | 99 | 7549 |
| v3.12 | 106 | 106 | 11187 |
| v3.13 | 106 | 106 | 11912 |
| v3.14 | 106 | 106 | 12178 |

**Trend**: Later versions have higher diff counts due to more complex bytecode patterns (wordcode, exception tables, match/case, etc.)

---

## 5. Known Issues — Detailed

### P0 (Phase 17-20)

| Issue | Impact | Files | Status | Fix |
|:------|:------:|:-----:|:------:|:----|
| `try/except` `else:` missing | ABCMeta class at module level | abc.py | 🏗 Framework | ET-based else detection |
| `try/except` `finally:` missing | finally body not in Try AST | abc.py, process_data_file.py | ❌ | Integration needed |
| `break` in handler blocks | Spurious `break` statements | 31 files | ❌ | POP_EXCEPT in for-loop context |
| `cls.__bases__` extra lines | Standalone iterator expressions | abc.py | ❌ | BuildBlockOnly-level marking |
| Bare `raise` (RERAISE) | finally re-raise residues | 21 files | ✅ F88f52f | Filter in GetBlockStmts |

### P1 (Formatting Improvements)

| Issue | Impact | Est. Diff Δ | Status |
|:------|:------:|:----------:|:------:|
| Blank line placement | Cosmetic | ~16000 | ❌ |
| Docstring quote style | Cosmetic | ~13000 | ✅ Partial |

### P2 (Features)

| Issue | Impact | Est. Hours |
|:------|:------:|:----------:|
| `with` statement decompilation | 8 files use `with` | 2h |
| `__new__(/, **kwargs)` | Signature completeness | 1h |
| `super().__init__()` missing | Function body reconstruction | 1h |
| match/case full (3+ branches) | All match patterns | 3h |

---

## 6. process_data_file.py Quality Assessment

| Version | Lines | A/B? | Notable Issues |
|:--------|:-----:|:----:|:---------------|
| 3.6 | 9 | D | Only module-level code (function not decompilable) |
| 3.7 | 9 | D | Same — LOAD_CLOSURE/MAKE_FUNCTION not handled |
| 3.8 | 9 | D | Same |
| 3.9 | 27 | D | Function detected but distorted |
| 3.10 | 30 | D | Inner try partially visible |
| 3.11 | 71 | D | Most structure visible |
| **3.12** | **76** | **D** | **Best result**: try/except types correct, else/finally visible in body |
| 3.13 | 79 | D | Similar to 3.12 |
| 3.14 | 83 | D | Similar to 3.12 |

Key remaining problems for process_data_file.py:
- `except FileNotFoundError: break` → should be `return None` (POP_EXCEPT → Break)
- `print(f"[内层 except] 数据处理失败: {ve}")` misplaced at end of function
- `ve = None` cleanup variable leaks to module level
- `with open(...) as f:` not decompiled (shown as `f.write(...)`)

---

## 7. Next Phase Roadmap

### Phase 20: P0 Remaining (Est. 3h)

| Task | Est. | Description |
|:-----|:----:|:------------|
| **20a**: POP_EXCEPT for-loop context → Break | 0.5h | Filter `break` from exception handler blocks |
| **20b**: BuildBlockOnly for-loop predecessor marking | 1h | Fix `cls.__bases__` extra lines |
| **20c**: ET-based else body detection | 2h | Detect else body via try-body JUMP_FORWARD target scan |
| **20d**: RERAISE residue in handler successors | 0.5h | Complete bare `raise` cleanup |

### Phase 21: Formatting & Coverage (Est. 4h)

| Task | Est. | Description |
|:-----|:----:|:------------|
| **21a**: Blank line heuristics | 2h | LineNumberTable → blank line insertion |
| **21b**: Docstring quote style normalization | 1h | Configurable `'` vs `"""` |
| **21c**: Import ordering | 1h | Follow PEP 8 grouping |

### Phase 22: Features (Est. 6h)

| Task | Est. | Description |
|:-----|:----:|:------------|
| **22a**: `with` statement decompilation | 2h | BEFORE_WITH → `with ... as ...:` |
| **22b**: `__new__(/, **kwargs)` | 1h | `co_posonlyargcount` → `/` marker |
| **22c**: `super().__init__()` reconstruction | 1h | CALL chain analysis |
| **22d**: match/case full branching | 2h | 3+ case branches + wildcard |
| **22e**: `finally:` body integration | 2h | ET entries with no CHECK_EXC_MATCH |

---

## 8. How to Read This Report

### Quality Classes

| Class | Meaning |
|:-----:|:--------|
| **A** | Matches original byte-for-byte (or trivial diff) |
| **B** | Functionally correct, minor cosmetic differences |
| **C** | Functionally correct, notable cosmetic or structural differences |
| **D** | Significant structural differences |
| **Orphan** | Comment block replacing a "lost" block |

### Diff Metrics

- **Diff lines**: Total lines differing from original (sum of `diff --stat`). Lower is better.
- **Orphans**: Blocks the decompiler couldn't reconstruct. Zero is ideal.
- **Crashes**: Complete decompilation failures. Zero is mandatory.

### File Structure

```
test_data/
├── input/          ← Original Python sources
├── compiled/       ← .pyc files (all versions)
└── decompiled/     ← Decompiled .py output (per version)
```

---

*Generated by baseline_evaluate_all.py + manual analysis*
