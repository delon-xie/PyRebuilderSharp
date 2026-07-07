def l7_1_empty_function():
    def f():
        pass
    return f


def l7_2_empty_class():
    class A:
        pass
    return A


def l7_3_deep_nesting():
    def nested():
        if True:
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                if True:
                                    if True:
                                        if True:
                                            if True:
                                                return 42
    return nested()


def l7_4_dead_code():
    return 1
    x = 2
    return x


def l7_5_constant_folding():
    x = 1 + 2
    y = "hello" + "world"
    z = True and False
    return x, y, z


def l7_6_unicode_identifiers():
    def 函数():
        变量 = "你好"
        return 变量
    return 函数()


def l7_7_exec_eval():
    exec("result = 1 + 2")
    return eval("3 + 4")


def l7_8_pass_statement():
    def f():
        pass
    return f()


def l7_9_continue_only():
    i = 0
    while i < 10:
        i += 1
        continue


def l7_10_break_only():
    while True:
        break


def l7_11_return_none():
    def f():
        return None
    return f()


def l7_12_multiple_returns():
    def f(x):
        if x > 0:
            return "positive"
        if x < 0:
            return "negative"
        return "zero"
    return f(0)


def l7_13_nested_loops():
    total = 0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                total += i + j + k
    return total


def l7_14_complex_expression():
    result = (((((1 + 2) * 3) - 4) / 5) ** 2) * 3 - 1
    return result


def l7_15_empty_return():
    def f():
        return
    return f()


def l7_16_conditional_return():
    def f(x):
        if x:
            return
        return 42
    return f(False)


def l7_17_global_assignment():
    global_var = 10
    def f():
        global global_var
        global_var = 20
    f()
    return global_var


def l7_18_nonlocal_assignment():
    def outer():
        x = 10
        def inner():
            nonlocal x
            x = 20
        inner()
        return x
    return outer()


def l7_19_empty_tuple_unpacking():
    a, b = (1, 2)
    return a, b


def l7_20_multiple_assignment():
    a = b = c = 1
    return a, b, c
