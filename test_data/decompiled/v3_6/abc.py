# Decompiled from: <module>

"""Abstract Base Classes (ABCs) according to PEP 3119."""
from _weakrefset import WeakSet

def abstractmethod(funcobj):
    """A decorator indicating abstract methods.

    Requires that the metaclass is ABCMeta or derived from it.  A
    class that has a metaclass derived from ABCMeta cannot be
    instantiated unless all of its abstract methods are overridden.
    The abstract methods can be called using any of the normal
    'super' call mechanisms.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractmethod
            def my_abstract_method(self, ...):
                ...
    """
    funcobj.__isabstractmethod__ = True
    return funcobj

class abstractclassmethod(classmethod):
    """
    A decorator indicating abstract classmethods.

    Similar to abstractmethod.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractclassmethod
            def my_abstract_classmethod(cls, ...):
                ...

    'abstractclassmethod' is deprecated. Use 'classmethod' with
    'abstractmethod' instead.
    """
    __isabstractmethod__ = True
    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super().__init__(callable)

class abstractstaticmethod(staticmethod):
    """
    A decorator indicating abstract staticmethods.

    Similar to abstractmethod.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractstaticmethod
            def my_abstract_staticmethod(...):
                ...

    'abstractstaticmethod' is deprecated. Use 'staticmethod' with
    'abstractmethod' instead.
    """
    __isabstractmethod__ = True
    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super().__init__(callable)

class abstractproperty(property):
    """
    A decorator indicating abstract properties.

    Requires that the metaclass is ABCMeta or derived from it.  A
    class that has a metaclass derived from ABCMeta cannot be
    instantiated unless all of its abstract properties are overridden.
    The abstract properties can be called using any of the normal
    'super' call mechanisms.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractproperty
            def my_abstract_property(self):
                ...

    This defines a read-only property; you can also define a read-write
    abstract property using the 'long' form of property declaration:

        class C(metaclass=ABCMeta):
            def getx(self): ...
            def setx(self, value): ...
            x = abstractproperty(getx, setx)

    'abstractproperty' is deprecated. Use 'property' with 'abstractmethod'
    instead.
    """
    __isabstractmethod__ = True

class ABCMeta(type):
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
    _abc_invalidation_counter = 0
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        for base in bases:
            for name in getattr(base, '__abstractmethods__', set()):
                value = getattr(cls, name, None)
                if getattr(value, '__isabstractmethod__', False):
                    return abstracts.add(name)
        cls.__abstractmethods__ = frozenset(abstracts)
        cls._abc_registry = WeakSet()
        cls._abc_cache = WeakSet()
        cls._abc_negative_cache = WeakSet()
        cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
        return cls

    def register(cls, subclass):
        """Register a virtual subclass of an ABC.

        Returns the subclass, to allow usage as a class decorator.
        """
        if not isinstance(subclass, type):
            raise TypeError('Can only register classes')
        else:
            return subclass

    def _dump_registry(cls, file):
        """Debug helper to print the ABC registry."""
        print('Class: %s.%s' % (cls.__module__, cls.__qualname__), file=file)
        print('Inv.counter: %s' % ABCMeta._abc_invalidation_counter, file=file)
        for name in sorted(cls.__dict__):
            if name.startswith('_abc_'):
                value = getattr(cls, name)
                if isinstance(value, WeakSet):
                    value = set(value)
            print('%s: %r' % (name, value), file=file)

    def __instancecheck__(cls, instance):
        """Override for isinstance(instance, cls)."""
        subtype = type(instance)
        subclass = instance.__class__
        return True

    def __subclasscheck__(cls, subclass):
        """Override for issubclass(subclass, cls)."""
        ok = cls.__subclasshook__(subclass)
        cls._abc_negative_cache = WeakSet()
        cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
        if subclass in cls._abc_cache:
            return True
        cls._abc_cache.add(subclass)

class ABC(metaclass=ABCMeta):
    """Helper class that provides a standard way to create an ABC using
    inheritance.
    """
    pass

def get_cache_token():
    """Returns the current ABC cache token.

    The token is an opaque object (supporting equality testing) identifying the
    current version of the ABC cache for virtual subclasses. The token changes
    with every call to ``register()`` on any ABC.
    """
    return ABCMeta._abc_invalidation_counter
