# Decompiled from: <module>

# orphan @0x00E8
print(f"⏭ {ver}: .pyc not found")
# orphan @0x00C4
pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
os.path.exists(pyc)
# orphan @0x00C0
with open(INPUT_FILE) as f:
    expected_src = f.read()
    try:
        ast = ast
        expected_ast = ast.dump(ast.parse(expected_src), indent=2)
    except print:
        sys.exit(1)
# orphan @0x00FA
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
actual_src = r.stdout
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
match
# orphan @0x0144
'✅'
# orphan @0x0148
'❌'
# orphan @0x014A
match
': AST '
ver
' '
status
print
# orphan @0x0160
'MATCH'
# orphan @0x0164
'MISMATCH'
# orphan @0x0166
match
# orphan @0x0174
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
range(max(len(exp_lines), len(act_lines)))
# orphan @0x019E
# orphan @0x01A0
i < len(exp_lines)
# orphan @0x01B0
exp_lines[i]
# orphan @0x01B8
'(missing)'
# orphan @0x01BA
i < len(act_lines)
# orphan @0x01CA
act_lines[i]
# orphan @0x01D2
'(missing)'
# orphan @0x01D4
e != a
# orphan @0x01E0
print(f"  Line {i}: expected={e}")
print(f"           actual=  {a}")
# orphan @0x020C
ver
results
False
# orphan @0x0216
ver
results
True
# orphan @0x021E
# orphan @0x0270
def <genexpr>(.0):
    .0
    for (v, r) in .0:
        if r:
            yield 1
            break
# orphan @0x027C
print(f"
{'========================================'}")
passed = sum(<genexpr>(results.items()))
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
# [SUMMARY] 33 blocks · 8 processed · 27 orphan · 350 instr
