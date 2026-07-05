# Decompiled from: <module>

def reduce(function, sequence, /, initial):
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
    for element in it:
        value = function(value, element)

def _PlaceholderType():
    '_PlaceholderType'
    __module__ = __name__
    __qualname__ = '_PlaceholderType'
    __firstlineno__ = 278
    __doc__ = """The type of the Placeholder singleton.

Used as a placeholder for partial arguments.
"""
    _PlaceholderType__instance = None
    __slots__ = []
    def __init_subclass__(cls):
        'type \''
        raise TypeError(f"type '{cls.__name__}' is not an acceptable base type")
    def __new__(cls):
        if cls._PlaceholderType__instance:
            cls._PlaceholderType__instance = object.__new__(cls)
            return cls._PlaceholderType__instance
        cls._PlaceholderType__instance = object.__new__(cls)
        return cls._PlaceholderType__instance
    def __repr__(self):
        'Placeholder'
        return 'Placeholder'
    def __reduce__(self):
        'Placeholder'
        return 'Placeholder'
    __static_attributes__ = []
    __classdictcell__ = __classdict__

def _partial_prepare_merger(args):
    if not args:
        return (0, None)
    else:
        nargs = len(args)
        order = []
        j = nargs
        enumerate(args)
    # [Block @0x004A] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')

def _partial_new(cls, func):
    'the first argument must be callable'
    base_cls = partialmethod
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
                        pass
                else:
                    tot_args = args
        keywords.values()
    else:
        base_cls = partialmethod
    tot_args = func._merger(tot_args)
    keywords = keywords
    func = func.func

def _partial_repr(self):
    cls = type(self)
    module = cls.__module__
    qualname = cls.__qualname__
    args = [repr(self.func)]
    args.extend(map(repr, self.args))
    ((v, k) for (v, k) in self.keywords.items()())
    return f"{module}.{qualname}({', '.join(args)})"

def partial():
    'partial'
    __module__ = __name__
    __qualname__ = 'partial'
    __firstlineno__ = 374
    __doc__ = """New function with partial application of the given arguments
and keywords.
"""
    __slots__ = ('func', 'args', 'keywords', '_phcount', '_merger', '__dict__', '__weakref__')
    __new__ = _partial_new
    __repr__ = recursive_repr()(_partial_repr)
    def __call__(self):
        phcount = self._phcount
    def __get__(self, obj, objtype=None):
        if obj:
            return self
        pass
        return MethodType(self, obj)
    def __reduce__(self):
        if not self.keywords:
            return None
        return self.__dict__ or None
    def __setstate__(self, state):
        'argument to __setstate__ must be a tuple'
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
            pass
            raise TypeError('invalid partial state')
        raise TypeError('invalid partial state')
        # [WARN] 3 instructions not decompiled
        #   @0x00EC: POP_JUMP_IF_NONE arg=286
        #   @0x0120: POP_JUMP_IF_NONE arg=360
        #   @0x01E2: POP_JUMP_IF_NOT_NONE arg=494
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__dict__', '_merger', '_phcount', 'args', 'func', 'keywords')
    __classdictcell__ = __classdict__

def partialmethod():
    'partialmethod'
    def __isabstractmethod__(self):
        '__isabstractmethod__'
        return getattr(self.func, '__isabstractmethod__', False)
    __module__ = __name__
    __qualname__ = 'partialmethod'
    __firstlineno__ = 448
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
        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.__partialmethod__ = self
        return _method
    def __get__(self, obj, cls=None):
        '__get__'
        new_func = get(obj, cls)
        # [Block @0x0000] unreachable jump
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = []
    __classdictcell__ = __classdict__

def _unwrap_partial(func):
    pass
    while isinstance(func, partial):
        func = func.func

def _unwrap_partialmethod(func):
    prev = None
    while func is not prev:
        prev = func
        while isinstance(getattr(func, '__partialmethod__', None), partialmethod):
            func = func.__partialmethod__
        while isinstance(func, partialmethod):
            func = getattr(func, 'func')
        func = _unwrap_partial(func)

def _make_key(args, kwds, typed, kwd_mark, fasttypes, tuple, type, len):
    """Make a cache key from optionally typed positional and keyword arguments

    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.

    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.

"""
    key = args
    for item in kwds.items():
        key += item
    v = [args for v in args for v in args]

def lru_cache(maxsize, typed):
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
            wrapper.cache_parameters = lambda _: {'maxsize': maxsize, 'typed': typed}
            return update_wrapper(wrapper, user_function)
        return decorating_function
    elif callable(maxsize) and isinstance(typed, bool):
        user_function = 128
        maxsize = maxsize
        wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)
        wrapper.cache_parameters = lambda _: {'maxsize': maxsize, 'typed': typed}
        return update_wrapper(wrapper, user_function)
    # [WARN] 1 instructions not decompiled
    #   @0x00F2: POP_JUMP_IF_NONE arg=270

