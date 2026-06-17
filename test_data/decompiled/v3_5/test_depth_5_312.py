# Decompiled from: <module>

def depth_5_if(x0, x1, x2, x3, x4):
    result = 0
    if x0 > 0:
        if x1 > 1:
            if x2 > 2:
                if x3 > 3:
                    if x4 > 4:
                        result = 42
                    else:
                        result = 41
                else:
                    result = 40
            else:
                result = 30
        else:
            result = 20
    else:
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
def depth_5_try():
    # orphan @0x001E
    result = -1
    result = 0
    try:
        try:
            try:
                try:
                    try:
                        result = 42
                    except:
                        pass
                except:
                    pass
            except:
                pass
        except:
            pass
    except:
        result = -5
    # orphan @0x002C
    # orphan @0x0030
    result = -2
    # orphan @0x003E
    # orphan @0x0042
    result = -3
    # orphan @0x0050
    # orphan @0x0054
    result = -4
    # orphan @0x0062
    # orphan @0x0066
    result = -5
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 18 instr
