# Decompiled from: <module>

'Run AST comparison for test_control_flow across all versions'
import os
import subprocess
import ast
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
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
            for i in e != a:
                if e != a:
                    print(f"  Line {i}: expected={e}
           actual=  {a}")
    except Exception:
        pass
return None
# orphan @0x0172
# orphan @0x0174
# orphan @0x0178
# orphan @0x0182
print('❌ %s: parse error: %s' % (ver, ex))
print('  Output: %s' % r.stdout[None:200])
None
# orphan @0x01B4
ex = None
# orphan @0x01C0
# [SUMMARY] 22 blocks · 17 processed · 6 orphan · 221 instr
