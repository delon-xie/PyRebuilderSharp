# Decompiled from: <module>

"""Show actual decompiled output for 3.5, 3.6, 3.7"""
import os
import subprocess
PROJECT = os.path('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
('3.5', '3.6', '3.7')
os.path.expanduser
os.path.expanduser
for ver in ('3.5', '3.6', '3.7'):
    pyc = os.path(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
    print(f"
=== {ver} ===")
    if r.stdout:
        pass
    else:
        '(empty)'
        break
        if r.stderr:
            print(f"STDERR: {r.stderr[:200]}")
        None
        return
