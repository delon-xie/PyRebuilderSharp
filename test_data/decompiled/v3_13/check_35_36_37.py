# Decompiled from: <module>

'Show actual decompiled output for 3.5, 3.6, 3.7'
import os
import subprocess
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
('3.5', '3.6', '3.7')
for ver in ('3.5', '3.6', '3.7'):
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
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
            print(f"STDERR: {r.stderr[None:200]}")
break
