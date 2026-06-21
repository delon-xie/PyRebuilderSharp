# PyRebuilderSharp Phase 8 Improvement Plan: Iterable Fix & Quality Push

**Date**: 2026-06-21
**Current commit**: `5251dfd`
**Baseline report**: `docs/baseline_evaluate_report_20260621.md`

---

## Current Baseline State

| Metric | Value | Status |
|:-------|:------|:------:|
| Decompilation success | 942/942 (100%) | ✅ |
| xUnit tests passing | 104/109 (95.4%) | ✅ (5 known_issue) |
| A+B class (≤15% diff) | 50/942 (5%) | ⚠️ |
| C class (≤40% diff) | 68/942 (7%) | ⚠️ |
| D class (>40% diff) | 824/942 (87%) | ⚠️ |
| Orphan blocks | 4989 | ⚠️ |
| **For-loop iterable errors** | **78 instances** | **❌ P0** |
| **Orphan `raise` injections** | **261 instances** | **❌ P1** |

## Prioritized Improvement Plan

### Phase 8a: P0 — Fix for-loop iterable confusion 🔴 (4h)

**The biggest semantic bug in the decompiler.**

**Problem**: `ExtractIterExpression()` (AstBuilder.cs:2747) walks the predecessor chain of a for-loop header and evaluates ALL instructions via StackMachine. When a predecessor block contains comparison expressions (from while-loop conditions or unrelated comparisons), the wrong stack value is returned as the iterable.

**Example**: `for i in range(n):` becomes `for i in j < i:`

**Fix approach**: Track `GET_ITER` opcode consumption in StackMachine. The instruction `GET_ITER` pops one value (the iterable) and pushes one value (the iterator). We need to:
1. Add `StackMachine` instrumentation for `GET_ITER` — record which expression it consumed
2. In `ExtractIterExpression`, instead of scanning predecessors, scan the for-loop header's own instructions for the pattern `[iterable-expr, GET_ITER, FOR_ITER]`
3. Re-trace from the header block to find the expression just before `GET_ITER`

**Files to modify**:
- `src/PyRebuilderSharp.Core/Builders/AstBuilder.cs` — `ExtractIterExpression` rewrite
- Potentially `src/PyRebuilderSharp.Core/StackMachine.cs` — `GET_ITER` tracking

**Verification**: Run baseline_evaluate_all.py — the 78 "for x in comparison" patterns must drop to 0. Key files to verify: mixed5_out.py, enum.py, debug_blocks.py, lv2_eval.py.

---

### Phase 8b: P1 — Suppress orphan `raise` statements 🟠 (1h)

**Problem**: After orphan blocks (marked with `# orphan @...`), the decompiler emits `raise` from `RAISE_VARARGS 0` opcodes. These are unreachable exception re-raises from orphaned handler blocks. 261 instances across all versions.

**Fix approach**: In the code generator (or during AST building), detect `raise` statements that appear immediately after an orphan block and suppress them. These are unreachable instructions from lost exception handler contexts.

**Files to modify**:
- `src/PyRebuilderSharp.Core/Generators/PythonCodeGenerator.cs` — suppress raise when preceded by orphan output
- OR `src/PyRebuilderSharp.Core/Builders/AstBuilder.cs` — filter orphan block's RAISE_VARARGS

**Verification**: Run the orphan raise scanner — count must drop to 0.

---

### Phase 8c: P1 — `with` statement recovery 🟠 (4h)

**Problem**: `with` context manager blocks compile to `SETUP_WITH` → body → `POP_BLOCK` → `WITH_EXCEPT_START` → cleanup. Currently decompiled as raw try/except with no `with` structure.

**Fix approach**: Detect `SETUP_WITH` / `WITH_EXCEPT_START` opcode patterns in BlockScanner and map them to a `With` AST node with context expression and body.

**Files to modify**:
- `src/PyRebuilderSharp.Core/Builders/AstBuilder.cs` — BuildWithStatement
- `src/PyRebuilderSharp.Core/Generators/PythonCodeGenerator.cs` — VisitWith
- AST model — `With` statement node

---

### Phase 8d: P2 — CFG handler→class edge fix 🟡 (4h)

(from previous report, still relevant)

**Problem**: ~50 files where class/function defs after handler blocks are misclassified as handler successors.

---

### Phase 8e: P3 — Debug noise cleanup ⚪ (2h)

**Quick wins — CLI flags**:

1. `# [SUMMARY]` noise — gate behind `--verbose`/`--debug` CLI flag
2. `# Decompiled from:` header — same flag
3. Module-level `return None` — skip for module-level AST root

---

## Execution Strategy

| Phase | Task | Effort | Type | Dependencies |
|:-----:|:-----|:------:|:----:|:------------|
| 8a | Fix for-loop iterable confusion | **4h** | Semantic fix | None |
| 8b | Suppress orphan `raise` statements | **1h** | Semantic fix | None |
| 8c | `with` statement recovery | **4h** | New feature | AST model + BlockScanner |
| 8d | CFG handler→class edge | **4h** | Bug fix | Phase 8a first? |
| 8e | Debug noise cleanup | **2h** | Quality | CLI changes |

**Recommended ordering**: 8a → 8b → 8d → 8e → 8c

---

## Verification for Each Phase

After each phase, run:
```bash
dotnet test tests/PyRebuilderSharp.Tests/ -c Release 2>&1 | tail -5
python3 tools/baseline_evaluate_all.py
```

And check:
- xUnit: 104 pass, 5 known_issue (no regression)
- Baseline: no new crashes, 0 new orphans
- Specific: 78 for-loop errors → 0, 261 orphan raises → 0

---

*Plan generated 2026-06-21 after baseline evaluation at commit `5251dfd`*
