def test1():
    try:
        x = 1
    finally:
        x = 2

def test2():
    try:
        for i in range(5):
            pass
    except:
        pass

def test3():
    try:
        a = 1
    except ValueError:
        a = 2
    except TypeError:
        a = 3
