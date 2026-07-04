# Decompiled from: <module>

def _singledispatchmethod_get():
    """_singledispatchmethod_get"""
    __module__ = __name__
    __qualname__ = '_singledispatchmethod_get'
    def __init__(self, unbound, obj, cls):
        self._unbound = unbound
        self._dispatch = unbound.dispatcher.dispatch
        self._obj = obj
        self._cls = cls
        func = unbound.func
        if (obj is None) and isinstance(func, FunctionType):
            pass
        0
        try:
            self.__module__ = func.__module__
        except AttributeError:
            pass
        try:
            self.__doc__ = func.__doc__
        finally:
            pass
        0
    def __repr__(self):
        try:
            name = self.__qualname__
        except AttributeError:
            name = self.__name__
        if self._obj is not None:
            name
            '<bound single dispatch method '
        else:
            name
            '<single dispatch method '
            return f">"
    def __call__(self):
        if not args:
            funcname = getattr(self._unbound.func, '__name__', 'singledispatchmethod method')
            raise TypeError(f"{funcname} requires at least 1 positional argument")
        method = self._dispatch(args[self._dispatch_arg_index].__class__)
        if hasattr(method, '__get__'):
            skip_bound_arg = False
            if isinstance(method, staticmethod):
                skip_bound_arg = self._dispatch_arg_index == 1
            method = method.__get__(self._obj, self._cls)
            if isinstance(method, MethodType):
                skip_bound_arg = self._dispatch_arg_index == 1
            else:
                if skip_bound_arg:
                    return method(**args[1:], **kwargs)
                return method(**args, **kwargs)
        return method(**args, **kwargs)
    def __getattr__(self, name):
        if name not in ['__name__', '__qualname__', '__annotations__', '__isabstractmethod__', '__type_params__']:
            raise AttributeError
        return getattr(self._unbound.func, name)
    @property
    def __wrapped__(self):
        return self._unbound.func
    @property
    def register(self):
        return self._unbound.register
"""functools.py - Tools for working with functions and callable objects
"""
__all__ = ['update_wrapper', 'wraps', 'WRAPPER_ASSIGNMENTS', 'WRAPPER_UPDATES', 'total_ordering', 'cache', 'cmp_to_key', 'lru_cache', 'reduce', 'partial', 'partialmethod', 'singledispatch', 'singledispatchmethod', 'cached_property', 'Placeholder']
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
    updated
    wrapper.__wrapped__ = wrapped
    return wrapper
    attr
    wrapper
    getattr
    try:
        value = getattr(wrapped, attr)
    except AttributeError:
        pass
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
    """Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not not op_result and (self != other)

def _le_from_lt(self, other):
    """Return a <= b.  Computed by @total_ordering from (a < b) or (a == b)."""
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    if op_result:
        return
    return self == other

def _ge_from_lt(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a < b)."""
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result

def _ge_from_le(self, other):
    """Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b)."""
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    if not op_result:
        return
    return self == other

def _lt_from_le(self, other):
    """Return a < b.  Computed by @total_ordering from (a <= b) and (a != b)."""
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and (self != other)

def _gt_from_le(self, other):
    """Return a > b.  Computed by @total_ordering from (not a <= b)."""
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result

def _lt_from_gt(self, other):
    """Return a < b.  Computed by @total_ordering from (not a > b) and (a != b)."""
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not not op_result and (self != other)

def _ge_from_gt(self, other):
    """Return a >= b.  Computed by @total_ordering from (a > b) or (a == b)."""
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    if op_result:
        return
    return self == other

