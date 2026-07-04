# Decompiled from: <module>

"""Run AST comparison for test_expr_basic across all versions"""
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
f = open(INPUT_FILE)
expected_src = f.read()
import ast
expected_ast = ast.dump(ast.parse(expected_src), indent=2)
with open(INPUT_FILE) as f:
    expected_src = f.read()
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
versions
print(f"\n{'========================================'}")
passed = sum((<genexpr>)(results.items()))
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
if not os.path.exists(pyc):
    print(f"⏭ {ver}: .pyc not found")
for i in range(max(len(exp_lines), len(act_lines))):
    if i < len(exp_lines):
        pass
    '(missing)'
    if i < len(act_lines):
        pass
    '(missing)'
    if e != a:
        print(f"  Line {i}: expected={e}")
        print(f"           actual=  {a}")
print(f"  Line {i}: expected={e}")
print(f"           actual=  {a}")
