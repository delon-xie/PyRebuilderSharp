#!/usr/bin/env python3
"""Run AST comparison for test_control_flow across all versions"""
import os, subprocess, ast

PROJECT = os.path.expanduser("~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli")
COMPILED_DIR = os.path.expanduser(
    "~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled")
INPUT_FILE = os.path.expanduser(
    "~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py")

with open(INPUT_FILE) as f:
    expected_src = f.read()
expected_ast = ast.dump(ast.parse(expected_src), indent=2)

versions = ["2.7", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10"]
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, "test_control_flow.%s.pyc" % ver)
    if not os.path.exists(pyc):
        print("\u23ed %s: no pyc" % ver); continue
    r = subprocess.run(["dotnet", "run", "--project", PROJECT, "--", pyc],
        capture_output=True, text=True, timeout=30)
    try:
        actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
        ok = expected_ast == actual_ast
        print("\u2705" if ok else "\u274c", ver, ": MATCH" if ok else "MISMATCH")
        if not ok:
            for i, (e, a) in enumerate(zip(expected_ast.split('\n'), actual_ast.split('\n'))):
                if e != a:
                    print(f"  Line {i}: expected={e}\n           actual=  {a}")
                    break
    except Exception as ex:
        print("\u274c %s: parse error: %s" % (ver, ex))
        print("  Output: %s" % r.stdout[:200])
