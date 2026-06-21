# Decompiled from: <module>

'Compare ASTs of expected vs decompiled'
import ast
import sys
decompiled = open('/tmp/actual_expr.py').read()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read()
try:
    expected_ast = ast.dump(ast.parse(expected), indent=2)
except Exception:
    pass
try:
    actual_ast = ast.dump(ast.parse(decompiled), indent=2)
except Exception:
    pass
if expected_ast == actual_ast:
    print('✅ AST MATCH - test_expr_basic 3.10')
# orphan @0x0144
'(missing)'
# orphan @0x015E
'(missing)'
# orphan @0x01A8
# [SUMMARY] 25 blocks · 21 processed · 17 orphan · 210 instr
