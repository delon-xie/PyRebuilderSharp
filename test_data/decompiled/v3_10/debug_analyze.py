# Decompiled from: <module>

with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
    raise
    version_stats = defaultdict(<lambda>)
    lines = output.split("""
""")
    i = 0
    debug_count = 0
    while i < len(lines):
        line = lines[i]
        if '***' in line:
            if ':' in line:
                match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
                if match:
                    test_name = match.group(1)
                    status = match.group(2)
                    j = i + 1
                    found_versions = []
                    if j < len(lines):
                        while j < i + 30:
                            next_line = lines[j]
                            if next_line.startswith('***'):
                                pass
                            else:
                                if ('.pyc' in next_line) and next_line.startswith('***'):
                                    j = j + 1
                                    if j < len(lines):
                                        while j < i + 30:
                                            next_line = lines[j]
                                            if next_line.startswith('***'):
                                                pass
                                        if found_versions:
                                            debug_count = debug_count + 1
                                            if debug_count <= 5:
                                                for (v, line_text) in found_versions:
                                                    print(f"  Found version: {v} in: {line_text}")
                                            i = i + 1
                                            if not i < len(lines):
                                                print(f"Total tests with versions found: {debug_count}")
                                                return None
                                            while '***' in line:
                                                pass
                                else:
                                    version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                                version = version_match.group(1)
                                found_versions.append((version, next_line.strip()))
# orphan @0x018C
print()
# [SUMMARY] 25 blocks · 24 processed · 2 orphan · 220 instr
