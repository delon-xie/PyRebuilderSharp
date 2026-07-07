def l4_1_no_args():
    return 42


def l4_2_positional_args(a, b=10):
    return a + b


def l4_3_varargs(*args, **kwargs):
    return len(args) + len(kwargs)


def l4_4_annotations(x: int, y: str) -> bool:
    return isinstance(x, int) and isinstance(y, str)


def l4_5_closure():
    def outer(x):
        def inner(y):
            return x + y
        return inner
    return outer(10)(5)


def l4_6_nonlocal():
    def outer():
        x = 1
        def inner():
            nonlocal x
            x += 1
            return x
        return inner()
    return outer()


def l4_7_global():
    x = 0
    def f():
        global x
        x += 1
        return x
    return f()


def l4_8_recursive():
    def fact(n):
        return 1 if n <= 1 else n * fact(n - 1)
    return fact(5)


def l4_9_decorator():
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) + 1
        return wrapper

    @decorator
    def f(x):
        return x
    return f(5)


def l4_10_nested_functions():
    def outer():
        x = 1
        def middle():
            y = 2
            def inner():
                return x + y
            return inner()
        return middle()
    return outer()


def l4_11_kwargs_only():
    def f(a, *, b):
        return a + b
    return f(1, b=2)


def l4_12_positional_only():
    def f(a, b, /, c):
        return a + b + c
    return f(1, 2, c=3)


def l4_13_return_none():
    def f():
        return
    return f()


def l4_14_docstring():
    def f():
        """This is a docstring"""
        return 42
    return f()


def l4_15_function_attributes():
    def f():
        pass
    f.attr = 42
    return f.attr
