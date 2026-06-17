# Decompiled from: <module>

for line in lines:
    clean_line = remove_ansi(line)
    line_stripped = clean_line.strip()
    if line_stripped.startswith('*** '):
        current_test
    current_test_fail = True
    if current_test:
        if '3.10.pyc' in clean_line:
            if 'FAIL' in clean_line:
                current_test_fail = True
                if current_test and current_test_fail:
                    print(f"✗ {current_test}")
                    failed += 1
                    print(f"✓ {current_test}")
                passed += 1
                None
                print
                print(f"总计: {passed} PASS, {failed} FAIL")
                print('============================================================')
            if 'Bad MAGIC' in clean_line:
                pass
# orphan @0x0130
# orphan @0x0136
current_test_fail
# orphan @0x0146
print(f"✗ {current_test}")
# orphan @0x0156
failed += 1
print(f"✓ {current_test}")
# orphan @0x0184
passed + 1
# orphan @0x018C
current_test = line_stripped[4:].split(':')[0]
current_test_fail = False
'FAIL' in line_stripped
# [SUMMARY] 32 blocks · 27 processed · 16 orphan · 204 instr
