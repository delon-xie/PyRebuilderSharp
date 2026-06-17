# Decompiled from: <module>

# orphan @0x00C0
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
    return re.sub('\\x1b\\[[0-9;]*m', '', text)
# orphan @0x011E
# orphan @0x012C
# orphan @0x013A
print(f"✗ {current_test}")
failed += 1
print(f"✓ {current_test}")
passed += 1
current_test = line_stripped[4:].split(':')[0]
current_test_fail = False
# orphan @0x01BA
current_test_fail = True
# orphan @0x01D4
# orphan @0x01E4
# orphan @0x01F4
# orphan @0x0200
# orphan @0x020C
current_test_fail = True
# orphan @0x022A
# orphan @0x0238
print(f"✗ {current_test}")
failed += 1
print(f"✓ {current_test}")
passed += 1
print('============================================================')
# orphan @0x029A
print('============================================================')
return None
# [SUMMARY] 32 blocks · 19 processed · 31 orphan · 204 instr
