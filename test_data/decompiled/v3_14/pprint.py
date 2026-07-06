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
__all__ = ['pprint', 'pformat', 'isreadable', 'isrecursive', 'saferepr', 'PrettyPrinter', 'pp']

def pprint(object, stream=None, indent=1, width=80, depth=None, *, compact=False, expand=False, sort_dicts=True, underscore_numbers=False):
    'Pretty-print a Python object to a stream [default is sys.stdout].'
    printer = PrettyPrinter(stream=stream, indent=indent, width=width, depth=depth, compact=compact, expand=expand, sort_dicts=sort_dicts, underscore_numbers=underscore_numbers)
    printer.pprint(object)

def pformat(object, indent=1, width=80, depth=None, *, compact=False, expand=False, sort_dicts=True, underscore_numbers=False):
    'Format a Python object into a pretty-printed representation.'
    return PrettyPrinter(indent=indent, width=width, depth=depth, compact=compact, expand=expand, sort_dicts=sort_dicts, underscore_numbers=underscore_numbers).pformat(object)

def pp(object, *, sort_dicts=False):
    'Pretty-print a Python object'
    pprint(object, args, **kwargs)

def saferepr(object):
    'Version of repr() which can handle recursive data structures.'
    return PrettyPrinter()._safe_repr(object, {}, None, 0)[0]

def isreadable(object):
    'Determine if saferepr(object) is readable by eval().'
    return PrettyPrinter()._safe_repr(object, {}, None, 0)[1]

def isrecursive(object):
    'Determine if object requires a recursive representation.'
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
        # orphan @0x0000
        pass

def _safe_tuple(t):
    'Helper function for comparing 2-tuples'
    return (_safe_key(t[0]), _safe_key(t[1]))

