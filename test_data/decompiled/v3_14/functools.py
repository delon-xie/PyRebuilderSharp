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
    assigned
    for attr in assigned:
        pass
    updated
    for attr in updated:
        getattr(attr, wrapper).update(getattr(attr, wrapped, {}))
    wrapper.__wrapped__ = wrapped
    return wrapper
    setattr(attr, wrapper, value)
    # orphan @0x00CA
    # orphan @0x00CC
    # [WARN] 3 instructions not decompiled
    #   @0x003C: JUMP_BACKWARD arg=6
    #   @0x0096: JUMP_BACKWARD arg=72
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
    """Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""
    op_result = type(self).__lt__(other, self)
    if op_result is name_4:
        return op_result
    elif not op_result:
        other != self
def _le_from_lt(self, other):
    """Return a <= b.  Computed by @total_ordering from (a < b) or (a == b)."""
    op_result = type(self).__lt__(other, self)
    if op_result is name_4:
        return op_result
    elif not op_result:
        other == self
def _ge_from_lt(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a < b)."""
    op_result = type(self).__lt__(other, self)
    if op_result is name_4:
        return op_result
    return not op_result
def _ge_from_le(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b)."""
    op_result = type(self).__le__(other, self)
    if op_result is name_4:
        return op_result
    elif not not op_result:
        other == self
def _lt_from_le(self, other):
    """Return a < b.  Computed by @total_ordering from (a <= b) and (a != b)."""
    op_result = type(self).__le__(other, self)
    if op_result is name_4:
        return op_result
    elif op_result:
        other != self
def _gt_from_le(self, other):
    """Return a > b.  Computed by @total_ordering from (not a <= b)."""
    op_result = type(self).__le__(other, self)
    if op_result is name_4:
        return op_result
    return not op_result
def _lt_from_gt(self, other):
    """Return a < b.  Computed by @total_ordering from (not a > b) and (a != b)."""
    op_result = type(self).__gt__(other, self)
    if op_result is name_4:
        return op_result
    elif not op_result:
        other != self
def _ge_from_gt(self, other):
    """Return a >= b.  Computed by @total_ordering from (a > b) or (a == b)."""
    op_result = type(self).__gt__(other, self)
    if op_result is name_4:
        return op_result
    elif not op_result:
        other == self
def _le_from_gt(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a > b)."""
    op_result = type(self).__gt__(other, self)
    if op_result is name_4:
        return op_result
    return not op_result
def _le_from_ge(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b)."""
    op_result = type(self).__ge__(other, self)
    if op_result is name_4:
        return op_result
    elif not not op_result:
        other == self
def _gt_from_ge(self, other):
    """Return a > b.  Computed by @total_ordering from (a >= b) and (a != b)."""
    op_result = type(self).__ge__(other, self)
    if op_result is name_4:
        return op_result
    elif op_result:
        other != self
def _lt_from_ge(self, other):
    """Return a < b.  Computed by @total_ordering from (not a >= b)."""
    op_result = type(self).__ge__(other, self)
    if op_result is name_4:
        return op_result
    return not op_result
_convert = frozendict({'__lt__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__le__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__gt__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__ge__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})
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
                getattr(op, cls, None) is not getattr(max, op, None)
            except:
                break
            if not True:
                pass
        if not roots:
            raise ValueError('must define at least one ordering operation: < > <= >=')
        root = max(roots)
        _convert[root]
        for _ in _convert[root]:
            if not roots not in opname:
                pass
            else:
                opfunc.__name__ = opname
                setattr(opname, cls, opfunc)
        return cls
    except:
        break
    op
    _convert
    # [WARN] 4 instructions not decompiled
    #   @0x005A: JUMP_BACKWARD arg=22
    #   @0x0062: JUMP_BACKWARD arg=22
    #   @0x00DA: JUMP_BACKWARD arg=196
    #   @0x0102: JUMP_BACKWARD arg=196
def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""
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
        pass
    it = iter(sequence)
    if initial is next:
        pass
    else:
        value = initial
    it
    for element in it:
        value = function(element, value)
    return value
    # orphan @0x00A0
    # [WARN] 1 instructions not decompiled
    #   @0x0064: JUMP_BACKWARD arg=78
(_initial_missing)
class _PlaceholderType:
    __firstlineno__ = 278
    __doc__ = """The type of the Placeholder singleton.

