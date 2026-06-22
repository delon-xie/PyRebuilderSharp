# Decompiled from: <module>

print(f"⏭ {ver}: .pyc not found")
pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
with open(INPUT_FILE) as f:
    expected_src = f.read()
    raise
    try:
        ast = ast
        expected_ast = ast.dump(ast.parse(expected_src), indent=2)
    except print:
        sys.exit(1)
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
actual_src = r.stdout
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
print(f"  Line {i}: expected={e}")
print(f"           actual=  {a}")
# orphan @0x01FE
True
# orphan @0x0262
print(f"
{'========================================'}")
passed = sum(<genexpr>(results.items()))
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
# [SUMMARY] 34 blocks · 32 processed · 28 orphan · 347 instr
