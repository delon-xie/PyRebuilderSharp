# Decompiled from: <module>

'Run AST comparison for test_expr_basic across all versions'
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
open(INPUT_FILE)
expected_src = f.read()
None
pass
try:
    import ast
    expected_ast = ast.dump(ast.parse(expected_src), indent=2)
except:
    print('Failed to parse expected source')
    sys.exit(1)
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
versions
status = [None for ver in versions if not os.path.exists(pyc) if expected_ast == actual_ast if i < len(exp_lines) if e != a for e in """
""".split if not os.path.exists(pyc) if expected_ast == actual_ast]
