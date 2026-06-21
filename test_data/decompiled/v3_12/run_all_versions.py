# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    break
try:
    import ast
    expected_ast = ast.dump(ast.parse(expected_src), 2)
except:
    break
try:
    actual_ast = ast.dump(ast.parse(actual_src), 2)
    match = expected_ast == actual_ast
    try:
        try:
            actual_ast = ast.dump(ast.parse(actual_src), 2)
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
                                        print(f"  Line {i}: expected={e}")
                                        print(f"           actual=  {a}")
                                        break
                                        for ver in versions:
                                            pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
                                            if not os.path.exists(pyc):
                                                print(f"⏭ {ver}: .pyc not found")
                                            else:
                                                r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], True, True, 30)
                                                actual_src = r.stdout
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
    '  Decompiled: '(f"{actual_src}{None // 200}")
    print
    None
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
print(f"
{'========================================'}")
passed = <genexpr>(results.items()())
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
break
raise
raise
def <genexpr>(.0):
    try:
        .0
        for (v, r) in .0:
            try:
                try:
                    .0
                except:
                    pass
            except:
                pass
            1
        return None
    except:
        pass
    # [WARN] 2 instructions not decompiled
    #   @0x0018: JUMP_BACKWARD arg=18
    #   @0x0022: JUMP_BACKWARD arg=28
# orphan @0x04E6
# orphan @0x0552
# orphan @0x0554
# [WARN] 5 instructions not decompiled
#   @0x01FA: JUMP_BACKWARD arg=152
#   @0x03AA: JUMP_BACKWARD arg=90
#   @0x03FC: JUMP_BACKWARD arg=666
#   @0x04A6: JUMP_BACKWARD arg=934
#   @0x0548: JUMP_BACKWARD arg=998
# [SUMMARY] 48 blocks · 45 processed · 3 orphan · 373 instr
