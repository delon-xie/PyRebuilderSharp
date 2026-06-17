# Decompiled from: <module>

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
    assigned
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
    updated
    for attr in updated:
        attr
        wrapper
        getattr
        break
    wrapper.__wrapped__ = wrapped
    return wrapper
    # orphan @0x002A
    setattr(wrapper, attr, value)
def wraps(wrapped, assigned, updated):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)
def _gt_from_lt(self, other):
    'Return a > b.  Computed by @total_ordering from (not a < b) and (a != b).'
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif not not op_result:
        self != other
def _le_from_lt(self, other):
    'Return a <= b.  Computed by @total_ordering from (a < b) or (a == b).'
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif op_result:
        return
def _ge_from_lt(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a < b).'
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result
def _ge_from_le(self, other):
    'Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b).'
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif not op_result:
        return
def _lt_from_le(self, other):
    'Return a < b.  Computed by @total_ordering from (a <= b) and (a != b).'
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif not op_result:
        self != other
def _gt_from_le(self, other):
    'Return a > b.  Computed by @total_ordering from (not a <= b).'
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result
def _lt_from_gt(self, other):
    'Return a < b.  Computed by @total_ordering from (not a > b) and (a != b).'
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif not not op_result:
        self != other
def _ge_from_gt(self, other):
    'Return a >= b.  Computed by @total_ordering from (a > b) or (a == b).'
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif op_result:
        return
def _le_from_gt(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a > b).'
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result
def _le_from_ge(self, other):
    'Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b).'
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif not op_result:
        return
def _gt_from_ge(self, other):
    'Return a > b.  Computed by @total_ordering from (a >= b) and (a != b).'
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    elif not op_result:
        self != other
