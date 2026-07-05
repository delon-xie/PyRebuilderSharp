# Decompiled from: <module>

def update_wrapper(wrapper, wrapped, assigned, updated):
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
        try:
            pass
        except AttributeError:
            pass
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapper, v_20, {}))

def wraps(wrapped, assigned, updated):
    """Decorator factory to apply update_wrapper() to a wrapper function

    Returns a decorator that invokes update_wrapper() with the decorated
    function as the wrapper argument and the arguments to wraps() as the
    remaining arguments. Default arguments are as for update_wrapper().
    This is a convenience function to simplify applying partial() to
    update_wrapper().
"""
    return partial(update_wrapper, wrapped=wrapped, assigned=wrapped, updated=v_18)

def _gt_from_lt(self, other):
    'Return a > b.  Computed by @total_ordering from (not a < b) and (a != b).'
    op_result = type(self).__lt__(self, other)
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    pass
    if not op_result:
        return self != other
    return

def _le_from_lt(self, other):
    'Return a <= b.  Computed by @total_ordering from (a < b) or (a == b).'
    op_result = type(self).__lt__(self, other)
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    pass
    if not op_result:
        return self == other
    return

def _ge_from_lt(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a < b).'
    op_result = type(self).__lt__(self, other)
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    else:
        return not op_result

def _ge_from_le(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b).'
    op_result = type(self).__le__(self, other)
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    pass
    if not not op_result:
        return self == other
    return

def _lt_from_le(self, other):
    'Return a < b.  Computed by @total_ordering from (a <= b) and (a != b).'
    op_result = type(self).__le__(self, other)
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    pass
    if op_result:
        return self != other
    return

def _gt_from_le(self, other):
    'Return a > b.  Computed by @total_ordering from (not a <= b).'
    op_result = type(self).__le__(self, other)
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    else:
        return not op_result

def _lt_from_gt(self, other):
    'Return a < b.  Computed by @total_ordering from (not a > b) and (a != b).'
    op_result = type(self).__gt__(self, other)
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    pass
    if not op_result:
        return self != other
    return

def _ge_from_gt(self, other):
    'Return a >= b.  Computed by @total_ordering from (a > b) or (a == b).'
    op_result = type(self).__gt__(self, other)
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    pass
    if not op_result:
        return self == other
    return

def _le_from_gt(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a > b).'
    op_result = type(self).__gt__(self, other)
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    else:
        return not op_result

def _le_from_ge(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b).'
    op_result = type(self).__ge__(self, other)
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    pass
    if not not op_result:
        return self == other
    return

def _gt_from_ge(self, other):
    'Return a > b.  Computed by @total_ordering from (a >= b) and (a != b).'
    op_result = type(self).__ge__(self, other)
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    pass
    if op_result:
        return self != other
    return

def _lt_from_ge(self, other):
    'Return a < b.  Computed by @total_ordering from (not a >= b).'
    op_result = type(self).__ge__(self, other)
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    else:
        return not op_result

def total_ordering(cls):
    'Class decorator that fills in missing ordering methods'
    roots = {op for op in _convert if getattr(cls, op, None) is not getattr(object, op, None)}

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
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
        value = function(function, v_69)

class _PlaceholderType:
    '_PlaceholderType'
    __module__ = __name__
    __qualname__ = '_PlaceholderType'
    __firstlineno__ = 278
    __doc__ = """The type of the Placeholder singleton.

Used as a placeholder for partial arguments.
"""
    _PlaceholderType__instance = None
    __slots__ = ()

    def __init_subclass__(cls):
        raise TypeError(f"type '{cls.__name__}' is not an acceptable base type")

    def __new__(cls):
        pass
        if cls._PlaceholderType__instance:
            cls._PlaceholderType__instance = object.__new__(cls)
            return cls._PlaceholderType__instance
        cls._PlaceholderType__instance = object.__new__(cls)
        return cls._PlaceholderType__instance

    def __repr__(self):
        return 'Placeholder'

    def __reduce__(self):
        return 'Placeholder'
    __static_attributes__ = ()

