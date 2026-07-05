def simple_comps():
    a = [x for x in range(5)]
    b = [x for x in range(10) if x % 2 == 0]
    c = [x * 2 + 1 for x in range(5)]
    return a, b, c
