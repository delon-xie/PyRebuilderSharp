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
None
import re
from collections import defaultdict
next_line = lines[j]
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
j += 1
debug_count += 1
# [Block @0x0358] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
