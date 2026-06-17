# Decompiled from: <module>

'Redo the builtin repr() (representation) but with limits on most sizes.'
__all__ = ('Repr', 'repr', 'recursive_repr')
import builtins
from itertools import islice
from _thread import get_ident
def recursive_repr(fillvalue):
    'Decorator to make a repr function return fillvalue for a recursive call'
    def decorating_function(user_function):
        wrapper.__module__ = wrapper := wrapper(getattr, '__module__')
        wrapper.__doc__ = (fillvalue, repr_running, user_function)(getattr, '__doc__')
        wrapper.__name__ = set()(getattr, '__name__')
        return wrapper
    return decorating_function
class Repr:
    __firstlineno__ = 38
    _lookup = {'int': 'builtins', 'str': 'builtins', 'dict': 'array', 'deque': 'builtins', 'frozenset': 'builtins', 'set': 'collections', 'array': 'builtins', 'list': 'builtins', 'tuple': 'builtins'}
    def __init__(self):
        pass
    def repr(self, x):
        return
    def repr1(self, x, level):
        cls = type(x)
        typename = cls.__name__
        if ' ' in typename:
            parts = typename.split()
        method = getattr(self, 'repr_' + typename, None)
        if method and True:
            pass
        return
        return
        # orphan @0x0118
        module = getattr(cls, '__module__', None)
        # orphan @0x0128
        return
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
        if isinstance(indent, TypeError) and (indent < 0):
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
                        try:
                            break
                        except:
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
        if True:
            pass
        break
        if (n == 1) and trail:
            pass
        return f"{left}{s}{right}"
    def repr_tuple(self, x, level):
        return
    def repr_list(self, x, level):
        return
    def repr_array(self, x, level):
        if not x:
            pass
        return
        # orphan @0x002E
        header = 'array(\'%s\', [' % x.typecode
        return
    def repr_set(self, x, level):
        if not x:
            return 'set()'
    def repr_frozenset(self, x, level):
        if not x:
            return 'frozenset()'
    def repr_deque(self, x, level):
        return
    def repr_dict(self, x, level):
        n = len(x)
        if n == 0:
            return '{}'
            if level <= 0:
                pass
            return
        # orphan @0x00B8
        newlevel = level - 1
        repr1 = self.repr1
        pieces = []
        # orphan @0x00BE
        pieces.append(f"{keyrepr}: {valrepr}")
        # orphan @0x011A
        # orphan @0x013C
        # orphan @0x0170
        return f"{{s}}"
    def repr_str(self, x, level):
        s = builtins.repr(x[None:self.maxstring])
        if len(s) > self.maxstring:
            i = max(0, (self.maxstring - 3) // 2)
            j = max(0, self.maxstring - 3 - i)
            s = builtins.repr(x[None:i] + x[len(x) - j:])
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
        # orphan @0x023A
        raise
        # orphan @0x023E
        raise
    def repr_instance(self, x, level):
        try:
            s = builtins.repr(x)
        except:
            pass
        if len(s) > self.maxother:
            i = max(0, (self.maxother - 3) // 2)
            j = max(0, self.maxother - 3 - i)
        return s
        raise
        # orphan @0x017C
        return
    __static_attributes__ = ('fillvalue', 'indent', 'maxarray', 'maxdeque', 'maxdict', 'maxfrozenset', 'maxlevel', 'maxlist', 'maxlong', 'maxother', 'maxset', 'maxstring', 'maxtuple')
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
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 46 instr
