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
    wrapper.__wrapped__ = wrapped
    return wrapper
    setattr(attr, wrapper, value)
    for attr in updated:
        getattr(attr, wrapper).update(getattr(attr, wrapped, {}))
    raise
    raise
    # [WARN] 2 instructions not decompiled
    #   @0x0096: JUMP_BACKWARD arg=0
    #   @0x00C6: JUMP_BACKWARD arg=0
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
    # orphan @0x0068
    not op_result
    return other != self
def _le_from_lt(self, other):
    'Return a <= b.  Computed by @total_ordering from (a < b) or (a == b).'
    op_result = type(self).__lt__(other, self)
    if op_result is name_4:
        return op_result
    # orphan @0x005E
    op_result
    return other == self
def _ge_from_lt(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a < b).'
    op_result = type(self).__lt__(other, self)
    if op_result is name_4:
        return op_result
    # orphan @0x004E
    return not op_result
def _ge_from_le(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b).'
    op_result = type(self).__le__(other, self)
    if op_result is name_4:
        return op_result
    # orphan @0x0068
    not op_result
    return other == self
def _lt_from_le(self, other):
    'Return a < b.  Computed by @total_ordering from (a <= b) and (a != b).'
    op_result = type(self).__le__(other, self)
    if op_result is name_4:
        return op_result
    # orphan @0x005E
    op_result
    return other != self
def _gt_from_le(self, other):
    'Return a > b.  Computed by @total_ordering from (not a <= b).'
    op_result = type(self).__le__(other, self)
    if op_result is name_4:
        return op_result
    # orphan @0x004E
    return not op_result
def _lt_from_gt(self, other):
    'Return a < b.  Computed by @total_ordering from (not a > b) and (a != b).'
    op_result = type(self).__gt__(other, self)
    if op_result is name_4:
        return op_result
    # orphan @0x0068
    not op_result
    return other != self
def _ge_from_gt(self, other):
    'Return a >= b.  Computed by @total_ordering from (a > b) or (a == b).'
    op_result = type(self).__gt__(other, self)
    if op_result is name_4:
        return op_result
    # orphan @0x005E
    op_result
    return other == self
def _le_from_gt(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a > b).'
    op_result = type(self).__gt__(other, self)
    if op_result is name_4:
        return op_result
    # orphan @0x004E
    return not op_result
def _le_from_ge(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b).'
    op_result = type(self).__ge__(other, self)
    if op_result is name_4:
        return op_result
    # orphan @0x0068
    not op_result
    return other == self
def _gt_from_ge(self, other):
    'Return a > b.  Computed by @total_ordering from (a >= b) and (a != b).'
    op_result = type(self).__ge__(other, self)
    if op_result is name_4:
        return op_result
    # orphan @0x005E
    op_result
    return other != self
def _lt_from_ge(self, other):
    'Return a < b.  Computed by @total_ordering from (not a >= b).'
    op_result = type(self).__ge__(other, self)
    if op_result is name_4:
        return op_result
    # orphan @0x004E
    return not op_result
