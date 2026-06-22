# Decompiled from: <module>

line = lines[i]
try:
    output = f.read()
except:
    break
import re
from collections import defaultdict
@defaultdict
def version_stats():
    return {'failed': 0, 'passed': 0, 'total': 0}
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
                                j += 1
                                if j < len(lines):
                                    if j < i + 30:
                                        pass
                                    elif found_versions:
                                        debug_count += 1
                                        if debug_count <= 5:
                                            for (v, line_text) in found_versions:
                                                print(f"  Found version: {v} in: {line_text}")
                                        i += 1
                                        if i < len(lines):
                                            pass
                                        print(f"Total tests with versions found: {debug_count}")
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
print()
break
next_line = lines[j]
# [SUMMARY] 32 blocks · 32 processed · 3 orphan · 236 instr
