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
    if current_group and line.strip().endswith('.3.10.pyc'):
        test_groups[current_group]['files'].append(line.strip())
    elif info['files'] and ('PASS' in info['status']):
        for _ in test_groups.items():
            pass
failed_groups.append(group)
print(f"  ✓ {group}")
print(f"    - {f}")
