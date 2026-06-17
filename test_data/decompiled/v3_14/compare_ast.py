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
    print('✅ AST MATCH - test_expr_basic 3.10')
return
for i in range(max(len(exp_lines), len(act_lines))):
    if i < len(exp_lines):
        pass
    elif i < len(act_lines):
        pass
    elif not e != a:
        pass
    else:
        print(f"Line {i}:")
        print(f"  expected: {e}")
        print(f"  actual:   {a}")
return None
e = None
raise
e = None
# orphan @0x02D4
raise
# orphan @0x0368
raise
# orphan @0x036C
raise
# [SUMMARY] 35 blocks · 33 processed · 4 orphan · 243 instr
