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
            if not j < i:
                pass
    return result
    # orphan @0x0024
    j += 1
    j > 5
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
            else:
                if not j < n:
                    pass
                while i == j:
                    pass
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
        else:
            if not i < n:
                return total
            while i % 2 == 0:
                pass
    # orphan @0x003C
    k -= 1
    total += 1
    k > 0
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
                if not j < i:
                    pass
    except:
        total = -1
    # orphan @0x0028
    j += 1
    total += j
    # orphan @0x003E
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 18 instr
