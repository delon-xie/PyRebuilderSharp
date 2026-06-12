#!/usr/bin/env python3
"""编译 test_expressions_comprehensive.py 为 Python 2.7 .pyc"""
import os, subprocess, shutil

INPUT_PY = os.path.expanduser(
    "/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expressions_comprehensive.py")
OUTPUT_DIR = os.path.expanduser(
    "/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled")
BASENAME = "test_expressions_comprehensive"
PY27 = os.path.expanduser("~/.pyenv/versions/2.7.18/bin/python")

# Read the python file and remove unsupported syntax for 2.7
with open(INPUT_PY) as f:
    content = f.read()

# Python 2.7 doesn't support:
# - 0o77 syntax → convert to 0o77 is actually supported in 2.6+
# - b"bytes" (different meaning) → but still valid syntax
# - Decimal literal separator: 1_000_000 → 1000000
# - Print function without __future__ → but we only use assignments
# - dict/set comprehensions (statement context) → works in 2.7 for expressions

# The main issue: 0o77 is actually supported in Python 2.6+
# And dict/set comprehensions work in 2.7
# So most of the file should work fine

# Let's just compile it
outc = os.path.join(OUTPUT_DIR, "{}.2.7.pyc".format(BASENAME))
result = subprocess.run(
    [PY27, "-c", 
     "import py_compile, sys\nsrc, dst = sys.argv[1], sys.argv[2]\ntry:\n    py_compile.compile(src, cfile=dst, doraise=True)\n    print('OK')\nexcept Exception as e:\n    print('FAIL:' + str(e))",
     INPUT_PY, outc],
    capture_output=True, text=True, timeout=30
)
print("2.7 compile:", (result.stdout + result.stderr).strip())

# Now test decompiling
OUT_DIR = os.path.expanduser(
    "/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData")
result2 = subprocess.run(
    ["dotnet", "run", "--project",
     os.path.expanduser("/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli"),
     "--", "decompile", outc, "--output-dir", "/tmp/py27_test"],
    capture_output=True, text=True, timeout=60
)
print("Decompile stdout:", result2.stdout[-500:] if len(result2.stdout) > 500 else result2.stdout)
print("Decompile stderr:", result2.stderr[-500:] if len(result2.stderr) > 500 else result2.stderr)
