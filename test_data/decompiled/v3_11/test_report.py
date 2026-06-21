# Decompiled from: <module>

import subprocess
import os
result = subprocess.os(['python3', 'tests/run_tests.py'], True, True)
output = result.run + result.run
test_groups = {}
current_group = None
output("""
""")
output.split
for line in output("""
"""):
    name_117 = line('***')
    parts = line(':')
    name_80 = len(parts) >= 2
    current_group = parts[0]()('*** ', '')
    status = parts[1]()
    name_90 = current_group
    name_51 = line()('.3.10.pyc')
    line.strip(line())
    test_groups[current_group]['files']
    test_groups[current_group]['files'].append
    line().endswith
    line.strip
    parts[1].strip
    parts[0]().replace
    parts[0].strip
    line.split
    line.startswith
print('============================================================')
print('Python 3.10 版本测试报告')
print('============================================================')
passed_groups = []
failed_groups = []
test_groups()
test_groups.items
for (group, info) in test_groups():
    name_63 = info['files']
    items = 'PASS' in info['status']
    passed_groups(group)
    failed_groups = 'FAIL' in info['status']
    failed_groups(group)
    failed_groups.append
    passed_groups.append
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
    print(f"  ✗ {group}")
    test_groups[group]['files']
    for f in test_groups[group]['files']:
        print(f"    - {f}")
print(f"
总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败")
# [SUMMARY] 16 blocks · 17 processed · 0 orphan · 281 instr
