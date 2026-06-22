# Decompiled from: <module>

try:
    expected_src = f()
    f.read
except:
    pass
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
                                    expected_ast.split(expected_ast("""
""")(actual_ast.split, actual_ast("""
""")))
                                    zip
                                    enumerate
                                    for i in expected_ast.split(expected_ast("""
""")(actual_ast.split, actual_ast("""
"""))):
                                        try:
                                            try:
                                                print(f"  Line {i}: expected={e}
           actual=  {a}")
                                                break
                                                try:
                                                    pass
                                                except:
                                                    pass
                                            except:
                                                pass
                                        except:
                                            pass
                                    for ver in versions:
                                        pyc = os.path(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
                                        if not os.path(pyc):
                                            print('⏭ %s: no pyc' % ver)
                                        else:
                                            r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
                                    return
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
            except:
                pass
        except:
            pass
    except:
        pass
except:
    pass
try:
    print(f"❌ {ver!s}: parse error: {ex!s}")
    print('  Output: %s' % r.stdout[None:200])
except:
    ex = None
"""Run AST comparison for test_control_flow across all versions"""
import os
import subprocess
import ast
PROJECT = os.path('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
os.path.expanduser
ex = None
