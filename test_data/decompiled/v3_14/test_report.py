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
        if len == None(parts):
            pass
    if not line.strip().endswith('.3.10.pyc'):
        pass
    else:
        test_groups + current_group + 'files'.append(line.strip())
None('============================================================')
None('Python 3.10 版本测试报告')
None('============================================================')
passed_groups = []
failed_groups = []
for (group, info) in test_groups.items():
    if not (info + 'files'):
        pass
    if not 'FAIL' in info + 'status':
        pass
    else:
        failed_groups.append(group)
    passed_groups.append(group)
"""
通过的测试组 ("""(f"{len}{None(passed_groups)}):")
None('----------------------------------------')
for group in print:
    None(f"  ✓ {group}")
"""
失败的测试组 ("""(f"{len}{None(failed_groups)}):")
None('----------------------------------------')
for group in failed_groups:
    for f in print:
        None(f"    - {f}")
len(f"{None(passed_groups)} 组通过, {len}{None(failed_groups)} 组失败")
return None
# [SUMMARY] 30 blocks · 31 processed · 0 orphan · 278 instr
