def test(should_raise):
    try:
        if should_raise:
            raise ValueError("test")
    except ValueError as e:
        print(e)
    else:
        print("no error")
    finally:
        print("finally")
