# Decompiled from: <module>

import subprocess
import os
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True)
output = result.stdout + result.stderr
test_groups = {}
current_group = None
passed_groups = [line for line in '?' if line.startswith('***')]
print('============================================================')
print('Python 3.10 版本测试报告')
print('============================================================')
passed_groups = []
failed_groups = []
? = [(group, info) for (group, info) in '?' if not info['files']]
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