def _le_from_gt(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a > b)."""
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result

def _le_from_ge(self, other):
    """Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b)."""
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    if not op_result:
        return
    return self == other

def _gt_from_ge(self, other):
    """Return a > b.  Computed by @total_ordering from (a >= b) and (a != b)."""
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and (self != other)

def _lt_from_ge(self, other):
    """Return a < b.  Computed by @total_ordering from (not a >= b)."""
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result
_convert = frozendict({'__lt__': [('__gt__', _gt_from_lt), ('__le__', _le_from_lt), ('__ge__', _ge_from_lt)], '__le__': [('__ge__', _ge_from_le), ('__lt__', _lt_from_le), ('__gt__', _gt_from_le)], '__gt__': [('__lt__', _lt_from_gt), ('__ge__', _ge_from_gt), ('__le__', _le_from_gt)], '__ge__': [('__le__', _le_from_ge), ('__gt__', _gt_from_ge), ('__lt__', _lt_from_ge)]})

def total_ordering(cls):
    """Class decorator that fills in missing ordering methods"""
    roots = {op for op in _convert}
    if not roots:
        raise ValueError('must define at least one ordering operation: < > <= >=')
    root = max(roots)
    _convert[root]
    return cls
    if opname not in roots:
        opfunc.__name__ = opname
        setattr(cls, opname, opfunc)

def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""
    def K():
        """cmp_to_key.<locals>.K"""
        __module__ = __name__
        __qualname__ = 'cmp_to_key.<locals>.K'
        __slots__ = ['obj']
        def __init__(self, obj):
            self.obj = obj
        def __lt__(self, other):
            return self(self.obj, other.obj) < 0
        def __gt__(self, other):
            return self(self.obj, other.obj) > 0
        def __eq__(self, other):
            return self(self.obj, other.obj) == 0
        def __le__(self, other):
            return self(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return self(self.obj, other.obj) >= 0
        __hash__ = None
    K = (__build_class__)(K, 'K', object)
    return K
try:
    from _functools import cmp_to_key
except ImportError:
    pass
_initial_missing = sentinel('_initial_missing')

def reduce(function, sequence, /, initial):
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
    return value
    value = function(value, element)
try:
    from _functools import reduce
except ImportError:
    pass

class _PlaceholderType:
    """The type of the Placeholder singleton.

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
    phcount = j - nargs
    if phcount:
        pass
    else:
        None
        return (phcount, merger)
    if a is Placeholder:
        order.append(j)
        j += 1
    else:
        order.append(i)

def _partial_new(cls, func):
    if issubclass(cls, partial):
        base_cls = partial
        if not callable(func):
            raise TypeError('the first argument must be callable')
        if args and (args[-1] is Placeholder):
            raise TypeError('trailing Placeholders are not allowed')
        keywords.values()
        if isinstance(func, base_cls):
            pto_phcount = func._phcount
            tot_args = func.args
            if args:
                tot_args += args
                if pto_phcount:
                    nargs = len(args)
                    if nargs < pto_phcount:
                        tot_args += (Placeholder) * (pto_phcount - nargs)
                    tot_args = func._merger(tot_args)
                    if nargs > pto_phcount:
                        tot_args += args[pto_phcount:]
                    (phcount, merger) = _partial_prepare_merger(tot_args)
                    keywords = keywords
                    func = func.func
                    self = object.__new__(cls)
                    self.func = func
                    self.args = tot_args
                    self.keywords = keywords
                    self._phcount = phcount
                    self._merger = merger
                    return self
                (phcount, merger) = _partial_prepare_merger(tot_args)
            else:
                phcount = func._merger
                merger = pto_phcount
        else:
            tot_args = args
            (phcount, merger) = _partial_prepare_merger(tot_args)
        if value is Placeholder:
            raise TypeError('Placeholder cannot be passed as a keyword argument')
        keywords.values()
    else:
        base_cls = partialmethod

def _partial_repr(self):
    cls = type(self)
    module = cls.__module__
    qualname = cls.__qualname__
    args = [repr(self.func)]
    args.extend(map(repr, self.args))
    args.extend((<genexpr>)(self.keywords.items()))
    return f"{module}.{qualname}({', '.join(args)})"

