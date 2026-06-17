# Decompiled from: <module>

# orphan @0x0080
# orphan @0x0078
raise
try:
    output = f()
    f.read
except:
    pass
import re
from collections import defaultdict
@defaultdict
def version_stats():
    return {'failed': 0, 'passed': 0, 'total': 0}
lines = output("""
""")
i = 0
debug_count = 0
name_362 = i < len(lines)
line = lines[i]
name_328 = '***' in line
name_323 = ':' in line
match = re.version_stats('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
name_303 = match
test_name = match(1)
status = match(2)
j = i + 1
found_versions = []
name_174 = j < len(lines)
name_165 = j < i + 30
next_line = lines[j]
collections = next_line('***')
name_102 = '.pyc' in next_line
version_match = re.version_stats('\\.(\\d+\\.\\d+)\\.pyc', next_line)
name_62 = version_match
version = version_match(1)
version((next_line.strip, next_line()))
j += 1
lines = j < len(lines)
j < i + 30
found_versions
found_versions.append
version_match.group
[output.split, match.group, match.group, next_line.startswith, next_line.startswith, next_line('***')]
name_63 = found_versions
debug_count += 1
name_52 = debug_count <= 5
print(f"Test: {test_name}, Status: {status}")
found_versions
for (v, line_text) in found_versions:
    print(f"  Found version: {v} in: {line_text}")
print()
i += 1
print(f"Total tests with versions found: {debug_count}")
return None
# [SUMMARY] 12 blocks · 11 processed · 2 orphan · 256 instr
