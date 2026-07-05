"""Abstract Base Classes (ABCs) according to PEP 3119."""

def abstractmethod(funcobj):
    funcobj.__isabstractmethod__ = True
    return funcobj

class abstractclassmethod(classmethod):
    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super().__init__(callable)

try:
    from _abc import get_cache_token, _abc_init
except ImportError:
    from _py_abc import ABCMeta, get_cache_token
else:
    class ABCMeta(type):
        def __new__(mcls, name, bases, namespace, /, **kwargs):
            cls = super().__new__(mcls, name, bases, namespace, **kwargs)
            _abc_init(cls)
            return cls
