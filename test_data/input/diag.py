#!/usr/bin/env python3
"""Diagnose 3.7 decompilation - test module-level code"""
import os, subprocess

PROJECT = os.path.expanduser("~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli")
pyc = os.path.expanduser(
    "~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.7.pyc")

# Test with --verbose or similar if available
r = subprocess.run(
    ["dotnet", "run", "--project", PROJECT, "--", pyc],
    capture_output=True, text=True, timeout=30
)
print("STDOUT:", r.stdout)
print("STDERR:", r.stderr)

# Also check 3.5
pyc35 = os.path.expanduser(
    "~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.5.pyc")
r2 = subprocess.run(
    ["dotnet", "run", "--project", PROJECT, "--", pyc35],
    capture_output=True, text=True, timeout=30
)
print("3.5 STDOUT:", r2.stdout[:200])
print("3.5 STDERR:", r2.stderr[:200])
