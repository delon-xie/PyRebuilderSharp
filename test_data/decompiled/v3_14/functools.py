# Decompiled from: <module>

def _lt_from_le(self, other):
    """Return a < b.  Computed by @total_ordering from (a <= b) and (a != b)."""
    op_result = self.__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif op_result:
        return self != other

def _gt_from_le(self, other):
    """Return a > b.  Computed by @total_ordering from (not a <= b)."""
    op_result = self.__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    else:
        return not op_result

def _lt_from_gt(self, other):
    """Return a < b.  Computed by @total_ordering from (not a > b) and (a != b)."""
    op_result = self.__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif not op_result:
        return self != other

def _ge_from_gt(self, other):
    """Return a >= b.  Computed by @total_ordering from (a > b) or (a == b)."""
    op_result = self.__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif not op_result:
        return self == other

def _le_from_gt(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a > b)."""
    op_result = self.__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    else:
        return not op_result

def _le_from_ge(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b)."""
    op_result = self.__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif not not op_result:
        return self == other

def _gt_from_ge(self, other):
    """Return a > b.  Computed by @total_ordering from (a >= b) and (a != b)."""
    op_result = self.__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif op_result:
        return self != other

def _lt_from_ge(self, other):
    """Return a < b.  Computed by @total_ordering from (not a >= b)."""
    op_result = self.__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    else:
        return not op_result

def total_ordering(cls):
    """Class decorator that fills in missing ordering methods"""
    {}
    op
    if not roots:
        ValueError
    None
    op
    cls
    getattr
    raise 'must define at least one ordering operation: < > <= >='
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
    def K():
        """cmp_to_key.<locals>.K"""
        __module__ = mycmp
        __qualname__ = 'cmp_to_key.<locals>.K'
        __firstlineno__ = 208
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
        __static_attributes__ = ['obj']
        __classdictcell__ = __classdict__
    K = K('K', object)
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
    it = sequence
    try:
        initial
    finally:
        value = it
    try:
        initial
    finally:
        value = it
    for element in it:
        value = function(value, element)
    for element in it:
        value = function(value, element)

def _PlaceholderType():
    """_PlaceholderType"""
    __qualname__ = '_PlaceholderType'
    __firstlineno__ = 278
    __doc__ = """The type of the Placeholder singleton.

Used as a placeholder for partial arguments.
"""
    _PlaceholderType__instance = None
    __slots__ = []
    def __init_subclass__(cls):
        """type '"""
        raise f"type '{cls.__name__}' is not an acceptable base type"
    def __new__(cls):
        cls._PlaceholderType__instance = object.__new__(cls)
        return cls._PlaceholderType__instance
        # [WARN] 1 instructions not decompiled
        #   @0x001A: POP_JUMP_IF_NOT_NONE arg=82
    def __repr__(self):
        """Placeholder"""
        return
    def __reduce__(self):
        """Placeholder"""
        return
    __static_attributes__ = []
    __classdictcell__ = __classdict__

def _partial_prepare_merger(args):
    if not True:
        return (0, None)
    # [Block @0x004A] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
    # [Block @0x00C6] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
    phcount = j - nargs

def _partial_new(cls, func):
    """the first argument must be callable"""
    if cls(partial):
        base_cls = partial
        if not callable(func):
            raise TypeError('the first argument must be callable')
        if args and (args[-1] is Placeholder):
            raise TypeError('trailing Placeholders are not allowed')
        else:
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
    cls = self
    module = cls.__module__
    qualname = cls.__qualname__
    args = [repr(self.func)]
    args.extend(map(repr, self.args))
    (k for (v, k) in iterable)
    return f"{module}.{qualname}({', '.join(args)})"

def partial():
    """partial"""
    __qualname__ = 'partial'
    __firstlineno__ = 374
    __doc__ = """New function with partial application of the given arguments
and keywords.
"""
    __slots__ = ('func', 'args', 'keywords', '_phcount', '_merger', '__dict__', '__weakref__')
    __new__ = _partial_new
    __repr__ = recursive_repr()(_partial_repr)
    def __call__(self):
        try:
            try:
                self
            finally:
                args = args[phcount:]
            keywords = keywords
            try:
                self
            finally:
                args = args[phcount:]
        finally:
            args = args[phcount:]
            self
            {}
            keywords = keywords
    def __get__(self, obj, objtype = None):
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
        if not state(tuple):
            raise TypeError('argument to __setstate__ must be a tuple')
        kwds = {}
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__dict__', '_merger', '_phcount', 'args', 'func', 'keywords')
    __classdictcell__ = __classdict__

