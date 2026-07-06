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
    pass
    pass
    version_stats = defaultdict(lambda: None)
    lines = output.split("""
""")
    i = 0
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
version = version_match.group(1)
j += 1
i += 1
for version in sorted(version_stats.keys()):
    stats = version_stats[version]
    t = stats['total']
    p = stats['passed']
    f = stats['failed']
    if t > 0:
        pass
    0
    total_passed += p
    total_failed += f
    total += t
    p(f"{'<10'} {f}{'<10'} {t}{'<10'} {rate}{'>8.1f'}%")
stats = version_stats[version]
t = stats['total']
p = stats['passed']
f = stats['failed']
total_passed += p
total_failed += f
total += t
p(f"{'<10'} {f}{'<10'} {t}{'<10'} {rate}{'>8.1f'}%")
print('----------------------------------------------------------------------')
