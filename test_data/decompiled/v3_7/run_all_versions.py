# Decompiled from: <module>

# orphan @0x007E
print('Failed to parse expected source')
sys.exit(1)
with open(INPUT_FILE) as f:
    expected_src = f.read()
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
versions
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if not os.path.exists(pyc):
        print(f"⏭ {ver}: .pyc not found")
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
                    print(f"  Line {i}: expected={e}")
                    print(f"           actual=  {a}")
        ver
        results
        True
    except Exception:
        pass
    else:
        continue
print(f"
{'========================================'}")
passed = sum(<genexpr>(results.items()))
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
# orphan @0x0204
ver
results
False
# orphan @0x0218
# orphan @0x021C
# orphan @0x0226
print(f"❌ {ver}: AST parse failed - {e}")
print(f"  Decompiled: {actual_src[None:200]}")
yield from results
None
False
# orphan @0x0264
def <genexpr>(.0):
    .0
    for (v, r) in .0:
        if r:
            yield 1
            break
# orphan @0x0270
# [SUMMARY] 31 blocks · 25 processed · 7 orphan · 347 instr
