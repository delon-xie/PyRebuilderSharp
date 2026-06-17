# Decompiled from: <module>

def depth_5_if(x0, x1, x2, x3, x4):
    result = 0
    if (x0 == 0) and (x1 == 1) and (x2 == 2) and (x3 == 3) and (x4 == 4):
        result = 42
    return
    result = 41
    result = 40
    result = 30
    result = 20
    # orphan @0x0074
    result = 10
def depth_5_for():
    total = 0
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    for e in range(2):
                        total += 1
def depth_5_while():
    total = 0
    while a == 0:
        return None
    a -= 1
    while b == 0:
        b -= 1
        while c == 0:
            c -= 1
            while d == 0:
                d -= 1
                while e == 0:
                    e -= 1
                    total += 1
    # [WARN] 5 instructions not decompiled
    #   @0x003C: JUMP_BACKWARD arg=54
    #   @0x0064: JUMP_BACKWARD arg=58
    #   @0x008C: JUMP_BACKWARD arg=58
    #   @0x00B4: JUMP_BACKWARD arg=58
    #   @0x00DC: JUMP_BACKWARD arg=58
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
