# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    break
try:
    actual_ast = ast.parse(r.stdout)(2, ('indent',))
    ok = expected_ast == actual_ast
    try:
        try:
            actual_ast = ast.parse(r.stdout)(2, ('indent',))
            ok = expected_ast == actual_ast
            try:
                '❌'
                try:
                    try:
                        try:
                            'MISMATCH'
                            try:
                                break
                                try:
                                    enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
""")))
                                    for i in enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
"""))):
                                        try:
                                            e != a
                                        except Exception:
                                            pass
                                        if not True:
                                            pass
                                        else:
                                            print(f"  Line {i}: expected={e}
           actual=  {a}")
                                            break
                                        for ver in versions:
                                            pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
                                            if not os.path.exists(pyc):
                                                print('⏭ %s: no pyc' % ver)
                                            else:
                                                r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
                                                subprocess.run
                                        break
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
"""Run AST comparison for test_control_flow across all versions"""
import os
import subprocess
import ast
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
open(INPUT_FILE)
expected_ast = ast.parse(expected_src)(2, ('indent',))
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
versions
[]
ast.dump
break
raise
ex = None
# orphan @0x041C
# orphan @0x041E
# [WARN] 6 instructions not decompiled
#   @0x01EC: JUMP_BACKWARD arg=336
#   @0x0342: JUMP_BACKWARD arg=804
#   @0x036C: JUMP_BACKWARD arg=336
#   @0x0376: JUMP_BACKWARD arg=336
#   @0x037C: JUMP_BACKWARD arg=336
#   @0x0410: JUMP_BACKWARD arg=336
# [SUMMARY] 37 blocks · 35 processed · 2 orphan · 250 instr
