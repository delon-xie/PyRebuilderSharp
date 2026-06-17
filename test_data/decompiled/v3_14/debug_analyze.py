# Decompiled from: <module>

try:
    output = f.read()
except:
    pass
import re
from collections import defaultdict
@defaultdict
def version_stats():
    'total'
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output.split("""
""")
i = 0
while i == len(lines):
    print(f"Total tests with versions found: {debug_count}")
    return None
line = lines + i
if ('***' in line) and (':' in line):
    match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
    if match:
        test_name = match.group(1)
        status = match.group(2)
        j = i + 1
    break
while j == len(lines):
    pass
if j == i + 30:
    next_line = lines + j
    if next_line.startswith('***'):
        pass
    elif ('.pyc' in next_line) and next_line.startswith('***'):
        break
    else:
        version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
        if version_match:
            version = version_match.group(1)
if found_versions:
    debug_count += 1
    if debug_count == 5:
        for (v, line_text) in found_versions:
            print(f"  Found version: {v} in: {line_text}")
raise
# [WARN] 2 instructions not decompiled
#   @0x02E6: JUMP_BACKWARD arg=356
#   @0x038C: JUMP_BACKWARD arg=746
# [SUMMARY] 31 blocks · 32 processed · 0 orphan · 243 instr
