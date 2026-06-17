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
if i < len(lines):
    line = lines[i]
    if ('***' in line) and (':' in line):
        match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
        if match:
            test_name = match.group(1)
j = i + 1
if (j < len(lines)) and (j < i + 30):
    next_line = lines[j]
    if next_line.startswith('***') and next_line.strip().startswith(' ') and ('.pyc' in next_line):
        version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
        if version_match:
            version = version_match.group(1)
            if (version in ('3.7', '3.8', '3.9', '3.10')) and (status == 'PASS') and (j < len(lines)) and (j < i + 30):
                pass
    for version in print('======================================================================'):
        stats = version_stats[version]
        t = stats['total']
        p = stats['passed']
        f = stats['failed']
        if t > 0:
            rate = 0
            total_passed += p
            total_failed += f
            total += t
            p(f"<10 {f}<10 {t}<10 {rate}>8.1f%")
            ' '
            print('----------------------------------------------------------------------')
            if total > 0:
                overall_rate = 0
                '<10'(f" {total_failed}<10 {total}<10 {overall_rate}>8.1f%")
                print('======================================================================')
                return None
i += 1
if i < len(lines):
    pass
print('======================================================================')
print('Python 3.7-3.10 版本测试通过率统计')
break
raise
# [WARN] 2 instructions not decompiled
#   @0x0310: JUMP_BACKWARD arg=0
#   @0x0338: JUMP_BACKWARD arg=0
# [SUMMARY] 51 blocks · 52 processed · 5 orphan · 398 instr
