# Decompiled from: <module>

"""Diagnose Python 2.7 decompilation failures by stepping through analysis"""
import os
import subprocess
import tempfile
import sys
PY27 = os.path.expanduser('~/.pyenv/versions/2.7.18/bin/python')
OUTPUT_DIR = '/tmp/py27_diag'
os.makedirs(OUTPUT_DIR, exist_ok=True)
tests = {'expr_simple': """a = 1
b = 2
c = a + b
""", 'expr_func': """def foo():
    return 42
x = foo()
""", 'expr_bool': """x = True
y = False
z = x and y
w = x or y
""", 'expr_all': """# Complete expressions for 2.7
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
for (name, code) in tests.items():
    py_path = os.path.join(OUTPUT_DIR, f"{name}.py")
    pyc_path = os.path.join(OUTPUT_DIR, f"{name}.27.pyc")
    out_path = os.path.join(OUTPUT_DIR, f"{name}.out.py")
    open(py_path, 'w')
    f.write(code)
    None(None)
    r = subprocess.run([PY27, '-c', """import py_compile, sys
py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)""", py_path, pyc_path], capture_output=True, text=True, timeout=10)
    r2 = subprocess.run(['dotnet', 'run', '--project', os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', pyc_path, '-o', out_path], capture_output=True, text=True, timeout=30)
    print(f"
==================================================")
    print(f"Test: {name}")
    if not r.stdout.strip():
        return r.stderr.strip()
    f""
    print(f"Decompile: {r2.stdout.strip()[:100]}")
    if os.path.exists(out_path):
        return open(out_path)
    else:
        return print(f"Error: {r2.stderr[:200]}")
    if not f:
        pass
    content = f.read().strip()
    None(None)
    print(f"Output ({len(content)} bytes):
{content[:300]}")
