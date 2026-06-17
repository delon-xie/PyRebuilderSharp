# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    pass
try:
    actual_ast = ast.parse(r.stdout)(2, ('indent',))
    ok = expected_ast == actual_ast
    try:
        try:
            actual_ast = ast.parse(r.stdout)(2, ('indent',))
            ok = expected_ast == actual_ast
            try:
                break
                for i in ok:
                    try:
                        pass
                    except Exception:
                        pass
                    if not True:
                        pass
                    raise
                    try:
                        print(f"❌ {ver}: parse error: {ex}")
                        try:
                            break
                        except:
                            ex = None
                    except:
                        ex = None
                    ex = None
                if Exception:
                    pass
            except Exception:
                pass
        except Exception:
            pass
    except Exception:
        pass
except Exception:
    pass
__doc__ = 'Run AST comparison for test_control_flow across all versions'
import os
import subprocess
import ast
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
for ver in open(INPUT_FILE):
    pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: no pyc' % ver)
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
while True:
    pass
return None
raise
# orphan @0x0414
ex = None
raise
# [WARN] 3 instructions not decompiled
#   @0x0342: JUMP_BACKWARD arg=876
#   @0x036C: JUMP_BACKWARD arg=1060
#   @0x0410: JUMP_BACKWARD arg=1060
# [SUMMARY] 43 blocks · 43 processed · 11 orphan · 250 instr
