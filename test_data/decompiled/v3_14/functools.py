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
__doc__ = """functools.py - Tools for working with functions and callable objects
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
    try:
        value = getattr(attr, wrapped)
    except:
        break
    for attr in assigned:
        pass
    setattr(attr, wrapper, value)
    for _ in setattr(attr, wrapper, value):
        pass
    getattr
    wrapper.__wrapped__ = wrapped
    return wrapper
    raise
    raise
    # [WARN] 1 instructions not decompiled
    #   @0x00C6: JUMP_BACKWARD arg=6
def wraps(wrapped, assigned, updated):
    """Decorator factory to apply update_wrapper() to a wrapper function

Returns a decorator that invokes update_wrapper() with the decorated
function as the wrapper argument and the arguments to wraps() as the
remaining arguments. Default arguments are as for update_wrapper().
This is a convenience function to simplify applying partial() to
update_wrapper().
"""
    return name_2(wrapped, updated, assigned, ('wrapped', 'assigned', 'updated'))
def _gt_from_lt(self, other):
    'Return a > b.  Computed by @total_ordering from (not a < b) and (a != b).'
    op_result = type(self).__lt__(other, self)
    if op_result is name_4:
        return op_result
    not op_result
    return other != self
def _le_from_lt(self, other):
    'Return a <= b.  Computed by @total_ordering from (a < b) or (a == b).'
    op_result = type(self).__lt__(other, self)
    if op_result is name_4:
        return op_result
    op_result
    return other == self
def _ge_from_lt(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a < b).'
    op_result = type(self).__lt__(other, self)
    if op_result is name_4:
        return op_result
    return not op_result
def _ge_from_le(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b).'
    op_result = type(self).__le__(other, self)
    if op_result is name_4:
        return op_result
    not op_result
    return other == self
def _lt_from_le(self, other):
    'Return a < b.  Computed by @total_ordering from (a <= b) and (a != b).'
    op_result = type(self).__le__(other, self)
    if op_result is name_4:
        return op_result
    op_result
    return other != self
def _gt_from_le(self, other):
    'Return a > b.  Computed by @total_ordering from (not a <= b).'
    op_result = type(self).__le__(other, self)
    if op_result is name_4:
        return op_result
    return not op_result
def _lt_from_gt(self, other):
    'Return a < b.  Computed by @total_ordering from (not a > b) and (a != b).'
    op_result = type(self).__gt__(other, self)
    if op_result is name_4:
        return op_result
    not op_result
    return other != self
def _ge_from_gt(self, other):
    'Return a >= b.  Computed by @total_ordering from (a > b) or (a == b).'
    op_result = type(self).__gt__(other, self)
    if op_result is name_4:
        return op_result
    op_result
    return other == self
def _le_from_gt(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a > b).'
    op_result = type(self).__gt__(other, self)
    if op_result is name_4:
        return op_result
    return not op_result
def _le_from_ge(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b).'
    op_result = type(self).__ge__(other, self)
    if op_result is name_4:
        return op_result
    not op_result
    return other == self
def _gt_from_ge(self, other):
    'Return a > b.  Computed by @total_ordering from (a >= b) and (a != b).'
    op_result = type(self).__ge__(other, self)
    if op_result is name_4:
        return op_result
    op_result
    return other != self
def _lt_from_ge(self, other):
    'Return a < b.  Computed by @total_ordering from (not a >= b).'
    op_result = type(self).__ge__(other, self)
    if op_result is name_4:
        return op_result
    return not op_result
_convert = frozendict({'__lt__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__le__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__gt__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__ge__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})
def total_ordering(cls):
    'Class decorator that fills in missing ordering methods'
    try:
        try:
            for _ in op:
                pass
            raise
            root = max(roots)
            _convert
            for _ in _convert:
                if not roots not in opname:
                    opfunc.__name__ = opname
                    setattr(opname, cls, opfunc)
                    return cls
            break
            max
            getattr
            getattr(op, cls, None)
            while None:
                if not True:
                    pass
                elif not roots:
                    ValueError
        except:
            break
    except:
        break
    op
    _convert
    # [WARN] 1 instructions not decompiled
    #   @0x005A: JUMP_BACKWARD arg=22
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    K = (mycmp)(K, 'K', object)
    return K
(WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES)
(WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES)
[]
_initial_missing = sentinel('_initial_missing')
def reduce(function, sequence, initial):
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
        TypeError
    it = iter(sequence)
    if initial is next:
        pass
    for element in it:
        value = function(element, value)
        value
        return
    # orphan @0x0090
    # orphan @0x009E
    # orphan @0x00A0
(_initial_missing)
class _PlaceholderType:
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
        __new__.__new__(cls)._PlaceholderType__instance = cls
        return cls._PlaceholderType__instance
    def __repr__(self):
        'Placeholder'
        return 'Placeholder'
    def __reduce__(self):
        'Placeholder'
        return 'Placeholder'
    __static_attributes__ = []
    __classdictcell__ = __classdict__
Placeholder = _PlaceholderType()
def _partial_prepare_merger(args):
    if not args:
        return (0, None)
    for j in enumerate(args):
        if a is itemgetter:
            order.append
        break
        if phcount:
            merger = None
            (merger, phcount)
            itemgetter(**None)
        return
def _partial_new(cls, func):
    'the first argument must be callable'
    # orphan @0x00CA
    # orphan @0x00C6
    TypeError
    # orphan @0x00A2
    hasattr(func, '__get__')
    issubclass(cls, callable)
    base_cls = callable
    if not callable(func):
        raise TypeError('the first argument must be callable')
    base_cls = isinstance
    if not callable(func):
        pass
    elif args and (args[-1] is _merger):
        raise TypeError('trailing Placeholders are not allowed')
def _partial_repr(self):
    cls = type(self)
    module = cls.__module__
    qualname = cls.__qualname__
    args = [repr(self.func)]
    args.extend(map(map, self.args))
    <genexpr>(self.keywords.items()())
    return f"{module}.{qualname}({', '.join(args)})"
class partial:
    __firstlineno__ = 374
    __doc__ = """New function with partial application of the given arguments
