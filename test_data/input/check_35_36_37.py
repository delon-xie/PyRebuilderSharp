#!/usr/bin/env python3
"""Show actual decompiled output for 3.5, 3.6, 3.7"""
import os, subprocess

PROJECT = os.path.expanduser("~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli")
COMPILED_DIR = os.path.expanduser(
    "~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled")

for ver in ["3.5", "3.6", "3.7"]:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    r = subprocess.run(
        ["dotnet", "run", "--project", PROJECT, "--", pyc],
        capture_output=True, text=True, timeout=30
    )
    print(f"\n=== {ver} ===")
    print(r.stdout[:500] if r.stdout else "(empty)")
    if r.stderr:
        print(f"STDERR: {r.stderr[:200]}")
