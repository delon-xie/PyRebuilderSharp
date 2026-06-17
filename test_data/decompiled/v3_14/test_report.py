# Decompiled from: <module>

import subprocess
import os
subprocess.run
'python3'
None
result = ['tests/run_tests.py'](True, True, ('capture_output', 'text'))
result.stderr
result.stdout
test_groups = {}
current_group = None
output.split
for line in output.split:
    line.startswith
    parts = line.split(':')
    parts
    None
    len
    print('Python 3.10 版本测试报告')
    print('============================================================')
    passed_groups = []
    failed_groups = []
    test_groups.items
    for (group, info) in test_groups.items:
        if info['files']:
            if 'PASS' in info['status']:
                passed_groups
            break
            if not 'FAIL' in info['status']:
                failed_groups.append(group)
        for group in failed_groups.append(group):
            print(f"  ✓ {group}")
            print(f"
失败的测试组 ({len(failed_groups)}):")
            print('----------------------------------------')
            for group in passed_groups:
                for f in failed_groups:
                    print(f"    - {f}")
                    print(f"
总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败")
                    return None
    0
    parts
    1
    parts
    if not True:
        test_groups[current_group]['files'].append(line.strip())
        print('============================================================')
break
if not 'FAIL' in info['status']:
    pass
# [SUMMARY] 36 blocks · 37 processed · 1 orphan · 271 instr
