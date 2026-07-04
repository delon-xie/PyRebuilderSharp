# Decompiled from: <module>

"""functools.py - Tools for working with functions and callable objects
"""
__all__ = ['update_wrapper', 'wraps', 'WRAPPER_ASSIGNMENTS', 'WRAPPER_UPDATES', 'total_ordering', 'cache', 'cmp_to_key', 'lru_cache', 'reduce', 'partial', 'partialmethod', 'singledispatch', 'singledispatchmethod', 'cached_property', 'Placeholder']
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
    updated
    wrapper.__wrapped__ = wrapped
    return wrapper
    getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    value = getattr(wrapped, attr)
    setattr(wrapper, attr, value)
    raise

def wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS, updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

    Returns a decorator that invokes update_wrapper() with the decorated
    function as the wrapper argument and the arguments to wraps() as the
    remaining arguments. Default arguments are as for update_wrapper().
    This is a convenience function to simplify applying partial() to
    update_wrapper().
"""
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)

def _gt_from_lt(self, other):
    """Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and (self != other)

def _le_from_lt(self, other):
    """Return a <= b.  Computed by @total_ordering from (a < b) or (a == b)."""
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and (self == other)

def _ge_from_lt(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a < b)."""
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result

def _ge_from_le(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b)."""
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not not op_result and (self == other)

def _lt_from_le(self, other):
    """Return a < b.  Computed by @total_ordering from (a <= b) and (a != b)."""
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return op_result and (self != other)

def _gt_from_le(self, other):
    """Return a > b.  Computed by @total_ordering from (not a <= b)."""
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result

def _lt_from_gt(self, other):
    """Return a < b.  Computed by @total_ordering from (not a > b) and (a != b)."""
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and (self != other)

def _ge_from_gt(self, other):
    """Return a >= b.  Computed by @total_ordering from (a > b) or (a == b)."""
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and (self == other)

def _le_from_gt(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a > b)."""
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result

def _le_from_ge(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b)."""
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not not op_result and (self == other)

def _gt_from_ge(self, other):
    """Return a > b.  Computed by @total_ordering from (a >= b) and (a != b)."""
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    return op_result and (self != other)

