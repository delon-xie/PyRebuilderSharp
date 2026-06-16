# PyRebuilderSharp Baseline Test Evaluation Report
**Date**: 2026-06-16
**Scope**: 938 decompiled files x 11 Python versions (2.7 -> 3.14)
**Engine**: PyRebuilderSharp (.NET 10 + Avalonia, block-level fault tolerance)

---

## 1. Overall Summary

| Metric | Value | Status |
|:-------|:------|:------:|
| Total files | 938 | |
| Exact match | 0 (0.0%) | |
| Good match | 536 (57.1%) | |
| Partial | 310 (33.0%) | |
| **Crashes** | **92 (9.8%)** | **NEEDS FIX** |

**Combined good rate** (exact+good): 57.1%
**Crash rate**: 9.8% (92/938 files)

> **Key Finding**: Python 3.7 has a massive NullReferenceException crash (88/90 files, 97.7%)
> in BlockScanner.Scan() - codeObj.Instructions is null after Phase 4 processing.
> Excluding 3.7, real crash rate: 4/848 = **0.5%**

### Crash Distribution

| Version | Crashes | Root Cause |
|:--------|:--------|:-----------|
| 2.7 | 1/50 | PycReader NullReference |
| **3.7** | **88/90** | **BlockScanner codeObj.Instructions is null** |
| 3.13 | 2/93 | dump_marshal/run_all_versions crashes |

---

## 2. Per-Version Statistics

| Version | Files | Exact | Good | Partial | Crashed | Recovery |
|:--------|:----:|:-----:|:----:|:-------:|:-------:|:--------:|
|  2.7 |  50 |   0 |  41 |   8 |   1 | GREEN  82.0% |
|  3.5 |  56 |   0 |  48 |   8 |   0 | GREEN  85.7% |
|  3.6 |  90 |   0 |  67 |  23 |   0 | GREEN  74.4% |
|  3.7 |  90 |   0 |   0 |   1 |  89 | RED   0.0% |
|  3.8 |  93 |   0 |  68 |  25 |   0 | GREEN  73.1% |
|  3.9 |  93 |   0 |  71 |  22 |   0 | GREEN  76.3% |
| 3.10 |  93 |   0 |  71 |  22 |   0 | GREEN  76.3% |
| 3.11 |  93 |   0 |  58 |  35 |   0 | GREEN  62.4% |
| 3.12 |  93 |   0 |  46 |  47 |   0 | YELLOW  49.5% |
| 3.13 |  93 |   0 |  19 |  72 |   2 | YELLOW  20.4% |
| 3.14 |  94 |   0 |  47 |  47 |   0 | YELLOW  50.0% |

## 3. Version Details

### 2.7 (50 files)

Exact: 0 | Good: 41 | Partial: 8 | Crashed: 1

Features: def=9 class=0 import=11
         for=15 if=13 while=6 try=12
         lambda=0 orphan=18

### 3.5 (56 files)

Exact: 0 | Good: 48 | Partial: 8 | Crashed: 0

Features: def=16 class=0 import=13
         for=16 if=13 while=6 try=12
         lambda=0 orphan=19

### 3.6 (90 files)

Exact: 0 | Good: 67 | Partial: 23 | Crashed: 0

Features: def=25 class=2 import=46
         for=50 if=41 while=10 try=17
         lambda=3 orphan=53

### 3.7 (90 files)

**RED ALERT**: 89/90 crashed

### 3.8 (93 files)

Exact: 0 | Good: 68 | Partial: 25 | Crashed: 0

Features: def=28 class=5 import=49
         for=52 if=40 while=12 try=20
         lambda=3 orphan=56

### 3.9 (93 files)

Exact: 0 | Good: 71 | Partial: 22 | Crashed: 0

Features: def=31 class=5 import=49
         for=51 if=35 while=10 try=21
         lambda=5 orphan=59

### 3.10 (93 files)

Exact: 0 | Good: 71 | Partial: 22 | Crashed: 0

