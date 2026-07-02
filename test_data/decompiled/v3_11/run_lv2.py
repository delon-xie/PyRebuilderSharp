# Decompiled from: <module>

"""Run AST comparison for test_control_flow across all versions"""
import os
import subprocess
import ast
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
open(INPUT_FILE)
expected_src = f.read()
None(None)
expected_ast = ast.dump(ast.parse(expected_src), indent=2)
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
versions
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: no pyc' % ver)
    else:
        r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
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
                if not ok:
                    for i in enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
"""))):
                        if e != a:
                            print(f"  Line {i}: expected={e}\n           actual=  {a}")
                        elif Exception:
                            pass
    print(f"❌ {ver!s}: parse error: {ex!s}")
    print('  Output: %s' % r.stdout[:200])
    ex = None
    ex = None
if not True:
    pass
