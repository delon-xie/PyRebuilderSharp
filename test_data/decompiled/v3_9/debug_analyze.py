# Decompiled from: <module>

match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
line = lines[i]
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
    version_stats = defaultdict(<lambda>)
    lines = output.split("""
""")
    i = 0
    debug_count = 0
test_name = match.group(1)
status = match.group(2)
j = i + 1
found_versions = []
next_line = lines[j]
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
version = version_match.group(1)
found_versions.append((version, next_line.strip()))
j += 1
debug_count += 1
print(f"  Found version: {v} in: {line_text}")
print()
i += 1
print(f"Total tests with versions found: {debug_count}")
# [SUMMARY] 26 blocks · 26 processed · 22 orphan · 204 instr
