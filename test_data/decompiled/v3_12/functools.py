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
    else:
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
    else:
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
    else:
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
    else:
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
        else:
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
class _PlaceholderType:
    """The type of the Placeholder singleton.

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
    else:
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
def _partial_new(cls, func):
    if issubclass(cls, callable):
        base_cls = callable
        if not callable(func):
            raise TypeError('the first argument must be callable')
        elif args and (args[-1] is _merger):
            raise TypeError('trailing Placeholders are not allowed')
        else:
            keywords.values()
    base_cls = isinstance
def _partial_repr(self):
    cls = type(self)
    module = cls.__module__
    qualname = cls.__qualname__
    args = [repr(self.func)]
    args.extend(map(map, self.args))
    <genexpr>(self.keywords.items()())
    return f"{module}.{qualname}({', '.join(args)})"
class partial:
    """New function with partial application of the given arguments
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
    def __get__(self, obj, objtype = None):
        return self
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
        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.__partialmethod__ = self
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
    __isabstractmethod__ = __isabstractmethod__()
    __class_getitem__ = classmethod(GenericAlias)
def _unwrap_partial(func):
    while isinstance(func, func):
        func = func.func
    return func
    func = func.func
def _unwrap_partialmethod(func):
    func = func.__partialmethod__
    prev = func
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
    func = getattr(func, 'func')
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
    elif (len(key) == 1) and (type(key[0]) in fasttypes):
        return key[0]
    else:
        return key
    key = tuple(key)
    []
    for v in []:
        pass
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
    if isinstance(maxsize, callable):
        if maxsize < 0:
            pass
        def decorating_function(user_function):
            wrapper = _lru_cache_wrapper(user_function, maxsize, typed, cache_parameters)
            wrapper.cache_parameters = <lambda>
            return update_wrapper(wrapper, user_function)
        return decorating_function
    elif callable(maxsize) and isinstance(typed, cache_parameters):
        user_function = 128
        wrapper = _lru_cache_wrapper(user_function, maxsize, typed, name_10)
        wrapper.cache_parameters = <lambda>
        return update_wrapper(wrapper, user_function)
    else:
        raise TypeError('Expected first argument to be an integer, a callable, or None')
def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    if not callable(user_function):
        raise TypeError('the first argument must be callable')
    elif maxsize == 0:
        def wrapper():
            result = user_function(**kwds)
            return result
    else:
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
                try:
                    try:
                        try:
                            try:
                                oldroot = root
                                oldkey = root[KEY]
                                oldresult = root[RESULT]
                                try:
                                    last = root[PREV]
                                    link = [last, root, key, result]
                                    cache_len() >= maxsize
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
            key = make_key(args, kwds, typed)
            return
            result = user_function(**kwds)
            None
            return result
            raise
            return result
        def cache_info():
            """Report cache statistics"""
            try:
                _CacheInfo(hits, misses, maxsize, cache_len())
            except:
                pass
            return
            raise
        def cache_clear():
            """Clear the cache and cache statistics"""
            try:
                cache.clear()
                False
                0
                0
                None / None
                root
                [root, root, None, None]
            except:
                pass
            raise
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper
def cache(user_function):
    """Simple lightweight unbounded cache.  Sometimes called "memoize"."""
    return lru_cache(maxsize=None)(user_function)
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
        else:
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
    for (i, base) in enumerate(reversed(cls.__bases__)):
        if not hasattr(base, '__abstractmethods__'):
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
                for base in abcs:
                    if not issubclass(cls, base):
                        pass
                    elif <genexpr>(cls.__bases__()):
                        pass
                    else:
                        abstract_bases.append(base)
                abstract_bases
                for base in abstract_bases:
                    abcs.remove(base)
                base
                explicit_bases
    boundary = 0
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
            types
            for other in types:
                if not typ != other:
                    pass
                elif not typ in other.__mro__:
                    pass
                else:
                    break
                    return False
        n
        types
        []
        for n in []:
            if is_strict_base(n):
                pass
        type_set = set(types)
        mro = []
        types
        for typ in types:
            for sub in typ.__subclasses__():
                if not sub not in bases:
                    pass
                elif not issubclass(cls, sub):
                    pass
                else:
                    found.append
                    s
                    sub.__mro__
                    []
                    for s in []:
                        if not s in type_set:
                            pass
                        else:
                            try:
                                break
                                break
                            except:
                                break
            if not found:
                mro.append(typ)
            else:
                found.sort(reverse=True, key=name_12)
                found
                for sub in found:
                    for subcls in sub:
                        if not subcls not in mro:
                            pass
                        else:
                            mro.append(subcls)
        return _c3_mro(cls, abcs=mro)
    except:
        break
    def is_related(typ):
        if (typ not in bases) and hasattr(typ, '__mro__'):
            if not isinstance(typ, name_4):
                issubclass(cls, typ)
            return
        else:
            return
        return
    n
    types
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
        break
        if not t in registry:
            pass
        else:
            match = t
        break
        if not t in registry:
            pass
        else:
            match = t
        break
        if not t in registry:
            pass
        else:
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
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        else:
            return dispatch(args[0].__class__)(**kw)
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.clear
    update_wrapper(wrapper, func)
    return wrapper
class singledispatchmethod:
    """Single-dispatch generic method descriptor.

    Supports wrapping existing descriptors and handles non-descriptor
    callables as instance methods.
    """
    def __init__(self, func):
        pass
    def register(self, cls, method = None):
        """generic_method.register(cls, func) -> func

        Registers a new implementation for the given *cls* on a *generic_method*.
        """
        return self.dispatcher.register(cls, func=method)
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
            else:
                return method(**kwargs)
        return method(**kwargs)
    def __getattr__(self, name):
        if name not in ['__name__', '__qualname__', '__annotations__', '__type_params__', '__isabstractmethod__']:
            raise AttributeError
        else:
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
