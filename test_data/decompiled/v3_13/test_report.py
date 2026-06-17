# Decompiled from: <module>

# orphan @0x0102
current_group = parts[0].strip().replace('*** ', '')
status = parts[1].strip()
# orphan @0x00C8
parts = line.split(':')
# orphan @0x009A
# orphan @0x0000
import subprocess
import os
result = ['python3', 'tests/run_tests.py'](True, True, ('capture_output', 'text'))
output = result.stdout + result.stderr
test_groups = {}
current_group = None
# orphan @0x0194
# orphan @0x01E0
test_groups[current_group]['files'].append(line.strip())
print('============================================================')
print('Python 3.10 版本测试报告')
print('============================================================')
passed_groups = []
failed_groups = []
# orphan @0x0292
# orphan @0x02AE
# orphan @0x02C4
passed_groups.append(group)
# orphan @0x02FC
failed_groups.append(group)
# orphan @0x032A
print(f"
通过的测试组 ({len(passed_groups)}):")
# orphan @0x0358
# orphan @0x0366
# orphan @0x0368
print(f"  ✓ {group}")
print(f"
失败的测试组 ({len(failed_groups)}):")
print('----------------------------------------')
# orphan @0x03C2
print(f"  ✗ {group}")
# orphan @0x03EE
print(f"    - {f}")
print(f"
总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败")
return None
# [SUMMARY] 36 blocks · 21 processed · 35 orphan · 269 instr
