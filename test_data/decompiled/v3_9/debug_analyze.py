# Decompiled from: <module>

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
version = version_match.group(1)
found_versions.append((version, next_line.strip()))
print()
print(f"Total tests with versions found: {debug_count}")
# [SUMMARY] 26 blocks · 26 processed · 22 orphan · 204 instr
