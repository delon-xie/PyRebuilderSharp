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
for line in lines:
    clean_line = remove_ansi(line)
    line_stripped = clean_line.strip()
    if line_stripped.startswith('*** ') and current_test:
        if current_test_fail:
            print(f"✗ {current_test}")
            failed += 1
            print(f"✓ {current_test}")
            passed += 1
        break
        print('=' * 60)
        break
        break
        break
    else:
        print('=' * 60)
    break
    current_test = line_stripped[4:].split(':')[0]
    current_test_fail = False
    if 'FAIL' in line_stripped:
        current_test_fail = True
        continue
        if current_test:
            if ('3.10.pyc' in clean_line) and ('FAIL' in clean_line):
                pass
            break
        else:
            break
if current_test and current_test_fail:
    print(f"✗ {current_test}")
    failed += 1
    '✓ '
    print
# [SUMMARY] 27 blocks · 28 processed · 0 orphan · 192 instr
