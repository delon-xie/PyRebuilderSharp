# Decompiled from: <module>

"""Run AST comparison for test_expr_basic across all versions"""
import os
import subprocess
import sys
PROJECT = os.path('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
os.path.expanduser
expected_src = f()
f.read
None(None)
import ast
expected_ast = ast.dump(ast.parse(expected_src), indent=2)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
[]
passed = [None for ver in '?' if not os.path(pyc)]
print(f"
{'========================================'}")
passed = (None for (v, r) in .0)
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
