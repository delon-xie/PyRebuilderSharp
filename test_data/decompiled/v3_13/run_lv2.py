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
                try:
                    try:
                        try:
                            try:
                                break
                                try:
                                    for i in enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
"""))):
                                        try:
                                            pass
                                        except Exception:
                                            pass
                                        if not True:
                                            pass
                                    break
                                    for ver in []:
                                        pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
                                        if not os.path.exists(pyc):
                                            print('⏭ %s: no pyc' % ver)
                                        else:
                                            r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
                                    break
                                except Exception:
                                    pass
                            except Exception:
                                pass
                        except Exception:
                            pass
                    except Exception:
                        pass
                except Exception:
                    pass
            except Exception:
                pass
        except Exception:
            pass
    except Exception:
        pass
except Exception:
    pass
try:
    print(f"❌ {ver}: parse error: {ex}")
    print('  Output: %s' % r.stdout[None:200])
except:
    ex = None
__doc__ = 'Run AST comparison for test_control_flow across all versions'
import os
import subprocess
import ast
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
expected_ast = ast.parse(expected_src)(2, ('indent',))
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
break
raise
ex = None
# orphan @0x041A
raise
# orphan @0x041E
raise
# [WARN] 4 instructions not decompiled
#   @0x01EC: JUMP_BACKWARD arg=160
#   @0x036C: JUMP_BACKWARD arg=544
#   @0x0376: JUMP_BACKWARD arg=554
#   @0x037C: JUMP_BACKWARD arg=560
# [SUMMARY] 37 blocks · 36 processed · 2 orphan · 250 instr
