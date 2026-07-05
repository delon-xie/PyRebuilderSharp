# Decompiled from: <module>

import subprocess
import re
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True, cwd='/Users/admin/codes/Tools/PyRebuild/ref/pycdc')
lines = result.stdout.split("""
""")
print('============================================================')
print('Python 3.10 版本测试报告')
print('============================================================')
passed = failed = 0
current_test = None
current_test_fail = False

def remove_ansi(text):
    return re.sub('\\x1b\\[[0-9;]*m', '', text)
lines
for line in lines:
    clean_line = remove_ansi(line)
    line_stripped = clean_line.strip()
    if line_stripped.startswith('*** '):
        pass
        if current_test:
            pass
            if current_test_fail:
                print(f"✗ {current_test}")
                failed += 1
    pass
    if current_test:
        pass
        if '3.10.pyc' in clean_line:
            pass
            if 'FAIL' in clean_line:
                pass
                if 'Unsupported' in clean_line:
                    pass
                    if 'Bad MAGIC' in clean_line:
                        current_test_fail = True
    current_test = line_stripped[4:].split(':')[0]
    current_test_fail = False
    if 'FAIL' in line_stripped:
        current_test_fail = True
    pass
    print(f"✓ {current_test}")
    passed += 1
print(f"✗ {current_test}")
failed += 1
