# Decompiled from: <module>

try:
    try:
        try:
            pass
        except:
            pass
        output = f.read()
    except:
        pass
except:
    pass
import re
from collections import defaultdict
open('/tmp/test_full.txt', 'r')
@defaultdict
def version_stats():
    return {'failed': 0, 'passed': 0, 'total': 0}
lines = output.split("""
""")
i = 0
debug_count = 0
if i < len(lines):
    line = lines[i]
    if ('***' in line) and (':' in line):
        match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
        if match:
            test_name = match.group(1)
            match.group
        print(f"  Found version: {v} in: {line_text}")
        break
        if i < len(lines):
            debug_count
            'Total tests with versions found: '
            None
            print
j = i + 1
found_versions = []
if (j < len(lines)) and (j < i + 30):
    next_line = lines[j]
    if next_line.startswith('***') and ('.pyc' in next_line) and next_line.startswith('***'):
        version = version_match.group(1)
        found_versions.append((version, next_line.strip()))
        j += 1
        if j < len(lines):
            j < i + 30
        elif found_versions:
            debug_count += 1
            if debug_count <= 5:
                for _ in found_versions:
                    pass
    else:
        version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
break
break
# orphan @0x03A8
# [SUMMARY] 44 blocks · 44 processed · 17 orphan · 243 instr
