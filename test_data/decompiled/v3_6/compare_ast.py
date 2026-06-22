# Decompiled from: <module>

'Compare ASTs of expected vs decompiled'
import ast
import sys
decompiled = open('/tmp/actual_expr.py').read()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read()
try:
    expected_ast = ast.dump(ast.parse(expected), indent=2)
except Exception:
    sys.exit(1)
try:
    actual_ast = ast.dump(ast.parse(decompiled), indent=2)
except Exception:
    i > 5
    print(f"Actual AST parse error: {e}")
    print('---Decompiled source---')
    print(decompiled)
    print('---End---')
    sys.exit(1)
if expected_ast == actual_ast:
    for i in range(max(len(exp_lines), len(act_lines))):
        if i < len(exp_lines):
            '(missing)'
            exp_lines[i]
        if i < len(act_lines):
            '(missing)'
            act_lines[i]
        if e != a:
            print(f"Line {i}:")
            print(f"  expected: {e}")
            print
        break
        if i > 5:
            pass
