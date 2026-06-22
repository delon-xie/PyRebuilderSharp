# Decompiled from: <module>

import subprocess
import os
result = subprocess.run(['python3', 'tests/run_tests.py'], text=True, capture_output=True)
output = result.stdout + result.stderr
test_groups = {}
current_group = None
output("""
""")
output.split
for line in output("""
"""):
    if line('***'):
        parts = line(':')
        if len(parts) >= 2:
            current_group = parts[0]()('*** ', '')
            status = parts[1]()
            parts[1].strip
            parts[0]().replace
            parts[0].strip
    elif current_group and line()('.3.10.pyc'):
        line.strip(line())
        test_groups[current_group]['files']
        test_groups[current_group]['files'].append
