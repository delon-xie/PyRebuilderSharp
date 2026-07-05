def test_or_expr():
    x = 1
    return x or x

def test_or_chain():
    return True or False or True

def test_and_chain():
    return True and False and True

def test_complex_bool():
    a = hasattr(x, 'get')
    b = hasattr(x, 'set')
    c = hasattr(x, 'delete')
    return a or b or c
