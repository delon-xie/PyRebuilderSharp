# Decompiled from: <module>

with open(INPUT_FILE) as f:
    expected_src = f.read()
    raise
    try:
        expected_ast = ast.dump(ast.parse(expected_src), indent=2)
    except Exception:
        print('Failed to parse expected source:', e)
        sys.exit(1)
# orphan @0x0154
'❌'
# orphan @0x0156
ver
status
'%s %s: AST %s'
print
# orphan @0x0168
'MISMATCH'
# orphan @0x01B8
'(missing)'
# orphan @0x01D0
'(missing)'
# orphan @0x025C
passed = sum(<genexpr>(results.items()))
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
# [SUMMARY] 34 blocks · 28 processed · 28 orphan · 331 instr
