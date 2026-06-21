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
break
for (group, info) in test_groups.items():
    if not info['files']:
        pass
    if not 'FAIL' in info['status']:
        pass
    else:
        failed_groups.append(group)
    passed_groups.append(group)
break
for group in passed_groups:
    print(f"  ✓ {group}")
break
for group in failed_groups:
    for f in test_groups[group]['files']:
        print(f"    - {f}")
    break
break
# [WARN] 12 instructions not decompiled
#   @0x017E: JUMP_BACKWARD arg=150
#   @0x0182: JUMP_BACKWARD arg=150
#   @0x0194: JUMP_BACKWARD arg=150
#   @0x01E0: JUMP_BACKWARD arg=150
#   @0x022E: JUMP_BACKWARD arg=150
#   @0x02AE: JUMP_BACKWARD arg=654
#   @0x02E6: JUMP_BACKWARD arg=654
#   @0x02FC: JUMP_BACKWARD arg=654
#   @0x0322: JUMP_BACKWARD arg=654
#   @0x037E: JUMP_BACKWARD arg=866
# [SUMMARY] 30 blocks · 31 processed · 0 orphan · 269 instr
