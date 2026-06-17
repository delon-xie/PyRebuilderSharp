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
    break
    if not current_test:
        pass
    if not '3.10.pyc' in clean_line:
        pass
    if 'FAIL' in clean_line:
        pass
    if not 'Bad MAGIC' in clean_line:
        pass
    current_test_fail = True
    break
    if current_test and current_test_fail:
        print(f"✗ {current_test}")
        failed += 1
        print(f"✓ {current_test}")
        passed += 1
        print('============================================================')
# [WARN] 6 instructions not decompiled
#   @0x01BE: JUMP_BACKWARD arg=0
#   @0x01C2: JUMP_BACKWARD arg=0
#   @0x01D4: JUMP_BACKWARD arg=0
#   @0x01E4: JUMP_BACKWARD arg=0
#   @0x020C: JUMP_BACKWARD arg=0
#   @0x0214: JUMP_BACKWARD arg=0
# [SUMMARY] 32 blocks · 33 processed · 2 orphan · 204 instr
