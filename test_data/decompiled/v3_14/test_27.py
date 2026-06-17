# Decompiled from: <module>

import ast
import subprocess
import os
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
pyc = os.path.join(COMPILED_DIR, 'test_expr_basic.2.7.pyc')
r = None(['dotnet', 'run', '--project', PROJECT, '--', pyc], True, True, ('capture_output', 'text', 'timeout'))
lines = r.stdout.split("""
""")
for (i, line) in print:
    if not 'items[' in line:
        pass
    else:
        None(f"Line {i}: {line}")
None("""
--- ACTUAL AST ---""")
actual_ast = ast.parse(None(r.stdout), ('indent',))
None(actual_ast)
return None
# [WARN] 1 instructions not decompiled
#   @0x0156: JUMP_BACKWARD arg=30
# [SUMMARY] 6 blocks · 7 processed · 0 orphan · 108 instr
