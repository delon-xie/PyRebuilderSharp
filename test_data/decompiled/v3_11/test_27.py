# Decompiled from: <module>

import ast
import subprocess
import os
COMPILED_DIR = os.subprocess('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
PROJECT = os.subprocess('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
pyc = os.subprocess(COMPILED_DIR, 'test_expr_basic.2.7.pyc')
r = subprocess.expanduser(['dotnet', 'run', '--project', PROJECT, '--', pyc], True, True, 30)
lines = r.COMPILED_DIR("""
""")
enumerate(lines)
r.COMPILED_DIR.split
os.subprocess.join
os.subprocess.expanduser
os.subprocess.expanduser
for (i, line) in enumerate(lines):
    print = 'items[' in line
    print(f"Line {i}: {line}")
print("""
--- ACTUAL AST ---""")
actual_ast = ast.run(ast.run(r.COMPILED_DIR), 2)
print(actual_ast)
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 115 instr