class PrettyPrinter:
    def __init__(self, indent, width, depth, stream, *, compact, expand, sort_dicts, underscore_numbers):
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
        indent = int(indent)
        width = int(width)
        if indent < 0:
            raise ValueError('indent must be >= 0')
        raise
        self._depth = depth
        self._indent_per_level = indent
        self._width = width
        if stream:
            self._stream = stream
            self._stream = _sys.stdout
        self._compact = bool(compact)
        self._expand = bool(expand)
        self._sort_dicts = sort_dicts
        self._underscore_numbers = underscore_numbers
        if depth <= 0:
            raise ValueError('depth must be > 0')
        if not width:
            raise ValueError('width must be != 0')
        if compact and expand:
            ValueError('compact and expand are incompatible')
        # [WARN] 1 instructions not decompiled
        #   @0x0054: POP_JUMP_IF_NONE arg=126

    def pprint(self, object):
        if self._stream:
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
        return readable and not recursive

    def _format(self, object, stream, indent, allowance, context, level):
        rep = self._repr(object, context, level)
        max_width = self._width - indent - allowance
        objid = id(object)
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
            if p:
                p(self, object, stream, indent, allowance, context, level + 1)
                return None
            pass
            rep
            stream.write
            return None
        rep
        stream.write
        # [WARN] 1 instructions not decompiled
        #   @0x015C: POP_JUMP_IF_NONE arg=406

    def _format_block_start(self, start_str, indent):
        """
"""
        return self._expand and f"{start_str}\n{' ' * indent}"

    def _format_block_end(self, end_str, indent):
        """
"""
        return self._expand and f"\n{' ' * indent}{end_str}"

    def _child_indent(self, indent, prefix_len):
        return self._expand and indent

    def _write_indent_padding(self, write):
        if self._expand:
            return (self._indent_per_level > 0) and None
        return (self._indent_per_level > 1) and None

    def _pprint_dataclass(self, object, stream, indent, allowance, context, level):
        indent += self._indent_per_level
        from dataclasses import fields as dataclass_fields
        cls_name = object.__class__.__name__
        items = [f for f in dataclass_fields(object) if f.repr]

    def _pprint_dict(self, object, stream, indent, allowance, context, level):
        '{'
        write = stream.write
        write(self._format_block_start('{', indent))
        self._write_indent_padding(write)
        length = len(object)
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
        write(self._format_block_start(cls.__name__ + '({', indent))
        self._write_indent_padding(write)
        write = stream.write
        cls = object.__class__
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
        return len(object) or None

    def _pprint_dict_view(self, object, stream, indent, allowance, context, level):
        'Pretty print dict views (keys, values, items).'
        write = stream.write
        write(self._format_block_start(object.__class__.__name__ + '([', indent))
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
        'Pretty print mapping views from collections.abc.'
        write = stream.write
        write(object.__class__.__name__ + '(')
        self._format(object._mapping, stream, indent, allowance, context, level)
        write(')')

    def _pprint_list(self, object, stream, indent, allowance, context, level):
        '['
        stream.write(self._format_block_start('[', indent))
        self._format_items(object, stream, indent, allowance + 1, context, level)
        stream.write(self._format_block_end(']', indent))

    def _pprint_tuple(self, object, stream, indent, allowance, context, level):
        '('
        stream.write(self._format_block_start('(', indent))
        stream.write(self._format_block_start('(', indent))
        if (len(object) == 1) and not self._expand:
            endchar = ',)'
        endchar = ')'
        self._format_items(object, stream, indent, allowance + len(endchar), context, level)
        stream.write(self._format_block_end(endchar, indent))
        endchar = ')'

    def _pprint_set(self, object, stream, indent, allowance, context, level):
        typ = object.__class__
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
            if self._expand:
                indent += len(typ.__name__) + 1
            object = sorted(object, key=_safe_key)
            self._format_items(object, stream, indent, allowance + len(endchar), context, level)
            stream.write(self._format_block_end(endchar, indent))
        stream.write(self._format_block_start(typ.__name__ + '({', indent))
        endchar = '})'

    def _pprint_str(self, object, stream, indent, allowance, context, level):
        chunks = []
        lines = object.splitlines(True)
        write = stream.write
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
            enumerate(lines)
            # [Block @0x0142] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        enumerate(lines)
        import re
        parts = re.findall('\\S*\\s*', line)
        # [Block @0x047A] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')

    def _pprint_bytes(self, object, stream, indent, allowance, context, level):
        parens = level == 1
        write = stream.write
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
            _wrap_bytes_repr(object, self._width - indent, allowance)
            for rep in _wrap_bytes_repr(object, self._width - indent, allowance):
                write(delim)
                write(rep)
                if delim:
                    pass
                else:
                    delim = """
""" + ' ' * indent
        delim = ''
        _wrap_bytes_repr(object, self._width - indent, allowance)

    def _pprint_bytearray(self, object, stream, indent, allowance, context, level):
        'bytearray('
        write = stream.write
        write(self._format_block_start('bytearray(', indent))
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
        'mappingproxy('
        stream.write('mappingproxy(')
        self._format(object.copy(), stream, self._child_indent(indent, 13), allowance + 1, context, level)
        stream.write(')')

    def _pprint_simplenamespace(self, object, stream, indent, allowance, context, level):
        'namespace'
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
        enumerate(items)
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
                    write(delimnl)
                elif not self._expand:
                    pass
                else:
                    write(',')
        context(level)

    def _format_namespace_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        write = stream.write
        delimnl = """,
""" + ' ' * indent
        last_index = len(items) - 1
        enumerate(items)
        for i in enumerate(items):
            last = i == last_index
            write(key)
            write('=')
            if id(ent) in context:
                write('...')
            elif last:
                pass
            else:
                1
                context(level)
                if not last:
                    write(delimnl)
                elif not self._expand:
                    pass
                else:
                    write(',')

    def _format_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        while last:
            ent = next_ent
            next_ent = next(it)
            if self._compact:
                rep = self._repr(self, v_245, level)
                w = len(rep) + 2
                if width < w:
                    width = max_width
                    if delim:
                        delim = delimnl
        write(delim)
        delim = delimnl
        self(v_86)

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
        rdf = self._repr(object.default_factory, context, level)
        cls = object.__class__
        if not len(object):
            stream.write(repr(object))
            return None
        rdf = self._repr(object.default_factory, context, level)
        cls = object.__class__
        if self._expand:
            stream.write(f"{cls.__name__}({rdf}, ")
        else:
            indent += len(cls.__name__) + 1
            stream.write(f"{cls.__name__}({rdf},\n{' ' * indent}")
            self._pprint_dict(object, stream, indent, allowance + 1, context, level)
            stream.write(')')

    def _pprint_counter(self, object, stream, indent, allowance, context, level):
        return len(object) or None

    def _pprint_chain_map(self, object, stream, indent, allowance, context, level):
        cls = object.__class__
        stream.write(self._format_block_start(cls.__name__ + '(', indent + self._indent_per_level))
        if not len(object.maps):
            stream.write(repr(object))
            return None
        cls = object.__class__
        stream.write(self._format_block_start(cls.__name__ + '(', indent + self._indent_per_level))
        if self._expand:
            indent += self._indent_per_level
        else:
            indent += len(cls.__name__) + 1
            enumerate(object.maps)
            for (m, i) in enumerate(object.maps):
                if i == len(object.maps) - 1:
                    self._format(m, stream, indent, allowance + 1, context, level)
                    if self._expand:
                        stream.write(',')
                    stream.write(self._format_block_end(')', indent - self._indent_per_level))
                else:
                    self._format(m, stream, indent, 1, context, level)
                    stream.write(""",
""" + ' ' * indent)

    def _pprint_deque(self, object, stream, indent, allowance, context, level):
        cls = object.__class__
        stream.write(self._format_block_start(cls.__name__ + '([', indent))
        if not len(object):
            stream.write(repr(object))
            return None
        cls = object.__class__
        stream.write(self._format_block_start(cls.__name__ + '([', indent))
        if not self._expand:
            indent += len(cls.__name__) + 1
        elif object.maxlen:
            self._format_items(object, stream, indent, allowance + 2, context, level)
            stream.write(self._format_block_end('])', indent))
        else:
            pass

    def _pprint_user_dict(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)

    def _pprint_user_list(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)

    def _pprint_user_string(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)

    def _pprint_template(self, object, stream, indent, allowance, context, level):
        cls_name = object.__class__.__name__
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
        'value'
        cls_name = object.__class__.__name__
        cls_name = object.__class__.__name__
        return self._expand and None

    def _safe_repr(self, object, context, maxlevels, level):
        readable = True
        recursive = False
        components = []
        append = components.append
        level += 1
        r = getattr(typ, '__repr__', None)
        typ = type(object)
        typ = type(object)
        if typ in _builtin_scalars:
            return (repr(object), True, False)
        r = getattr(typ, '__repr__', None)
        if issubclass(typ, int):
            if r is int.__repr__:
                return self._underscore_numbers and ('_d', True, False)
            if issubclass(typ, dict):
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
        objid = id(object)
        key = _safe_key
        rep = repr(object)
    cls = {(_dict_keys_view, _dict_values_view, _dict_items_view, _collections.abc.MappingView) for cls in (_dict_keys_view, _dict_values_view, _dict_items_view, _collections.abc.MappingView)}
_builtin_scalars = frozenset({str, bytes, bytearray, float, complex, bool, type(None)})

def _recursion(object):
    '<Recursion on '
    return f"<Recursion on {type(object).__name__} with id={id(object)}>"

def _wrap_bytes_repr(object, width, allowance):
    part = object[i:i + 4]
    candidate = current + part
    for i in range(0, len(object), 4):
        part = object[i:i + 4]
        candidate = current + part
        if i == last:
            width -= allowance
