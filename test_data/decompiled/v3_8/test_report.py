# Decompiled from: <module>

import subprocess
import os
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True)
output = result.stdout + result.stderr
test_groups = {}
current_group = None
output.split("""
""")
print('============================================================')
print('Python 3.10 版本测试报告')
print('============================================================')
passed_groups = []
failed_groups = []
test_groups.items()
print(f"\n通过的测试组 ({len(passed_groups)}):")
print('----------------------------------------')
passed_groups
print(f"\n失败的测试组 ({len(failed_groups)}):")
print('----------------------------------------')
failed_groups
print(f"\n总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败")
print(f"  ✗ {group}")
test_groups[group]['files']
print(f"    - {f}")
print(f"  ✓ {group}")
if info['files'] and ('PASS' in info['status']):
    passed_groups.append(group)
if line.startswith('***'):
    parts = line.split(':')
    if len(parts) >= 2:
        current_group = parts[0].strip().replace('*** ', '')
        status = parts[1].strip()
failed_groups.append(group)
