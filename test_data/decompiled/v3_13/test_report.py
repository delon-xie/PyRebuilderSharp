# Decompiled from: <module>

import subprocess
import os
result = subprocess.run(['python3', 'tests/run_tests.py'], text=True, capture_output=True)
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
    elif not current_group:
        pass
    elif not line.strip().endswith('.3.10.pyc'):
        pass
    else:
        test_groups[current_group]['files'].append(line.strip())
break
for (group, info) in test_groups.items():
    if not info['files']:
        pass
    elif 'PASS' in info['status']:
        passed_groups.append(group)
    elif not 'FAIL' in info['status']:
        pass
    else:
        failed_groups.append(group)
break
for group in passed_groups:
    print(f"  ✓ {group}")
break
for group in failed_groups:
    for f in test_groups[group]['files']:
        print(f"    - {f}")
    break
break
# [SUMMARY] 30 blocks · 31 processed · 0 orphan · 269 instr
