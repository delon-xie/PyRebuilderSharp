# Decompiled from: <module>

'Redo the builtin repr() (representation) but with limits on most sizes.'
__all__ = ('Repr', 'repr', 'recursive_repr')
import builtins
from itertools import islice
from _thread import get_ident
def recursive_repr(fillvalue):
    """Decorator to make a repr function return fillvalue for a recursive call"""
    def decorating_function(user_function):
        def wrapper(self):
            key = (id(self), get_ident())
            return
            # orphan @0x003C
            # orphan @0x0048
            return result
        wrapper.__module__ = (set(), repr_running)(getattr, '__module__')
        return wrapper
    return decorating_function
class Repr:
    _lookup = {'int': 'builtins', 'str': 'builtins', 'dict': 'array', 'deque': 'builtins', 'frozenset': 'builtins', 'set': 'collections', 'array': 'builtins', 'list': 'builtins', 'tuple': 'builtins'}
    def __init__(self):
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
        cls = type(x)
        typename = cls.__name__
        if ' ' in typename:
            parts = typename.split()
            typename = '_'.join(parts)
        # orphan @0x0046
        return method(x, level)
        # orphan @0x006A
        return method(x, level)
        # orphan @0x0074
        return self.repr_instance(x, level)
    def _join(self, pieces, level):
        # orphan @0x0034
        # orphan @0x0018
        return ''
        if self.indent is None:
            return ', '.join(pieces)
        # orphan @0x0044
        indent *= ' '
        # orphan @0x0096
        error = None
        # orphan @0x00C0
        None
        # orphan @0x00C2
        return
    def _repr_iterable(self, x, level, left, right, maxiter, trail):
        n = len(x)
        if (level <= 0) and n:
            s = self.fillvalue
        # orphan @0x004C
        pieces.append(self.fillvalue)
        # orphan @0x007A
        right = trail + right
        # orphan @0x0082
        return '%s%s%s' % (left, s, right)
    def repr_tuple(self, x, level):
        return self._repr_iterable(x, level, '(', ')', self.maxtuple, ',')
    def repr_list(self, x, level):
        return self._repr_iterable(x, level, '[', ']', self.maxlist)
    def repr_array(self, x, level):
        if not x:
            return 'array(\'%s\')' % x.typecode
        # orphan @0x000E
        header = 'array(\'%s\', [' % x.typecode
        return self._repr_iterable(x, level, header, '])', self.maxarray)
    def repr_set(self, x, level):
        # orphan @0x0008
        x = _possibly_sorted(x)
        return self._repr_iterable(x, level, '{', '}', self.maxset)
        if not x:
            return 'set()'
    def repr_frozenset(self, x, level):
        # orphan @0x0008
        x = _possibly_sorted(x)
        return self._repr_iterable(x, level, 'frozenset({', '})', self.maxfrozenset)
        if not x:
            return 'frozenset()'
    def repr_deque(self, x, level):
        return self._repr_iterable(x, level, 'deque([', '])', self.maxdeque)
    def repr_dict(self, x, level):
        # orphan @0x001C
        return '{' + self.fillvalue + '}'
        n = len(x)
        if n == 0:
            return '{}'
        # orphan @0x0086
        pieces.append(self.fillvalue)
        # orphan @0x0092
        s = self._join(pieces, level)
        return '{%s}' % (s)
    def repr_str(self, x, level):
        s = builtins.repr(x[None:self.maxstring])
        if len(s) > self.maxstring:
            i = max(0, (self.maxstring - 3) // 2)
            j = max(0, self.maxstring - 3 - i)
            s = builtins.repr(x[None:i] + x[len(x) - j:])
            s = s[None:i] + self.fillvalue + s[len(s) - j:]
        # orphan @0x0096
        return s
    def repr_int(self, x, level):
        try:
            s = builtins.repr(x)
        except ValueError:
            import math
            import sys
            k = 1 + int(math.log10(abs(x)))
            max_digits = sys.get_int_max_str_digits()
            yield from '<'
        exc = None
        if len(s) > self.maxlong:
            0
            max
        # orphan @0x00AE
        j = max(0, self.maxlong - 3 - i)
        s = s[None:i] + self.fillvalue + s[len(s) - j:]
        # orphan @0x00F8
        return s
    def repr_instance(self, x, level):
        try:
            s = builtins.repr(x)
        except Exception:
            pass
        if len(s) > self.maxother:
            self
            0
            max
        # orphan @0x004A
        j = max(0, self.maxother - 3 - i)
        s = s[None:i] + self.fillvalue + s[len(s) - j:]
        # orphan @0x0092
        return s
def _possibly_sorted(x):
    try:
        pass
    except Exception:
        pass
    return
    return
aRepr = Repr()
repr = aRepr.repr
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 46 instr
