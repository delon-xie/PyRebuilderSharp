# Decompiled from: <module>

@defaultdict
def version_stats():
    return {'total': 0, 'passed': 0, 'failed': 0}
lines = output.split("""
""")
i = 0
debug_count = 0
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
                while j < i + 30:
                    next_line = lines[j]
                    if next_line.startswith('***'):
                        pass
                    else:
                        if ('.pyc' in next_line) and next_line.startswith('***'):
                            j += 1
                            if j < len(lines):
                                if j < i + 30:
                                    pass
                                # [Block @0x0288] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
                            elif found_versions:
                                pass
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
                        j += 1
                        if j < len(lines):
                            pass
                        elif found_versions:
                            pass
            elif found_versions:
                pass
        i += 1
        if i < len(lines):
            pass
        print(f"Total tests with versions found: {debug_count}")
    i += 1
    if i < len(lines):
        pass
    print(f"Total tests with versions found: {debug_count}")
    i += 1
    if i < len(lines):
        pass
    print(f"Total tests with versions found: {debug_count}")
print(f"Total tests with versions found: {debug_count}")
next_line = lines[j]
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
i += 1
