# Decompiled from: <module>

def depth_5_if(x0, x1, x2, x3, x4):
    result = 0
    if x0 > 0:
        if (x1 > 1) and (x2 > 2) and (x3 > 3) and (x4 > 4):
            result = 42
            return None
    else:
        result = 10
    # orphan @0x005C
    result = 40
    return None
    # orphan @0x006C
    result = 20
def depth_5_for():
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    for e in range(2):
                        total += 1
                        return None
    # [WARN] 5 instructions not decompiled
    #   @0x00A4: JUMP_BACKWARD arg=-2
    #   @0x00AC: JUMP_BACKWARD arg=-2
    #   @0x00B4: JUMP_BACKWARD arg=-2
    #   @0x00BC: JUMP_BACKWARD arg=-2
    #   @0x00C4: JUMP_BACKWARD arg=-2
def depth_5_while():
    # orphan @0x003E
    b -= 1
    c = 2
    total = 0
    a = 2
    if a > 0:
        a -= 1
        b = 2
        if not b > 0:
            pass
        d = 2
        if not d > 0:
            pass
    # orphan @0x0064
    # orphan @0x0066
    # orphan @0x008E
    d -= 1
    # orphan @0x00A4
    # orphan @0x00B4
    # orphan @0x00C8
    total += 1
    return None
    # [WARN] 2 instructions not decompiled
    #   @0x003C: JUMP_BACKWARD arg=0
    #   @0x008C: JUMP_BACKWARD arg=0
def depth_5_try():
    # orphan @0x0020
    try:
        result = 42
    except:
        result = -1
    try:
        result = -2
    except:
        pass
    try:
        result = -3
    except:
        pass
    try:
        result = -4
    except:
        pass
    try:
        result = -5
    except:
        pass
    result = 0
    return None
    return None
    raise
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 15 instr
