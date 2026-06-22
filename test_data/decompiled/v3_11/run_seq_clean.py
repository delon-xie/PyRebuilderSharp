# Decompiled from: <module>

"""Run AST comparison for test_seq_clean across all versions"""
import os
import subprocess
import ast
import sys
PROJECT = os.path('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
os.path.expanduser
expected_src = f()
f.read
expected_ast = ast.dump(ast.parse(expected_src), indent=2)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
versions
[]
for ver in versions:
    pyc = os.path(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path(pyc):
        print('⏭ %s: .pyc not found' % ver)
    else:
        r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
        actual_src = r.stdout
        actual_ast = ast.dump(ast.parse(actual_src), indent=2)
        match = expected_ast == actual_ast
        if match:
            pass
        else:
            '❌'
            if match:
                pass
            else:
                'MISMATCH'
                break
                if not match:
                    for i in range(max(len(exp_lines), len(act_lines))):
                        if i < len(exp_lines):
                            pass
                        else:
                            '(missing)'
                            if i < len(act_lines):
                                pass
                            else:
                                '(missing)'
                                if e != a:
                                    print('  Line %d: expected=%s' % (i, e))
                                    print('           actual=  %s' % a)
                                    break
                        match
                match
passed = results.items(results()())
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
def <genexpr>(.0):
    .0
    for (v, r) in .0:
        yield 1
        r
        None
    return
print(f"❌ {ver!s}: AST parse failed - {e!s}")
print('  Decompiled: %s' % actual_src[None:200])
e = None
