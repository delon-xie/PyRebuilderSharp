#!/usr/bin/env python3
"""
Generate the full test data matrix: compile all test_data/input/*.py
with all available Python versions and store in test_data/compiled/{name}.{ver}.pyc

Handles cross-version syntax differences gracefully.
"""
import os, sys, subprocess, glob, shutil, tempfile

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

# Build Python path map
python_paths = {}
for ver, expected in VERSION_MAP.items():
    p = find_python(expected)
    if p:
        python_paths[ver] = p
    else:
        print(f"WARNING: Python {ver} ({expected}) not found")
print(f"Available Python versions: {', '.join(sorted(python_paths.keys()))}")

# Write helper compile script
compile_script = os.path.join(COMPILED_DIR, "_compile_helper.py")
with open(compile_script, 'w') as f:
    f.write("""
import py_compile, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    py_compile.compile(src, cfile=dst, doraise=True)
    print("OK")
except py_compile.PyCompileError as e:
    sys.exit(2)
except Exception as e:
    print(f"ERR: {e}")
    sys.exit(3)
""")

# Get input files
input_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.py")))
print(f"\nInput files: {len(input_files)}")

stats = {"ok": 0, "skip": 0, "fail": 0, "total": 0}

for src_path in input_files:
    fname = os.path.basename(src_path)
    stem = fname.replace('.py', '')
    
    for ver, py_path in python_paths.items():
        dst_name = f"{stem}.{ver}.pyc"
        dst_path = os.path.join(COMPILED_DIR, dst_name)
        stats["total"] += 1
        
        # Always recompile
        r = subprocess.run([py_path, compile_script, src_path, dst_path],
                          capture_output=True, text=True, timeout=30)
        stdout = r.stdout.strip()
        
        if stdout == "OK":
            stats["ok"] += 1
        elif r.returncode == 2:
            # Compile error (syntax incompatible with this Python version)
            stats["fail"] += 1
            # Only show first few failures per file
            if stats["fail"] <= 5:
                pass  # Don't print every failure
        else:
            stats["fail"] += 1

os.unlink(compile_script)

print(f"\n{'='*50}")
print(f"Compilation complete:")
print(f"  OK:   {stats['ok']}")
print(f"  FAIL: {stats['fail']}")
print(f"  SKIP: {stats['skip']}")
print(f"  TOTAL:{stats['total']}")

# Show which files failed the most
print(f"\nSample of failed files (first 10):")
failure_count = 0
for src_path in input_files:
    fname = os.path.basename(src_path)
    stem = fname.replace('.py', '')
    failures = []
    for ver in sorted(python_paths.keys()):
        dst_name = f"{stem}.{ver}.pyc"
        dst_path = os.path.join(COMPILED_DIR, dst_name)
        if not os.path.exists(dst_path):
            failures.append(ver)
    if failures:
        print(f"  {fname}: missing versions {', '.join(failures)}")
        failure_count += 1
        if failure_count >= 10:
            break
