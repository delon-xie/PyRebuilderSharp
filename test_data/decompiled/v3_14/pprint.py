# Decompiled from: <module>

"""Support to pretty-print lists, tuples, & dictionaries recursively.

Very simple, but useful, especially in debugging data structures.

Classes
-------

PrettyPrinter()
    Handle pretty-printing operations onto a stream using a configured
    set of formatting parameters.

Functions
---------

pformat()
    Format a Python object into a pretty-printed representation.

pprint()
    Pretty-print a Python object to a stream [default is sys.stdout].

saferepr()
    Generate a 'standard' repr()-like value, but protect against recursive
    data structures.

"""
import collections as _collections
import sys as _sys
import types as _types
from io import StringIO as _StringIO
__all__ = ('pprint', 'pformat', 'isreadable', 'isrecursive', 'saferepr', 'PrettyPrinter', 'pp')
def pprint(object, stream, indent, width, depth):
    'Pretty-print a Python object to a stream [default is sys.stdout].'
def pformat(object, indent, width, depth):
    'Format a Python object into a pretty-printed representation.'
    return
def pp(object):
    'Pretty-print a Python object'
def saferepr(object):
    'Version of repr() which can handle recursive data structures.'
    return
def isreadable(object):
    'Determine if saferepr(object) is readable by eval().'
    return
def isrecursive(object):
    'Determine if object requires a recursive representation.'
    return
_safe_key = None(_safe_key, '_safe_key')
def _safe_tuple(t):
    'Helper function for comparing 2-tuples'
    return ()
PrettyPrinter = None(PrettyPrinter, 'PrettyPrinter')
_builtin_scalars = str(# Unknown node: SetLiteral)
def _recursion(object):
    '<Recursion on '
    return f"{'<Recursion on '(type).__name__}{' with id='(id)}>"
def _wrap_bytes_repr(object, width, allowance):
    try:
        current = b''
        for i in iterable:
            if True:
                pass
            try:
                try:
                    current = b''
                    try:
                        pass
                    except:
                        pass
                except:
                    pass
            except:
                pass
            current = candidate
            break
        if True:
            pass
        return
    except:
        pass
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 111 instr
