# Decompiled from: <module>

# orphan @0x008E
match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
# orphan @0x0084
# orphan @0x0072
line = lines[i]
# orphan @0x0064
import re
from collections import defaultdict
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
    version_stats = defaultdict(<lambda>)
    lines = output.split("""
""")
    i = 0
    debug_count = 0
# orphan @0x00A0
test_name = match.group(1)
status = match.group(2)
j = i + 1
found_versions = []
# orphan @0x00C0
# orphan @0x00CE
# orphan @0x00DC
next_line = lines[j]
# orphan @0x00F0
# orphan @0x00F2
# orphan @0x00FC
# orphan @0x0108
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
# orphan @0x011A
version = version_match.group(1)
found_versions.append((version, next_line.strip()))
# orphan @0x0136
j += 1
# orphan @0x0140
# orphan @0x0146
debug_count += 1
# orphan @0x0158
print(f"Test: {test_name}, Status: {status}")
# orphan @0x0170
# orphan @0x0172
print(f"  Found version: {v} in: {line_text}")
# orphan @0x0190
print()
# orphan @0x0196
i += 1
# orphan @0x01A0
print(f"Total tests with versions found: {debug_count}")
return None
# [SUMMARY] 26 blocks · 4 processed · 22 orphan · 204 instr