Used as a placeholder for partial arguments.
"""
    _PlaceholderType__instance = None
    __slots__ = []
    def __init_subclass__(cls):
        """type '"""
        raise TypeError(f"type '{cls.__name__}' is not an acceptable base type")
    def __new__(cls):
        __new__.__new__(cls)._PlaceholderType__instance = cls
        return cls._PlaceholderType__instance
    def __repr__(self):
        """Placeholder"""
        return 'Placeholder'
    def __reduce__(self):
        """Placeholder"""
        return 'Placeholder'
    __static_attributes__ = []
    __classdictcell__ = __classdict__
Placeholder = _PlaceholderType()
def _partial_prepare_merger(args):
    if not args:
        return (0, None)
    nargs = len(args)
    order = []
    j = nargs
    enumerate(args)
    for j in enumerate(args):
        if a is itemgetter:
            order.append(j)
            j += 1
        else:
            order.append(i)
    phcount = nargs - j
    if phcount:
        pass
    else:
        None
    return (merger, phcount)
    # [WARN] 2 instructions not decompiled
    #   @0x009C: JUMP_BACKWARD arg=74
    #   @0x00C2: JUMP_BACKWARD arg=74
def _partial_new(cls, func):
    """the first argument must be callable"""
    if issubclass(cls, callable):
        base_cls = callable
        if not callable(func):
            raise TypeError('the first argument must be callable')
        elif args and (args[-1] is _merger):
            raise TypeError('trailing Placeholders are not allowed')
    else:
        base_cls = isinstance
    if not hasattr(func, '__get__'):
        raise TypeError(f"the first argument {func} must be a callable or a descriptor")
    # [WARN] 1 instructions not decompiled
    #   @0x0168: JUMP_BACKWARD arg=334
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
        else:
            pto_args = self.args
        keywords = keywords
        return pto_args(**keywords)
        # orphan @0x012C
    def __get__(self, obj, objtype):
        return self
        # orphan @0x000E
        return MethodType(obj, self)
    def __reduce__(self):
        if not self.keywords:
            None
        elif not self.__dict__:
            None
    def __setstate__(self, state):
        """argument to __setstate__ must be a tuple"""
        if not isinstance(state, TypeError):
            raise TypeError('argument to __setstate__ must be a tuple')
        elif len(state) != 4:
            raise TypeError(f"expected 4 items in state, got {len(state)}")
        elif callable(func) and isinstance(args, TypeError) and isinstance(kwds, func) and not isinstance(namespace, func):
            raise TypeError('invalid partial state')
        elif args and (args[-1] is keywords):
            raise TypeError('trailing Placeholders are not allowed')
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
                pass
            if phcount:
                pass
            else:
                pto_args = cell_5.args
            keywords = keywords
            return pto_args(**keywords)
            # orphan @0x0130
        cell_0.__isabstractmethod__.__isabstractmethod__ = _method
        cell_0.__partialmethod__ = _method
        return _method
    def __get__(self, obj, cls):
        """__get__"""
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
        # orphan @0x0138
        # orphan @0x013A
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = []
    __classdictcell__ = __classdict__
def _unwrap_partial(func):
    while isinstance(func, func):
        func = func.func
    return func
    # [WARN] 1 instructions not decompiled
    #   @0x0046: JUMP_BACKWARD arg=2
def _unwrap_partialmethod(func):
    prev = None
    while prev is not func:
        prev = func
        while isinstance(getattr(func, '__partialmethod__', None), _unwrap_partial):
            func = func.__partialmethod__
        while isinstance(func, _unwrap_partial):
            func = getattr(func, 'func')
        func = _unwrap_partial(func)
    return func
    # [WARN] 3 instructions not decompiled
    #   @0x006E: JUMP_BACKWARD arg=20
    #   @0x00B6: JUMP_BACKWARD arg=114
    #   @0x00D0: JUMP_BACKWARD arg=6
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
        []
        for _ in []:
            try:
                try:
                    []
                    if kwds:
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
            key = item + key
    elif typed:
        None
        v
        args
    key = tuple(key)
    []
    for _ in []:
        pass
    # [WARN] 3 instructions not decompiled
    #   @0x0072: JUMP_BACKWARD arg=92
    #   @0x00BE: JUMP_BACKWARD arg=170
    #   @0x0130: JUMP_BACKWARD arg=284
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
    if isinstance(cell_0, callable):
        if cell_0 < 0:
            0
        def decorating_function(user_function):
            <lambda>.cache_parameters = wrapper
            return update_wrapper(user_function, wrapper)
        return decorating_function
    elif callable(cell_0) and isinstance(cell_1, cache_parameters):
        user_function = 128
        wrapper = _lru_cache_wrapper(user_function, cell_0, cell_1, name_10)
        <lambda>.cache_parameters = wrapper
        return update_wrapper(user_function, wrapper)
