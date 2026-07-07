def l1_1_if_else_simple():
    x = 1
    if x > 0:
        result = "positive"
    else:
        result = "non-positive"
    return result


def l1_2_if_elif_else():
    x = 0
    if x > 0:
        result = "positive"
    elif x < 0:
        result = "negative"
    else:
        result = "zero"
    return result


def l1_3_ternary():
    a = 1
    cond = True
    x = a if cond else 0
    return x


def l1_4_while_simple():
    i = 0
    total = 0
    while i < 10:
        total += i
        i += 1
    return total


def l1_5_for_range():
    total = 0
    for i in range(10):
        total += i
    return total


def l1_6_for_iterable():
    lst = [1, 2, 3]
    total = 0
    for item in lst:
        total += item
    return total


def l1_7_break_continue():
    i = 0
    total = 0
    while True:
        i += 1
        if i > 10:
            break
        if i % 2 == 0:
            continue
        total += i
    return total


def l1_8_for_else():
    for x in [1, 2, 3]:
        if x == 5:
            break
    else:
        return "not found"
    return "found"


def l1_9_while_else():
    i = 0
    while i < 5:
        if i == 10:
            break
        i += 1
    else:
        return "completed"
    return "broke"


def l1_10_if_no_else():
    x = 1
    if x > 0:
        result = "positive"
    return result


def l1_11_nested_if():
    x = 1
    y = 2
    if x > 0:
        if y > 0:
            result = "both positive"
        else:
            result = "x positive, y non-positive"
    else:
        result = "x non-positive"
    return result