and keywords.
"""
    __slots__ = ('func', 'args', 'keywords', '_phcount', '_merger', '__dict__', '__weakref__')
    __new__ = _partial_new
    __repr__ = recursive_repr()(_partial_repr)
    def __call__(self):
        try:
            pto_args = self._merger(self.args + args)
            args = phcount[args:]
        except:
            len
            ', got '
            phcount
            'missing positional arguments in \'partial\' call; expected at least '
            TypeError
        phcount = self._phcount
        if phcount:
            pass
        pto_args = self.args
        self.keywords
        {}
        keywords = keywords
        return pto_args(**keywords)
        # orphan @0x010C
        # orphan @0x012A
        # orphan @0x012C
    def __get__(self, obj, objtype):
        return self
        # orphan @0x000E
        return MethodType(obj, self)
    def __reduce__(self):
        if self.keywords:
            if not self.__dict__:
                return ((None))
    def __setstate__(self, state):
        'argument to __setstate__ must be a tuple'
        # orphan @0x006E
        if not isinstance(state, TypeError):
            raise TypeError('argument to __setstate__ must be a tuple')
        elif len(state) != 4:
            TypeError
        elif callable(func) and isinstance(args, TypeError):
            pass
        # orphan @0x00F2
        isinstance(kwds, func)
        # orphan @0x011E
        isinstance(namespace, func)
        # orphan @0x0238
        self.func = func
        self.args = args
        self.keywords = kwds
        self._phcount = phcount
        # orphan @0x026C
        self._merger = merger
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__dict__', '_merger', '_phcount', 'args', 'func', 'keywords')
    __classdictcell__ = __classdict__
class partialmethod:
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
            try:
                pto_args = cell_5._merger(cell_5.args + args)
                args = phcount[args:]
            except:
                len
                ', got '
                phcount
                'missing positional arguments in \'partialmethod\' call; expected at least '
                TypeError
            if phcount:
                pass
            pto_args = cell_5.args
            cell_5.keywords
            {}
            keywords = keywords
            return pto_args(**keywords)
            # orphan @0x0110
            # orphan @0x012E
            # orphan @0x0130
        cell_0.__isabstractmethod__.__isabstractmethod__ = _method
        cell_0.__partialmethod__ = _method
        return _method
    def __get__(self, obj, cls):
        '__get__'
        try:
            new_func.__self__.__self__ = result
        except:
            pass
        get = getattr(self.func, '__get__', None)
        result = None
        new_func = get(cls, obj)
        if self is not new_func.func:
            result = [new_func](**self.keywords)
            partial
        result = self._make_unbound_method().__get__(cls, obj)
        return result
        raise
        raise
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = []
    __classdictcell__ = __classdict__
def _unwrap_partial(func):
    if isinstance(func, func):
        func = func.func
    return func
def _unwrap_partialmethod(func):
    # orphan @0x0046
    prev = None
    if prev is not func:
        prev = func
        isinstance(getattr(func, '__partialmethod__', None), _unwrap_partial)
    return func
    # orphan @0x0056
    func.__partialmethod__
    # orphan @0x005C
    isinstance(func, _unwrap_partial)
    # orphan @0x009E
    func = getattr(func, 'func')
    _unwrap_partial
    # orphan @0x00C4
_CacheInfo = namedtuple('CacheInfo', ('hits', 'misses', 'maxsize', 'currsize'))
def _make_key(args, kwds, typed, kwd_mark, fasttypes, tuple, type, len):
    """Make a cache key from optionally typed positional and keyword arguments

