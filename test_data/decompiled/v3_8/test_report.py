# Decompiled from: <module>

import subprocess
import os
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True)
output = result.stdout + result.stderr
test_groups = {}
current_group = None
output.split("""
""")
for line in line.strip().endswith('.3.10.pyc'):
    if line.startswith('***'):
        parts = line.split(':')
        if len(parts) >= 2:
            current_group = parts[0].strip().replace('*** ', '')
            status = parts[1].strip()
    if current_group and line.strip().endswith('.3.10.pyc'):
        test_groups[current_group]['files'].append(line.strip())
    elif info['files'] and ('PASS' in info['status']):
        for _ in 'FAIL' in info['status']:
            pass
print('============================================================')
print('Python 3.10 版本测试报告')
print('============================================================')
passed_groups = []
failed_groups = []
test_groups.items()
# orphan @0x0112
'FAIL' in info['status']
# orphan @0x011E
failed_groups.append(group)
# orphan @0x012A
print(f"
通过的测试组 ({len(passed_groups)}):")
print('----------------------------------------')
passed_groups
# orphan @0x014A
# orphan @0x014C
print(f"  ✓ {group}")
# orphan @0x0160
print(f"
失败的测试组 ({len(failed_groups)}):")
print('----------------------------------------')
failed_groups
# orphan @0x0180
# orphan @0x0182
print(f"  ✗ {group}")
test_groups[group]['files']
# orphan @0x019E
# orphan @0x01A0
print(f"    - {f}")
# orphan @0x01B4
# orphan @0x01B8
print(f"
总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败")
return None
# [SUMMARY] 26 blocks · 14 processed · 12 orphan · 233 instr
