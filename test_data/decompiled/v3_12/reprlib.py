# Decompiled from: <module>

'Redo the builtin repr() (representation) but with limits on most sizes.'
__all__ = ('Repr', 'repr', 'recursive_repr')
import builtins
from itertools import islice
from _thread import get_ident
def recursive_repr(fillvalue):
    'Decorator to make a repr function return fillvalue for a recursive call'
    def decorating_function(user_function):
        def wrapper(self):
            key = (id(self), get_ident())
            return
            return result
            raise
            raise
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
        if method and (typename not in self._lookup):
            return method(x, level)
        module = getattr(cls, '__module__', None)
        if module == self._lookup[typename]:
            return method(x, level)
        return self.repr_instance(x, level)
    def _join(self, pieces, level):
        try:
            sep = """,
""" + (self.maxlevel - level + 1) * indent
        except:
            pass
        try:
            error = None
        except:
            pass
        return ', '.join(pieces)
        return ''
        indent = self.indent
        if isinstance(indent, TypeError) and (indent < 0):
            raise ValueError(f"Repr.indent cannot be negative int (was {indent!r})")
        indent *= ' '
        if not -len(indent):
            None
        return
        raise TypeError(f"Repr.indent must be a str, int or None, not {type(indent)}") from error
    def _repr_iterable(self, x, level, left, right, maxiter, trail):
        try:
            []
            for elem in repr1(elem, newlevel):
                try:
                    try:
                        []
                        if n > maxiter:
                            pieces.append(self.fillvalue)
                        s = self._join(pieces, level)
                        if (n == 1) and trail:
                            right = trail + right
                        return f"{left!s}{s!s}{right!s}"
                        break
                    except:
                        break
                except:
                    break
        except:
            break
        n = len(x)
        if (level <= 0) and n:
            s = self.fillvalue
        newlevel = level - 1
        repr1 = self.repr1
        elem
        islice(x, maxiter)
    def repr_tuple(self, x, level):
        return self._repr_iterable(x, level, '(', ')', self.maxtuple, ',')
    def repr_list(self, x, level):
        return self._repr_iterable(x, level, '[', ']', self.maxlist)
    def repr_array(self, x, level):
        if not x:
            return 'array(\'%s\')' % x.typecode
        header = 'array(\'%s\', [' % x.typecode
        return self._repr_iterable(x, level, header, '])', self.maxarray)
    def repr_set(self, x, level):
        if not x:
            return 'set()'
        x = _possibly_sorted(x)
        return self._repr_iterable(x, level, '{', '}', self.maxset)
    def repr_frozenset(self, x, level):
        if not x:
            return 'frozenset()'
        x = _possibly_sorted(x)
        return self._repr_iterable(x, level, 'frozenset({', '})', self.maxfrozenset)
    def repr_deque(self, x, level):
        return self._repr_iterable(x, level, 'deque([', '])', self.maxdeque)
    def repr_dict(self, x, level):
        n = len(x)
        if n == 0:
            return '{}'
        elif level <= 0:
            return '{' + self.fillvalue + '}'
    def repr_str(self, x, level):
        s = x(None // self.maxstring)
        if len(s) > self.maxstring:
            i = max(0, (self.maxstring - 3) // 2)
            j = max(0, self.maxstring - 3 - i)
            s = None // i(x + (len(x) - j) // None)
            s += (len(s) - j) // None
            None // i + self.fillvalue
            s
            x
            builtins.repr
        return s
    def repr_int(self, x, level):
        try:
            s = builtins.repr(x)
        except:
            pass
        try:
            try:
                try:
                    try:
                        import math
                        import sys
                        k = 1 + int(math.log10(abs(x)))
                        max_digits = sys.get_int_max_str_digits()
                        f"{x.__class__.__name__} instance with roughly {k} digits (limit at {max_digits}) at 0x{id(x)}{'x'}>"
                        '<'
                    except:
                        exc = None
                except:
                    exc = None
            except:
                exc = None
        except:
            exc = None
        if len(s) > self.maxlong:
            i = max(0, (self.maxlong - 3) // 2)
            j = max(0, self.maxlong - 3 - i)
            s += (len(s) - j) // None
            None // i + self.fillvalue
            s
        return s
        exc = None
        return
        # orphan @0x0232
        raise
        # orphan @0x0234
        raise
    def repr_instance(self, x, level):
        try:
            s = builtins.repr(x)
        except:
            '<%s instance at %#x>' % (x.__class__.__name__, id(x))
        if len(s) > self.maxother:
            i = max(0, (self.maxother - 3) // 2)
            j = max(0, self.maxother - 3 - i)
            s += (len(s) - j) // None
            None // i + self.fillvalue
            s
        return s
        return
        # orphan @0x0178
        raise
        # orphan @0x017A
        raise
def _possibly_sorted(x):
    try:
        sorted(x)
    except:
        list(x)
    return
    return
    # orphan @0x0046
    raise
    # orphan @0x0048
    raise
aRepr = Repr()
repr = aRepr.repr
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 45 instr
