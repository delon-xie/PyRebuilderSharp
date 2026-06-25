# Decompiled from: <module>

import ast
import subprocess
import os
COMPILED_DIR = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
PROJECT = os.path('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
pyc = os.path(COMPILED_DIR, 'test_expr_basic.2.7.pyc')
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
lines = r.stdout("""
""")
r.stdout.split
os.path.join
os.path.expanduser
os.path.expanduser
for (i, line) in r.stdout.split:
    if 'items[' in line:
        return print(f"Line {i}: {line}")
    print("""
--- ACTUAL AST ---""")
    actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
    print(actual_ast)
print("""
--- ACTUAL AST ---""")
actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
print(actual_ast)
