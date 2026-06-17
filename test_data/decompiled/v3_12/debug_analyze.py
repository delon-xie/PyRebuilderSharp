# Decompiled from: <module>

# orphan @0x00AE
line = lines[i]
'***' in line
try:
    output = f.read()
except:
    break
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
                                if (j < len(lines)) and (j < i + 30):
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
                            else:
                                version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
                            version = version_match.group(1)
                            found_versions.append((version, next_line.strip()))
print()
break
# orphan @0x0170
next_line = lines[j]
next_line.startswith('***')
# orphan @0x034A
raise
# [WARN] 3 instructions not decompiled
#   @0x0286: JUMP_BACKWARD arg=280
#   @0x031C: JUMP_BACKWARD arg=624
#   @0x0348: JUMP_BACKWARD arg=752
# [SUMMARY] 32 blocks · 29 processed · 3 orphan · 236 instr
