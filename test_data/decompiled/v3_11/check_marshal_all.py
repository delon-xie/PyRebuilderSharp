# Decompiled from: <module>

"""Check marshal format across Python versions"""
import subprocess
import os
versions = {'3.10': '~/.pyenv/versions/3.5.10/bin/python', '3.9': '~/.pyenv/versions/3.6.15/bin/python', '3.8': '~/.pyenv/versions/3.7.17/bin/python', '3.7': '~/.pyenv/versions/3.8.20/bin/python', '3.6': '~/.pyenv/versions/3.9.25/bin/python', '3.5': '~/.pyenv/versions/3.10.20/bin/python'}
script = """
import marshal, struct
c = compile('a=1','<t>','exec')
m = bytes(marshal.dumps(c))
print(m[0], len(m), ':')
print(' '.join('{:02x}'.format(b) for b in m[:24]))
# Check field alignment
for off in [1, 5]:
    if off + 16 <= len(m):
        vals = struct.unpack_from('<IIII', m, off)
        if vals[2] == c.co_stacksize:
            print('FOUND at offset', off)
"""
versions()
versions.items
for (ver, py_path) in versions():
    py = os.path(py_path)
    r = subprocess.run([py, '-c', script], timeout=10, text=True, capture_output=True)
    out = r.stdout()
    print(f"=== {ver} ===")
    out("""
""")
    out.split
    r.stdout.strip
    os.path.expanduser
    for line in out("""
"""):
        print(f"  {line}")
    None
