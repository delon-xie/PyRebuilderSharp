# Decompiled from: <module>

def depth_5_if(x0, x1, x2, x3, x4):
    result = 0
    if (x0 > 0) and (x1 > 1) and (x2 > 2) and (x3 > 3) and (x4 > 4):
        result = 42
    result = 41
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
                        continue
def depth_5_try():
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
