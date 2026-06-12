#!/usr/bin/env python3
"""Run AST comparison for test_seq_clean across all versions"""
import os, subprocess, ast, sys

PROJECT = os.path.expanduser("~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli")
COMPILED_DIR = os.path.expanduser(
    "~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled")
INPUT_FILE = os.path.expanduser(
    "~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py")

with open(INPUT_FILE) as f:
    expected_src = f.read()

try:
    expected_ast = ast.dump(ast.parse(expected_src), indent=2)
except Exception as e:
    print("Failed to parse expected source:", e)
    sys.exit(1)

versions = ["2.7", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10"]
results = {}

for ver in versions:
    pyc = os.path.join(COMPILED_DIR, "test_seq_clean.%s.pyc" % ver)
    if not os.path.exists(pyc):
        print("\u23ed %s: .pyc not found" % ver)
        continue
    
    r = subprocess.run(
        ["dotnet", "run", "--project", PROJECT, "--", pyc],
        capture_output=True, text=True, timeout=30
    )
    actual_src = r.stdout
    
    try:
        actual_ast = ast.dump(ast.parse(actual_src), indent=2)
        match = expected_ast == actual_ast
        status = "\u2705" if match else "\u274c"
        print("%s %s: AST %s" % (status, ver, "MATCH" if match else "MISMATCH"))
        if not match:
            exp_lines = expected_ast.split('\n')
            act_lines = actual_ast.split('\n')
            for i in range(max(len(exp_lines), len(act_lines))):
                e = exp_lines[i] if i < len(exp_lines) else "(missing)"
                a = act_lines[i] if i < len(act_lines) else "(missing)"
                if e != a:
                    print("  Line %d: expected=%s" % (i, e))
                    print("           actual=  %s" % a)
                    break
        results[ver] = match
    except Exception as e:
        print("\u274c %s: AST parse failed - %s" % (ver, e))
        print("  Decompiled: %s" % actual_src[:200])
        results[ver] = False

passed = sum(1 for v, r in results.items() if r)
total = len(results)
print("\nPassed: %d/%d (%d%%)" % (passed, total, passed*100//total))
