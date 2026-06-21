# Decompiled from: <module>

import ast
import subprocess
import os
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
pyc = os.path.join(COMPILED_DIR, 'test_expr_basic.2.7.pyc')
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], True, True, 30)
lines = r.stdout.split("""
""")
enumerate(lines)
for (i, line) in enumerate(lines):
    if not 'items[' in line:
        pass
    else:
        print(f"Line {i}: {line}")
print("""
--- ACTUAL AST ---""")
actual_ast = ast.dump(ast.parse(r.stdout), 2)
print(actual_ast)
# [WARN] 2 instructions not decompiled
#   @0x0150: JUMP_BACKWARD arg=22
#   @0x016E: JUMP_BACKWARD arg=52
# [SUMMARY] 6 blocks · 7 processed · 0 orphan · 105 instr
