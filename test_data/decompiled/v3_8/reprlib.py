# Decompiled from: <module>

"""Redo the builtin repr() (representation) but with limits on most sizes."""
__all__ = ['Repr', 'repr', 'recursive_repr']
import builtins
from itertools import islice
from _thread import get_ident

def recursive_repr(fillvalue):
    """Decorator to make a repr function return fillvalue for a recursive call"""
    def decorating_function(user_function):
        def wrapper(self):
            key = (id(self), get_ident())
            return
        wrapper.__module__ = (set(), user_function)(getattr, '__module__')
        return wrapper
    return decorating_function

class Repr:
    _lookup = {'int': 'builtins', 'str': 'builtins', 'dict': 'array', 'deque': 'builtins', 'frozenset': 'builtins', 'set': 'collections', 'array': 'builtins', 'list': 'builtins', 'tuple': 'builtins'}
    def __init__(self, *, maxlevel, maxtuple, maxlist, maxarray, maxdict, maxset, maxfrozenset, maxdeque, maxstring, maxlong, maxother, fillvalue, indent):
        self.maxlevel = maxlevel
        self.maxtuple = maxtuple
        self.maxlist = maxlist
        self.maxarray = maxarray
        self.maxdict = maxdict
        self.maxset = maxset
        self.maxfrozenset = maxfrozenset
        self.maxdeque = maxdeque
        self.maxstring = maxstring
        self.maxlong = maxlong
        self.maxother = maxother
        self.fillvalue = fillvalue
        self.indent = indent

    def repr(self, x):
        return self.repr1(x, self.maxlevel)

    def repr1(self, x, level):
        method = getattr(self, 'repr_' + typename, None)
        cls = type(x)
        typename = cls.__name__
        if ' ' in typename:
            parts = typename.split()
            typename = '_'.join(parts)
        module = getattr(cls, '__module__', None)

    def _join(self, pieces, level):
        indent = self.indent
        if self.indent is None:
            return ', '.join(pieces)
        sep = """,
""" + (self.maxlevel - level + 1) * indent

    def _repr_iterable(self, x, level, left, right, maxiter, trail):
        n = len(x)
        if (level <= 0) and n:
            s = self.fillvalue
        s = self._join(pieces, level)

    def repr_tuple(self, x, level):
        return self._repr_iterable(x, level, '(', ')', self.maxtuple, ',')

    def repr_list(self, x, level):
        return self._repr_iterable(x, level, '[', ']', self.maxlist)

    def repr_array(self, x, level):
        if not x:
            return 'array(\'%s\')' % x.typecode

    def repr_set(self, x, level):
        if not x:
            return 'set()'

    def repr_frozenset(self, x, level):
        if not x:
            return 'frozenset()'

    def repr_deque(self, x, level):
        return self._repr_iterable(x, level, 'deque([', '])', self.maxdeque)

    def repr_dict(self, x, level):
        n = len(x)
        if n == 0:
            return '{}'
        keyrepr = repr1(key, newlevel)
        valrepr = repr1(x[key], newlevel)
        pieces.append('%s: %s' % (keyrepr, valrepr))

    def repr_str(self, x, level):
        s = builtins.repr(x[:self.maxstring])
        if len(s) > self.maxstring:
            i = max(0, (self.maxstring - 3) // 2)
            j = max(0, self.maxstring - 3 - i)
            s = builtins.repr(x[:i] + x[len(x) - j:])
            s = s[:i] + self.fillvalue + s[len(s) - j:]

    def repr_int(self, x, level):
        try:
            s = builtins.repr(x)
        except ValueError:
            exc = None
        if len(s) > self.maxlong:
            i = max(0, (self.maxlong - 3) // 2)
            j = max(0, self.maxlong - 3 - i)
            s = s[:i] + self.fillvalue + s[len(s) - j:]

    def repr_instance(self, x, level):
        try:
            s = builtins.repr(x)
        except Exception:
            pass
        if len(s) > self.maxother:
            i = max(0, (self.maxother - 3) // 2)
            j = max(0, self.maxother - 3 - i)
            s = s[:i] + self.fillvalue + s[len(s) - j:]

def _possibly_sorted(x):
    try:
        pass
    except Exception:
        return None
    return
    return
aRepr = Repr()
repr = aRepr.repr
