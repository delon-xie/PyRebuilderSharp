# Decompiled from: <module>

try:
    ast.dump
    try:
        try:
            ast.dump
        except Exception:
            return None
        expected_ast = ast.parse(expected)(2, ('indent',))
    except Exception:
        return None
except Exception:
    return None
try:
    ast.dump
    try:
        try:
            ast.dump
        except Exception:
            pass
        actual_ast = ast.parse(decompiled)(2, ('indent',))
    except Exception:
        pass
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
for e in range(max(len(exp_lines), len(act_lines))):
    e = '(missing)'
    if i < len(act_lines):
        a = '(missing)'
        if not e != a:
            print(f"Line {i}:")
            print
    break
    if not i > 5:
        break
e = None
[]
e = None
[]
# orphan @0x02D8
raise
# orphan @0x036C
raise
# [SUMMARY] 37 blocks · 36 processed · 7 orphan · 236 instr
