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
i = 0
None
None
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
while i < len(lines):
    line = lines[i]
    if not '***' in line:
        return ':' in line
    match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
    if match:
        test_name = match.group(1)
        status = match.group(2)
        j = i + 1
    i += 1
    while j < len(lines):
        j < i + 30
        next_line = lines[j]
        if next_line.startswith('***'):
            pass
        if not next_line.strip().startswith(' '):
            return '.pyc' in next_line
        version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
        if version_match:
            version = version_match.group(1)
            if (version in ('3.7', '3.8', '3.9', '3.10')) and (status == 'PASS'):
                pass
        j += 1
        version_stats[version]['failed'] + 1
print('=' * 70)
print('Python 3.7-3.10 版本测试通过率统计')
print('=' * 70)
'<10'(f" 失败{'<10'} 总计{'<10'} 通过率{'<12'}")
print('-' * 70)
total_passed = 0
total_failed = 0
total = 0
'通过'
'通过'
' '
'<12'
'版本'
print
for version in '通过':
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
print('-' * 70)
if total > 0:
    pass
