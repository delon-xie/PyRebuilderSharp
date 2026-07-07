def test_if_else_simple():
    x = 1
    if x > 0:
        result = "positive"
    else:
        result = "non-positive"
    return result

def test_if_elif_else():
    x = 0
    if x > 0:
        result = "positive"
    elif x < 0:
        result = "negative"
    else:
        result = "zero"
    return result

def test_if_no_else():
    x = 1
    if x > 0:
        result = "positive"
    return result

def test_nested_if_else():
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

def test_if_return_in_body():
    x = 1
    if x > 0:
        return "positive"
    else:
        return "non-positive"