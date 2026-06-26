# Decompiled from: <module>

"""Run AST comparison for test_seq_clean across all versions"""
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
__name__()
open(INPUT_FILE)
__module__
open(INPUT_FILE)
expected_src = f.read()
None(None, None)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
[]
e = [os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver) for ver in versions if not os.path.exists(pyc)]
passed = sum(<genexpr>())
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
for i in range(max(len(exp_lines), len(act_lines))):
    if i < len(exp_lines):
        pass
    else:
        '(missing)'
        if i < len(act_lines):
            pass
        else:
            '(missing)'
            e != a
            if not True:
                pass
            else:
                print('  Line %d: expected=%s' % (i, e))
                print('           actual=  %s' % a)
