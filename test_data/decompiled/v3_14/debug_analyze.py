# Decompiled from: <module>

try:
    try:
        try:
            raise
            raise
        except:
            pass
    except:
        pass
except:
    pass
import re
from collections import defaultdict
@defaultdict
def version_stats():
    'total'
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
            if (j < len(lines)) and (j < i + 30):
                next_line = lines[j]
                if next_line.startswith('***') and ('.pyc' in next_line) and next_line.startswith('***'):
                    pass
                else:
                    version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                version = version_match.group(1)
                found_versions.append((version, next_line.strip()))
                j += 1
                if found_versions:
                    debug_count += 1
                    if debug_count <= 5:
                        for (v, line_text) in debug_count <= 5:
                            print(f"  Found version: {v} in: {line_text}")
                            print()
                            i += 1
                            print(f"Total tests with versions found: {debug_count}")
                            return None
# [WARN] 2 instructions not decompiled
#   @0x02E6: JUMP_BACKWARD arg=0
#   @0x038C: JUMP_BACKWARD arg=0
# [SUMMARY] 38 blocks · 39 processed · 3 orphan · 230 instr
