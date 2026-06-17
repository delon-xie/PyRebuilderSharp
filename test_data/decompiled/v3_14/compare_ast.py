# Decompiled from: <module>

try:
    expected_ast = ast.parse(expected)(2, ('indent',))
except Exception:
    return None
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
    return None
break
if not i > 5:
    pass
for e in range(max(len(exp_lines), len(act_lines))):
    e = '(missing)'
    if i < len(act_lines):
        a = '(missing)'
        if not e != a:
            pass
    print(f"Line {i}:")
    print(f"  expected: {e}")
break
e = None
raise
e = None
# orphan @0x036C
raise
# [WARN] 2 instructions not decompiled
#   @0x0212: JUMP_BACKWARD arg=0
#   @0x0268: JUMP_BACKWARD arg=0
# [SUMMARY] 37 blocks · 37 processed · 8 orphan · 243 instr
