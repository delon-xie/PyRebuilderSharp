# Decompiled from: <module>

test_name = match.group(1)
status = match.group(2)
j = i + 1
found_versions = []
match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
line = lines[i]

@defaultdict
def version_stats():
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output.split("""
""")
i = 0
debug_count = 0
while next_line.startswith('***'):
    if ('.pyc' in next_line) and next_line.startswith('***'):
        j += 1
        if (j < len(lines)) and (j < i + 30):
            pass
        # [Block @0x02C0] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
    print()
next_line = lines[j]
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
debug_count += 1
i += 1
