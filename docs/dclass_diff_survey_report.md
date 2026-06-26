# D-Class Decompiled File Diff Category Survey Report

**Date**: 2026-06-26
**Files Surveyed**: 31 D-class decompiled files across Python versions 3.10–3.14
**Files Included**: reprlib.py (v3.10–3.14), pprint.py (v3.14), functools.py (v3.10–3.14), enum.py (v3.10–3.14), abc.py (v3.10–3.14), check_35_fields.py (v3.10–3.13), check_py27_magic.py (v3.10–3.11), test_for_try.py (v3.11–3.12), match_simple.py (v3.10–3.11)

## Category Frequency (sorted by prevalence)

| Rank | Category | Count | % | Description |
|:----:|:---------|:-----:|:-:|:------------|
| 1 | **HEADER** | 31/31 | 100% | `# Decompiled from:` tag replaces original copyright/author headers |
| 2 | **BLANK_LINES** | 27/31 | 87% | Blank lines between function/class definitions are lost |
| 3 | **IMPORT_FORMAT** | 25/31 | 81% | Multi-line imports collapsed; import count/grouping differs |
| 4 | **SEMANTIC_ERROR** | 23/31 | 74% | Lost try/except/else blocks; simplified boolean logic; missing else branches |
| 5 | **TRY_EXCEPT_MISSING** | 22/31 | 70% | Entire try/except blocks absent from decompiled output |
| 6 | **ALL_TUPLE** | 16/31 | 52% | `__all__ = [...]` → `__all__ = (...)` list→tuple conversion |
| 7 | **FUNC_CALL_SYNTAX** | 11/31 | 35% | `[new_func](**kwargs)` / `[]()` bracket-call syntax errors |
| 8 | **KWARG_ORDER** | 7/31 | 22% | Keyword arguments reversed in function calls (e.g., PrettyPrinter) |
| 9 | **CALL_EXPR_FRAGMENT** | 3/31 | 10% | String-literal method calls: `', '.join` → `','.join % ','(...)` |
| 10 | **DOCSTRING_FORMAT** | 3/31 | 10% | `"""text"""` → `__doc__ = 'text'` or single-quote conversion |
| 11 | **DEFAULT_PARAMS_LOST** | 2/31 | 6% | `def foo(x=None)` → `def foo(x)` — default parameter values lost |
| 12 | **VARIABLE_NAME** | 1/31 | 3% | `.cell` used as variable name instead of proper name |

## Concrete Examples Per Category

### 1. HEADER (100%)
```
-#  Author:      Fred L. Drake, Jr.
-#  Copyright (C) 2006 Python Software Foundation.
-# Written by Nick Coghlan <ncoghlan at gmail.com>,
+# Decompiled from: <module>
```

### 2. BLANK_LINES (87%)
Original had blank lines between all function/class definitions. Decompiled lost all of them:
- reprlib.py: 10 blank lines → 0
- functools.py: 99 blank lines → 8
- pprint.py: 55 blank lines → 0

### 3. IMPORT_FORMAT (81%)
Multi-line imports collapsed to single-line, or import grouping changed:
```
-import math, sys
+import math
+import sys
```
Parenthesized multi-line imports flattened:
```
-from _abc import (get_cache_token, _abc_init, _abc_register,
-                  _abc_instancecheck, _abc_subclasscheck)
+from _abc import get_cache_token, _abc_init, _abc_register, _abc_instancecheck, _abc_subclasscheck
```

### 4. SEMANTIC_ERROR (74%)
**Lost else branches**: `try/except/else` loses the `else:` clause entirely:
```
 try:
     from _abc import ...
 except ImportError:
     from _py_abc import ABCMeta
-else:
-    class ABCMeta(type):
```
**Simplified boolean logic**: `return op_result or self == other` → `if op_result: return ... return self == other`
```
-    return op_result or self == other
+    if op_result:
+        return
+    return self == Other
```

### 5. TRY_EXCEPT_MISSING (70%)
Entire try/except blocks absent from decompiled output:
- abc.py v3.11+: entire try/except/else block removed
- reprlib.py v3.10+: 5 try blocks in original → 0 in decompiled
- functools.py v3.10+: 18 try blocks → 0

### 6. ALL_TUPLE (52%)
```
-__all__ = ["Repr", "repr", "recursive_repr"]
+__all__ = ('Repr', 'repr', 'recursive_repr')
```

### 7. FUNC_CALL_SYNTAX (35%)
**Bracket call syntax**: `[new_func](**self.keywords)` instead of `new_func(*self.args, **self.keywords)`
**Empty list call**: `[](...)` pattern — empty list used as a callable:
```
-interesting = set(dir()) - set(dir(object))
+interesting = [](('__class__', '__contains__', '__doc__', ...))
```

### 8. KWARG_ORDER (22%)
Keyword arguments fully reversed in function calls:
```
-printer = PrettyPrinter(stream=stream, indent=indent, width=width, depth=depth, ...)
+printer = PrettyPrinter(underscore_numbers=underscore_numbers, sort_dicts=sort_dicts, ..., stream=stream)
```
Also seen in `partial()`, `subprocess.run()` calls.

### 9. CALL_EXPR_FRAGMENT (10%)
String literals used as callables:
```
-raise TypeError("invalid enum member name(s) %s" % ', '.join(...))
+raise 'invalid enum member name(s) %s'(','.join % ','(<genexpr>()))
```

### 10. DOCSTRING_FORMAT (10%)
```
-"""Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""
+__doc__ = "Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."
```

### 11. DEFAULT_PARAMS_LOST (6%)
```
-def __get__(self, obj, objtype=None):
+def __get__(self, obj, objtype):
```

### 12. VARIABLE_NAME (3%)
```
-key = result(args, kwds, .cell)
+key = oldkey(args, kwds, .cell)
```
`.cell` used as a variable reference instead of a proper variable name.

## Observations

1. **All 31 files** show HEADER category (copyright → decompiled tag) — this is universal.
2. **BLANK_LINES and IMPORT_FORMAT** are the most prevalent formatting issues (87% and 81%) and are purely cosmetic.
3. **SEMANTIC_ERROR is over-counted** for try/except cases — "lost try" blocks overlap with TRY_EXCEPT_MISSING category. The true semantic error (e.g., lost else branches, simplified boolean logic) affects ~30% of files functionally.
4. **FUNC_CALL_SYNTAX** (35%) is the most serious functional bug — `[new_func](**self.keywords)` produces different runtime behavior than the original `partial(new_func, *self.args, **self.keywords)`.
5. **KWARG_ORDER** (22%) is cosmetic but affects readability — reversed keyword arguments in constructor calls.
6. **DEFAULT_PARAMS_LOST** (6%) is rare but semantically meaningful — function signature loses parameter defaults.
7. **VARIABLE_NAME** with `.cell` (3%) is the most severe naming issue — decompiler uses internal `.cell` references instead of proper local variable names.
