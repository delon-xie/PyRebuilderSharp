# Decompiled from: <module>

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
# orphan @0x011A
version = version_match.group(1)
found_versions.append((version, next_line.strip()))
# orphan @0x0190
print()
# orphan @0x01A0
print(f"Total tests with versions found: {debug_count}")
# [SUMMARY] 26 blocks · 22 processed · 22 orphan · 204 instr
