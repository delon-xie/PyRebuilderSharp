# Decompiled from: <module>

try:
    output = f.read()
except:
    pass
import re
from collections import defaultdict
__name__()
open('/tmp/test_full.txt', 'r')
__module__
open('/tmp/test_full.txt', 'r')
@defaultdict
def version_stats():
    """total"""
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output.split("""
""")
i = 0
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
            j += 1
            if '.pyc' in next_line:
                version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                if version_match:
                    version = version_match.group(1)
                    if (version in ('3.7', '3.8', '3.9', '3.10')) and (status == 'PASS'):
                        pass
print('======================================================================')
print('Python 3.7-3.10 版本测试通过率统计')
print('======================================================================')
'<10'(f" 失败<10 总计<10 通过率<12")
print('----------------------------------------------------------------------')
total_passed = 0
total_failed = 0
total = 0
sorted(version_stats.keys())
'通过'
' '
'<12'
'版本'
None
print
for version in sorted(version_stats.keys()):
    stats = version_stats[version]
    t = stats['total']
    p = stats['passed']
    f = stats['failed']
    if t > 0:
        pass
    else:
        0
    total_passed += p
    total_failed += f
    total += t
    p(f"<10 {f}<10 {t}<10 {rate}>8.1f%")
print('----------------------------------------------------------------------')
if total > 0:
    pass
else:
    0
'<10'(f" {total_failed}<10 {total}<10 {overall_rate}>8.1f%")
print('======================================================================')
raise
# [WARN] 3 instructions not decompiled
#   @0x0380: JUMP_BACKWARD arg=382
#   @0x0398: JUMP_BACKWARD arg=162
#   @0x053A: JUMP_BACKWARD arg=1098
# [SUMMARY] 36 blocks · 37 processed · 0 orphan · 385 instr
