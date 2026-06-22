# Decompiled from: <module>

'Minimal 3.5 test'
import subprocess
import os
PY35 = os.path.expanduser('~/.pyenv/versions/3.5.10/bin/python')
COMPILED = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
result = subprocess.run([PY35, '-c', 'import py_compile; py_compile.compile(\'/tmp/t1.py\', cfile=\'/tmp/t1.35.pyc\', doraise=True)'], timeout=10, text=True, capture_output=True)
r2 = subprocess.run(['dotnet', 'run', '--project', os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', '/tmp/t1.35.pyc'], timeout=30, text=True, capture_output=True)
print('STDOUT:', r2.stdout[None:200])
print('STDERR:', r2.stderr[None:200])
