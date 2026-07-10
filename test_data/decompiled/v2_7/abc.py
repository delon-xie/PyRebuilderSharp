# Decompiled from: <module>

class _C:
    pass

class abstractproperty:
    """A decorator indicating abstract properties.

    Requires that the metaclass is ABCMeta or derived from it.  A
    class that has a metaclass derived from ABCMeta cannot be
    instantiated unless all of its abstract properties are overridden.
    The abstract properties can be called using any of the normal
    'super' call mechanisms.

    Usage:

        class C:
            __metaclass__ = ABCMeta
            @abstractproperty
            def my_abstract_property(self):
                ...

    This defines a read-only property; you can also define a read-write
    abstract property using the 'long' form of property declaration:

        class C:
            __metaclass__ = ABCMeta
            def getx(self): ...
            def setx(self, value): ...
            x = abstractproperty(getx, setx)
    """
    __isabstractmethod__ = True

def ABCMeta():
    """Metaclass for defining Abstract Base Classes (ABCs).

    Use this metaclass to create an ABC.  An ABC can be subclassed
    directly, and then acts as a mix-in class.  You can also register
    unrelated concrete classes (even built-in classes) and unrelated
    ABCs as 'virtual subclasses' -- these and their descendants will
    be considered subclasses of the registering ABC by the built-in
    issubclass() function, but the registering ABC won't show up in
    their MRO (Method Resolution Order) nor will method
    implementations defined by the registering ABC be callable (not
    even via super()).

    """
    __module__ = __name__
    __doc__ = """Metaclass for defining Abstract Base Classes (ABCs).

    Use this metaclass to create an ABC.  An ABC can be subclassed
    directly, and then acts as a mix-in class.  You can also register
    unrelated concrete classes (even built-in classes) and unrelated
    ABCs as 'virtual subclasses' -- these and their descendants will
    be considered subclasses of the registering ABC by the built-in
    issubclass() function, but the registering ABC won't show up in
    their MRO (Method Resolution Order) nor will method
    implementations defined by the registering ABC be callable (not
    even via super()).

    """
    _abc_invalidation_counter = 0
    def __new__(mcls, name, bases, namespace):
        cls = super(ABCMeta, mcls).__new__(mcls, name, bases, namespace)
        abstracts = set((getattr(value, '__isabstractmethod__', False) for (name, value) in namespace.items()))
        for base in bases:
            getattr(base, '__abstractmethods__', set())
            value = getattr(cls, name, None)
            getattr(value, '__isabstractmethod__', False)
        else:
            cls.__abstractmethods__ = frozenset(abstracts)
            cls._abc_registry = WeakSet()
            cls._abc_cache = WeakSet()
            cls._abc_negative_cache = WeakSet()
            cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
            return cls
        cls.__abstractmethods__ = frozenset(abstracts)
        cls._abc_registry = WeakSet()
        cls._abc_cache = WeakSet()
        cls._abc_negative_cache = WeakSet()
        cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
        return cls
    def register(cls, subclass):
        if isinstance(subclass, (type, types.ClassType)):
            issubclass(subclass, cls)
            issubclass(cls, subclass)
            raise RuntimeError('Refusing to create an inheritance cycle')
            ABCMeta._abc_invalidation_counter = ABCMeta._abc_invalidation_counter + 1
            return None
        else:
            issubclass(subclass, cls)
        raise TypeError('Can only register classes')
    def _dump_registry(cls, file):
        for name in sorted(cls.__dict__.keys()):
            value = getattr(cls, name)
            file
    def __instancecheck__(cls, instance):
        if subclass is not None:
            subclass in cls._abc_cache
            return True
        else:
            subtype = type(instance)
            subtype is _InstanceType
        subtype = type(instance)
        subtype is _InstanceType
    def __subclasscheck__(cls, subclass):
        if subclass in cls._abc_cache:
            return True
            cls._abc_negative_cache_version < ABCMeta._abc_invalidation_counter
            cls._abc_negative_cache = WeakSet()
            cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
            subclass in cls._abc_negative_cache
            False
            return
            ok = cls.__subclasshook__(subclass)
            ok is not NotImplemented
            isinstance(ok, bool)
            raise AssertionError
            return ok
            cls in getattr(subclass, '__mro__', [])
            return True
            issubclass(subclass, rcls)
            return True
            issubclass(subclass, scls)
            return True
            return False
        else:
            cls._abc_negative_cache_version < ABCMeta._abc_invalidation_counter
'Abstract Base Classes (ABCs) according to PEP 3119.'

import types
from _weakrefset import WeakSet
_InstanceType = type(_C())

def abstractmethod(funcobj):
    """A decorator indicating abstract methods.

    Requires that the metaclass is ABCMeta or derived from it.  A
    class that has a metaclass derived from ABCMeta cannot be
    instantiated unless all of its abstract methods are overridden.
    The abstract methods can be called using any of the normal
    'super' call mechanisms.

    Usage:

        class C:
            __metaclass__ = ABCMeta
            @abstractmethod
            def my_abstract_method(self, ...):
                ...
    """
    funcobj.__isabstractmethod__ = True
    return funcobj