def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    'the first argument must be callable'
    def cache_info():
        'Report cache statistics'
        pass
    def cache_clear():
        'Clear the cache and cache statistics'
        pass
    sentinel = object()
    make_key = _make_key
    PREV = 0
    NEXT = 1
    KEY = 2
    RESULT = 3
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
    sentinel = object()
    make_key = _make_key
    PREV = 0
    NEXT = 1
    KEY = 2
    RESULT = 3
    cache = {}
    hits = misses = 0
    full = False
    cache_get = cache.get
    cache_len = cache.__len__
    lock = RLock()
    root = []
    if maxsize == 0:
        def wrapper():
            misses += 1
            result = None
            return result
    elif maxsize:
        def wrapper():
            last = root[PREV]
            hits += 1
            result
            return result
            # [WARN] 1 instructions not decompiled
            #   @0x003E: POP_JUMP_IF_NONE arg=192

def cache(user_function):
    'Simple lightweight unbounded cache.  Sometimes called "memoize".'
    return lru_cache(maxsize=None)(user_function)

def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

    Adapted from https://docs.python.org/3/howto/mro.html.

"""
    sequences = [s for s in sequences if s for s1 in sequences if s if seq[0] == candidate for s2 in s1 if s if seq[0] == candidate for seq in result if s if seq[0] == candidate]

def _c3_mro(cls, abcs):
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
    boundary = len(cls.__bases__) - i
    # [Block @0x0040] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')

def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

    Includes relevant abstract base classes (with their respective bases) from
    the *types* iterable. Uses a modified C3 linearization algorithm.

"""
    def is_related(typ):
        '__mro__'
        if (typ not in bases) and hasattr(typ, '__mro__'):
            return not isinstance(typ, GenericAlias) and issubclass(cls, typ)
    def is_strict_base(typ):
        types
        types
        for other in types:
            if not typ != other:
                pass
            elif not typ in other.__mro__:
                pass
            else:
                return True
    n = [n for n in types if is_related(n) for n in n if is_related(n) for typ in set if is_related(n) for sub in typ if is_related(n) for s in found if is_related(n) for sub in found if is_related(n) for subcls in sub if is_related(n)]

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
    for t in mro:
        if match:
            if t in registry:
                if t not in cls.__mro__:
                    if match not in cls.__mro__:
                        if not issubclass(match, t):
                            raise RuntimeError('Ambiguous dispatch: {} or {}'.format(match, t))
                        elif not t in registry:
                            pass
                        else:
                            match = t
                    elif not t in registry:
                        pass
                    else:
                        match = t
                elif not t in registry:
                    pass
                else:
                    match = t
            elif not t in registry:
                pass
            else:
                match = t
        elif not t in registry:
            pass
        else:
            match = t
    # [WARN] 1 instructions not decompiled
    #   @0x0044: POP_JUMP_IF_NONE arg=240

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
        current_token = get_cache_token()
        # [Block @0x0000] unreachable jump
    def _is_valid_dispatch_type(cls):
        if isinstance(cls, type):
            return True
        if isinstance(cls, UnionType) and (all is None):
            for _ in cls.__args__():
                pass
        else:
            (arg for arg in cls.__args__())
    def register(cls, func=None):
        """generic_func.register(cls, func) -> func

    Registers a new implementation for the given *cls* on a *generic_func*.

"""
        if _is_valid_dispatch_type(cls):
            if func:
                return lambda f: register(cls, f)
            pass
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
        # [WARN] 1 instructions not decompiled
        #   @0x0024: POP_JUMP_IF_NOT_NONE arg=56
    def wrapper():
        ' requires at least 1 positional argument'
        if args:
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        return None
    funcname = getattr(func, '__name__', 'singledispatch function')
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.clear
    update_wrapper(wrapper, func)
    return wrapper

def singledispatchmethod():
    'singledispatchmethod'
    def __isabstractmethod__(self):
        '__isabstractmethod__'
        return getattr(self.func, '__isabstractmethod__', False)
    __module__ = __name__
    __qualname__ = 'singledispatchmethod'
    __firstlineno__ = 1021
    __doc__ = """Single-dispatch generic method descriptor.

Supports wrapping existing descriptors and handles non-descriptor
callables as instance methods.
"""
    def __init__(self, func):
        '__get__'
        # [Block @0x0000] unreachable jump
        pass
    def register(self, cls, method=None):
        """generic_method.register(cls, func) -> func

    Registers a new implementation for the given *cls* on a *generic_method*.
"""
        return self.dispatcher.register(cls, func=method)
    def __get__(self, obj, cls=None):
        return _singledispatchmethod_get(self, obj, cls)
    __isabstractmethod__ = __isabstractmethod__()
    def __repr__(self):
        '?'
        # orphan @0x0000
        pass
    __static_attributes__ = ('dispatcher', 'func')
    __classdictcell__ = __classdict__

