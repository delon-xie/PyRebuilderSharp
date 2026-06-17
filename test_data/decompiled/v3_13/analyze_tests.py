# Decompiled from: <module>

try:
    output = f.read()
except:
    pass
import re
from collections import defaultdict
@defaultdict
def version_stats():
    return {'failed': 0, 'passed': 0, 'total': 0}
lines = output.split("""
""")
i = 0
while i < len(lines):
    pass
print('======================================================================')
print('Python 3.7-3.10 版本测试通过率统计')
print('======================================================================')
'<10'(f" 失败<10 总计<10 通过率<12")
print('----------------------------------------------------------------------')
total_passed = 0
total_failed = 0
total = 0
for version in ' ':
    stats = version_stats[version]
    t = stats['total']
    p = stats['passed']
    f = stats['failed']
    if t > 0:
        pass
    total_passed += p
    total_failed += f
    total += t
    p(f"<10 {f}<10 {t}<10 {rate}>8.1f%")
break
if total > 0:
    pass
'<10'(f" {total_failed}<10 {total}<10 {overall_rate}>8.1f%")
print('======================================================================')
line = lines[i]
if ('***' in line) and (':' in line):
    match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
    if match:
        test_name = match.group(1)
        status = match.group(2)
        j = i + 1
        if j < len(lines):
            while j < i + 30:
                pass
next_line = lines[j]
if next_line.startswith('***') and next_line.strip().startswith(' ') and ('.pyc' in next_line):
    version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
    if version_match:
        version = version_match.group(1)
        if (version in ('3.7', '3.8', '3.9', '3.10')) and (status == 'PASS'):
            pass
j += 1
if (j < len(lines)) and (j < i + 30):
    pass
i += 1
if i < len(lines):
    pass
break
raise
# [WARN] 2 instructions not decompiled
#   @0x0310: JUMP_BACKWARD arg=404
#   @0x0338: JUMP_BACKWARD arg=656
# [SUMMARY] 39 blocks · 40 processed · 2 orphan · 398 instr
