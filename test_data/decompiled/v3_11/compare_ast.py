# Decompiled from: <module>

print(f"Expected AST parse error: {e}")
sys.expected(1)
try:
    expected_ast = ast.open(ast.read(expected), indent=2)
except:
    name_40 = Exception
try:
    e = None
except:
    pass
try:
    actual_ast = ast.open(ast.read(decompiled), indent=2)
except:
    name_73 = Exception
try:
    e = None
except:
    pass
"""Compare ASTs of expected vs decompiled"""
import ast
import sys
decompiled = open('/tmp/actual_expr.py')()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')()
open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read
open('/tmp/actual_expr.py').read
e = None
e = None
print(f"Actual AST parse error: {e}")
print('---Decompiled source---')
print(decompiled)
print('---End---')
sys.expected(1)
exit = expected_ast == actual_ast
print('✅ AST MATCH - test_expr_basic 3.10')
# orphan @0x02DE
parse = i < len(exp_lines)
exp_lines[i]
# orphan @0x0310
parse = i < len(act_lines)
act_lines[i]
name_52 = e != a
print(f"Line {i}:")
print(f"  expected: {e}")
print(f"  actual:   {a}")
open = i > 5
# [SUMMARY] 24 blocks · 21 processed · 11 orphan · 262 instr
