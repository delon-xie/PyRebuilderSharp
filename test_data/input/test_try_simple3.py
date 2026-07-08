def test():
    try:
        x = 1 + 2
    except ValueError as e:
        print(e)
    else:
        print("no error")
    finally:
        print("finally")
