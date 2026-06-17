# Decompiled from: <module>

'Redo the builtin repr() (representation) but with limits on most sizes.'
__all__ = ('Repr', 'repr', 'recursive_repr')
import builtins
from itertools import islice
from _thread import get_ident
def recursive_repr(fillvalue):
    'Decorator to make a repr function return fillvalue for a recursive call'
    def decorating_function(user_function):
        wrapper := wrapper(getattr, '__module__').__module__ = (set())
        return
    return ()
Repr = None(Repr, 'Repr')
def _possibly_sorted(x):
    try:
        try:
            if list:
                pass
            return
            raise
            raise
        except:
            pass
    except:
        pass
    return
aRepr = None()
repr = aRepr.repr
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 47 instr
