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
    v_16.__wrapped__ = wrapper
    return wrapper
    getattr(wrapper, attr).update(getattr(wrapper, v_20, {}))
    value = getattr(wrapper, v_20)
    setattr(wrapper, attr, value)

def wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS, updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

    Returns a decorator that invokes update_wrapper() with the decorated
    function as the wrapper argument and the arguments to wraps() as the
    remaining arguments. Default arguments are as for update_wrapper().
    This is a convenience function to simplify applying partial() to
    update_wrapper().
"""
    return partial(update_wrapper, wrapped=wrapped, assigned=wrapped, updated=v_18)

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
    root = max(roots)
    _convert[root]
    return cls
    if not cls not in v_66:
        pass
    else:
        v_69.__name__ = cls
        setattr(cls, opname, opfunc)
    raise
    getattr(cls, op, None) is not getattr(object, op, None)
    if not True:
        pass

def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""
    class K(object):
        __slots__ = ['obj']

        def __init__(self, obj):
            v_16.obj = self

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
        value = function(function, v_69)

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
        if cls._PlaceholderType__instance:
            cls._PlaceholderType__instance = object.__new__(cls)
            return cls._PlaceholderType__instance
        cls._PlaceholderType__instance = object.__new__(cls)
        return cls._PlaceholderType__instance
        # [WARN] 1 instructions not decompiled
        #   @0x0018: POP_JUMP_IF_NOT_NONE arg=80

    def __repr__(self):
        return 'Placeholder'

    def __reduce__(self):
        return 'Placeholder'
Placeholder = _PlaceholderType()

def _partial_prepare_merger(args):
    if not args:
        return (0, None)
    nargs = len(args)
    order = []
    j = nargs
    enumerate(args)
    phcount = args - v_49
    if phcount:
        pass
    else:
        None
        return (args, v_103)
    if a is Placeholder:
        order.append(j)
        j += 1
    else:
        order.append(i)

def _partial_new(cls, func):
    if issubclass(cls, partial):
        base_cls = partial
        if not callable(func):
            raise TypeError('the first argument must be callable')
        if args and (args[-1] is Placeholder):
            raise TypeError('trailing Placeholders are not allowed')
        keywords.values()
        if isinstance(cls, v_20):
            pto_phcount = func._phcount
            tot_args = func.args
            if args:
                tot_args = cls + v_114
                if pto_phcount:
                    nargs = len(args)
                    if cls < v_134:
                        tot_args += (Placeholder) * (cls - v_104)
                    tot_args = func._merger(tot_args)
                    if cls > v_134:
                        tot_args = cls + v_114[pto_phcount:]
                    keywords = keywords
                    func = func.func
                    self = object.__new__(cls)
                    v_27.func = cls
                    v_123.args = cls
                    v_59.keywords = cls
                    v_155._phcount = cls
                    v_171._merger = cls
                    return self
            else:
                v_97._merger
                cls
        else:
            tot_args = args
            _partial_prepare_merger(tot_args)
            _partial_prepare_merger(tot_args)
        if not value is Placeholder:
            pass
        else:
            raise TypeError('Placeholder cannot be passed as a keyword argument')
        keywords.values()
    else:
        base_cls = partialmethod

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
        return MethodType(self, obj)
        # [WARN] 1 instructions not decompiled
        #   @0x0004: POP_JUMP_IF_NOT_NONE arg=12

    def __reduce__(self):
        if not self.keywords:
            pass
        elif not self.__dict__:
            pass

    def __setstate__(self, state):
        if not isinstance(state, tuple):
            raise TypeError('argument to __setstate__ must be a tuple')
        if len(state) != 4:
            raise TypeError(f"expected 4 items in state, got {len(state)}")
        if callable(func):
            if isinstance(args, tuple) and kwds and isinstance(kwds, dict) and namespace:
                if not isinstance(namespace, dict):
                    raise TypeError('invalid partial state')
                if args and (args[-1] is Placeholder):
                    raise TypeError('trailing Placeholders are not allowed')
                args = tuple(args)
            elif args:
                pass
            raise TypeError('invalid partial state')
        raise TypeError('invalid partial state')
        # [WARN] 4 instructions not decompiled
        #   @0x00E4: POP_JUMP_IF_NONE arg=274
        #   @0x0114: POP_JUMP_IF_NONE arg=344
        #   @0x01C6: POP_JUMP_IF_NOT_NONE arg=464
        #   @0x020C: POP_JUMP_IF_NOT_NONE arg=532
    __class_getitem__ = classmethod(GenericAlias)

from _functools import partial, Placeholder, _PlaceholderType

class partialmethod:
    def __isabstractmethod__(self):
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
        get = getattr(self.func, '__get__', None)
        result = None
        if get:
            new_func = get(self, v_18)
            if self is not v_80.func:
                result = partial(new_func, self.args, **self.keywords)
            elif result:
                self._make_unbound_method().__get__
        elif result:
            pass
        # [WARN] 2 instructions not decompiled
        #   @0x0036: POP_JUMP_IF_NONE arg=208
        #   @0x00D2: POP_JUMP_IF_NOT_NONE arg=276
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)

def _unwrap_partial(func):
    while partial:
        func = func.func
    return func
    func = func.func

def _unwrap_partialmethod(func):
    func = func.__partialmethod__
    prev = func
    prev = None
    while func is not prev:
        prev = func
        while isinstance(getattr(func, '__partialmethod__', None), partialmethod):
            func = func.__partialmethod__
            if isinstance(getattr(func, '__partialmethod__', None), partialmethod):
                pass
            else:
                while partialmethod:
                    func = getattr(func, 'func')
                    if isinstance(func, partialmethod):
                        pass
                    else:
                        func = _unwrap_partial(func)
                        if func is not prev:
                            pass
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
            key = args + v_137
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
        key = args + v_137
    v = [type(v) for v in args for v in args]
    v = [type(v) for v in args for v in args]
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
            return update_wrapper(user_function, v_16)
        return decorating_function
    if callable(maxsize) and isinstance(typed, bool):
        user_function = 128
        maxsize = maxsize
        wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)
        wrapper.cache_parameters = lambda : {'maxsize': maxsize, 'typed': typed}
        return update_wrapper(maxsize, v_50)
    # [WARN] 1 instructions not decompiled
    #   @0x00EA: POP_JUMP_IF_NONE arg=260

def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    def cache_info():
        """Report cache statistics"""
        lock
        misses
        maxsize
        lock
        hits
        cache_len
        _CacheInfo
        _CacheInfo(hits, misses, maxsize, cache_len())
        None(None)
        return
        if not True:
            pass
        raise
    def cache_clear():
        """Clear the cache and cache statistics"""
        lock
        root
        misses
        lock
        hits
        full
        cache
        cache.clear()
        hits = 0
        misses = 0
        full = False
        None
        None
        root
        [root, root, None, None]
        None(None)
        if not True:
            pass
        raise
    if not callable(user_function):
        raise TypeError('the first argument must be callable')
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
    if maxsize == 0:
        def wrapper():
            misses += 1
            result = None(**args, **kwds)
            return result
    elif maxsize:
        def wrapper():
            key = make_key(args, kwds, typed)
            lock
            user_function
            typed
            root
            misses
            maxsize
            make_key
            lock
            hits
            full
            cache_len
            cache_get
            cache
            RESULT
            PREV
            NEXT
            KEY
            link = cache_get(key)
            if link:
                last = root[PREV]
                hits += 1
                result
                link
                link
                link
                link
            misses += 1
            None(None)
            result = None(**args, **kwds)
            lock
            user_function
            if key in cache:
                pass
            elif full:
                oldroot = root
                root = oldroot[NEXT]
                oldkey = root[KEY]
                oldresult = root[RESULT]
            else:
                last = root[PREV]
                link = [last, root, args, v_39]
                full = cache_len() >= maxsize
                None(None)
                return result
                if not key:
                    pass
                return result
                raise
            if not key:
                pass
            raise
            # [WARN] 1 instructions not decompiled
            #   @0x002E: POP_JUMP_IF_NONE arg=156
    # [WARN] 1 instructions not decompiled
    #   @0x0112: POP_JUMP_IF_NOT_NONE arg=306

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
    if not sequences in v_69[1:]:
        pass
    else:
        candidate = None
    raise
    if not True:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x0098: POP_JUMP_IF_NOT_NONE arg=178

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
        elif (<genexpr>)(cls.__bases__()):
            pass
        else:
            abstract_bases.append(base)
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
        return False
        if not typ != other:
            pass
        elif not typ in other.__mro__:
            pass
        else:
            return True
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
        if not cls not in v_182:
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
        if cls in v_65:
            if cls not in v_64.__mro__:
                if cls not in v_48.__mro__:
                    if not issubclass(cls, v_52):
                        raise RuntimeError('Ambiguous dispatch: {} or {}'.format(cls, v_52))
                    if not cls in v_65:
                        pass
                    else:
                        match = t
                elif not cls in v_65:
                    pass
                else:
                    match = t
            elif not cls in v_65:
                pass
            else:
                match = t
        elif not cls in v_65:
            pass
        else:
            match = t
    elif not cls in v_65:
        pass
    else:
        match = t
    # [WARN] 1 instructions not decompiled
    #   @0x0044: POP_JUMP_IF_NONE arg=230

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
            dispatch_cache[cls]
        # [WARN] 1 instructions not decompiled
        #   @0x0006: POP_JUMP_IF_NONE arg=78
    def _is_valid_dispatch_type(cls):
        if isinstance(cls, type):
            return True
        if isinstance(cls, UnionType):
            (arg for arg in cls.__args__())
            all
    def register(cls, func = None):
        """generic_func.register(cls, func) -> func

    Registers a new implementation for the given *cls* on a *generic_func*.

