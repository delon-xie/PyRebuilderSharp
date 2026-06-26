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
def pprint(object, stream, indent, width, depth, *, compact = None, expand = 1, sort_dicts = 80, underscore_numbers = None):
    """Pretty-print a Python object to a stream [default is sys.stdout]."""
    printer = PrettyPrinter(underscore_numbers=underscore_numbers, sort_dicts=sort_dicts, expand=expand, compact=compact, depth=depth, width=width, indent=indent, stream=stream)
    printer.pprint(object)

def pformat(object, indent, width, depth, *, compact, expand = 1, sort_dicts = 80, underscore_numbers = None):
    """Format a Python object into a pretty-printed representation."""
    return PrettyPrinter(underscore_numbers=underscore_numbers, sort_dicts=sort_dicts, expand=expand, compact=compact, depth=depth, width=width, indent=indent).pformat(object)

def pp(object, *, sort_dicts):
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
        except TypeError:
            (str(type(self.obj)), id(self.obj)) < (str(type(other.obj)), id(other.obj))
        return

def _safe_tuple(t):
    """Helper function for comparing 2-tuples"""
    return (_safe_key(t[0]), _safe_key(t[1]))

class PrettyPrinter:
    def __init__(self, indent, width, depth, stream, *, compact = 1, expand = 80, sort_dicts = None, underscore_numbers = None):
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
            return not recursive
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
            return stream.write(rep)

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
        from dataclasses import fields as dataclass_fields
        cls_name = object.__class__.__name__
        if self._expand:
            indent += self._indent_per_level
        else:
            indent += len(cls_name) + 1
            f
            []
            for _ in []:
                if not True:
                    pass
            stream.write(self._format_block_start(cls_name + '(', indent))
            self._format_namespace_items(items, stream, indent, allowance, context, level)
            stream.write(self._format_block_end(')', indent - self._indent_per_level))
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
    {}
    for _ in {}:
        pass
    def _pprint_list(self, object, stream, indent, allowance, context, level):
        """["""
        stream.write(self._format_block_start('[', indent))
        self._format_items(object, stream, indent, allowance + 1, context, level)
        stream.write(self._format_block_end(']', indent))

    def _pprint_tuple(self, object, stream, indent, allowance, context, level):
        """("""
        stream.write(self._format_block_start('(', indent))
        if (len(object) == 1) and not self._expand:
            endchar = ',)'
        endchar = ')'
        self._format_items(object, stream, indent, allowance + len(endchar), context, level)
        stream.write(self._format_block_end(endchar, indent))
        endchar = ')'

    def _pprint_set(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        typ = object.__class__
        if typ is set:
            stream.write(self._format_block_start('{', indent))
            endchar = '}'
        else:
            stream.write(self._format_block_start(typ.__name__ + '({', indent))
            endchar = '})'
            if not self._expand:
                indent += len(typ.__name__) + 1
            object = sorted(object, key=_safe_key)
            self._format_items(object, stream, indent, allowance + len(endchar), context, level)
            stream.write(self._format_block_end(endchar, indent))

    def _pprint_str(self, object, stream, indent, allowance, context, level):
        write = stream.write
        if not len(object):
            write(repr(object))
            return None
        chunks = []
        lines = object.splitlines(True)
        if (level == 1) and self._expand:
            indent += self._indent_per_level
        else:
            indent += 1
            allowance += 1
            self._width - indent
            self._width - indent
            for (line, i) in self._width - indent:
                rep = repr(line)
                if i == len(lines) - 1:
                    max_width1 -= allowance
                elif len(rep) <= max_width1:
                    return chunks.append(rep)
                else:
                    import re
                    parts = re.findall('\\S*\\s*', line)
                    if not parts:
                        raise None
                    elif parts[-1]:
                        raise None
                    else:
                        parts.pop()
                        max_width2 = max_width
                        current = ''
            if len(chunks) == 1:
                write(rep)
                return None
            elif level == 1:
                return write(self._format_block_start('(', indent))
        self._width - indent
        self._width - indent

    def _pprint_bytes(self, object, stream, indent, allowance, context, level):
        write = stream.write
        if len(object) <= 4:
            write(repr(object))
            return None
        parens = level == 1
        if parens and self._expand:
            indent += self._indent_per_level
        else:
            indent += 1
            allowance += 1
            write(self._format_block_start('(', indent))
            delim = ''
            for rep in _wrap_bytes_repr(object, self._width - indent, allowance):
                write(delim)
                write(rep)
                if delim:
                    pass
                else:
                    delim = """
""" + ' ' * indent
            if parens:
                write(self._format_block_end(')', indent - self._indent_per_level))
                return None
        delim = ''

    def _pprint_bytearray(self, object, stream, indent, allowance, context, level):
        """bytearray("""
        write = stream.write
        write(self._format_block_start('bytearray(', indent))
        if self._expand:
            write(' ' * self._indent_per_level)
            recursive_indent = indent + self._indent_per_level
        else:
            recursive_indent = indent + 10
            self._pprint_bytes(bytes(object), stream, recursive_indent, allowance + 1, context, level + 1)
            write(self._format_block_end(')', indent))

    def _pprint_mappingproxy(self, object, stream, indent, allowance, context, level):
        """mappingproxy("""
        stream.write('mappingproxy(')
        self._format(object.copy(), stream, self._child_indent(indent, 13), allowance + 1, context, level)
        stream.write(')')

    def _pprint_simplenamespace(self, object, stream, indent, allowance, context, level):
        """namespace"""
        if type(object) is _types.SimpleNamespace:
            cls_name = 'namespace'
        else:
            cls_name = object.__class__.__name__
            if self._expand:
                indent += self._indent_per_level
            else:
                indent += len(cls_name) + 1
                items = object.__dict__.items()
                stream.write(self._format_block_start(cls_name + '(', indent))
                self._format_namespace_items(items, stream, indent, allowance, context, level)
                stream.write(self._format_block_end(')', indent - self._indent_per_level))

    def _format_dict_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        write = stream.write
        indent += self._indent_per_level
        delimnl = """,
""" + ' ' * indent
        last_index = len(items) - 1
        for i in enumerate(items):
            last = i == last_index
            rep = self._repr(key, context, level)
            write(rep)
            write(': ')
            if last:
                pass
            else:
                1
                context(level)
                if not last:
                    return write(delimnl)
                elif not self._expand:
                    pass
                else:
                    return write(',')

    def _format_namespace_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        write = stream.write
        delimnl = """,
""" + ' ' * indent
        last_index = len(items) - 1
        for i in enumerate(items):
            last = i == last_index
            write(key)
            write('=')
            if id(ent) in context:
                return write('...')
            elif last:
                pass
            else:
                1
                context(level)
                if not last:
                    return write(delimnl)
                elif not self._expand:
                    pass
                else:
                    return write(',')

    def _format_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        try:
            next_ent = next(it)
        except StopIteration:
            pass
        write = stream.write
        indent += self._indent_per_level
        self._write_indent_padding(write)
        delimnl = """,
""" + ' ' * indent
        delim = ''
        it := iter(items)
        self._width - indent + 1
        self._width - indent + 1
        last = False
        while last:
            ent = next_ent
            next_ent = next(it)
            if self._compact:
                rep = self._repr(level)
                w = len(rep) + 2
                if width < w:
                    width = max_width
                    if delim:
                        delim = delimnl
                    elif width >= w:
                        width -= w
                        write(delim)
                        delim = ', '
                        write(rep)
                elif width >= w:
                    pass
            write(delim)
            delim = delimnl
            if last:
                pass
            else:
                return 1

    def _repr(self, object, context, level):
        if not readable:
            self._readable = False
        elif recursive:
            self._recursive = True

    def format(self, object, context, maxlevels, level):
        """Format object for a specific context, returning a string
    and flags indicating whether the representation is 'readable'
    and whether the object represents a recursive construct.
"""
        return self._safe_repr(object, context, maxlevels, level)

    def _pprint_default_dict(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        rdf = self._repr(object.default_factory, context, level)
        cls = object.__class__
        if self._expand:
            return stream.write(f"{cls.__name__}({rdf}, ")
        else:
            indent += len(cls.__name__) + 1
            stream.write(f"{cls.__name__}({rdf},
{' ' * indent}")
            self._pprint_dict(object, stream, indent, allowance + 1, context, level)
            stream.write(')')

    def _pprint_counter(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
        else:
            cls = object.__class__
            stream.write(self._format_block_start(cls.__name__ + '({', indent))
            self._write_indent_padding(stream.write)
            items = object.most_common()
            self._format_dict_items(items, stream, self._child_indent(indent, len(cls.__name__) + 1), allowance + 2, context, level)
            stream.write(self._format_block_end('})', indent))

    def _pprint_chain_map(self, object, stream, indent, allowance, context, level):
        if not len(object.maps):
            stream.write(repr(object))
            return None
        cls = object.__class__
        stream.write(self._format_block_start(cls.__name__ + '(', indent + self._indent_per_level))
        if self._expand:
            indent += self._indent_per_level
        else:
            indent += len(cls.__name__) + 1
            for (m, i) in enumerate(object.maps):
                if i == len(object.maps) - 1:
                    self._format(m, stream, indent, allowance + 1, context, level)
                    if self._expand:
                        return stream.write(',')
                    stream.write(self._format_block_end(')', indent - self._indent_per_level))
                else:
                    self._format(m, stream, indent, 1, context, level)
                    stream.write(""",
""" + ' ' * indent)

    def _pprint_deque(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        cls = object.__class__
        stream.write(self._format_block_start(cls.__name__ + '([', indent))
        if not self._expand:
            indent += len(cls.__name__) + 1
        self._format_items(object, stream, indent, allowance + 2, context, level)
        stream.write(self._format_block_end('])', indent))

    def _pprint_user_dict(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)

    def _pprint_user_list(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)

    def _pprint_user_string(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)

    def _pprint_template(self, object, stream, indent, allowance, context, level):
        cls_name = object.__class__.__name__
        if self._expand:
            indent += self._indent_per_level
        else:
            indent += len(cls_name) + 1
            items = (('strings', object.strings), ('interpolations', object.interpolations))
            stream.write(self._format_block_start(cls_name + '(', indent))
            self._format_namespace_items(items, stream, indent, allowance, context, level)
            stream.write(self._format_block_end(')', indent - self._indent_per_level))

    def _pprint_interpolation(self, object, stream, indent, allowance, context, level):
        """value"""
        cls_name = object.__class__.__name__
        if self._expand:
            indent += self._indent_per_level
            items = (('value', object.value), ('expression', object.expression), ('conversion', object.conversion), ('format_spec', object.format_spec))
            stream.write(self._format_block_start(cls_name + '(', indent))
            self._format_namespace_items(items, stream, indent, allowance, context, level)
            stream.write(self._format_block_end(')', indent - self._indent_per_level))
        else:
            indent += len(cls_name)
            items = (object.value, object.expression, object.conversion, object.format_spec)
            stream.write(cls_name + '(')
            self._format_items(items, stream, indent, allowance, context, level)
            stream.write(')')
    t = ('<f-string>')
    def _safe_repr(self, object, context, maxlevels, level):
        typ = type(object)
        if typ in _builtin_scalars:
            return (repr(object), True, False)
        r = getattr(typ, '__repr__', None)
        if issubclass(typ, int):
            if r is int.__repr__:
                if self._underscore_numbers:
                    return ('_d', True, False)
                else:
                    return (repr(object), True, False)
            elif issubclass(typ, dict):
                pass
            elif issubclass(typ, frozendict):
                pass
            elif issubclass(typ, list):
                pass
            elif issubclass(typ, tuple):
                pass
            elif issubclass(typ, _collections.abc.MappingView):
                pass
        elif issubclass(typ, dict):
            pass
        elif issubclass(typ, frozendict):
            pass
        elif issubclass(typ, list):
            pass
        elif issubclass(typ, tuple):
            pass
        elif issubclass(typ, _collections.abc.MappingView):
            pass
    with ('<f-string>') as t:
        _safe_repr = _safe_repr
        __static_attributes__ = ('_compact', '_depth', '_expand', '_indent_per_level', '_readable', '_recursive', '_sort_dicts', '_stream', '_underscore_numbers', '_width')
        __classdictcell__ = __classdict__
        return None
_builtin_scalars = frozenset({str, bytes, bytearray, float, complex, bool, type(None)})
def _recursion(object):
    """<Recursion on """
    return f"<Recursion on {type(object).__name__} with id={id(object)}>"

def _wrap_bytes_repr(object, width, allowance):
    current = b''
    last = len(object) // 4 * 4
    for i in range(0, len(object), 4):
        part = object[i:i + 4]
        candidate = current + part
        if i == last:
            width -= allowance
        elif len(repr(candidate)) > width:
            if current:
                pass
            current = part
        else:
            current = candidate
    if current:
        pass
    repr(current)
    repr(current)
