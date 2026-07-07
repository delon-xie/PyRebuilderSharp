# Decompiled from: <module>

def depth_5_if(x0, x1, x2, x3, x4):
    result = 0
    if x0 > 0:
        if x1 > 1:
            if x2 > 2:
                if x3 > 3:
                    return (x4 > 4) and None
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
        pass

def depth_5_while():
    total = 0
    a = 2
    while a > 0:
        a -= 1
        b = 2
        while b > 0:
            pass
        b -= 1
        c = 2
        while c > 0:
            pass
        c -= 1
        d = 2
        while d > 0:
            pass
        d -= 1
        e = 2
        while e > 0:
            pass
        e -= 1
        total += 1

def depth_5_try():
    result = 0
    try:
        result = 42
    except:
        result = -1
