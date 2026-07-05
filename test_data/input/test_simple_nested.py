def simple_test():
    a = [x for x in range(5)]
    b = [x for x in range(10) if x % 2 == 0]
    c = [x * 2 + 1 for x in range(5)]
    nested = [x for row in [[1,2,3], [4,5,6]] for x in row]
    return a, b, c, nested
