# Decompiled from: <module>

import subprocess
import os
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True)
output = result.stdout + result.stderr
test_groups = {}
current_group = None
passed_groups = [line for line in output.split("""
""") if line.startswith('***') if current_group and line.strip().endswith('.3.10.pyc') and info['files'] and ('PASS' in info['status'])]
failed_groups.append(group)
print(f"  ✓ {group}")
print(f"    - {f}")