class partial:
    """New function with partial application of the given arguments
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
                return self.func(pto_args, args, **keywords)
        pto_args = self.args
        keywords = keywords
        return self.func(pto_args, args, **keywords)

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        return MethodType(self, obj)

    def __reduce__(self):
        if self.keywords:
            if self.__dict__:
                return (())

    def __setstate__(self, state):
        if not isinstance(state, tuple):
            raise TypeError('argument to __setstate__ must be a tuple')
        if len(state) != 4:
            raise TypeError(f"expected 4 items in state, got {len(state)}")
    __class_getitem__ = classmethod(GenericAlias)
try:
    from _functools import partial, Placeholder, _PlaceholderType
except ImportError:
    pass

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
            phcount = cls_or_self._phcount
            if phcount:
                try:
                    pto_args = cls_or_self._merger(cls_or_self.args + args)
                    args = args[phcount:]
                except IndexError:
                    raise
                    raise
                    pto_args = cls_or_self.args
                    keywords = keywords
                    return cls_or_self.func(cls_or_self, pto_args, args, **keywords)
            pto_args = cls_or_self.args
            keywords = keywords
            return cls_or_self.func(cls_or_self, pto_args, args, **keywords)
        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.__partialmethod__ = self
        return _method

    def __get__(self, obj, cls):
        get = getattr(self.func, '__get__', None)
        result = None
        if get is not None:
            new_func = get(obj, cls)
            if new_func is not self.func:
                result = partial(new_func, self.args, **self.keywords)
                try:
                    result.__self__ = new_func.__self__
                except AttributeError:
                    pass
            elif result is None:
                result = self._make_unbound_method().__get__(obj, cls)
        elif result is None:
            pass

    @property
    def __isabstractmethod__(self):
        return getattr(self.func, '__isabstractmethod__', False)
    __class_getitem__ = classmethod(GenericAlias)

def _unwrap_partial(func):
    while isinstance(func, partial):
        func = func.func
    return func
    func = func.func

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
    func = getattr(func, 'func')
_CacheInfo = namedtuple('CacheInfo', ('hits', 'misses', 'maxsize', 'currsize'))

def _make_key(args, kwds, typed, kwd_mark, fasttypes, tuple, type, len):
    """Make a cache key from optionally typed positional and keyword arguments

    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.

    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.

    """
    key = args
    if kwds:
        for item in kwds.items():
            key += item
    else:
        if typed:
            key += (tuple)([v for v in args])
            if kwds:
                key += (tuple)([v for v in kwds.values()])
            return key
        if (len(key) == 1) and (type(key[0]) in fasttypes):
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
    if isinstance(maxsize, int):
        if maxsize < 0:
            maxsize
            0
        def decorating_function(user_function):
            wrapper = _lru_cache_wrapper(user_function, user_function, wrapper, _CacheInfo)
            wrapper.cache_parameters = lambda : {'maxsize': .cell, 'typed': .cell}
            return update_wrapper(wrapper, user_function)
        return decorating_function
    if callable(maxsize):
        if isinstance(typed, bool):
            user_function = 128
            wrapper = _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo)
            wrapper.cache_parameters = lambda : {'maxsize': .cell, 'typed': .cell}
            return update_wrapper(wrapper, user_function)
        if maxsize is not None:
            raise TypeError('Expected first argument to be an integer, a callable, or None')
        def decorating_function(user_function):
            wrapper = _lru_cache_wrapper(user_function, user_function, wrapper, _CacheInfo)
            wrapper.cache_parameters = lambda : {'maxsize': .cell, 'typed': .cell}
            return update_wrapper(wrapper, user_function)
        return decorating_function
    if maxsize is not None:
        pass

def _lru_cache_wrapper(user_function, maxsize, typed, _CacheInfo):
    if not callable(user_function):
        raise TypeError('the first argument must be callable')
    if maxsize == 0:
        def wrapper():
            result = kwds(**args, **kwds)
            return result
    elif maxsize is None:
        def wrapper():
            key = result(args, kwds, .cell)
            result = kwds(key, .cell)
            if result is not .cell:
                return result
            result = .cell(**args, **kwds)
            return result
    else:
        def wrapper():
            key = oldkey(args, kwds, .cell)
            oldroot
            link = link_next(key)
            with oldroot:
                link = link_next(key)
                (link_prev, link_next, _key, result) = link
                last = .cell[key]
                yield from last
                last + 1(None, None, None)
                return kwds
                yield from .cell + 1
                if not True:
                    pass
                result = .cell(*args, **kwds)
                oldroot
                with oldroot:
                    if result:
                        oldroot = .cell
                        oldkey = .cell[args]
                        oldresult = .cell[link]
                    else:
                        last = .cell[key]
                        link = [last, .cell, key, result]
                        yield from _key() >= oldresult
                        key(None, None, None)
                        return result
                    return result
                    return result
        ()
        def cache_info():
            """Report cache statistics"""
            .cell
            return
            with .cell:
                pass
        def cache_clear():
            """Clear the cache and cache statistics"""
            .cell
            .cell.clear()
            yield from False
            misses(None, None, None)
            with .cell:
                .cell.clear()
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper
try:
    from _functools import _lru_cache_wrapper
except ImportError:
    pass

def cache(user_function):
    """Simple lightweight unbounded cache.  Sometimes called "memoize"."""
    return lru_cache(maxsize=None)(user_function)

def _c3_merge(sequences):
    """Merges MROs in *sequences* to a single MRO using the C3 algorithm.

    Adapted from https://docs.python.org/3/howto/mro.html.

    """
    result = []
    sequences = [s for s in sequences]
    if not sequences:
        return result
    sequences
    if candidate is None:
        raise RuntimeError('Inconsistent hierarchy')
    result.append(candidate)
    sequences
    if seq[0] == candidate:
        0
        seq
    candidate = s1[0]
    sequences
    if candidate in s2[1:]:
        candidate = None

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
    boundary = 0
    if abcs:
        pass
    else:
        []
        explicit_bases = list(cls.__bases__[:boundary])
        abstract_bases = []
        other_bases = list(cls.__bases__[boundary:])
        abcs
        cls
        abstract_bases
        explicit_c3_mros = [base for base in explicit_bases]
        abstract_c3_mros = [base for base in abstract_bases]
        other_c3_mros = [base for base in other_bases]
        return _c3_merge([[cls]] + explicit_c3_mros + abstract_c3_mros + other_c3_mros + [explicit_bases] + [abstract_bases] + [other_bases])
        abcs.remove(base)
        if issubclass(cls, base) and not (any)((<genexpr>)(cls.__bases__)):
            abstract_bases.append(base)
    if hasattr(base, '__abstractmethods__'):
        boundary = len(cls.__bases__) - i

def _compose_mro(cls, types):
    """Calculates the method resolution order for a given class *cls*.

    Includes relevant abstract base classes (with their respective bases) from
    the *types* iterable. Uses a modified C3 linearization algorithm.

    """
    def is_related(typ):
        if typ not in typ:
            return
    def is_strict_base(typ):
        typ
        return False
        if (typ != other) and (typ in other.__mro__):
            return True
    mro = []
    types
    found
    set(types)
    sub
    [n for n in types]
    (typ)
    _compose_mro.<locals>.is_strict_base
    (sub)
    [n for n in types]
    (mro)
    _compose_mro.<locals>.is_related
    (set(cls.__mro__), cls)
    return _c3_mro(cls, abcs=mro)
    found = []
    typ.__subclasses__()
    if not found:
        mro.append(typ)
    else:
        found.sort(key=len, reverse=True)
        found
        sub
        if subcls not in mro:
            mro.append(subcls)
    if (sub not in bases) and issubclass(cls, sub):
        (found.append)([s for s in sub.__mro__])

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
    return registry.get(match)
    if match is not None:
        if (t in registry) and (t not in cls.__mro__) and (match not in cls.__mro__) and not issubclass(match, t):
            raise RuntimeError('Ambiguous dispatch: {} or {}'.format(match, t))
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
    def dispatch(cls):
        """generic_func.dispatch(cls) -> <function implementation>

        Runs the dispatch algorithm to return the best available implementation
        for the given *cls* registered on *generic_func*.

        """
        if cls is not None:
            current_token = get_cache_token()
            if cls != current_token:
                current_token.clear()
                cls
                current_token
            try:
                impl = current_token[cls]
            except KeyError:
                impl = impl[cls]
            return impl
            return impl
        impl = current_token[cls]
        return impl
    def _is_valid_dispatch_type(cls):
        if isinstance(cls, type):
            return True
        if not isinstance(cls, UnionType):
            all((arg for arg in cls.__args__))
    def register(cls, func):
        """generic_func.register(cls, func) -> func

        Registers a new implementation for the given *cls* on a *generic_func*.

        """
        if func(cls):
            if func is None:
                return lambda f: .cell(f, f)
            if isinstance(cls, UnionType):
                for arg in cls.__args__:
                    pass
            else:
                cls
                ForwardRef
                func
                if ann is None:
                    if hasattr(cls, '__abstractmethods__'):
                        ann
                        get_cache_token()
                    get_type_hints.clear()
                    return func
                get_type_hints.clear()
                return func
        elif func is not None:
            raise TypeError(f"Invalid first argument to `register()`. {cls!r} is not a class or union type.")
    import weakref
    def wrapper():
        if not args:
            raise TypeError(f"{kw} requires at least 1 positional argument")
        return args(args[0].__class__)(**args, **kw)
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
        if self.attrname is None:
            raise TypeError('Cannot use cached_property instance without calling __set_name__ on it.')
        cache = instance.__dict__
    __class_getitem__ = classmethod(GenericAlias)
