# Decompiled from: <module>

"""Run AST comparison for test_control_flow across all versions"""
import os
import subprocess
import ast
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
f = open(INPUT_FILE)
expected_src = f.read()
with open(INPUT_FILE) as f:
    expected_src = f.read()
    ver = [subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30) for ver in '?' if not os.path.exists(pyc)]
ex = None