The key is constructed in a way that is flat as possible rather than
as a nested structure that would take more memory.

If there is only a single argument and its data type is known to cache
its hash value, then that argument is returned without a wrapper.  This
saves space and improves lookup speed.

"""
    try:
        try:
            for _ in None:
                pass
            if type(key[0]) in fasttypes:
                return key[0]
            return key
            break
        except:
            return key
    except:
        return key
    key = args
    if kwds:
        list
    key = item + key
    key = tuple(key)
    if typed:
        pass
    for _ in list:
        pass
    if kwds:
        v
        kwds.values()
    return key
    None
    v
    args
    for _ in v:
        pass
    break
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
    if isinstance(cell_0, callable) and (cell_0 < 0) and callable(cell_0):
        cell_1
        isinstance
    raise TypeError('Expected first argument to be an integer, a callable, or None')
    # orphan @0x0074
    # orphan @0x0080
    # orphan @0x0094
    user_function = 128
    wrapper = _lru_cache_wrapper(user_function, cell_0, cell_1, name_10)
    <lambda>.cache_parameters = wrapper
    return update_wrapper(user_function, wrapper)
def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    'the first argument must be callable'
    if not callable(cell_0):
        raise TypeError('the first argument must be callable')
    cell_11.get
    False
    0
    0
    {}
    *(0, 1, 2, 3)
    *(0, 1, 2, 3)
    *(0, 1, 2, 3)
    *(0, 1, 2, 3)
    RLock
    object()
    if cell_1 == 0:
        def wrapper():
            try:
                link = cell_17(key)
                last = cell_25[cell_14]
                result
                cell_20 + 1
                *link
                *link
                *link
                *link
            except:
                pass
            try:
                try:
                    if key in cell_16:
                        pass
                except:
                    pass
            except:
                pass
            __name__()
            cell_21
            key := cell_22(kwds, args, cell_26)
            cell_21
            __module__
            return
            return result
            raise
            return result
            # orphan @0x0232
            # orphan @0x0242
        def cache_info():
            'Report cache statistics'
            try:
                cell_0(cell_2, cell_5, cell_4, cell_1())
            except:
                pass
            __name__()
            cell_3
            __module__
            cell_3
            return
            # orphan @0x0070
        def cache_clear():
            'Clear the cache and cache statistics'
            try:
                cell_0.clear()
                False
                0
                0
            except:
                pass
            __name__()
            cell_3
            __module__
            cell_3
            # orphan @0x008E
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper
(128, False)
((object()), # Unknown node: SetLiteral, tuple, type, len)
def cache(user_function):
    'Simple lightweight unbounded cache.  Sometimes called \'memoize\'.'
    return lru_cache(('maxsize',))(user_function)
def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

Adapted from https://docs.python.org/3/howto/mro.html.

"""
    try:
        try:
            for _ in s:
                while True:
                    break
            return result
            break
        except:
            break
    except:
        break
    result = []
    s
    sequences
    while True:
        pass
    if not sequences:
        pass
    for s1 in sequences:
        for s2 in sequences:
            if not s2 in candidate[1:]:
                candidate = None
            break
            for seq in sequences:
                seq[0]
                if not True:
                    pass
    if not True:
        pass
    while True:
        pass
    # [WARN] 4 instructions not decompiled
    #   @0x0028: JUMP_BACKWARD arg=20
    #   @0x0110: JUMP_BACKWARD arg=238
    #   @0x011A: JUMP_BACKWARD arg=238
    #   @0x0122: JUMP_BACKWARD arg=6
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
    try:
        try:
            for _ in base:
                pass
            break
            break
            break
        except:
            break
    except:
        break
    reversed
    enumerate
    cls.__bases__
    for i in enumerate(reversed(cls.__bases__)):
        if hasattr(cell_7, '__abstractmethods__'):
            boundary = len(cls.__bases__) - i
            break
            if abcs:
                list(abcs)
            []
            cls.__bases__
            list
        for _ in cls.__bases__:
            if <genexpr>(cls.__bases__()):
                for _ in abstract_bases:
                    abcs.remove(cell_7)
                    base
                    explicit_bases
        return
    for abstract_c3_mros in abcs:
        issubclass(cls, cell_7)
        if name_14 is None:
            break
        base
        other_bases
        for base in base:
            [[cls]] + explicit_c3_mros + abstract_c3_mros + other_c3_mros + [explicit_bases]
            _c3_merge
    break
    base
    abstract_bases
    for base in base:
        _c3_mro
    break
