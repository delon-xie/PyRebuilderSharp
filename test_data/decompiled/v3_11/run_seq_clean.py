# Decompiled from: <module>

pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
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
try:
    expected_ast = ast.dump(ast.parse(expected_src), indent=2)
print('Failed to parse expected source:', e)
sys.exit(1)
if not True:
    pass
raise
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
f""
print('  Line %d: expected=%s' % (i, e))
print('           actual=  %s' % a)