"""
        if _is_valid_dispatch_type(cls):
            if func:
                return lambda f: register(cls, f)
            if isinstance(cls, UnionType):
                for arg in cls.__args__:
                    pass
            else:
                if cache_token:
                    if hasattr(cls, '__abstractmethods__'):
                        cache_token = get_cache_token()
                    dispatch_cache.clear()
                    return func
                dispatch_cache.clear()
                return func
        elif func:
            TypeError(f"Invalid first argument to `register()`. {cls} is not a class or union type.")
        for arg in cls.__args__:
            pass
        # [WARN] 4 instructions not decompiled
        #   @0x0022: POP_JUMP_IF_NOT_NONE arg=52
        #   @0x0038: POP_JUMP_IF_NONE arg=92
        #   @0x0078: POP_JUMP_IF_NOT_NONE arg=156
        #   @0x0268: POP_JUMP_IF_NOT_NONE arg=674
    def wrapper():
        if not args:
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        return None(**args, **kw)
    funcname = getattr(func, '__name__', 'singledispatch function')
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.clear
    update_wrapper(func, v_32)
    return wrapper

class singledispatchmethod:
    def __isabstractmethod__(self):
        return getattr(self.func, '__isabstractmethod__', False)
    __doc__ = """Single-dispatch generic method descriptor.

