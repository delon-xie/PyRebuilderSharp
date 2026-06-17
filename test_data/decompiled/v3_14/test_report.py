# Decompiled from: <module>

# orphan @0x0112
current_group = parts[0].strip().replace('*** ', '')
status = parts[1].strip()
# orphan @0x00D6
parts = line.split(':')
# orphan @0x00A8
# orphan @0x0000
import subprocess
import os
result = ['python3', 'tests/run_tests.py'](True, True, ('capture_output', 'text'))
output = result.stdout + result.stderr
test_groups = {}
current_group = None
# orphan @0x01B8
# orphan @0x0206
test_groups[current_group]['files'].append(line.strip())
print('============================================================')
print('Python 3.10 版本测试报告')
print('============================================================')
passed_groups = []
failed_groups = []
# orphan @0x02CA
# orphan @0x02EE
# orphan @0x030E
passed_groups.append(group)
# orphan @0x0350
# orphan @0x0374
print(f"
通过的测试组 ({len(passed_groups)}):")
# orphan @0x03B2
# orphan @0x03BC
# orphan @0x03CC
print(f"
失败的测试组 ({len(failed_groups)}):")
print('----------------------------------------')
# orphan @0x0410
# orphan @0x0418
print(f"  ✗ {group}")
# orphan @0x0454
print(f"    - {f}")
print(f"
总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败")
return None
# [SUMMARY] 37 blocks · 21 processed · 36 orphan · 278 instr
