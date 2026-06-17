# Decompiled from: <module>

import ast
import subprocess
import os
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
pyc = os.path.join(COMPILED_DIR, 'test_expr_basic.2.7.pyc')
r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
for (i, line) in r.stdout:
    if not 'items[' in line:
        print(f"Line {i}: {line}")
        break
# [SUMMARY] 7 blocks · 8 processed · 1 orphan · 106 instr
