# Decompiled from: <module>

'Redo the builtin repr() (representation) but with limits on most sizes.'
__all__ = ['Repr', 'repr', 'recursive_repr']
import builtins
from itertools import islice
from _thread import get_ident

def recursive_repr(fillvalue='...'):
    'Decorator to make a repr function return fillvalue for a recursive call'
    def decorating_function(user_function):
        repr_running = set()
        def wrapper(self):
            key = (id(self), get_ident())
            if key in repr_running:
                return fillvalue
            repr_running.add(key)
            try:
                result = user_function(self)
            finally:
                repr_running.discard(key)
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
    _lookup = {'tuple': 'builtins', 'list': 'builtins', 'array': 'array', 'set': 'builtins', 'frozenset': 'builtins', 'deque': 'collections', 'dict': 'builtins', 'str': 'builtins', 'int': 'builtins'}

    def __init__(self, *, maxlevel=6, maxtuple=6, maxlist=6, maxarray=5, maxdict=4, maxset=6, maxfrozenset=6, maxdeque=6, maxstring=30, maxlong=40, maxother=30, fillvalue='...', indent=None):
        v_16.maxlevel = v_32.maxtuple = v_48.maxlist = v_64.maxarray = v_80.maxdict = v_96.maxset = v_112.maxfrozenset = v_128.maxdeque = v_144.maxstring = v_160.maxlong = v_176.maxother = v_192.fillvalue = v_208.indent = self

    def repr(self, x):
        return self.repr1(self, v_16.maxlevel)

    def repr1(self, x, level):
        cls = type(x)
        typename = cls.__name__
        if ' ' in typename:
            parts = typename.split()
            typename = '_'.join(parts)
        method = getattr(self, 'repr_' + typename, None)
        if method:
            if self not in v_64._lookup:
                return method(self, v_18)
            module = getattr(cls, '__module__', None)
            return (self == v_112._lookup[typename]) and method(self, v_18)
        return self.repr_instance(self, v_18)

    def _join(self, pieces, level):
        if self.indent:
            return ', '.join(pieces)
        pass
        return ''
        self.indent
        if isinstance(indent, int):
            if indent < 0:
                raise ValueError(f"Repr.indent cannot be negative int (was {indent})")
            indent *= ' '
            pass
            return -len(indent) or None
        pass

    def _repr_iterable(self, x, level, left, right, maxiter, trail=''):
        n = len(x)
        if (level <= 0) and n:
            s = self.fillvalue
        newlevel = level - 1
        repr1 = self.repr1
        elem
        islice(self, v_21)
        []
        pieces = [islice(self, v_21) for elem in islice(self, v_21)]
        raise
        pass
        s = self._join(self, v_194)

    def repr_tuple(self, x, level):
        return self._repr_iterable(self, v_18, '(', ')', self.maxtuple, ',')

    def repr_list(self, x, level):
        return self._repr_iterable(self, v_18, '[', ']', self.maxlist)

    def repr_array(self, x, level):
        return x or ('array(\'%s\')' % x.typecode)

    def repr_set(self, x, level):
        return x or 'set()'

    def repr_frozenset(self, x, level):
        return x or 'frozenset()'

    def repr_deque(self, x, level):
        return self._repr_iterable(self, v_18, 'deque([', '])', self.maxdeque)

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

    def repr_str(self, x, level):
        s = builtins.repr(x[:self.maxstring])
        if len(s) > self.maxstring:
            i = max(0, (self.maxstring - 3) // 2)
            j = max(0, self.maxstring - 3 - i)
            s = builtins.repr(x[:i] + x[len(x) - j:])
            s = s[:i] + self.fillvalue + s[len(s) - j:]
        return s

    def repr_int(self, x, level):
        pass
        s = builtins.repr(x)
        if len(s) > self.maxlong:
            i = max(0, (self.maxlong - 3) // 2)
            j = max(0, self.maxlong - 3 - i)
            s = s[:i] + self.fillvalue + s[len(s) - j:]
        return s
        pass

    def repr_instance(self, x, level):
        pass
        s = builtins.repr(x)
        if len(s) > self.maxother:
            i = max(0, (self.maxother - 3) // 2)
            j = max(0, self.maxother - 3 - i)
            s = s[:i] + self.fillvalue + s[len(s) - j:]
        return s
        '<%s instance at %#x>' % (x.__class__.__name__, id(x))

def _possibly_sorted(x):
    pass
    sorted(x)
    list(x)
aRepr = Repr()
repr = aRepr.repr
