def test_for_else_simple():
    for i in range(3):
        pass
    else:
        return "completed"

def test_while_else_simple():
    i = 0
    while i < 3:
        i += 1
    else:
        return "completed"
