# Decompiled from: <module>

# orphan @0x00C0
def <genexpr>(.0):
    .0
    for (v, r) in .0:
        if r:
            yield 1
            break
with open(INPUT_FILE) as f:
    expected_src = f.read()
    try:
        expected_ast = ast.dump(ast.parse(expected_src), indent=2)
    except Exception:
        print('Failed to parse expected source:', e)
        sys.exit(1)
# orphan @0x015A
'❌'
# orphan @0x015C
print
# orphan @0x0170
'MISMATCH'
# orphan @0x01C4
'(missing)'
# orphan @0x01DE
'(missing)'
# orphan @0x0272
passed = sum(<genexpr>(results.items()))
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
# [SUMMARY] 33 blocks · 26 processed · 27 orphan · 332 instr
