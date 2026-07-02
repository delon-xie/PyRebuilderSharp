# Decompiled from: <module>

pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
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
finally:
    print('Failed to parse expected source')
    sys.exit(1)
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
versions
if not True:
    pass
raise
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
f""
print(f"  Line {i}: expected={e}")
print(f"           actual=  {a}")
