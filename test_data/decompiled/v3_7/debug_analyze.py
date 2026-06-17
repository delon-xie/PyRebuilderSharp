# Decompiled from: <module>

import re
from collections import defaultdict
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
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
    i += 1
    while j < len(lines):
        if j < i + 30:
            next_line = lines[j]
            if next_line.startswith('***'):
                pass
        if found_versions:
            debug_count += 1
            if debug_count <= 5:
                for (v, line_text) in found_versions:
                    print(f"  Found version: {v} in: {line_text}")
        if '.pyc' in next_line:
            if not next_line.startswith('***'):
                version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                if version_match:
                    version = version_match.group(1)
                    found_versions.append((version, next_line.strip()))
        j += 1
        print()
print(f"Total tests with versions found: {debug_count}")
return None
# [SUMMARY] 23 blocks · 24 processed · 0 orphan · 200 instr
