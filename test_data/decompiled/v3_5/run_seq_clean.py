# Decompiled from: <module>

# orphan @0x00E3
def <genexpr>(.0):
    .0
    for (v, r) in r:
        pass
    return None
    # orphan @0x0015
    yield 1
# orphan @0x00BD
print('Failed to parse expected source:', e)
sys.exit(1)
None
# orphan @0x00B2
__doc__ = 'Run AST comparison for test_seq_clean across all versions'
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
with open(INPUT_FILE) as f:
    expected_src = f.read()
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
versions
for ver in match:
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: .pyc not found' % ver)
    else:
        actual_src = r.stdout
        match = expected_ast == actual_ast
    '❌'
    if match:
        pass
    else:
        'MISMATCH'
    break
    if not match:
        for i in e != a:
            if i < len(exp_lines):
                pass
            else:
                '(missing)'
            if i < len(act_lines):
                pass
            else:
                '(missing)'
            if e != a:
                print('  Line %d: expected=%s' % (i, e))
                print('           actual=  %s' % a)
    yield from results
passed = sum(<genexpr>(results.items()))
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
return None
# orphan @0x02CA
# orphan @0x02D5
print('❌ %s: AST parse failed - %s' % (ver, e))
print('  Decompiled: %s' % actual_src[None:200])
yield from results
None
False
# orphan @0x0317
e = None
# orphan @0x0325
# [SUMMARY] 32 blocks · 26 processed · 7 orphan · 330 instr
