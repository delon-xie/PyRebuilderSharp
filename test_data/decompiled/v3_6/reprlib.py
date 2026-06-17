# Decompiled from: <module>

'Redo the builtin repr() (representation) but with limits on most sizes.'
__all__ = ['Repr', 'repr', 'recursive_repr']
import builtins
from itertools import islice
from _thread import get_ident
def recursive_repr(fillvalue):
    'Decorator to make a repr function return fillvalue for a recursive call'
    def decorating_function(user_function):
        def wrapper(self):
            key = (id(self), get_ident())
            if True:
                return
            return result
            # orphan @0x001A
        wrapper.__module__ = (set())(getattr, '__module__')
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
            method = getattr(self, 'repr_' + typename, None)
            if method:
                pass
        elif True:
            return method(x, level)
        # orphan @0x0050
        module = getattr(cls, '__module__', None)
        # orphan @0x006A
        return method(x, level)
        # orphan @0x0074
        return self.repr_instance(x, level)
        # orphan @0x00DE
    def _join(self, pieces, level):
        # orphan @0x001C
        # orphan @0x0018
        return ''
        # orphan @0x0014
        if self.indent is None:
            return ', '.join(pieces)
        elif isinstance(indent, int):
            if indent < 0:
                raise ValueError(f"Repr.indent cannot be negative int (was {indent!r})")
            raise TypeError(f"Repr.indent must be a str, int or None, not {type(indent)}") from error
            error = None
            if -len(indent):
                return
        # orphan @0x0044
        indent = ' '
        sep = """,
""" + (self.maxlevel - level + 1) * indent
        # orphan @0x0068
        # orphan @0x0070
        # orphan @0x010C
    def _repr_iterable(self, x, level, left, right, maxiter, trail):
        n = len(x)
        if level <= 0:
            if n:
                s = self.fillvalue
            pieces = Repr._repr_iterable.<locals>.<listcomp>(islice(x, maxiter))
            if n > maxiter:
                pieces.append(self.fillvalue)
                s = self._join(pieces, level)
                if n == 1:
                    if trail:
                        if self.indent is None:
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
        return self._repr_iterable(x, level, header, '])', self.maxarray)
        # orphan @0x000E
    def repr_set(self, x, level):
        # orphan @0x0008
        if not x:
            return 'set()'
        return self._repr_iterable(x, level, '{', '}', self.maxset)
    def repr_frozenset(self, x, level):
        # orphan @0x0008
        if not x:
            return 'frozenset()'
        return self._repr_iterable(x, level, 'frozenset({', '})', self.maxfrozenset)
    def repr_deque(self, x, level):
        return self._repr_iterable(x, level, 'deque([', '])', self.maxdeque)
    def repr_dict(self, x, level):
        # orphan @0x001C
        # orphan @0x0014
        n = len(x)
        if n == 0:
            return '{}'
        return '}'
        newlevel = level - 1
        repr1 = self.repr1
        pieces = []
        for key in _possibly_sorted(x):
            keyrepr = repr1(key, newlevel)
            valrepr = repr1(x[key], newlevel)
            pieces.append('%s: %s' % (keyrepr, valrepr))
        if n > self.maxdict:
            pieces.append(self.fillvalue)
            s = self._join(pieces, level)
            return '{%s}' % (s)
    def repr_str(self, x, level):
        s = builtins.repr(x[None:self.maxstring])
        if len(s) > self.maxstring:
            i = max(0, (self.maxstring - 3) // 2)
            j = max(0, self.maxstring - 3 - i)
            s = builtins.repr(x[None:i] + x[len(x) - j:])
            s = s[None:i] + self.fillvalue + s[len(s) - j:]
            return s
    def repr_int(self, x, level):
        # orphan @0x0030
        import math
        import sys
        k = 1 + int(math.log10(abs(x)))
        # orphan @0x002C
        raise AssertionError
        # orphan @0x0018
        # orphan @0x0010
        try:
            s = builtins.repr(x)
        except ValueError:
            j = max(0, self.maxlong - 3 - i)
            s = s[None:i] + self.fillvalue + s[len(s) - j:]
            return s
        if len(s) > self.maxlong:
            pass
        # orphan @0x005C
        return f"{x.__class__.__name__} instance with roughly {k} digits (limit at {max_digits}) at 0x{id(x)}{'x'}>"
        # orphan @0x0086
        exc = None
        # orphan @0x00A8
        j = max(0, self.maxlong - 3 - i)
        s = s[None:i] + self.fillvalue + s[len(s) - j:]
        return s
    def repr_instance(self, x, level):
        # orphan @0x0018
        return '<%s instance at %#x>' % (x.__class__.__name__, id(x))
        # orphan @0x0010
        try:
            s = builtins.repr(x)
        except Exception:
            j = max(0, self.maxother - 3 - i)
            s = s[None:i] + self.fillvalue + s[len(s) - j:]
            return s
            return '<%s instance at %#x>' % (x.__class__.__name__, id(x))
        if len(s) > self.maxother:
            pass
        # orphan @0x0032
        # orphan @0x004A
        j = max(0, self.maxother - 3 - i)
        s = s[None:i] + self.fillvalue + s[len(s) - j:]
        return s
def _possibly_sorted(x):
    try:
        return sorted(x)
    except Exception:
        return list(x)
    if True:
        return list(x)
aRepr = Repr()
repr = aRepr.repr
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 47 instr
