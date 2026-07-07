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
                else:
                    result += 1
    return result

def mixed_2(n):
    total = 0
    range(n)
    for i in range(n):
        j = 0
        while j < n:
            j += 1
            for k in range(i):
                total += k

def mixed_3(n):
    total = i = 0
    while i < n:
        i += 1
        for j in range(i):
            k = j
            while k > 0:
                k -= 1
                total += 1

def mixed_4(n):
    total = 0
    try:
        if n > 0:
            for i in range(n):
                j = 0
                while j < i:
                    j += 1
                    total += j
    except:
        total = -1
