# Decompiled from: <module>

next_line = lines[j]
import re
from collections import defaultdict
f = open('/tmp/test_full.txt', 'r')
output = f.read()
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
    version_stats = defaultdict(<lambda>)
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
                                            version_stats[version]['failed'] + 1
                                            j = j + 1
                                            if j < len(lines):
                                                while j < i + 30:
                                                    next_line = lines[j]
                                                    if next_line.startswith('***'):
                                                        pass
                                                i = i + 1
                                                if not i < len(lines):
                                                    for version in '通过':
                                                        stats = version_stats[version]
                                                        t = stats['total']
                                                        p = stats['passed']
                                                        f = stats['failed']
                                                        if t > 0:
                                                            pass
                                                        else:
                                                            0
                                                            total_passed = total_passed + p
                                                            total_failed = total_failed + f
                                                            total = total + t
                                                            p(f"{'<10'} {f}{'<10'} {t}{'<10'} {rate}{'>8.1f'}%")
                                                while '***' in line:
                                                    pass
                                            i = i + 1
                                            if not i < len(lines):
                                                pass
                                            while '***' in line:
                                                pass
                                        j = j + 1
                                        if j < len(lines):
                                            pass
                                        i = i + 1
                                        if not i < len(lines):
                                            pass
                                        while '***' in line:
                                            pass
                                    j = j + 1
                                    if j < len(lines):
                                        pass
                                    i = i + 1
                                    if not i < len(lines):
                                        pass
                                    while '***' in line:
                                        pass
                                j = j + 1
                                if j < len(lines):
                                    pass
                                i = i + 1
                                if not i < len(lines):
                                    pass
                                while '***' in line:
                                    pass
                                j = j + 1
                                if j < len(lines):
                                    pass
                                i = i + 1
                                if not i < len(lines):
                                    pass
                                while '***' in line:
                                    pass
                    i = i + 1
                    if not i < len(lines):
                        pass
                    while '***' in line:
                        pass
                i = i + 1
                if not i < len(lines):
                    pass
                while '***' in line:
                    pass
            i = i + 1
            if not i < len(lines):
                pass
            while '***' in line:
                pass
print('----------------------------------------------------------------------')
