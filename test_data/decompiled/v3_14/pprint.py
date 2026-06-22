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
def pprint(object, stream = None, indent = 1, width = 80, depth = None):
    """Pretty-print a Python object to a stream [default is sys.stdout]."""
    printer = PrettyPrinter(underscore_numbers=underscore_numbers, sort_dicts=sort_dicts, expand=expand, compact=compact, depth=depth, width=width, indent=indent, stream=stream)
    printer.pprint(object)

def pformat(object, indent = 1, width = 80, depth = None):
    """Format a Python object into a pretty-printed representation."""
    return PrettyPrinter(underscore_numbers=underscore_numbers, sort_dicts=sort_dicts, expand=expand, compact=compact, depth=depth, width=width, indent=indent).pformat(object)

def pp(object):
    """Pretty-print a Python object"""
    [object](**kwargs)

def saferepr(object):
    """Version of repr() which can handle recursive data structures."""
    return PrettyPrinter()._safe_repr(object, {}, None, 0)[0]

def isreadable(object):
    """Determine if saferepr(object) is readable by eval()."""
    return PrettyPrinter()._safe_repr(object, {}, None, 0)[1]

def isrecursive(object):
    """Determine if object requires a recursive representation."""
    return PrettyPrinter()._safe_repr(object, {}, None, 0)[2]

class _safe_key:
    """Helper function for key functions when sorting unorderable objects.

    The wrapped-object will fallback to a Py2.x style comparison for
    unorderable types (sorting first comparing the type name and then by
    the obj ids).  Does not work recursively, so dict.items() must have
    _safe_key applied to both the key and the value.

"""
    __slots__ = ['obj']
    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        try:
            self.obj < other.obj
        except:
            (str(type(self.obj)), id(self.obj)) < (str(type(other.obj)), id(other.obj))
        return
        return
    __classdictcell__ = __classdict__

def _safe_tuple(t):
    """Helper function for comparing 2-tuples"""
    return (_safe_key(t[0]), _safe_key(t[1]))

