# Decompiled from: <module>

# orphan @0x00D4
next_line.strip().startswith(' ')
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
while i < len(lines):
    total_failed = 0
    total = 0
    version_stats
    sorted
    for version in version_stats:
        version_stats[version]
        t = stats['total']
        p = stats['passed']
        f = stats['failed']
        if t > 0:
            0
            p / t * 100
        total_passed
        total_passed = p
        total_failed += f
        total += t
        ' '
        '<5'
        version
        'Python '
        print
        t
        ' '
        '<10'
        f
        ' '
        '<10'
        p
        break
    '-'
    print
    break
    if total > 0:
        0
        total_passed / total * 100
    '<10'(f" {total_failed}{'<10'} {total}{'<10'} {overall_rate}{'>8.1f'}%")
    print('=' * 70)
    return None
line = lines[i]
if '***' in line:
    0
    version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
    if version_match:
        version = version_match.group(1)
        if (version in ('3.7', '3.8', '3.9', '3.10')) and (status == 'PASS'):
            version_stats[version]['failed'] + 1
            version_stats[version]['passed'] + 1
match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
if match:
    test_name = match.group(1)
    status = match.group(2)
    j = i + 1
# orphan @0x0172
print('=' * 70)
print('Python 3.7-3.10 版本测试通过率统计')
print('=' * 70)
'<10'
'失败'
' '
'<10'
'通过'
' '
'<12'
'版本'
print
# orphan @0x01AA
print('-' * 70)
# [SUMMARY] 37 blocks · 35 processed · 7 orphan · 354 instr
