# Decompiled from: <module>

try:
    from _functools import cmp_to_key
except ImportError:
    pass
try:
    from _functools import reduce
except ImportError:
    pass
try:
    from _functools import partial
    from _functools import Placeholder
    from _functools import _PlaceholderType
except ImportError:
    pass
try:
    from _functools import _lru_cache_wrapper
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
    try:
        value = getattr(wrapped, attr)
    except:
        break
    assigned
    for attr in assigned:
        pass
    updated
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    wrapper.__wrapped__ = wrapped
    return wrapper
    setattr(wrapper, attr, value)
    # orphan @0x00C6
    # orphan @0x00C8
    # [WARN] 3 instructions not decompiled
    #   @0x0040: JUMP_BACKWARD arg=60
    #   @0x009A: JUMP_BACKWARD arg=84
    #   @0x00C4: JUMP_BACKWARD arg=192
def wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS, updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(name_2, wrapped, assigned, updated)
def _gt_from_lt(self, other):
    """Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""
    op_result = type(self).__lt__(self, other)
    if op_result is name_4:
        return op_result
    elif not op_result:
        self != other
def _le_from_lt(self, other):
    """Return a <= b.  Computed by @total_ordering from (a < b) or (a == b)."""
    op_result = type(self).__lt__(self, other)
    if op_result is name_4:
        return op_result
    elif not op_result:
        self == other
def _ge_from_lt(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a < b)."""
    op_result = type(self).__lt__(self, other)
    if op_result is name_4:
        return op_result
    return not op_result
def _ge_from_le(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b)."""
    op_result = type(self).__le__(self, other)
    if op_result is name_4:
        return op_result
    elif not not op_result:
        self == other
def _lt_from_le(self, other):
    """Return a < b.  Computed by @total_ordering from (a <= b) and (a != b)."""
    op_result = type(self).__le__(self, other)
    if op_result is name_4:
        return op_result
    elif op_result:
        self != other
def _gt_from_le(self, other):
    """Return a > b.  Computed by @total_ordering from (not a <= b)."""
    op_result = type(self).__le__(self, other)
    if op_result is name_4:
        return op_result
    return not op_result
def _lt_from_gt(self, other):
    """Return a < b.  Computed by @total_ordering from (not a > b) and (a != b)."""
    op_result = type(self).__gt__(self, other)
    if op_result is name_4:
        return op_result
    elif not op_result:
        self != other
def _ge_from_gt(self, other):
    """Return a >= b.  Computed by @total_ordering from (a > b) or (a == b)."""
    op_result = type(self).__gt__(self, other)
    if op_result is name_4:
        return op_result
    elif not op_result:
        self == other
def _le_from_gt(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a > b)."""
    op_result = type(self).__gt__(self, other)
    if op_result is name_4:
        return op_result
    return not op_result
