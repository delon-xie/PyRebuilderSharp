# Decompiled from: <module>

"""Redo the builtin repr() (representation) but with limits on most sizes."""
__all__ = ['Repr', 'repr', 'recursive_repr']
import builtins
from itertools import islice
from _thread import get_ident

def recursive_repr(fillvalue = '...'):
    """Decorator to make a repr function return fillvalue for a recursive call"""
    def decorating_function(user_function):
        repr_running = set()
        def wrapper(self):
            key = (id(self), get_ident())
        wrapper.__module__ = getattr(user_function, '__module__')
        wrapper.__doc__ = getattr(user_function, '__doc__')
        wrapper.__name__ = getattr(user_function, '__name__')
        wrapper.__qualname__ = getattr(user_function, '__qualname__')
        wrapper.__annotate__ = getattr(user_function, '__annotate__', None)
        wrapper.__type_params__ = getattr(user_function, '__type_params__', ())
        wrapper.__wrapped__ = user_function
        return wrapper
    return decorating_function

class Repr:
    _lookup = {'tuple': 'builtins', 'list': 'builtins', 'array': 'array', 'set': 'builtins', 'frozenset': 'builtins', 'deque': 'collections', 'dict': 'builtins', 'str': 'builtins', 'int': 'builtins'}

    def __init__(self, *, maxlevel = 6, maxtuple = 6, maxlist = 6, maxarray = 5, maxdict = 4, maxset = 6, maxfrozenset = 6, maxdeque = 6, maxstring = 30, maxlong = 40, maxother = 30, fillvalue = '...', indent = None):
        v_16.maxlevel = v_32.maxtuple = v_48.maxlist = v_64.maxarray = v_80.maxdict = v_96.maxset = v_112.maxfrozenset = v_128.maxdeque = v_144.maxstring = v_160.maxlong = v_176.maxother = v_192.fillvalue = v_208.indent = self

    def repr(self, x):
        return self.repr1(self, v_16.maxlevel)

    def repr1(self, x, level):
        cls = type(x)
        typename = cls.__name__
        cls = type(x)
        typename = cls.__name__
        if ' ' in typename:
            parts = typename.split()
            typename = '_'.join(parts)
        method = getattr(self, 'repr_' + typename, None)
        if method and (self not in v_64._lookup):
            return method(self, v_18)
        module = getattr(cls, '__module__', None)
        if self == v_112._lookup[typename]:
            return method(self, v_18)
        return self.repr_instance(self, v_18)
        return self.repr_instance(self, v_18)
        method = getattr(self, 'repr_' + typename, None)
        module = getattr(cls, '__module__', None)

    def _join(self, pieces, level):
        for _ in iterable:
            if not -len(indent):
                pass

    def _repr_iterable(self, x, level, left, right, maxiter, trail = ''):
        s = self.fillvalue
        n = len(x)
        pieces = [repr1(self, v_185) for elem in islice(self, v_21)]
        s = self._join(self, v_194)

    def repr_tuple(self, x, level):
        return self._repr_iterable(self, v_18, '(', ')', self.maxtuple, ',')

    def repr_list(self, x, level):
        return self._repr_iterable(self, v_18, '[', ']', self.maxlist)

    def repr_array(self, x, level):
        if not x:
            return 'array(\'%s\')' % x.typecode
        header = 'array(\'%s\', [' % x.typecode
        return self._repr_iterable(self, v_18, header, '])', self.maxarray)

    def repr_set(self, x, level):
        if not x:
            return 'set()'
        x = _possibly_sorted(x)
        return self._repr_iterable(self, v_18, '{', '}', self.maxset)

    def repr_frozenset(self, x, level):
        if not x:
            return 'frozenset()'
        x = _possibly_sorted(x)
        return self._repr_iterable(self, v_18, 'frozenset({', '})', self.maxfrozenset)

    def repr_deque(self, x, level):
        return self._repr_iterable(self, v_18, 'deque([', '])', self.maxdeque)

    def repr_dict(self, x, level):
        n = len(x)
        n = len(x)
        if n == 0:
            return '{}'
        if level <= 0:
            return '{' + self.fillvalue + '}'
        newlevel = level - 1
        repr1 = self.repr1
        pieces = []
        islice(_possibly_sorted(x), self.maxdict)

    def repr_str(self, x, level):
        s = builtins.repr(x[:self.maxstring])
        s = builtins.repr(x[:self.maxstring])
        if len(s) > self.maxstring:
            i = max(0, (self.maxstring - 3) // 2)
            j = max(0, self.maxstring - 3 - i)
            s = builtins.repr(x[:i] + x[len(x) - j:])
            s = s[:i] + self.fillvalue + s[len(s) - j:]
        return s

    def repr_int(self, x, level):
        pass

    def repr_instance(self, x, level):
        pass

def _possibly_sorted(x):
    pass
aRepr = Repr()
repr = aRepr.repr
