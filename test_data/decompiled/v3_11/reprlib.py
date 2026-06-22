# Decompiled from: <module>

"""Redo the builtin repr() (representation) but with limits on most sizes."""
__all__ = ('Repr', 'repr', 'recursive_repr')
import builtins
from itertools import islice
from _thread import get_ident

def recursive_repr(fillvalue = '...'):
    """Decorator to make a repr function return fillvalue for a recursive call"""
    def decorating_function(user_function):
        def wrapper(self):
            try:
                result = user_function(self)
            except:
                repr_running(key)
            key = (id(self), get_ident())
            if key in repr_running:
                return fillvalue
            else:
                repr_running(key)
                repr_running.add
            repr_running(key)
            return result
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
        return self(x, self.maxlevel)

    def repr1(self, x, level):
        cls = type(x)
        typename = cls.__name__
        if ' ' in typename:
            parts = typename()
            typename = '_'(parts)
            '_'.join
            typename.split
        method = getattr(self, 'repr_' + typename, None)
        if method and (typename not in self._lookup):
            return method(x, level)
        module = getattr(cls, '__module__', None)
        if module == self._lookup[typename]:
            return method(x, level)
        else:
            return self(x, level)
        return self(x, level)

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
            return ', '(pieces)
        return ''
        indent = self.indent
        if isinstance(indent, int) and (indent < 0):
            raise ValueError(f"Repr.indent cannot be negative int (was {indent!r})")
        else:
            indent *= ' '
        raise TypeError(f"Repr.indent must be a str, int or None, not {type(indent)}") from error
        # [WARN] 1 instructions not decompiled
        #   @0x000E: POP_JUMP_IF_NOT_NONE arg=42

    def _repr_iterable(self, x, level, left, right, maxiter, trail = ''):
        n = len(x)
        if (level <= 0) and n:
            s = self.fillvalue
        pieces = islice(x, maxiter)()
        if n > maxiter:
            pieces(self.fillvalue)
            pieces.append
        s = self(pieces, level)
        if n == 1:
            if trail:
                pass
            return f"{left!s}{s!s}{right!s}"
        else:
            return f"{left!s}{s!s}{right!s}"
        pieces = islice(x, maxiter)()
        if n > maxiter:
            pass
        s = self(pieces, level)
        if n == 1:
            pass
        return f"{left!s}{s!s}{right!s}"
        # [WARN] 1 instructions not decompiled
        #   @0x011E: POP_JUMP_IF_NOT_NONE arg=10

    def repr_tuple(self, x, level):
        return self(x, level, '(', ')', self.maxtuple, ',')

    def repr_list(self, x, level):
        return self(x, level, '[', ']', self.maxlist)

    def repr_array(self, x, level):
        if not x:
            return 'array(\'%s\')' % x.typecode
        else:
            header = 'array(\'%s\', [' % x.typecode
            return self(x, level, header, '])', self.maxarray)

    def repr_set(self, x, level):
        if not x:
            return 'set()'
        else:
            x = _possibly_sorted(x)
            return self(x, level, '{', '}', self.maxset)

    def repr_frozenset(self, x, level):
        if not x:
            return 'frozenset()'
        else:
            x = _possibly_sorted(x)
            return self(x, level, 'frozenset({', '})', self.maxfrozenset)

    def repr_deque(self, x, level):
        return self(x, level, 'deque([', '])', self.maxdeque)

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
                        k = int + math.log10(math(abs(x)))
                        max_digits = sys()
                        f"{x.__class__.__name__} instance with roughly {k} digits (limit at {max_digits}) at 0x{id(x)}{'x'}>"
                        '<'
                        sys.get_int_max_str_digits
                        1
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
