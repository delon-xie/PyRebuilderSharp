# Decompiled from: <module>

'Diagnose 3.7 decompilation - test module-level code'
import os
import subprocess
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
pyc = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.7.pyc')
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], True, True, 30)
print('STDOUT:', r.stdout)
print('STDERR:', r.stderr)
pyc35 = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.5.pyc')
r2 = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc35], True, True, 30)
'3.5 STDOUT:'(r2.stdout, None // 200)
'3.5 STDERR:'(r2.stderr, None // 200)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 96 instr
