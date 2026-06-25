# Decompiled from: <module>

match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
line = lines[i]
import re
from collections import defaultdict
f = open('/tmp/test_full.txt', 'r')
output = f.read()
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
    version_stats = defaultdict(<lambda>)
    lines = output.split("""
""")
    i = 0
    debug_count = 0
next_line = lines[j]
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
j += 1
debug_count += 1
print(f"  Found version: {v} in: {line_text}")
i += 1
