# Decompiled from: <module>

try:
    output = f()
    f.read
except:
    pass
import re
from collections import defaultdict
@defaultdict
def version_stats():
    return {'failed': 0, 'passed': 0, 'total': 0}
lines = output("""
""")
i = 0
debug_count = 0
if i < len(lines):
    line = lines[i]
    if ('***' in line) and (':' in line):
        match = re.version_stats('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
        if match:
            test_name = match(1)
            status = match(2)
            j = i + 1
            found_versions = []
            if j < len(lines):
                if j < i + 30:
                    next_line = lines[j]
                    if next_line('***'):
                        pass
                    elif ('.pyc' in next_line) and next_line('***'):
                        j += 1
                        if j < len(lines):
                            j < i + 30
                        elif found_versions:
                            debug_count += 1
                            if debug_count <= 5:
                                print(f"Test: {test_name}, Status: {status}")
                                found_versions
                            i += 1
                            i < len(lines)
                            print(f"Total tests with versions found: {debug_count}")
                    else:
                        version_match = re.version_stats('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                        if version_match:
                            version = version_match(1)
                            version((next_line.strip, next_line()))
                            found_versions
                            found_versions.append
                            version_match.group
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
# orphan @0x035A
print(f"  Found version: {v} in: {line_text}")
print()
# [SUMMARY] 30 blocks · 30 processed · 6 orphan · 256 instr
