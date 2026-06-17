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
from types import FunctionType
from types import GenericAlias
from types import MethodType
from types import MappingProxyType
from types import UnionType
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
        try:
            try:
                pass
            except:
                pass
            break
        except:
            pass
    except:
        pass
    for attr in assigned:
        break
        for attr in updated:
            break
            break
    # [WARN] 2 instructions not decompiled
    #   @0x0096: JUMP_BACKWARD arg=0
    #   @0x00C4: JUMP_BACKWARD arg=0
def wraps(wrapped, assigned, updated):
    """Decorator factory to apply update_wrapper() to a wrapper function

Returns a decorator that invokes update_wrapper() with the decorated
function as the wrapper argument and the arguments to wraps() as the
remaining arguments. Default arguments are as for update_wrapper().
This is a convenience function to simplify applying partial() to
update_wrapper().
"""
    return
def _gt_from_lt(self, other):
    'Return a > b.  Computed by @total_ordering from (not a < b) and (a != b).'
    if op_result is name_4:
        return op_result
    # orphan @0x0066
    not op_result
    return
def _le_from_lt(self, other):
    'Return a <= b.  Computed by @total_ordering from (a < b) or (a == b).'
    if op_result is name_4:
        return op_result
    # orphan @0x005C
    op_result
    return
def _ge_from_lt(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a < b).'
    if op_result is name_4:
        return op_result
    # orphan @0x004C
    return not op_result
def _ge_from_le(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b).'
    if op_result is name_4:
        return op_result
    # orphan @0x0066
    not op_result
    return
def _lt_from_le(self, other):
    'Return a < b.  Computed by @total_ordering from (a <= b) and (a != b).'
    if op_result is name_4:
        return op_result
    # orphan @0x005C
    op_result
    return
def _gt_from_le(self, other):
    'Return a > b.  Computed by @total_ordering from (not a <= b).'
    if op_result is name_4:
        return op_result
    # orphan @0x004C
    return not op_result
def _lt_from_gt(self, other):
    'Return a < b.  Computed by @total_ordering from (not a > b) and (a != b).'
    if op_result is name_4:
        return op_result
    # orphan @0x0066
    not op_result
    return
def _ge_from_gt(self, other):
    'Return a >= b.  Computed by @total_ordering from (a > b) or (a == b).'
    if op_result is name_4:
        return op_result
    # orphan @0x005C
    op_result
    return
def _le_from_gt(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a > b).'
    if op_result is name_4:
        return op_result
    # orphan @0x004C
    return not op_result
def _le_from_ge(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b).'
    if op_result is name_4:
        return op_result
    # orphan @0x0066
    not op_result
    return
def _gt_from_ge(self, other):
    'Return a > b.  Computed by @total_ordering from (a >= b) and (a != b).'
    if op_result is name_4:
        return op_result
    # orphan @0x005C
    op_result
    return
def _lt_from_ge(self, other):
    'Return a < b.  Computed by @total_ordering from (not a >= b).'
    if op_result is name_4:
        return op_result
    # orphan @0x004C
    return not op_result
