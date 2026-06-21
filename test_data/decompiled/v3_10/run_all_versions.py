# Decompiled from: <module>

# orphan @0x00E2
print(f"⏭ {ver}: .pyc not found")
# orphan @0x00BE
pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
os.path.exists(pyc)
# orphan @0x00BC
with open(INPUT_FILE) as f:
    expected_src = f.read()
    raise
    try:
        ast = ast
        expected_ast = ast.dump(ast.parse(expected_src), indent=2)
    except print:
        sys.exit(1)
# orphan @0x00F4
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
actual_src = r.stdout
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
match
# orphan @0x013A
'✅'
# orphan @0x013E
'❌'
# orphan @0x0140
match
': AST '
ver
' '
status
print
# orphan @0x0154
'MATCH'
# orphan @0x0158
'MISMATCH'
# orphan @0x015A
match
# orphan @0x0166
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
range(max(len(exp_lines), len(act_lines)))
# orphan @0x0190
# orphan @0x0192
i < len(exp_lines)
# orphan @0x01A0
exp_lines[i]
# orphan @0x01A8
'(missing)'
# orphan @0x01AA
i < len(act_lines)
# orphan @0x01B8
act_lines[i]
# orphan @0x01C0
'(missing)'
# orphan @0x01C2
e != a
# orphan @0x01CC
print(f"  Line {i}: expected={e}")
print(f"           actual=  {a}")
# orphan @0x01F2
# orphan @0x01F4
ver
results
False
# orphan @0x01FE
ver
results
True
# orphan @0x0206
# orphan @0x020A
Exception
print(f"❌ {ver}: AST parse failed - {e}")
print(f"  Decompiled: {actual_src[None:200]}")
yield from results
def <genexpr>(.0):
    .0
    for (v, r) in .0:
        if r:
            yield 1
            break
False
# orphan @0x0258
e = None
# orphan @0x0262
print(f"
{'========================================'}")
passed = sum(<genexpr>(results.items()))
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
# [SUMMARY] 34 blocks · 7 processed · 28 orphan · 347 instr
