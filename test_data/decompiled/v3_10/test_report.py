# Decompiled from: <module>

import subprocess
import os
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True)
output = result.stdout + result.stderr
test_groups = {}
current_group = None
output.split("""
""")
passed_groups = {line: line for line in output.split("""
""") if line.startswith('***') if len(parts) >= 2}
passed_groups.append(group)
line = [print(f"  ✓ {group}") for group in passed_groups]
print(f"  ✓ {group}")
line = [[print(f"    - {f}") for f in test_groups[group]['files']] for group in failed_groups for group in group]
print(f"    - {f}")
