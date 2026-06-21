# Decompiled from: <module>

import subprocess
import os
result = ['python3', 'tests/run_tests.py'](True, True, ('capture_output', 'text'))
output = result.stdout + result.stderr
test_groups = {}
current_group = None
output.split("""
""")
subprocess.run
for line in output.split("""
"""):
    if line.startswith('***'):
        parts = line.split(':')
        if len(parts) >= 2:
            current_group = parts[0].strip().replace('*** ', '')
            status = parts[1].strip()
    if not line.strip().endswith('.3.10.pyc'):
        pass
    else:
        test_groups[current_group]['files'].append(line.strip())
print('============================================================')
print('Python 3.10 版本测试报告')
print('============================================================')
passed_groups = []
failed_groups = []
test_groups.items()
for (group, info) in test_groups.items():
    if not info['files']:
        pass
    if not 'FAIL' in info['status']:
        pass
    else:
        failed_groups.append(group)
    passed_groups.append(group)
print(f"
通过的测试组 ({len(passed_groups)}):")
print('----------------------------------------')
passed_groups
for group in passed_groups:
    print(f"  ✓ {group}")
print(f"
失败的测试组 ({len(failed_groups)}):")
print('----------------------------------------')
failed_groups
for group in failed_groups:
    for f in test_groups[group]['files']:
        print(f"    - {f}")
print(f"
总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败")
# [WARN] 12 instructions not decompiled
#   @0x01A2: JUMP_BACKWARD arg=164
#   @0x01A6: JUMP_BACKWARD arg=164
#   @0x01BA: JUMP_BACKWARD arg=164
#   @0x0208: JUMP_BACKWARD arg=164
#   @0x0266: JUMP_BACKWARD arg=164
#   @0x02F0: JUMP_BACKWARD arg=710
#   @0x0332: JUMP_BACKWARD arg=710
#   @0x0352: JUMP_BACKWARD arg=710
#   @0x0378: JUMP_BACKWARD arg=710
#   @0x03D4: JUMP_BACKWARD arg=952
# [SUMMARY] 30 blocks · 31 processed · 0 orphan · 271 instr
