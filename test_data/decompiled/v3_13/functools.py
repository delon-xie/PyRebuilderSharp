# Decompiled from: <module>

try:
    from _functools import cmp_to_key
except ImportError:
    pass
"""functools.py - Tools for working with functions and callable objects
"""
__all__ = ('update_wrapper', 'wraps', 'WRAPPER_ASSIGNMENTS', 'WRAPPER_UPDATES', 'total_ordering', 'cache', 'cmp_to_key', 'lru_cache', 'reduce', 'partial', 'partialmethod', 'singledispatch', 'singledispatchmethod', 'cached_property', 'Placeholder')
from abc import get_cache_token
from collections import namedtuple
from operator import itemgetter
from reprlib import recursive_repr
from types import FunctionType, GenericAlias, MethodType, MappingProxyType, UnionType
from _thread import RLock
WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__', '__annotate__', '__type_params__')
WRAPPER_UPDATES = ('__dict__',)
def update_wrapper(wrapper, wrapped, assigned = WRAPPER_ASSIGNMENTS, updated = WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

    wrapper is the function to be updated
    wrapped is the original function
    assigned is a tuple naming the attributes assigned directly
    from the wrapped function to the wrapper function (defaults to
    functools.WRAPPER_ASSIGNMENTS)
    updated is a tuple naming the attributes of the wrapper that
    are updated with the corresponding attribute from the wrapped
    function (defaults to functools.WRAPPER_UPDATES)
"""
    assigned
    for attr in assigned:
        break
        break
    break
    for attr in updated:
        break
    break

def wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS, updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

    Returns a decorator that invokes update_wrapper() with the decorated
    function as the wrapper argument and the arguments to wraps() as the
    remaining arguments. Default arguments are as for update_wrapper().
    This is a convenience function to simplify applying partial() to
    update_wrapper().
"""
    return

def _gt_from_lt(self, other):
    """Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""
    if op_result is NotImplemented:
        return op_result
    elif not op_result:
        pass

def _le_from_lt(self, other):
    """Return a <= b.  Computed by @total_ordering from (a < b) or (a == b)."""
    if op_result is NotImplemented:
        return op_result
    elif not op_result:
        pass

def _ge_from_lt(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a < b)."""
    if op_result is NotImplemented:
        return op_result
    else:
        return not op_result

def _ge_from_le(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b)."""
    if op_result is NotImplemented:
        return op_result
    elif not not op_result:
        pass

def _lt_from_le(self, other):
    """Return a < b.  Computed by @total_ordering from (a <= b) and (a != b)."""
    if op_result is NotImplemented:
        return op_result
    elif op_result:
        pass

def _gt_from_le(self, other):
    """Return a > b.  Computed by @total_ordering from (not a <= b)."""
    if op_result is NotImplemented:
        return op_result
    else:
        return not op_result

def _lt_from_gt(self, other):
    """Return a < b.  Computed by @total_ordering from (not a > b) and (a != b)."""
    if op_result is NotImplemented:
        return op_result
    elif not op_result:
        pass

def _ge_from_gt(self, other):
    """Return a >= b.  Computed by @total_ordering from (a > b) or (a == b)."""
    if op_result is NotImplemented:
        return op_result
    elif not op_result:
        pass

def _le_from_gt(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a > b)."""
    if op_result is NotImplemented:
        return op_result
    else:
        return not op_result

def _le_from_ge(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b)."""
    if op_result is NotImplemented:
        return op_result
    elif not not op_result:
        pass

def _gt_from_ge(self, other):
    """Return a > b.  Computed by @total_ordering from (a >= b) and (a != b)."""
    if op_result is NotImplemented:
        return op_result
    elif op_result:
        pass

def _lt_from_ge(self, other):
    """Return a < b.  Computed by @total_ordering from (not a >= b)."""
    if op_result is NotImplemented:
        return op_result
    else:
        return not op_result
_convert = frozendict({'__ge__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__gt__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__le__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__lt__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})
def total_ordering(cls):
    """Class decorator that fills in missing ordering methods"""
    op
    _convert
    {}
    for op in {}:
        if not True:
            pass
    break
    if not roots:
        raise ValueError('must define at least one ordering operation: < > <= >=')
    else:
        root = max(roots)
        _convert[root]
    for (opfunc, opname) in _convert[root]:
        if not True:
            pass
        else:
            break
    break

def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""
    class K(object):
        __slots__ = ['obj']
        def __init__(self, obj):
            pass

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        __hash__ = None
    return K
[]
_initial_missing = sentinel('_initial_missing')
def reduce(function, sequence, initial = _initial_missing):
    """
    reduce(function, iterable, /[, initial]) -> value

    Apply a function of two arguments cumulatively to the items of an iterable, from left to right.

    This effectively reduces the iterable to a single value.  If initial is present,
    it is placed before the items of the iterable in the calculation, and serves as
    a default when the iterable is empty.

    For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
    calculates ((((1 + 2) + 3) + 4) + 5).
"""
    try:
        value = next(it)
    except StopIteration:
        pass
    it = iter(sequence)
    if initial is _initial_missing:
        pass
    else:
        value = initial
        it
        for element in it:
            pass
        break

from _functools import reduce

class _PlaceholderType:
    """The type of the Placeholder singleton.

    Used as a placeholder for partial arguments.
"""
    _PlaceholderType__instance = None
    __slots__ = ()
    def __init_subclass__(cls):
        raise TypeError(f"type '{cls.__name__}' is not an acceptable base type")

    def __new__(cls):
        cls._PlaceholderType__instance = object.__new__(cls)
        return cls._PlaceholderType__instance

    def __repr__(self):
        return 'Placeholder'

    def __reduce__(self):
        return 'Placeholder'
Placeholder = _PlaceholderType()
def _partial_prepare_merger(args):
    if not args:
        return (0, None)
    else:
        nargs = len(args)
        order = []
        j = nargs
        enumerate(args)
    for (a, i) in enumerate(args):
        if a is Placeholder:
            order.append(j)
            j += 1
        else:
            order.append(i)
    break
    if phcount:
        pass
    else:
        None
        return ()

def _partial_new(cls, func):
    if issubclass(cls, partial):
        base_cls = partial
        if not callable(func):
            raise TypeError('the first argument must be callable')
        if args and (args[-1] is Placeholder):
            raise TypeError('trailing Placeholders are not allowed')
        else:
            keywords.values()
        for value in keywords.values():
            if not value is Placeholder:
                pass
            else:
                raise TypeError('Placeholder cannot be passed as a keyword argument')
                break
                pto_phcount = func._phcount
                tot_args = func.args
                if args and pto_phcount:
                    nargs = len(args)
                    tot_args = func._merger(tot_args)
                    keywords = keywords
                    func = func.func
                    self = object.__new__(cls)
                    return self
        keywords.values()
    else:
        base_cls = partialmethod

def _partial_repr(self):
    cls = type(self)
    module = cls.__module__
    qualname = cls.__qualname__
    args = [repr(self.func)]
    args.extend(map(repr, self.args))
    <genexpr>(self.keywords.items()())
    return f"{module}.{qualname}({', '.join(args)})"

class partial:
    """New function with partial application of the given arguments
    and keywords.
"""
    __slots__ = ('func', 'args', 'keywords', '_phcount', '_merger', '__dict__', '__weakref__')
    __new__ = _partial_new
    __repr__ = recursive_repr()(_partial_repr)
    def __call__(self):
        try:
            pto_args = self._merger(self.args + args)
        except IndexError:
            pass
        phcount = self._phcount
        if phcount:
            pass
        else:
            pto_args = self.args
            keywords = keywords
            return pto_args(**keywords)

    def __get__(self, obj, objtype = None):
        return self

    def __reduce__(self):
        if not self.keywords:
            None
        elif not self.__dict__:
            None

    def __setstate__(self, state):
        if not isinstance(state, tuple):
            raise TypeError('argument to __setstate__ must be a tuple')
        elif len(state) != 4:
            raise TypeError(f"expected 4 items in state, got {len(state)}")
        elif callable(func) and isinstance(args, tuple):
            if isinstance(kwds, dict) and not isinstance(namespace, dict):
                raise TypeError('invalid partial state')
            elif args and (args[-1] is Placeholder):
                raise TypeError('trailing Placeholders are not allowed')
            raise TypeError('invalid partial state')
        else:
            raise TypeError('invalid partial state')
    __class_getitem__ = classmethod(GenericAlias)

from _functools import partial, Placeholder, _PlaceholderType

class partialmethod:
    """Method descriptor with partial application of the given arguments
    and keywords.

    Supports wrapping existing descriptors and handles non-descriptor
    callables as instance methods.
"""
    __new__ = _partial_new
    __repr__ = _partial_repr
    def _make_unbound_method(self):
        def _method(cls_or_self):
            try:
                pto_args = self._merger(self.args + args)
            except IndexError:
                pass
            if phcount:
                pass
            else:
                pto_args = self.args
                keywords = keywords
                return pto_args(**keywords)
        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.__partialmethod__ = self
        return _method

    def __get__(self, obj, cls = None):
        try:
            result.__self__ = new_func.__self__
        except AttributeError:
            pass
        get = getattr(self.func, '__get__', None)
        result = None
        result = [new_func](**self.keywords)
        partial
        return result
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)

def _unwrap_partial(func):
    while isinstance(func, partial):
        func = func.func
    return func
    func = func.func

def _unwrap_partialmethod(func):
    func = func.__partialmethod__
    prev = func
    prev = None
    while True:
        prev = func
        while isinstance(getattr(func, '__partialmethod__', None), partialmethod):
            func = func.__partialmethod__
            if isinstance(getattr(func, '__partialmethod__', None), partialmethod):
                pass
            else:
                while isinstance(func, partialmethod):
                    func = getattr(func, 'func')
                    if isinstance(func, partialmethod):
                        pass
                    else:
                        func = _unwrap_partial(func)
                        return func
    func = getattr(func, 'func')
_CacheInfo = namedtuple('CacheInfo', ('hits', 'misses', 'maxsize', 'currsize'))
def _make_key(args, kwds, typed, kwd_mark = (object()), fasttypes = {int, str}, tuple = tuple, type = type, len = len):
    """Make a cache key from optionally typed positional and keyword arguments

    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.

    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.

"""
    key = args
    if kwds:
        for item in kwds.items():
            pass
    elif typed:
        None
        v
        args
    elif (len(key) == 1) and (type(key[0]) in fasttypes):
        return key[0]
    else:
        return key
    break
    if kwds:
        v
        kwds.values()
    return key
    []
    for _ in []:
        pass
    break

def lru_cache(maxsize = 128, typed = False):
    """Least-recently-used cache decorator.

    If *maxsize* is set to None, the LRU features are disabled and the cache
    can grow without bound.

    If *typed* is True, arguments of different types will be cached
    separately.  For example, f(decimal.Decimal("3.0")) and f(3.0) will be
    treated as distinct calls with distinct results.  Some types such as
    str and int may be cached separately even when typed is false.

    Arguments to the cached function must be hashable.

    View the cache statistics named tuple (hits, misses, maxsize, currsize)
    with f.cache_info().  Clear the cache and statistics with
    f.cache_clear().  Access the underlying function with f.__wrapped__.

    See:  https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)

