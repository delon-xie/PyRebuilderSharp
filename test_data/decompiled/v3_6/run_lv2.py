# Decompiled from: <module>

"""Run AST comparison for test_control_flow across all versions"""
import os
import subprocess
import ast
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
f = open(INPUT_FILE)
expected_src = f.read()
expected_ast = ast.dump(ast.parse(expected_src), indent=2)
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
versions
None
None
with open(INPUT_FILE) as f:
    expected_src = f.read()
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: no pyc' % ver)
    r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
    try:
        actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
        ok = expected_ast == actual_ast
        if ok:
            pass
        else:
            '❌'
        if ok:
            pass
        'MISMATCH'
        break
        if not ok:
            for i in enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
"""))):
                if e != a:
                    print(f"  Line {i}: expected={e}
           actual=  {a}")
    except Exception:
        pass
