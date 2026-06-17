# Decompiled from: <module>

import ast
import subprocess
import os
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
pyc = os.path.join(COMPILED_DIR, 'test_expr_basic.2.7.pyc')
r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
lines = r.stdout.split("""
""")
for (i, line) in enumerate(lines):
    if not 'items[' in line:
        pass
    else:
        print(f"Line {i}: {line}")
break
# [SUMMARY] 6 blocks · 7 processed · 0 orphan · 106 instr
