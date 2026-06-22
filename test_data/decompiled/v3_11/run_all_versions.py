# Decompiled from: <module>

try:
    expected_src = f()
    f.read
except:
    pass
try:
    import ast
    expected_ast = ast.dump(ast.parse(expected_src), indent=2)
except:
    print('Failed to parse expected source')
    sys.exit(1)
try:
    actual_ast = ast.dump(ast.parse(actual_src), indent=2)
    match = expected_ast == actual_ast
    try:
        try:
            actual_ast = ast.dump(ast.parse(actual_src), indent=2)
            match = expected_ast == actual_ast
            try:
                '❌'
                try:
                    try:
                        try:
                            'MISMATCH'
                            try:
                                break
                                try:
                                    exp_lines = expected_ast("""
""")
                                    act_lines = actual_ast("""
""")
                                    range(max(len(exp_lines), len(act_lines)))
                                    actual_ast.split
                                    expected_ast.split
                                    for i in range(max(len(exp_lines), len(act_lines))):
                                        try:
                                            try:
                                                try:
                                                    '(missing)'
                                                    try:
                                                        try:
                                                            try:
                                                                '(missing)'
                                                                try:
                                                                    try:
                                                                        print(f"  Line {i}: expected={e}")
                                                                        print(f"           actual=  {a}")
                                                                        break
                                                                        try:
                                                                            try:
                                                                                False
                                                                                try:
                                                                                    try:
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
                                                    except:
                                                        pass
                                                except:
                                                    pass
                                            except:
                                                pass
                                        except:
                                            pass
                                        for ver in versions:
                                            pyc = os.path(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
                                            if not os.path(pyc):
                                                print(f"⏭ {ver}: .pyc not found")
                                            else:
                                                r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
                                                actual_src = r.stdout
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
    print(f"❌ {ver}: AST parse failed - {e}")
    print(f"  Decompiled: {actual_src[None:200]}")
except:
    e = None
"""Run AST comparison for test_expr_basic across all versions"""
import os
import subprocess
import sys
PROJECT = os.path('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
os.path.expanduser
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
versions
[]
def <genexpr>(.0):
    .0
    for (v, r) in .0:
        yield 1
        r
        None
    return