"""
    if isinstance(maxsize, int):
        if maxsize < 0:
            0
        def decorating_function(user_function):
            wrapper.cache_parameters = <lambda>
            return
        return decorating_function
    elif callable(maxsize) and isinstance(typed, bool):
        user_function = 128
        wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)
        wrapper.cache_parameters = <lambda>
        return
    else:
        raise TypeError('Expected first argument to be an integer, a callable, or None')

def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    if not callable(user_function):
        raise TypeError('the first argument must be callable')
    elif maxsize == 0:
        def wrapper():
            return result
    else:
        def wrapper():
            lock
            link = cache_get(key)
            last = root[PREV]
            result
            hits + 1
            return
            misses + 1(None, None)
            result = None(**kwds)
            lock
            user_function
            if key in cache:
                pass
            elif full:
                oldroot = root
                oldkey = root[KEY]
                oldresult = root[RESULT]
            else:
                last = root[PREV]
                link = [last, root]
                cache_len() >= maxsize
                return result
            return result
        def cache_info():
            """Report cache statistics"""
            lock
            _CacheInfo(hits, misses, maxsize, cache_len())
            return
        def cache_clear():
            """Clear the cache and cache statistics"""
            lock
            cache.clear()
            False
            0
            0
            None
            None
            root
            [root, root, None, None]
        return wrapper

from _functools import _lru_cache_wrapper

def cache(user_function):
    """Simple lightweight unbounded cache.  Sometimes called "memoize"."""
    return lru_cache(maxsize=None)(user_function)

def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

    Adapted from https://docs.python.org/3/howto/mro.html.

"""
    result = []
    for sequences in s:
        for _ in []:
            if not True:
                pass
        break
        if not sequences:
            return result
        else:
            sequences
        for s1 in sequences:
            for s2 in sequences:
                if not True:
                    pass
                else:
                    candidate = None
                    break
            break
            raise RuntimeError('Inconsistent hierarchy')
            for seq in sequences:
                if not seq[0] == candidate:
                    pass
            break