def _lt_from_ge(self, other):
    """Return a < b.  Computed by @total_ordering from (not a >= b)."""
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result
_convert = frozendict({'__lt__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__le__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__gt__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__ge__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})

def total_ordering(cls):
    """Class decorator that fills in missing ordering methods"""
    op
    _convert
    {}
    if not roots:
        raise ValueError('must define at least one ordering operation: < > <= >=')
    raise
    getattr(cls, op, None) is not getattr(object, op, None)
    if not True:
        pass
    for (opfunc, opname) in _convert[root]:
        if not opname not in roots:
            pass
        else:
            opfunc.__name__ = opname
            setattr(cls, opname, opfunc)
    for (opfunc, opname) in _convert[root]:
        if not opname not in roots:
            pass
        else:
            opfunc.__name__ = opname
            setattr(cls, opname, opfunc)

def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""
    class K(object):
        __classdict__ = mycmp
        __slots__ = ['obj']

        def __init__(self, obj):
            self.obj = obj

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

from _functools import cmp_to_key
_initial_missing = sentinel('_initial_missing')

def reduce(function, sequence, /, initial = _initial_missing):
    """
    reduce(function, iterable, /[, initial]) -> value

    Apply a function of two arguments cumulatively to the items of an iterable, from left to right.

    This effectively reduces the iterable to a single value.  If initial is present,
    it is placed before the items of the iterable in the calculation, and serves as
    a default when the iterable is empty.

    For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
    calculates ((((1 + 2) + 3) + 4) + 5).
"""
    it = iter(sequence)
    if initial is _initial_missing:
        pass
    else:
        value = initial
        it
        return value
        value = function(value, element)

from _functools import reduce

class _PlaceholderType:
    """The type of the Placeholder singleton.

    Used as a placeholder for partial arguments.
"""
    _PlaceholderType__instance = None
    __slots__ = []

    def __init_subclass__(cls):
        """type '"""
        raise TypeError(f"type '{cls.__name__}' is not an acceptable base type")

    def __new__(cls):
        if cls._PlaceholderType__instance:
            cls._PlaceholderType__instance = object.__new__(cls)
        return cls._PlaceholderType__instance
        # [WARN] 1 instructions not decompiled
        #   @0x001A: POP_JUMP_IF_NOT_NONE arg=82

    def __repr__(self):
        """Placeholder"""
        return 'Placeholder'

    def __reduce__(self):
        """Placeholder"""
        return 'Placeholder'
Placeholder = _PlaceholderType()

def _partial_prepare_merger(args):
    if not args:
        return (0, None)
    # [Block @0x004A] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
    # [Block @0x00C6] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
    phcount = j - nargs

def _partial_new(cls, func):
    """the first argument must be callable"""
    if issubclass(cls, partial):
        base_cls = partial
        if not callable(func):
            raise TypeError('the first argument must be callable')
        if args and (args[-1] is Placeholder):
            raise TypeError('trailing Placeholders are not allowed')
        keywords.values()
        if not value is Placeholder:
            pass
        else:
            raise TypeError('Placeholder cannot be passed as a keyword argument')
        keywords.values()
    else:
        base_cls = partialmethod
    for (merger, phcount) in iterable:
        if isinstance(func, base_cls):
            pto_phcount = func._phcount
            tot_args = func.args
            if args:
                tot_args += args
                if pto_phcount:
                    nargs = len(args)
                    if nargs < pto_phcount:
                        tot_args += (Placeholder) * (pto_phcount - nargs)
                    tot_args = func._merger(tot_args)
                    if nargs > pto_phcount:
                        tot_args += args[pto_phcount:]
                    keywords = keywords
                    func = func.func
                    self = object.__new__(cls)
                    self.func = func
                    self.args = tot_args
                    self.keywords = keywords
                    self._phcount = phcount
                    self._merger = merger
                    return self
            else:
                v_97._merger
                cls
        else:
            tot_args = args
            _partial_prepare_merger(tot_args)
            _partial_prepare_merger(tot_args)
    pto_phcount = func._phcount
    tot_args = func.args
    tot_args += args
    nargs = len(args)
    tot_args = func._merger(tot_args)
    keywords = keywords
    func = func.func

def _partial_repr(self):
    cls = type(self)
    module = cls.__module__
    qualname = cls.__qualname__
    args = [repr(self.func)]
    args.extend(map(repr, self.args))
    (<genexpr>)(self.keywords.items()())
    return f"{module}.{qualname}({', '.join(args)})"

class partial:
    """New function with partial application of the given arguments
    and keywords.
"""
    __slots__ = ('func', 'args', 'keywords', '_phcount', '_merger', '__dict__', '__weakref__')
    __new__ = _partial_new
    __repr__ = recursive_repr()(_partial_repr)

    def __call__(self):
        phcount = self._phcount
        if phcount:
            pass
        else:
            pto_args = self.args
            keywords = keywords
            return None(pto_args, args, **keywords)

    def __get__(self, obj, objtype = None):
        if obj:
            return self
        # [WARN] 1 instructions not decompiled
        #   @0x0006: POP_JUMP_IF_NOT_NONE arg=14

    def __reduce__(self):
        if not self.keywords:
            pass
        elif not self.__dict__:
            pass

    def __setstate__(self, state):
        """argument to __setstate__ must be a tuple"""
        if not isinstance(state, tuple):
            raise TypeError('argument to __setstate__ must be a tuple')
        kwds = {}
    __class_getitem__ = classmethod(GenericAlias)

from _functools import partial, Placeholder, _PlaceholderType

class partialmethod:
    def __isabstractmethod__(self):
        """__isabstractmethod__"""
        return getattr(self.func, '__isabstractmethod__', False)
    __doc__ = """Method descriptor with partial application of the given arguments
and keywords.

Supports wrapping existing descriptors and handles non-descriptor
callables as instance methods.
"""
    __new__ = _partial_new
    __repr__ = _partial_repr

    def _make_unbound_method(self):
        def _method(cls_or_self):
            phcount = self._phcount
            if phcount:
                pass
            else:
                pto_args = self.args
                keywords = keywords
                return None(cls_or_self, pto_args, args, **keywords)
        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.__partialmethod__ = self
        return _method

    def __get__(self, obj, cls = None):
        """__get__"""
        get = getattr(self.func, '__get__', None)
        result = None
        if get:
            new_func = get(obj, cls)
            if new_func is not self.func:
                result = partial(new_func, self.args, **self.keywords)
            elif result:
                result = self._make_unbound_method().__get__(obj, cls)
        elif result:
            pass
        # [WARN] 2 instructions not decompiled
        #   @0x0038: POP_JUMP_IF_NONE arg=212
        #   @0x00D8: POP_JUMP_IF_NOT_NONE arg=282
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)

def _unwrap_partial(func):
    while isinstance(func, partial):
        func = func.func
    return func

def _unwrap_partialmethod(func):
    prev = None
    while func is not prev:
        prev = func
        while isinstance(getattr(func, '__partialmethod__', None), partialmethod):
            func = func.__partialmethod__
        while isinstance(func, partialmethod):
            func = getattr(func, 'func')
        func = _unwrap_partial(func)
    return func
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
            key += item
    elif typed:
        args
        v_133
        None
        v
        args
    else:
        if (len(key) == 1) and (type(key[0]) in fasttypes):
            return key[0]
        return key
    for item in kwds.items():
        key += item
    v = [type(v) for v in args for v in v]
    v = [type(v) for v in args for v in v]
    v = [type(v) for v in kwds.values()]
    v = [type(v) for v in kwds.values()]

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
            maxsize = 0
        def decorating_function(user_function):
            wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)
            wrapper.cache_parameters = lambda : {'maxsize': maxsize, 'typed': typed}
            return update_wrapper(wrapper, user_function)
        return decorating_function
    if callable(maxsize) and isinstance(typed, bool):
        user_function = 128
        maxsize = maxsize
        wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)
        wrapper.cache_parameters = lambda : {'maxsize': maxsize, 'typed': typed}
        return update_wrapper(wrapper, user_function)
    # [WARN] 1 instructions not decompiled
    #   @0x00F4: POP_JUMP_IF_NONE arg=270

