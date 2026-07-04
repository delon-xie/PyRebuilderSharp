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
expected_ast = ast.dump(ast.parse(expected_src), indent=2)
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
versions
passed = [os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver) for ver in versions if not os.path.exists(pyc) if expected_ast == actual_ast if i < len(exp_lines) for i in """
""".split if not os.path.exists(pyc) if i < len(exp_lines) if expected_ast == actual_ast]
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
f""
