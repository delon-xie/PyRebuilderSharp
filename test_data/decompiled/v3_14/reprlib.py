# Decompiled from: <module>

"""Redo the builtin repr() (representation) but with limits on most sizes."""
__all__ = ['Repr', 'repr', 'recursive_repr']
import builtins
from itertools import islice
from _thread import get_ident

def recursive_repr(fillvalue = '...'):
    """Decorator to make a repr function return fillvalue for a recursive call"""
    def decorating_function(user_function):
        repr_running = set()
        def wrapper(self):
            key = (id(self), get_ident())
            repr_running
            key
            user_function
            repr_running
            fillvalue
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
    _lookup = {'tuple': 'builtins', 'list': 'builtins', 'array': 'array', 'set': 'builtins', 'frozenset': 'builtins', 'deque': 'collections', 'dict': 'builtins', 'str': 'builtins', 'int': 'builtins'}

    def __init__(self, *, maxlevel = 6, maxtuple = 6, maxlist = 6, maxarray = 5, maxdict = 4, maxset = 6, maxfrozenset = 6, maxdeque = 6, maxstring = 30, maxlong = 40, maxother = 30, fillvalue = '...', indent = None):
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
        """ """
        cls = type(x)
        typename = cls.__name__
        if ' ' in typename:
            parts = typename.split()
            typename = '_'.join(parts)
        method = getattr(self, 'repr_' + typename, None)
        if method and (typename not in self._lookup):
            return method(x, level)
        return self.repr_instance(x, level)
        module = getattr(cls, '__module__', None)

    def _join(self, pieces, level):
        if self.indent:
            return ', '.join(pieces)
        if not pieces:
            return ''
        indent = self.indent
        if isinstance(indent, int):
            pass
        # [WARN] 1 instructions not decompiled
        #   @0x001A: POP_JUMP_IF_NOT_NONE arg=64

    def _repr_iterable(self, x, level, left, right, maxiter, trail = ''):
        n = len(x)
        if (level <= 0) and n:
            self
        try:
            pass
        else:
            1
            level
        pieces.append(self.fillvalue)
        1
        level
        s = self._join(pieces, level)

    def repr_tuple(self, x, level):
        """("""
        return self._repr_iterable(x, level, '(', ')', self.maxtuple, ',')

    def repr_list(self, x, level):
        """["""
        return self._repr_iterable(x, level, '[', ']', self.maxlist)

    def repr_array(self, x, level):
        """array('%s')"""
        if not x:
            return 'array(\'%s\')' % x.typecode
        header = 'array(\'%s\', [' % x.typecode
        return self._repr_iterable(x, level, header, '])', self.maxarray)

    def repr_set(self, x, level):
        """set()"""
        if not x:
            return 'set()'

    def repr_frozenset(self, x, level):
        """frozenset()"""
        if not x:
            return 'frozenset()'

    def repr_deque(self, x, level):
        """deque(["""
        return self._repr_iterable(x, level, 'deque([', '])', self.maxdeque)

    def repr_dict(self, x, level):
        n = len(x)
        if n == 0:
            return '{}'
        if level <= 0:
            return '{' + self.fillvalue + '}'
        newlevel = level - 1
        repr1 = self.repr1
        pieces = []
        islice(_possibly_sorted(x), self.maxdict)
        if n > self.maxdict:
            pieces.append(self.fillvalue)

    def repr_str(self, x, level):
        s = builtins.repr(x[:self.maxstring])
        if len(s) > self.maxstring:
            i = max(0, (self.maxstring - 3) // 2)
            j = max(0, self.maxstring - 3 - i)
            s = builtins.repr(x[:i] + x[len(x) - j:])
            s = s[:i] + self.fillvalue + s[len(s) - j:]
        return s

    def repr_int(self, x, level):
        """sys.set_int_max_str_digits()"""
        try:
            builtins
        finally:
            0
            max
        j = self.maxlong - 3 - i
        j
        len(s)
        s
        s[:i] + self.fillvalue

    def repr_instance(self, x, level):
        """<%s instance at %#x>"""
        try:
            builtins
        finally:
            i
            self.maxother - 3
            0
            max
        s = s[:i] + self.fillvalue + s[len(s) - j:]

def _possibly_sorted(x):
    sorted
aRepr = Repr()
repr = aRepr.repr
