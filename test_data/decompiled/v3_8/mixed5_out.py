# Decompiled from: <module>

def mixed_1(n):
    result = 0
    if n > 0:
        for i in range(n):
            j = 0
            while j < i:
                j += 1
                if j > 5:
                    result += j
                result += 1
                continue

def mixed_2(n):
    total = 0
    range(n)
    for i in range(n):
        j = 0
        while j < n:
            j += 1
            if i == j:
                for k in range(i):
                    total += k
            continue
    return total

def mixed_3(n):
    total = 0
    i = 0
    while i < n:
        i += 1
        if i % 2 == 0:
            for j in range(i):
                k = j
                while k > 0:
                    k -= 1
                    total += 1
                    continue
        for _ in range(i):
            pass
    return total

def mixed_4(n):
    total = 0
    try:
        if n > 0:
            for i in range(n):
                j = 0
                while j < i:
                    j += 1
                    try:
                        total += j
                    except:
                        pass
                    continue
    except:
        total = -1
