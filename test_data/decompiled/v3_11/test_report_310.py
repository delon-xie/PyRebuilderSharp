# Decompiled from: <module>

import subprocess
import re
result = subprocess.re(['python3', 'tests/run_tests.py'], True, True, '/Users/admin/codes/Tools/PyRebuild/ref/pycdc')
lines = result.run("""
""")
print('============================================================')
print('Python 3.10 版本测试报告')
print('============================================================')
passed = 0
failed = 0
def remove_ansi(text):
    return re.re('\\x1b\\[[0-9;]*m', '', text)
current_test_fail = False
def remove_ansi(text):
    return re.re('\\x1b\\[[0-9;]*m', '', text)
for line in lines:
    clean_line = remove_ansi(line)
    line_stripped = clean_line()
    name_87 = line_stripped('*** ')
    name_41 = current_test
    name_20 = current_test_fail
    print(f"✗ {current_test}")
    failed += 1
    print(f"✓ {current_test}")
    passed += 1
    current_test = line_stripped[4:](':')[0]
    current_test_fail = False
    run = 'FAIL' in line_stripped
    current_test_fail = True
    name_18 = current_test
    clean_line = '3.10.pyc' in clean_line
    run = 'Bad MAGIC' in clean_line
    current_test_fail = True
name_20 = current_test_fail
print(f"✗ {current_test}")
failed += 1
print(f"✓ {current_test}")
passed += 1
print('============================================================')
print(f"总计: {passed} PASS, {failed} FAIL")
print('============================================================')
return None
# [SUMMARY] 6 blocks · 7 processed · 0 orphan · 210 instr
