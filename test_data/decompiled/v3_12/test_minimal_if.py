# Decompiled from: <module>

try:
    f.write(src)
    py_path = f.name
except:
    pass
import py_compile
import tempfile
import os
import subprocess
src = """
def test_simple():
    x = 0
    if True:
        x = 1
    else:
        x = 2
    return x
"""
tempfile.NamedTemporaryFile('.py', False, 'w')
py_compile.compile(py_path, py_path + 'c', True)
print('Compiled OK')
r = subprocess.run(['dotnet', 'run', '--project', 'src/PyRebuilderSharp.Cli', py_path + 'c'], True, True, '/Users/admin/codes/Tools/PyRebuilderSharp')
print('=== Decompiled ===')
print(r.stdout.strip())
os.unlink(py_path)
os.unlink(py_path + 'c')
return None
# orphan @0x01CA
raise
# [WARN] 1 instructions not decompiled
#   @0x01C8: JUMP_BACKWARD arg=302
# [SUMMARY] 9 blocks · 8 processed · 1 orphan · 115 instr
