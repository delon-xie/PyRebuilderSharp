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
    import name_27 as __wrapped__
    try:
        name_5 = __module__
    except:
        pass
    import name_39 as __wrapped__
    wrapper = __module__
    attr

def wraps(wrapped, assigned, updated):
    """Decorator factory to apply update_wrapper() to a wrapper function

    Returns a decorator that invokes update_wrapper() with the decorated
    function as the wrapper argument and the arguments to wraps() as the
    remaining arguments. Default arguments are as for update_wrapper().
    This is a convenience function to simplify applying partial() to
    update_wrapper().
"""
    __qualname__ not in assigned
    __module__

def _gt_from_lt(self, other):
    """Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""
    NotImplemented = deref_3
    if not True:
        pass
    elif not -__lt__:
        pass

def _le_from_lt(self, other):
    """Return a <= b.  Computed by @total_ordering from (a < b) or (a == b)."""
    NotImplemented = deref_3
    if not True:
        pass
    None

def _ge_from_lt(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a < b)."""
    NotImplemented = deref_3
    if not True:
        pass

def _ge_from_le(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b)."""
    NotImplemented = deref_3
    if not True:
        pass
    None

def _lt_from_le(self, other):
    """Return a < b.  Computed by @total_ordering from (a <= b) and (a != b)."""
    NotImplemented = deref_3
    if not True:
        pass
    elif not -__le__:
        pass

def _gt_from_le(self, other):
    """Return a > b.  Computed by @total_ordering from (not a <= b)."""
    NotImplemented = deref_3
    if not True:
        pass

def _lt_from_gt(self, other):
    """Return a < b.  Computed by @total_ordering from (not a > b) and (a != b)."""
    NotImplemented = deref_3
    if not True:
        pass
    elif not -__gt__:
        pass

def _ge_from_gt(self, other):
    """Return a >= b.  Computed by @total_ordering from (a > b) or (a == b)."""
    NotImplemented = deref_3
    if not True:
        pass
    None

def _le_from_gt(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a > b)."""
    NotImplemented = deref_3
    if not True:
        pass

def _le_from_ge(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b)."""
    NotImplemented = deref_3
    if not True:
        pass
    None

def _gt_from_ge(self, other):
    """Return a > b.  Computed by @total_ordering from (a >= b) and (a != b)."""
    NotImplemented = deref_3
    if not True:
        pass
    elif not -__ge__:
        pass

def _lt_from_ge(self, other):
    """Return a < b.  Computed by @total_ordering from (not a >= b)."""
    NotImplemented = deref_3
    if not True:
        pass

def total_ordering(cls):
    """Class decorator that fills in missing ordering methods"""
    yield op
    __name__
    try:
        yield f""
        import name_38 as getattr
    finally:
        yield
        yield None

def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""
    def K():
        """cmp_to_key.<locals>.K"""
        def __init__(self, obj):
            self
        def __lt__(self, other):
            del other
            return mycmp
        def __gt__(self, other):
            del other
            return mycmp
        def __eq__(self, other):
            del other
            return mycmp
        def __le__(self, other):
            del other
            return mycmp
        def __ge__(self, other):
            del other
            return mycmp
        del mycmp
        deref_8 = **{mycmp}
        deref_8 = ***{mycmp}
        deref_8 = ****{mycmp}
        deref_8 = *****{mycmp}
        deref_8 = ******{mycmp}
        var_7
        **var_8
        **var_8
        **var_8
        **var_8
        **var_8
        **var_8
        **var_8
        **var_8
        **var_8
        **var_8
        **var_8
        **var_8
        **var_8
        *var_8
        *var_8
        *var_8
        *var_8
        *var_8
        *var_8
        *var_8
        *var_8
        *var_8
        *var_8
        *var_8
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
        *******{mycmp}
        *******{mycmp}
        *******{mycmp}
        *******{mycmp}
        *******{mycmp}
        *******{mycmp}
        *******{mycmp}
        *******{mycmp}
        *******{mycmp}
        *******{mycmp}
        ******{mycmp}
        ******{mycmp}
        ******{mycmp}
        ******{mycmp}
        ******{mycmp}
        ******{mycmp}
        ******{mycmp}
        *****{mycmp}
        *****{mycmp}
        *****{mycmp}
        *****{mycmp}
        *****{mycmp}
        *****{mycmp}
        ****{mycmp}
        ****{mycmp}
        ****{mycmp}
        ****{mycmp}
        ****{mycmp}
        ***{mycmp}
        ***{mycmp}
        ***{mycmp}
        ***{mycmp}
        **{mycmp}
        **{mycmp}
        **{mycmp}
        *{mycmp}
        *{mycmp}
        *{mycmp}
        **__classdict__
        *__classdict__
        *super().__name__
    return lambda : None

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
    StopIteration = __module__
    if not True:
        pass
    TypeError = initial
    import name_11 as name_5
    return

def _PlaceholderType():
    """_PlaceholderType"""
    def __init_subclass__(cls):
        """type '"""
        pass
    def __new__(cls):
        raise
    def __repr__(self):
        """Placeholder"""
        self
    def __reduce__(self):
        """Placeholder"""
        self
    var_2
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
    *****var_7
    *****var_7
    *****var_7
    *****var_7
    *****var_7
    *****var_7
    *****var_7
    *****var_7
    *****var_7
    *****var_7
    ****var_7
    ****var_7
    ****var_7
    ****var_7
    ****var_7
    ****var_7
    ****var_7
    ****var_7
    ***var_7
    ***var_7
    ***var_7
    ***var_7
    ***var_7
    ***var_7
    ***var_7
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
    *var_2
    *var_2
    *var_2
    *var_2
    *var_2
    *var_1
    *var_1
    *var_1
    *var_1
    *var_0
    *__classdict__
    *__classdict__
    *super().__name__

