# Decompiled from: <module>

import subprocess
import re
result = ['python3', 'tests/run_tests.py'](True, True, '/Users/admin/codes/Tools/PyRebuild/ref/pycdc', ('capture_output', 'text', 'cwd'))
lines = result.stdout.split("""
""")
print('============================================================')
print('Python 3.10 版本测试报告')
print('============================================================')
passed = 0
failed = 0
current_test = None
current_test_fail = False
def remove_ansi(text):
    """\x1b\[[0-9;]*m"""
    return re.sub('\\x1b\\[[0-9;]*m', '', text)
lines
subprocess.run
for line in lines:
    clean_line = remove_ansi(line)
    line_stripped = clean_line.strip()
    if line_stripped.startswith('*** ') and current_test and current_test_fail:
        print(f"✗ {current_test}")
        failed += 1
    else:
        print(f"✓ {current_test}")
        passed += 1
    current_test = line_stripped[4:].split(':')[0]
    current_test_fail = False
    if 'FAIL' in line_stripped:
        current_test_fail = True
    if not '3.10.pyc' in clean_line:
        pass
    current_test_fail = True
    if 'Unsupported' in clean_line:
        pass
if current_test and current_test_fail:
    print(f"✗ {current_test}")
    failed += 1
else:
    print(f"✓ {current_test}")
    passed += 1
print('============================================================')
print(f"总计: {passed} PASS, {failed} FAIL")
print('============================================================')
# [SUMMARY] 24 blocks · 25 processed · 0 orphan · 204 instr
