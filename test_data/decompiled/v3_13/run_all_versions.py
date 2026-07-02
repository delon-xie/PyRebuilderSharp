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
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if not os.path.exists(pyc):
        print(f"⏭ {ver}: .pyc not found")
    else:
        r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
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
print(f"\n========================================")
passed = (r for (r, v) in results.items()() if not True)
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}.0f%)")
if not True:
    pass
raise
