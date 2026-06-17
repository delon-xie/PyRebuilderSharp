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
    # orphan @0x003C
    # orphan @0x0020
    # orphan @0x0000
    total = 0
    # orphan @0x0058
    # orphan @0x0074
    # orphan @0x0090
    total += 1
def depth_5_while():
    # orphan @0x003A
    b -= 1
    c = 2
    # orphan @0x0016
    a -= 1
    b = 2
    # orphan @0x0000
    total = 0
    a = 2
    # orphan @0x0062
    # orphan @0x0078
    d = 2
    # orphan @0x008A
    d -= 1
    e = 2
    # orphan @0x00B2
    # orphan @0x00C8
    total += 1
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
