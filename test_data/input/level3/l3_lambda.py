def l3_1_simple_lambda():
    f = lambda x: x + 1
    return f(1)


def l3_2_lambda_capture():
    outer_var = 10
    f = lambda: outer_var
    return f()


def l3_3_lambda_defaults():
    f = lambda x, y=10: x + y
    return f(5)


def l3_4_lambda_as_param():
    lst = [(2, 'b'), (1, 'a'), (3, 'c')]
    result = sorted(lst, key=lambda x: x[0])
    return result


def l3_5_nested_lambda():
    f = lambda x: lambda y: x + y
    g = f(10)
    return g(5)


def l3_6_lambda_varargs():
    f = lambda *args, **kwargs: sum(args) + len(kwargs)
    return f(1, 2, 3, a=1, b=2)


def l3_7_lambda_multiple_params():
    f = lambda a, b, c: a + b + c
    return f(1, 2, 3)


def l3_8_lambda_in_dict():
    ops = {
        'add': lambda x, y: x + y,
        'sub': lambda x, y: x - y,
    }
    return ops['add'](1, 2)


def l3_9_lambda_return():
    def wrapper():
        return lambda: 42
    f = wrapper()
    return f()


def l3_10_lambda_conditional():
    f = lambda x: x if x > 0 else 0
    return f(-5)
