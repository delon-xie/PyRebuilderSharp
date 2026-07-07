def l5_1_empty_class():
    class A:
        pass
    return A


def l5_2_class_with_attrs():
    class A:
        x = 1
        def __init__(self):
            self.y = 2
    a = A()
    return a.x, a.y


def l5_3_inheritance():
    class A:
        pass
    class B(A):
        pass
    return B


def l5_4_super_method():
    class A:
        def method(self):
            return 1
    class B(A):
        def method(self):
            return super().method() + 1
    b = B()
    return b.method()


def l5_5_classmethod_staticmethod():
    class A:
        @classmethod
        def cls_method(cls):
            return cls.__name__
        @staticmethod
        def static_method():
            return "static"
    return A.cls_method(), A.static_method()


def l5_6_property():
    class A:
        def __init__(self):
            self._x = 0

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, value):
            self._x = value
    a = A()
    a.x = 42
    return a.x


def l5_7_metaclass():
    class Meta(type):
        pass
    class A(metaclass=Meta):
        pass
    return type(A).__name__


def l5_8_multiple_inheritance():
    class A:
        pass
    class B:
        pass
    class C(A, B):
        pass
    return C.__mro__


def l5_9_method_override():
    class A:
        def method(self):
            return "A"
    class B(A):
        def method(self):
            return "B"
    b = B()
    return b.method()


def l5_10_private_attributes():
    class A:
        def __init__(self):
            self.__private = 42
            self.public = 100
    a = A()
    return a.public


def l5_11_class_variables():
    class A:
        count = 0
        def __init__(self):
            A.count += 1
    a1 = A()
    a2 = A()
    return A.count


def l5_12_slots():
    class A:
        __slots__ = ('x', 'y')
        def __init__(self):
            self.x = 1
            self.y = 2
    a = A()
    return a.x, a.y


def l5_13_descriptors():
    class Descriptor:
        def __get__(self, obj, objtype):
            return 42
    class A:
        attr = Descriptor()
    a = A()
    return a.attr


def l5_14_abc():
    from abc import ABC, abstractmethod
    class Base(ABC):
        @abstractmethod
        def method(self):
            pass
    class Concrete(Base):
        def method(self):
            return "implemented"
    c = Concrete()
    return c.method()


def l5_15_class_decorator():
    def decorator(cls):
        cls.decorated = True
        return cls
    @decorator
    class A:
        pass
    return A.decorated