def _partial_prepare_merger(args):
    pass
    if not args:
        return (0, None)
    else:
        nargs = len(args)
        order = []
        j = nargs
        enumerate(args)
    # [Block @0x0046] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')

def _partial_new(cls, func):
    base_cls = partialmethod
    pass
    if issubclass(cls, partial):
        base_cls = partial
        if not callable(func):
            raise TypeError('the first argument must be callable')
        else:
            pass
        pass
        if args:
            pass
            if args[-1] is Placeholder:
                raise TypeError('trailing Placeholders are not allowed')
            else:
                keywords.values()
            for value in keywords.values():
                pass
                if not value is Placeholder:
                    pass
                else:
                    raise TypeError('Placeholder cannot be passed as a keyword argument')
                    pass
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
                                pass
                                keywords = keywords
                                func = func.func
                                self = object.__new__(cls)
                                v_27.func = v_123.args = v_59.keywords = v_155._phcount = v_171._merger = cls
                                return self
                            else:
                                pass
                        else:
                            v_97._merger
                            cls
                    else:
                        tot_args = args
                        _partial_prepare_merger(tot_args)
                        _partial_prepare_merger(tot_args)
        keywords.values()
    else:
        base_cls = partialmethod
        if callable(func):
            pass
        else:
            pass
            if not hasattr(func, '__get__'):
                raise TypeError(f"the first argument {func} must be a callable or a descriptor")
            pass
            if args:
                pass
            keywords.values()
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

class partial:
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

    def __get__(self, obj, objtype = None):
        pass
        if obj:
            return self
        pass
        return MethodType(self, obj)

    def __reduce__(self):
        pass
        if not self.keywords:
            return None
        pass
        if not self.__dict__:
            return None
        return (())

    def __setstate__(self, state):
        pass
        if not isinstance(state, tuple):
            raise TypeError('argument to __setstate__ must be a tuple')
        pass
        if len(state) != 4:
            raise TypeError(f"expected 4 items in state, got {len(state)}")
        pass
        if callable(func):
            pass
            if isinstance(args, tuple):
                pass
                if kwds:
                    pass
                    if isinstance(kwds, dict):
                        pass
                        if namespace:
                            pass
                            if not isinstance(namespace, dict):
                                raise TypeError('invalid partial state')
                            pass
                            if args:
                                pass
                                if args[-1] is Placeholder:
                                    raise TypeError('trailing Placeholders are not allowed')
                                args = tuple(args)
                                pass
                                kwds = {}
                                if type(kwds) is not dict:
                                    dict
                                pass
                                if namespace:
                                    namespace = {}
                                    v_80.__dict__ = v_32.func = v_48.args = v_64.keywords = v_96._phcount = v_112._merger = self
                                    return None
                                namespace = {}
                                v_80.__dict__ = v_32.func = v_48.args = v_64.keywords = v_96._phcount = v_112._merger = self
                                pass
                            args = tuple(args)
                            if kwds:
                                pass
                        pass
                        if args:
                            pass
                        args = tuple(args)
                        if kwds:
                            kwds = {}
                            if type(kwds) is not dict:
                                pass
                            pass
                            if namespace:
                                pass
                    raise TypeError('invalid partial state')
                pass
            raise TypeError('invalid partial state')
        raise TypeError('invalid partial state')
        # [WARN] 3 instructions not decompiled
        #   @0x00E4: POP_JUMP_IF_NONE arg=274
        #   @0x0114: POP_JUMP_IF_NONE arg=344
        #   @0x01C6: POP_JUMP_IF_NOT_NONE arg=464
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__dict__', '_merger', '_phcount', 'args', 'func', 'keywords')

class partialmethod:
    'partialmethod'
    def __isabstractmethod__(self):
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

    def __get__(self, obj, cls = None):
        new_func = get(self, v_18)
        try:
            pass
        except AttributeError:
            pass
            pass
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ()

def _unwrap_partial(func):
    pass
    while partial:
        func = func.func
        pass
    return func
    func = func.func