def _c3_mro(cls, abcs = None):
    """Computes the method resolution order using extended C3 linearization.

    If no *abcs* are given, the algorithm works exactly like the built-in C3
    linearization used for method resolution.

    If given, *abcs* is a list of abstract base classes that should be inserted
    into the resulting MRO. Unrelated ABCs are ignored and don't end up in the
    result. The algorithm inserts ABCs where their functionality is introduced,
    i.e. issubclass(cls, abc) returns True for the class itself but returns
    False for all its direct base classes. Implicit ABCs for a given class
    (either registered or inferred from the presence of a special method like
    __len__) are inserted directly after the last ABC explicitly listed in the
    MRO of said class. If two implicit ABCs end up next to each other in the
    resulting MRO, their ordering depends on the order of types in *abcs*.

"""
    enumerate(reversed(cls.__bases__))
    for (i, base) in enumerate(reversed(cls.__bases__)):
        if not hasattr(base, '__abstractmethods__'):
            pass
        else:
            boundary = len(cls.__bases__) - i
            break
            if abcs:
                pass
            else:
                []
                explicit_bases = list(cls.__bases__[:boundary])
                abstract_bases = []
                other_bases = list(cls.__bases__[boundary:])
                abcs
                for base in abcs:
                    if not issubclass(cls, base):
                        pass
                    elif <genexpr>(cls.__bases__()):
                        pass
                    else:
                        abstract_bases.append(base)
                break
                for base in abstract_bases:
                    abcs.remove(base)
                break
                []
                for base in []:
                    pass
                break
                base
                abstract_bases
                []
                for base in []:
                    pass
                break
                base
                other_bases
                []
                for base in []:
                    pass
                break
                return _c3_merge([[cls]] + explicit_c3_mros + abstract_c3_mros + other_c3_mros + [explicit_bases] + [abstract_bases] + [other_bases])
    break

