#!/usr/bin/env python3
"""Run AST comparison for test_expr_basic across all versions"""
import os, subprocess, sys

PROJECT = os.path.expanduser("~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli")
COMPILED_DIR = os.path.expanduser(
    "~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled")
INPUT_FILE = os.path.expanduser(
    "~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py")

with open(INPUT_FILE) as f:
    expected_src = f.read()

try:
    import ast
    expected_ast = ast.dump(ast.parse(expected_src), indent=2)
except:
    print("Failed to parse expected source")
    sys.exit(1)

versions = ["2.7", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10"]
results = {}

for ver in versions:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if not os.path.exists(pyc):
        print(f"⏭ {ver}: .pyc not found")
        continue
    
    r = subprocess.run(
        ["dotnet", "run", "--project", PROJECT, "--", pyc],
        capture_output=True, text=True, timeout=30
    )
    actual_src = r.stdout
    
    try:
        actual_ast = ast.dump(ast.parse(actual_src), indent=2)
        match = expected_ast == actual_ast
        status = "✅" if match else "❌"
        print(f"{status} {ver}: AST {'MATCH' if match else 'MISMATCH'}")
        if not match:
            exp_lines = expected_ast.split('\n')
            act_lines = actual_ast.split('\n')
            for i in range(max(len(exp_lines), len(act_lines))):
                e = exp_lines[i] if i < len(exp_lines) else "(missing)"
                a = act_lines[i] if i < len(act_lines) else "(missing)"
                if e != a:
                    print(f"  Line {i}: expected={e}")
                    print(f"           actual=  {a}")
                    break
            results[ver] = False
        else:
            results[ver] = True
    except Exception as e:
        print(f"❌ {ver}: AST parse failed - {e}")
        print(f"  Decompiled: {actual_src[:200]}")
        results[ver] = False

print(f"\n{'='*40}")
passed = sum(1 for v, r in results.items() if r)
total = len(results)
print(f"Passed: {passed}/{total} ({passed/total*100:.0f}%)")
