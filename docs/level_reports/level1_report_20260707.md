# Level 1 Baseline Test Report

**Level**: 1 — 基础控制流（if/else, for/while, break/continue, loop-else）
**Date**: 2026-07-07 19:36
**Source files**: 10
**Unique files in test**: 10
**Versions**: 11 (2.7, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14)
**Engine**: PyRebuilderSharp (dd577a8)
**Total time**: 8.8s

---

## 1. Executive Summary

| Metric | Value | Status |
|:-------|:-----:|:------:|
| Source files | 10 | |
| Unique decompiled results | 10 | |
| Total (file × version) | 90 | |
| Compile OK | 90 | ✅ |
| Compile FAIL (syntax inc.) | 20 | ⚠️ |
| Decompile OK | 90 | ✅ |
| Decompile FAIL | 0 | ❌ |
| **A class (≤3% diff)** | **0** | ✅ |
| **B class (≤15% diff)** | **0** | ✅ |
| C class (≤40% diff) | 8 | ⚠️ |
| D class (>40% diff) | 82 | ⚠️ |
| **A+B acceptable** | **0 (0%)** | |
| Total orphan blocks | 0 | ⚠️ |
| Total diff lines | 2084 | |

---

## 2. Per-Version Breakdown

| Version | OK | Fail | A | B | C | D | A+B% | Orphans |
|:-------:|:--:|:----:|:-:|:-:|:-:|:-:|:----:|:-------:|
| 2.7 | 0 | 0 | 0 | 0 | 0 | 0 | 0% | — |
| 3.5 | 0 | 0 | 0 | 0 | 0 | 0 | 0% | — |
| 3.6 | 10 | 0 | 0 | 0 | 1 | 9 | 0% | — |
| 3.7 | 10 | 0 | 0 | 0 | 1 | 9 | 0% | — |
| 3.8 | 10 | 0 | 0 | 0 | 1 | 9 | 0% | — |
| 3.9 | 10 | 0 | 0 | 0 | 1 | 9 | 0% | — |
| 3.10 | 10 | 0 | 0 | 0 | 1 | 9 | 0% | — |
| 3.11 | 10 | 0 | 0 | 0 | 0 | 10 | 0% | — |
| 3.12 | 10 | 0 | 0 | 0 | 1 | 9 | 0% | — |
| 3.13 | 10 | 0 | 0 | 0 | 1 | 9 | 0% | — |
| 3.14 | 10 | 0 | 0 | 0 | 1 | 9 | 0% | — |


---

## 3. File-Level Detail

| File | #Ver | Best | Worst | Orphans | Detail |
|:-----|:----:|:----:|:-----:|:-------:|:-------|
| l0_basic.py | 9 | 🔴D | 🔴D | 0 | 3.6:D(+13/-20), 3.7:D(+13/-20), 3.8:D(+13/-20), 3.9:D(+14/-21), 3.10:D(+14/-21)… |
| test_break_for.py | 9 | 🔴D | 🔴D | 0 | 3.6:D(+3/-2), 3.7:D(+3/-2), 3.8:D(+3/-2), 3.9:D(+3/-2), 3.10:D(+4/-2)… |
| test_brk_cont.py | 9 | 🔴D | 🔴D | 0 | 3.6:D(+2/-3), 3.7:D(+2/-3), 3.8:D(+2/-3), 3.9:D(+2/-3), 3.10:D(+4/-4)… |
| test_just_for.py | 9 | 🟠C | 🔴D | 0 | 3.6:C(+1/-0), 3.7:C(+1/-0), 3.8:C(+1/-0), 3.9:C(+1/-0), 3.10:C(+1/-0)… |
| test_continue_for.py | 9 | 🔴D | 🔴D | 0 | 3.6:D(+2/-1), 3.7:D(+2/-1), 3.8:D(+2/-1), 3.9:D(+2/-1), 3.10:D(+2/-2)… |
| if_else.py | 9 | 🔴D | 🔴D | 0 | 3.6:D(+12/-16), 3.7:D(+12/-16), 3.8:D(+12/-16), 3.9:D(+12/-16), 3.10:D(+17/-18)… |
| l1_control.py | 9 | 🔴D | 🔴D | 0 | 3.6:D(+29/-45), 3.7:D(+29/-45), 3.8:D(+25/-44), 3.9:D(+27/-48), 3.10:D(+35/-51)… |
| loop_else.py | 9 | 🔴D | 🔴D | 0 | 3.6:D(+21/-21), 3.7:D(+20/-21), 3.8:D(+11/-20), 3.9:D(+11/-20), 3.10:D(+17/-25)… |
| test_control_flow.py | 9 | 🔴D | 🔴D | 0 | 3.6:D(+5/-8), 3.7:D(+5/-8), 3.8:D(+6/-8), 3.9:D(+6/-8), 3.10:D(+3/-9)… |
| loop_else_simple.py | 9 | 🔴D | 🔴D | 0 | 3.6:D(+3/-3), 3.7:D(+3/-3), 3.8:D(+3/-3), 3.9:D(+3/-3), 3.10:D(+3/-4)… |


