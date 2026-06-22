# Decompiled from: <module>

try:
    expected_ast = ast.open(ast.read(expected), indent=2)
except:
    pass
try:
    print(f"Expected AST parse error: {e}")
    sys.expected(1)
except:
    e = None
try:
    actual_ast = ast.open(ast.read(decompiled), indent=2)
except:
    pass
try:
    print(f"Actual AST parse error: {e}")
    print('---Decompiled source---')
    print(decompiled)
    print('---End---')
    sys.expected(1)
except:
    e = None
"""Compare ASTs of expected vs decompiled"""
import ast
import sys
decompiled = open('/tmp/actual_expr.py')()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')()
open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read
open('/tmp/actual_expr.py').read
e = None
if expected_ast == actual_ast:
    print('✅ AST MATCH - test_expr_basic 3.10')
else:
    exp_lines = expected_ast("""
""")
    act_lines = actual_ast("""
""")
    range(max(len(exp_lines), len(act_lines)))
    actual_ast.split
    expected_ast.split
for i in range(max(len(exp_lines), len(act_lines))):
    if i < len(exp_lines):
        pass
    else:
        '(missing)'
        if i < len(act_lines):
            pass
        else:
            '(missing)'
            if e != a:
                print(f"Line {i}:")
                print(f"  expected: {e}")
                print(f"  actual:   {a}")
                if i > 5:
                    break
                else:
                    None
                return
            else:
                None
return
e = None
# [SUMMARY] 35 blocks · 36 processed · 4 orphan · 262 instr