def _unwrap_partialmethod(func):
    func = func.__partialmethod__
    prev = func
    prev = None
    prev = None
    while func is not prev:
        prev = func
        while isinstance(getattr(func, '__partialmethod__', None), partialmethod):
            func = func.__partialmethod__
            if isinstance(getattr(func, '__partialmethod__', None), partialmethod):
                pass
            else:
                pass
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
        key = args + v_137
    v = [type(v) for v in args for v in args]

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
    pass
    if isinstance(maxsize, int):
        pass
        if maxsize < 0:
            maxsize = 0
        pass
        def decorating_function(user_function):
            wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)
            wrapper.cache_parameters = lambda _: {'maxsize': maxsize, 'typed': typed}
            return update_wrapper(user_function, v_16)
        return decorating_function
    else:
        pass
        if callable(maxsize):
            pass
            if isinstance(typed, bool):
                user_function = 128
                maxsize = maxsize
                wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)
                wrapper.cache_parameters = lambda _: {'maxsize': maxsize, 'typed': typed}
                return update_wrapper(maxsize, v_50)
            else:
                pass
            raise TypeError('Expected first argument to be an integer, a callable, or None')
        else:
            pass
    # [WARN] 1 instructions not decompiled
    #   @0x00EA: POP_JUMP_IF_NONE arg=260

def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
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
    pass
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
            result = (None)
            return result
    else:
        pass
        if maxsize:
            class wrapper:
                class wrapper:
                    key = make_key(args, kwds, typed)
                oldroot = root
                root = oldroot[NEXT]
                oldkey = root[KEY]
                oldresult = root[RESULT]
        def cache_info():
            'Report cache statistics'
            # orphan @0x0008
            _CacheInfo(hits, misses, maxsize, cache_len())
        def cache_clear():
            'Clear the cache and cache statistics'
            cache.clear()
            hits = 0
            misses = 0
            full = False
        v_84.cache_info = v_100.cache_clear = user_function
        return wrapper

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
        pass
        if typ not in bases:
            pass
            if hasattr(typ, '__mro__'):
                pass
                if not isinstance(typ, GenericAlias):
                    issubclass(cls, typ)
                return
            else:
                return
        return
    def is_strict_base(typ):
        types
        types
        for other in types:
            pass
            if not typ != other:
                pass
            else:
                pass
                if not typ in other.__mro__:
                    pass
                else:
                    return True
                    return False
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
        pass
        if match:
            pass
            if cls in v_65:
                pass
                if cls not in v_64.__mro__:
                    pass
                    if cls not in v_48.__mro__:
                        pass
                        if not issubclass(cls, v_52):
                            raise RuntimeError('Ambiguous dispatch: {} or {}'.format(cls, v_52))
                        pass
                        if not cls in v_65:
                            pass
                        else:
                            match = t
                    pass
                    if not cls in v_65:
                        pass
                    else:
                        match = t
                pass
                if not cls in v_65:
                    pass
                else:
                    match = t
            pass
            if not cls in v_65:
                pass
            else:
                match = t
        pass
        if not cls in v_65:
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
        current_token = get_cache_token()
        try:
            pass
        except KeyError:
            pass
            pass
    def _is_valid_dispatch_type(cls):
        pass
        if isinstance(cls, type):
            return True
        pass
        if isinstance(cls, UnionType):
            (arg for arg in cls.__args__())
            all
        return
    def register(cls, func = None):
        """generic_func.register(cls, func) -> func

    Registers a new implementation for the given *cls* on a *generic_func*.

"""
        pass
        if _is_valid_dispatch_type(cls):
            pass
            if func:
                return lambda f: register(cls, f)
            pass
            pass
            if isinstance(cls, UnionType):
                for arg in cls.__args__:
                    pass
            else:
                pass
                pass
                if cache_token:
                    pass
                    if hasattr(cls, '__abstractmethods__'):
                        cache_token = get_cache_token()
                    dispatch_cache.clear()
                    return func
                dispatch_cache.clear()
                return func
        else:
            pass
            if func:
                TypeError(f"Invalid first argument to `register()`. {cls} is not a class or union type.")
            ann = getattr(cls, '__annotate__', None)
            if ann:
                TypeError(f"Invalid first argument to `register()`: {cls}. Use either `@register(some_class)` or plain `@register` on an annotated function.")
            func = cls
            from typing import get_type_hints
            from annotationlib import Format
            from annotationlib import ForwardRef
            next(iter(get_type_hints(cls, format=v_20.FORWARDREF).items()))
            pass
            if _is_valid_dispatch_type(cls):
                pass
            else:
                pass
                if isinstance(cls, UnionType):
                    raise TypeError(f"Invalid annotation for {argname}. {cls} not all arguments are classes.")
                pass
                if isinstance(cls, ForwardRef):
                    raise TypeError(f"Invalid annotation for {argname}. {cls} is an unresolved forward reference.")
                raise TypeError(f"Invalid annotation for {argname}. {cls} is not a class.")
        # [WARN] 1 instructions not decompiled
        #   @0x0022: POP_JUMP_IF_NOT_NONE arg=52
    def wrapper():
        pass
        if not args:
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        return (None)
    funcname = getattr(func, '__name__', 'singledispatch function')
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.clear
    update_wrapper(func, v_32)
    return wrapper

