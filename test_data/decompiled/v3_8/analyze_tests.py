# Decompiled from: <module>

import re
from collections import defaultdict
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
while i < len(lines):
    line = lines[i]
    if ('***' in line) and (':' in line):
        match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
        if match:
            test_name = match.group(1)
            status = match.group(2)
            j = i + 1
    i += 1
    while j < len(lines):
        if j < i + 30:
            next_line = lines[j]
            if next_line.startswith('***'):
                pass
        if next_line.strip().startswith(' ') and ('.pyc' in next_line):
            version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
            if version_match:
                version = version_match.group(1)
                if (version in ('3.7', '3.8', '3.9', '3.10')) and (status == 'PASS'):
                    pass
        j += 1
        version_stats[version]['failed'] + 1
print('======================================================================')
print('Python 3.7-3.10 版本测试通过率统计')
print('======================================================================')
'<10'(f" 失败{'<10'} 总计{'<10'} 通过率{'<12'}")
print('----------------------------------------------------------------------')
total_passed = 0
total_failed = 0
total = 0
sorted(version_stats.keys())
'通过'
' '
'<12'
'版本'
print
for version in ' ':
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
print('----------------------------------------------------------------------')
if total > 0:
    pass
# orphan @0x0282
0
# orphan @0x0284
'<10'(f" {total_failed}{'<10'} {total}{'<10'} {overall_rate}{'>8.1f'}%")
print('======================================================================')
return None
# [SUMMARY] 29 blocks · 27 processed · 2 orphan · 338 instr