---

## 4. Hardest Files (C/D class)

| File | Version | Diff Lines | Ratio | Orphans | Core Issue |
|:-----|:-------:|:----------:|:-----:|:-------:|:-----------|
| l1_control.py | 3.12 | +41/-54 | 93.1% | 0 | (see displus) |
| l1_control.py | 3.13 | +41/-54 | 93.1% | 0 | (see displus) |
| l1_control.py | 3.11 | +36/-51 | 85.3% | 0 | (see displus) |
| l1_control.py | 3.14 | +33/-53 | 84.3% | 0 | (see displus) |
| l1_control.py | 3.10 | +35/-51 | 84.3% | 0 | (see displus) |
| l1_control.py | 3.9 | +27/-48 | 73.5% | 0 | (see displus) |
| l1_control.py | 3.6 | +29/-45 | 72.5% | 0 | (see displus) |
| l1_control.py | 3.7 | +29/-45 | 72.5% | 0 | (see displus) |
| l1_control.py | 3.8 | +25/-44 | 67.6% | 0 | (see displus) |
| loop_else.py | 3.12 | +29/-30 | 105.4% | 0 | (see displus) |


---

## 5. Improvement Analysis

### 5.1 Orphan Block Analysis
✅ 无 orphan 块

### 5.2 跨版本一致问题（9 个文件在大多数版本中为 D 类）

| File | Affected Versions |
|:-----|:-----------------|
| if_else.py | 3.10, 3.14, 3.11, 3.12, 3.8, 3.13, 3.9, 3.6, 3.7 |
| l0_basic.py | 3.6, 3.13, 3.7, 3.12, 3.8, 3.9, 3.11, 3.10, 3.14 |
| l1_control.py | 3.14, 3.10, 3.11, 3.12, 3.8, 3.13, 3.9, 3.6, 3.7 |
| loop_else.py | 3.13, 3.12, 3.9, 3.11, 3.10, 3.8, 3.14, 3.7, 3.6 |
| loop_else_simple.py | 3.13, 3.12, 3.11, 3.6, 3.7, 3.14, 3.10, 3.8, 3.9 |
| test_break_for.py | 3.11, 3.6, 3.14, 3.10, 3.7, 3.8, 3.9, 3.13, 3.12 |
| test_brk_cont.py | 3.14, 3.8, 3.10, 3.9, 3.11, 3.6, 3.7, 3.12, 3.13 |
| test_continue_for.py | 3.6, 3.7, 3.8, 3.11, 3.10, 3.14, 3.9, 3.13, 3.12 |
| test_control_flow.py | 3.11, 3.10, 3.14, 3.13, 3.7, 3.12, 3.6, 3.9, 3.8 |

这些文件在所有版本中表现一致，说明是**反编译器固有缺陷**而非版本特定问题。
查阅 displus 输出找共性 pattern。


### 5.3 按版本降级检查

| Version | C+D Ratio | Assessment |
|:-------:|:---------:|:-----------|
| 2.7 | 0% | ✅ 良好 |
| 3.5 | 0% | ✅ 良好 |
| 3.6 | 100% | 🔴 突出问题 |
| 3.7 | 100% | 🔴 突出问题 |
| 3.8 | 100% | 🔴 突出问题 |
| 3.9 | 100% | 🔴 突出问题 |
| 3.10 | 100% | 🔴 突出问题 |
| 3.11 | 100% | 🔴 突出问题 |
| 3.12 | 100% | 🔴 突出问题 |
| 3.13 | 100% | 🔴 突出问题 |
| 3.14 | 100% | 🔴 突出问题 |


### 5.4 推荐修复优先级

| Priority | Issue | Level Impact | Suggested Approach |
|:--------:|:------|:------------:|:-------------------|
| P2 | 解决 9 个跨版本 D 类文件的共性问题 | 9 files | 对比 displus 输出定位共性 pattern |


---

## 6. Sample: Worst File at Displus Detail

See `test_data/displus/level1/` for full per-file per-version pyc2displus dumps.
These contain complete bytecode, exception tables, lnotab, and code object details.

---

## 7. Next Steps

| Priority | Action |
|:--------:|:-------|
| P0 | Fix hardest file(s) in this level |
| P1 | Run test again to verify fix |
| P2 | Move to next level |
| P3 | Track per-level convergence across iterations |

---

*Report generated by `tools/test_by_level.py` on 2026-07-07 19:36*