def _lt_from_ge(self, other):
    'Return a < b.  Computed by @total_ordering from (not a >= b).'
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result
_convert = frozendict({'__ge__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__gt__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__le__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__lt__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})
def total_ordering(cls):
    'Class decorator that fills in missing ordering methods'
    roots = total_ordering.<locals>.<setcomp>(_convert)
    if not roots:
        raise ValueError('must define at least one ordering operation: < > <= >=')
    root = max(roots)
    _convert[root]
    for (opname, opfunc) in _convert[root]:
        if opname not in roots:
            opfunc.__name__ = opname
            break
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
    value = initial
    it
    for element in it:
        value = function(value, element)
    return value
    # orphan @0x0034
    raise
try:
    from _functools import reduce
except ImportError:
    pass
class _PlaceholderType:
    __doc__ = """The type of the Placeholder singleton.

    Used as a placeholder for partial arguments.
    """
    _PlaceholderType__instance = None
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
    if not args:
        return (0, None)
    nargs = len(args)
    order = []
    j = nargs
    enumerate(args)
    for (i, a) in enumerate(args):
        if a is Placeholder:
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
def _partial_new(cls, func):
    if issubclass(cls, partial):
        base_cls = partial
        if not callable(func):
            raise TypeError('the first argument must be callable')
        elif args and (args[-1] is Placeholder):
            raise TypeError('trailing Placeholders are not allowed')
    else:
        base_cls = partialmethod
    if not hasattr(func, '__get__'):
        raise TypeError(f"the first argument {func!r} must be a callable or a descriptor")
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
        pto_args = self.args
        keywords = keywords
        return pto_args(**keywords)
        # orphan @0x0050
        raise
    def __get__(self, obj, objtype):
        if obj is None:
            return self
        return MethodType(self, obj)
    def __reduce__(self):
        if self.keywords:
            if self.__dict__:
                return (())
            None
        else:
            None
    def __setstate__(self, state):
        if not isinstance(state, tuple):
            raise TypeError('argument to __setstate__ must be a tuple')
        elif len(state) != 4:
            raise TypeError(f"expected 4 items in state, got {len(state)}")
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
            keywords = keywords
            return pto_args(**keywords)
            # orphan @0x0050
            raise
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
        # orphan @0x0068
        result is None
        # orphan @0x0070
        result = self._make_unbound_method().__get__(obj, cls)
        # orphan @0x0080
        return result
    @property
    def __isabstractmethod__(self):
        return getattr(self.func, '__isabstractmethod__', False)
    __class_getitem__ = classmethod(GenericAlias)
def _unwrap_partial(func):
    while isinstance(func, partial):
        func = func.func
    return func
    # orphan @0x000A
    func = func.func
    isinstance(func, partial)
def _unwrap_partialmethod(func):
    prev = None
    while func is not prev:
        prev = func
        while isinstance(getattr(func, '__partialmethod__', None), partialmethod):
            func = func.__partialmethod__
        while isinstance(func, partialmethod):
            func = getattr(func, 'func')
        func = _unwrap_partial(func)
        if not func is not prev:
            return func
        while isinstance(getattr(func, '__partialmethod__', None), partialmethod):
            while isinstance(getattr(func, '__partialmethod__', None), partialmethod):
                pass
    # orphan @0x0044
    func = getattr(func, 'func')
    isinstance(func, partialmethod)
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
    elif typed:
        key += (tuple)(_make_key.<locals>.<listcomp>(args))
        if kwds:
            key += (tuple)(_make_key.<locals>.<listcomp>(kwds.values()))
        return key
    elif len(key) == 1:
        return key[0]
        return key
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
    0
    def decorating_function(user_function):
        wrapper.cache_parameters = lru_cache.<locals>.decorating_function.<locals>.<lambda>
        return update_wrapper(wrapper, user_function)
    return decorating_function
def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    if not True:
        raise TypeError('the first argument must be callable')
    elif # Unknown node: Slice == 0:
        def wrapper():
            result = 1(**kwds)
            return result
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
    for _ in sequences:
        return result
    sequences
    for s1 in sequences:
        for s2 in sequences:
            if candidate in s2[1:]:
                candidate = None
                break
        break
    if candidate is None:
        raise RuntimeError('Inconsistent hierarchy')
    result.append(candidate)
    sequences
    for seq in sequences:
        if seq[0] == candidate:
            0
            seq
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
    enumerate(reversed(cls.__bases__))
    for i in enumerate(reversed(cls.__bases__)):
        boundary = len(cls.__bases__) - i
        break
        explicit_bases = list(cls.__bases__[None:boundary])
        abstract_bases = []
        other_bases = list(cls.__bases__[boundary:])
        for _ in []:
            if not (any)(_c3_mro.<locals>.<genexpr>(cls.__bases__)):
                break
        abstract_bases
        for _ in abstract_bases:
            break
        explicit_c3_mros = _c3_mro.<locals>.<listcomp>(explicit_bases)
        abstract_c3_mros = _c3_mro.<locals>.<listcomp>(abstract_bases)
        other_c3_mros = _c3_mro.<locals>.<listcomp>(other_bases)
        return _c3_merge([[cls]] + explicit_c3_mros + abstract_c3_mros + other_c3_mros + [explicit_bases] + [abstract_bases] + [other_bases])
    boundary = 0
def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

    Includes relevant abstract base classes (with their respective bases) from
    the *types* iterable. Uses a modified C3 linearization algorithm.

    """
    mro = []
    (_compose_mro.<locals>.is_strict_base)(_compose_mro.<locals>.<listcomp>)(set)
    ((_compose_mro.<locals>.is_related)(_compose_mro.<locals>.<listcomp>))
    ()
    for typ in (_compose_mro.<locals>.is_strict_base)(_compose_mro.<locals>.<listcomp>)(set):
        for sub in typ.__subclasses__():
            found.append(_compose_mro.<locals>.<listcomp>(sub.__mro__))
        if not found:
            mro.append(typ)
        else:
            found.sort(key=len, reverse=True)
            found
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
    mro
    for t in mro:
        if match is not None:
            if (t in registry) and (t not in cls.__mro__) and (match not in cls.__mro__) and not issubclass(match, t):
                raise RuntimeError('Ambiguous dispatch: {} or {}'.format(match, t))
            break
            return registry.get(match)
        elif t in registry:
            match = t
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
        pass
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
__build_class__(_singledispatchmethod_get, '_singledispatchmethod_get')
(None,)
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
        elif name != self.attrname:
            raise TypeError(f"Cannot assign the same cached_property to two different names ({self.attrname!r} and {name!r}).")
    def __get__(self, instance, owner):
        if instance is None:
            return self
        elif self.attrname is None:
            raise TypeError('Cannot use cached_property instance without calling __set_name__ on it.')
        # orphan @0x00BE
        TypeError
        msg = f"The '__dict__' attribute on {type(instance).__name__!r} instance does not support item assignment for caching {self.attrname!r} property."
        raise TypeError(msg) from None
    __class_getitem__ = classmethod(GenericAlias)
return None
# [SUMMARY] 13 blocks · 14 processed · 3 orphan · 378 instr
