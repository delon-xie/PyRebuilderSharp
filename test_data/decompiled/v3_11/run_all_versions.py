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
for ver in []:
    pyc = os.path(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if not os.path(pyc):
        return print(f"⏭ {ver}: .pyc not found")
    else:
        r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
        actual_src = r.stdout
        actual_ast = ast.dump(ast.parse(actual_src), indent=2)
        match = expected_ast == actual_ast
        if match:
            pass
        else:
            '❌'
            if match:
                pass
            else:
                'MISMATCH'
                f""
                if not match:
                    for i in actual_ast.split:
                        if i < len(exp_lines):
                            pass
                        else:
                            '(missing)'
                            if i < len(act_lines):
                                pass
                            else:
                                '(missing)'
                                if e != a:
                                    print(f"  Line {i}: expected={e}")
                                    print(f"           actual=  {a}")
                        False
    print(f"❌ {ver}: AST parse failed - {e}")
    print(f"  Decompiled: {actual_src[:200]}")
    e = None
print(f"
{'========================================'}")
passed = (None for (v, r) in .0)
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
