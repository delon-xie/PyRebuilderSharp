#!/usr/bin/env python3
"""
Recompile test_data/input/*.py to test_data/compiled/*.pyc
using all available Python versions via pyenv.
"""
import os, sys, subprocess, glob

INPUT_DIR = "test_data/input"
COMPILED_DIR = "test_data/compiled"
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

python_paths = {}
for ver, expected in VERSION_MAP.items():
    p = find_python(expected)
    if p:
        python_paths[ver] = p
        print(f"  Python {ver}: {p}")
    else:
        print(f"  Python {ver}: NOT FOUND")

# Key stdlib files to recompile
key_files = {"abc.py", "enum.py", "functools.py", "reprlib.py", "pprint.py",
             "contextlib.py", "dataclasses.py", "ast.py", "re.py"}

# Find input files
input_files = glob.glob(os.path.join(INPUT_DIR, "*.py"))
input_files = [f for f in input_files if os.path.basename(f) in key_files]

# Write a helper compile script
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

results = {"ok": 0, "skip": 0, "fail": 0}
for src_path in input_files:
    fname = os.path.basename(src_path)
    stem = fname.replace('.py', '')
    
    for ver, py_path in python_paths.items():
        dst_name = f"{stem}.{ver}.pyc"
        dst_path = os.path.join(COMPILED_DIR, dst_name)
        
        # Check if update needed
        if os.path.exists(dst_path):
            src_mtime = os.path.getmtime(src_path)
            dst_mtime = os.path.getmtime(dst_path)
            if dst_mtime > src_mtime:
                results["skip"] += 1
                continue
        
        r = subprocess.run([py_path, compile_script, src_path, dst_path],
                          capture_output=True, text=True, timeout=30)
        out = r.stdout.strip()
        if out == "OK":
            results["ok"] += 1
            print(f"  {stem} {ver}")
        else:
            print(f"  FAIL {stem} {ver}: {out}")
            results["fail"] += 1

os.unlink(compile_script)
print(f"\nDone: {results['ok']} ok, {results['skip']} skip, {results['fail']} fail")