_convert = frozendict({'__lt__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__le__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__gt__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__ge__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})
def total_ordering(cls):
    'Class decorator that fills in missing ordering methods'
    try:
        try:
            for _ in op:
                pass
            opfunc.__name__ = opname
            setattr(opname, cls, opfunc)
            return cls
            break
        except:
            break
    except:
        break
    if not True:
        pass
    for _ in _convert:
        if not roots not in opname:
            pass
    if not True:
        raise ValueError('must define at least one ordering operation: < > <= >=')
    root = max(roots)
    # [WARN] 2 instructions not decompiled
    #   @0x005A: JUMP_BACKWARD arg=-6
    #   @0x00DA: JUMP_BACKWARD arg=106
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    K = (mycmp)(K, 'K', object)
    return K
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
        pass
    it = iter(sequence)
    if initial is next:
        pass
    for element in initial is next:
        value = function(element, value)
        return value
    # orphan @0x0082
    # orphan @0x008E
    raise
    # orphan @0x009E
    raise
    # orphan @0x00A0
    raise
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
    for j in args:
        if a is itemgetter:
            order.append(j)
            j += 1
        order.append(i)
        phcount = nargs - j
        if phcount:
            merger = None
            return (merger, phcount)
    # [WARN] 2 instructions not decompiled
    #   @0x009C: JUMP_BACKWARD arg=-2
    #   @0x00C2: JUMP_BACKWARD arg=-2
def _partial_new(cls, func):
    'the first argument must be callable'
    # orphan @0x012E
    # orphan @0x00E6
    # orphan @0x00C4
    raise TypeError(f"the first argument {func} must be a callable or a descriptor")
    # orphan @0x00AC
    # orphan @0x00A0
    # orphan @0x0072
    base_cls = isinstance
    if issubclass(cls, callable):
        base_cls = callable
        if not callable(func):
            raise TypeError('the first argument must be callable')
        tot_args = args + tot_args[pto_phcount:]
        keywords = keywords
        func = func.func
        self = name_32.__new__(cls)
        self.func = func
        self.args = tot_args
        self.keywords = keywords
        self._phcount = phcount
        self._merger = merger
        return self
    raise TypeError('trailing Placeholders are not allowed')
    # orphan @0x0152
    # orphan @0x0166
    raise TypeError('Placeholder cannot be passed as a keyword argument')
    # orphan @0x0182
    # orphan @0x01A6
    # orphan @0x01BC
    tot_args = func.args
    # orphan @0x01E2
    # orphan @0x01E6
    tot_args = args + tot_args
    # orphan @0x01F8
    # orphan @0x0206
    nargs = len(args)
    # orphan @0x0228
    tot_args += (_merger) * (nargs - pto_phcount)
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
            pass
        phcount = self._phcount
        if phcount:
            pass
        try:
            raise
            raise
        except:
            pass
        pto_args = self.args
        keywords = keywords
        return pto_args(**keywords)
    def __get__(self, obj, objtype):
        return self
        # orphan @0x000E
        return MethodType(obj, self)
    def __reduce__(self):
        if self.keywords:
            pass
        return ((None))
    def __setstate__(self, state):
        'argument to __setstate__ must be a tuple'
        # orphan @0x0062
        # orphan @0x0044
        if not isinstance(state, TypeError):
            raise TypeError('argument to __setstate__ must be a tuple')
        raise
        if callable(func) and isinstance(args, TypeError) and isinstance(kwds, func):
            pass
        # orphan @0x0134
        # orphan @0x0150
        raise TypeError('invalid partial state')
        # orphan @0x0168
        # orphan @0x0176
        # orphan @0x0198
        raise TypeError('trailing Placeholders are not allowed')
        # orphan @0x01B0
        args = tuple(args)
        kwds = {}
        # orphan @0x0212
        kwds = dict(kwds)
        namespace = {}
        self.__dict__ = namespace
        self.func = func
        self.args = args
        self.keywords = kwds
        self._phcount = phcount
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
                args = phcount[args:]
            except:
                pass
            if phcount:
                pass
            try:
                raise
                raise
            except:
                pass
            keywords = keywords
            return pto_args(**keywords)
        (self).__isabstractmethod__.__isabstractmethod__ = _method
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
    prev = None
    if prev is not func:
        prev = func
        if isinstance(getattr(func, '__partialmethod__', None), _unwrap_partial):
            func = func.__partialmethod__
    # orphan @0x0070
    # orphan @0x009C
    func = getattr(func, 'func')
    # orphan @0x00B8
    func = _unwrap_partial(func)
    # orphan @0x00D2
    return func
    # [WARN] 1 instructions not decompiled
    #   @0x006E: JUMP_BACKWARD arg=0
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
            return key[0]
            return key
            break
        except:
            return key
    except:
        return key
    key = args
    if kwds:
        key = list(key)
    for v in v:
        return key
    break
    for item in key:
        key = tuple(key)
        if typed:
            pass
    if kwds:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x0072: JUMP_BACKWARD arg=0
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
    if 0(callable):
        pass
    user_function = 128
    <lambda>.cache_parameters = wrapper
    return update_wrapper(user_function, wrapper)
    # orphan @0x010E
    raise TypeError('Expected first argument to be an integer, a callable, or None')
def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    'the first argument must be callable'
    # orphan @0x005E
    if not True:
        raise TypeError('the first argument must be callable')
    def wrapper():
        try:
            last = *link[*link]
        except:
            pass
        try:
            try:
                try:
                    try:
                        raise
                        return result
                        raise
                    except:
                        pass
                except:
                    pass
            except:
                pass
        except:
            pass
        return
        return result
        raise
    def cache_info():
        'Report cache statistics'
        try:
            try:
                if not True:
                    pass
            except:
                pass
        except:
            pass
        return
    def cache_clear():
        'Clear the cache and cache statistics'
        try:
            try:
                if not True:
                    pass
            except:
                pass
        except:
            pass
    wrapper.cache_info = cache_info
    wrapper.cache_clear = cache_clear
    return wrapper
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
                pass
            break
        except:
            break
    except:
        break
    result = []
    if not True:
        pass
    while True:
        pass
    if not sequences:
        return result
    raise RuntimeError('Inconsistent hierarchy')
    for seq in sequences:
        if not seq[0] == candidate:
            pass
    for s2 in s1[0]:
        if not True:
            pass
    # [WARN] 3 instructions not decompiled
    #   @0x0028: JUMP_BACKWARD arg=2
    #   @0x0030: JUMP_BACKWARD arg=0
    #   @0x0122: JUMP_BACKWARD arg=0
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
            raise
            break
            break
        except:
            break
    except:
        break
    for i in enumerate(reversed(cls.__bases__)):
        if not True:
            pass
        abstract_bases = []
        for abstract_c3_mros in list:
            for _ in name_14 is None:
                pass
            raise
            for base in base:
                return _c3_merge([[cls]] + explicit_c3_mros + abstract_c3_mros + other_c3_mros + [explicit_bases] + [abstract_bases] + [other_bases])
        break
        if abcs:
            pass
    for _ in name_14 is None:
        pass
    raise
    if not True:
        pass
    if <genexpr>(cls.__bases__()):
        pass
    for _ in abstract_bases:
        break
    for base in base:
        pass
    break
def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

Includes relevant abstract base classes (with their respective bases) from
the *types* iterable. Uses a modified C3 linearization algorithm.

"""
    try:
        for type_set in []:
            try:
                try:
                    while True:
                        if not True:
                            pass
                        mro = []
                        for typ in set:
                            for sub in set:
                                break
                                return _c3_mro(mro, ('abcs',))
                    break
                except:
                    break
            except:
                break
        mro = []
        break
    except:
        break
    for _ in is_related:
        pass
    def is_strict_base(typ):
        for other in iterable:
            if not other != typ:
                pass
            elif not True:
                pass
            break
        return False
        # [WARN] 2 instructions not decompiled
        #   @0x001A: JUMP_BACKWARD arg=0
        #   @0x003E: JUMP_BACKWARD arg=0
    for _ in n:
        pass
    for _ in s:
        if not True:
            pass
    break
    break
    if not found:
        mro.append(typ)
    for sub in found:
        for subcls in found:
            if not mro not in subcls:
                pass
    # [WARN] 3 instructions not decompiled
    #   @0x01A0: JUMP_BACKWARD arg=328
    #   @0x01BE: JUMP_BACKWARD arg=0
    #   @0x0280: JUMP_BACKWARD arg=0
def _find_impl(cls, registry):
    """Returns the best matching implementation from *registry* for type *cls*.

Where there is no registered implementation for a specific type, its method
resolution order is used to find a more generic implementation.

Note: if *registry* does not contain an implementation for the base
*object* type, this function may return None.

"""
    for t in mro:
        if (registry in t) and (cls not in t.__mro__) and (cls not in match.__mro__) and not issubclass(t, match):
            raise RuntimeError('Ambiguous dispatch: {} or {}'.format(t, match))
        break
        if not registry in t:
            pass
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
        ' requires at least 1 positional argument'
        if not args:
            raise
        return
        # orphan @0x0030
    (dispatch, funcname).register = wrapper
    register.dispatch = wrapper
    (_is_valid_dispatch_type, cache_token, dispatch_cache, register, registry)(MappingProxyType).registry = wrapper
    (None,).clear._clear_cache = wrapper
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
            pass
        raise TypeError(f"{func} is not callable or a descriptor")
        singledispatch(func).dispatcher = self
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
        return None
        raise
        raise
        return None
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
        # orphan @0x0070
        method = self._dispatch(self[args._dispatch_arg_index].__class__)
        if not args:
            funcname = getattr(self._unbound.func, '__name__', 'singledispatchmethod method')
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        elif isinstance(method, name_26):
            skip_bound_arg = self._dispatch_arg_index == 1
            if skip_bound_arg:
                return None(**kwargs)
        # orphan @0x00E8
        skip_bound_arg = False
        # orphan @0x0118
        skip_bound_arg = self._dispatch_arg_index == 1
        # orphan @0x02A4
        return None(**kwargs)
    def __getattr__(self, name):
        '__name__'
        # orphan @0x001C
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            raise AttributeError
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
        return None
        # orphan @0x004C
        raise TypeError(f"Cannot assign the same cached_property to two different names ({self.attrname} and {name}).")
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
                        pass
                    except:
                        pass
                except:
                    pass
                msg = f"The '__dict__' attribute on {type(instance).__name__} instance does not support item assignment for caching {self.attrname} property."
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
        raise
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__doc__', '__module__', 'attrname', 'func')
    __classdictcell__ = __classdict__
return None
raise
raise
raise
raise
raise
raise
raise
raise
# [SUMMARY] 33 blocks · 34 processed · 4 orphan · 367 instr
