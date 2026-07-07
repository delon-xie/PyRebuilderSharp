def l6_1_generator_function():
    def gen():
        yield 1
        yield 2
        yield 3
    return list(gen())


def l6_2_generator_expression():
    g = (x * x for x in range(10))
    return list(g)


def l6_3_list_comprehension():
    result = [x * x for x in range(10) if x % 2 == 0]
    return result


def l6_4_dict_set_comprehension():
    items = [(1, 'a'), (2, 'b')]
    d = {k: v for k, v in items}
    s = {x for x in range(5)}
    return d, s


def l6_5_nested_comprehension():
    result = [[x + y for x in range(3)] for y in range(3)]
    return result


def l6_6_async_await():
    async def f():
        return 42

    async def g():
        result = await f()
        return result + 1
    return "async"


def l6_7_walrus_operator():
    items = [1, 2, 3]
    if (n := len(items)) > 0:
        return n
    return 0


def l6_8_match_case():
    def match_value(value):
        match value:
            case 1:
                return "one"
            case 2:
                return "two"
            case _:
                return "other"
    return match_value(1)


def l6_9_dataclass():
    from dataclasses import dataclass
    @dataclass
    class Point:
        x: int
        y: int
    p = Point(1, 2)
    return p.x, p.y


def l6_10_enum():
    from enum import Enum
    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3
    return Color.RED.value


def l6_11_context_manager():
    class CM:
        def __init__(self, name):
            self.name = name
        def __enter__(self):
            return self.name
        def __exit__(self, *args):
            pass

    with CM("test") as val:
        result = val
    return result


def l6_12_decorator_with_args():
    def repeat(times):
        def decorator(func):
            def wrapper(*args):
                results = []
                for _ in range(times):
                    results.append(func(*args))
                return results
            return wrapper
        return decorator

    @repeat(3)
    def f(x):
        return x * 2
    return f(5)


def l6_13_property_with_decorator():
    class A:
        def __init__(self):
            self._value = 0

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, v):
            self._value = v

        @value.deleter
        def value(self):
            self._value = -1
    a = A()
    a.value = 42
    del a.value
    return a.value


def l6_14_classmethod_chaining():
    class Builder:
        def __init__(self):
            self.value = 0

        @classmethod
        def create(cls):
            return cls()

        def add(self, x):
            self.value += x
            return self

        def build(self):
            return self.value
    return Builder.create().add(1).add(2).build()


def l6_15_lambda_in_comprehension():
    funcs = [lambda x, i=i: x + i for i in range(5)]
    return [f(1) for f in funcs]
