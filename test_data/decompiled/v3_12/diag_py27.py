# Decompiled from: <module>

try:
    f.write(code)
except:
    break
try:
    content = f.read().strip()
except:
    break
__doc__ = 'Diagnose Python 2.7 decompilation failures by stepping through analysis'
import os
import subprocess
import tempfile
import sys
PY27 = os.path.expanduser('~/.pyenv/versions/2.7.18/bin/python')
OUTPUT_DIR = '/tmp/py27_diag'
os.makedirs(OUTPUT_DIR, True)
tests = {'expr_all': """a = 1
b = 2
c = a + b
""", 'expr_bool': """def foo():
    return 42
x = foo()
""", 'expr_func': """x = True
y = False
z = x and y
w = x or y
""", 'expr_simple': """# Complete expressions for 2.7
a = 1
b = True
c = None
d = 3.14
e = "hello"
f = x + y
g = x - y
h = x * y
i = x / y
j = -x
k = not x
l = x < y
m = x == y
n = x is y
o = func(x)
p = items[0]
q = items[1:10]
r = obj.attr
s = x if cond else y
"""}
tests.items()
for (name, code) in tests.items():
    py_path = os.path.join(OUTPUT_DIR, f"{name}.py")
    pyc_path = os.path.join(OUTPUT_DIR, f"{name}.27.pyc")
    out_path = os.path.join(OUTPUT_DIR, f"{name}.out.py")
    open(py_path, 'w')
break
r = subprocess.run([PY27, '-c', """import py_compile, sys
py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)""", py_path, pyc_path], True, True, 10)
r2 = subprocess.run(['dotnet', 'run', '--project', os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', pyc_path, '-o', out_path], True, True, 30)
print(f"
{'=================================================='}")
print(f"Test: {name}")
if not r.stdout.strip():
    break
break
if os.path.exists(out_path):
    open(out_path)
else:
    'Error: '(f"{r2.stderr}{None // 200}")
break
'Output ('(f"{len(content)} bytes):
{content}{None // 300}")
break
raise
break
# orphan @0x0488
# [WARN] 4 instructions not decompiled
#   @0x0422: JUMP_BACKWARD arg=878
#   @0x0456: JUMP_BACKWARD arg=930
#   @0x046E: JUMP_BACKWARD arg=684
#   @0x0486: JUMP_BACKWARD arg=150
# [SUMMARY] 24 blocks · 23 processed · 1 orphan · 262 instr
