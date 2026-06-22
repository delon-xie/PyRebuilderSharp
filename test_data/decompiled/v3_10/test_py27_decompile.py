# Decompiled from: <module>

with open(INPUT_PY) as f:
    content = f.read()
    raise
    outc = os.path.join(OUTPUT_DIR, '{}.2.7.pyc'.format(BASENAME))
    result = subprocess.run([PY27, '-c', """import py_compile, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    py_compile.compile(src, cfile=dst, doraise=True)
    print('OK')
except Exception as e:
    print('FAIL:' + str(e))""", INPUT_PY, outc], capture_output=True, text=True, timeout=30)
    print('2.7 compile:', result.stdout + result.stderr.strip())
    OUT_DIR = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData')
    result2 = subprocess.run(['dotnet', 'run', '--project', os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', 'decompile', outc, '--output-dir', '/tmp/py27_test'], capture_output=True, text=True, timeout=60)
    if len(result2.stdout) > 500:
        pass
    else:
        result2.stdout
        if len(result2.stderr) > 500:
            return None
# [SUMMARY] 9 blocks · 10 processed · 0 orphan · 166 instr
