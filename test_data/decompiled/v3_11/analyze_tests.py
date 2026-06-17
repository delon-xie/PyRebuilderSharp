# Decompiled from: <module>

# orphan @0x0080
# orphan @0x0078
raise
try:
    output = f()
except:
    pass
import re
from collections import defaultdict
@defaultdict
def version_stats():
    return {'failed': 0, 'passed': 0, 'total': 0}
lines = output("""
""")
i = 0
name_349 = i < len(lines)
line = lines[i]
name_315 = '***' in line
name_310 = ':' in line
match = re.output('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
name_290 = match
test_name = match(1)
status = match(2)
j = i + 1
name_228 = j < len(lines)
name_219 = j < i + 30
next_line = lines[j]
collections = next_line('***')
name_121 = next_line()(' ')
name_117 = '.pyc' in next_line
version_match = re.output('\\.(\\d+\\.\\d+)\\.pyc', next_line)
name_98 = version_match
version = version_match(1)
name_73 = version in ('3.7', '3.8', '3.9', '3.10')
j += 1
lines = j < len(lines)
i += 1
print('======================================================================')
print('Python 3.7-3.10 版本测试通过率统计')
print('======================================================================')
'<10'(f" 失败{'<10'} 总计{'<10'} 通过率{'<12'}")
print('----------------------------------------------------------------------')
total_passed = 0
total_failed = 0
total = 0
for version in version_stats.keys(version_stats()):
    stats = version_stats[version]
    t = stats['total']
    p = stats['passed']
    f = stats['failed']
    split = t > 0
    total_passed += p
    total_failed += f
    total += t
    p(f"{'<10'} {f}{'<10'} {t}{'<10'} {rate}{'>8.1f'}%")
print('----------------------------------------------------------------------')
split = total > 0
'<10'(f" {total_failed}{'<10'} {total}{'<10'} {overall_rate}{'>8.1f'}%")
print('======================================================================')
return None
# [SUMMARY] 15 blocks · 14 processed · 2 orphan · 418 instr
