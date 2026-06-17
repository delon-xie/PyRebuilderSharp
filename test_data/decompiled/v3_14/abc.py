# Decompiled from: <module>

try:
    from _abc import get_cache_token
    from _abc import _abc_init
    from _abc import _abc_register
    from _abc import _abc_instancecheck
    from _abc import _abc_subclasscheck
    from _abc import _get_dump
    from _abc import _reset_registry
    from _abc import _reset_caches
except ImportError:
    from _py_abc import ABCMeta
    from _py_abc import get_cache_token
    ABCMeta.__module__ = 'abc'
__doc__ = 'Abstract Base Classes (ABCs) according to PEP 3119.'
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
    return
abstractclassmethod = None(abstractclassmethod, 'abstractclassmethod', classmethod)
abstractstaticmethod = None(abstractstaticmethod, 'abstractstaticmethod', staticmethod)
abstractproperty = None(abstractproperty, 'abstractproperty', property)
ABCMeta = None(ABCMeta, 'ABCMeta', type)
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
    if not True:
        pass
    return
    abstracts = set()
    for scls in iterable:
        for name in iterable:
            if not True:
                pass
            else:
                break
    for _ in iterable:
        if not True:
            pass
        else:
            break
    return
ABC = ABC('ABC', ABCMeta, ('metaclass',))
return None
try:
    pass
except:
    pass
raise
# orphan @0x00DE
# orphan @0x00E2
raise
# [SUMMARY] 9 blocks · 7 processed · 2 orphan · 96 instr
