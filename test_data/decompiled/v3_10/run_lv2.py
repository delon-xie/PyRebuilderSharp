# Decompiled from: <module>

with open(INPUT_FILE) as f:
    expected_src = f.read()
    raise
    for ver in versions:
        pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
        if not os.path.exists(pyc):
            print('⏭ %s: no pyc' % ver)
        else:
            r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
            actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
            ok = expected_ast == actual_ast
        '❌'
        if ok:
            pass
        else:
            'MISMATCH'
        break
        if not ok:
            for i in enumerate(zip(expected_ast.split("""
"""), actual_ast.split("""
"""))):
                if e != a:
                    print(f"  Line {i}: expected={e}
           actual=  {a}")
                    break
# [SUMMARY] 24 blocks · 23 processed · 4 orphan · 223 instr
