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
        method = getattr(self, 'repr_' + typename, None)
        if method and (self not in typename._lookup):
            pass
        return
        return
        # orphan @0x012E
        module = getattr(cls, '__module__', None)
        # orphan @0x0140
        return self.repr_instance(level, x)
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
        return
        indent = self.indent
        if indent < 0:
            pass
        raise
        if not -len(indent):
            pass
        return
        raise TypeError(f"Repr.indent must be a str, int or None, not {type(indent)}") from error
    def _repr_iterable(self, x, level, left, right, maxiter, trail):
        try:
            for _ in []:
                try:
                    try:
                        if maxiter > n:
                            pass
                        break
                        if (n == 1) and trail:
                            pass
                        return f"{left}{s}{right}"
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
    def repr_tuple(self, x, level):
        '('
        return self._repr_iterable(level, x, '(', ')', self.maxtuple, ',')
    def repr_list(self, x, level):
        '['
        return self._repr_iterable(level, x, '[', ']', self.maxlist)
    def repr_array(self, x, level):
        'array(\'%s\')'
        if not x:
            pass
        return
        # orphan @0x0038
        header = 'array(\'%s\', [' % x.typecode
        return self._repr_iterable(level, x, header, '])', self.maxarray)
    def repr_set(self, x, level):
        'set()'
        # orphan @0x0016
        x = _possibly_sorted(x)
        return self._repr_iterable(level, x, '{', '}', self.maxset)
        if not x:
            pass
        return
    def repr_frozenset(self, x, level):
        'frozenset()'
        # orphan @0x0016
        x = _possibly_sorted(x)
        return self._repr_iterable(level, x, 'frozenset({', '})', self.maxfrozenset)
        if not x:
            pass
        return
    def repr_deque(self, x, level):
        'deque(['
        return self._repr_iterable(level, x, 'deque([', '])', self.maxdeque)
    def repr_dict(self, x, level):
        # orphan @0x006A
        return
        # orphan @0x0036
        n = len(x)
        if n == 0:
            pass
        return
        # orphan @0x00D6
        newlevel = level - 1
        repr1 = self.repr1
        pieces = []
        # orphan @0x00DC
        keyrepr = repr1(newlevel, key)
        valrepr = repr1(key[x], newlevel)
        pieces.append(f"{keyrepr}: {valrepr}")
        # orphan @0x0140
        # orphan @0x0162
        # orphan @0x0198
        s = self._join(level, pieces)
        return f"{{s}}"
    def repr_str(self, x, level):
        s = builtins.repr(x[None:self.maxstring])
        if len(s) > self.maxstring:
            i = max(0, (self.maxstring - 3) // 2)
            j = max(0, self.maxstring - 3 - i)
            s = builtins.repr(x[None:i] + x[len(x) - j:])
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
        except:
            exc = None
        if len(s) > self.maxlong:
            i = max(0, (self.maxlong - 3) // 2)
            j = max(0, self.maxlong - 3 - i)
        return s
        exc = None
        return
        # orphan @0x0280
        raise
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
        return s
        raise
        # orphan @0x01C0
        return
    __static_attributes__ = ('fillvalue', 'indent', 'maxarray', 'maxdeque', 'maxdict', 'maxfrozenset', 'maxlevel', 'maxlist', 'maxlong', 'maxother', 'maxset', 'maxstring', 'maxtuple')
    __classdictcell__ = __classdict__
def _possibly_sorted(x):
    try:
        try:
            if list:
                pass
            return
        except:
            pass
    except:
        pass
    return
aRepr = Repr()
repr = aRepr.repr
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 47 instr
