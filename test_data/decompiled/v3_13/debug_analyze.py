# Decompiled from: <module>

import re
from collections import defaultdict
open('/tmp/test_full.txt', 'r')
output = f.read()
None

@defaultdict
def version_stats():
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output.split("""
""")
i = debug_count = 0
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
                while j < i + 30:
                    next_line = lines[j]
                    if next_line.startswith('***'):
                        pass
                    elif ('.pyc' in next_line) and next_line.startswith('***'):
                        j += 1
                        if (j < len(lines)) and (j < i + 30):
                            pass
                        i += 1
                        if i < len(lines):
                            pass
                        print(f"Total tests with versions found: {debug_count}")
                        pass
                    else:
                        version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                        if version_match:
                            version = version_match.group(1)
                            found_versions.append((version, next_line.strip()))
next_line = lines[j]
