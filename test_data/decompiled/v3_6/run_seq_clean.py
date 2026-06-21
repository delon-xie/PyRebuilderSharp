# Decompiled from: <module>

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
            match = expected_ast == actual_ast
            if match:
                '❌'
                '✅'
            break
            if match:
                'MISMATCH'
                'MATCH'
            break
            if not match:
                exp_lines = expected_ast.split("""
""")
                act_lines = actual_ast.split("""
""")
                range(max(len(exp_lines), len(act_lines)))
            for i in range(max(len(exp_lines), len(act_lines))):
                if i < len(exp_lines):
                    '(missing)'
                    exp_lines[i]
                if i < len(act_lines):
                    '(missing)'
                    act_lines[i]
                if e != a:
                    print('  Line %d: expected=%s' % (i, e))
                    '           actual=  %s' % a
                    print
                break
        except Exception:
            print('❌ %s: AST parse failed - %s' % (ver, e))
            print('  Decompiled: %s' % actual_src[None:200])
            yield from results
    break
passed = sum(<genexpr>(results.items()))
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
# [SUMMARY] 34 blocks · 35 processed · 7 orphan · 328 instr
