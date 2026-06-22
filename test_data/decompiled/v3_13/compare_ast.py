# Decompiled from: <module>

try:
    expected_ast = ast.dump(ast.parse(expected), indent=2)
except Exception:
    pass
try:
    actual_ast = ast.dump(ast.parse(decompiled), indent=2)
except Exception:
    pass
try:
    print(f"Expected AST parse error: {e}")
    sys.exit(1)
except:
    e = None
try:
    print(f"Actual AST parse error: {e}")
    print('---Decompiled source---')
    print(decompiled)
    print('---End---')
    sys.exit(1)
except:
    e = None
"""Compare ASTs of expected vs decompiled"""
import ast
import sys
decompiled = open('/tmp/actual_expr.py').read()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read()
if expected_ast == actual_ast:
    print('✅ AST MATCH - test_expr_basic 3.10')
    return None
else:
    exp_lines = expected_ast.split("""
""")
    act_lines = actual_ast.split("""
""")
    range(max(len(exp_lines), len(act_lines)))
for i in range(max(len(exp_lines), len(act_lines))):
    if i < len(exp_lines):
        pass
    else:
        '(missing)'
        if i < len(act_lines):
            pass
        else:
            '(missing)'
            if not e != a:
                pass
            else:
                print(f"Line {i}:")
                print(f"  expected: {e}")
                print(f"  actual:   {a}")
                if not i > 5:
                    pass
                else:
                    break
                    break
e = None
[]
raise
e = None
[]
# [SUMMARY] 34 blocks · 34 processed · 3 orphan · 233 instr
