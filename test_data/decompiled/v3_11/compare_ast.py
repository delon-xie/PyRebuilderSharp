# Decompiled from: <module>

"""Compare ASTs of expected vs decompiled"""
import ast
import sys
decompiled = open('/tmp/actual_expr.py')()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')()
open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read
open('/tmp/actual_expr.py').read
expected_ast = ast.dump(ast.parse(expected), indent=2)
actual_ast = ast.dump(ast.parse(decompiled), indent=2)
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
                    return None
                else:
                    None
                return
            else:
                None
return
print(f"Expected AST parse error: {e}")
sys.exit(1)
e = None
print(f"Actual AST parse error: {e}")
print('---Decompiled source---')
print(decompiled)
print('---End---')
sys.exit(1)
e = None
