# Decompiled from: <module>

for line in lines:
    clean_line = remove_ansi(line)
    line_stripped = clean_line.strip()
    if line_stripped.startswith('*** ') and current_test and current_test_fail:
        print(f"✗ {current_test}")
        failed += 1
        print(f"✓ {current_test}")
        passed += 1
        current_test = line_stripped[4:].split(':')[0]
        current_test_fail = False
        if 'FAIL' in line_stripped:
            current_test_fail = True
    print('============================================================')
    print(f"总计: {passed} PASS, {failed} FAIL")
    print('============================================================')
    if not current_test:
        pass
    if not '3.10.pyc' in clean_line:
        pass
    if 'FAIL' in clean_line:
        pass
    if not 'Bad MAGIC' in clean_line:
        pass
    current_test_fail = True
    if current_test and current_test_fail:
        print(f"✗ {current_test}")
        failed += 1
        print(f"✓ {current_test}")
        passed += 1
# [WARN] 6 instructions not decompiled
#   @0x01EC: JUMP_BACKWARD arg=0
#   @0x01F0: JUMP_BACKWARD arg=0
#   @0x0204: JUMP_BACKWARD arg=0
#   @0x0216: JUMP_BACKWARD arg=0
#   @0x0244: JUMP_BACKWARD arg=0
#   @0x024C: JUMP_BACKWARD arg=0
# [SUMMARY] 33 blocks · 34 processed · 2 orphan · 204 instr
