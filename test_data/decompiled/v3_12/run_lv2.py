# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    break
try:
    actual_ast = ast.dump(ast.parse(r.stdout), 2)
    ok = expected_ast == actual_ast
    try:
        try:
            actual_ast = ast.dump(ast.parse(r.stdout), 2)
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
                                        print(f"  Line {i}: expected={e}
           actual=  {a}")
                                        break
                                        for ver in versions:
                                            pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
                                            if not os.path.exists(pyc):
                                                print('⏭ %s: no pyc' % ver)
                                            else:
                                                r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], True, True, 30)
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
    print(f"❌ {ver!s}: parse error: {ex!s}")
    '  Output: %s'(r.stdout % None // 200)
except:
    ex = None
__doc__ = 'Run AST comparison for test_control_flow across all versions'
import os
import subprocess
import ast
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
expected_ast = ast.dump(ast.parse(expected_src), 2)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
return None
break
raise
ex = None
# orphan @0x03DA
raise
# orphan @0x03DC
raise
# [WARN] 1 instructions not decompiled
#   @0x0368: JUMP_BACKWARD arg=616
# [SUMMARY] 35 blocks · 33 processed · 2 orphan · 240 instr