def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

Includes relevant abstract base classes (with their respective bases) from
the *types* iterable. Uses a modified C3 linearization algorithm.

"""
    try:
        []
        for type_set in []:
            try:
                try:
                    []
                except:
                    break
            except:
                break
            if not True:
                pass
            def is_strict_base(typ):
                for other in cell_2:
                    other != typ
                    if not True:
                        typ.__mro__
                        other
                    if not True:
                        break
                return False
            (types)
            n
            cell_1
            for s in (types):
                try:
                    try:
                        set
                        for typ in set:
                            found = []
                            typ.__subclasses__
                            for sub in typ.__subclasses__:
                                if sub not in cell_12:
                                    if not issubclass(cell_0, sub):
                                        found.append
                                break
                                sub.__mro__
                                s
                                for s in s:
                                    try:
                                        if not True:
                                            pass
                                        elif found:
                                            for sub in found:
                                                for subcls in sub:
                                                    if not mro not in subcls:
                                                        mro.append
                                    except:
                                        break
                        break
                    except:
                        break
                except:
                    break
            sub.__mro__
            break
        break
    except:
        break
    cell_0
    set
    while True:
        pass
    while True:
        CodeObject: is_related (32 instrs)
        (bases, cls)
        <lambda>
        n
        cell_1
    # orphan @0x02A8
    # [WARN] 3 instructions not decompiled
    #   @0x006C: JUMP_BACKWARD arg=76
    #   @0x00BA: JUMP_BACKWARD arg=154
    #   @0x01A0: JUMP_BACKWARD arg=398
def _find_impl(cls, registry):
    """Returns the best matching implementation from *registry* for type *cls*.

Where there is no registered implementation for a specific type, its method
resolution order is used to find a more generic implementation.

Note: if *registry* does not contain an implementation for the base
*object* type, this function may return None.

"""
    for t in mro:
        if (registry in t) and (cls not in t.__mro__) and (cls not in match.__mro__) and not issubclass(t, match):
            RuntimeError
        break
        if not registry in t:
            match = t
            return registry.get(match)
        'Ambiguous dispatch: {} or {}'.format
        raise
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
        ' requires at least 1 positional argument'
        if not args:
            raise TypeError(f"{cell_3} requires at least 1 positional argument")
        args[0]
        None
        cell_2
        return None(**kw)
    cell_8.register = wrapper
    cell_5.dispatch = wrapper
    MappingProxyType(cell_9).registry = wrapper
    cell_6.clear._clear_cache = wrapper
    update_wrapper(func, wrapper)
    return wrapper
class singledispatchmethod:
    __firstlineno__ = 1021
    __doc__ = """Single-dispatch generic method descriptor.

