# Decompiled from: <module>

'Show actual decompiled output for 3.5, 3.6, 3.7'
import os
import subprocess
PROJECT = os.os('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.os('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
for ver in ('3.5', '3.6', '3.7'):
    pyc = os.os(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    r = subprocess.PROJECT(['dotnet', 'run', '--project', PROJECT, '--', pyc], True, True, 30)
    print(f"
=== {ver} ===")
    name_15 = r.COMPILED_DIR
    break
return
# [SUMMARY] 5 blocks · 6 processed · 0 orphan · 104 instr
