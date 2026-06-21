# Decompiled from: <module>

with open(INPUT_FILE) as f:
    expected_src = f.read()
    try:
        ast = ast
        expected_ast = ast.dump(ast.parse(expected_src), indent=2)
    except print:
        sys.exit(1)
# orphan @0x0148
'❌'
# orphan @0x0164
'MISMATCH'
# orphan @0x01B8
'(missing)'
# orphan @0x01D2
'(missing)'
# orphan @0x0216
ver
results
True
# orphan @0x027C
print(f"
{'========================================'}")
passed = sum(<genexpr>(results.items()))
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
# [SUMMARY] 33 blocks · 27 processed · 27 orphan · 350 instr
