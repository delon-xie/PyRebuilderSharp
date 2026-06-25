# Decompiled from: <module>

"""Run AST comparison for test_control_flow across all versions"""
import os
import subprocess
import ast
PROJECT = os.path('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
os.path.expanduser
expected_src = f()
f.read
expected_ast = ast.dump(ast.parse(expected_src), indent=2)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
versions
[]
for ver in versions:
    pyc = os.path(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
    if not os.path(pyc):
        print('⏭ %s: no pyc' % ver)
    else:
        r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
        actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
        ok = expected_ast == actual_ast
        if ok:
            pass
        else:
            '❌'
            if ok:
                pass
            else:
                'MISMATCH'
                break
                if not ok:
                    for i in expected_ast.split(expected_ast("""
""")(actual_ast.split, actual_ast("""
"""))):
                        if e != a:
                            print(f"  Line {i}: expected={e}
           actual=  {a}")
                            break
return
print(f"❌ {ver!s}: parse error: {ex!s}")
print('  Output: %s' % r.stdout[:200])
ex = None
