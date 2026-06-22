# Decompiled from: <module>

import ast
import subprocess
import os
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
pyc = os.path.join(COMPILED_DIR, 'test_expr_basic.2.7.pyc')
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
lines = r.stdout.split("""
""")
enumerate(lines)
for (i, line) in enumerate(lines):
    if 'items[' in line:
        print(f"Line {i}: {line}")
print("""
--- ACTUAL AST ---""")
actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
print(actual_ast)
# [SUMMARY] 5 blocks · 6 processed · 0 orphan · 96 instr
