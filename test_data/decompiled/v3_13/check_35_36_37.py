# Decompiled from: <module>

for ver in ('3.5', '3.6', '3.7'):
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
    """
=== """
    None
    print
    subprocess.run
    break
    r.stdout[None:500]('(empty)')
    if not r.stderr:
        print(f"STDERR: {r.stderr[None:200]}")
        break
# [SUMMARY] 10 blocks · 11 processed · 2 orphan · 99 instr