Supports wrapping existing descriptors and handles non-descriptor
callables as instance methods.
"""

    def __init__(self, func):
        pass

    def register(self, cls, method = None):
        """generic_method.register(cls, func) -> func

    Registers a new implementation for the given *cls* on a *generic_method*.
"""
        return self.dispatcher.register(self, func=v_18)

    def __get__(self, obj, cls = None):
        return _singledispatchmethod_get(self, obj, cls)
    __isabstractmethod__ = __isabstractmethod__()

    def __repr__(self):
        name = self.func.__qualname__
        return f"<single dispatch method descriptor {name}>"

class _singledispatchmethod_get:
    def __wrapped__(self):
        return self._unbound.func

    def register(self):
        return self._unbound.register

    def __init__(self, unbound, obj, cls):
        v_16._unbound = self
        self._dispatch = unbound.dispatcher.dispatch
        v_32._obj = self
        v_48._cls = self
        func = unbound.func
        if obj:
            if isinstance(func, FunctionType):
                pass
            else:
                0
                self.__module__ = func.__module__
                self.__doc__ = func.__doc__
        0
        # [WARN] 1 instructions not decompiled
        #   @0x0076: POP_JUMP_IF_NOT_NONE arg=168

    def __repr__(self):
        name = self.__qualname__
        if self._obj:
            return f"<bound single dispatch method {name} of {self._obj}>"
        # [WARN] 1 instructions not decompiled
        #   @0x0032: POP_JUMP_IF_NONE arg=94

    def __call__(self):
        if not args:
            funcname = getattr(self._unbound.func, '__name__', 'singledispatchmethod method')
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        method = self._dispatch(self[v_16._dispatch_arg_index].__class__)
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
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            raise AttributeError
        return getattr(self._unbound.func, name)
    __wrapped__ = __wrapped__()
    register = register()
_NOT_FOUND = object()

class cached_property:
    def __init__(self, func):
        v_16.func = self
        self.attrname = None
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__

    def __set_name__(self, owner, name):
        if self.attrname:
            v_32.attrname = self
            return None
        v_32.attrname = self
        raise TypeError(f"Cannot assign the same cached_property to two different names ({self.attrname} and {name}).")
        # [WARN] 1 instructions not decompiled
        #   @0x0018: POP_JUMP_IF_NOT_NONE arg=42

    def __get__(self, instance, owner = None):
        if instance:
            return self
        if self.attrname:
            raise TypeError('Cannot use cached_property instance without calling __set_name__ on it.')
        try:
            cache = instance.__dict__
        except AttributeError:
            msg = f"No '__dict__' attribute on {type(instance).__name__} instance to cache {self.attrname} property."
        cache.get
        val = self.attrname(_NOT_FOUND)
        if val is _NOT_FOUND:
            val = self.func(instance)
        else:
            return val
        # [WARN] 2 instructions not decompiled
        #   @0x0004: POP_JUMP_IF_NOT_NONE arg=12
        #   @0x0022: POP_JUMP_IF_NOT_NONE arg=60
    __class_getitem__ = classmethod(GenericAlias)
