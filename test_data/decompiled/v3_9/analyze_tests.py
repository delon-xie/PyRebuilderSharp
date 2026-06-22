# Decompiled from: <module>

next_line = lines[j]
test_name = match.group(1)
status = match.group(2)
j = i + 1
match = re.search('\\*\\*\\*\\s+([^:]+):\\s+(PASS|FAIL)', line)
line = lines[i]
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()
    version_stats = defaultdict(<lambda>)
    lines = output.split("""
""")
    i = 0
version_match = re.search('\\.(\\d+\\.\\d+)\\.pyc', next_line)
version = version_match.group(1)
# orphan @0x015E
version_stats[version]['failed'] + 1
j += 1
i += 1
stats = version_stats[version]
t = stats['total']
p = stats['passed']
f = stats['failed']
# orphan @0x0226
0
total_passed += p
total_failed += f
total += t
p(f"{'<10'} {f}{'<10'} {t}{'<10'} {rate}{'>8.1f'}%")
print('----------------------------------------------------------------------')
# orphan @0x0296
0
'<10'(f" {total_failed}{'<10'} {total}{'<10'} {overall_rate}{'>8.1f'}%")
print('======================================================================')
# [SUMMARY] 32 blocks · 29 processed · 28 orphan · 348 instr
