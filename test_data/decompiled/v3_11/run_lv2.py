# Decompiled from: <module>

None(None)
i = [os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver) for ver in versions if not os.path.exists(pyc) if expected_ast == actual_ast if e != a for ver in ver if not os.path.exists(pyc) if expected_ast == actual_ast]
actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
ok = expected_ast == actual_ast
