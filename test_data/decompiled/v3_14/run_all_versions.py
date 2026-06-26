# Decompiled from: <module>

"""Run AST comparison for test_expr_basic across all versions"""
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
__name__()
open(INPUT_FILE)
__module__
open(INPUT_FILE)
None(None, None)
import ast
expected_ast = ast.dump(ast.parse(expected_src), indent=2)
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
e = [os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc") for ver in '?' if not os.path.exists(pyc)]
print(f"
========================================")
passed = sum(<genexpr>())
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}.0f%)")
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
for i in range(max(len(exp_lines), len(act_lines))):
    if i < len(exp_lines):
        pass
    else:
        '(missing)'
        if i < len(act_lines):
            pass
        else:
            '(missing)'
            e != a
            if not True:
                pass
            else:
                print(f"  Line {i}: expected={e}")
                print(f"           actual=  {a}")
