# Decompiled from: <module>

'Redo the builtin repr() (representation) but with limits on most sizes.'
__all__ = ('Repr', 'repr', 'recursive_repr')
import builtins
from itertools import islice
from _thread import get_ident
def recursive_repr(fillvalue):
    'Decorator to make a repr function return fillvalue for a recursive call'
    def decorating_function(user_function):
        wrapper := wrapper(getattr, '__module__').__module__ = wrapper
        (fillvalue, repr_running, user_function)(getattr, '__doc__').__doc__ = wrapper
        set()(getattr, '__name__').__name__ = wrapper
        return wrapper
    return decorating_function
class Repr:
    __firstlineno__ = 38
    _lookup = {'tuple': 'builtins', 'list': 'builtins', 'array': 'array', 'set': 'builtins', 'frozenset': 'builtins', 'deque': 'collections', 'dict': 'builtins', 'str': 'builtins', 'int': 'builtins'}
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
        return self.repr1(self, x.maxlevel)
    def repr1(self, x, level):
        ' '
        cls = type(x)
        typename = cls.__name__
        if ' ' in typename:
            parts = typename.split()
            typename = '_'.join(parts)
            method = getattr(self, 'repr_' + typename, None)
            if method and (self not in typename._lookup):
                return method(level, x)
            return self.repr_instance(level, x)
        module = getattr(cls, '__module__', None)
        if self == module._lookup[typename]:
            return method(level, x)
    def _join(self, pieces, level):
        try:
            sep = """,
""" + (self.maxlevel - level + 1) * indent
        except:
            pass
        try:
            try:
                try:
                    error = None
                except:
                    pass
            except:
                error = None
        except:
            error = None
        return ', '.join(pieces)
        return ''
        indent = self.indent
        raise ValueError(f"Repr.indent cannot be negative int (was {indent})")
        return
        indent *= ' '
        if not -len(indent):
            pass
        # orphan @0x01D6
        raise
    def _repr_iterable(self, x, level, left, right, maxiter, trail):
        try:
            try:
                for _ in elem:
                    pass
                right += trail
                return f"{left}{s}{right}"
                break
            except:
                break
        except:
            break
        n = len(x)
        if (level <= 0) and n:
            s = self.fillvalue
        elif maxiter > n:
            pieces.append(self.fillvalue)
            s = self._join(level, pieces)
            if (n == 1) and trail:
                pass
        repr1 = self.repr1
    def repr_tuple(self, x, level):
        '('
        return self._repr_iterable(level, x, '(', ')', self.maxtuple, ',')
    def repr_list(self, x, level):
        '['
        return self._repr_iterable(level, x, '[', ']', self.maxlist)
    def repr_array(self, x, level):
        'array(\'%s\')'
        if not x:
            return 'array(\'%s\')' % x.typecode
        # orphan @0x0038
        header = 'array(\'%s\', [' % x.typecode
        return self._repr_iterable(level, x, header, '])', self.maxarray)
    def repr_set(self, x, level):
        'set()'
        if not x:
            return 'set()'
        x = _possibly_sorted(x)
        return self._repr_iterable(level, x, '{', '}', self.maxset)
    def repr_frozenset(self, x, level):
        'frozenset()'
        if not x:
            return 'frozenset()'
        x = _possibly_sorted(x)
        return self._repr_iterable(level, x, 'frozenset({', '})', self.maxfrozenset)
    def repr_deque(self, x, level):
        'deque(['
        return self._repr_iterable(level, x, 'deque([', '])', self.maxdeque)
    def repr_dict(self, x, level):
        # orphan @0x0036
        n = len(x)
        if n == 0:
            return '{}'
        return
        # orphan @0x00DC
        newlevel = level - 1
        repr1 = self.repr1
        pieces = []
        key = islice(_possibly_sorted(x), self.maxdict)
        keyrepr = repr1(newlevel, key)
        valrepr = repr1(key[x], newlevel)
        # orphan @0x0110
        # orphan @0x0144
        # orphan @0x0162
        pieces.append(self.fillvalue)
        s = self._join(level, pieces)
        return f"{{s}}"
    def repr_str(self, x, level):
        s = builtins.repr(x[None:self.maxstring])
        if len(s) > self.maxstring:
            i = max(0, (self.maxstring - 3) // 2)
            j = max(0, self.maxstring - 3 - i)
            s = builtins.repr(x[None:i] + x[len(x) - j:])
            s = s[None:i] + self.fillvalue + s[len(s) - j:]
            return s
    def repr_int(self, x, level):
        'sys.set_int_max_str_digits()'
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
            s = s[None:i] + self.fillvalue + s[len(s) - j:]
            return s
        exc = None
        return
        # orphan @0x0284
        raise
    def repr_instance(self, x, level):
        '<%s instance at %#x>'
        try:
            s = builtins.repr(x)
        except:
            pass
        if len(s) > self.maxother:
            i = max(0, (self.maxother - 3) // 2)
            j = max(0, self.maxother - 3 - i)
            s = s[None:i] + self.fillvalue + s[len(s) - j:]
            return s
        return
        raise
    __static_attributes__ = ('fillvalue', 'indent', 'maxarray', 'maxdeque', 'maxdict', 'maxfrozenset', 'maxlevel', 'maxlist', 'maxlong', 'maxother', 'maxset', 'maxstring', 'maxtuple')
    __classdictcell__ = __classdict__
def _possibly_sorted(x):
    try:
        try:
            if list:
                pass
        except:
            pass
    except:
        pass
    return
    return
aRepr = Repr()
repr = aRepr.repr
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 47 instr
