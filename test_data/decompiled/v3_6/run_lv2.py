# Decompiled from: <module>

with open(INPUT_FILE) as f:
    expected_src = f.read()
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
    if os.path.exists(pyc):
        break
    else:
        print('⏭ %s: no pyc' % ver)
        r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
        try:
            actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
            ok = expected_ast == actual_ast
            if ok:
                '❌'
                '✅'
            if ok:
                'MISMATCH'
                ': MATCH'
            break
            if not ok:
                enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
""")))
            for i in enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
"""))):
                if e != a:
                    print(f"  Line {i}: expected={e}
           actual=  {a}")
                break
        except Exception:
            print('❌ %s: parse error: %s' % (ver, ex))
            print('  Output: %s' % r.stdout[None:200])
# [SUMMARY] 23 blocks · 24 processed · 4 orphan · 221 instr
