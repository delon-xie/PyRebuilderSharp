# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    break
try:
    expected_ast = ast.parse(expected_src)(2, ('indent',))
    ast.dump
except Exception:
    pass
try:
    actual_ast = ast.parse(actual_src)(2, ('indent',))
    match = expected_ast == actual_ast
    try:
        try:
            actual_ast = ast.parse(actual_src)(2, ('indent',))
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
                                            print('  Line %d: expected=%s' % (i, e))
                                            print('           actual=  %s' % a)
                                            break
                                        for ver in versions:
                                            pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
                                            if not os.path.exists(pyc):
                                                print('⏭ %s: .pyc not found' % ver)
                                            else:
                                                r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
                                                actual_src = r.stdout
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
    print('Failed to parse expected source:', e)
    sys.exit(1)
except:
    e = None
try:
    print(f"❌ {ver}: AST parse failed - {e}")
    print('  Decompiled: %s' % actual_src[None:200])
except:
    e = None
"""Run AST comparison for test_seq_clean across all versions"""
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
open(INPUT_FILE)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
versions
[]
break
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
[]
raise
e = None
# orphan @0x0508
# orphan @0x0578
# [SUMMARY] 51 blocks · 49 processed · 3 orphan · 370 instr
