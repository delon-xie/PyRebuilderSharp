#!/usr/bin/env python3
"""Diagnose Python 2.7 decompilation failures by stepping through analysis"""
import os, subprocess, tempfile, sys

PY27 = os.path.expanduser("~/.pyenv/versions/2.7.18/bin/python")
OUTPUT_DIR = "/tmp/py27_diag"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Test files to compile
tests = {
    "expr_simple": "a = 1\nb = 2\nc = a + b\n",
    "expr_func": "def foo():\n    return 42\nx = foo()\n",
    "expr_bool": "x = True\ny = False\nz = x and y\nw = x or y\n",
    "expr_all": """# Complete expressions for 2.7
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
""",
}

for name, code in tests.items():
    py_path = os.path.join(OUTPUT_DIR, f"{name}.py")
    pyc_path = os.path.join(OUTPUT_DIR, f"{name}.27.pyc")
    out_path = os.path.join(OUTPUT_DIR, f"{name}.out.py")

    with open(py_path, 'w') as f:
        f.write(code)

    # Compile with 2.7
    r = subprocess.run([PY27, "-c",
        "import py_compile, sys\npy_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)",
        py_path, pyc_path], capture_output=True, text=True, timeout=10)

    # Decompile
    r2 = subprocess.run(
        ["dotnet", "run", "--project",
         os.path.expanduser("~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli"),
         "--", pyc_path, "-o", out_path],
        capture_output=True, text=True, timeout=30
    )

    print(f"\n{'='*50}")
    print(f"Test: {name}")
    print(f"Compile: {r.stdout.strip() or r.stderr.strip()}")
    print(f"Decompile: {r2.stdout.strip()[:100]}")
    if os.path.exists(out_path):
        with open(out_path) as f:
            content = f.read().strip()
        print(f"Output ({len(content)} bytes):\n{content[:300]}")
    else:
        print(f"Error: {r2.stderr[:200]}")
