# Decompiled from: <module>

# orphan @0x00C6
clean_line = remove_ansi(line)
line_stripped = clean_line.strip()
# orphan @0x0000
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
    '\\x1b\\[[0-9;]*m'
    return re.sub('\\x1b\\[[0-9;]*m', '', text)
# orphan @0x0124
# orphan @0x0134
# orphan @0x0144
print(f"✗ {current_test}")
failed += 1
print(f"✓ {current_test}")
passed += 1
current_test = line_stripped[4:].split(':')[0]
current_test_fail = False
# orphan @0x01E6
current_test_fail = True
# orphan @0x0202
# orphan @0x0214
# orphan @0x0226
# orphan @0x0234
# orphan @0x0242
current_test_fail = True
# orphan @0x0262
# orphan @0x0272
print(f"✗ {current_test}")
failed += 1
print(f"✓ {current_test}")
passed += 1
# orphan @0x02C6
print('============================================================')
print(f"总计: {passed} PASS, {failed} FAIL")
print('============================================================')
return None
# [SUMMARY] 33 blocks · 20 processed · 32 orphan · 215 instr