def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    """the first argument must be callable"""
    if not callable(cell_0):
        raise TypeError('the first argument must be callable')
    elif cell_1 == 0:
        def wrapper():
            return result
    else:
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
                    try:
                        if cell_19:
                            pass
                        else:
                            last = cell_25[cell_14]
                            link = [last, cell_25, result, key]
                            cell_18() >= cell_23
                        return result
                        try:
                            try:
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
            except:
                pass
            __name__()
            cell_21
            key := cell_22(kwds, args, cell_26)
            cell_21
            __module__
            return
            raise
        (KEY, NEXT, PREV, RESULT, cache, cache_get, cache_len, full, hits, lock, make_key, maxsize, misses, root, typed, user_function)
        (cache, cache_get, hits, make_key, misses, sentinel, typed, user_function)
(128, False)
((object()), {int, str}, tuple, type, len)
def cache(user_function):
    """Simple lightweight unbounded cache.  Sometimes called "memoize"."""
    return lru_cache(('maxsize',))(user_function)
def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

Adapted from https://docs.python.org/3/howto/mro.html.

"""
    try:
        []
        for _ in []:
            try:
                try:
                    []
                except:
                    break
            except:
                break
            if not True:
                pass
        if not sequences:
            return result
        sequences
        for s1 in sequences:
            for s2 in sequences:
                if not s2 in candidate[1:]:
                    pass
                else:
                    candidate = None
                    break
            break
            raise RuntimeError('Inconsistent hierarchy')
            for seq in sequences:
                if not seq[0] == candidate:
                    pass
            s
            sequences
    except:
        break
    result = []
    # [WARN] 7 instructions not decompiled
    #   @0x0028: JUMP_BACKWARD arg=20
    #   @0x0030: JUMP_BACKWARD arg=20
    #   @0x0090: JUMP_BACKWARD arg=112
    #   @0x009A: JUMP_BACKWARD arg=84
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
        explicit_bases = list(cls.__bases__[None:boundary])
        abstract_bases = []
        other_bases = list(cls.__bases__[boundary:])
        abcs
        for _ in abcs:
            if not issubclass(cls, cell_7):
                pass
            <genexpr>(cls.__bases__())
            (base)
            None
            break
            for _ in cls.__bases__():
                if not True:
                    pass
        abstract_bases
        for _ in abstract_bases:
            abcs.remove(cell_7)
        base
        explicit_bases
    boundary = 0
    # [WARN] 9 instructions not decompiled
    #   @0x0070: JUMP_BACKWARD arg=64
    #   @0x0174: JUMP_BACKWARD arg=330
    #   @0x01CC: JUMP_BACKWARD arg=442
    #   @0x0220: JUMP_BACKWARD arg=330
    #   @0x0246: JUMP_BACKWARD arg=330
    #   @0x027A: JUMP_BACKWARD arg=594
    #   @0x02AC: JUMP_BACKWARD arg=654
    #   @0x02E2: JUMP_BACKWARD arg=708
    #   @0x0318: JUMP_BACKWARD arg=762
def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

Includes relevant abstract base classes (with their respective bases) from
the *types* iterable. Uses a modified C3 linearization algorithm.

"""
    try:
        []
        for _ in []:
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
            cell_2
            for other in cell_2:
                if not other != typ:
                    pass
                break
            return False
            # [WARN] 2 instructions not decompiled
            #   @0x001A: JUMP_BACKWARD arg=8
            #   @0x003E: JUMP_BACKWARD arg=8
        (types)
        n
        cell_1
        []
        for _ in []:
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
                try:
                    []
                    for _ in []:
                        if not True:
                            pass
                        break
                    break
                except:
                    break
            if not found:
                mro.append(typ)
            else:
                name_12(True, ('key', 'reverse'))
                found
                found.sort
            for sub in found:
                for subcls in sub:
                    if not mro not in subcls:
                        pass
                    else:
                        mro.append(subcls)
        return cell_0(mro, ('abcs',))
    except:
        break
    def is_related(typ):
        """__mro__"""
        if (typ not in cell_1) and hasattr(typ, '__mro__') and not isinstance(typ, name_4):
            issubclass(cell_2, typ)
        return
    set(cell_0.__mro__)
    (bases, cls)
    n
    cell_1
    # orphan @0x02AC
    # [WARN] 14 instructions not decompiled
    #   @0x006C: JUMP_BACKWARD arg=76
    #   @0x0074: JUMP_BACKWARD arg=76
    #   @0x00BA: JUMP_BACKWARD arg=154
    #   @0x00C2: JUMP_BACKWARD arg=154
    #   @0x012C: JUMP_BACKWARD arg=280
    #   @0x0154: JUMP_BACKWARD arg=280
    #   @0x01A0: JUMP_BACKWARD arg=398
    #   @0x01A8: JUMP_BACKWARD arg=398
    #   @0x01BE: JUMP_BACKWARD arg=280
    #   @0x01F8: JUMP_BACKWARD arg=238
