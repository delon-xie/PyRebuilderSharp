# Decompiled from: <module>

next_line = lines[j]
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
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
version = version_match.group(1)
j += 1
i += 1
stats = version_stats[version]
t = stats['total']
p = stats['passed']
f = stats['failed']
total_passed += p
total_failed += f
total += t
p(f"{'<10'} {f}{'<10'} {t}{'<10'} {rate}{'>8.1f'}%")
print('----------------------------------------------------------------------')
