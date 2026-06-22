# Decompiled from: <module>

with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as f:
    f.write(src)
    py_path = f.name
    py_compile.compile(py_path, cfile=py_path + 'c', doraise=True)
    print('Compiled OK')
    r = subprocess.run(['dotnet', 'run', '--project', 'src/PyRebuilderSharp.Cli', py_path + 'c'], capture_output=True, text=True, cwd='/Users/admin/codes/Tools/PyRebuilderSharp')
    print('=== Decompiled ===')
    print(r.stdout.strip())
    os.unlink(py_path)
    os.unlink(py_path + 'c')
    return None