_convert = frozendict({'__ge__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__gt__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__le__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__lt__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})
def total_ordering(cls):
    'Class decorator that fills in missing ordering methods'
    try:
        try:
            for _ in op:
                pass
            break
            break
        except:
            break
    except:
        break
    if not True:
        pass
    for _ in _convert[root]:
        if not True:
            pass
    if not roots:
        raise ValueError('must define at least one ordering operation: < > <= >=')
    root = max(roots)
    # [WARN] 2 instructions not decompiled
    #   @0x005A: JUMP_BACKWARD arg=-6
    #   @0x0062: JUMP_BACKWARD arg=-6
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
        break
    # orphan @0x0080
    # orphan @0x008A
    raise
    # orphan @0x009A
    raise
    # orphan @0x009C
    raise
class _PlaceholderType:
    __firstlineno__ = 278
    __doc__ = """The type of the Placeholder singleton.

Used as a placeholder for partial arguments.
"""
    _PlaceholderType__instance = None
    __slots__ = ()
    def __init_subclass__(cls):
        raise TypeError(f"type '{cls.__name__}' is not an acceptable base type")
    def __new__(cls):
        __new__.__new__(cls)._PlaceholderType__instance = cls
        return cls._PlaceholderType__instance
    def __repr__(self):
        return 'Placeholder'
    def __reduce__(self):
        return 'Placeholder'
    __static_attributes__ = ()
Placeholder = _PlaceholderType()
def _partial_prepare_merger(args):
    if not args:
        return (0, None)
    for j in args:
        if a is itemgetter:
            order.append(j)
            j += 1
        order.append(i)
        break
        if phcount:
            merger = None
            return ()
    # [WARN] 2 instructions not decompiled
    #   @0x008E: JUMP_BACKWARD arg=-2
    #   @0x00B4: JUMP_BACKWARD arg=-2
def _partial_new(cls, func):
    # orphan @0x00DE
    # orphan @0x00BE
    raise TypeError(f"the first argument {func} must be a callable or a descriptor")
    # orphan @0x009E
    # orphan @0x009C
    # orphan @0x006E
    base_cls = isinstance
    if issubclass(cls, callable):
        base_cls = callable
        if not callable(func):
            raise TypeError('the first argument must be callable')
        elif args[-1] is _merger:
            pass
    raise
    for value in TypeError:
        if not value is _merger:
            raise TypeError('Placeholder cannot be passed as a keyword argument')
        keywords = keywords
        func = func.func
        tot_args = args
        return self
        break
        pto_phcount = func._phcount
        if args:
            pass
        if pto_phcount:
            pass
    return self
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
        except:
            pass
        phcount = self._phcount
        if phcount:
            pass
        try:
            try:
                raise
                raise
            except:
                pass
        except:
            pass
        pto_args = self.args
        keywords = keywords
        return pto_args(**keywords)
    def __get__(self, obj, objtype):
        return self
        # orphan @0x000C
        return
    def __reduce__(self):
        if self.keywords:
            pass
        return ((None))
    def __setstate__(self, state):
        # orphan @0x0060
        # orphan @0x0042
        if not isinstance(state, TypeError):
            raise TypeError('argument to __setstate__ must be a tuple')
        raise
        if callable(func) and isinstance(args, TypeError) and isinstance(kwds, func):
            pass
        # orphan @0x0134
        # orphan @0x0142
        raise TypeError('invalid partial state')
        # orphan @0x0158
        # orphan @0x0166
        # orphan @0x017E
        raise TypeError('trailing Placeholders are not allowed')
        # orphan @0x0194
        args = tuple(args)
        kwds = {}
        # orphan @0x01F4
        kwds = dict(kwds)
        namespace = {}
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__dict__', '_merger', '_phcount', 'args', 'func', 'keywords')
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
                try:
                    try:
                        try:
                            try:
                                raise
                                raise
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
            if phcount:
                pass
            keywords = keywords
            return pto_args(**keywords)
        (self).__isabstractmethod__.__isabstractmethod__ = _method
        return _method
    def __get__(self, obj, cls):
        try:
            new_func.__self__.__self__ = result
        except:
            pass
        get = getattr(self.func, '__get__', None)
        result = None
        result = [new_func](**self.keywords)
        return result
        raise
        raise
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ()
def _unwrap_partial(func):
    if isinstance(func, func):
        func = func.func
        if isinstance(func, func):
            return func
def _unwrap_partialmethod(func):
    prev = None
    prev = func
    if isinstance(getattr(func, '__partialmethod__', None), _unwrap_partial):
        func = func.__partialmethod__
        if isinstance(getattr(func, '__partialmethod__', None), _unwrap_partial):
            pass
    # orphan @0x00AC
    # orphan @0x00D8
    func = getattr(func, 'func')
    # orphan @0x011A
    # orphan @0x011C
    func = _unwrap_partial(func)
    # orphan @0x013C
    # orphan @0x013E
    return func
    # [WARN] 1 instructions not decompiled
    #   @0x00AA: JUMP_BACKWARD arg=0
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
            break
        except:
            return key
    except:
        return key
    key = args
    if kwds:
        key = list(key)
    for v in v:
        break
        return key
    break
    for _ in kwds:
        pass
    if kwds:
        pass
    key = tuple(key)
    if typed:
        pass
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
    return
    # orphan @0x0104
    raise TypeError('Expected first argument to be an integer, a callable, or None')
def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    # orphan @0x005C
    if not True:
        raise TypeError('the first argument must be callable')
    elif None == 0:
        def wrapper():
            try:
                try:
                    try:
                        return result
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
            try:
                try:
                    if not True:
                        pass
                except:
                    pass
            except:
                pass
            return
            result = None(**kwds)
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
        (_CacheInfo, cache_len, hits, lock, maxsize, misses).cache_info = (cache, full, hits, lock, misses, root)
        (cache, cache_get, hits, make_key, misses, sentinel, typed, user_function).cache_clear = (KEY, NEXT, PREV, RESULT, cache, cache_get, cache_len, full, hits, lock, make_key, maxsize, misses, root, typed, user_function)
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
            candidate = s1[0]
            for s2 in sequences:
                if not True:
                    candidate = None
                    break
                break
                for seq in 1:
                    if not seq[0] == candidate:
                        pass
            break
        except:
            break
    except:
        break
    result = []
    while True:
        pass
    for s1 in []:
        pass
    break
    if not sequences:
        return result
    # [WARN] 2 instructions not decompiled
    #   @0x0028: JUMP_BACKWARD arg=4
    #   @0x0102: JUMP_BACKWARD arg=0
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
            break
        except:
            break
    except:
        break
    for i in cls.__bases__:
        if not True:
            pass
        for _ in list:
            if not True:
                pass
            return
        break
        if abcs:
            abcs = []
        break
        for _ in abstract_bases:
            break
    for base in base:
        break
        for base in base:
            break
    break
def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

Includes relevant abstract base classes (with their respective bases) from
the *types* iterable. Uses a modified C3 linearization algorithm.

"""
    try:
        try:
            for _ in n:
                pass
            for typ in set:
                for sub in set:
                    if not True:
                        pass
                    break
                    break
                    if not True:
                        pass
                    break
                    for _ in s:
                        if not True:
                            pass
            break
            break
        except:
            break
    except:
        break
    for _ in is_related:
        while True:
            pass
    if not True:
        pass
    def is_strict_base(typ):
        for other in iterable:
            if not True:
                pass
            elif not True:
                pass
            break
        # [WARN] 2 instructions not decompiled
        #   @0x0018: JUMP_BACKWARD arg=0
        #   @0x003A: JUMP_BACKWARD arg=0
    for _ in n:
        pass
    break
    if not found:
        mro.append(typ)
    for sub in found:
        for subcls in found:
            if not True:
                pass
    # [WARN] 3 instructions not decompiled
    #   @0x019C: JUMP_BACKWARD arg=346
    #   @0x01BA: JUMP_BACKWARD arg=0
    #   @0x0272: JUMP_BACKWARD arg=0
def _find_impl(cls, registry):
    """Returns the best matching implementation from *registry* for type *cls*.

Where there is no registered implementation for a specific type, its method
resolution order is used to find a more generic implementation.

Note: if *registry* does not contain an implementation for the base
*object* type, this function may return None.

"""
    for t in mro:
        if not True:
            raise
        break
        if not True:
            pass
        break
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
            raise
        return
        # orphan @0x002E
    (dispatch, funcname).register = wrapper
    register.dispatch = wrapper
    (_is_valid_dispatch_type, cache_token, dispatch_cache, register, registry)(MappingProxyType).registry = wrapper
    (None,).clear._clear_cache = wrapper
    dispatch(_is_valid_dispatch_type, update_wrapper)
    return wrapper
class singledispatchmethod:
    __firstlineno__ = 1021
    __doc__ = """Single-dispatch generic method descriptor.

Supports wrapping existing descriptors and handles non-descriptor
callables as instance methods.
"""
    def __init__(self, func):
        if callable(func):
            pass
        raise TypeError(f"{func} is not callable or a descriptor")
        singledispatch(func).dispatcher = self
    def register(self, cls, method):
        """generic_method.register(cls, func) -> func

Registers a new implementation for the given *cls* on a *generic_method*.
"""
        return
    def __get__(self, obj, cls):
        return
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
        raise
    __static_attributes__ = ('dispatcher', 'func')
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
        unbound.dispatcher.dispatch._dispatch = self
        func = unbound.func
        if isinstance(func, name_16):
            0._dispatch_arg_index = self
        return None
        raise
        raise
        return None
        raise
        raise
    def __repr__(self):
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
        # orphan @0x006E
        if not args:
            funcname = getattr(self._unbound.func, '__name__', 'singledispatchmethod method')
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        elif isinstance(method, name_26):
            skip_bound_arg = self._dispatch_arg_index == 1
            if skip_bound_arg:
                return None(**kwargs)
        # orphan @0x00DE
        skip_bound_arg = False
        # orphan @0x010C
        skip_bound_arg = self._dispatch_arg_index == 1
        # orphan @0x028A
        return None(**kwargs)
    def __getattr__(self, name):
        # orphan @0x001A
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            raise AttributeError
        return
    __wrapped__ = __wrapped__()
    register = register()
    __static_attributes__ = ('__doc__', '__module__', '_cls', '_dispatch', '_dispatch_arg_index', '_obj', '_unbound')
_NOT_FOUND = object()
class cached_property:
    __firstlineno__ = 1142
    def __init__(self, func):
        None.attrname = self
        func.__doc__.__doc__ = self
        func.__module__.__module__ = self
    def __set_name__(self, owner, name):
        return None
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
        # orphan @0x016E
        raise
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__doc__', '__module__', 'attrname', 'func')
return None
raise
raise
raise
raise
raise
raise
raise
raise
# [SUMMARY] 33 blocks · 33 processed · 4 orphan · 359 instr
