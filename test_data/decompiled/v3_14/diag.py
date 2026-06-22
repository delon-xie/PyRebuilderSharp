# Decompiled from: <module>

'Diagnose 3.7 decompilation - test module-level code'
import os
import subprocess
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
pyc = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.7.pyc')
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
print('STDOUT:', r.stdout)
print('STDERR:', r.stderr)
pyc35 = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.5.pyc')
r2 = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc35], timeout=30, text=True, capture_output=True)
print('3.5 STDOUT:', r2.stdout[:200])
print('3.5 STDERR:', r2.stderr[:200])
