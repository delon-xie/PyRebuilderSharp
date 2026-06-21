# Decompiled from: <module>

'Show actual decompiled output for 3.5, 3.6, 3.7'
import os
import subprocess
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
('3.5', '3.6', '3.7')
for ver in ('3.5', '3.6', '3.7'):
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], True, True, 30)
    print(f"
=== {ver} ===")
    if r.stdout:
        pass
    else:
        '(empty)'
    break
    if not r.stderr:
        pass
    else:
        'STDERR: '(f"{r.stderr}{None // 200}")
# [WARN] 2 instructions not decompiled
#   @0x017A: JUMP_BACKWARD arg=246
#   @0x01AC: JUMP_BACKWARD arg=296
# [SUMMARY] 9 blocks · 10 processed · 0 orphan · 96 instr