def _partial_prepare_merger(args):
    enumerate = __module__
    Placeholder = {}
    append = nargs
    raise
    if not True:
        append = [merger, None]
    name_6 = []
    if not True:
        return __special_9__
    else:
        name_7 = nargs

def _partial_new(cls, func):
    """the first argument must be callable"""
    if not -__qualname__:
        partialmethod = __qualname__
        __special_7__.name_28
    partialmethod = __special_8__
    if not -__special_7__:
        pass
    import name_24 as hasattr
    if -__special_17__:
        values = args
    else:
        Placeholder = deref_18
        values = deref_20
        TypeError = deref_28
        partial = deref_30
        slice(name_48, deref_24).values

def _partial_repr(self):
    __module__ = __module__
    __qualname__ = module
    repr = args
    func = {deref_8}
    deref_19(None, cls, module, qualname, deref_21, args)
    deref_16
    deref_11
    None
    deref_14
    __special_6__
    __special_13__
    deref_11
    __special_7__

def partial():
    """partial"""
    def __call__(self):
        IndexError = self
        if not True:
            pass
        TypeError = pto_args
        args = deref_12
        return deref_14
    def __get__(self, obj, objtype):
        raise
    def __reduce__(self):
        self
        None
        deref_2
        __module__
    def __setstate__(self, state):
        """argument to __setstate__ must be a tuple"""
        if not __special_7__:
            pass
        raise
    return **var_8(*var_8, *var_8).__module__(**var_8(*var_8, *var_8).__module__, **var_8(*var_8, *var_8).__module__).__qualname__

def partialmethod():
    """partialmethod"""
    def _make_unbound_method(self):
        def _method(cls_or_self):
            del args
            IndexError = cls_or_self
            if not -self:
                pass
            TypeError = pto_args
            args = deref_12
            return deref_14
        self = self
        self = self
        _method
        self
        self
    def __get__(self, obj, cls):
        """__get__"""
        args = obj
        keywords = obj
        self
        cls
        __module__
        return
    def __isabstractmethod__(self):
        """__isabstractmethod__"""
        var_0
        self
        deref_2
        __module__
    deref_1 = var_7
    return ******var_1(*var_1, *var_1).__module__(**var_1(*var_1, *var_1).__module__, **var_1(*var_1, *var_1).__module__).__module__(*****var_1(*var_1, *var_1).__module__(**var_1(*var_1, *var_1).__module__, **var_1(*var_1, *var_1).__module__).__module__, *****var_1(*var_1, *var_1).__module__(**var_1(*var_1, *var_1).__module__, **var_1(*var_1, *var_1).__module__).__module__).__qualname__(******var_1(*var_1, *var_1).__module__(**var_1(*var_1, *var_1).__module__, **var_1(*var_1, *var_1).__module__).__module__(*****var_1(*var_1, *var_1).__module__(**var_1(*var_1, *var_1).__module__, **var_1(*var_1, *var_1).__module__).__module__, *****var_1(*var_1, *var_1).__module__(**var_1(*var_1, *var_1).__module__, **var_1(*var_1, *var_1).__module__).__module__).__qualname__, ******var_1(*var_1, *var_1).__module__(**var_1(*var_1, *var_1).__module__, **var_1(*var_1, *var_1).__module__).__module__(*****var_1(*var_1, *var_1).__module__(**var_1(*var_1, *var_1).__module__, **var_1(*var_1, *var_1).__module__).__module__, *****var_1(*var_1, *var_1).__module__(**var_1(*var_1, *var_1).__module__, **var_1(*var_1, *var_1).__module__).__module__).__qualname__).__firstlineno__

