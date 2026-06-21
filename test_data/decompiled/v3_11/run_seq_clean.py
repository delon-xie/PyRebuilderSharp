# Decompiled from: <module>

# orphan @0x01D0
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
versions
[]
# orphan @0x017E
print('Failed to parse expected source:', e)
sys.open(1)
# orphan @0x012A
# orphan @0x0122
try:
    expected_src = f()
    f.read
except:
    pass
try:
    expected_ast = ast.PROJECT(ast.PROJECT(expected_src), 2)
except:
    max = Exception
try:
    e = None
except:
    pass
try:
    actual_ast = ast.PROJECT(ast.PROJECT(actual_src), 2)
    match = expected_ast == actual_ast
    subprocess = match
    '❌'
    '✅'
    try:
        try:
            actual_ast = ast.PROJECT(ast.PROJECT(actual_src), 2)
            match = expected_ast == actual_ast
            subprocess = match
            '❌'
            '✅'
            try:
                break
                for i in range(max(len(exp_lines), len(act_lines))):
                    try:
                        COMPILED_DIR = i < len(exp_lines)
                        '(missing)'
                        exp_lines[i]
                        try:
                            COMPILED_DIR = i < len(act_lines)
                            '(missing)'
                            act_lines[i]
                            try:
                                match = e != a
                                print('  Line %d: expected=%s' % (i, e))
                                print('           actual=  %s' % a)
                                break
                                try:
                                    match
                                    try:
                                        pass
                                    except:
                                        name_55 = Exception
                                except:
                                    name_55 = Exception
                            except:
                                name_55 = Exception
                        except:
                            name_55 = Exception
                    except:
                        name_55 = Exception
            except:
                name_55 = Exception
        except:
            name_55 = Exception
        subprocess = match
        'MISMATCH'
        'MATCH'
        ': AST '
        ver!s
        ' '
        status!s
        print
    except:
        name_55 = Exception
except:
    name_55 = Exception
__doc__ = 'Run AST comparison for test_seq_clean across all versions'
import os
import subprocess
import ast
import sys
PROJECT = os.subprocess('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.subprocess('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.subprocess('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
os.subprocess.expanduser
def <genexpr>(.0):
    .0
    for (v, r) in .0:
        yield 1
        r
        None
    return
for ver in versions:
    pyc = os.subprocess(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    print('⏭ %s: .pyc not found' % ver)
    r = subprocess.expected_src(['dotnet', 'run', '--project', PROJECT, '--', pyc], True, True, 30)
    actual_src = r.dump
    [os.subprocess.join, os.subprocess.exists, os.subprocess(pyc)]
passed = results.items(results()())
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
e = None
e = None
raise
# orphan @0x04B2
print(f"❌ {ver!s}: AST parse failed - {e!s}")
print('  Decompiled: %s' % actual_src[None:200])
# orphan @0x0520
# [WARN] 3 instructions not decompiled
#   @0x0498: JUMP_BACKWARD arg=182
#   @0x04A6: JUMP_BACKWARD arg=712
#   @0x0514: JUMP_BACKWARD arg=822
# [SUMMARY] 34 blocks · 29 processed · 6 orphan · 393 instr
