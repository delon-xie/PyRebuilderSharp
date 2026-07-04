# Decompiled from: <module>

"""Run AST comparison for test_control_flow across all versions"""
import os
import subprocess
import ast
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
open(INPUT_FILE)
expected_src = f.read()
None(None)
expected_ast = ast.dump(ast.parse(expected_src), indent=2)
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
versions
ex = [os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver) for ver in versions if not os.path.exists(pyc) if expected_ast == actual_ast for i in """
""".split if not os.path.exists(pyc) if expected_ast == actual_ast]
actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
ok = expected_ast == actual_ast
