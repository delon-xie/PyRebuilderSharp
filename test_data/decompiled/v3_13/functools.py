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
    break
    for attr in updated:
        break
    break
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
        pass
    return
    # orphan @0x0066
    not op_result
    # orphan @0x006C
    return
def _le_from_lt(self, other):
    'Return a <= b.  Computed by @total_ordering from (a < b) or (a == b).'
    if op_result is name_4:
        pass
    return
    # orphan @0x005C
    op_result
    # orphan @0x0062
    return
def _ge_from_lt(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a < b).'
    if op_result is name_4:
        pass
    return
    # orphan @0x004C
    return not op_result
def _ge_from_le(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b).'
    if op_result is name_4:
        pass
    return
    # orphan @0x0066
    not op_result
    # orphan @0x006C
    return
def _lt_from_le(self, other):
    'Return a < b.  Computed by @total_ordering from (a <= b) and (a != b).'
    if op_result is name_4:
        pass
    return
    # orphan @0x005C
    op_result
    # orphan @0x0062
    return
def _gt_from_le(self, other):
    'Return a > b.  Computed by @total_ordering from (not a <= b).'
    if op_result is name_4:
        pass
    return
    # orphan @0x004C
    return not op_result
def _lt_from_gt(self, other):
    'Return a < b.  Computed by @total_ordering from (not a > b) and (a != b).'
    if op_result is name_4:
        pass
    return
    # orphan @0x0066
    not op_result
    # orphan @0x006C
    return
def _ge_from_gt(self, other):
    'Return a >= b.  Computed by @total_ordering from (a > b) or (a == b).'
    if op_result is name_4:
        pass
    return
    # orphan @0x005C
    op_result
    # orphan @0x0062
    return
def _le_from_gt(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a > b).'
    if op_result is name_4:
        pass
    return
    # orphan @0x004C
    return not op_result
def _le_from_ge(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b).'
    if op_result is name_4:
        pass
    return
    # orphan @0x0066
    not op_result
    # orphan @0x006C
    return
def _gt_from_ge(self, other):
    'Return a > b.  Computed by @total_ordering from (a >= b) and (a != b).'
    if op_result is name_4:
        pass
    return
    # orphan @0x005C
    op_result
    # orphan @0x0062
    return
def _lt_from_ge(self, other):
    'Return a < b.  Computed by @total_ordering from (not a >= b).'
    if op_result is name_4:
        pass
    return
    # orphan @0x004C
    return not op_result
