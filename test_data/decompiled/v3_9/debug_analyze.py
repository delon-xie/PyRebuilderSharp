# Decompiled from: <module>

# orphan @0x008E
match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
match
# orphan @0x0084
':' in line
# orphan @0x0072
line = lines[i]
'***' in line
# orphan @0x0064
i < len(lines)
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
j < len(lines)
# orphan @0x00CE
j < i + 30
# orphan @0x00DC
next_line = lines[j]
next_line.startswith('***')
# orphan @0x00F0
# orphan @0x00F2
'.pyc' in next_line
# orphan @0x00FC
next_line.startswith('***')
# orphan @0x0108
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
version_match
# orphan @0x011A
version = version_match.group(1)
found_versions.append((version, next_line.strip()))
# orphan @0x0136
j += 1
# orphan @0x0140
found_versions
# orphan @0x0146
debug_count += 1
debug_count <= 5
# orphan @0x0158
print(f"Test: {test_name}, Status: {status}")
found_versions
# orphan @0x0170
# orphan @0x0172
print(f"  Found version: {v} in: {line_text}")
# orphan @0x0190
print()
# orphan @0x0196
i += 1
# orphan @0x01A0
print(f"Total tests with versions found: {debug_count}")
# [SUMMARY] 26 blocks · 4 processed · 22 orphan · 204 instr
