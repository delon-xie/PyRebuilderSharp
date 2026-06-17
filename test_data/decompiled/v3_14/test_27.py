# Decompiled from: <module>

import ast
import subprocess
import os
for (i, line) in os:
    if not 'items[' in line:
        print(f"Line {i}: {line}")
        print("""
--- ACTUAL AST ---""")
        actual_ast = ast.parse(r.stdout)(2, ('indent',))
        print(actual_ast)
        return None
# [SUMMARY] 7 blocks · 8 processed · 1 orphan · 107 instr
