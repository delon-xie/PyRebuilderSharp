def test(flag):
    try:
        if flag:
            raise ValueError("test")
    except ValueError as e:
        print(e)
    else:
        print("no error")
    finally:
        print("finally")
