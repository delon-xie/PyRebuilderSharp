def l9_1_full_app_pattern():
    class DatabaseConnection:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self._connected = False

        def connect(self):
            self._connected = True

        def disconnect(self):
            self._connected = False

        def __enter__(self):
            self.connect()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.disconnect()

        def query(self, sql):
            if not self._connected:
                raise RuntimeError("Not connected")
            return f"Querying: {sql}"

    def process_data(db: DatabaseConnection, queries):
        results = []
        for sql in queries:
            try:
                result = db.query(sql)
                if result:
                    results.append(result)
                else:
                    results.append("empty")
            except RuntimeError as e:
                results.append(f"Error: {e}")
            except Exception as e:
                results.append(f"Unexpected: {e}")
        return results

    with DatabaseConnection("localhost", 5432) as db:
        queries = ["SELECT * FROM users", "SELECT * FROM orders", "INVALID SQL"]
        return process_data(db, queries)


def l9_2_comprehensive_decorator():
    def logging_decorator(log_level="INFO"):
        def decorator(func):
            import functools
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(f"[{log_level}] Calling {func.__name__}")
                try:
                    result = func(*args, **kwargs)
                    print(f"[{log_level}] {func.__name__} returned {result}")
                    return result
                except Exception as e:
                    print(f"[{log_level}] {func.__name__} raised {e}")
                    raise
            return wrapper
        return decorator

    @logging_decorator(log_level="DEBUG")
    def complex_calculation(a, b, c=10):
        if a > b:
            result = a * b
        else:
            result = a + b
        result += c
        if result > 100:
            raise ValueError("Result too big")
        return result

    try:
        return complex_calculation(10, 20, c=5)
    except ValueError:
        return "error"


def l9_3_stateful_generator():
    class StatefulGenerator:
        def __init__(self, initial):
            self.state = initial

        def generate(self):
            while self.state < 100:
                yield self.state
                self.state *= 2
                if self.state == 0:
                    raise StopIteration("Cannot generate")

        def reset(self, value):
            self.state = value

    gen = StatefulGenerator(1)
    results = list(gen.generate())
    gen.reset(10)
    results.extend(list(gen.generate()))
    return results


def l9_4_metaclass_factory():
    def create_factory(base_class):
        class FactoryMeta(type):
            def __new__(cls, name, bases, attrs):
                attrs['create'] = classmethod(
                    lambda cls, *args, **kwargs: cls(*args, **kwargs)
                )
                return super().__new__(cls, name, bases, attrs)

        class Factory(base_class, metaclass=FactoryMeta):
            pass
        return Factory

    class Product:
        def __init__(self, name, price):
            self.name = name
            self.price = price

    ProductFactory = create_factory(Product)
    return ProductFactory.create("Test", 99.99).name


def l9_5_nested_context_managers():
    class ResourceManager:
        def __init__(self, name):
            self.name = name

        def __enter__(self):
            return f"Entered {self.name}"

        def __exit__(self, *args):
            pass

    with ResourceManager("A") as a, \
         ResourceManager("B") as b, \
         ResourceManager("C") as c:
        return f"{a}, {b}, {c}"


def l9_6_complex_type_hints():
    from typing import List, Dict, Optional, Union, Any, Callable

    def process_data(
        items: List[Dict[str, Union[int, str]]],
        transform: Optional[Callable[[Any], Any]] = None
    ) -> Dict[str, List[Any]]:
        result: Dict[str, List[Any]] = {}
        for item in items:
            key = str(item.get("id", "unknown"))
            if key not in result:
                result[key] = []
            value = item.get("value")
            if transform:
                value = transform(value)
            result[key].append(value)
        return result

    data = [{"id": 1, "value": 10}, {"id": 2, "value": "test"}]
    return process_data(data, transform=lambda x: str(x) if x else "none")


def l9_7_recursive_decorator():
    def recursive_decorator(max_depth=3):
        def decorator(func):
            depth = 0
            def wrapper(*args):
                nonlocal depth
                depth += 1
                if depth > max_depth:
                    return "max depth"
                if args[0] == 0:
                    depth = 0
                    return 1
                result = func(*args)
                depth -= 1
                return result
            return wrapper
        return decorator

    @recursive_decorator(max_depth=5)
    def fib(n):
        return fib(n - 1) + fib(n - 2)

    return fib(5)


def l9_8_async_generator():
    async def async_range(n):
        for i in range(n):
            yield i

    async def process():
        results = []
        async for num in async_range(5):
            results.append(num * 2)
        return results
    return "async generator"


def l9_9_dynamic_class_creation():
    def create_class(class_name, methods):
        class_dict = {}
        for name, func in methods.items():
            class_dict[name] = func

        new_class = type(class_name, (object,), class_dict)
        return new_class

    methods = {
        '__init__': lambda self, x: setattr(self, 'x', x),
        'get_x': lambda self: self.x,
        'set_x': lambda self, x: setattr(self, 'x', x),
    }

    DynamicClass = create_class("Dynamic", methods)
    instance = DynamicClass(42)
    instance.set_x(100)
    return instance.get_x()


def l9_10_full_stack_application():
    class Configuration:
        def __init__(self, **kwargs):
            self._config = kwargs

        def get(self, key, default=None):
            return self._config.get(key, default)

    class Service:
        def __init__(self, config):
            self.config = config

        def process(self, data):
            result = []
            for item in data:
                try:
                    if self.config.get("validate", True):
                        if not isinstance(item, int):
                            raise ValueError(f"Invalid type: {type(item)}")
                    result.append(item * self.config.get("multiplier", 2))
                except ValueError as e:
                    result.append(f"Validation error: {e}")
            return result

    def main():
        config = Configuration(validate=True, multiplier=3)
        service = Service(config)
        data = [1, 2, "3", 4, 5]
        return service.process(data)

    return main()
