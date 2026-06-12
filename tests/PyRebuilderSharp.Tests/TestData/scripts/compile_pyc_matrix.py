#!/usr/bin/env python3
"""
compile_pyc_matrix.py — 用所有 pyenv Python 版本编译 .py 到各版本 .pyc

用法: python3 compile_pyc_matrix.py <input.py> <output_dir>
输出: <output_dir>/<basename>.<version>.pyc
"""

import os, sys, subprocess, py_compile

INPUT_PY = sys.argv[1]
OUTPUT_DIR = sys.argv[2]
BASENAME = os.path.splitext(os.path.basename(INPUT_PY))[0]

os.makedirs(OUTPUT_DIR, exist_ok=True)

PYENV_ROOT = os.path.expanduser("~/.pyenv/versions")

VERSIONS = [
    "2.7.18",
    "3.5.10", "3.6.15", "3.7.17", "3.8.20", "3.9.25",
    "3.10.0", "3.10.20",
    "3.11.0", "3.11.15",
    "3.12.13",
    "3.13.12",
    "3.14.3",
]

compile_script = """
import py_compile, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    py_compile.compile(src, cfile=dst, doraise=True)
    size = len(open(dst, 'rb').read())
    print('OK:' + str(size))
except Exception as e:
    print('FAIL:' + str(e))
"""

for ver in VERSIONS:
    py = os.path.join(PYENV_ROOT, ver, "bin", "python")
    if not os.path.isfile(py):
        print(f"SKIP {ver} (not found)")
        continue

    tag = ".".join(ver.split(".")[:2])
    outc = os.path.join(OUTPUT_DIR, "{}.{}.pyc".format(BASENAME, tag))

    print("COMPILE {} -> {}".format(ver, os.path.basename(outc)), end=" ")
    sys.stdout.flush()

    result = subprocess.run(
        [py, "-c", compile_script, INPUT_PY, outc],
        capture_output=True, text=True, timeout=30
    )

    out = (result.stdout + result.stderr).strip()
    print(out)

print("DONE")
