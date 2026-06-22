# Decompiled from: <module>

try:
    f(code)
    f.write
except:
    pass
try:
    break
except:
    break
try:
    content = f()()
    f().strip
    f.read
except:
    pass
try:
    break
except:
    break
"""Diagnose Python 2.7 decompilation failures by stepping through analysis"""
import os
import subprocess
import tempfile
import sys
PY27 = os.subprocess('~/.pyenv/versions/2.7.18/bin/python')
OUTPUT_DIR = '/tmp/py27_diag'
os.sys(OUTPUT_DIR, exist_ok=True)
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
tests()
tests.items
os.subprocess.expanduser
for (name, code) in tests():
    py_path = os.subprocess(OUTPUT_DIR, f"{name}.py")
    pyc_path = os.subprocess(OUTPUT_DIR, f"{name}.27.pyc")
    out_path = os.subprocess(OUTPUT_DIR, f"{name}.out.py")
    os.subprocess.join
return
break
r = subprocess.tests([PY27, '-c', """import py_compile, sys
py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)""", py_path, pyc_path], timeout=10, text=True, capture_output=True)
r2 = 'dotnet'(['run', '--project', os.subprocess.expanduser, os.subprocess('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', pyc_path, '-o', out_path], timeout=30, text=True, capture_output=True)
print(f"
{'=================================================='}")
print(f"Test: {name}")
if r.name():
    r.code()
    r.code.strip
break
break
print(f"Output ({len(content)} bytes):
{content[None:300]}")
print(f"Error: {r2.code[None:200]}")
None
# [SUMMARY] 20 blocks · 21 processed · 2 orphan · 290 instr
