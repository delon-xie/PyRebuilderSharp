# Decompiled from: <module>

with open('/tmp/diag35.cs', 'w') as f:
    f.write(test_code)
    raise
    r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', '/tmp/t1.35.pyc'], capture_output=True, text=True, timeout=30)
    print('Stdout:', r.stdout[None:500])
    print('Stderr:', r.stderr[None:500])
    return None
# [SUMMARY] 4 blocks · 4 processed · 0 orphan · 92 instr
