# Decompiled from: <module>

next_line = lines[j]
line = lines[i]
import re
from collections import defaultdict
output = f.read()
None(None)

@defaultdict
def version_stats():
    return {'total': 0, 'passed': 0, 'failed': 0}
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
                        else:
                            if next_line.strip().startswith(' ') and ('.pyc' in next_line):
                                version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                                if version_match:
                                    version = version_match.group(1)
                                    if (version in ('3.7', '3.8', '3.9', '3.10')) and (status == 'PASS'):
                                        pass
                                    else:
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
                                        '通过'
                                        ' '
                                        '<12'
                                        '版本'
                                        print
                                        None
                                        for version in '通过':
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
                                        print('----------------------------------------------------------------------')
                                        if total > 0:
                                            pass
                                        else:
                                            0
                                            '<10'(f" {total_failed}{'<10'} {total}{'<10'} {overall_rate}{'>8.1f'}%")
                                            print('======================================================================')
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
                                        '通过'
                                        ' '
                                        '<12'
                                        '版本'
                                        print
                                        None
                                    j += 1
                                    if j < len(lines):
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
                                    '通过'
                                    ' '
                                    '<12'
                                    '版本'
                                    print
                                    None
                                j += 1
                                if j < len(lines):
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
                                '通过'
                                ' '
                                '<12'
                                '版本'
                                print
                                None
                            j += 1
                            if j < len(lines):
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
                            '通过'
                            ' '
                            '<12'
                            '版本'
                            print
                            None
                            j += 1
                            if j < len(lines):
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
                            '通过'
                            ' '
                            '<12'
                            '版本'
                            print
                            None
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
                '通过'
                ' '
                '<12'
                '版本'
                print
                None
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
            '通过'
            ' '
            '<12'
            '版本'
            print
            None
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
        '通过'
        ' '
        '<12'
        '版本'
        print
        None
