# Decompiled from: <module>

def depth_5_if(x0, x1, x2, x3, x4):
    result = 0
    if (x0 == 0) and (x1 == 1) and (x2 == 2) and (x3 == 3) and (x4 == 4):
        result = 42
def depth_5_for():
    total = 0
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    for e in range(2):
                        total += 1
                    break
                break
            break
        break
    break
def depth_5_while():
    # orphan @0x004A
    c -= 1
    d = 2
    # orphan @0x0030
    b -= 1
    c = 2
    # orphan @0x0016
    a -= 1
    b = 2
    total = 0
    a = 2
    while a == 0:
        pass
    return None
    # orphan @0x0064
    d -= 1
    e = 2
    # orphan @0x007E
    e -= 1
    total += 1
    # orphan @0x009E
    # orphan @0x00A0
    # orphan @0x00AE
    # orphan @0x00B0
    # orphan @0x00BE
    # orphan @0x00C0
    # orphan @0x00CE
    # orphan @0x00D0
    # orphan @0x00DE
def depth_5_try():
    # orphan @0x001E
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
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 14 instr
