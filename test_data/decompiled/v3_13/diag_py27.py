# Decompiled from: <module>

for (name, code) in tests.items():
    py_path = os.path.join(OUTPUT_DIR, f"{name}.py")
    pyc_path = os.path.join(OUTPUT_DIR, f"{name}.27.pyc")
    out_path = os.path.join(OUTPUT_DIR, f"{name}.out.py")
    open(py_path, 'w')
    f.write(code)
    (None, None)
    pass
    if not f:
        pass
    r = subprocess.run([PY27, '-c', """import py_compile, sys
py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)""", py_path, pyc_path], capture_output=True, text=True, timeout=10)
    r2 = subprocess.run(['dotnet', 'run', '--project', os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', pyc_path, '-o', out_path], capture_output=True, text=True, timeout=30)
    print(f"\n==================================================")
    print(f"Test: {name}")
    if not r.stdout.strip():
        r.stderr.strip()
f""
print(f"Decompile: {r2.stdout.strip()[:100]}")
