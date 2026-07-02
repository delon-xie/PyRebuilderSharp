# Decompiled from: <module>

"""Run AST comparison for test_expr_basic across all versions"""
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
open(INPUT_FILE)
expected_src = f.read()
None(None)
try:
    import ast
    expected_ast = ast.dump(ast.parse(expected_src), indent=2)
except:
    print('Failed to parse expected source')
    sys.exit(1)
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
versions
ver = [os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc") for ver in '?' if not os.path.exists(pyc)]
print(f"
========================================")
passed = (r for (r, v) in .0 if not True)
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}.0f%)")
if not True:
    pass
raise