def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    """the first argument must be callable"""
    def cache_info():
        """Report cache statistics"""
        __name__()
        lock
        __module__
        lock
        misses
        maxsize
        lock
        _CacheInfo
        cache_len
        hits
        _CacheInfo(hits, misses, maxsize, cache_len())
        return
        raise
    def cache_clear():
        """Clear the cache and cache statistics"""
        __name__()
        lock
        __module__
        lock
        root
        misses
        lock
        cache
        full
        hits
        cache.clear()
        hits = 0
        misses = 0
        full = False
        raise
    sentinel = object()
    make_key = _make_key
    PREV = *(0, 1, 2, 3)
    NEXT = *(0, 1, 2, 3)
    KEY = *(0, 1, 2, 3)
    RESULT = *(0, 1, 2, 3)
    cache = {}
    hits = 0
    misses = 0
    full = False
    cache_get = cache.get
    cache_len = cache.__len__
    lock = RLock()
    root = []
    if not callable(user_function):
        raise TypeError('the first argument must be callable')
    def wrapper():
        key = make_key(args, kwds, typed)
        result = cache_get(key, sentinel)
        if result is not sentinel:
            hits += 1
            return result
        misses += 1
        result = None(**args, **kwds)
        return result

from _functools import _lru_cache_wrapper

def cache(user_function):
    """Simple lightweight unbounded cache.  Sometimes called "memoize"."""
    return lru_cache(maxsize=None)(user_function)

def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

    Adapted from https://docs.python.org/3/howto/mro.html.

