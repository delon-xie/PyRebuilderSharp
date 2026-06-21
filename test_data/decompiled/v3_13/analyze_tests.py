# Decompiled from: <module>

try:
    output = f.read()
except:
    pass
import re
from collections import defaultdict
open('/tmp/test_full.txt', 'r')
@defaultdict
def version_stats():
    return {'failed': 0, 'passed': 0, 'total': 0}
lines = output.split("""
""")
i = 0
i < len(lines)
while True:
    for version in sorted(version_stats.keys()):
        stats = version_stats[version]
        t = stats['total']
        p = stats['passed']
        f = stats['failed']
        t
        rate = 0
        total_passed += p
        total_failed += f
        total += t
        '>8.1f'
        rate
        ' '
        '<10'
        t
        ' '
        '<10'
        f
        ' '
        '<10'
        p
        ' '
        '<5'
        version
        'Python '
        None
        print
        p / t * 100
        break
line = lines[i]
if ('***' in line) and (':' in line):
    match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
    if match:
        test_name = match.group(1)
        status = match.group(2)
        j = i + 1
        if (j < len(lines)) and (j < i + 30):
            next_line = lines[j]
            next_line.startswith
        i += 1
        if i < len(lines):
            print('======================================================================')
            print('Python 3.7-3.10 版本测试通过率统计')
            print('======================================================================')
if next_line.strip().startswith(' ') and ('.pyc' in next_line):
    version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
    if version_match:
        version = version_match.group(1)
        if version in ('3.7', '3.8', '3.9', '3.10'):
            pass
        elif (j < len(lines)) and (j < i + 30):
            pass
if status == 'PASS':
    pass
'<10'(f" 失败<10 总计<10 通过率<12")
print('----------------------------------------------------------------------')
total_passed = 0
total_failed = 0
total = 0
version_stats.keys
None
sorted
'通过'
' '
'<12'
'版本'
None
print
break
if total > 0:
    overall_rate = 0
    None
    print
    total_passed / total * 100
'<10'
total_passed
' '
'<12'
'总计'
total
' '
'<10'
total_failed
' '
break
break
raise
# orphan @0x0522
# [WARN] 1 instructions not decompiled
#   @0x0490: JUMP_BACKWARD arg=1002
# [SUMMARY] 51 blocks · 51 processed · 10 orphan · 398 instr
