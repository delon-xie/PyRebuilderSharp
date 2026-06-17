# Decompiled from: <module>

# orphan @0x0166
next_line = lines[j]
# orphan @0x00AA
line = lines[i]
try:
    output = f.read()
except:
    break
import re
from collections import defaultdict
@defaultdict
def version_stats():
    return {'failed': 0, 'passed': 0, 'total': 0}
lines = output.split("""
""")
i = 0
while i < len(lines):
    line = lines[i]
    if '***' in line:
        if ':' in line:
            match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
            if match:
                test_name = match.group(1)
                status = match.group(2)
                j = i + 1
                if j < len(lines):
                    while j < i + 30:
                        next_line = lines[j]
                        if next_line.startswith('***'):
                            pass
                        elif next_line.strip().startswith(' ') and ('.pyc' in next_line):
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
                                print('======================================================================')
                                print('Python 3.7-3.10 版本测试通过率统计')
                                print('======================================================================')
                                '<10'(f" 失败{'<10'} 总计{'<10'} 通过率{'<12'}")
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
                                    p(f"{'<10'} {f}{'<10'} {t}{'<10'} {rate}{'>8.1f'}%")
                                print('----------------------------------------------------------------------')
                                if total > 0:
                                    pass
                                '<10'(f" {total_failed}{'<10'} {total}{'<10'} {overall_rate}{'>8.1f'}%")
                                print('======================================================================')
break
# orphan @0x04D2
raise
# [WARN] 3 instructions not decompiled
#   @0x02CA: JUMP_BACKWARD arg=358
#   @0x02EE: JUMP_BACKWARD arg=582
#   @0x04D0: JUMP_BACKWARD arg=1144
# [SUMMARY] 38 blocks · 35 processed · 3 orphan · 392 instr