def partialmethod():
    """partialmethod"""
    def __isabstractmethod__(self):
        """__isabstractmethod__"""
        return self.func('__isabstractmethod__', False)
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
            self
            try:
                try:
                    self
                finally:
                    args = args[phcount:]
                keywords = keywords
                try:
                    self
                finally:
                    args = args[phcount:]
            finally:
                args = args[phcount:]
                self
                {}
                keywords = keywords
        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.__partialmethod__ = self
        return _method
    def __get__(self, obj, cls = None):
        """__get__"""
        get = self.func('__get__', None)
        result = None
        if get:
            new_func = get(obj, cls)
            self
            new_func
        elif result:
            result = self._make_unbound_method().__get__(obj, cls)
        # [WARN] 2 instructions not decompiled
        #   @0x0038: POP_JUMP_IF_NONE arg=212
        #   @0x00D8: POP_JUMP_IF_NOT_NONE arg=282
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = []
    __classdictcell__ = __classdict__

def _unwrap_partial(func):
    pass

def _unwrap_partialmethod(func):
    while func is not prev:
        prev = func
        while isinstance(getattr(func, '__partialmethod__', None), partialmethod):
            func = func.__partialmethod__
        while isinstance(func, partialmethod):
            func = getattr(func, 'func')
        func = _unwrap_partial(func)
    return func

def _make_key(args, kwds, typed, kwd_mark, fasttypes, tuple, type, len):
    """Make a cache key from optionally typed positional and keyword arguments

    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.

    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.

"""
    if kwds:
        key = list(key)
        key += kwd_mark
        kwds.items
    typed
    try:
        v_133
        args
        kwds.values()
        v
        v_133
        []
        args
    finally:
        kwds.values()
        v
        v_133
        []
        args
    return key
    if (len(key) == 1) and (type(key[0]) in fasttypes):
        return key[0]
    else:
        return key
    return key
    for item in kwds.items:
        item
        key
    for item in kwds.items:
        item
        key
    v = [type(v) for v in kwds.values()]
    v = [type(v) for v in kwds.values()]

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
    if maxsize(int):
        if maxsize < 0:
            maxsize = 0
        def decorating_function(user_function):
            wrapper = typed(user_function, maxsize, typed, _CacheInfo)
            wrapper.cache_parameters = lambda : {typed: maxsize, 'typed': typed}
            return update_wrapper(wrapper, user_function)
        return decorating_function
    elif callable(maxsize) and isinstance(typed, bool):
        user_function = 128
        maxsize = maxsize
        wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)
        wrapper.cache_parameters = lambda : {typed: maxsize, 'typed': typed}
        return update_wrapper(wrapper, user_function)
    # [WARN] 1 instructions not decompiled
    #   @0x00F4: POP_JUMP_IF_NONE arg=270

def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    """the first argument must be callable"""
    def cache_info():
        """Report cache statistics"""
        _CacheInfo
        cache_len
        hits
        lock
        maxsize
        misses
        __module__
        misses
        __name__()
        _CacheInfo
        return
    def cache_clear():
        """Clear the cache and cache statistics"""
        cache
        full
        hits
        lock
        misses
        root
        __module__
        root
        try:
            __name__()
            cache
        finally:
            None
            None
            root
            root
        PySliceData { Start = , Stop = , Step =  }
        root
        []
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
    if not user_function:
        raise TypeError('the first argument must be callable')
    def wrapper():
        key = user_function(args, kwds, typed)
        result = cache_get(key, sentinel)
        if result is not sentinel:
            hits += 1
            return result
        misses += 1
        result = None(**args, **kwds)
        return result

def cache(user_function):
    """Simple lightweight unbounded cache.  Sometimes called "memoize"."""
    return user_function()

def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

    Adapted from https://docs.python.org/3/howto/mro.html.

"""
    []
    s
    sequences
    candidate = None
    for s1 in sequences:
        candidate = s1[0]
        sequences
        if not candidate in s2[1:]:
            pass
        else:
            candidate = None
        if candidate:
            raise RuntimeError('Inconsistent hierarchy')
        else:
            result.append(candidate)
            sequences
        raise
        if not seq[0] == candidate:
            pass
    for seq in sequences:
        if not seq[0] == candidate:
            pass
    for seq in sequences:
        if not seq[0] == candidate:
            pass

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
    reversed(cls.__bases__)
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
        explicit_bases
        []
        base
        abstract_bases
        []
        base
        other_bases
        []
        base
        return _c3_merge([[cls]] + explicit_c3_mros + abstract_c3_mros + other_c3_mros + [explicit_bases] + [abstract_bases] + [other_bases])
        abcs.remove(base)
        issubclass
        base
        cls
        if not True:
            pass
    if not hasattr(base, '__abstractmethods__'):
        pass
    else:
        boundary = len(cls.__bases__) - i

def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

    Includes relevant abstract base classes (with their respective bases) from
    the *types* iterable. Uses a modified C3 linearization algorithm.

"""
    def is_related(typ):
        """__mro__"""
        if (cls not in bases) and hasattr(typ, '__mro__'):
            if not isinstance(typ, GenericAlias):
                issubclass(cls, typ)
            return
        else:
            return
        return
    def is_strict_base(typ):
        types
        if not typ != other:
            pass
        elif not typ in other.__mro__:
            pass
        else:
            return True
        for _ in iterable:
            return False
    cls
    cls
    found
    n = [typ for typ in types for sub in set for s in sub for sub in set for subcls in set]