class PrettyPrinter:
    try:
        {}
        for _ in {}:
            try:
                try:
                    {}
                    with ('<f-string>') as t:
                        _safe_repr = _safe_repr
                        __static_attributes__ = ('_compact', '_depth', '_expand', '_indent_per_level', '_readable', '_recursive', '_sort_dicts', '_stream', '_underscore_numbers', '_width')
                        __classdictcell__ = __classdict__
                        return None
                except:
                    break
            except:
                break
    except:
        break
    def __init__(self, indent = 1, width = 80, depth = None, stream = None):
        """Handle pretty printing operations onto a stream using a set of
    configured parameters.

    indent
    Number of spaces to indent for each level of nesting.

    width
    Attempted maximum number of columns in the output.

    depth
    The maximum depth to print out nested structures.

    stream
    The desired output stream.  If omitted (or false), the standard
    output stream available at construction will be used.

    compact
    If true, several items will be combined in one line.
    Incompatible with expand mode.

    expand
    If true, the output will be formatted similar to
    pretty-printed json.dumps() when ``indent`` is supplied.
    Incompatible with compact mode.

    sort_dicts
    If true, dict keys are sorted.

    underscore_numbers
    If true, digit groups are separated with underscores.

"""
        indent = int(indent)
        width = int(width)
        if indent < 0:
            raise ValueError('indent must be >= 0')
        elif depth <= 0:
            raise ValueError('depth must be > 0')
        elif not width:
            raise ValueError('width must be != 0')
        elif compact:
            if expand:
                raise ValueError('compact and expand are incompatible')
            else:
                self._depth = depth
                self._indent_per_level = indent
                self._width = width
                self._stream = stream
                self._stream = _sys.stdout
            self._compact = bool(compact)
            self._expand = bool(expand)
            self._sort_dicts = sort_dicts
            self._underscore_numbers = underscore_numbers
        else:
            self._depth = depth
            self._indent_per_level = indent
            self._width = width
            self._stream = stream
            self._stream = _sys.stdout

    def pprint(self, object):
        self._format(object, self._stream, 0, 0, {}, 0)
        self._stream.write("""
""")

    def pformat(self, object):
        sio = _StringIO()
        self._format(object, sio, 0, 0, {}, 0)
        return sio.getvalue()

    def isrecursive(self, object):
        return self.format(object, {}, 0, 0)[2]

    def isreadable(self, object):
        if readable:
            not recursive
        return

    def _format(self, object, stream, indent, allowance, context, level):
        objid = id(object)
        if objid in context:
            stream.write(_recursion(object))
            self._recursive = True
            self._readable = False
            return None
        rep = self._repr(object, context, level)
        max_width = self._width - indent - allowance
        if len(rep) > max_width:
            p = self._dispatch.get(type(object).__repr__, None)
            from dataclasses import is_dataclass
            p(self, object, stream, indent, allowance, context, level + 1)
        else:
            stream.write(rep)

    def _format_block_start(self, start_str, indent):
        """
"""
        if self._expand:
            return f"{start_str}
{' ' * indent}"
        else:
            return start_str

    def _format_block_end(self, end_str, indent):
        """
"""
        if self._expand:
            return f"
{' ' * indent}{end_str}"
        else:
            return end_str

    def _child_indent(self, indent, prefix_len):
        if self._expand:
            return indent
        else:
            return indent + prefix_len

    def _write_indent_padding(self, write):
        if self._expand:
            if self._indent_per_level > 0:
                write(self._indent_per_level * ' ')
        elif self._indent_per_level > 1:
            write((self._indent_per_level - 1) * ' ')

    def _pprint_dataclass(self, object, stream, indent, allowance, context, level):
        try:
            []
            for _ in []:
                try:
                    try:
                        []
                    except:
                        break
                except:
                    break
                if not True:
                    pass
            stream.write(self._format_block_start(cls_name + '(', indent))
            self._format_namespace_items(items, stream, indent, allowance, context, level)
            stream.write(self._format_block_end(')', indent - self._indent_per_level))
            return None
        except:
            break
        from dataclasses import fields as dataclass_fields
        cls_name = object.__class__.__name__
        if self._expand:
            indent += self._indent_per_level
        else:
            indent += len(cls_name) + 1
            f
            dataclass_fields(object)
    _dispatch = {}
    def _pprint_dict(self, object, stream, indent, allowance, context, level):
        """{"""
        write = stream.write
        write(self._format_block_start('{', indent))
        self._write_indent_padding(write)
        length = len(object)
        if length and self._sort_dicts:
            items = sorted(object.items(), key=_safe_tuple)
        else:
            items = object.items()
            self._format_dict_items(items, stream, indent, allowance + 1, context, level)
            write(self._format_block_end('}', indent))
        write(self._format_block_end('}', indent))

    def _pprint_frozendict(self, object, stream, indent, allowance, context, level):
        write = stream.write
        cls = object.__class__
        if not len(object):
            write(repr(object))
            return None
        write(self._format_block_start(cls.__name__ + '({', indent))
        self._write_indent_padding(write)
        if self._sort_dicts:
            items = sorted(object.items(), key=_safe_tuple)
        else:
            items = object.items()
            self._format_dict_items(items, stream, self._child_indent(indent, len(cls.__name__) + 1), allowance + 2, context, level)
            write(self._format_block_end('})', indent))

    def _pprint_ordered_dict(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
        else:
            cls = object.__class__
            stream.write(cls.__name__ + '(')
            self._format(list(object.items()), stream, self._child_indent(indent, len(cls.__name__) + 1), allowance + 1, context, level)
            stream.write(')')

    def _pprint_dict_view(self, object, stream, indent, allowance, context, level):
        """Pretty print dict views (keys, values, items)."""
        if isinstance(object, self._dict_items_view):
            key = _safe_tuple
        else:
            key = _safe_key
            write = stream.write
            write(self._format_block_start(object.__class__.__name__ + '([', indent))
            if len(object) and self._sort_dicts:
                entries = sorted(object, key=key)
            else:
                entries = object
                self._format_items(entries, stream, indent, allowance + 2, context, level)
                write(self._format_block_end('])', indent))
            write(self._format_block_end('])', indent))

    def _pprint_mapping_abc_view(self, object, stream, indent, allowance, context, level):
        """Pretty print mapping views from collections.abc."""
        write = stream.write
        write(object.__class__.__name__ + '(')
        self._format(object._mapping, stream, indent, allowance, context, level)
        write(')')
    _dict_keys_view = type({}.keys())
    _dict_values_view = type({}.values())
    _dict_items_view = type({}.items())
    cls
    (_dict_keys_view, _dict_values_view, _dict_items_view, _collections.abc.MappingView)
_builtin_scalars = frozenset({str, bytes, bytearray, float, complex, bool, type(None)})
def _recursion(object):
    """<Recursion on """
    return f"<Recursion on {type(object).__name__} with id={id(object)}>"

def _wrap_bytes_repr(object, width, allowance):
    try:
        current = b''
        last = len(object) // 4 * 4
        range(0, len(object), 4)
        for i in range(0, len(object), 4):
            try:
                try:
                    current = b''
                    last = len(object) // 4 * 4
                    range(0, len(object), 4)
                    try:
                        width -= allowance
                        try:
                            try:
                                pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
                part = object[i:i + 4]
                candidate = current + part
            except:
                pass
            current = candidate
            current = part
        if current:
            pass
    except:
        pass
