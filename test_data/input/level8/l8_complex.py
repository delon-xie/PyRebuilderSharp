def l8_1_complex_control_flow():
    result = []
    for i in range(10):
        if i % 2 == 0:
            if i == 0:
                result.append("zero")
            else:
                result.append("even")
        else:
            if i == 1:
                result.append("one")
            elif i == 3:
                result.append("three")
            else:
                result.append("odd")
    return result


def l8_2_loop_with_try():
    total = 0
    for i in range(10):
        try:
            total += 1 / (10 - i)
        except ZeroDivisionError:
            total += 100
    return total


def l8_3_nested_try_except():
    try:
        try:
            1 / 0
        except ZeroDivisionError:
            try:
                1 / 0
            except ZeroDivisionError:
                return "inner-inner"
            return "inner"
    except Exception:
        return "outer"


def l8_4_generator_with_exception():
    def gen():
        for i in range(5):
            try:
                if i == 3:
                    raise ValueError("test")
                yield i
            except ValueError:
                yield "error"
    return list(gen())


def l8_5_decorator_chain():
    def decorator1(func):
        def wrapper(*args):
            return "1-" + func(*args)
        return wrapper

    def decorator2(func):
        def wrapper(*args):
            return "2-" + func(*args)
        return wrapper

    @decorator1
    @decorator2
    def f(x):
        return str(x)
    return f(42)


def l8_6_class_with_complex_methods():
    class Calculator:
        def __init__(self):
            self._value = 0

        def add(self, x):
            self._value += x
            return self

        def subtract(self, x):
            self._value -= x
            return self

        @classmethod
        def create(cls, initial):
            obj = cls()
            obj._value = initial
            return obj

        @property
        def value(self):
            return self._value
    return Calculator.create(10).add(5).subtract(3).value


def l8_7_list_comprehension_with_condition():
    data = [(i, i * 2) for i in range(20) if i % 3 == 0]
    return data


def l8_8_dict_comprehension_nested():
    matrix = [[1, 2], [3, 4], [5, 6]]
    result = {i: {j: matrix[i][j] for j in range(len(matrix[i]))} for i in range(len(matrix))}
    return result


def l8_9_async_with_exception():
    async def safe_divide(a, b):
        try:
            if b == 0:
                raise ValueError("division by zero")
            return a / b
        except ValueError as e:
            return str(e)
    return "async"


def l8_10_metaclass_with_decorator():
    class Meta(type):
        def __new__(cls, name, bases, attrs):
            for key, value in attrs.items():
                if callable(value) and not key.startswith("_"):
                    attrs[key] = lambda func: (lambda *args, **kwargs: func(*args, **kwargs) + 1)(value)
            return super().__new__(cls, name, bases, attrs)

    class Example(metaclass=Meta):
        def method(self):
            return 10
    return Example().method()


def l8_11_recursive_generator():
    def fibonacci(n):
        if n <= 0:
            return
        if n == 1:
            yield 0
            return
        if n == 2:
            yield 0
            yield 1
            return
        a, b = 0, 1
        yield a
        yield b
        for _ in range(n - 2):
            a, b = b, a + b
            yield b
    return list(fibonacci(10))


def l8_12_context_manager_chaining():
    class CM1:
        def __enter__(self):
            return "cm1"
        def __exit__(self, *args):
            pass

    class CM2:
        def __enter__(self):
            return "cm2"
        def __exit__(self, *args):
            pass

    with CM1() as c1, CM2() as c2:
        result = c1 + "-" + c2
    return result


def l8_13_property_with_validation():
    class Person:
        def __init__(self):
            self._age = 0

        @property
        def age(self):
            return self._age

        @age.setter
        def age(self, value):
            if not isinstance(value, int):
                raise TypeError("age must be int")
            if value < 0:
                raise ValueError("age must be positive")
            self._age = value
    p = Person()
    p.age = 25
    return p.age


def l8_14_lambda_closure_complex():
    def create_multipliers():
        return [lambda x, i=i: x * i for i in range(5)]

    multipliers = create_multipliers()
    return [m(2) for m in multipliers]


def l8_15_exception_handling_with_finally():
    def process(items):
        result = []
        for item in items:
            try:
                result.append(int(item))
            except ValueError:
                result.append("error")
            finally:
                result.append("done")
        return result
    return process(["1", "abc", "3"])
