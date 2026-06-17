# Decompiled from: <module>

def mixed_1(n):
    result = 0
    if n > 0:
        for i in range(n):
            j = 0
            if j < i:
                j += 1
                if j > 5:
                    result += j
                    result += 1
            if not j < i:
                pass
    # orphan @0x0050
    return result
def mixed_2(n):
    total = 0
    for i in range(n):
        j = 0
        if j < n:
            j += 1
            if i == j:
                for k in range(i):
                    total += k
        if not j < n:
            pass
    return total
def mixed_3(n):
    total = 0
    i = 0
    if i < n:
        i += 1
        if i % 2 == 0:
            for j in range(i):
                k = j
                if k > 0:
                    k -= 1
                    total += 1
                    if not k > 0:
                        pass
    # orphan @0x0056
    # orphan @0x005E
    return total
def mixed_4(n):
    total = 0
    try:
        if n > 0:
            pass
        elif j < i:
            j += 1
            try:
                total += j
            except:
                pass
        for i in range(n):
            pass
    except:
        total = -1
    # orphan @0x0046
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 18 instr
