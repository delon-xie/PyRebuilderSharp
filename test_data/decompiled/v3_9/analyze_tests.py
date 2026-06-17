# Decompiled from: <module>

# orphan @0x00EA
# orphan @0x00E8
# orphan @0x00D4
next_line = lines[j]
# orphan @0x00C6
# orphan @0x00B8
# orphan @0x009C
test_name = match.group(1)
status = match.group(2)
j = i + 1
# orphan @0x008A
match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
# orphan @0x0080
# orphan @0x006E
line = lines[i]
# orphan @0x0060
import re
from collections import defaultdict
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
    version_stats = defaultdict(<lambda>)
    lines = output.split("""
""")
    i = 0
# orphan @0x00FA
# orphan @0x0104
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
# orphan @0x0116
version = version_match.group(1)
# orphan @0x012A
# orphan @0x0148
# orphan @0x015E
# orphan @0x0172
j += 1
# orphan @0x017C
i += 1
# orphan @0x0186
print('======================================================================')
print('Python 3.7-3.10 版本测试通过率统计')
print('======================================================================')
'<10'(f" 失败{'<10'} 总计{'<10'} 通过率{'<12'}")
print('----------------------------------------------------------------------')
total_passed = 0
total_failed = 0
total = 0
# orphan @0x01EC
# orphan @0x01EE
stats = version_stats[version]
t = stats['total']
p = stats['passed']
f = stats['failed']
# orphan @0x021A
# orphan @0x0226
# orphan @0x0228
total_passed += p
total_failed += f
total += t
p(f"{'<10'} {f}{'<10'} {t}{'<10'} {rate}{'>8.1f'}%")
# orphan @0x0278
print('----------------------------------------------------------------------')
# orphan @0x028A
# orphan @0x0296
# orphan @0x0298
'<10'(f" {total_failed}{'<10'} {total}{'<10'} {overall_rate}{'>8.1f'}%")
print('======================================================================')
return None
# [SUMMARY] 32 blocks · 4 processed · 28 orphan · 348 instr