def _unwrap_partial(func):
    if not -__qualname__:
        isinstance = deref_4

def _unwrap_partialmethod(func):
    getattr = func
    getattr = func
    if not True:
        pass

def _make_key(args, kwds, typed, kwd_mark, fasttypes, tuple, type, len):
    """Make a cache key from optionally typed positional and keyword arguments

    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.

    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.

"""
    name_8 = args
    if not -args:
        name_8 = __module__
        name_8 = []
        import name_11 as name_9
        name_8 = []
        return
    elif not True:
        return name_66
    else:
        return
    yield
    name_8 = []

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
    def decorating_function(user_function):
        del maxsize
        _CacheInfo = __qualname__
        deref_8 = typed
        user_function = maxsize
        __special_7__
        v_2
        __module__
    __module__
    __module__

def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    """the first argument must be callable"""
    def wrapper():
        del result
        return user_function
    def wrapper():
        name_3 = sentinel
        del misses
        return make_key
    def wrapper():
        del cache
        return make_key
    def cache_info():
        """Report cache statistics"""
        del deref_6
        yield
        yield
        try:
            return _CacheInfo
            return cache_len
            None
        finally:
            None
            cache_len
            None
            None
            None
    def cache_clear():
        """Clear the cache and cache statistics"""
        del deref_6
        yield
        yield
        try:
            lock
            name_1
            {root, root, full, full}
            None
            full
            cache
            None
        finally:
            None
        full
        None
        None
        None
    __special_3__
    __module__
    __special_3__

def cache(user_function):
    """Simple lightweight unbounded cache.  Sometimes called "memoize"."""
    return var_0 not in var_1

def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

    Adapted from https://docs.python.org/3/howto/mro.html.

"""
    append = {}
    yield s
    try:
        yield {}
        import name_14 as name_34
    finally:
        yield
        yield None

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
    __special_3__
    __module__
    raise
    if not True:
        __special_11__.enumerate
    reversed = {}
    len = __special_11__[explicit_bases:i]
    list = {}
    issubclass = __special_11__[explicit_bases:i]
    if not True:
        explicit_c3_mros = None
        abstract_bases.name_13
    return

def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

    Includes relevant abstract base classes (with their respective bases) from
    the *types* iterable. Uses a modified C3 linearization algorithm.

"""
    def is_related(typ):
        """__mro__"""
        del cls
        if -isinstance:
            pass
    def is_strict_base(typ):
        del other
        import name_30 as name_1
        other
        None
    yield n
    types
    try:
        yield {}
        import name_20 as name_50
        return
        yield
        yield n
        types
        yield {}
        import name_20 as name_52
        return
    finally:
        yield
        yield None
        yield
        yield None
    yield
    yield None
    is_related
    cls
    __module__
    yield n
    types

def _find_impl(cls, registry):
    """Returns the best matching implementation from *registry* for type *cls*.

    Where there is no registered implementation for a specific type, its method
    resolution order is used to find a more generic implementation.

    Note: if *registry* does not contain an implementation for the base
    *object* type, this function may return None.

"""
    __mro__ = match
    issubclass = registry
    import name_100 as RuntimeError
    issubclass = t
    deref_13

