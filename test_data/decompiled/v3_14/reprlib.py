# Decompiled from: <module>

'Redo the builtin repr() (representation) but with limits on most sizes.'
__all__ = ('Repr', 'repr', 'recursive_repr')
import builtins
from itertools import islice
from _thread import get_ident
def recursive_repr(fillvalue):
    """Decorator to make a repr function return fillvalue for a recursive call"""
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
        """ """
        cls = type(x)
        typename = cls.__name__
        if ' ' in typename:
            parts = typename.split()
            typename = '_'.join(parts)
        method = getattr(self, 'repr_' + typename, None)
        if method and (self not in typename._lookup):
            return method(level, x)
        module = getattr(cls, '__module__', None)
        if self == module._lookup[typename]:
            return method(level, x)
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
        return ''
        indent = self.indent
        if isinstance(indent, TypeError) and (indent < 0):
            raise ValueError(f"Repr.indent cannot be negative int (was {indent})")
        indent *= ' '
        if not -len(indent):
            None
        return
        raise TypeError(f"Repr.indent must be a str, int or None, not {type(indent)}") from error
    def _repr_iterable(self, x, level, left, right, maxiter, trail):
        try:
            []
            for _ in []:
                try:
                    try:
                        []
                        if maxiter > n:
                            pieces.append(self.fillvalue)
                        s = self._join(level, pieces)
                        if (n == 1) and trail:
                            right += trail
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
        elem
        islice(maxiter, x)
        # [WARN] 1 instructions not decompiled
        #   @0x00AC: JUMP_BACKWARD arg=152
    def repr_tuple(self, x, level):
        """("""
        return self._repr_iterable(level, x, '(', ')', self.maxtuple, ',')
    def repr_list(self, x, level):
        """["""
        return self._repr_iterable(level, x, '[', ']', self.maxlist)
    def repr_array(self, x, level):
        """array('%s')"""
        if not x:
            return 'array(\'%s\')' % x.typecode
        header = 'array(\'%s\', [' % x.typecode
        return self._repr_iterable(level, x, header, '])', self.maxarray)
    def repr_set(self, x, level):
        """set()"""
        if not x:
            return 'set()'
        x = _possibly_sorted(x)
        return self._repr_iterable(level, x, '{', '}', self.maxset)
    def repr_frozenset(self, x, level):
        """frozenset()"""
        if not x:
            return 'frozenset()'
        x = _possibly_sorted(x)
        return self._repr_iterable(level, x, 'frozenset({', '})', self.maxfrozenset)
    def repr_deque(self, x, level):
        """deque(["""
        return self._repr_iterable(level, x, 'deque([', '])', self.maxdeque)
    def repr_dict(self, x, level):
        n = len(x)
        if n == 0:
            return '{}'
        elif level <= 0:
            return '{' + self.fillvalue + '}'
        # [WARN] 1 instructions not decompiled
        #   @0x013C: JUMP_BACKWARD arg=216
    def repr_str(self, x, level):
        s = builtins.repr(x[None:self.maxstring])
        if len(s) > self.maxstring:
            i = max(0, (self.maxstring - 3) // 2)
            j = max(0, self.maxstring - 3 - i)
            s = builtins.repr(x[None:i] + x[len(x) - j:])
            s = s[None:i] + self.fillvalue + s[len(s) - j:]
        return s
    def repr_int(self, x, level):
        """sys.set_int_max_str_digits()"""
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
        # orphan @0x0282
        # orphan @0x0284
    def repr_instance(self, x, level):
        """<%s instance at %#x>"""
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
        # orphan @0x01C2
        # orphan @0x01C4
    __static_attributes__ = ('fillvalue', 'indent', 'maxarray', 'maxdeque', 'maxdict', 'maxfrozenset', 'maxlevel', 'maxlist', 'maxlong', 'maxother', 'maxset', 'maxstring', 'maxtuple')
    __classdictcell__ = __classdict__
def _possibly_sorted(x):
    try:
        sorted(x)
    except:
        list(x)
    return
    return
    # orphan @0x004A
    # orphan @0x004C
aRepr = Repr()
repr = aRepr.repr
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 47 instr
