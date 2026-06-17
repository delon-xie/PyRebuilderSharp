# Decompiled from: <module>

for ver in ('3.5', '3.6', '3.7'):
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
    print(f"
=== {ver} ===")
    if r.stdout:
        r.stdout[None:500]('(empty)')
        if not r.stderr:
            pass
    print(f"STDERR: {r.stderr[None:200]}")
    break
# [WARN] 2 instructions not decompiled
#   @0x0188: JUMP_BACKWARD arg=0
#   @0x01BC: JUMP_BACKWARD arg=0
# [SUMMARY] 10 blocks · 11 processed · 1 orphan · 99 instr
