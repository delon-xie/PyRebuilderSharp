#!/usr/bin/env python3
"""Force recompile abc.py with all Python versions to test defaults."""
import os, sys, subprocess

COMPILED_DIR = "test_data/compiled"
INPUT_DIR = "test_data/input"
PYENV_ROOT = os.path.expanduser("~/.pyenv/versions")

VERSION_MAP = {
    "3.5": "3.5.10",
    "3.6": "3.6.15",
    "3.7": "3.7.17",
    "3.8": "3.8.20",
    "3.9": "3.9.25",
    "3.10": "3.10.20",
    "3.11": "3.11.15",
    "3.12": "3.12.13",
    "3.13": "3.13.12",
    "3.14": "3.14.3",
}

def find_python(ver_str):
    for d in os.listdir(PYENV_ROOT):
        if d.startswith(ver_str):
            for candidate in ["bin/python3", "bin/python3.14"]:
                p = os.path.join(PYENV_ROOT, d, candidate)
                if os.path.isfile(p):
                    return p
    return None

compile_script = os.path.join(COMPILED_DIR, "_do_compile.py")
with open(compile_script, 'w') as f:
    f.write("""
import py_compile, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    py_compile.compile(src, cfile=dst, doraise=True)
    print("OK")
except py_compile.PyCompileError as e:
    print(f"FAIL: {e}")
except Exception as e:
    print(f"ERR: {e}")
""")

src_path = os.path.join(INPUT_DIR, "abc.py")

# First check: does the current abc.py actually have the default params?
with open(src_path) as f:
    content = f.read()
if "fget=None" in content:
    print("✅ abc.py has `fget=None` defaults in source")
else:
    print("❌ abc.py does NOT have `fget=None` — can't fix test data")
    sys.exit(1)

for ver, expected in VERSION_MAP.items():
    py_path = find_python(expected)
    if not py_path:
        print(f"  Py{ver}: no python found")
        continue
    
    dst_name = f"abc.{ver}.pyc"
    dst_path = os.path.join(COMPILED_DIR, dst_name)
    
    r = subprocess.run([py_path, compile_script, src_path, dst_path],
                      capture_output=True, text=True, timeout=30)
    out = r.stdout.strip()
    if out == "OK":
        print(f"  Py{ver}: compiled ✅")
    else:
        print(f"  Py{ver}: {out}")

os.unlink(compile_script)
print("\nDone — now run baseline to verify default params appear")
