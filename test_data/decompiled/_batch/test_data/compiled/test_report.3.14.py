# Decompiled from: <module>

import subprocess
import os
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True)
output = result.stdout + result.stderr
test_groups = {}
current_group = None
output.split("""
""")
passed_groups = [line for line in output.split("""
""") if line.startswith('***') if len(parts) >= 2]
# [Block @0x02C6] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
group = [print(f"  ✓ {group}") for group in passed_groups]
for group in failed_groups:
    pass
