# Decompiled from: <module>

import subprocess
import os
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True)
output = result.stdout + result.stderr
test_groups = {}
current_group = None
output.split("""
""")
for line in output.split("""
"""):
    if line.startswith('***'):
        parts = line.split(':')
        if len(parts) >= 2:
            current_group = parts[0].strip().replace('*** ', '')
            status = parts[1].strip()
            continue
            if current_group and line.strip().endswith('.3.10.pyc'):
                test_groups[current_group]['files'].append(line.strip())
            test_groups.items()
            for (group, info) in test_groups.items():
                if info['files'] and ('PASS' in info['status']):
                    passed_groups.append(group)
                    info['status']
                    'FAIL'
                return
                failed_groups.append(group)
            print(f"
通过的测试组 ({len(passed_groups)}):")
            print('-' * 40)
            passed_groups
            for group in passed_groups:
                print(f"  ✓ {group}")
            print(f"
失败的测试组 ({len(failed_groups)}):")
            print('-' * 40)
            failed_groups
            for group in failed_groups:
                for f in test_groups[group]['files']:
                    print(f"    - {f}")
            print(f"
总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败")
            None
            break
print('=' * 60)
print('Python 3.10 版本测试报告')
'=' * 60
print
