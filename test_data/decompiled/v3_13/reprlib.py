# Decompiled from: <module>

'Redo the builtin repr() (representation) but with limits on most sizes.'
__all__ = ('Repr', 'repr', 'recursive_repr')
import builtins
from itertools import islice
from _thread import get_ident
def recursive_repr(fillvalue):
    'Decorator to make a repr function return fillvalue for a recursive call'
    def decorating_function(user_function):
        getattr(cell_0, '__module__').__module__ = wrapper
        getattr(cell_0, '__doc__').__doc__ = wrapper
        getattr(cell_0, '__name__').__name__ = wrapper
        getattr(cell_0, '__qualname__').__qualname__ = wrapper
        getattr(cell_0, '__annotate__', None).__annotate__ = wrapper
        getattr(cell_0, '__type_params__', ()).__type_params__ = wrapper
        cell_0.__wrapped__ = wrapper
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
                pass
        # orphan @0x00B8
        # orphan @0x00CA
        return
        # orphan @0x0118
        module = getattr(cls, '__module__', None)
        return
        # orphan @0x01A2
        return
    def _join(self, pieces, level):
        try:
            sep = """,
""" + (self.maxlevel - level + 1) * indent
        except:
            name_12
        try:
            error = None
        except:
            pass
        return ', '.join(pieces)
        return ''
        if isinstance(indent, TypeError):
            indent < 0
        indent *= ' '
        raise ValueError(f"Repr.indent cannot be negative int (was {indent})")
        if not -len(indent):
            return
        raise TypeError(f"Repr.indent must be a str, int or None, not {type(indent)}") from error
    def _repr_iterable(self, x, level, left, right, maxiter, trail):
        try:
            try:
                for _ in elem:
                    pass
                return f"{left}{s}{right}"
                break
                break
            except:
                break
        except:
            break
        len(x)
        if (level <= 0) and n:
            s = self.fillvalue
            newlevel = level - 1
            repr1 = self.repr1
        elem
        pieces.append(self.fillvalue)
        if (n == 1) and trail:
            self.indent
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
        # orphan @0x0020
        return
    def repr_frozenset(self, x, level):
        if not x:
            return 'frozenset()'
        # orphan @0x0020
        return
    def repr_deque(self, x, level):
        return
    def repr_dict(self, x, level):
        # orphan @0x0048
        return
        n = len(x)
        if n == 0:
            return '{}'
            if level <= 0:
                self.fillvalue
                '{'
            newlevel = level - 1
            repr1 = self.repr1
            pieces = []
            islice
            for key in islice:
                pieces.append(f"{keyrepr}: {valrepr}")
                break
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
                        math.log10
                        int
                        1
                        try:
                            max_digits = sys.get_int_max_str_digits()
                            f"{x.__class__.__name__} instance with roughly {k} digits (limit at {max_digits}) at 0x{id(x)}x>"
                            '<'
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
            s = s[None:i] + self.fillvalue + s[len(s) - j:]
            return s
        exc = None
        return
        # orphan @0x023E
    def repr_instance(self, x, level):
        try:
            s = builtins.repr(x)
        except:
            '<%s instance at %#x>' % (x.__class__.__name__, id(x))
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
        sorted(x)
    except:
        list(x)
    return
    return
    raise
aRepr = Repr()
repr = aRepr.repr
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 46 instr
