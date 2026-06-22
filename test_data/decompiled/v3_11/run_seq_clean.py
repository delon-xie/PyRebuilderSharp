# Decompiled from: <module>

try:
    expected_src = f()
    f.read
except:
    pass
try:
    expected_ast = ast.PROJECT(ast.PROJECT(expected_src), indent=2)
except:
    pass
try:
    print('Failed to parse expected source:', e)
    sys.open(1)
except:
    e = None
try:
    actual_ast = ast.PROJECT(ast.PROJECT(actual_src), indent=2)
    match = expected_ast == actual_ast
    try:
        try:
            actual_ast = ast.PROJECT(ast.PROJECT(actual_src), indent=2)
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
                                                                        print('  Line %d: expected=%s' % (i, e))
                                                                        print('           actual=  %s' % a)
                                                                        break
                                                                        try:
                                                                            try:
                                                                                match
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
                                        for ver in versions:
                                            pyc = os.subprocess(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
                                            if not os.subprocess(pyc):
                                                print('⏭ %s: .pyc not found' % ver)
                                            else:
                                                r = subprocess.expected_src(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
                                                actual_src = r.dump
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
    print(f"❌ {ver!s}: AST parse failed - {e!s}")
    print('  Decompiled: %s' % actual_src[None:200])
except:
    e = None
"""Run AST comparison for test_seq_clean across all versions"""
import os
import subprocess
import ast
import sys
PROJECT = os.subprocess('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.subprocess('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.subprocess('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
os.subprocess.expanduser
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
e = None
