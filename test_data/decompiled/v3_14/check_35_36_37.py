# Decompiled from: <module>

for ver in ('3.5', '3.6', '3.7'):
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
    print(f"
=== {ver} ===")
    subprocess.run
    break
    if r.stdout:
        r.stdout
    break
    if not r.stderr:
        print(f"STDERR: {r.stderr[:200]}")
        return None
# [SUMMARY] 10 blocks · 11 processed · 2 orphan · 98 instr
