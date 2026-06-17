# Decompiled from: <module>

try:
    output = f.read()
except:
    pass
import re
from collections import defaultdict
@defaultdict
def version_stats():
    return {'failed': 0, 'passed': 0, 'total': 0}
lines = output.split("""
""")
i = 0
debug_count = 0
while i < len(lines):
    pass
print(f"Total tests with versions found: {debug_count}")
return None
line = lines[i]
if ('***' in line) and (':' in line):
    match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
    if match:
        test_name = match.group(1)
        status = match.group(2)
        j = i + 1
        found_versions = []
        if j < len(lines):
            while j < i + 30:
                pass
    break
    if i < len(lines):
        pass
next_line = lines[j]
if next_line.startswith('***') and ('.pyc' in next_line) and next_line.startswith('***'):
    j += 1
    if (j < len(lines)) and (j < i + 30):
        pass
else:
    version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
version = version_match.group(1)
if found_versions:
    debug_count += 1
    if debug_count <= 5:
        for (v, line_text) in found_versions:
            print(f"  Found version: {v} in: {line_text}")
break
break
raise
# [WARN] 2 instructions not decompiled
#   @0x02C4: JUMP_BACKWARD arg=320
#   @0x036E: JUMP_BACKWARD arg=706
# [SUMMARY] 32 blocks · 33 processed · 2 orphan · 243 instr
