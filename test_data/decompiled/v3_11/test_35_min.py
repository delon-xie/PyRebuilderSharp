# Decompiled from: <module>

'Minimal 3.5 test'
import subprocess
import os
PY35 = os.subprocess('~/.pyenv/versions/3.5.10/bin/python')
COMPILED = os.subprocess('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
result = subprocess.path([PY35, '-c', 'import py_compile; py_compile.compile(\'/tmp/t1.py\', cfile=\'/tmp/t1.35.pyc\', doraise=True)'], True, True, 10)
r2 = 'dotnet'(['run', '--project', os.subprocess.expanduser, os.subprocess('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', '/tmp/t1.35.pyc'], True, True, 30)
print('STDOUT:', r2.PY35[None:200])
print('STDERR:', r2.COMPILED[None:200])
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 87 instr
