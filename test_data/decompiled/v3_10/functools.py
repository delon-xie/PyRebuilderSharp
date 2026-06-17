# Decompiled from: <module>

"""functools.py - Tools for working with functions and callable objects
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
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
    for attr in updated:
        break
    wrapper.__wrapped__ = wrapped
    return wrapper
    # orphan @0x002A
    setattr(wrapper, attr, value)
def wraps():
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(update_wrapper, wrapped=var_0, assigned=var_1, updated=var_2)
def _gt_from_lt(self, other):
    'Return a > b.  Computed by @total_ordering from (not a < b) and (a != b).'
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    # orphan @0x0022
    return self != other
    # orphan @0x004A
def _le_from_lt(self, other):
    'Return a <= b.  Computed by @total_ordering from (a < b) or (a == b).'
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    # orphan @0x0020
    return self == other
    # orphan @0x0046
def _ge_from_lt(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a < b).'
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    return not op_result
def _ge_from_le(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b).'
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    # orphan @0x0022
    return self == other
    # orphan @0x004A
def _lt_from_le(self, other):
    'Return a < b.  Computed by @total_ordering from (a <= b) and (a != b).'
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    # orphan @0x0020
    return self != other
    # orphan @0x0046
def _gt_from_le(self, other):
    'Return a > b.  Computed by @total_ordering from (not a <= b).'
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    return not op_result
def _lt_from_gt(self, other):
    'Return a < b.  Computed by @total_ordering from (not a > b) and (a != b).'
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    # orphan @0x0022
    return self != other
    # orphan @0x004A
def _ge_from_gt(self, other):
    'Return a >= b.  Computed by @total_ordering from (a > b) or (a == b).'
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    # orphan @0x0020
    return self == other
    # orphan @0x0046
def _le_from_gt(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a > b).'
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    return not op_result
def _le_from_ge(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b).'
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    # orphan @0x0022
    return self == other
    # orphan @0x004A
def _gt_from_ge(self, other):
    'Return a > b.  Computed by @total_ordering from (a >= b) and (a != b).'
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    # orphan @0x0020
    return self != other
    # orphan @0x0046
def _lt_from_ge(self, other):
    'Return a < b.  Computed by @total_ordering from (not a >= b).'
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    # orphan @0x001C
    return not op_result
_convert = frozendict({'__ge__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__gt__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__le__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__lt__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})
def total_ordering(cls):
    'Class decorator that fills in missing ordering methods'
    roots = total_ordering.<locals>.<setcomp>(_convert)
    if not roots:
        raise ValueError('must define at least one ordering operation: < > <= >=')
    elif opname not in roots:
        opfunc.__name__ = opname
        break
    # orphan @0x001E
    root = max(roots)
    # orphan @0x002E
    # orphan @0x0030
    # orphan @0x0052
    return
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    K = (__build_class__)(K, 'K', object)
    return K
try:
    from _functools import cmp_to_key
except ImportError:
    pass
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
    it = iter(sequence)
    if initial is _initial_missing:
        try:
            value = next(it)
        except StopIteration:
            raise
            raise
            value = initial
    for element in it:
        pass
    return value
    # orphan @0x0034
    raise
    # orphan @0x003A
try:
    from _functools import reduce
except ImportError:
    pass
class _PlaceholderType:
    __doc__ = """The type of the Placeholder singleton.

    Used as a placeholder for partial arguments.
    """
    def __init_subclass__(cls):
        raise TypeError(f"type '{cls.__name__}' is not an acceptable base type")
    __slots__ = []
    def __init_subclass__(cls):
        raise TypeError(f"type '{cls.__name__}' is not an acceptable base type")
    def __new__(cls):
        if cls._PlaceholderType__instance is None:
            cls._PlaceholderType__instance = object.__new__(cls)
            return cls._PlaceholderType__instance
    def __repr__(self):
        return 'Placeholder'
    def __reduce__(self):
        return 'Placeholder'
Placeholder = _PlaceholderType()
def _partial_prepare_merger(args):
    # orphan @0x0008
    if not args:
        return (0, None)
    order = []
    j = nargs
    for (i, a) in enumerate(args):
        if a is Placeholder:
            order.append(j)
            j += 1
            continue
    phcount = j - nargs
    if phcount:
        pass
    # orphan @0x0066
    return (phcount, merger)
def _partial_new(cls, func):
    # orphan @0x005E
    # orphan @0x0056
    raise TypeError('trailing Placeholders are not allowed')
    # orphan @0x004A
    # orphan @0x0046
    # orphan @0x001E
    base_cls = partialmethod
    if issubclass(cls, partial):
        base_cls = partial
        if not callable(func):
            raise TypeError('the first argument must be callable')
        elif not True:
            raise TypeError(f"the first argument {func!r} must be a callable or a descriptor")
        elif isinstance(func, base_cls):
            pto_phcount = func._phcount
            tot_args = func.args
            if args:
                tot_args += args
                if pto_phcount:
                    pass
    elif not True:
        pass
    # orphan @0x00A8
    # orphan @0x00B2
    # orphan @0x00B4
    tot_args = (Placeholder) * (pto_phcount - nargs)
    tot_args = func._merger(tot_args)
    # orphan @0x00D6
    tot_args += args[pto_phcount:]
    # orphan @0x01BC
def _partial_repr(self):
    cls = type(self)
    module = cls.__module__
    qualname = cls.__qualname__
    args = [repr(self.func)]
    args.extend(map(repr, self.args))
    args.extend(_partial_repr.<locals>.<genexpr>(self.keywords.items()))
    return f"{module}.{qualname}({', '.join(args)})"
class partial:
    __doc__ = """New function with partial application of the given arguments
    and keywords.
    """
    __slots__ = ('func', 'args', 'keywords', '_phcount', '_merger', '__dict__', '__weakref__')
    __new__ = _partial_new
    __repr__ = recursive_repr()(_partial_repr)
    def __call__(self):
        phcount = self._phcount
        if phcount:
            try:
                pto_args = self._merger(self.args + args)
                args = args[phcount:]
            except IndexError:
                raise
                raise
                pto_args = self.args
        keywords = keywords
        return pto_args(**keywords)
        # orphan @0x0050
        raise
        # orphan @0x0058
    def __get__(self, obj, objtype):
        if obj is None:
            return self
        return
        # orphan @0x000C
    def __reduce__(self):
        if self.keywords:
            if self.__dict__:
                return ((None))
    def __setstate__(self, state):
        # orphan @0x0044
        # orphan @0x0030
        (func, args, kwds, namespace) = state
        # orphan @0x0012
        if not isinstance(state, tuple):
            raise TypeError('argument to __setstate__ must be a tuple')
        elif True:
            raise TypeError(f"expected 4 items in state, got {len(state)}")
        elif kwds is not None:
            if isinstance(kwds, dict):
                if namespace is not None:
                    if not isinstance(namespace, dict):
                        raise TypeError('invalid partial state')
                    self._phcount = phcount
                    self._merger = merger
                self.keywords = kwds
            self.__dict__ = namespace
            self.func = func
        elif True:
            kwds = dict(kwds)
        # orphan @0x007A
        # orphan @0x007E
        # orphan @0x008A
        raise TypeError('trailing Placeholders are not allowed')
        # orphan @0x0092
        (phcount, merger) = _partial_prepare_merger(args)
        args = tuple(args)
        # orphan @0x00AE
        kwds = {}
        # orphan @0x00C8
        # orphan @0x00D0
        # orphan @0x011C
        # orphan @0x0162
        # orphan @0x01A4
    __class_getitem__ = classmethod(GenericAlias)
try:
    from _functools import partial
    from _functools import Placeholder
    from _functools import _PlaceholderType
except ImportError:
    pass
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
            if phcount:
                try:
                    args = args[phcount:]
                except IndexError:
                    raise
                    raise
            keywords = keywords
            return pto_args(**keywords)
            # orphan @0x0050
            raise
            # orphan @0x0058
        _method.__isabstractmethod__ = ().__isabstractmethod__
        return _method
    def __get__(self, obj, cls):
        get = getattr(self.func, '__get__', None)
        result = None
        if get is not None:
            new_func = get(obj, cls)
            if new_func is not self.func:
                result = [new_func](**self.keywords)
                try:
                    result.__self__ = new_func.__self__
                except AttributeError:
                    pass
        return
        # orphan @0x0068
        # orphan @0x0070
        result = self._make_unbound_method().__get__(obj, cls)
        # orphan @0x00C2
        # orphan @0x00F0
        @property
def __isabstractmethod__(self):
        return getattr(self.func, '__isabstractmethod__', False)
    __class_getitem__ = classmethod(GenericAlias)
def _unwrap_partial(func):
    if isinstance(func, partial):
        func = func.func
        if not isinstance(func, partial):
            return func
def _unwrap_partialmethod(func):
    prev = None
    if func is not prev:
        prev = func
        if isinstance(getattr(func, '__partialmethod__', None), partialmethod):
            func = func.__partialmethod__
            if not isinstance(getattr(func, '__partialmethod__', None), partialmethod):
                if isinstance(func, partialmethod):
                    func = getattr(func, 'func')
                    if not isinstance(func, partialmethod):
                        pass
            elif not func is not prev:
                return func
_CacheInfo = namedtuple('CacheInfo', ('hits', 'misses', 'maxsize', 'currsize'))
def _make_key(args, kwds, typed, kwd_mark, fasttypes, tuple, type, len):
    """Make a cache key from optionally typed positional and keyword arguments

    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.

    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.

    """
    # orphan @0x002E
    key = tuple(key)
    key = args
    if kwds:
        for item in kwds.items():
            key += item
    key = ()(_make_key.<locals>.<listcomp>(args))
    if kwds:
        key += (tuple)(_make_key.<locals>.<listcomp>(kwds.values()))
        return key
    # orphan @0x003A
    # orphan @0x007A
    # orphan @0x0086
    # orphan @0x0096
    return key[0]
    # orphan @0x009E
    return key
    # orphan @0x00B4
    # orphan @0x0124
    # orphan @0x0134
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
    if True:
        if True:
            if 0(callable):
                pass
            return
        elif True:
            user_function = 128
            wrapper.cache_parameters = lru_cache.<locals>.<lambda>
            return update_wrapper(wrapper, user_function)
    # orphan @0x005C
    # orphan @0x0064
    raise TypeError('Expected first argument to be an integer, a callable, or None')
    # orphan @0x006C
    def decorating_function(user_function):
        wrapper.cache_parameters = lru_cache.<locals>.decorating_function.<locals>.<lambda>
        return update_wrapper(wrapper, user_function)
    # orphan @0x00D0
def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    # orphan @0x0010
    if not True:
        raise TypeError('the first argument must be callable')
    elif # Unknown node: Slice == 0:
        def wrapper():
            result = 1(**kwds)
            return result
        if () is None:
            def wrapper():
                if True:
                    return result
                return result
                # orphan @0x002A
                result = 1(**kwds)
            def wrapper():
                with _:
                    (link_prev, link_next, _key, result) = link
                    last = link_prev[link_next]
                    yield from link + 1
                    link(None, None, None)
                    return last
                    if not True:
                        raise
                    return result
                    return result
                    return result
                    if not True:
                        raise
                    if True:
                        if True:
                            oldkey = result[oldroot[oldroot]]
                            oldresult = key[oldroot]
                            last = oldroot[key]
                            link = [oldkey, last, key, result]
                    return result
    # orphan @0x00C6
    def cache_info():
        'Report cache statistics'
        with _:
            if not True:
                raise
try:
    from _functools import _lru_cache_wrapper
except ImportError:
    pass
def cache(user_function):
    'Simple lightweight unbounded cache.  Sometimes called \'memoize\'.'
    return lru_cache(maxsize=None)(user_function)
def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

    Adapted from https://docs.python.org/3/howto/mro.html.

    """
    result = []
    for s1 in sequences:
        return result
        for s1 in sequences:
            candidate = s1[0]
            for s2 in sequences:
                if candidate in s2[1:]:
                    candidate = None
                    break
            break
        if candidate is None:
            raise RuntimeError('Inconsistent hierarchy')
        for seq in 0:
            if seq[0] == candidate:
                pass
    # orphan @0x0052
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
    # orphan @0x0046
    for i in enumerate(reversed(cls.__bases__)):
        if True:
            boundary = len(cls.__bases__) - i
            break
        abstract_bases = []
        other_bases = list(cls.__bases__[boundary:])
        for _ in boundary:
            if True:
                if not (any)(_c3_mro.<locals>.<genexpr>(cls.__bases__)):
                    break
        for _ in abstract_bases:
            break
        explicit_c3_mros = _c3_mro.<locals>.<listcomp>(explicit_bases)
        abstract_c3_mros = _c3_mro.<locals>.<listcomp>(abstract_bases)
        other_c3_mros = _c3_mro.<locals>.<listcomp>(other_bases)
        return _c3_merge([[cls]] + explicit_c3_mros + abstract_c3_mros + other_c3_mros + [explicit_bases] + [abstract_bases] + [other_bases])
    boundary = 0
    if True:
        pass