def _find_impl(cls, registry):
    """Returns the best matching implementation from *registry* for type *cls*.

    Where there is no registered implementation for a specific type, its method
    resolution order is used to find a more generic implementation.

    Note: if *registry* does not contain an implementation for the base
    *object* type, this function may return None.

"""
    mro = cls(registry.keys())
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
        if registry:
            current_token = get_cache_token()
            cache_token != current_token
        cache_token = current_token
        impl = registry[cls]
        cls
        dispatch_cache
        impl = _find_impl(cls, registry)
        # [WARN] 1 instructions not decompiled
        #   @0x0008: POP_JUMP_IF_NONE arg=82
    def _is_valid_dispatch_type(cls):
        if cls(type):
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
        if registry(cls):
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
        if not funcname:
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        return None(**args, **kw)
    funcname = getattr(func, '__name__', 'singledispatch function')
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.clear
    update_wrapper(wrapper, func)
    return wrapper

def singledispatchmethod():
    """singledispatchmethod"""
    def __isabstractmethod__(self):
        """__isabstractmethod__"""
        return self.func('__isabstractmethod__', False)
    __qualname__ = 'singledispatchmethod'
    __firstlineno__ = 1021
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
        return cls
    def __get__(self, obj, cls = None):
        return self(obj, cls)
    __isabstractmethod__ = __isabstractmethod__()
    def __repr__(self):
        """?"""
        pass
    __static_attributes__ = ('dispatcher', 'func')
    __classdictcell__ = __classdict__

def _singledispatchmethod_get():
    """_singledispatchmethod_get"""
    def __wrapped__(self):
        return
    def register(self):
        return
    __qualname__ = '_singledispatchmethod_get'
    __firstlineno__ = 1059
    def __init__(self, unbound, obj, cls):
        self._dispatch = unbound.dispatcher.dispatch
        self._obj = obj
        self._cls = cls
        unbound
    def __repr__(self):
        """?"""
        pass
    def __call__(self):
        """__name__"""
        if not True:
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
        raise AttributeError
    __wrapped__ = __wrapped__()
    register = register()
    __static_attributes__ = ('__doc__', '__module__', '_cls', '_dispatch', '_dispatch_arg_index', '_obj', '_unbound')
    __classdictcell__ = __classdict__

def cached_property():
    """cached_property"""
    __qualname__ = 'cached_property'
    __firstlineno__ = 1142
    def __init__(self, func):
        self.attrname = None
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__
    def __set_name__(self, owner, name):
        self.attrname = name
        # [WARN] 1 instructions not decompiled
        #   @0x001A: POP_JUMP_IF_NOT_NONE arg=46
    def __get__(self, instance, owner = None):
        val = _NOT_FOUND
        return self
        # [WARN] 2 instructions not decompiled
        #   @0x0006: POP_JUMP_IF_NOT_NONE arg=14
        #   @0x0026: POP_JUMP_IF_NOT_NONE arg=64
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__doc__', '__module__', 'attrname', 'func')
    __classdictcell__ = __classdict__
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
    for attr in iterable:
        value = getattr(wrapped, attr)
        setattr(wrapper, attr, value)
    for attr in iterable:
        value = getattr(wrapped, attr)
        setattr(wrapper, attr, value)
    for attr in updated:
        getattr
        try:
            wrapper(attr)
        finally:
            getattr(wrapped, attr, {})
        wrapper.__wrapped__ = wrapped
        return wrapper
    for attr in updated:
        getattr
        try:
            wrapper(attr)
        finally:
            getattr(wrapped, attr, {})
        wrapper.__wrapped__ = wrapped
        return wrapper

def wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS, updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

    Returns a decorator that invokes update_wrapper() with the decorated
    function as the wrapper argument and the arguments to wraps() as the
    remaining arguments. Default arguments are as for update_wrapper().
    This is a convenience function to simplify applying partial() to
    update_wrapper().
"""
    return update_wrapper

def _gt_from_lt(self, other):
    """Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""
    op_result = self.__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and (self != other)

def _le_from_lt(self, other):
    """Return a <= b.  Computed by @total_ordering from (a < b) or (a == b)."""
    op_result = self.__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and (self == other)

def _ge_from_lt(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a < b)."""
    op_result = self.__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result

def _ge_from_le(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b)."""
    op_result = self.__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not not op_result and (self == other)
CodeObject: _lt_from_le (21 instrs)
try:
    _lt_from_le = lambda : None
    CodeObject: _gt_from_le (17 instrs)
finally:
    CodeObject: reduce (44 instrs)
    (_initial_missing)
lambda : None
