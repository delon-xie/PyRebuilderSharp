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
    raise
    for ver in versions:
        pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
        if not os.path.exists(pyc):
            print('⏭ %s: no pyc' % ver)
            continue
        Exception
        try:
            print('❌ %s: parse error: %s' % (ver, ex))
            print('  Output: %s' % r.stdout[None:200])
        finally:
            ex = None
            raise
            raise
            return None
        ex = None
        try:
            actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
            ok = expected_ast == actual_ast
            if ok:
                pass
            if ok:
                pass
            break
            if not ok:
                for i in enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
"""))):
                    if e != a:
                        print(f"  Line {i}: expected={e}
           actual=  {a}")
                        break
        except Exception:
            print('❌ %s: parse error: %s' % (ver, ex))
            print('  Output: %s' % r.stdout[None:200])
# orphan @0x016C
# orphan @0x032E
# [SUMMARY] 25 blocks · 24 processed · 2 orphan · 223 instr
