# Decompiled from: <module>

# orphan @0x00BC
# orphan @0x00B1
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
for ver in ver:
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        break
    else:
        actual_src = r.stdout
        try:
            match = expected_ast == actual_ast
            if match:
                pass
            else:
                '\\u274c'
            if match:
                pass
            else:
                'MISMATCH'
            if not True:
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
                        continue
            else:
                yield from results
            for ver in ver:
                pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
                if not os.path.exists(pyc):
                    break
            passed = sum(<genexpr>(results.items()))
            total = len(results)
            return
        except Exception:
            pass
passed = sum(<genexpr>(results.items()))
total = len(results)
return
# orphan @0x0298
# orphan @0x02AA
# orphan @0x02B5
ver
results
# orphan @0x02E3
# [SUMMARY] 32 blocks · 27 processed · 6 orphan · 304 instr
