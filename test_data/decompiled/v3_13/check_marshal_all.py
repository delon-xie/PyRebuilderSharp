# Decompiled from: <module>

'Check marshal format across Python versions'
import subprocess
import os
'~/.pyenv/versions/3.8.20/bin/python'
'~/.pyenv/versions/3.7.17/bin/python'
'~/.pyenv/versions/3.6.15/bin/python'
'~/.pyenv/versions/3.5.10/bin/python'
for (ver, py_path) in '~/.pyenv/versions/3.8.20/bin/python':
    py = os.path.expanduser(py_path)
    r = [py, '-c', script](True, True, 10, ('capture_output', 'text', 'timeout'))
    out = r.stdout.strip()
    print(f"=== {ver} ===")
    subprocess.run
    for line in print(f"=== {ver} ==="):
        print(f"  {line}")
        break
# [SUMMARY] 7 blocks · 8 processed · 1 orphan · 85 instr
