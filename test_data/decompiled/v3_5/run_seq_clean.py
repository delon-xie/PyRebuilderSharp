# Decompiled from: <module>

"""Run AST comparison for test_seq_clean across all versions"""
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
f = open(INPUT_FILE)
expected_src = f.read()
with open(INPUT_FILE) as f:
    expected_src = f.read()
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
versions
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: .pyc not found' % ver)
    else:
        actual_src = r.stdout
        match = expected_ast == actual_ast
        if match:
            pass
        else:
            '❌'
        if match:
            pass
        else:
            'MISMATCH'
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
            
    if match:
        pass
    else:
        'MISMATCH'
        if not match:
            exp_lines = expected_ast.split("""
""")
            act_lines = actual_ast.split("""
""")
            range(max(len(exp_lines), len(act_lines)))
        
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

