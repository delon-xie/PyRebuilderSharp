# Decompiled from: <module>

import re
from collections import defaultdict
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
while i < len(lines):
    pass
line = lines[i]
if ('***' in line) and True:
    version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
    if version_match:
        version = version_match.group(1)
        found_versions.append((version, next_line.strip()))
        j += 1
        if found_versions:
            debug_count += 1
            if debug_count <= 5:
                for (v, line_text) in found_versions:
                    print(f"  Found version: {v} in: {line_text}")
match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
if match:
    test_name = match.group(1)
    status = match.group(2)
    j = i + 1
    found_versions = []
# orphan @0x00B0
# orphan @0x00BC
# orphan @0x00CA
next_line = lines[j]
# orphan @0x00DC
# orphan @0x00E6
# orphan @0x0180
# orphan @0x0182
print()
i += 1
print(f"Total tests with versions found: {debug_count}")
return None
# [SUMMARY] 29 blocks · 23 processed · 10 orphan · 201 instr
