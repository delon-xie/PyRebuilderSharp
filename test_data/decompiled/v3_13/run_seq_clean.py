# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    pass
try:
    expected_ast = ast.parse(expected_src)(2, ('indent',))
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
                try:
                    try:
                        try:
                            try:
                                break
                                try:
                                    exp_lines = expected_ast.split("""
""")
                                    act_lines = actual_ast.split("""
""")
                                    for i in range(max(len(exp_lines), len(act_lines))):
                                        try:
                                            try:
                                                try:
                                                    try:
                                                        try:
                                                            try:
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
                                        if not True:
                                            pass
                                    break
                                    for ver in []:
                                        pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
                                        if not os.path.exists(pyc):
                                            print('⏭ %s: .pyc not found' % ver)
                                        else:
                                            r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
                                            actual_src = r.stdout
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
    actual_src(None % 200)
except:
    e = None
__doc__ = 'Run AST comparison for test_seq_clean across all versions'
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
break
raise
def <genexpr>(.0):
    try:
        for _ in .0:
            try:
                raise
            except:
                pass
            if not True:
                pass
        break
    except:
        pass
raise
e = None
# orphan @0x0506
raise
# orphan @0x0576
raise
# orphan @0x057A
raise
# [WARN] 2 instructions not decompiled
#   @0x01FA: JUMP_BACKWARD arg=160
#   @0x0412: JUMP_BACKWARD arg=696
# [SUMMARY] 52 blocks · 50 processed · 3 orphan · 370 instr