_convert = frozendict({'__ge__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__gt__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__le__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__lt__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})
def total_ordering(cls):
    'Class decorator that fills in missing ordering methods'
    try:
        for op in op:
            try:
                break
            except:
                break
            if not True:
                pass
        break
        if not roots:
            pass
        raise
        root = max(roots)
        for _ in _convert[root]:
            if not True:
                pass
            else:
                break
        break
    except:
        break
    # [WARN] 1 instructions not decompiled
    #   @0x005A: JUMP_BACKWARD arg=70
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
    value = initial
    for element in it:
        pass
    break
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
        cls._PlaceholderType__instance = __new__.__new__(cls)
        return cls._PlaceholderType__instance
    def __repr__(self):
        return 'Placeholder'
    def __reduce__(self):
        return 'Placeholder'
    __static_attributes__ = ()
Placeholder = _PlaceholderType()
def _partial_prepare_merger(args):
    if not args:
        for j in enumerate(args):
            if a is itemgetter:
                order.append(j)
                j += 1
            else:
                order.append(i)
    # orphan @0x00B8
    # orphan @0x00D2
    # orphan @0x00E0
    # orphan @0x00E4
    return ()
def _partial_new(cls, func):
    # orphan @0x0118
    raise
    # orphan @0x0104
    # orphan @0x00EC
    # orphan @0x00DE
    if issubclass(cls, callable):
        base_cls = callable
        if not callable(func):
            pass
        raise
        base_cls = isinstance
        if callable(func) or not hasattr(func, '__get__'):
            raise
    # orphan @0x011A
    # orphan @0x0138
    # orphan @0x013E
    # orphan @0x0152
    # orphan @0x0154
    raise TypeError('Placeholder cannot be passed as a keyword argument')
    # orphan @0x016C
    # orphan @0x0190
    pto_phcount = func._phcount
    tot_args = func.args
    # orphan @0x01CE
    # orphan @0x01E4
    nargs = len(args)
    # orphan @0x0204
    # orphan @0x0220
    tot_args = func._merger(tot_args)
    # orphan @0x024E
    # orphan @0x025A
    # orphan @0x0276
    # orphan @0x0290
    keywords = keywords
    func = func.func
    # orphan @0x02C8
    tot_args = args
    # orphan @0x02E8
    self = name_32.__new__(cls)
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
        pto_args = self.args
        keywords = keywords
        return pto_args(**keywords)
        # orphan @0x011E
        raise
        # orphan @0x0120
        raise
    def __get__(self, obj, objtype):
        return self
        # orphan @0x000C
        return
    def __reduce__(self):
        if not self.keywords:
            pass
        elif not self.__dict__:
            pass
    def __setstate__(self, state):
        if not isinstance(state, TypeError):
            pass
        raise
        if len(state) != 4:
            pass
        raise
        if callable(func) and isinstance(args, TypeError) and isinstance(kwds, func) and not isinstance(namespace, func):
            pass
        raise
        if args and (args[-1] is keywords):
            pass
        raise
        args = tuple(args)
        kwds = {}
        if type(kwds) is not func:
            pass
        namespace = {}
        # orphan @0x0142
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
            if phcount:
                pass
            keywords = keywords
            return pto_args(**keywords)
        _method.__isabstractmethod__ = (self).__isabstractmethod__
        return _method
    def __get__(self, obj, cls):
        try:
            result.__self__ = new_func.__self__
        except:
            pass
        get = getattr(self.func, '__get__', None)
        result = None
        if True:
            result = [new_func](**self.keywords)
        return result
        raise
        raise
        # orphan @0x012E
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ()
def _unwrap_partial(func):
    while isinstance(func, func):
        pass
    return func
    # orphan @0x002C
    func = func.func
    # orphan @0x006E
def _unwrap_partialmethod(func):
    # orphan @0x0052
    func = func.__partialmethod__
    # orphan @0x000E
    prev = func
    prev = None
    while True:
        pass
    return func
    # orphan @0x00AA
    # orphan @0x00AC
    # orphan @0x00D8
    func = getattr(func, 'func')
    # orphan @0x011A
    # orphan @0x011C
    func = _unwrap_partial(func)
    # orphan @0x013C
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
        for _ in []:
            try:
                try:
                    try:
                        break
                    except:
                        return key
                except:
                    return key
            except:
                return key
    except:
        return key
    key = args
    if kwds:
        for item in kwds.items():
            pass
    elif typed:
        pass
    break
    if kwds:
        pass
    for _ in []:
        pass
    break
    if type(key[0]) in fasttypes:
        pass
    return
    # orphan @0x0182
    raise
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
    if True and True:
        pass
    elif True and True:
        user_function = 128
        wrapper.cache_parameters = <lambda>
    # orphan @0x0104
    raise TypeError('Expected first argument to be an integer, a callable, or None')
def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    if not True:
        pass
    raise
    if None == 0:
        def wrapper():
            return result
    def wrapper():
        try:
            try:
                try:
                    try:
                        try:
                            link = [last]
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
        return result
        return result
        # orphan @0x01DA
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
    (cache, full, hits, lock, misses, root).cache_info = (_CacheInfo, cache_len, hits, lock, maxsize, misses)
    return wrapper
def cache(user_function):
    'Simple lightweight unbounded cache.  Sometimes called \'memoize\'.'
    return lru_cache(('maxsize',))(user_function)
def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

Adapted from https://docs.python.org/3/howto/mro.html.

"""
    try:
        for _ in s:
            try:
                break
            except:
                break
            if not True:
                pass
        break
        if not sequences:
            pass
        return
    except:
        break
    result = []
    for _ in s:
        pass
    for s1 in sequences:
        for s2 in sequences:
            if not True:
                pass
            else:
                candidate = None
                break
        break
        raise RuntimeError('Inconsistent hierarchy')
        for seq in 0:
            if not seq[0] == candidate:
                pass
        break
    break
    # [WARN] 2 instructions not decompiled
    #   @0x0028: JUMP_BACKWARD arg=22
    #   @0x00F0: JUMP_BACKWARD arg=28
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
        for base in []:
            try:
                try:
                    try:
                        break
                    except:
                        break
                except:
                    break
            except:
                break
    except:
        break
    try:
        for base in []:
            try:
                try:
                    try:
                        break
                    except:
                        break
                except:
                    break
            except:
                break
    except:
        break
    for i in enumerate(reversed(cls.__bases__)):
        if not True:
            pass
        else:
            boundary = len(cls.__bases__) - i
            break
        if abcs:
            pass
        explicit_bases = list(cls.__bases__[None:boundary])
        abstract_bases = []
        other_bases = list(cls.__bases__[boundary:])
        for _ in abcs:
            if not True:
                pass
            break
        break
        for _ in abstract_bases:
            break
        break
    break
    for base in []:
        pass
    break
    return _c3_merge([[cls]] + explicit_c3_mros + abstract_c3_mros + other_c3_mros + [explicit_bases] + [abstract_bases] + [other_bases])
    # orphan @0x02F8
    raise
def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

Includes relevant abstract base classes (with their respective bases) from
the *types* iterable. Uses a modified C3 linearization algorithm.

"""
    try:
        for _ in n:
            try:
                break
                break
                break
            except:
                break
            if not True:
                pass
        break
        def is_strict_base(typ):
            for other in iterable:
                if not True:
                    pass
                break
                break
        for _ in n:
            if True:
                pass
        break
        mro = []
        for typ in n:
            for sub in typ.__subclasses__():
                if not True:
                    pass
                for _ in s:
                    if not True:
                        pass
                break
                break
            break
            if not found:
                mro.append(typ)
            else:
                name_12(True, ('key', 'reverse'))
            for sub in found:
                for subcls in sub:
                    if not True:
                        pass
                    else:
                        mro.append(subcls)
                break
            break
        break
    except:
        break
    def is_related(typ):
        if True and hasattr(typ, '__mro__') and not isinstance(typ, name_4):
            pass
        return
    # [WARN] 3 instructions not decompiled
    #   @0x006C: JUMP_BACKWARD arg=34
    #   @0x00BA: JUMP_BACKWARD arg=34
    #   @0x019C: JUMP_BACKWARD arg=20
def _find_impl(cls, registry):
    """Returns the best matching implementation from *registry* for type *cls*.

Where there is no registered implementation for a specific type, its method
resolution order is used to find a more generic implementation.

Note: if *registry* does not contain an implementation for the base
*object* type, this function may return None.

"""
    match = None
    for t in mro:
        if True and True and True and not True:
            pass
        raise
        break
        if not True:
            pass
        else:
            match = t
    break
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
        if not args:
            pass
        raise
        return None(**kw)
    wrapper.register = (dispatch, funcname)
    wrapper.dispatch = register
    wrapper.registry = (_is_valid_dispatch_type, cache_token, dispatch_cache, register, registry)(MappingProxyType)
    wrapper._clear_cache = (None,).clear
    dispatch(_is_valid_dispatch_type, update_wrapper)
    return wrapper
class singledispatchmethod:
    __firstlineno__ = 1021
    __doc__ = """Single-dispatch generic method descriptor.

Supports wrapping existing descriptors and handles non-descriptor
callables as instance methods.
"""
    def __init__(self, func):
        if callable(func) or not hasattr(func, '__get__'):
            raise
        # orphan @0x0062
        self.dispatcher = singledispatch(func)
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
        # orphan @0x009E
        # orphan @0x00A6
        raise
    __static_attributes__ = ('dispatcher', 'func')
class _singledispatchmethod_get:
    __firstlineno__ = 1059
    def __init__(self, unbound, obj, cls):
        try:
            self.__module__ = func.__module__
        except:
            pass
        try:
            self.__doc__ = func.__doc__
        except:
            pass
        self._dispatch = unbound.dispatcher.dispatch
        func = unbound.func
        if isinstance(func, name_16):
            pass
        return None
        raise
        raise
        raise
        raise
        # orphan @0x0116
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
        # orphan @0x00B8
        # orphan @0x00C0
        raise
    def __call__(self):
        if not args:
            funcname = getattr(self._unbound.func, '__name__', 'singledispatchmethod method')
        raise
        if hasattr(method, '__get__'):
            skip_bound_arg = False
            if isinstance(method, name_18):
                pass
            method = method.__get__(self._obj, self._cls)
            if isinstance(method, name_26):
                pass
            elif skip_bound_arg:
                pass
        # orphan @0x01E2
        return None(**kwargs)
    def __getattr__(self, name):
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            pass
        raise
        return getattr(self._unbound.func, name)
    __wrapped__ = __wrapped__()
    register = register()
    __static_attributes__ = ('__doc__', '__module__', '_cls', '_dispatch', '_dispatch_arg_index', '_obj', '_unbound')
_NOT_FOUND = object()
class cached_property:
    __firstlineno__ = 1142
    def __init__(self, func):
        self.attrname = None
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__
    def __set_name__(self, owner, name):
        return None
        if True:
            pass
        raise
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
                        try:
                            pass
                        except:
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
        return
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
# orphan @0x02CC
# orphan @0x02E4
# orphan @0x02FC
# orphan @0x0314
# [SUMMARY] 33 blocks · 30 processed · 4 orphan · 359 instr
