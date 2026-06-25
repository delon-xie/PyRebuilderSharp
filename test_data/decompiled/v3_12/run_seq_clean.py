# Decompiled from: <module>

try:
    expected_ast = ast.dump(ast.parse(expected_src), indent=2)
except Exception:
    pass
"""Run AST comparison for test_seq_clean across all versions"""
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
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
                f""
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
                                if not e != a:
                                    pass
                                else:
                                    print('  Line %d: expected=%s' % (i, e))
                                    print('           actual=  %s' % a)
passed = sum(<genexpr>())
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