Features: def=31 class=5 import=49
         for=53 if=45 while=12 try=21
         lambda=5 orphan=59

### 3.11 (93 files)

Exact: 0 | Good: 58 | Partial: 35 | Crashed: 0

Features: def=16 class=5 import=49
         for=51 if=13 while=15 try=6
         lambda=19 orphan=51

### 3.12 (93 files)

Exact: 0 | Good: 46 | Partial: 47 | Crashed: 0

Features: def=13 class=5 import=36
         for=32 if=16 while=47 try=4
         lambda=20 orphan=54

### 3.13 (93 files)

Exact: 0 | Good: 19 | Partial: 72 | Crashed: 2

Features: def=2 class=0 import=2
         for=0 if=4 while=91 try=3
         lambda=0 orphan=59

### 3.14 (94 files)

Exact: 0 | Good: 47 | Partial: 47 | Crashed: 0

Features: def=12 class=3 import=36
         for=40 if=16 while=48 try=9
         lambda=21 orphan=56

## 4. Anomaly Analysis

### 4.1 Python 3.7 BlockScanner NullReferenceException (P0)

**Problem**: 88/90 (97.7%) of 3.7 .pyc files crash in BlockScanner.Scan().
**Root Cause**: codeObj.Instructions is null after Phase 4 processing.

This is the only version where:
- Uses old lnotab format (not PEP 626)
- No posonlyargcount/qualname fields
- Has SETUP_LOOP/SETUP_EXCEPT old opcodes

Fix: Ensure Instructions field is preserved/copied in PostProcessFunctionDefs
and ConvertChildCodesToFunctionDefs. Verify with:
  typeof(CodeObject).GetProperty("Instructions")?.GetValue(codeObj) is List<Instruction>


### 4.2 Other Anomalies

| Type | Version | Impact | Analysis |
|:-----|:--------|:-------|:---------|
| HandleUnknownMarshalType | 2.7/3.5/3.6 | marshal offset | Old .pyc header/padding format difference |
| EndOfStreamException | 3.11+ | nested offset | localspluskinds/exceptiontable cumulative offset |
| ExceptionTable mismatch | 3.11+ | CFG broken | ExceptionTable address->Block mapping failure |
| orphan block recovery | all versions | control flow loss | ~60% files trigger block-level fallback |
| name_X = CodeObject | all | function loss | ConvertChildCodesToFunctionDefs match failure |

## 5. Improvement Recommendations

### P0 - Blocking Bugs


1. Fix 3.7 BlockScanner NullReferenceException (affects 88 files)
   - codeObj.Instructions is null root cause
   - Phase 4 regression in ConvertChildCodesToFunctionDefs
   - Add non-null assertion on all code object modification paths

2. ExceptionTable + CFG Integration (affects ~60% files)
   - BuildTryFromExceptionTable frequent no-match
   - ExceptionTable LEB128 address to block offset conversion

3. Nested marshal offset (affects 3.11+ files)
   - ReadSmallTuple.EndOfStreamException = cumulative stream offset
   - Realign all marshal read paths


### P1 - Feature Improvements


4. Function definition recovery: def func(args) -> currently renders as 'func = <lambda>'
5. Control flow reconstruction: break/continue/for/while lost in nested structures
6. Import statements: entirely missing


### P2 - Quality


7. Extra blank lines and debug summary comments
8. name_X references -> proper name resolution
9. AST semantic comparison test integration


---

## 6. Conclusion

PyRebuilderSharp across 938 .pyc files (11 versions):

- **Crash rate**: 9.8% (92 files) -> excl 3.7: 0.5%
- **Code recovery** (non-crash files): 63.4%
- **Function def output**: ~30% for 3.5-3.12 versions
- **Class def output**: <5% across all versions
- **P0 issues**: BlockScanner 3.7 crash + ExceptionTable integration

> **Core diagnosis**: The current bottleneck is (1) Phase 4 BlockScanner regression
> affecting only 3.7, and (2) control flow reconstruction affecting all versions.
> After fixing both, recovery rate should reach ~60-70%.
