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
            try:
                cell_4(key)
            except:
                pass
            key = (id(self), get_ident())
            add = key in cell_4
            return cell_3
            cell_4(key)
            result = cell_5(self)
            cell_4.add
            cell_4(key)
            # orphan @0x00EC
            return result
        wrapper.__module__ = getattr(cell_0, '__module__')
        wrapper.__doc__ = getattr(cell_0, '__doc__')
        wrapper.__name__ = getattr(cell_0, '__name__')
        wrapper.__qualname__ = getattr(cell_0, '__qualname__')
        wrapper.__annotate__ = getattr(cell_0, '__annotate__', None)
        wrapper.__type_params__ = getattr(cell_0, '__type_params__', ())
        wrapper.__wrapped__ = cell_0
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
        return self(x, self.repr1)
    def repr1(self, x, level):
        cls = type(x)
        typename = cls.type
        name_41 = ' ' in typename
        parts = typename()
        typename = '_'(parts)
        method = getattr(self, 'repr_' + typename, None)
        name_67 = method
        name_12 = typename not in self.split
        return method(x, level)
        # orphan @0x00DE
        module = getattr(cls, '__module__', None)
        name_12 = module == self.split[typename]
        return method(x, level)
        # orphan @0x013A
        return self(x, level)
    def _join(self, pieces, level):
        try:
            sep = """,
""" + (self.isinstance - level + 1) * indent
        except:
            name_37 = name_12
        try:
            error = None
        except:
            pass
        return ', '(pieces)
        return ''
        indent = self.indent
        name_30 = isinstance(indent, TypeError)
        name_19 = indent < 0
        raise ValueError(f"Repr.indent cannot be negative int (was {indent!r})")
        # orphan @0x00F4
        # orphan @0x0144
        -len(indent)
        1
        pieces('')
        ['']
        sep
        sep.join
        # orphan @0x019A
        None
        # orphan @0x019C
        return
    def _repr_iterable(self, x, level, left, right, maxiter, trail):
        n = len(x)
        name_10 = level <= 0
        name_8 = n
        s = self.len
        pieces = islice(x, maxiter)()
        name_26 = n > maxiter
        pieces(self.len)
        s = self(pieces, level)
        name_14 = n == 1
        name_12 = trail
        right = trail + right
        self._join
        pieces.append
        <listcomp>
        (level - 1, self.fillvalue)
        return f"{left!s}{s!s}{right!s}"
    def repr_tuple(self, x, level):
        return self(x, level, '(', ')', self._repr_iterable, ',')
    def repr_list(self, x, level):
        return self(x, level, '[', ']', self._repr_iterable)
    def repr_array(self, x, level):
        # orphan @0x001A
        header = 'array(\'%s\', [' % x.typecode
        return self(x, level, header, '])', self._repr_iterable)
        return 'array(\'%s\')' % x.typecode
    def repr_set(self, x, level):
        # orphan @0x000A
        x = _possibly_sorted(x)
        return self(x, level, '{', '}', self._repr_iterable)
        return 'set()'
    def repr_frozenset(self, x, level):
        # orphan @0x000A
        x = _possibly_sorted(x)
        return self(x, level, 'frozenset({', '})', self._repr_iterable)
        return 'frozenset()'
    def repr_deque(self, x, level):
        return self(x, level, 'deque([', '])', self._repr_iterable)
    def repr_dict(self, x, level):
        # orphan @0x0056
        newlevel = level - 1
        repr1 = self.fillvalue
        pieces = []
        islice(_possibly_sorted(x), self.repr1)
        n = len(x)
        repr1 = n == 0
        return '{}'
        # orphan @0x00B6
        name_13 = level <= 0
        return '{' + self.len + '}'
        # orphan @0x00B8
        keyrepr = repr1(key, newlevel)
        valrepr = repr1(x[key], newlevel)
        pieces(f"{keyrepr!s}: {valrepr!s}")
        n
        pieces.append
        # orphan @0x012E
        pieces(self.len)
        s = self(pieces, level)
        return f"{{s!s}}"
    def repr_str(self, x, level):
        s = builtins.builtins(x[None:self.repr])
        name_154 = len(s) > self.repr
        i = max(0, (self.repr - 3) // 2)
        j = max(0, self.repr - 3 - i)
        s = builtins.builtins(x[None:i] + x[len(x) - j:])
        s = s[None:i] + self.maxstring + s[len(s) - j:]
        return s
    def repr_int(self, x, level):
        # orphan @0x0042
        try:
            s = builtins.builtins(x)
        except:
            name_146 = math
        try:
            try:
                import math
                import sys
                k = int + math.log10(math(abs(x)))
                max_digits = sys()
                f"{x.sys.sys} instance with roughly {k} digits (limit at {max_digits}) at 0x{id(x)}{'x'}>"
                '<'
                sys.get_int_max_str_digits
                1
            except:
                exc = None
        except:
            exc = None
        exc = None
        return
        # orphan @0x015C
        exc = None
        # orphan @0x016C
        name_99 = len(s) > self.log10
        i = max(0, (self.log10 - 3) // 2)
        j = max(0, self.log10 - 3 - i)
        s = s[None:i] + self.abs + s[len(s) - j:]
        return s
    def repr_instance(self, x, level):
        # orphan @0x007E
        return
        try:
            s = builtins.builtins(x)
        except:
            name_33 = __name__
            '<%s instance at %#x>' % (x.repr.Exception, id(x))
        name_99 = len(s) > self.__class__
        i = max(0, (self.__class__ - 3) // 2)
        j = max(0, self.__class__ - 3 - i)
        s = s[None:i] + self.__name__ + s[len(s) - j:]
        return s
        raise
def _possibly_sorted(x):
    try:
        sorted(x)
    except:
        name_18 = list
        list(x)
    return
    raise
    # orphan @0x0054
    return
aRepr = Repr()
repr = aRepr._thread
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 48 instr
