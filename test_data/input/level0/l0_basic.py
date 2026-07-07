def l0_1_constants():
    a = 42
    b = 3.14
    c = "hello"
    d = 'world'
    e = 0
    f = -1
    return a, b, c, d, e, f


def l0_2_bool_none():
    x = True
    y = False
    z = None
    return x, y, z


def l0_3_arithmetic():
    a = 1
    b = 2
    c = 3
    result = a + b * c
    result2 = (a + b) * c
    result3 = a - b
    result4 = a / b
    result5 = a // b
    result6 = a % b
    result7 = a ** b
    return result, result2, result3, result4, result5, result6, result7


def l0_4_comparison():
    a = 1
    b = 2
    c = 3
    d = 4
    result1 = a > b
    result2 = c <= d
    result3 = a > b and c <= d
    result4 = a > b or c <= d
    result5 = not result1
    return result1, result2, result3, result4, result5


def l0_5_containers():
    lst = [1, 2, 3]
    lst2 = []
    d = {"a": 1, "b": 2}
    d2 = {}
    s = {1, 2, 3}
    s2 = set()
    t = (1, 2, 3)
    t2 = tuple()
    return lst, lst2, d, d2, s, s2, t, t2


def l0_6_slicing():
    s = "hello world"
    result1 = s[1:10]
    result2 = s[1:10:2]
    result3 = s[:5]
    result4 = s[5:]
    result5 = s[::-1]
    return result1, result2, result3, result4, result5


def l0_7_attr_access():
    class Obj:
        def __init__(self):
            self.value = 42

        def method(self, arg):
            return self.value + arg

    obj = Obj()
    attr = obj.value
    result = obj.method(10)
    return attr, result