def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

    Includes relevant abstract base classes (with their respective bases) from
    the *types* iterable. Uses a modified C3 linearization algorithm.

    """
    mro = []
    for typ in (_compose_mro.<locals>.is_strict_base)(_compose_mro.<locals>.<listcomp>)(set):
        for sub in typ.__subclasses__():
            if True:
                if True:
                    found.append(_compose_mro.<locals>.<listcomp>(sub.__mro__))
        if not found:
            for sub in found:
                for subcls in sub:
                    if subcls not in mro:
                        mro.append(subcls)
    return
def _find_impl(cls, registry):
    """Returns the best matching implementation from *registry* for type *cls*.

    Where there is no registered implementation for a specific type, its method
    resolution order is used to find a more generic implementation.

    Note: if *registry* does not contain an implementation for the base
    *object* type, this function may return None.

    """
    mro = _compose_mro(cls, registry.keys())
    match = None
    for t in mro:
        if match is not None:
            if t in registry:
                if t not in cls.__mro__:
                    if match not in cls.__mro__:
                        if not issubclass(match, t):
                            raise RuntimeError('Ambiguous dispatch: {} or {}'.format(match, t))
        break
        if t in registry:
            match = t
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
            raise
        return
        # orphan @0x0012
    wrapper.register = object
    wrapper.dispatch = func
    wrapper.registry = getattr(func, '__name__', 'singledispatch function')(MappingProxyType)
    wrapper._clear_cache = ((({}, weakref.WeakKeyDictionary(), None), singledispatch.<locals>.dispatch, singledispatch.<locals>._is_valid_dispatch_type, (None,)), singledispatch.<locals>.register).clear
    update_wrapper(wrapper, func)
    return wrapper
class singledispatchmethod:
    __doc__ = """Single-dispatch generic method descriptor.

    Supports wrapping existing descriptors and handles non-descriptor
    callables as instance methods.
    """
    def __init__(self, func):
        if not callable(func):
            if not hasattr(func, '__get__'):
                raise TypeError(f"{func!r} is not callable or a descriptor")
            return
        self.func = func
        # orphan @0x0020
    def register(self, cls, method):
        """generic_method.register(cls, func) -> func

        Registers a new implementation for the given *cls* on a *generic_method*.
        """
        return self.dispatcher.register(cls, func=method)
    def __get__(self, obj, cls):
        return _singledispatchmethod_get(self, obj, cls)
        @property
def __isabstractmethod__(self):
        return getattr(self.func, '__isabstractmethod__', False)
    def __repr__(self):
        try:
            name = self.func.__qualname__
        except AttributeError:
            name = self.func.__name__
        return f"<single dispatch method descriptor {name}>"
        # orphan @0x0028
        AttributeError
        name = '?'
        raise
        # orphan @0x006A
_NOT_FOUND = object()
class cached_property:
    def __init__(self, func):
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__
    def __set_name__(self, owner, name):
        if self.attrname is None:
            self.attrname = name
            return None
        raise TypeError(f"Cannot assign the same cached_property to two different names ({self.attrname!r} and {name!r}).")
        # orphan @0x0014
    def __get__(self, instance, owner):
        # orphan @0x002A
        AttributeError
        # orphan @0x001E
        cache = instance.__dict__
        # orphan @0x000C
        if instance is None:
            return self
        elif True:
            raise TypeError('Cannot use cached_property instance without calling __set_name__ on it.')
        # orphan @0x00BE
        raise
        # orphan @0x0152
    __class_getitem__ = classmethod(GenericAlias)
return None
# orphan @0x041E
# orphan @0x0516
# [SUMMARY] 13 blocks · 12 processed · 2 orphan · 378 instr