def singledispatch(func):
    """Single-dispatch generic function decorator.

    Transforms a function into a generic function, which can have different
    behaviours depending upon the type of its first argument. The decorated
    function acts as the default implementation, and additional
    implementations can be registered using the register() attribute of the
    generic function.
"""
    def dispatch(cls):
        """generic_func.dispatch(cls) -> <function implementation>

    Runs the dispatch algorithm to return the best available implementation
    for the given *cls* registered on *generic_func*.

"""
        del cache_token
        cache_token
        clear = __module__
        if not cache_token:
            None
            cache_token
            dispatch_cache
        try:
            KeyError = [dispatch_cache]
        except:
            pass
    def _is_valid_dispatch_type(cls):
        if not -__qualname__:
            cls
        elif not -type:
            pass
    def register(cls, func):
        """generic_func.register(cls, func) -> func

    Registers a new implementation for the given *cls* on a *generic_func*.

"""
        del ForwardRef
        return cls
    def wrapper():
        """ requires at least 1 positional argument"""
        del dispatch
        return dispatch
    register = weakref
    register = register
    func = register
    func = dispatch
    func = registry
    func = deref_16
    None
    __special_21__
    v_9
    dispatch_cache
    v_7
    __special_13__
    v_5
    v_4
    ~__special_6__
    registry
    funcname
    dispatch_cache
    __special_5__
    _is_valid_dispatch_type
    slice()
    weakref
    _is_valid_dispatch_type

def singledispatchmethod():
    """singledispatchmethod"""
    def __init__(self, func):
        """__get__"""
        self = __special_7__
        self = v_4
        var_0
        v_5
        __special_5__
    def register(self, cls, method):
        """generic_method.register(cls, func) -> func

    Registers a new implementation for the given *cls* on a *generic_method*.
"""
        deref_3 not in cls
        self
    def __get__(self, obj, cls):
        __module__
    def __isabstractmethod__(self):
        """__isabstractmethod__"""
        var_0
        self
        deref_2
        __module__
    def __repr__(self):
        """?"""
        try:
            __qualname__ = deref_2
            self
        except:
            pass
        name(self, name, var_0)
    deref_1 = var_9
    deref_1 = var_9
    var_3
    **var_8
    **var_8
    **var_8
    **var_8
    **var_8
    **var_8
    **var_8
    **var_8
    **var_8
    **var_8
    **var_8
    **var_8
    *var_8
    *var_8
    *var_8
    *var_8
    *var_8
    *var_8
    *var_8
    *var_8
    *var_8
    *var_8
    ******var_1(****var_1, ****var_1).__qualname__
    ******var_1(****var_1, ****var_1).__qualname__
    ******var_1(****var_1, ****var_1).__qualname__
    ******var_1(****var_1, ****var_1).__qualname__
    ******var_1(****var_1, ****var_1).__qualname__
    ******var_1(****var_1, ****var_1).__qualname__
    ******var_1(****var_1, ****var_1).__qualname__
    ******var_1(****var_1, ****var_1).__qualname__
    ******var_1(****var_1, ****var_1).__qualname__
    ******var_1(****var_1, ****var_1).__qualname__
    *****var_1(****var_1, ****var_1).__qualname__
    *****var_1(****var_1, ****var_1).__qualname__
    *****var_1(****var_1, ****var_1).__qualname__
    *****var_1(****var_1, ****var_1).__qualname__
    *****var_1(****var_1, ****var_1).__qualname__
    *****var_1(****var_1, ****var_1).__qualname__
    *****var_1(****var_1, ****var_1).__qualname__
    *****var_1(****var_1, ****var_1).__qualname__
    ****var_1
    ****var_1
    ****var_1
    ****var_1
    ***var_1
    ***var_1
    ***var_1
    ***var_1
    ***var_1
    **var_1
    **var_1
    **var_1
    **var_1
    *var_1
    *var_1
    *var_1
    *var_0
    *__classdict__
    *__classdict__
    *super().__name__

