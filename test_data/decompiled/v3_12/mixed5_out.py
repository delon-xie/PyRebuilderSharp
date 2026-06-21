# Decompiled from: <module>

def mixed_1(n):
    result = 0
    if n > 0:
        for i in range(n):
            j = 0
            if not j < i:
                pass
            while j > 5:
                result += 1
                if j < i:
                    pass
            result += j
    return result
    # orphan @0x0074
    # [WARN] 3 instructions not decompiled
    #   @0x003A: JUMP_BACKWARD arg=22
    #   @0x0070: JUMP_BACKWARD arg=54
    #   @0x0072: JUMP_BACKWARD arg=78
def mixed_2(n):
    total = 0
    range(n)
    for i in range(n):
        j = 0
        if not j < n:
            pass
        while i == j:
            if j < n:
                pass
        range(i)
        for k in range(i):
            total += k
    return total
    # [WARN] 4 instructions not decompiled
    #   @0x0030: JUMP_BACKWARD arg=22
    #   @0x006C: JUMP_BACKWARD arg=18
    #   @0x007A: JUMP_BACKWARD arg=74
    #   @0x007C: JUMP_BACKWARD arg=98
def mixed_3(n):
    # orphan @0x0014
    i += 1
    i % 2 == 0
    total = 0
    i = 0
    while i < n:
        i += 1
        if i % 2 == 0:
            for j in range(i):
                k = j
                if not k > 0:
                    pass
                while k > 0:
                    pass
        else:
            if i < n:
                pass
            return total
    # orphan @0x007C
    # [WARN] 4 instructions not decompiled
    #   @0x0058: JUMP_BACKWARD arg=22
    #   @0x0078: JUMP_BACKWARD arg=32
    #   @0x007A: JUMP_BACKWARD arg=56
    #   @0x0088: JUMP_BACKWARD arg=118
def mixed_4(n):
    try:
        try:
            try:
                try:
                    range(n)
                    for i in range(n):
                        try:
                            j = 0
                        except:
                            break
                        j += 1
                        try:
                            total += j
                        except:
                            break
                        if j < i:
                            pass
                        raise
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
    # orphan @0x0068
    # orphan @0x0082
    # [WARN] 4 instructions not decompiled
    #   @0x003E: JUMP_BACKWARD arg=22
    #   @0x0060: JUMP_BACKWARD arg=34
    #   @0x0062: JUMP_BACKWARD arg=58
    #   @0x006E: JUMP_BACKWARD arg=26
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 14 instr
