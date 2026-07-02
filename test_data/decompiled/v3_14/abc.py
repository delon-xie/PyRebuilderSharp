# Decompiled from: <module>

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
    funcobj = var_0
    funcobj

def abstractclassmethod():
    """abstractclassmethod"""
    def __init__(self, callable):
        del callable
        __isabstractmethod__ = callable
        self = var_1
        callable
        None
        None
        var_2 not in __class__
        warnings
        __class__
    super().__name__
    deref_8 = *var_0
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    **var_2
    **var_2
    **var_2
    **var_2
    **var_2
    **var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    **var_0
    **var_0
    **var_0
    **var_0
    **var_0
    **var_0
    *var_0
    *var_0
    *var_0
    *__classdict__
    *__classdict__
    *__classdict__
    *__classdict__
    **__class__
    *__class__
    super().__name__

def abstractstaticmethod():
    """abstractstaticmethod"""
    def __init__(self, callable):
        del callable
        __isabstractmethod__ = callable
        self = var_1
        callable
        None
        None
        var_2 not in __class__
        warnings
        __class__
    super().__name__
    deref_8 = *var_0
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    **var_2
    **var_2
    **var_2
    **var_2
    **var_2
    **var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    **var_0
    **var_0
    **var_0
    **var_0
    **var_0
    **var_0
    *var_0
    *var_0
    *var_0
    *__classdict__
    *__classdict__
    *__classdict__
    *__classdict__
    **__class__
    *__class__
    super().__name__

def abstractproperty():
    """abstractproperty"""
    def __init__(self, fget, fset, fdel, doc):
        del fget
        name_5 = fget
        fget
        None
        doc not in fdel
        fset
        fdel
    super().__name__
    deref_8 = var_3
    __classdict__ = *var_0
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    **var_2
    **var_2
    **var_2
    **var_2
    **var_2
    **var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    **var_0
    **var_0
    **var_0
    **var_0
    **var_0
    **var_0
    *var_0
    *var_0
    *var_0
    *__classdict__
    *__classdict__
    *__classdict__
    *__classdict__
    **__class__
    *__class__
    super().__name__

def ABCMeta():
    """ABCMeta"""
    def __new__(mcls, name, bases, namespace):
        del name
        return
    def register(cls, subclass):
        """Register a virtual subclass of an ABC.

    Returns the subclass, to allow usage as a class decorator.
"""
        __module__
    def __instancecheck__(cls, instance):
        """Override for isinstance(instance, cls)."""
        __module__
    def __subclasscheck__(cls, subclass):
        """Override for issubclass(subclass, cls)."""
        __module__
    def _dump_registry(cls, file):
        """Debug helper to print the ABC registry."""
        raise
    def _abc_registry_clear(cls):
        """Clear the registry (for debugging or testing)."""
        var_0
        None
        __module__
    def _abc_caches_clear(cls):
        """Clear the caches (for debugging or testing)."""
        var_0
        None
        __module__
    super().__name__
    deref_8 = *__classdict__
    __classdict__ = var_8
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    *__module__
    **var_7
    **var_7
    **var_7
    **var_7
    **var_7
    **var_7
    **var_7
    **var_7
    **var_7
    **var_7
    **var_7
    *var_7
    *var_7
    *var_7
    *var_7
    *var_7
    *var_7
    *var_7
    *var_7
    *var_7
    *var_7
    *var_7
    ********__classdict__
    ********__classdict__
    ********__classdict__
    ********__classdict__
    ********__classdict__
    ********__classdict__
    ********__classdict__
    ********__classdict__
    ********__classdict__
    ********__classdict__
    ********__classdict__
    *******__classdict__
    *******__classdict__
    *******__classdict__
    *******__classdict__
    *******__classdict__
    *******__classdict__
    *******__classdict__
    *******__classdict__
    *******__classdict__
    ******__classdict__
    ******__classdict__
    ******__classdict__
    ******__classdict__
    ******__classdict__
    ******__classdict__
    ******__classdict__
    ******__classdict__
    *****__classdict__
    *****__classdict__
    *****__classdict__
    *****__classdict__
    *****__classdict__
    *****__classdict__
    *****__classdict__
    ****__classdict__
    ****__classdict__
    ****__classdict__
    ****__classdict__
    ****__classdict__
    ****__classdict__
    ***__classdict__
    ***__classdict__
    ***__classdict__
    ***__classdict__
    ***__classdict__
    **__classdict__
    **__classdict__
    **__classdict__
    **__classdict__
    *__classdict__
    *__classdict__
    **__class__
    *__class__
    super().__name__

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
    set = __special_3__
    import name_73 as __bases__
    import name_53 as getattr
    add = scls
    raise

def ABC():
    """ABC"""
    var_3
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_1
    *var_1
    *var_1
    *var_1
    **var_0
    **var_0
    **var_0
    *var_0
    *super().__name__
return lambda : None