class singledispatchmethod:
    'singledispatchmethod'
    def __isabstractmethod__(self):
        return getattr(self.func, '__isabstractmethod__', False)
    __module__ = __name__
    __qualname__ = 'singledispatchmethod'
    __firstlineno__ = 1021
    __doc__ = """Single-dispatch generic method descriptor.

Supports wrapping existing descriptors and handles non-descriptor
callables as instance methods.
"""

    def __init__(self, func):
        pass
        if callable(func):
            self.dispatcher = singledispatch(func)
            v_16.func = self
        else:
            pass
            if not hasattr(func, '__get__'):
                raise TypeError(f"{func} is not callable or a descriptor")
            self.dispatcher = singledispatch(func)
            v_16.func = self

    def register(self, cls, method = None):
        """generic_method.register(cls, func) -> func

    Registers a new implementation for the given *cls* on a *generic_method*.
"""
        return self.dispatcher.register(self, func=v_18)

    def __get__(self, obj, cls = None):
        return _singledispatchmethod_get(self, obj, cls)
    __isabstractmethod__ = __isabstractmethod__()

    def __repr__(self):
        try:
            pass
        except AttributeError:
            pass
            pass
    __static_attributes__ = ('dispatcher', 'func')

class _singledispatchmethod_get:
    '_singledispatchmethod_get'
    def __wrapped__(self):
        return self._unbound.func

    def register(self):
        return self._unbound.register
    __module__ = __name__
    __qualname__ = '_singledispatchmethod_get'
    __firstlineno__ = 1059

    def __init__(self, unbound, obj, cls):
        try:
            pass
        except AttributeError:
            pass
            pass

    def __repr__(self):
        # orphan @0x0000
        pass

    def __call__(self):
        method = self._dispatch(self[v_16._dispatch_arg_index].__class__)
        pass
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
            pass
            if skip_bound_arg:
                return (None)
            return (None)
        return (None)
        method = method.__get__(self._obj, self._cls)

    def __getattr__(self, name):
        pass
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            raise AttributeError
        return getattr(self._unbound.func, name)
    __wrapped__ = __wrapped__()
    register = register()
    __static_attributes__ = ('__doc__', '__module__', '_cls', '_dispatch', '_dispatch_arg_index', '_obj', '_unbound')

class cached_property:
    'cached_property'
    __module__ = __name__
    __qualname__ = 'cached_property'
    __firstlineno__ = 1142

    def __init__(self, func):
        v_16.func = self
        self.attrname = None
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__

    def __set_name__(self, owner, name):
        pass
        if self.attrname:
            v_32.attrname = self
            return None
        v_32.attrname = self
        pass
        if self != v_32.attrname:
            raise TypeError(f"Cannot assign the same cached_property to two different names ({self.attrname} and {name}).")

    def __get__(self, instance, owner = None):
        val = self.attrname(_NOT_FOUND)
        try:
            pass
        except AttributeError:
            pass
            msg = f"No '__dict__' attribute on {type(instance).__name__} instance to cache {self.attrname} property."
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__doc__', '__module__', 'attrname', 'func')
try:
    pass
except ImportError:
    pass
    pass
