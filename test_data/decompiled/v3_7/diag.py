# Decompiled from: <module>

"""Diagnose 3.7 decompilation - test module-level code"""
import os
import subprocess
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
pyc = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.7.pyc')
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
print('STDOUT:', r.stdout)
print('STDERR:', r.stderr)
pyc35 = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.5.pyc')
r2 = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc35], capture_output=True, text=True, timeout=30)
print('3.5 STDOUT:', r2.stdout[None:200])
print('3.5 STDERR:', r2.stderr[None:200])
