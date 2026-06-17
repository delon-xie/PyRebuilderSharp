# Decompiled from: <module>

# orphan @0x008A
pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
print(f"
=== {ver} ===")
# orphan @0x0000
__doc__ = 'Show actual decompiled output for 3.5, 3.6, 3.7'
import os
import subprocess
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
# orphan @0x013C
r.stdout[None:500]('(empty)')
# orphan @0x0188
print(f"STDERR: {r.stderr[None:200]}")
return None
# [SUMMARY] 10 blocks · 7 processed · 9 orphan · 99 instr
