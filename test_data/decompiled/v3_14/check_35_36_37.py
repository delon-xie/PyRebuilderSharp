# Decompiled from: <module>

for ver in ('3.5', '3.6', '3.7'):
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
    print(f"
=== {ver} ===")
    if r.stdout:
        r.stdout[:500]('(empty)')
        if not r.stderr:
            pass
    print(f"STDERR: {r.stderr[:200]}")
    return None
# [WARN] 2 instructions not decompiled
#   @0x019A: JUMP_BACKWARD arg=0
#   @0x01D6: JUMP_BACKWARD arg=0
# [SUMMARY] 10 blocks · 11 processed · 1 orphan · 98 instr
