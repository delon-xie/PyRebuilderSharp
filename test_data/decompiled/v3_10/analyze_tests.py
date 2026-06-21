# Decompiled from: <module>

# orphan @0x00C8
next_line = lines[j]
next_line.startswith('***')
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
    raise
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
                            elif next_line.strip().startswith(' ') and ('.pyc' in next_line):
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
                                            for version in sorted(version_stats.keys()):
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
# orphan @0x027E
print('----------------------------------------------------------------------')
total > 0
# orphan @0x0290
total_passed / total * 100
# orphan @0x029C
0
# orphan @0x029E
'<10'(f" {total_failed}{'<10'} {total}{'<10'} {overall_rate}{'>8.1f'}%")
print('======================================================================')
# [SUMMARY] 31 blocks · 26 processed · 5 orphan · 364 instr
