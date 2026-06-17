# Decompiled from: <module>

'Show actual decompiled output for 3.5, 3.6, 3.7'
import os
import subprocess
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
for ver in 'STDERR: ':
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
    print(f"
=== {ver} ===")
    if r.stdout:
        pass
    break
    if not r.stderr:
        pass
    else:
        r.stderr(f"{None}{200}")
break
# [WARN] 1 instructions not decompiled
#   @0x0188: JUMP_BACKWARD arg=262
# [SUMMARY] 9 blocks · 10 processed · 0 orphan · 99 instr
