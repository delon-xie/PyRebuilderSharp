"""Abstract Base Classes (ABCs) according to PEP 3119."""

def abstractmethod(funcobj):
    funcobj.__isabstractmethod__ = True
    return funcobj

class abstractclassmethod(classmethod):
    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super().__init__(callable)