def _le_from_ge(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b)."""
    op_result = type(self).__ge__(self, other)
    if op_result is name_4:
        return op_result
    elif not not op_result:
        self == other
def _gt_from_ge(self, other):
    """Return a > b.  Computed by @total_ordering from (a >= b) and (a != b)."""
    op_result = type(self).__ge__(self, other)
    if op_result is name_4:
        return op_result
    elif op_result:
        self != other
def _lt_from_ge(self, other):
    """Return a < b.  Computed by @total_ordering from (not a >= b)."""
    op_result = type(self).__ge__(self, other)
    if op_result is name_4:
        return op_result
    return not op_result
_convert = frozendict({'__ge__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__gt__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__le__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__lt__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})
def total_ordering(cls):
    """Class decorator that fills in missing ordering methods"""
    try:
        {}
        for op in {}:
            try:
                try:
                    {}
                except:
                    break
            except:
                break
        if not roots:
            raise ValueError('must define at least one ordering operation: < > <= >=')
        root = max(roots)
        _convert[root]
        for (opname, opfunc) in _convert[root]:
            if not opname not in roots:
                pass
            else:
                opfunc.__name__ = opname
                setattr(cls, opname, opfunc)
        return cls
    except:
        break
    op
    _convert
    # [WARN] 4 instructions not decompiled
    #   @0x0058: JUMP_BACKWARD arg=68
    #   @0x005E: JUMP_BACKWARD arg=74
    #   @0x00BC: JUMP_BACKWARD arg=22
    #   @0x00E6: JUMP_BACKWARD arg=64
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
        pass
    it = iter(sequence)
    if initial is next:
        pass
    else:
        value = initial
    it
    for element in it:
        value = function(value, element)
    return value
    # orphan @0x0096
    # [WARN] 1 instructions not decompiled
    #   @0x0062: JUMP_BACKWARD arg=26
class _PlaceholderType:
    __doc__ = """The type of the Placeholder singleton.

    Used as a placeholder for partial arguments.
    """
    _PlaceholderType__instance = None
    __slots__ = ()
    def __init_subclass__(cls):
        raise TypeError(f"type '{cls.__name__}' is not an acceptable base type")
    def __new__(cls):
        cls._PlaceholderType__instance = __new__.__new__(cls)
        return cls._PlaceholderType__instance
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
    for (i, a) in enumerate(args):
        if a is itemgetter:
            order.append(j)
            j += 1
        else:
            order.append(i)
    phcount = j - nargs
    if phcount:
        pass
    else:
        None
    return (phcount, merger)
    # [WARN] 2 instructions not decompiled
    #   @0x0084: JUMP_BACKWARD arg=74
    #   @0x00A8: JUMP_BACKWARD arg=110
def _partial_new(cls, func):
    if issubclass(cls, callable):
        base_cls = callable
        if not callable(func):
            raise TypeError('the first argument must be callable')
        elif args and (args[-1] is _merger):
            raise TypeError('trailing Placeholders are not allowed')
    base_cls = isinstance
    if callable(func):
        pass
    raise TypeError(f"the first argument {func!r} must be a callable or a descriptor")
    # [WARN] 1 instructions not decompiled
    #   @0x0118: JUMP_BACKWARD arg=24
def _partial_repr(self):
    cls = type(self)
    module = cls.__module__
    qualname = cls.__qualname__
    args = [repr(self.func)]
    args.extend(map(map, self.args))
    <genexpr>(self.keywords.items()())
    return f"{module}.{qualname}({', '.join(args)})"
class partial:
    __doc__ = """New function with partial application of the given arguments
    and keywords.
    """
    __slots__ = ('func', 'args', 'keywords', '_phcount', '_merger', '__dict__', '__weakref__')
    __new__ = _partial_new
    __repr__ = recursive_repr()(_partial_repr)
    def __call__(self):
        try:
            pto_args = self._merger(self.args + args)
            args = phcount // None
            args
        except:
            pass
        phcount = self._phcount
        if phcount:
            pass
        else:
            pto_args = self.args
        keywords = keywords
        return pto_args(**keywords)
        # orphan @0x0116
    def __get__(self, obj, objtype = None):
        return self
        # orphan @0x000A
        return MethodType(self, obj)
    def __reduce__(self):
        if not self.keywords:
            None
        elif not self.__dict__:
            None
    def __setstate__(self, state):
        if not isinstance(state, TypeError):
            raise TypeError('argument to __setstate__ must be a tuple')
        elif len(state) != 4:
            raise TypeError(f"expected 4 items in state, got {len(state)}")
    __class_getitem__ = classmethod(GenericAlias)
class partialmethod:
    __doc__ = """Method descriptor with partial application of the given arguments
    and keywords.

    Supports wrapping existing descriptors and handles non-descriptor
    callables as instance methods.
    """
    __new__ = _partial_new
    __repr__ = _partial_repr
    def _make_unbound_method(self):
        def _method(cls_or_self):
            try:
                pto_args = cell_5._merger(cell_5.args + args)
                args = phcount // None
                args
            except:
                pass
            phcount = cell_5._phcount
            if phcount:
                pass
            else:
                pto_args = cell_5.args
            keywords = keywords
            return pto_args(**keywords)
            # orphan @0x011A
        _method.__isabstractmethod__ = cell_0.__isabstractmethod__
        _method.__partialmethod__ = cell_0
        return _method
    def __get__(self, obj, cls = None):
        try:
            result.__self__ = new_func.__self__
        except:
            pass
        get = getattr(self.func, '__get__', None)
        result = None
        new_func = get(obj, cls)
        if new_func is not self.func:
            result = [new_func](**self.keywords)
            partial
        result = self._make_unbound_method().__get__(obj, cls)
        return result
        # orphan @0x012E
        # orphan @0x0130
        # [WARN] 1 instructions not decompiled
        #   @0x012C: JUMP_BACKWARD arg=94
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)
def _unwrap_partial(func):
    while isinstance(func, func):
        func = func.func
    return func
    # orphan @0x0022
    func = func.func
    isinstance(func, func)
    # [WARN] 1 instructions not decompiled
    #   @0x005A: JUMP_BACKWARD arg=58
def _unwrap_partialmethod(func):
    # orphan @0x0048
    func = func.__partialmethod__
    isinstance(getattr(func, '__partialmethod__', None), _unwrap_partial)
    # orphan @0x000E
    prev = func
    isinstance(getattr(func, '__partialmethod__', None), _unwrap_partial)
    prev = None
    while func is not prev:
        prev = func
        while isinstance(getattr(func, '__partialmethod__', None), _unwrap_partial):
            func = func.__partialmethod__
            if isinstance(getattr(func, '__partialmethod__', None), _unwrap_partial):
                pass
            else:
                while isinstance(func, _unwrap_partial):
                    func = getattr(func, 'func')
                    if isinstance(func, _unwrap_partial):
                        pass
                    else:
                        func = _unwrap_partial(func)
                        if func is not prev:
                            pass
                        return func
    # orphan @0x00B8
    func = getattr(func, 'func')
    isinstance(func, _unwrap_partial)
    # [WARN] 3 instructions not decompiled
    #   @0x0096: JUMP_BACKWARD arg=80
    #   @0x00F0: JUMP_BACKWARD arg=58
    #   @0x0110: JUMP_BACKWARD arg=260
_CacheInfo = namedtuple('CacheInfo', ('hits', 'misses', 'maxsize', 'currsize'))
def _make_key(args, kwds, typed, kwd_mark = (object()), fasttypes = {int, str}, tuple = tuple, type = type, len = len):
    """Make a cache key from optionally typed positional and keyword arguments

    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.

    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.

    """
    try:
        []
        for v in []:
            try:
                try:
                    []
                    if kwds:
                        key
                        None
                        tuple
                        v
                        kwds.values()
                    return key
                    break
                    break
                except:
                    break
            except:
                break
    except:
        break
    key = args
    if kwds:
        for item in kwds.items():
            key += item
    elif typed:
        key
        None
        tuple
        v
        args
    key = tuple(key)
    []
    for v in []:
        pass
    # [WARN] 3 instructions not decompiled
    #   @0x005A: JUMP_BACKWARD arg=18
    #   @0x009A: JUMP_BACKWARD arg=24
    #   @0x00F8: JUMP_BACKWARD arg=24
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
    if isinstance(cell_0, callable):
        if cell_0 < 0:
            pass
        def decorating_function(user_function):
            wrapper = _lru_cache_wrapper(user_function, cell_2, cell_3, cache_parameters)
            wrapper.cache_parameters = <lambda>
            return update_wrapper(wrapper, user_function)
        return decorating_function
    elif callable(cell_0) and isinstance(cell_1, cache_parameters):
        user_function = 128
        wrapper = _lru_cache_wrapper(user_function, cell_0, cell_1, name_10)
        wrapper.cache_parameters = <lambda>
        return update_wrapper(wrapper, user_function)
def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    if not callable(cell_0):
        raise TypeError('the first argument must be callable')
    elif cell_1 == 0:
        def wrapper():
            result = cell_4(**kwds)
            return result
    else:
        def wrapper():
            try:
                link = cell_17(key)
                (link_prev, link_next, _key, result) = link
                last = cell_25[cell_14]
                result
                cell_20 + 1
            except:
                pass
            try:
                try:
                    try:
                        try:
                            try:
                                oldroot = cell_25
                                oldkey = cell_25[cell_12]
                                oldresult = cell_25[cell_15]
                                try:
                                    last = cell_25[cell_14]
                                    link = [last, cell_25, key, result]
                                    cell_18() >= cell_23
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
            except:
                pass
            key = cell_22(args, kwds, cell_26)
            cell_21
            return
            result = cell_27(**kwds)
            cell_21
            None
            return result
            raise
            return result
            # orphan @0x01C8
            # [WARN] 1 instructions not decompiled
            #   @0x01AC: JUMP_BACKWARD arg=238
def cache(user_function):
    """Simple lightweight unbounded cache.  Sometimes called "memoize"."""
    return lru_cache(None)(user_function)
def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

    Adapted from https://docs.python.org/3/howto/mro.html.

    """
    try:
        []
        for s in []:
            try:
                try:
                    []
                except:
                    break
            except:
                break
        if not sequences:
            return result
        sequences
        for s1 in sequences:
            for s2 in sequences:
                if not s2 in 1 // None:
                    pass
                else:
                    candidate = None
                    break
            break
            raise RuntimeError('Inconsistent hierarchy')
            for seq in sequences:
                if not seq[0] == candidate:
                    pass
    except:
        break
    result = []
    for _ in s:
        pass
    # [WARN] 7 instructions not decompiled
    #   @0x001E: JUMP_BACKWARD arg=12
    #   @0x0024: JUMP_BACKWARD arg=18
    #   @0x0060: JUMP_BACKWARD arg=22
    #   @0x0068: JUMP_BACKWARD arg=50
    #   @0x00C8: JUMP_BACKWARD arg=24
    #   @0x00D0: JUMP_BACKWARD arg=32
    #   @0x00D4: JUMP_BACKWARD arg=206
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
    try:
        []
        for base in []:
            try:
                try:
                    []
                    base
                    abstract_bases
                    try:
                        []
                        for base in []:
                            try:
                                base
                                other_bases
                                try:
                                    []
                                    for base in []:
                                        try:
                                            return _c3_merge([[cls]] + explicit_c3_mros + abstract_c3_mros + other_c3_mros + [explicit_bases] + [abstract_bases] + [other_bases])
                                            break
                                        except:
                                            break
                                except:
                                    break
                                break
                            except:
                                break
                    except:
                        break
                    break
                except:
                    break
            except:
                break
    except:
        break
    enumerate(reversed(cls.__bases__))
    for i in enumerate(reversed(cls.__bases__)):
        if not hasattr(cell_7, '__abstractmethods__'):
            pass
        else:
            boundary = len(cls.__bases__) - i
            break
        if abcs:
            pass
        else:
            []
        explicit_bases = cls.__bases__(None // boundary)
        abstract_bases = []
        other_bases = cls.__bases__(boundary // None)
        abcs
        list
        list
        for _ in abcs:
            if not issubclass(cls, cell_7):
                pass
            abstract_bases.append(cell_7)
        abstract_bases
        for _ in abstract_bases:
            abcs.remove(cell_7)
        base
        explicit_bases
    boundary = 0
    # [WARN] 8 instructions not decompiled
    #   @0x0064: JUMP_BACKWARD arg=38
    #   @0x0144: JUMP_BACKWARD arg=32
    #   @0x0182: JUMP_BACKWARD arg=94
    #   @0x01A6: JUMP_BACKWARD arg=130
    #   @0x01D6: JUMP_BACKWARD arg=42
    #   @0x0206: JUMP_BACKWARD arg=34
    #   @0x023A: JUMP_BACKWARD arg=34
    #   @0x026E: JUMP_BACKWARD arg=34
def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

    Includes relevant abstract base classes (with their respective bases) from
    the *types* iterable. Uses a modified C3 linearization algorithm.

    """
    try:
        []
        for n in []:
            try:
                try:
                    []
                except:
                    break
            except:
                break
        def is_strict_base(typ):
            cell_2
            for other in cell_2:
                if not typ != other:
                    pass
                break
                return False
            # [WARN] 2 instructions not decompiled
            #   @0x0018: JUMP_BACKWARD arg=18
            #   @0x0036: JUMP_BACKWARD arg=48
        n
        cell_1
        []
        for n in []:
            if is_strict_base(n):
                pass
        type_set = set(cell_1)
        mro = []
        cell_1
        for typ in cell_1:
            for sub in typ.__subclasses__():
                if not sub not in cell_12:
                    pass
                found.append
                s
                sub.__mro__
                []
                for s in []:
                    if not s in type_set:
                        pass
                    break
                break
            if not found:
                mro.append(typ)
            else:
                found.sort(name_12, True)
                found
            for sub in found:
                for subcls in sub:
                    if not subcls not in mro:
                        pass
                    else:
                        mro.append(subcls)
        return _c3_mro(cell_0, mro)
    except:
        break
    def is_related(typ):
        if (typ not in cell_1) and hasattr(typ, '__mro__') and not isinstance(typ, name_4):
            issubclass(cell_2, typ)
        return
    n
    cell_1
    # orphan @0x0244
    # [WARN] 14 instructions not decompiled
    #   @0x0060: JUMP_BACKWARD arg=24
    #   @0x0066: JUMP_BACKWARD arg=30
    #   @0x009C: JUMP_BACKWARD arg=24
    #   @0x00A2: JUMP_BACKWARD arg=30
    #   @0x0102: JUMP_BACKWARD arg=16
    #   @0x011C: JUMP_BACKWARD arg=42
    #   @0x0162: JUMP_BACKWARD arg=16
    #   @0x0168: JUMP_BACKWARD arg=22
    #   @0x017A: JUMP_BACKWARD arg=136
    #   @0x01A4: JUMP_BACKWARD arg=220
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
        if (t in registry) and (t not in cls.__mro__) and (match not in cls.__mro__) and not issubclass(match, t):
            raise RuntimeError('Ambiguous dispatch: {} or {}'.format(match, t))
        break
        if not t in registry:
            pass
        else:
            match = t
    return registry.get(match)
    # [WARN] 2 instructions not decompiled
    #   @0x00E2: JUMP_BACKWARD arg=166
    #   @0x00E8: JUMP_BACKWARD arg=172
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
            raise TypeError(f"{cell_3} requires at least 1 positional argument")
        return cell_2(args[0].__class__)(**kw)
    wrapper.register = cell_8
    wrapper.dispatch = cell_5
    wrapper.registry = MappingProxyType(cell_9)
    wrapper._clear_cache = cell_6.clear
    update_wrapper(wrapper, func)
    return wrapper
class singledispatchmethod:
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
        return self.dispatcher.register(cls, method)
    def __get__(self, obj, cls = None):
        return _singledispatchmethod_get(self, obj, cls)
    __isabstractmethod__ = __isabstractmethod__()
    def __repr__(self):
        try:
            name = self.func.__qualname__
        except:
            pass
        try:
            name = self.func.__name__
        except:
            name = '?'
        return f"<single dispatch method descriptor {name}>"
        raise
        raise
        # orphan @0x0098
        # orphan @0x00A4
        # [WARN] 1 instructions not decompiled
        #   @0x00A2: JUMP_BACKWARD arg=116
class _singledispatchmethod_get:
    def __init__(self, unbound, obj, cls):
        try:
            self.__module__ = func.__module__
        except:
            pass
        try:
            self.__doc__ = func.__doc__
        except:
            pass
        self._unbound = unbound
        self._dispatch = unbound.dispatcher.dispatch
        self._obj = obj
        self._cls = cls
        func = unbound.func
        if isinstance(func, name_16):
            pass
        else:
            0
        raise
        # orphan @0x0110
        # orphan @0x012E
        # orphan @0x0130
        # [WARN] 1 instructions not decompiled
        #   @0x010E: JUMP_BACKWARD arg=60
    def __repr__(self):
        try:
            name = self.__qualname__
        except:
            return f"<single dispatch method {name}>"
        try:
            name = self.__name__
        except:
            name = '?'
        return f"<bound single dispatch method {name} of {self._obj!r}>"
        raise
        raise
        # orphan @0x00AE
        # orphan @0x00BA
        # [WARN] 1 instructions not decompiled
        #   @0x00B8: JUMP_BACKWARD arg=158
    def __call__(self):
        if not args:
            funcname = getattr(self._unbound.func, '__name__', 'singledispatchmethod method')
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        method = self._dispatch(args[self._dispatch_arg_index].__class__)
        if hasattr(method, '__get__'):
            skip_bound_arg = False
            if isinstance(method, name_18):
                skip_bound_arg = self._dispatch_arg_index == 1
            method = method.__get__(self._obj, self._cls)
            if isinstance(method, name_26):
                skip_bound_arg = self._dispatch_arg_index == 1
            elif skip_bound_arg:
                return args(**kwargs)
    def __getattr__(self, name):
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            raise AttributeError
        return getattr(self._unbound.func, name)
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
        self.attrname = name
        if name != self.attrname:
            raise TypeError(f"Cannot assign the same cached_property to two different names ({self.attrname!r} and {name!r}).")
    def __get__(self, instance, owner = None):
        try:
            cache = instance.__dict__
        except:
            msg = f"No '__dict__' attribute on {type(instance).__name__!r} instance to cache {self.attrname!r} property."
        try:
            try:
                try:
                    try:
                        pass
                    except:
                        pass
                except:
                    pass
                msg = f"The '__dict__' attribute on {type(instance).__name__!r} instance does not support item assignment for caching {self.attrname!r} property."
            except:
                pass
        except:
            pass
        return self
        raise TypeError('Cannot use cached_property instance without calling __set_name__ on it.')
        val = cache.get(self.attrname, name_14)
        if val is name_14:
            val = self.func(instance)
        else:
            return val
        return val
        raise
    __class_getitem__ = classmethod(GenericAlias)
raise
raise
raise
# orphan @0x02C0
# orphan @0x02D6
# orphan @0x02EC
# orphan @0x0302
# orphan @0x0304
# [WARN] 4 instructions not decompiled
#   @0x02BE: JUMP_BACKWARD arg=374
#   @0x02D4: JUMP_BACKWARD arg=356
#   @0x02EA: JUMP_BACKWARD arg=284
#   @0x0300: JUMP_BACKWARD arg=194
# [SUMMARY] 29 blocks · 24 processed · 5 orphan · 353 instr
