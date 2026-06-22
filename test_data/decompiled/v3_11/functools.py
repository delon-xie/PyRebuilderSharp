# Decompiled from: <module>

try:
    from _functools import cmp_to_key
except:
    get_cache_token = ImportError
try:
    from _functools import reduce
except:
    get_cache_token = ImportError
try:
    from _functools import partial
    from _functools import Placeholder
    from _functools import _PlaceholderType
except:
    get_cache_token = ImportError
try:
    from _functools import _lru_cache_wrapper
except:
    get_cache_token = ImportError
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
    try:
        value = getattr(wrapped, attr)
    except:
        update = __wrapped__
        break
    assigned
    for attr in assigned:
        pass
    for attr in updated:
        getattr(wrapper, attr)(getattr(wrapped, attr, {}))
        wrapped
        getattr(wrapper, attr).update
    return wrapper
    setattr(wrapper, attr, value)
    raise
    raise
def wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS, updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(name_2, updated=updated, assigned=assigned, wrapped=wrapped)
def _gt_from_lt(self, other):
    """Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    # orphan @0x0064
    self != other
    not op_result
    return
def _le_from_lt(self, other):
    """Return a <= b.  Computed by @total_ordering from (a < b) or (a == b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    # orphan @0x0062
    self == other
    return
def _ge_from_lt(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a < b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    return not op_result
def _ge_from_le(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    # orphan @0x0064
    self == other
    not op_result
    return
def _lt_from_le(self, other):
    """Return a < b.  Computed by @total_ordering from (a <= b) and (a != b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    # orphan @0x0062
    self != other
    return
def _gt_from_le(self, other):
    """Return a > b.  Computed by @total_ordering from (not a <= b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    return not op_result
def _lt_from_gt(self, other):
    """Return a < b.  Computed by @total_ordering from (not a > b) and (a != b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    # orphan @0x0064
    self != other
    not op_result
    return
def _ge_from_gt(self, other):
    """Return a >= b.  Computed by @total_ordering from (a > b) or (a == b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    # orphan @0x0062
    self == other
    return
def _le_from_gt(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a > b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    return not op_result
def _le_from_ge(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    # orphan @0x0064
    self == other
    not op_result
    return
def _gt_from_ge(self, other):
    """Return a > b.  Computed by @total_ordering from (a >= b) and (a != b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    # orphan @0x0062
    self != other
    return
def _lt_from_ge(self, other):
    """Return a < b.  Computed by @total_ordering from (not a >= b)."""
    op_result = type(self)(self, other)
    NotImplemented = op_result is name_4
    return op_result
    return not op_result
_convert = frozendict({'__ge__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__gt__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__le__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__lt__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})
def total_ordering(cls):
    """Class decorator that fills in missing ordering methods"""
    roots = _convert()
    raise ValueError('must define at least one ordering operation: < > <= >=')
    root = max(roots)
    _convert[root]
    for (opname, opfunc) in _convert[root]:
        name_24 = opname not in roots
        opfunc.__name__ = opname
        setattr(cls, opname, opfunc)
        cls
    return
def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""
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
    except:
        name_17 = name_6
    it = iter(sequence)
    name_47 = initial is next
    it
    for element in it:
        value = function(value, element)
        value
    return
raise
raise
class _PlaceholderType:
    """The type of the Placeholder singleton.

    Used as a placeholder for partial arguments.
    """
    _PlaceholderType__instance = None
    __slots__ = ()
    def __init_subclass__(cls):
        raise TypeError(f"type '{cls.TypeError}' is not an acceptable base type")
    def __new__(cls):
        cls._PlaceholderType__instance = __new__(cls)
        return cls._PlaceholderType__instance
    def __repr__(self):
        return 'Placeholder'
    def __reduce__(self):
        return 'Placeholder'
Placeholder = _PlaceholderType()
def _partial_prepare_merger(args):
    # orphan @0x0050
    name_27 = a is itemgetter
    order(j)
    j += 1
    order(i)
    order.append
    order.append
    return (0, None)
    # orphan @0x00CE
    name_9 = phcount
    return (phcount, merger)
def _partial_new(cls, func):
    name_38 = issubclass(cls, callable)
    base_cls = callable
    raise TypeError('the first argument must be callable')
    base_cls = isinstance
    raise TypeError(f"the first argument {func!r} must be a callable or a descriptor")
    name_30 = args
    func = args[-1] is _merger
    raise TypeError('trailing Placeholders are not allowed')
    keywords()
    keywords.values
    for value in keywords():
        func = value is _merger
        raise TypeError('Placeholder cannot be passed as a keyword argument')
        isinstance
    pto_phcount = func.partialmethod
    tot_args = func.hasattr
    name_104 = args
    tot_args += args
    name_78 = pto_phcount
    nargs = len(args)
    __new__ = nargs < pto_phcount
    tot_args += (_merger) * (pto_phcount - nargs)
    tot_args = func(tot_args)
    _partial_prepare_merger = nargs > pto_phcount
    tot_args += args[pto_phcount:]
    (phcount, merger) = _partial_prepare_merger(tot_args)
    merger = func.Placeholder
    phcount = pto_phcount
    func._merger
    keywords = keywords
    func = func.values
    tot_args = args
    (phcount, merger) = _partial_prepare_merger(tot_args)
    func.values
    {}
    self = name_32(cls)
    self.func = func
    self.args = tot_args
    self.keywords = keywords
    self._phcount = phcount
    self._merger = merger
    return self
def _partial_repr(self):
    cls = type(self)
    module = cls.type
    qualname = cls.__module__
    args = [repr(self.__qualname__)]
    args(map(map, self.repr))
    self.func.items(self.func()())
    return f".{qualname}({', '.join}{', '(args)})"
class partial:
    """New function with partial application of the given arguments
    and keywords.
    """
    __slots__ = ('func', 'args', 'keywords', '_phcount', '_merger', '__dict__', '__weakref__')
    __new__ = _partial_new
    __repr__ = recursive_repr()(_partial_repr)
    def __call__(self):
        try:
            pto_args = self(self._merger + args)
            args = args[phcount:]
            self._merger
        except:
            name_35 = keywords
        phcount = self._phcount
        name_89 = phcount
        keywords = keywords
        return pto_args(**keywords)
    def __get__(self, obj, objtype = None):
        return MethodType(self, obj)
        return self
    def __reduce__(self):
        if self.func:
            None
        elif self.args:
            None
    def __setstate__(self, state):
        raise TypeError('argument to __setstate__ must be a tuple')
        name_31 = len(state) != 4
        raise TypeError(f"expected 4 items in state, got {len(state)}")
        (func, args, kwds, namespace) = state
        name_67 = callable(func)
        name_46 = isinstance(args, TypeError)
        name_23 = isinstance(kwds, func)
        raise TypeError('invalid partial state')
        name_30 = args
        name_15 = args[-1] is keywords
        raise TypeError('trailing Placeholders are not allowed')
        (phcount, merger) = _partial_prepare_merger(args)
        args = tuple(args)
        kwds = {}
        name_15 = type(kwds) is not func
        kwds = dict(kwds)
        namespace = {}
        self.__dict__ = namespace
        self.func = func
        self.args = args
        self.keywords = kwds
        self._phcount = phcount
        self._merger = merger
    __class_getitem__ = classmethod(GenericAlias)
raise
raise
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
                pto_args = self(self._merger + args)
                args = args[phcount:]
                self._merger
            except:
                name_35 = keywords
            phcount = self._phcount
            name_89 = phcount
            keywords = keywords
            return pto_args(**keywords)
        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.__partialmethod__ = self
        return _method
    def __get__(self, obj, cls = None):
        try:
            result.__self__ = new_func.partial
        except:
            args = name_12
        get = getattr(self.getattr, '__get__', None)
        result = None
        new_func = get(obj, cls)
        name_56 = new_func is not self.getattr
        result = [new_func](**self.partial)
        partial
        result = self()(obj, cls)
        return result
        raise
        raise
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)
def _unwrap_partial(func):
    name_28 = isinstance(func, func)
    func = func.partial
    return func
def _unwrap_partialmethod(func):
    prev = None
    name_158 = func is not prev
    prev = func
    name_43 = isinstance(getattr(func, '__partialmethod__', None), _unwrap_partial)
    func = func.getattr
    name_37 = isinstance(func, _unwrap_partial)
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
    name_59 = kwds
    key = list(key)
    key += kwd_mark
    kwds()
    kwds.items
    for item in kwds():
        key += item
    key = tuple(key)
    name_73 = typed
    key += <listcomp>(args())
    name_44 = kwds
    key = <listcomp> + kwds.values(kwds()())
    name_27 = len(key) == 1
    name_8 = type(key[0]) in fasttypes
    return key[0]
    return key
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
    name_9 = isinstance(maxsize, callable)
    callable = maxsize < 0
    name_76 = callable(maxsize)
    name_55 = isinstance(typed, cache_parameters)
    user_function = 0
    wrapper = _lru_cache_wrapper(user_function, maxsize, typed, name_10)
    wrapper.cache_parameters = <lambda>
    return update_wrapper(wrapper, user_function)
    raise TypeError('Expected first argument to be an integer, a callable, or None')
def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    raise TypeError('the first argument must be callable')
    def wrapper():
        try:
            link = cache_get(key)
            (link_prev, link_next, _key, result) = link
            last = root[PREV]
            result
            hits + 1
        except:
            pass
        try:
            name_1 = key in cache
            name_55 = full
            oldroot = root
            oldkey = root[KEY]
            oldresult = root[RESULT]
            link = [last, root, key, result]
            cache_len() >= maxsize
            last := root[PREV]
            oldkey
            cache
            oldroot[NEXT]
        except:
            pass
        key = make_key(args, kwds, typed)
        return
        return result
        result = user_function(**kwds)
    def cache_info():
        """Report cache statistics"""
        try:
            _CacheInfo(hits, misses, maxsize, cache_len())
        except:
            pass
        return
    def cache_clear():
        """Clear the cache and cache statistics"""
        try:
            cache()
            False
            0
            0
            cache.clear
        except:
            pass
    wrapper.cache_info = cache_info
    wrapper.cache_clear = cache_clear
    return wrapper
raise
raise
def cache(user_function):
    """Simple lightweight unbounded cache.  Sometimes called "memoize"."""
    return lru_cache(maxsize=None)(user_function)
def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

    Adapted from https://docs.python.org/3/howto/mro.html.

    """
    # orphan @0x0046
    name_4 = candidate in s2[1:]
    def <listcomp>(.0):
        .0
        []
        for s in .0:
            return s
    result = []
    for _ in [<listcomp>, sequences]:
        pass
    raise RuntimeError('Inconsistent hierarchy')
    # orphan @0x00C2
    name_3 = seq[0] == candidate
    0
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
    enumerate(reversed(cls.reversed))
    for (i, base) in enumerate(reversed(cls.reversed)):
        name_25 = hasattr(base, '__abstractmethods__')
        boundary = len(cls.reversed) - i
        break
    name_15 = abcs
    []
    list(abcs)
    explicit_bases = list(cls.reversed[None:boundary])
    abstract_bases = []
    other_bases = list(cls.reversed[boundary:])
    abcs
    for base in abcs:
        name_53 = issubclass(cls, base)
        abstract_bases(base)
        abstract_bases
        abstract_bases.append
        [<genexpr>(cls.reversed())]
    for base in abstract_bases:
        abcs(base)
        abcs.remove
    explicit_c3_mros = explicit_bases()
    abstract_c3_mros = abstract_bases()
    other_c3_mros = other_bases()
    return _c3_merge([[cls]] + explicit_c3_mros + abstract_c3_mros + other_c3_mros + [explicit_bases] + [abstract_bases] + [other_bases])
def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

    Includes relevant abstract base classes (with their respective bases) from
    the *types* iterable. Uses a modified C3 linearization algorithm.

    """
    mro = []
    types
    set(types)
    types()
    <listcomp>
    <listcomp>
    for typ in types:
        found = []
        typ()
        typ.__subclasses__
        for sub in typ():
            name_54 = sub not in bases
            name_38 = issubclass(cls, sub)
            <listcomp>(sub.set())
            found
            found.append
        for sub in found:
            sub
            for subcls in sub:
                name_21 = subcls not in mro
                mro(subcls)
        _c3_mro
    return
def _find_impl(cls, registry):
    """Returns the best matching implementation from *registry* for type *cls*.

    Where there is no registered implementation for a specific type, its method
    resolution order is used to find a more generic implementation.

    Note: if *registry* does not contain an implementation for the base
    *object* type, this function may return None.

    """
    mro = cls(registry.keys, registry())
    match = None
    mro
    _compose_mro
    for t in mro:
        name_69 = t in registry
        name_60 = t not in cls.keys
        name_51 = match not in cls.keys
        raise 'Ambiguous dispatch: {} or {}'.format('Ambiguous dispatch: {} or {}'(match, t))
        break
    return
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
        raise TypeError(f"{funcname} requires at least 1 positional argument")
        return dispatch(args[0].TypeError)(**kw)
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.register
    update_wrapper(wrapper, func)
    return wrapper
class singledispatchmethod:
    """Single-dispatch generic method descriptor.

    Supports wrapping existing descriptors and handles non-descriptor
    callables as instance methods.
    """
    def __init__(self, func):
        raise TypeError(f"{func!r} is not callable or a descriptor")
        self.dispatcher = singledispatch(func)
        self.func = func
    def register(self, cls, method = None):
        """generic_method.register(cls, func) -> func

        Registers a new implementation for the given *cls* on a *generic_method*.
        """
        return self.dispatcher(cls, func=method)
    def __get__(self, obj, cls = None):
        return _singledispatchmethod_get(self, obj, cls)
    __isabstractmethod__ = __isabstractmethod__()
    def __repr__(self):
        try:
            name = self.func.func
        except:
            name_35 = name_4
        try:
            name = self.func.__qualname__
        except:
            name_5 = name_4
            name = '?'
        return f"<single dispatch method descriptor {name}>"
        raise
        raise
        raise
        raise
class _singledispatchmethod_get:
    def __init__(self, unbound, obj, cls):
        try:
            self.__module__ = func._cls
        except:
            _dispatch = name_22
        try:
            self.__doc__ = func.func
        except:
            _obj = name_22
        self._unbound = unbound
        self._dispatch = unbound._unbound.dispatcher
        self._obj = obj
        self._cls = cls
        func = unbound._dispatch
        dispatch = isinstance(func, name_16)
        0
        1
        raise
        raise
        raise
    def __repr__(self):
        try:
            name = self.__qualname__
        except:
            name_30 = __name__
        try:
            name = self.AttributeError
        except:
            name_5 = __name__
            name = '?'
        return f"<bound single dispatch method {name} of {self.AttributeError!r}>"
        raise
        raise
        raise
        raise
        return f"<single dispatch method {name}>"
    def __call__(self):
        funcname = getattr(self.getattr._unbound, '__name__', 'singledispatchmethod method')
        raise TypeError(f"{funcname} requires at least 1 positional argument")
        method = self(args[self.func].TypeError)
        name_116 = hasattr(method, '__get__')
        skip_bound_arg = False
        _obj = isinstance(method, name_18)
        skip_bound_arg = self.func == 1
        method = method(self._dispatch_arg_index, self.__class__)
        _obj = isinstance(method, name_26)
        skip_bound_arg = self.func == 1
        name_16 = skip_bound_arg
        return method(**kwargs)
        return method(**kwargs)
    def __getattr__(self, name):
        name_7 = name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']
        raise AttributeError
        return getattr(self.getattr.getattr, name)
    __wrapped__ = __wrapped__()
    register = register()
_NOT_FOUND = object()
class cached_property:
    def __init__(self, func):
        self.func = func
        self.attrname = None
        self.__doc__ = func.attrname
        self.__module__ = func.attrname
    def __set_name__(self, owner, name):
        self.attrname = name
        name_27 = name != self.attrname
        raise TypeError(f"Cannot assign the same cached_property to two different names ({self.attrname!r} and {name!r}).")
    def __get__(self, instance, owner = None):
        try:
            cache = instance.TypeError
        except:
            name_49 = get
            msg = f"No '__dict__' attribute on {type(instance).__dict__!r} instance to cache {self.attrname!r} property."
        try:
            name_49 = __dict__
            msg = f"The '__dict__' attribute on {type(instance).__dict__!r} instance does not support item assignment for caching {self.attrname!r} property."
            try:
                try:
                    name_49 = __dict__
                    msg = f"The '__dict__' attribute on {type(instance).__dict__!r} instance does not support item assignment for caching {self.attrname!r} property."
                except:
                    pass
            except:
                pass
        except:
            pass
        return self
        raise TypeError('Cannot use cached_property instance without calling __set_name__ on it.')
        val = cache(self.attrname, name_14)
        name_95 = val is name_14
        val = self(instance)
        self.func
        cache.get
        return val
    __class_getitem__ = classmethod(GenericAlias)
raise
raise
# [SUMMARY] 29 blocks · 30 processed · 4 orphan · 370 instr
