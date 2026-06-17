# Decompiled from: <module>

try:
    output = f.read()
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
while i < len(lines):
    for version in ' ':
        stats = version_stats[version]
        t = stats['total']
        p = stats['passed']
        f = stats['failed']
        if t > 0:
            pass
        total_passed += p
        total_failed += f
        total += t
        p(f"<10 {f}<10 {t}<10 {rate}>8.1f%")
    print('----------------------------------------------------------------------')
    if total > 0:
        pass
    '<10'(f" {total_failed}<10 {total}<10 {overall_rate}>8.1f%")
    print('======================================================================')
line = lines[i]
if ('***' in line) and (':' in line):
    match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
    if match:
        test_name = match.group(1)
        status = match.group(2)
while j < len(lines):
    pass
if j < i + 30:
    next_line = lines[j]
    if next_line.startswith('***'):
        pass
    elif next_line.strip().startswith(' ') and ('.pyc' in next_line):
        version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
        if version_match:
            version = version_match.group(1)
            if (version in ('3.7', '3.8', '3.9', '3.10')) and (status == 'PASS'):
                pass
j += 1
i += 1
raise
# [WARN] 2 instructions not decompiled
#   @0x0380: JUMP_BACKWARD arg=518
#   @0x0398: JUMP_BACKWARD arg=762
# [SUMMARY] 38 blocks · 39 processed · 0 orphan · 400 instr
