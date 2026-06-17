# Decompiled from: <module>

# orphan @0x0000
import ast
import subprocess
import os
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
pyc = os.path.join(COMPILED_DIR, 'test_expr_basic.2.7.pyc')
r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
lines = r.stdout.split("""
""")
# orphan @0x0140
# orphan @0x0154
print(f"Line {i}: {line}")
print("""
--- ACTUAL AST ---""")
actual_ast = ast.parse(r.stdout)(2, ('indent',))
print(actual_ast)
return None
# [SUMMARY] 7 blocks · 5 processed · 6 orphan · 108 instr
