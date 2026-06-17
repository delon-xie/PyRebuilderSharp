# Decompiled from: <module>

'Minimal 3.5 test'
import subprocess
import os
PY35 = os.path.expanduser('~/.pyenv/versions/3.5.10/bin/python')
COMPILED = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
result = [PY35, '-c', 'import py_compile; py_compile.compile(\'/tmp/t1.py\', cfile=\'/tmp/t1.35.pyc\', doraise=True)'](True, True, 10, ('capture_output', 'text', 'timeout'))
r2 = ['dotnet', 'run', '--project', os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', '/tmp/t1.35.pyc'](True, True, 30, ('capture_output', 'text', 'timeout'))
r2.stdout(None, 200)
r2.stderr(None, 200)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 77 instr
