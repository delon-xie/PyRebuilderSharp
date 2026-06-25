# Decompiled from: <module>

def mixed_1(n):
    result = 0
    if n > 0:
        for i in range(n):
            j = 0
            while j < i:
                pass
            j += 1
            if j > 5:
                result += j
            else:
                result += 1
    return result

def mixed_2(n):
    total = 0
    for i in range(n):
        j = 0
        while j < n:
            pass
        j += 1
        if not i == j:
            pass
        else:
            for k in range(i):
                total += k
    return total

def mixed_3(n):
    total = 0
    i = 0
    while i < n:
        i += 1
        if not i % 2 == 0:
            pass
        else:
            for j in range(i):
                k = j
                while k > 0:
                    pass
                k -= 1
                total += 1
    return total

def mixed_4(n):
    total = 0
    if n > 0:
        pass
    for i in range(n):
        j = 0
        while i:
            if not True:
                pass
            else:
                j += 1
                total += j
