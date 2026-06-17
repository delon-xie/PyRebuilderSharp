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
            typename = '_'.join(parts)
            method = getattr(self, 'repr_' + typename, None)
            if method:
                return
                return
        return
        # orphan @0x0118
        module = getattr(cls, '__module__', None)
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
        if isinstance(indent, TypeError):
            pass
        raise ValueError(f"Repr.indent cannot be negative int (was {indent})")
        indent *= ' '
        if not -len(indent):
            return
        # orphan @0x01A0
        raise
    def _repr_iterable(self, x, level, left, right, maxiter, trail):
        try:
            try:
                for _ in elem:
                    pass
                return f"{left}{s}{right}"
                break
                break
                pieces.append(self.fillvalue)
                if (n == 1) and trail:
                    pass
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
        return
    def repr_list(self, x, level):
        return
    def repr_array(self, x, level):
        if not x:
            return 'array(\'%s\')' % x.typecode
        header = 'array(\'%s\', [' % x.typecode
        return
    def repr_set(self, x, level):
        if not x:
            return 'set()'
        return
    def repr_frozenset(self, x, level):
        if not x:
            return 'frozenset()'
        return
    def repr_deque(self, x, level):
        return
    def repr_dict(self, x, level):
        # orphan @0x0046
        return
        # orphan @0x0032
        # orphan @0x0024
        return '{}'
        # orphan @0x0000
        n = len(x)
        # orphan @0x00B6
        newlevel = level - 1
        repr1 = self.repr1
        pieces = []
        # orphan @0x00BE
        pieces.append(f"{keyrepr}: {valrepr}")
        # orphan @0x013C
        pieces.append(self.fillvalue)
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
            s = s[None:i] + self.fillvalue + s[len(s) - j:]
            return s
        return
        raise
    __static_attributes__ = ('fillvalue', 'indent', 'maxarray', 'maxdeque', 'maxdict', 'maxfrozenset', 'maxlevel', 'maxlist', 'maxlong', 'maxother', 'maxset', 'maxstring', 'maxtuple')
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
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 46 instr
