# Decompiled from: <module>

def depth_5_if(x0, x1, x2, x3, x4):
    result = 0
    if (x0 > 0) and (x1 > 1) and (x2 > 2) and (x3 > 3) and (x4 > 4):
        result = 42
        return None
    result = 41
    result = 40
    result = 30
    result = 20
    result = 10
def depth_5_for():
    total = 0
    range(2)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    for e in range(2):
                        total += 1
def depth_5_while():
    # orphan @0x002C
    b -= 1
    c = 2
    c > 0
    # orphan @0x0014
    a -= 1
    b = 2
    b > 0
    total = 0
    a = 2
    while a > 0:
        a -= 1
        b = 2
        while b > 0:
            b -= 1
            c = 2
            while c > 0:
                c -= 1
                d = 2
                while d > 0:
                    d -= 1
                    e = 2
                    while e > 0:
                        e -= 1
                        total += 1
                        if e > 0:
                            pass
                        elif d > 0:
                            pass
                        elif c > 0:
                            pass
                        elif b > 0:
                            pass
                        elif a > 0:
                            pass
    # orphan @0x0044
    c -= 1
    d = 2
    d > 0
    # orphan @0x005C
    d -= 1
    e = 2
    e > 0
    # orphan @0x0074
    e -= 1
    total += 1
    e > 0
def depth_5_try():
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
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 14 instr
