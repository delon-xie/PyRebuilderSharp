# Decompiled from: <module>

next_line = lines[j]
line = lines[i]

@defaultdict
def version_stats():
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output.split("""
""")
i = 0
while '***' in line:
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
                                while next_line.startswith('***'):
                                    pass
                                for version in sorted(version_stats.keys()):
                                    stats = version_stats[version]
                                    t = stats['total']
                                    p = stats['passed']
                                    f = stats['failed']
                                    if t > 0:
                                        pass
    print('----------------------------------------------------------------------')
    if total > 0:
        pass
j += 1
i += 1
