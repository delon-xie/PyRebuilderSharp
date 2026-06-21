# Decompiled from: <module>

# orphan @0x00B2
# orphan @0x00A6
def <genexpr>(.0):
    .0
    for (v, r) in .0:
        if r:
            yield 1
            break
# orphan @0x0086
print('Failed to parse expected source:', e)
sys.exit(1)
None
# orphan @0x007E
with open(INPUT_FILE) as f:
    expected_src = f.read()
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
versions
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: .pyc not found' % ver)
    r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
    actual_src = r.stdout
    try:
        actual_ast = ast.dump(ast.parse(actual_src), indent=2)
        match = expected_ast == actual_ast
        if match:
            pass
        else:
            '❌'
        if match:
            pass
        'MISMATCH'
        break
        if not match:
            for i in range(max(len(exp_lines), len(act_lines))):
                if i < len(exp_lines):
                    pass
                '(missing)'
                if i < len(act_lines):
                    pass
                '(missing)'
                if e != a:
                    print('  Line %d: expected=%s' % (i, e))
                    print('           actual=  %s' % a)
    except Exception:
        pass
passed = sum(<genexpr>(results.items()))
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
# orphan @0x0208
# orphan @0x020A
yield from results
match
# orphan @0x0216
# orphan @0x0220
print('❌ %s: AST parse failed - %s' % (ver, e))
print('  Decompiled: %s' % actual_src[None:200])
yield from results
None
False
# orphan @0x0258
e = None
# orphan @0x0264
# [SUMMARY] 33 blocks · 24 processed · 10 orphan · 328 instr
