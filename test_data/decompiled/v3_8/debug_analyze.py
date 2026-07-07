# Decompiled from: <module>

import re
from collections import defaultdict
f = open('/tmp/test_full.txt', 'r')
output = f.read()

@defaultdict
def version_stats():
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output.split("""
""")
i = debug_count = 0
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
if i < len(lines):
    line = lines[i]
    if ('***' in line) and (':' in line):
        match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
        if match:
            test_name = match.group(1)
            status = match.group(2)
            j = i + 1
            found_versions = []
next_line = lines[j]
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
j += 1
debug_count += 1
print(f"  Found version: {v} in: {line_text}")
i += 1
