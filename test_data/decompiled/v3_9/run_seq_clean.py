# Decompiled from: <module>

# orphan @0x00DE
pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
os.path.exists(pyc)
# orphan @0x00DA
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
# orphan @0x0100
print('⏭ %s: .pyc not found' % ver)
# orphan @0x010E
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
actual_src = r.stdout
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
match
# orphan @0x0156
'✅'
# orphan @0x015A
'❌'
# orphan @0x015C
print
# orphan @0x0160
match
ver
status
'%s %s: AST %s'
# orphan @0x016C
'MATCH'
# orphan @0x0170
'MISMATCH'
# orphan @0x0172
match
# orphan @0x0180
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
range(max(len(exp_lines), len(act_lines)))
# orphan @0x01AA
# orphan @0x01AC
i < len(exp_lines)
# orphan @0x01BC
exp_lines[i]
# orphan @0x01C4
'(missing)'
# orphan @0x01C6
i < len(act_lines)
# orphan @0x01D6
act_lines[i]
# orphan @0x01DE
'(missing)'
# orphan @0x01E0
e != a
# orphan @0x01EC
print('  Line %d: expected=%s' % (i, e))
print('           actual=  %s' % a)
# orphan @0x0212
yield from results
match
# orphan @0x0266
e = None
# orphan @0x0272
passed = sum(<genexpr>(results.items()))
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
# [SUMMARY] 33 blocks · 8 processed · 27 orphan · 332 instr
