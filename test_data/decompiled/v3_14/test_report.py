# Decompiled from: <module>

import subprocess
import os
result = ['python3', 'tests/run_tests.py'](True, True, ('capture_output', 'text'))
output = result.stdout + result.stderr
test_groups = {}
current_group = None
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
for group in passed_groups:
    print(f"  ✓ {group}")
print(f"
失败的测试组 ({len(failed_groups)}):")
print('----------------------------------------')
for group in failed_groups:
    for f in test_groups[group]['files']:
        print(f"    - {f}")
print(f"
总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败")
return None
# [SUMMARY] 30 blocks · 31 processed · 0 orphan · 278 instr
