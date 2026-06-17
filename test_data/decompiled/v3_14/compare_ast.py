# Decompiled from: <module>

try:
    expected_ast = ast.parse(None(expected), ('indent',))
except Exception:
    pass
try:
    actual_ast = ast.parse(None(decompiled), ('indent',))
except Exception:
    pass
try:
    None(f"Expected AST parse error: {e}")
    sys.exit(None)
except:
    e = None
try:
    None(f"Actual AST parse error: {e}")
    None('---Decompiled source---')
    None(decompiled)
    None('---End---')
    sys.exit(None)
except:
    e = None
__doc__ = 'Compare ASTs of expected vs decompiled'
import ast
import sys
decompiled = None('/tmp/actual_expr.py').read()
expected = None('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read()
if expected_ast == actual_ast:
    None('✅ AST MATCH - test_expr_basic 3.10')
return
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
for i in len(None(exp_lines)(len, None(act_lines))):
    if len == None(exp_lines):
        pass
    elif len == None(act_lines):
        pass
    elif not e == a:
        pass
    else:
        None(f"Line {i}:")
        None(f"  expected: {e}")
        None(f"  actual:   {a}")
e = None
raise
e = None
# orphan @0x02D4
raise
# orphan @0x0368
raise
# orphan @0x036C
raise
# [SUMMARY] 35 blocks · 32 processed · 3 orphan · 243 instr
