# Decompiled from: <module>

import re
from collections import defaultdict
open('/tmp/test_full.txt', 'r')
output = f.read()
None(None)

@defaultdict
def version_stats():
    return {'total': 0, 'passed': 0, 'failed': 0}
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
            status = match.group(2)
            j = i + 1
            found_versions = []
            if j < len(lines):
                if j < i + 30:
                    next_line = lines[j]
                    if next_line.startswith('***'):
                        pass
                    elif ('.pyc' in next_line) and next_line.startswith('***'):
                        j += 1
                        if j < len(lines):
                            return j < i + 30
                        elif found_versions:
                            debug_count += 1
                            if debug_count <= 5:
                                print(f"Test: {test_name}, Status: {status}")
                                found_versions
                            i += 1
                            i < len(lines)
                            print(f"Total tests with versions found: {debug_count}")
                    else:
                        version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                        if version_match:
                            version = version_match.group(1)
                            found_versions.append((version, next_line.strip()))
                        j += 1
                        if j < len(lines):
                            pass
                        elif found_versions:
                            pass
                elif found_versions:
                    pass
            elif found_versions:
                pass
        i += 1
        i < len(lines)
    i += 1
    i < len(lines)
    i += 1
    i < len(lines)
print(f"Total tests with versions found: {debug_count}")
if not True:
    pass
raise
# [Block @0x0358] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
