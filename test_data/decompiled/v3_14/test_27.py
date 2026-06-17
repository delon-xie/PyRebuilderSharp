# Decompiled from: <module>

import ast
import subprocess
import os
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
pyc = os.path.join(COMPILED_DIR, 'test_expr_basic.2.7.pyc')
for (i, line) in subprocess.run:
    if not 'items[' in line:
        print(f"Line {i}: {line}")
        print("""
--- ACTUAL AST ---""")
        actual_ast = ast.parse(r.stdout)(2, ('indent',))
        print(actual_ast)
        return None
# [SUMMARY] 7 blocks · 8 processed · 1 orphan · 107 instr
