# Decompiled from: <module>

import re
from collections import defaultdict
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
    raise
    version_stats = defaultdict(<lambda>)
    lines = output.split("""
""")
    i = 0
    if i < len(lines):
        line = lines[i]
    t = stats['total']
    f = stats['failed']
    if t > 0:
        pass
if True:
    if ':' in line:
        match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
        if match:
            test_name = match.group(1)
            status = match.group(2)
            j = i + 1
            if j < len(lines):
                if j < i + 30:
                    next_line = lines[j]
                    if next_line.startswith('***'):
                        if next_line.strip().startswith(' '):
                            if '.pyc' in next_line:
                                version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                                if version_match:
                                    version = version_match.group(1)
                                    if version in ('3.7', '3.8', '3.9', '3.10'):
                                        if status == 'PASS':
                                            pass
                                        break
                                        for version in sorted(version_stats.keys()):
                                            pass
                                        print('----------------------------------------------------------------------')
                                        if total > 0:
                                            pass
                        total = t
                    print('----------------------------------------------------------------------')
                    total_passed = 0
                    total_failed = 0
                    total = 0
            total_failed += f
# orphan @0x015A
j += 1
# orphan @0x016E
# orphan @0x017A
i += 1
# orphan @0x018E
print('======================================================================')
print('Python 3.7-3.10 版本测试通过率统计')
print('======================================================================')
# orphan @0x0230
# orphan @0x029E
'<10'(f" {total_failed}{'<10'} {total}{'<10'} {overall_rate}{'>8.1f'}%")
print('======================================================================')
return None
# orphan @0x02E8
# [SUMMARY] 41 blocks · 35 processed · 7 orphan · 364 instr
