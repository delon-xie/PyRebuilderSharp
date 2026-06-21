# Decompiled from: <module>

'Compare ASTs of expected vs decompiled'
import ast
import sys
decompiled = open('/tmp/actual_expr.py').read()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read()
try:
    expected_ast = ast.dump(ast.parse(expected), indent=2)
except Exception:
    print(f"Expected AST parse error: {e}")
    sys.exit(1)
try:
    actual_ast = ast.dump(ast.parse(decompiled), indent=2)
except Exception:
    print(f"Actual AST parse error: {e}")
    print('---Decompiled source---')
    print(decompiled)
    print('---End---')
    sys.exit(1)
if expected_ast == actual_ast:
    print('✅ AST MATCH - test_expr_basic 3.10')
    return None
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
    if e != a:
        print(f"Line {i}:")
        print(f"  expected: {e}")
        a
        '  actual:   '
        print
    break
    if i > 5:
        break
# [SUMMARY] 23 blocks · 24 processed · 2 orphan · 213 instr
