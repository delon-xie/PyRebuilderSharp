# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    break
try:
    import ast
    expected_ast = ast.dump(ast.parse(expected_src), indent=2)
except:
    break
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
                                    exp_lines = expected_ast.split("""
""")
                                    act_lines = actual_ast.split("""
""")
                                    range(max(len(exp_lines), len(act_lines)))
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
                                                                    e != a
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
                                        if not True:
                                            pass
                                        else:
                                            print(f"  Line {i}: expected={e}")
                                            print(f"           actual=  {a}")
                                            break
                                            for ver in versions:
                                                pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
                                                if not os.path.exists(pyc):
                                                    print(f"⏭ {ver}: .pyc not found")
                                                else:
                                                    r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
                                                    actual_src = r.stdout
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
    print(f"❌ {ver}: AST parse failed - {e}")
    print(f"  Decompiled: {actual_src[None:200]}")
except:
    e = None
"""Run AST comparison for test_expr_basic across all versions"""
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
open(INPUT_FILE)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
versions
[]
break
raise
raise
def <genexpr>(.0):
    try:
        .0
        for (r, v) in .0:
            try:
                try:
                    .0
                except:
                    pass
                r
            except:
                pass
            if not True:
                pass
            else:
                1
        break
    except:
        pass
