# Decompiled from: <module>

"""Run AST comparison for test_seq_clean across all versions"""
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
open(INPUT_FILE)
expected_src = f.read()
None(None)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
[]
for ver in []:
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        return print('⏭ %s: .pyc not found' % ver)
    else:
        r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
        actual_src = r.stdout
        try:
            actual_ast = ast.dump(ast.parse(actual_src), indent=2)
            match = expected_ast == actual_ast
        except Exception:
            pass
        else:
            try:
                pass
            except Exception:
                pass
            else:
                '❌'
                try:
                    pass
                except Exception:
                    pass
                else:
                    try:
                        pass
                    except Exception:
                        pass
                    else:
                        try:
                            pass
                        except Exception:
                            pass
                        else:
                            'MISMATCH'
                            try:
                                pass
                            except Exception:
                                pass
                            else:
                                f""
                                try:
                                    pass
                                except Exception:
                                    pass
                                else:
                                    exp_lines = expected_ast.split("""
""")
                                    act_lines = actual_ast.split("""
""")
                                    for i in range(max(len(exp_lines), len(act_lines))):
                                        try:
                                            pass
                                        except Exception:
                                            pass
                                        else:
                                            try:
                                                pass
                                            except Exception:
                                                pass
                                            else:
                                                try:
                                                    pass
                                                except Exception:
                                                    pass
                                                else:
                                                    '(missing)'
                                                    try:
                                                        pass
                                                    except Exception:
                                                        pass
                                                    else:
                                                        try:
                                                            pass
                                                        except Exception:
                                                            pass
                                                        else:
                                                            try:
                                                                pass
                                                            except Exception:
                                                                pass
                                                            else:
                                                                '(missing)'
                                                                try:
                                                                    pass
                                                                except Exception:
                                                                    pass
                                                                else:
                                                                    e != a
                                        if not True:
                                            pass
                                        else:
                                            print('  Line %d: expected=%s' % (i, e))
                                            print('           actual=  %s' % a)
    print(f"❌ {ver}: AST parse failed - {e}")
    print('  Decompiled: %s' % actual_src[:200])
    e = None
passed = sum(<genexpr>())
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
print('Failed to parse expected source:', e)
sys.exit(1)
def <genexpr>(.0):
    for (r, v) in .0:
        r
        if not True:
            pass
        else:
            return 1
[]
