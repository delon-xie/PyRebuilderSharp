# Decompiled from: <module>

# orphan @0x00EA
next_line.strip().startswith(' ')
# orphan @0x00E8
# orphan @0x00D4
next_line = lines[j]
next_line.startswith('***')
# orphan @0x00C6
j < i + 30
# orphan @0x00B8
j < len(lines)
# orphan @0x009C
test_name = match.group(1)
status = match.group(2)
j = i + 1
# orphan @0x008A
match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
match
# orphan @0x0080
':' in line
# orphan @0x006E
line = lines[i]
'***' in line
# orphan @0x0060
i < len(lines)
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
    version_stats = defaultdict(<lambda>)
    lines = output.split("""
""")
    i = 0
# orphan @0x00FA
'.pyc' in next_line
# orphan @0x0104
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
version_match
# orphan @0x0116
version = version_match.group(1)
version in ('3.7', '3.8', '3.9', '3.10')
# orphan @0x012A
status == 'PASS'
version_stats[version]['total'] + 1
# orphan @0x0148
version_stats[version]['passed'] + 1
# orphan @0x015E
version_stats[version]['failed'] + 1
# orphan @0x0172
j += 1
# orphan @0x017C
i += 1
# orphan @0x0186
print('======================================================================')
print('Python 3.7-3.10 版本测试通过率统计')
print('======================================================================')
'<10'(f" 失败{'<10'} 总计{'<10'} 通过率{'<12'}")
print('----------------------------------------------------------------------')
total_passed = 0
total_failed = 0
total = 0
sorted(version_stats.keys())
'通过'
' '
'<12'
'版本'
print
# orphan @0x01EC
# orphan @0x01EE
stats = version_stats[version]
t = stats['total']
p = stats['passed']
f = stats['failed']
t > 0
# orphan @0x021A
p / t * 100
# orphan @0x0226
0
# orphan @0x0228
total_passed += p
total_failed += f
total += t
p(f"{'<10'} {f}{'<10'} {t}{'<10'} {rate}{'>8.1f'}%")
' '
'<5'
version
'Python '
print
# orphan @0x0278
print('----------------------------------------------------------------------')
total > 0
# orphan @0x028A
total_passed / total * 100
# orphan @0x0296
0
# orphan @0x0298
'<10'(f" {total_failed}{'<10'} {total}{'<10'} {overall_rate}{'>8.1f'}%")
print('======================================================================')
# [SUMMARY] 32 blocks · 4 processed · 28 orphan · 348 instr
