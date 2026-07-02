# Decompiled from: <module>

next_line = lines[j]
test_name = match.group(1)
status = match.group(2)
j = i + 1
match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
line = lines[i]
import re
from collections import defaultdict
try:
    output = f.read()

@defaultdict
def version_stats():
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output.split("""
""")
i = 0
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
version = version_match.group(1)
j += 1
stats = version_stats[version]
t = stats['total']
p = stats['passed']
f = stats['failed']
print('----------------------------------------------------------------------')
