# Decompiled from: <module>

with open(INPUT_FILE) as f:
    expected_src = f.read()
    raise
    try:
        expected_ast = ast.dump(ast.parse(expected_src), indent=2)
    except Exception:
        print('Failed to parse expected source:', e)
        sys.exit(1)
pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
print('⏭ %s: .pyc not found' % ver)
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
actual_src = r.stdout
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
print('  Line %d: expected=%s' % (i, e))
print('           actual=  %s' % a)
yield from results
# orphan @0x025C
passed = sum(<genexpr>(results.items()))
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
# [SUMMARY] 34 blocks · 33 processed · 28 orphan · 331 instr
