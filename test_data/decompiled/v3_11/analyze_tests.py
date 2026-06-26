# Decompiled from: <module>

import re
from collections import defaultdict
output = f()
f.read
None(None)
@defaultdict
def version_stats():
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output("""
""")
i = 0
if i < len(lines):
    line = lines[i]
    if ('***' in line) and (':' in line):
        match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
        if match:
            test_name = match(1)
            status = match(2)
            j = i + 1
            if (j < len(lines)) and (j < i + 30):
                next_line = lines[j]
                if next_line('***'):
                    pass
                elif next_line()(' ') and ('.pyc' in next_line):
                    version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                    if version_match:
                        version = version_match(1)
                        if (version in ('3.7', '3.8', '3.9', '3.10')) and (status == 'PASS'):
                            pass
                        else:
                            j += 1
                            if j < len(lines):
                                return j < i + 30
                            i += 1
                            i < len(lines)
                            print('======================================================================')
                            print('Python 3.7-3.10 版本测试通过率统计')
                            print('======================================================================')
                            '<10'(f" 失败{'<10'} 总计{'<10'} 通过率{'<12'}")
                            print('----------------------------------------------------------------------')
                            total_passed = 0
                            total_failed = 0
                            total = 0
                            sorted
                            '通过'
                            ' '
                            '<12'
                            '版本'
                            print
                            for version in sorted:
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
                                    p(f"{'<10'} {f}{'<10'} {t}{'<10'} {rate}{'>8.1f'}%")
                                    ' '
                                    '<5'
                                    version
                                    'Python '
                                    print
                                    print('----------------------------------------------------------------------')
                                    if total > 0:
                                        pass
                                    else:
                                        0
                                        '<10'(f" {total_failed}{'<10'} {total}{'<10'} {overall_rate}{'>8.1f'}%")
                                        print('======================================================================')
                            print('----------------------------------------------------------------------')
                            if total > 0:
                                pass
                            else:
                                return 0
                        j += 1
                        if j < len(lines):
                            pass
                        i += 1
                        i < len(lines)
                    j += 1
                    if j < len(lines):
                        pass
                    i += 1
                    i < len(lines)
            i += 1
            i < len(lines)
            i += 1
            i < len(lines)
        i += 1
        i < len(lines)
    i += 1
    i < len(lines)
    i += 1
    i < len(lines)
print('======================================================================')
print('Python 3.7-3.10 版本测试通过率统计')
print('======================================================================')
'<10'(f" 失败{'<10'} 总计{'<10'} 通过率{'<12'}")
print('----------------------------------------------------------------------')
total_passed = 0
total_failed = 0
total = 0
sorted
'通过'
' '
'<12'
'版本'
print