def _find_impl(cls, registry):
    """Returns the best matching implementation from *registry* for type *cls*.

Where there is no registered implementation for a specific type, its method
resolution order is used to find a more generic implementation.

Note: if *registry* does not contain an implementation for the base
*object* type, this function may return None.

"""
    mro = _compose_mro(registry, cls.keys())
    match = None
    mro
    for t in mro:
        if (registry in t) and (cls not in t.__mro__) and (cls not in match.__mro__) and not issubclass(t, match):
            raise RuntimeError('Ambiguous dispatch: {} or {}'.format(t, match))
        break
        if not registry in t:
            pass
        else:
            match = t
    return registry.get(match)
    # [WARN] 2 instructions not decompiled
    #   @0x00FC: JUMP_BACKWARD arg=60
    #   @0x0104: JUMP_BACKWARD arg=60
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
        """ requires at least 1 positional argument"""
        if not args:
            raise TypeError(f"{cell_3} requires at least 1 positional argument")
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
        """__get__"""
        pass
    def register(self, cls, method):
        """generic_method.register(cls, func) -> func

Registers a new implementation for the given *cls* on a *generic_method*.
"""
        return method(cls, ['func'])
    def __get__(self, obj, cls):
        return _singledispatchmethod_get(obj, self, cls)
    __isabstractmethod__ = __isabstractmethod__()
    def __repr__(self):
        """?"""
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
        # orphan @0x00A4
        # orphan @0x00AC
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
            pass
        else:
            0
        raise
        # orphan @0x0120
        # orphan @0x0144
        # orphan @0x0146
    def __repr__(self):
        """?"""
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
        # orphan @0x00C0
        # orphan @0x00C8
    def __call__(self):
        """__name__"""
        if not args:
            funcname = getattr(self._unbound.func, '__name__', 'singledispatchmethod method')
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        method = self._dispatch(self[args._dispatch_arg_index].__class__)
        if hasattr(method, '__get__'):
            skip_bound_arg = False
            if isinstance(method, name_18):
                skip_bound_arg = self._dispatch_arg_index == 1
            method = method.__get__(self._obj, self._cls)
            if isinstance(method, name_26):
                skip_bound_arg = self._dispatch_arg_index == 1
            elif skip_bound_arg:
                return None(**kwargs)
    def __getattr__(self, name):
        """__name__"""
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            raise AttributeError
        return getattr(self._unbound.func, name)
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
        else:
            return val
        return val
        raise
    __class_getitem__ = classmethod(GenericAlias)
    __static_attributes__ = ('__doc__', '__module__', 'attrname', 'func')
    __classdictcell__ = __classdict__
raise
raise
raise
# orphan @0x02D8
# orphan @0x02F2
# orphan @0x030C
# orphan @0x0326
# orphan @0x0328
# [SUMMARY] 29 blocks · 25 processed · 5 orphan · 363 instr