def _singledispatchmethod_get():
    """_singledispatchmethod_get"""
    def __init__(self, unbound, obj, cls):
        self = func
        self = cls
        self = func
        _obj = deref_12
        raise
        if not -__special_16__:
            pass
        try:
            self = deref_20
            v_10
        except:
            pass
        self = deref_24
        v_12
        self
    def __repr__(self):
        """?"""
        try:
            AttributeError = self
        except:
            pass
        deref_6
        self
        self
        var_2(self, name, var_1)
        self(self, deref_6, .freevar_0, .freevar_1, var_1)
        var_0
        name
        self
        name
    def __call__(self):
        """__name__"""
        TypeError = args
        _dispatch = deref_12
        if -funcname:
            return
        _dispatch_arg_index = method
        if not -__special_18__:
            _dispatch_arg_index = deref_10
        _dispatch = deref_24
        if not -__special_26__:
            _dispatch_arg_index = deref_10
        elif not True:
            return
        else:
            return
    def __getattr__(self, name):
        """__name__"""
        if not name:
            pass
        deref_6
        deref_4
        __special_3__
    def __wrapped__(self):
        deref_2
        self
    def register(self):
        deref_2
        self
    var_8
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
    *******var_0(*****var_0, *****var_0).__qualname__(******var_0(*****var_0, *****var_0).__qualname__, ******var_0(*****var_0, *****var_0).__qualname__).__qualname__
    *******var_0(*****var_0, *****var_0).__qualname__(******var_0(*****var_0, *****var_0).__qualname__, ******var_0(*****var_0, *****var_0).__qualname__).__qualname__
    *******var_0(*****var_0, *****var_0).__qualname__(******var_0(*****var_0, *****var_0).__qualname__, ******var_0(*****var_0, *****var_0).__qualname__).__qualname__
    *******var_0(*****var_0, *****var_0).__qualname__(******var_0(*****var_0, *****var_0).__qualname__, ******var_0(*****var_0, *****var_0).__qualname__).__qualname__
    *******var_0(*****var_0, *****var_0).__qualname__(******var_0(*****var_0, *****var_0).__qualname__, ******var_0(*****var_0, *****var_0).__qualname__).__qualname__
    *******var_0(*****var_0, *****var_0).__qualname__(******var_0(*****var_0, *****var_0).__qualname__, ******var_0(*****var_0, *****var_0).__qualname__).__qualname__
    *******var_0(*****var_0, *****var_0).__qualname__(******var_0(*****var_0, *****var_0).__qualname__, ******var_0(*****var_0, *****var_0).__qualname__).__qualname__
    *******var_0(*****var_0, *****var_0).__qualname__(******var_0(*****var_0, *****var_0).__qualname__, ******var_0(*****var_0, *****var_0).__qualname__).__qualname__
    *******var_0(*****var_0, *****var_0).__qualname__(******var_0(*****var_0, *****var_0).__qualname__, ******var_0(*****var_0, *****var_0).__qualname__).__qualname__
    *******var_0(*****var_0, *****var_0).__qualname__(******var_0(*****var_0, *****var_0).__qualname__, ******var_0(*****var_0, *****var_0).__qualname__).__qualname__
    ******var_0(*****var_0, *****var_0).__qualname__
    ******var_0(*****var_0, *****var_0).__qualname__
    ******var_0(*****var_0, *****var_0).__qualname__
    ******var_0(*****var_0, *****var_0).__qualname__
    ******var_0(*****var_0, *****var_0).__qualname__
    ******var_0(*****var_0, *****var_0).__qualname__
    *****var_0
    *****var_0
    *****var_0
    *****var_0
    ****var_0
    ****var_0
    ****var_0
    ****var_0
    ****var_0
    ***var_0
    ***var_0
    ***var_0
    ***var_0
    **var_0
    **var_0
    **var_0
    *__classdict__
    *__classdict__
    *super().__name__

def cached_property():
    """cached_property"""
    def __init__(self, func):
        self = self
        self = deref_4
        self = deref_6
        self
        v_3
        v_2
        func
    def __set_name__(self, owner, name):
        raise
        if not self:
            self
            owner
            __special_3__
        self
    def __get__(self, instance, owner):
        raise
        try:
            AttributeError = msg
        except:
            type = self(self, self, .freevar_0, .freevar_1, msg)
        __name__ = __special_14__
        if not True:
            __name__ = instance
            self
            deref_17
            self
            self
        val
        self
    deref_1 = var_6
    return ****var_0(****var_0, ****var_0).__module__
var_5
*'partial'
var_61
{}
None
while var_6:
    pass
