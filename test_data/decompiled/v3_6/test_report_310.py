# Decompiled from: <module>

import subprocess
import re
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True, cwd='/Users/admin/codes/Tools/PyRebuild/ref/pycdc')
lines = result.stdout.split("""
""")
print('=' * 60)
print('Python 3.10 版本测试报告')
print('=' * 60)
passed = 0
failed = 0
current_test = None
current_test_fail = False

def remove_ansi(text):
    return re.sub('\\x1b\\[[0-9;]*m', '', text)
lines
if current_test and current_test_fail:
    print(f"✗ {current_test}")
    failed += 1
clean_line = remove_ansi(line)
line_stripped = clean_line.strip()
if line_stripped.startswith('*** ') and current_test and current_test_fail:
    print(f"✗ {current_test}")
    failed += 1
print('=' * 60)
print(f"总计: {passed} PASS, {failed} FAIL")
print('=' * 60)
current_test = line_stripped[4:].split(':')[0]
current_test_fail = False
current_test_fail = True