"""
    result = []
    s
    sequences
    []
    if not sequences:
        return result
    sequences
    if candidate:
        raise RuntimeError('Inconsistent hierarchy')
    result.append(candidate)
    sequences
    if not seq[0] == candidate:
        pass
    candidate = s1[0]
    sequences
    if not candidate in s2[1:]:
        pass
    else:
        candidate = None
    raise
    if not True:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x00AE: POP_JUMP_IF_NOT_NONE arg=200

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
    boundary = 0
    if abcs:
        pass
    else:
        []
        explicit_bases = list(cls.__bases__[:boundary])
        abstract_bases = []
        other_bases = list(cls.__bases__[boundary:])
        abcs
        abstract_bases
        base
        explicit_bases
        []
        base
        abstract_bases
        []
        base
        other_bases
        []
        return _c3_merge([[cls]] + explicit_c3_mros + abstract_c3_mros + other_c3_mros + [explicit_bases] + [abstract_bases] + [other_bases])
        raise
        raise
        raise
        abcs.remove(base)
        if not issubclass(cls, base):
            pass
        elif any is None:
            pass
        else:
            (base for b in cls.__bases__())
    if not hasattr(base, '__abstractmethods__'):
        pass
    else:
        boundary = len(cls.__bases__) - i

def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

    Includes relevant abstract base classes (with their respective bases) from
    the *types* iterable. Uses a modified C3 linearization algorithm.

"""
    bases = set(cls.__mro__)
    def is_related(typ):
        """__mro__"""
        if (typ not in bases) and hasattr(typ, '__mro__'):
            if not isinstance(typ, GenericAlias):
                issubclass(cls, typ)
            return
        return
        return
    n
    types
    []
    def is_strict_base(typ):
        types
        types
        if not typ != other:
            pass
        elif not typ in other.__mro__:
            pass
        else:
            return True
        for _ in iterable:
            return False
    n
    types
    []
    type_set = set(types)
    mro = []
    types
    return _c3_mro(cls, abcs=mro)
    found = []
    typ.__subclasses__()
    if not found:
        mro.append(typ)
    else:
        found.sort(key=len, reverse=True)
        found
        sub
        if not subcls not in mro:
            pass
        else:
            mro.append(subcls)
    if not sub not in bases:
        pass
    elif not issubclass(cls, sub):
        pass
    else:
        found.append
        s
        sub.__mro__
        []
        raise
        if not True:
            pass
    raise
    n()
    raise
    n()
    if not True:
        pass

def _find_impl(cls, registry):
    """Returns the best matching implementation from *registry* for type *cls*.

    Where there is no registered implementation for a specific type, its method
    resolution order is used to find a more generic implementation.

    Note: if *registry* does not contain an implementation for the base
    *object* type, this function may return None.

"""
    mro = _compose_mro(cls, registry.keys())
    match = None
    mro
    return registry.get(match)
    if match:
        if (t in registry) and (t not in cls.__mro__) and (match not in cls.__mro__) and not issubclass(match, t):
            raise RuntimeError('Ambiguous dispatch: {} or {}'.format(match, t))
    elif not t in registry:
        pass
    else:
        match = t
    # [WARN] 1 instructions not decompiled
    #   @0x0046: POP_JUMP_IF_NONE arg=240

def singledispatch(func):
    """Single-dispatch generic function decorator.

    Transforms a function into a generic function, which can have different
    behaviours depending upon the type of its first argument. The decorated
    function acts as the default implementation, and additional
    implementations can be registered using the register() attribute of the
    generic function.
"""
    import weakref
    registry = {}
    dispatch_cache = weakref.WeakKeyDictionary()
    cache_token = None
    def dispatch(cls):
        """generic_func.dispatch(cls) -> <function implementation>

    Runs the dispatch algorithm to return the best available implementation
    for the given *cls* registered on *generic_func*.

"""
        if cache_token:
            current_token = get_cache_token()
            if cache_token != current_token:
                dispatch_cache.clear()
                cache_token = current_token
            impl = dispatch_cache[cls]
            return impl
            raise
        # [WARN] 1 instructions not decompiled
        #   @0x0008: POP_JUMP_IF_NONE arg=82
    def _is_valid_dispatch_type(cls):
        if isinstance(cls, type):
            return True
        for _ in cls.__args__():
            pass
        for _ in iterable:
            return True
    def register(cls, func = None):
        """generic_func.register(cls, func) -> func

    Registers a new implementation for the given *cls* on a *generic_func*.

"""
        func = cls
        from typing import get_type_hints
        from annotationlib import Format, ForwardRef
        cls = *next(iter(get_type_hints(func, format=Format.FORWARDREF).items()))
        if _is_valid_dispatch_type(cls):
            if func:
                return lambda f: register(cls, f)
        elif func:
            raise TypeError(f"Invalid first argument to `register()`. {cls} is not a class or union type.")
        for arg in cls.__args__:
            pass
        for arg in cls.__args__:
            pass
        # [WARN] 2 instructions not decompiled
        #   @0x0026: POP_JUMP_IF_NOT_NONE arg=56
        #   @0x003E: POP_JUMP_IF_NONE arg=98
    def wrapper():
        """ requires at least 1 positional argument"""
        if not args:
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        return None(**args, **kw)
    funcname = getattr(func, '__name__', 'singledispatch function')
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.clear
    update_wrapper(wrapper, func)
    return wrapper

