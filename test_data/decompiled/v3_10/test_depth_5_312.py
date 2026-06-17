# Decompiled from: <module>

def depth_5_if(x0, x1, x2, x3, x4):
    result = 0
    if x0 > 0:
        if x1 > 1:
            if x2 > 2:
                if x3 > 3:
                    if x4 > 4:
                        result = 42
                        return None
    # orphan @0x0034
    result = 41
    return None
    # orphan @0x003C
    result = 40
    return None
    # orphan @0x0044
    result = 30
    return None
    # orphan @0x004C
    result = 20
    return None
    # orphan @0x0054
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
    a = 2
    if a > 0:
        a -= 1
        b = 2
        if b > 0:
            b -= 1
            c = 2
            if c > 0:
                c -= 1
                d = 2
                if d > 0:
                    d -= 1
                    e = 2
                    if e > 0:
                        e -= 1
                        total += 1
                        if not e > 0:
                            if not d > 0:
                                if not c > 0:
                                    if not b > 0:
                                        if not a > 0:
                                            pass
def depth_5_try():
    # orphan @0x0022
    # orphan @0x0016
    result = -1
    result = 0
    try:
        try:
            try:
                try:
                    try:
                        result = 42
                    except:
                        return None
                        result = -4
                except:
                    return None
                    result = -4
            except:
                return None
                result = -4
        except:
            result = -5
    except:
        result = -5
    # orphan @0x0026
    result = -2
    # orphan @0x0032
    # orphan @0x0036
    result = -3
    return None
    # orphan @0x0052
    result = -4
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 18 instr