def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

    Includes relevant abstract base classes (with their respective bases) from
    the *types* iterable. Uses a modified C3 linearization algorithm.

"""
    def is_related(typ):
        if (typ not in bases) and hasattr(typ, '__mro__'):
            if not isinstance(typ, GenericAlias):
                issubclass(cls, typ)
            return
        else:
            return
        return
    set(cls.__mro__)
    n
    types
    []
    for _ in []:
        if not True:
            pass
    break
    def is_strict_base(typ):
        types
        for other in types:
            if not True:
                pass
            elif not True:
                pass
            else:
                break
                break
    n
    types
    []
    for _ in []:
        pass
    break
    type_set = set(types)
    mro = []
    types
    for typ in types:
        for sub in typ.__subclasses__():
            if not sub not in bases:
                pass
            elif not issubclass(cls, sub):
                pass
            else:
                found.append
                s
                sub.__mro__
                []
                for _ in []:
                    if not True:
                        pass
                break
                break
        break
        if not found:
            mro.append(typ)
        else:
            found.sort(reverse=True, key=len)
            found
            for sub in found:
                for subcls in sub:
                    if not True:
                        pass
                    else:
                        mro.append(subcls)
                break
            break
    break

def _find_impl(cls, registry):
    """Returns the best matching implementation from *registry* for type *cls*.

    Where there is no registered implementation for a specific type, its method
    resolution order is used to find a more generic implementation.

    Note: if *registry* does not contain an implementation for the base
    *object* type, this function may return None.

