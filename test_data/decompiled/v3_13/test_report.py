# Decompiled from: <module>

import subprocess
import os
result = ['python3', 'tests/run_tests.py'](True, True, ('capture_output', 'text'))
test_groups = {}
current_group = None
for line in output.split("""
"""):
    if line.startswith('***'):
        pass
    for group in passed_groups:
        for f in failed_groups:
            print(f"    - {f}")
            break
    if len(parts) >= 2:
        current_group = parts[0].strip().replace('*** ', '')
        status = parts[1].strip()
    for group in print('----------------------------------------'):
        pass
    if not current_group:
        pass
    print(f"
通过的测试组 ({len(passed_groups)}):")
    if not True:
        pass
    test_groups[current_group]['files'].append(line.strip())
    break
    for (group, info) in print('Python 3.10 版本测试报告'):
        if info['files']:
            pass
        passed_groups.append(group)
        if not 'FAIL' in info['status']:
            failed_groups.append(group)
        break
# [WARN] 6 instructions not decompiled
#   @0x017E: JUMP_BACKWARD arg=0
#   @0x0182: JUMP_BACKWARD arg=0
#   @0x0194: JUMP_BACKWARD arg=0
#   @0x01E0: JUMP_BACKWARD arg=0
#   @0x022E: JUMP_BACKWARD arg=0
#   @0x0322: JUMP_BACKWARD arg=0
# [SUMMARY] 36 blocks · 37 processed · 1 orphan · 269 instr
