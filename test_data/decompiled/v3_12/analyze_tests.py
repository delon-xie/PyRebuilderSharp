# Decompiled from: <module>

next_line = lines[j]
test_name = match.group(1)
status = match.group(2)
j = i + 1
match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
line = lines[i]

@defaultdict
def version_stats():
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output.split("""
""")
i = 0
while '***' in line:
    i += 1
    if i < len(lines):
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
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
version = version_match.group(1)
j += 1
