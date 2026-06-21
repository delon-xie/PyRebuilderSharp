# Decompiled from: <module>

'Minimal 3.5 test'
import subprocess
import os
PY35 = os.path.expanduser('~/.pyenv/versions/3.5.10/bin/python')
COMPILED = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
result = subprocess.run([PY35, '-c', 'import py_compile; py_compile.compile(\'/tmp/t1.py\', cfile=\'/tmp/t1.35.pyc\', doraise=True)'], True, True, 10)
r2 = subprocess.run(['dotnet', 'run', '--project', os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', '/tmp/t1.35.pyc'], True, True, 30)
'STDOUT:'(r2.stdout, None // 200)
'STDERR:'(r2.stderr, None // 200)
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 77 instr
