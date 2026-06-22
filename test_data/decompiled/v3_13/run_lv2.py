# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    break
try:
    actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
    ok = expected_ast == actual_ast
    try:
        try:
            actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
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
                                                    r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
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
break
raise
ex = None
