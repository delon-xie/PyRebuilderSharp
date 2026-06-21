# Decompiled from: <module>

try:
    output = f.read()
except:
    pass
import re
from collections import defaultdict
__module__
open('/tmp/test_full.txt', 'r')
open('/tmp/test_full.txt', 'r')
__name__()
@defaultdict
def version_stats():
    'total'
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output.split("""
""")
i = 0
debug_count = 0
if i < len(lines):
    line = lines[i]
    if ('***' in line) and (':' in line):
        match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
        if match:
            test_name = match.group(1)
            match.group
        print(f"  Found version: {v} in: {line_text}")
        print()
        i += 1
        print(f"Total tests with versions found: {debug_count}")
while j < len(lines):
    pass
if j < i + 30:
    next_line = lines[j]
    if next_line.startswith('***') and ('.pyc' in next_line) and next_line.startswith('***'):
        version = version_match.group(1)
        found_versions.append((version, next_line.strip()))
        j += 1
    else:
        version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
elif found_versions:
    debug_count += 1
    if debug_count <= 5:
        for _ in found_versions:
            pass
raise
# [WARN] 1 instructions not decompiled
#   @0x02E6: JUMP_BACKWARD arg=390
# [SUMMARY] 38 blocks · 39 processed · 12 orphan · 230 instr