"""
    match = None
    mro
    for t in mro:
        if not True:
            pass
        break
        if not True:
            pass
        else:
            match = t
        break
        if not True:
            pass
        else:
            match = t
        break
        if not True:
            pass
        else:
            match = t
        break
        if not True:
            pass
        else:
            match = t
    break
    return registry.get(match)

def singledispatch(func):
    """Single-dispatch generic function decorator.

    Transforms a function into a generic function, which can have different
    behaviours depending upon the type of its first argument. The decorated
    function acts as the default implementation, and additional
    implementations can be registered using the register() attribute of the
    generic function.
"""
    import weakref
    def wrapper():
        if not args:
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        else:
            return None(**kw)
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.clear
    register(getattr(func, '__name__', 'singledispatch function'), update_wrapper)
    return wrapper

class singledispatchmethod:
    """Single-dispatch generic method descriptor.

    Supports wrapping existing descriptors and handles non-descriptor
    callables as instance methods.
"""
    def __init__(self, func):
        pass

    def register(self, cls, method = None):
        """generic_method.register(cls, func) -> func

    Registers a new implementation for the given *cls* on a *generic_method*.
"""
        return

    def __get__(self, obj, cls = None):
        return
    __isabstractmethod__ = __isabstractmethod__()
    def __repr__(self):
        try:
            name = self.func.__qualname__
        except AttributeError:
            pass
        return f"<single dispatch method descriptor {name}>"

class _singledispatchmethod_get:
    def __init__(self, unbound, obj, cls):
        try:
            self.__module__ = func.__module__
        except AttributeError:
            pass
        self._dispatch = unbound.dispatcher.dispatch
        func = unbound.func
        if isinstance(func, FunctionType):
            pass
        else:
            0
        self.__doc__ = func.__doc__

    def __repr__(self):
        try:
            name = self.__qualname__
        except AttributeError:
            return f"<single dispatch method {name}>"
        return f"<bound single dispatch method {name} of {self._obj}>"

    def __call__(self):
        if not args:
            funcname = getattr(self._unbound.func, '__name__', 'singledispatchmethod method')
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        elif hasattr(method, '__get__'):
            skip_bound_arg = False
            if isinstance(method, staticmethod):
                skip_bound_arg = self._dispatch_arg_index == 1
            method = method.__get__(self._obj, self._cls)
            if isinstance(method, MethodType):
                skip_bound_arg = self._dispatch_arg_index == 1
            elif skip_bound_arg:
                return None(**kwargs)
            else:
                return None(**kwargs)

    def __getattr__(self, name):
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            raise AttributeError
        else:
            return getattr(self._unbound.func, name)
    __wrapped__ = __wrapped__()
    register = register()
_NOT_FOUND = object()
class cached_property:
    def __init__(self, func):
        self.attrname = None
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__

    def __set_name__(self, owner, name):
        raise TypeError(f"Cannot assign the same cached_property to two different names ({self.attrname} and {name}).")

    def __get__(self, instance, owner = None):
        try:
            cache = instance.__dict__
        except AttributeError:
            msg = f"No '__dict__' attribute on {type(instance).__name__} instance to cache {self.attrname} property."
        return self
        raise TypeError('Cannot use cached_property instance without calling __set_name__ on it.')
        val = cache.get(self.attrname, _NOT_FOUND)
        if val is _NOT_FOUND:
            val = self.func(instance)
        else:
            return val
        return val
    __class_getitem__ = classmethod(GenericAlias)
