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
    else:
        return result
def mixed_2(n):
    total = 0
    range(n)
    for i in range(n):
        j = 0
        while j < n:
            j += 1
    return total
def mixed_3(n):
    total = 0
    i = 0
    while i < n:
        i += 1
    return total
    k = j
def mixed_4(n):
    total = 0
    try:
        if n > 0:
            pass
        else:
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
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 14 instr
