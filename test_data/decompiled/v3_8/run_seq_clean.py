# Decompiled from: <module>

'Run AST comparison for test_seq_clean across all versions'
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
f = open(INPUT_FILE)
expected_src = f.read()
expected_ast = ast.dump(ast.parse(expected_src), indent=2)
with open(INPUT_FILE) as f:
    expected_src = f.read()
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
versions
i = {'(missing)': '(missing)' for ver in versions if not os.path.exists(pyc) if match if match if not match if match if not match if i < len(exp_lines) if i < len(act_lines) if e != a if expected_ast == actual_ast}