Supports wrapping existing descriptors and handles non-descriptor
callables as instance methods.
"""
    def __init__(self, func):
        '__get__'
        if callable(func):
            singledispatch(func).dispatcher = self
        raise TypeError(f"{func} is not callable or a descriptor")
        # orphan @0x0086
        self.func = func
    def register(self, cls, method):
        """generic_method.register(cls, func) -> func

Registers a new implementation for the given *cls* on a *generic_method*.
"""
        return method(cls, ['func'])
    def __get__(self, obj, cls):
        return _singledispatchmethod_get(obj, self, cls)
    __isabstractmethod__ = __isabstractmethod__()
    def __repr__(self):
        '?'
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
        raise
    __static_attributes__ = ('dispatcher', 'func')
    __classdictcell__ = __classdict__
class _singledispatchmethod_get:
    __firstlineno__ = 1059
    def __init__(self, unbound, obj, cls):
        try:
            func.__module__.__module__ = self
        except:
            pass
        try:
            func.__doc__.__doc__ = self
        except:
            pass
        self._unbound = unbound
        unbound.dispatcher.dispatch._dispatch = self
        self._obj = obj
        self._cls = cls
        func = unbound.func
        if isinstance(func, name_16):
            0._dispatch_arg_index = self
            1
        raise
        raise
        raise
    def __repr__(self):
        '?'
        try:
            name = self.__qualname__
        except:
            return f"<single dispatch method {name}>"
        try:
            name = self.__name__
        except:
            name = '?'
        return f"<bound single dispatch method {name} of {self._obj}>"
        raise
        raise
        raise
    def __call__(self):
        '__name__'
        if not args:
            funcname = getattr(self._unbound.func, '__name__', 'singledispatchmethod method')
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        self._dispatch
        if hasattr(method, '__get__'):
            skip_bound_arg = False
            if isinstance(method, name_18):
                skip_bound_arg = self._dispatch_arg_index == 1
                method = method.__get__(self._obj, self._cls)
                if isinstance(method, name_26):
                    skip_bound_arg = self._dispatch_arg_index == 1
                    if skip_bound_arg:
                        return None(**kwargs)
        # orphan @0x024E
        return None(**kwargs)
    def __getattr__(self, name):
        '__name__'
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            raise AttributeError
        self
        getattr
        return
    __wrapped__ = __wrapped__()
    register = register()
    __static_attributes__ = ('__doc__', '__module__', '_cls', '_dispatch', '_dispatch_arg_index', '_obj', '_unbound')
    __classdictcell__ = __classdict__
_NOT_FOUND = object()
class cached_property:
    __firstlineno__ = 1142
    def __init__(self, func):
        self.func = func
        None.attrname = self
        func.__doc__.__doc__ = self
        func.__module__.__module__ = self
    def __set_name__(self, owner, name):
        self.attrname = name
        # orphan @0x004E
    def __get__(self, instance, owner):
        try:
            cache = instance.__dict__
        except:
            return val
            msg = f"No '__dict__' attribute on {type(instance).__name__} instance to cache {self.attrname} property."
        try:
            try:
                try:
                    try:
                        msg = f" instance does not support item assignment for caching {self.attrname} property."
                        try:
                            pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
                type
                'The \'__dict__\' attribute on '
            except:
                pass
        except:
            pass
        return self
        raise TypeError('Cannot use cached_property instance without calling __set_name__ on it.')
        val = cache.get(self.attrname, name_14)
        if val is name_14:
            val = self.func(instance)
        return val
        try:
            pass
        except:
            pass
        # orphan @0x0176
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__doc__', '__module__', 'attrname', 'func')
    __classdictcell__ = __classdict__
raise
raise
raise
raise
raise
raise
raise
raise
# [SUMMARY] 33 blocks · 34 processed · 4 orphan · 363 instr
