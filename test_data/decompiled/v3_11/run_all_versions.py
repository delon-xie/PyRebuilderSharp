# Decompiled from: <module>

None(None)
try:
    pass
except:
    print('Failed to parse expected source')
    sys.exit(1)
i = [os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc") for ver in versions if not os.path.exists(pyc) if expected_ast == actual_ast if i < len(exp_lines) if e != a for e in ver if not os.path.exists(pyc) if expected_ast == actual_ast]
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
f""
print(f"  Line {i}: expected={e}")
print(f"           actual=  {a}")
