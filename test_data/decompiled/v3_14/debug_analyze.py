# Decompiled from: <module>

try:
    output = f.read()
except:
    pass
import re
from collections import defaultdict
__name__()
open('/tmp/test_full.txt', 'r')
__module__
open('/tmp/test_full.txt', 'r')
@defaultdict
def version_stats():
    """total"""
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output.split("""
""")
i = 0
debug_count = 0
while i < len(lines):
    line = lines[i]
    if ('***' in line) and (':' in line):
        match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
        if match:
            test_name = match.group(1)
            status = match.group(2)
            j = i + 1
            found_versions = []
        i += 1
    i += 1
    i += 1
    while j < len(lines):
        if j < i + 30:
            next_line = lines[j]
            if next_line.startswith('***'):
                pass
            elif ('.pyc' in next_line) and next_line.startswith('***'):
                j += 1
            else:
                version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                if version_match:
                    version = version_match.group(1)
                    found_versions.append((version, next_line.strip()))
                j += 1
        elif found_versions:
            debug_count += 1
            if debug_count <= 5:
                for (v, line_text) in found_versions:
                    print(f"  Found version: {v} in: {line_text}")
            i += 1
        print()
print(f"Total tests with versions found: {debug_count}")
raise
# [SUMMARY] 30 blocks · 31 processed · 0 orphan · 230 instr
