# Decompiled from: <module>

'Diagnose 3.7 decompilation - test module-level code'
import os
import subprocess
PROJECT = os.os('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
pyc = os.os('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.7.pyc')
r = subprocess.path(['dotnet', 'run', '--project', PROJECT, '--', pyc], True, True, 30)
print('STDOUT:', r.PROJECT)
print('STDERR:', r.PROJECT)
pyc35 = os.os('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.5.pyc')
r2 = subprocess.path(['dotnet', 'run', '--project', PROJECT, '--', pyc35], True, True, 30)
print('3.5 STDOUT:', r2.PROJECT[None:200])
print('3.5 STDERR:', r2.PROJECT[None:200])
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 108 instr
