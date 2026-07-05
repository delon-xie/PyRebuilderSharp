# Decompiled from: <module>

match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
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
None
None
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
if i < len(lines):
    line = lines[i]
    if not '***' in line:
next_line = lines[j]
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
j += 1
debug_count += 1
# [Block @0x0160] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
print(f"  Found version: {v} in: {line_text}")
i += 1
