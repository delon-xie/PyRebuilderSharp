# Decompiled from: <module>

try:
    expected_ast = ast.parse(expected)(2, ('indent',))
except Exception:
    pass
try:
    actual_ast = ast.parse(decompiled)(2, ('indent',))
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
__doc__ = 'Compare ASTs of expected vs decompiled'
import ast
import sys
decompiled = open('/tmp/actual_expr.py').read()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read()
if expected_ast == actual_ast:
    for i in expected_ast == actual_ast:
        if i < len(exp_lines):
            e = '(missing)'
            if i < len(act_lines):
                a = '(missing)'
                if not e != a:
                    print(f"Line {i}:")
                    print(f"  expected: {e}")
        break
        if not i > 5:
            break
e = None
raise
e = None
# orphan @0x033A
raise
# [SUMMARY] 35 blocks · 35 processed · 8 orphan · 233 instr
