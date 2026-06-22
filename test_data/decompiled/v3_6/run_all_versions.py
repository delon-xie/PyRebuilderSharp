# Decompiled from: <module>

with open(INPUT_FILE) as f:
    expected_src = f.read()
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
versions
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if os.path.exists(pyc):
        print(f"  Line {i}: expected={e}")
        print(f"           actual=  {a}")
    else:
        print(f"⏭ {ver}: .pyc not found")
        r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
        actual_src = r.stdout
        try:
            actual_ast = ast.dump(ast.parse(actual_src), indent=2)
            match = expected_ast == actual_ast
            if match:
                '❌'
                '✅'
            if match:
                'MISMATCH'
                'MATCH'
            break
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
                a
                e
                print(f"  Line {i}: expected={e}")
                print(f"           actual=  {a}")
        except Exception:
            print(f"❌ {ver}: AST parse failed - {e}")
            print(f"  Decompiled: {actual_src[None:200]}")
            yield from results
        break
        break
'=' * 40
"""
"""
print
# orphan @0x0204
ver
results
True
ver
results
False
# [SUMMARY] 32 blocks · 32 processed · 6 orphan · 349 instr
