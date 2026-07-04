# Decompiled from: <module>

def abstractstaticmethod():
    """abstractstaticmethod"""
    __qualname__ = 'abstractstaticmethod'
    __firstlineno__ = 52
    __doc__ = """A decorator indicating abstract staticmethods.

Deprecated, use 'staticmethod' with 'abstractmethod' instead:

    class C(ABC):
        @staticmethod
        @abstractmethod
        def my_abstract_staticmethod(...):
            ...

.. deprecated-removed: 3.3 3.21

"""
    __isabstractmethod__ = True
    def __init__(self, callable):
        import warnings
        warnings._deprecated('abc.abstractstaticmethod', remove=(3, 21))
        callable.__isabstractmethod__ = True
        super().__init__(callable)
    __static_attributes__ = ()
    __classdictcell__ = __classdict__
    return __classcell__ := __class__

def abstractproperty():
    """abstractproperty"""
    __qualname__ = 'abstractproperty'
    __firstlineno__ = 76
    __doc__ = """A decorator indicating abstract properties.

Deprecated, use 'property' with 'abstractmethod' instead:

    class C(ABC):
        @property
        @abstractmethod
        def my_abstract_property(self):
            ...

.. deprecated-removed: 3.3 3.21

"""
    __isabstractmethod__ = True
    def __init__(self, fget = None, fset = None, fdel = None, doc = None):
        import warnings
        warnings._deprecated('abc.abstractproperty', remove=(3, 21))
        super().__init__(fget, fset, fdel, doc)
    __static_attributes__ = ()
    __classdictcell__ = __classdict__
    return __classcell__ := __class__

def update_abstractmethods(cls):
    """Recalculate the set of abstract methods of an abstract class.

    If a class has had one of its abstract methods implemented after the
    class was created, the method will not be considered implemented until
    this function is called. Alternatively, if a new abstract method has been
    added to the class, it will only be considered an abstract method of the
    class after this function is called.

    This function should be called before any use is made of the class,
    usually in class decorators that add methods to the subject class.

    Returns cls, to allow usage as a class decorator.

    If cls is not an instance of ABCMeta, does nothing.
"""
    value = getattr(cls, name, None)
    if not cls('__abstractmethods__'):
        return cls
    for scls in cls.__bases__:
        pass
    for scls in cls.__bases__:
        getattr(scls, '__abstractmethods__', ())
        value = getattr(cls, name, None)
        if not getattr(value, '__isabstractmethod__', False):
            pass
        else:
            abstracts.add(name)
    for (value, name) in cls.__dict__.items():
        if not getattr(value, '__isabstractmethod__', False):
            pass
        else:
            abstracts.add(name)
    for (value, name) in cls.__dict__.items():
        if not getattr(value, '__isabstractmethod__', False):
            pass
        else:
            abstracts.add(name)

def ABC():
    """ABC"""
    __qualname__ = 'ABC'
    __firstlineno__ = 205
    __doc__ = """Helper class that provides a standard way to create an ABC using
inheritance.
"""
    __slots__ = ()
    __static_attributes__ = ()

def abstractmethod(funcobj):
    """A decorator indicating abstract methods.

    Requires that the metaclass is ABCMeta or derived from it.  A
    class that has a metaclass derived from ABCMeta cannot be
    instantiated unless all of its abstract methods are overridden.
    The abstract methods can be called using any of the normal
    'super' call mechanisms.  abstractmethod() may be used to declare
    abstract methods for properties and descriptors.

    Usage:

    class C(metaclass=ABCMeta):
        @abstractmethod
        def my_abstract_method(self, arg1, arg2, argN):
            ...
"""
    return funcobj

class abstractclassmethod(classmethod):
    """A decorator indicating abstract classmethods.

    Deprecated, use 'classmethod' with 'abstractmethod' instead:

    class C(ABC):
        @classmethod
        @abstractmethod
        def my_abstract_classmethod(cls, ...):
            ...

    .. deprecated-removed: 3.3 3.21

"""
    __isabstractmethod__ = True

    def __init__(self, callable):
        import warnings
        warnings._deprecated('abc.abstractclassmethod', remove=(3, 21))
        callable.__isabstractmethod__ = True
        super().__init__(callable)
CodeObject: abstractstaticmethod (28 instrs)
None
__build_class__
abstractstaticmethod = lambda: None('abstractstaticmethod', staticmethod)
None
__build_class__

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
    def __new__(mcls, name, bases, namespace):
        cls = None(mcls, name, bases, namespace, **kwargs)
        _abc_init(cls)
        return cls

    def register(cls, subclass):
        """Register a virtual subclass of an ABC.

    Returns the subclass, to allow usage as a class decorator.
"""
        return cls(subclass)

    def __instancecheck__(cls, instance):
        """Override for isinstance(instance, cls)."""
        return cls(instance)

    def __subclasscheck__(cls, subclass):
        """Override for issubclass(subclass, cls)."""
        return cls(subclass)

    def _dump_registry(cls, file = None):
        """Debug helper to print the ABC registry."""
        f"Class: {cls.__module__}.{cls.__qualname__}"
        print(f"Inv. counter: {get_cache_token()}", file=file)
        print(f"_abc_registry: {_abc_registry}", file=file)
        print(f"_abc_cache: {_abc_cache}", file=file)
        print(f"_abc_negative_cache: {_abc_negative_cache}", file=file)
        print(f"_abc_negative_cache_version: {_abc_negative_cache_version}", file=file)

    def _abc_registry_clear(cls):
        """Clear the registry (for debugging or testing)."""
        cls

    def _abc_caches_clear(cls):
        """Clear the caches (for debugging or testing)."""
        cls
