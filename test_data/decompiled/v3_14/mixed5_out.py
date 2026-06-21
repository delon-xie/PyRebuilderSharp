# Decompiled from: <module>

def mixed_1(n):
    result = 0
    if n > 0:
        for i in range(n):
            j = 0
            while i < j:
                pass
            j += 1
            if j > 5:
                result = j + result
            else:
                result += 1
    return result
    # orphan @0x008E
    # [WARN] 3 instructions not decompiled
    #   @0x0040: JUMP_BACKWARD arg=42
    #   @0x0074: JUMP_BACKWARD arg=52
    #   @0x008A: JUMP_BACKWARD arg=52
def mixed_2(n):
    total = 0
    range(n)
    for i in range(n):
        j = 0
        while n < j:
            pass
        j += 1
        if not j == i:
            pass
        else:
            range(i)
        for k in range(i):
            total = k + total
    return total
    # [WARN] 4 instructions not decompiled
    #   @0x0032: JUMP_BACKWARD arg=28
    #   @0x0054: JUMP_BACKWARD arg=38
    #   @0x0084: JUMP_BACKWARD arg=110
    #   @0x008C: JUMP_BACKWARD arg=38
def mixed_3(n):
    total = 0
    i = 0
    while n < i:
        i += 1
        if not i % 2 == 0:
            pass
        else:
            range(i)
        for j in range(i):
            k = j
            while k > 0:
                pass
            k -= 1
            total += 1
    return total
    # [WARN] 4 instructions not decompiled
    #   @0x0044: JUMP_BACKWARD arg=10
    #   @0x0076: JUMP_BACKWARD arg=94
    #   @0x009E: JUMP_BACKWARD arg=104
    #   @0x00A6: JUMP_BACKWARD arg=10
def mixed_4(n):
    try:
        try:
            try:
                try:
                    range(n)
                    for i in range(n):
                        try:
                            j = 0
                            while j:
                                try:
                                    pass
                                except:
                                    break
                                j += 1
                                try:
                                    total = j + total
                                except:
                                    break
                                return None
                                raise
                                raise
                        except:
                            break
                    return None
                except:
                    break
            except:
                break
        except:
            break
    except:
        break
    total = 0
    # orphan @0x0078
    # [WARN] 3 instructions not decompiled
    #   @0x0044: JUMP_BACKWARD arg=46
    #   @0x006C: JUMP_BACKWARD arg=56
    #   @0x007E: JUMP_BACKWARD arg=56
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 15 instr
