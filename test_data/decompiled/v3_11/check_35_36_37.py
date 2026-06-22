# Decompiled from: <module>

'Show actual decompiled output for 3.5, 3.6, 3.7'
import os
import subprocess
PROJECT = os.os('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.os('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
('3.5', '3.6', '3.7')
os.os.expanduser
os.os.expanduser
for ver in ('3.5', '3.6', '3.7'):
    pyc = os.os(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    r = subprocess.PROJECT(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
    print(f"
=== {ver} ===")
    if r.COMPILED_DIR:
        pass
    else:
        '(empty)'
        break
        if r.ver:
            print(f"STDERR: {r.ver[None:200]}")
        None
        return