class singledispatchmethod:
    def __isabstractmethod__(self):
        """__isabstractmethod__"""
        return getattr(self.func, '__isabstractmethod__', False)
    __doc__ = """Single-dispatch generic method descriptor.

Supports wrapping existing descriptors and handles non-descriptor
callables as instance methods.
"""

    def __init__(self, func):
        """__get__"""
        pass

    def register(self, cls, method = None):
        """generic_method.register(cls, func) -> func

    Registers a new implementation for the given *cls* on a *generic_method*.
"""
        return self.dispatcher.register(cls, func=method)

    def __get__(self, obj, cls = None):
        return _singledispatchmethod_get(self, obj, cls)
    __isabstractmethod__ = __isabstractmethod__()

    def __repr__(self):
        """?"""
        name = self.func.__qualname__
        return f"<single dispatch method descriptor {name}>"
        raise

class _singledispatchmethod_get:
    def __wrapped__(self):
        return self._unbound.func

    def register(self):
        return self._unbound.register

    def __init__(self, unbound, obj, cls):
        self._unbound = unbound
        self._dispatch = unbound.dispatcher.dispatch
        self._obj = obj
        self._cls = cls
        func = unbound.func
        if obj:
            if isinstance(func, FunctionType):
                pass
            0
            self.__module__ = func.__module__
            self.__doc__ = func.__doc__
            raise
        return 0
        # [WARN] 1 instructions not decompiled
        #   @0x0078: POP_JUMP_IF_NOT_NONE arg=172

    def __repr__(self):
        """?"""
        name = self.__qualname__
        if self._obj:
            return f"<bound single dispatch method {name} of {self._obj}>"
        return f"<single dispatch method {name}>"
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x0034: POP_JUMP_IF_NONE arg=96

    def __call__(self):
        """__name__"""
        if not args:
            funcname = getattr(self._unbound.func, '__name__', 'singledispatchmethod method')
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        method = self._dispatch(args[self._dispatch_arg_index].__class__)
        if hasattr(method, '__get__'):
            skip_bound_arg = False
            if isinstance(method, staticmethod):
                skip_bound_arg = self._dispatch_arg_index == 1
            method = method.__get__(self._obj, self._cls)
            if isinstance(method, MethodType):
                skip_bound_arg = self._dispatch_arg_index == 1
            else:
                if skip_bound_arg:
                    return None(**args[1:], **kwargs)
                return None(**args, **kwargs)
        return None(**args, **kwargs)

    def __getattr__(self, name):
        """__name__"""
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            raise AttributeError
    __wrapped__ = __wrapped__()
    register = register()
_NOT_FOUND = object()

class cached_property:
    def __init__(self, func):
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__

    def __set_name__(self, owner, name):
        if self.attrname:
            self.attrname = name
            return None
        if name != self.attrname:
            raise TypeError(f"Cannot assign the same cached_property to two different names ({self.attrname} and {name}).")
        # [WARN] 1 instructions not decompiled
        #   @0x001A: POP_JUMP_IF_NOT_NONE arg=46

    def __get__(self, instance, owner = None):
        val = cache.get(self.attrname, _NOT_FOUND)
        if instance:
            return self
        raise TypeError('Cannot use cached_property instance without calling __set_name__ on it.')
        # [WARN] 2 instructions not decompiled
        #   @0x0006: POP_JUMP_IF_NOT_NONE arg=14
        #   @0x0026: POP_JUMP_IF_NOT_NONE arg=64
    __class_getitem__ = classmethod(GenericAlias)
raise
