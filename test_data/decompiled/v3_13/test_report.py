# Decompiled from: <module>

# orphan @0x014C
current_group
# orphan @0x0102
current_group = parts[0].strip().replace('*** ', '')
1
parts
# orphan @0x00EE
# orphan @0x00EA
None
len
# orphan @0x00C8
parts = line.split(':')
# orphan @0x009A
line.startswith('***')
# orphan @0x0096
# orphan @0x0070
current_group = None
output.split("""
""")
# orphan @0x005A
test_groups = {}
# orphan @0x0052
# orphan @0x0022
result = ['python3', 'tests/run_tests.py'](True, True, ('capture_output', 'text'))
result
result.stdout
import subprocess
import os
subprocess.run
# orphan @0x0194
line
# orphan @0x019A
# orphan @0x01E0
test_groups[current_group]['files'].append(line.strip())
print('============================================================')
'Python 3.10 版本测试报告'
None
print
# orphan @0x024C
print('============================================================')
passed_groups = []
failed_groups = []
test_groups.items
# orphan @0x0282
# orphan @0x0292
info['files']
# orphan @0x02AE
'PASS' in info['status']
# orphan @0x02C4
passed_groups.append
# orphan @0x02CC
'FAIL' in info['status']
# orphan @0x02FC
failed_groups.append(group)
# orphan @0x032A
print(f"
通过的测试组 ({len(passed_groups)}):")
print('----------------------------------------')
passed_groups
# orphan @0x0366
print(f"  ✓ {group}")
print(f"
失败的测试组 ({len(failed_groups)}):")
print('----------------------------------------')
failed_groups
# orphan @0x03C2
print(f"  ✗ {group}")
test_groups[group]['files']
# orphan @0x03EE
print(f"    - {f}")
print(f"
总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败")
# [SUMMARY] 35 blocks · 11 processed · 33 orphan · 269 instr