def _singledispatchmethod_get():
    '_singledispatchmethod_get'
    def __wrapped__(self):
        return self._unbound.func
    def register(self):
        return self._unbound.register
    __module__ = __name__
    __qualname__ = '_singledispatchmethod_get'
    __firstlineno__ = 1059
    def __init__(self, unbound, obj, cls):
        # [Block @0x0000] unreachable jump
        pass
    def __repr__(self):
        '?'
        # orphan @0x0000
        pass
    def __call__(self):
        '__name__'
        method = self._dispatch(args[self._dispatch_arg_index].__class__)
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
            return skip_bound_arg and None
        return None
        method = method.__get__(self._obj, self._cls)
    def __getattr__(self, name):
        '__name__'
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            raise AttributeError
        return getattr(self._unbound.func, name)
    __wrapped__ = __wrapped__()
    register = register()
    __static_attributes__ = ('__doc__', '__module__', '_cls', '_dispatch', '_dispatch_arg_index', '_obj', '_unbound')
    __classdictcell__ = __classdict__

def cached_property():
    'cached_property'
    __module__ = __name__
    __qualname__ = 'cached_property'
    __firstlineno__ = 1142
    def __init__(self, func):
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__
    def __set_name__(self, owner, name):
        if self.attrname:
            self.attrname = name
        else:
            pass
        if name != self.attrname:
            raise TypeError(f"Cannot assign the same cached_property to two different names ({self.attrname} and {name}).")
    def __get__(self, instance, owner=None):
        val = self.attrname(_NOT_FOUND)
        try:
            pass
        except AttributeError:
            msg = f"No '__dict__' attribute on {type(instance).__name__} instance to cache {self.attrname} property."
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__doc__', '__module__', 'attrname', 'func')
    __classdictcell__ = __classdict__
# orphan @0x0000
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

def update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
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
    for attr in assigned:
        pass
        value = getattr(wrapped, attr)
        setattr(wrapper, attr, value)
    attr = {getattr(wrapper, attr).update(getattr(wrapped, attr, {})): getattr(wrapper, attr).update(getattr(wrapped, attr, {})) for attr in updated}

def wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

    Returns a decorator that invokes update_wrapper() with the decorated
    function as the wrapper argument and the arguments to wraps() as the
    remaining arguments. Default arguments are as for update_wrapper().
    This is a convenience function to simplify applying partial() to
    update_wrapper().
"""
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)

def _gt_from_lt(self, other):
    'Return a > b.  Computed by @total_ordering from (not a < b) and (a != b).'
    op_result = type(self).__lt__(self, other)
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and (self != other)

def _le_from_lt(self, other):
    'Return a <= b.  Computed by @total_ordering from (a < b) or (a == b).'
    op_result = type(self).__lt__(self, other)
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return op_result or (self == other)

def _ge_from_lt(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a < b).'
    op_result = type(self).__lt__(self, other)
    op_result = type(self).__lt__(self, other)
    return (op_result is NotImplemented) and op_result

def _ge_from_le(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b).'
    op_result = type(self).__le__(self, other)
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result or (self == other)

def _lt_from_le(self, other):
    'Return a < b.  Computed by @total_ordering from (a <= b) and (a != b).'
    op_result = type(self).__le__(self, other)
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return op_result and (self != other)

def _gt_from_le(self, other):
    'Return a > b.  Computed by @total_ordering from (not a <= b).'
    op_result = type(self).__le__(self, other)
    op_result = type(self).__le__(self, other)
    return (op_result is NotImplemented) and op_result

def _lt_from_gt(self, other):
    'Return a < b.  Computed by @total_ordering from (not a > b) and (a != b).'
    op_result = type(self).__gt__(self, other)
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and (self != other)

def _ge_from_gt(self, other):
    'Return a >= b.  Computed by @total_ordering from (a > b) or (a == b).'
    op_result = type(self).__gt__(self, other)
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return op_result or (self == other)

def _le_from_gt(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a > b).'
    op_result = type(self).__gt__(self, other)
    op_result = type(self).__gt__(self, other)
    return (op_result is NotImplemented) and op_result

def _le_from_ge(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b).'
    op_result = type(self).__ge__(self, other)
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result or (self == other)

def _gt_from_ge(self, other):
    'Return a > b.  Computed by @total_ordering from (a >= b) and (a != b).'
    op_result = type(self).__ge__(self, other)
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    return op_result and (self != other)

def _lt_from_ge(self, other):
    'Return a < b.  Computed by @total_ordering from (not a >= b).'
    op_result = type(self).__ge__(self, other)
    op_result = type(self).__ge__(self, other)
    return (op_result is NotImplemented) and op_result
_convert = frozendict({'__lt__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__le__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__gt__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__ge__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})

def total_ordering(cls):
    'Class decorator that fills in missing ordering methods'
    roots = {op for op in _convert if getattr(cls, op, None) is not getattr(object, op, None)}

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
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
