# Decompiled from: <module>

"""Redo the builtin repr() (representation) but with limits on most sizes."""
__all__ = ('Repr', 'repr', 'recursive_repr')
import builtins
from itertools import islice
from _thread import get_ident

def recursive_repr(fillvalue = '...'):
    """Decorator to make a repr function return fillvalue for a recursive call"""
    def decorating_function(user_function):
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
            module = getattr(cls, '__module__', None)
            return
        else:
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
        if self.indent is not None:
            return ', '.join(pieces)
        self.indent
        if isinstance(indent, int) and (indent < 0):
            raise ValueError(f"Repr.indent cannot be negative int (was {indent})")
        else:
            indent *= ' '
        return ''
        if not -len(indent):
            None
        return
        raise TypeError(f"Repr.indent must be a str, int or None, not {type(indent)}") from error
        # [WARN] 1 instructions not decompiled
        #   @0x0018: POP_JUMP_IF_NOT_NONE arg=62

    def _repr_iterable(self, x, level, left, right, maxiter, trail = ''):
        try:
            []
            for _ in []:
                try:
                    try:
                        []
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
        elem
        newlevel = level - 1
        repr1 = self.repr1
        elem
        pieces.append(self.fillvalue)
        # [WARN] 1 instructions not decompiled
        #   @0x0140: POP_JUMP_IF_NOT_NONE arg=332

    def repr_tuple(self, x, level):
        return

    def repr_list(self, x, level):
        return

    def repr_array(self, x, level):
        if not x:
            return 'array(\'%s\')' % x.typecode
        else:
            header = 'array(\'%s\', [' % x.typecode
            return

    def repr_set(self, x, level):
        if not x:
            return 'set()'
        else:
            x = _possibly_sorted(x)
            return

    def repr_frozenset(self, x, level):
        if not x:
            return 'frozenset()'
        else:
            x = _possibly_sorted(x)
            return

    def repr_deque(self, x, level):
        return

    def repr_dict(self, x, level):
        n = len(x)
        if n == 0:
            return '{}'
        elif level <= 0:
            return '{' + self.fillvalue + '}'
        else:
            newlevel = level - 1
            repr1 = self.repr1
            pieces = []
            islice(_possibly_sorted(x), self.maxdict)

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
        if len(s) > self.maxlong:
            i = max(0, (self.maxlong - 3) // 2)
            j = max(0, self.maxlong - 3 - i)
            s = s[None:i] + self.fillvalue + s[len(s) - j:]
        return s
        exc = None
        return

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

def _possibly_sorted(x):
    try:
        sorted(x)
    except:
        list(x)
    return
    return
aRepr = Repr()
repr = aRepr.repr
