def test_for_else_normal():
    for i in range(3):
        if i == 5:
            break
    else:
        return "completed"
    return "broke"

def test_for_else_break():
    for i in range(3):
        if i == 1:
            break
    else:
        return "completed"
    return "broke"

def test_for_else_empty():
    for i in []:
        pass
    else:
        return "empty"
    return "not empty"

def test_for_no_else():
    total = 0
    for i in range(5):
        total += i
    return total

def test_while_else_normal():
    i = 0
    while i < 3:
        if i == 5:
            break
        i += 1
    else:
        return "completed"
    return "broke"

def test_while_else_break():
    i = 0
    while i < 3:
        if i == 1:
            break
        i += 1
    else:
        return "completed"
    return "broke"

def test_while_no_else():
    i = 0
    total = 0
    while i < 5:
        total += i
        i += 1
    return total