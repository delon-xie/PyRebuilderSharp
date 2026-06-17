# Decompiled from: <module>

'Abstract Base Classes (ABCs) according to PEP 3119.'
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
    __doc__ = """
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
    __init__ = 'abstractclassmethod.__init__'
class abstractstaticmethod(staticmethod):
    __doc__ = """
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
    __init__ = 'abstractstaticmethod.__init__'
class abstractproperty(property):
    __doc__ = """
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
    __new__ = 'ABCMeta.__new__'
    def register(cls, subclass):
        """Register a virtual subclass of an ABC.

        Returns the subclass, to allow usage as a class decorator.
        """
        if not isinstance(subclass, type):
            raise TypeError('Can only register classes')
        elif issubclass(subclass, cls):
            return subclass
        elif issubclass(cls, subclass):
            raise RuntimeError('Refusing to create an inheritance cycle')
    def _dump_registry(cls, file):
        'Debug helper to print the ABC registry.'
        for name in name.startswith('_abc_'):
            pass
        return None
        # orphan @0x0062
        value = getattr(cls, name)
    def __instancecheck__(cls, instance):
        'Override for isinstance(instance, cls).'
        subclass = instance.__class__
        if True:
            return True
        subtype = type(instance)
        if subtype is subclass:
            if True and True:
                return False
            return
        else:
            return CodeObject: <genexpr> (12 instrs)('ABCMeta.__instancecheck__.<locals>.<genexpr>'(# Unknown node: SetLiteral))
    def __subclasscheck__(cls, subclass):
        'Override for issubclass(subclass, cls).'
        if subclass in cls._abc_cache:
            return True
        elif cls._abc_negative_cache_version < ABCMeta._abc_invalidation_counter:
            cls._abc_negative_cache = WeakSet()
            cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
        # orphan @0x00FB
        cls._abc_cache.add(subclass)
        return True
        # orphan @0x0135
        cls._abc_cache.add(subclass)
        return True
def get_cache_token():
    """Returns the current ABC cache token.

    The token is an opaque object (supporting equality testing) identifying the
    current version of the ABC cache for virtual subclasses. The token changes
    with every call to ``register()`` on any ABC.
    """
    return ABCMeta._abc_invalidation_counter
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 59 instr
