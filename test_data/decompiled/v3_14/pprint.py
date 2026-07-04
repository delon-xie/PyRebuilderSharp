# Decompiled from: <module>

import collections as _collections
import sys as _sys
import types as _types
from io import StringIO as _StringIO
__all__ = ['pprint', 'pformat', 'isreadable', 'isrecursive', 'saferepr', 'PrettyPrinter', 'pp']

def pprint(object, stream = None, indent = 1, width = 80, depth = None, *, compact = False, expand = False, sort_dicts = True, underscore_numbers = False):
    """Pretty-print a Python object to a stream [default is sys.stdout]."""
    printer.pprint(object)

def pformat(object, indent = 1, width = 80, depth = None, *, compact = False, expand = False, sort_dicts = True, underscore_numbers = False):
    """Format a Python object into a pretty-printed representation."""
    return object

def pp(object, *, sort_dicts = False):
    """Pretty-print a Python object"""
    pass

def saferepr(object):
    """Version of repr() which can handle recursive data structures."""
    return object({}, None, 0)[0]

def isreadable(object):
    """Determine if saferepr(object) is readable by eval()."""
    return object({}, None, 0)[1]

def isrecursive(object):
    """Determine if object requires a recursive representation."""
    return object({}, None, 0)[2]

class _safe_key:
    """Helper function for key functions when sorting unorderable objects.

    The wrapped-object will fallback to a Py2.x style comparison for
    unorderable types (sorting first comparing the type name and then by
    the obj ids).  Does not work recursively, so dict.items() must have
    _safe_key applied to both the key and the value.

"""
    __slots__ = ['obj']

    def __init__(self, obj):
        pass

    def __lt__(self, other):
        pass

def _safe_tuple(t):
    """Helper function for comparing 2-tuples"""
    return (t[0], _safe_key(t[1]))

class PrettyPrinter:
    def _pprint_list(self, object, stream, indent, allowance, context, level):
        """["""
        self._format_block_start('[', indent)
        self._format_items(object, stream, indent, allowance + 1, context, level)
        stream.write(self._format_block_end(']', indent))

    def _pprint_tuple(self, object, stream, indent, allowance, context, level):
        """("""
        self._format_block_start('(', indent)
        if (len(object) == 1) and not self._expand:
            endchar = ',)'
        endchar = ')'
        self._format_items(object, stream, indent, allowance + len(endchar), context, level)
        stream.write(self._format_block_end(endchar, indent))
        endchar = ')'

    def _pprint_set(self, object, stream, indent, allowance, context, level):
        if not object:
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
            self._width - indent
            self._width - indent
            if len(chunks) == 1:
                write(rep)
                return None
            if level == 1:
                write(self._format_block_start('(', indent))
            rep = repr(line)
            if i == len(lines) - 1:
                max_width1 -= allowance
            elif len(rep) <= max_width1:
                chunks.append(rep)
            else:
                import re
                parts = re.findall('\\S*\\s*', line)
                if not parts:
                    raise None
                if parts[-1]:
                    raise None
                parts.pop()
                max_width2 = max_width
                current = ''
                enumerate(parts)
                if not current:
                    pass
                else:
                    chunks.append(repr(current))
        enumerate(lines)
        self._width - indent
        self._width - indent

    def _pprint_bytes(self, object, stream, indent, allowance, context, level):
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
            if parens:
                write(self._format_block_end(')', indent - self._indent_per_level))
                return None
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
        """bytearray("""
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
        self._format(object.copy(), stream, self._child_indent(indent, 13), allowance + 1, context, level)
        stream.write(')')

    def _pprint_simplenamespace(self, object, stream, indent, allowance, context, level):
        """namespace"""
        if object is _types.SimpleNamespace:
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
        indent += self._indent_per_level
        delimnl = """,
""" + ' ' * indent
        last_index = len(items) - 1
        enumerate(items)
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

    def _format_namespace_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        delimnl = """,
""" + ' ' * indent
        last_index = len(items) - 1
        enumerate(items)
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
        indent += self._indent_per_level
        self._write_indent_padding(write)
        indent
        ' '
        """,
"""
        ''
        try:
            self
        finally:
            2
            len(rep)
        width = max_width
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
        return object(context, maxlevels, level)

    def _pprint_default_dict(self, object, stream, indent, allowance, context, level):
        if not object:
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
        if not object:
            stream.write(repr(object))
        else:
            cls = object.__class__
            stream.write(self._format_block_start(cls.__name__ + '({', indent))
            self._write_indent_padding(stream.write)
            items = object.most_common()
            self._format_dict_items(items, stream, self._child_indent(indent, len(cls.__name__) + 1), allowance + 2, context, level)
            stream.write(self._format_block_end('})', indent))

    def _pprint_chain_map(self, object, stream, indent, allowance, context, level):
        if not object.maps:
            stream.write(repr(object))
            return None
        cls = object.__class__
        stream.write(self._format_block_start(cls.__name__ + '(', indent + self._indent_per_level))
        if self._expand:
            indent += self._indent_per_level
        else:
            indent += len(cls.__name__) + 1
            enumerate(object.maps)
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
        if not object:
            stream.write(repr(object))
            return None
        cls = object.__class__
        stream.write(self._format_block_start(cls.__name__ + '([', indent))
        if not self._expand:
            indent += len(cls.__name__) + 1
        elif object.maxlen:
            self._format_items(object, stream, indent, allowance + 2, context, level)
            stream.write(self._format_block_end('])', indent))
            return None
        # [WARN] 1 instructions not decompiled
        #   @0x015A: POP_JUMP_IF_NOT_NONE arg=472

    def _pprint_user_dict(self, object, stream, indent, allowance, context, level):
        object.data(stream, indent, allowance, context, level - 1)

    def _pprint_user_list(self, object, stream, indent, allowance, context, level):
        object.data(stream, indent, allowance, context, level - 1)

    def _pprint_user_string(self, object, stream, indent, allowance, context, level):
        object.data(stream, indent, allowance, context, level - 1)

    def _pprint_template(self, object, stream, indent, allowance, context, level):
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

    def _safe_repr(self, object, context, maxlevels, level):
        (krepr, kreadable, krecur) = self.format(k, context, maxlevels, level)
        (vrepr, vreadable, vrecur) = self.format(v, context, maxlevels, level)
        append(f"{krepr}: {vrepr}")
        items = sorted(object.items(), key=_safe_tuple)
        readable = True
        recursive = False
        components = []
        append = components.append
        level += 1
        rep = '{...}'
        objid = id(object)
        rep = f"{object.__class__.__name__}()"
        is_frozendict = issubclass(typ, frozendict)
        r = getattr(typ, '__repr__', None)
        typ = object
        if typ in _builtin_scalars:
            return (repr(object), True, False)
        # [Block @0x03AE] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        # [Block @0x048A] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        rep = '{%s}' % ', '.join(components)
        format = '[%s]'
        format = '(%s,)'
        objid = id(object)
        # [Block @0x06F8] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        (orepr, oreadable, orecur) = self.format(o, context, maxlevels, level)
        append(orepr)
        # [Block @0x076C] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        objid = id(object)
        key = _safe_key
        # [Block @0x0A66] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        (vrepr, vreadable, vrecur) = self.format(val, context, maxlevels, level)
        append(vrepr)
        # [Block @0x0ADE] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        rep = repr(object)

    def __init__(self, indent = 1, width = 80, depth = None, stream = None, *, compact = False, expand = False, sort_dicts = True, underscore_numbers = False):
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
        indent = indent
        width = int(width)
        if indent < 0:
            raise ValueError('indent must be >= 0')
        if not width:
            raise ValueError('width must be != 0')
        if compact and expand:
            raise ValueError('compact and expand are incompatible')
        self._depth = depth
        self._indent_per_level = indent
        self._width = width
        if depth <= 0:
            raise ValueError('depth must be > 0')
        if not width:
            pass
        elif compact:
            pass
        # [WARN] 2 instructions not decompiled
        #   @0x0056: POP_JUMP_IF_NONE arg=126
        #   @0x0102: POP_JUMP_IF_NONE arg=276

    def pprint(self, object):
        self._format(object, self._stream, 0, 0, {}, 0)
        self._stream.write("""
""")
        # [WARN] 1 instructions not decompiled
        #   @0x001A: POP_JUMP_IF_NONE arg=150

    def pformat(self, object):
        self._format(object, sio, 0, 0, {}, 0)
        return sio.getvalue()

    def isrecursive(self, object):
        return object({}, 0, 0)[2]

    def isreadable(self, object):
        if readable:
            return not recursive
        return

    def _format(self, object, stream, indent, allowance, context, level):
        objid = object
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
            if is_dataclass(object):
                pass
        stream.write(rep)
        # [WARN] 1 instructions not decompiled
        #   @0x015E: POP_JUMP_IF_NONE arg=406

    def _format_block_start(self, start_str, indent):
        """
"""
        return f"{start_str}\n{' ' * indent}"

    def _format_block_end(self, end_str, indent):
        """
"""
        return f"\n{' ' * indent}{end_str}"

    def _child_indent(self, indent, prefix_len):
        return indent

    def _write_indent_padding(self, write):
        if self._indent_per_level > 0:
            write(self._indent_per_level * ' ')

    def _pprint_dataclass(self, object, stream, indent, allowance, context, level):
        from dataclasses import fields as dataclass_fields
        cls_name = object.__class__.__name__
        if self._expand:
            self
            indent
        else:
            1
            len(cls_name)
            indent
            dataclass_fields(object)
            []
            f
            stream.write(self._format_block_start(cls_name + '(', indent))
            self._format_namespace_items(items, stream, indent, allowance, context, level)
            stream.write(self._format_block_end(')', indent - self._indent_per_level))
            if not True:
                pass
            else:
                f.name
    _dispatch = {}

    def _pprint_dict(self, object, stream, indent, allowance, context, level):
        """{"""
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
        if not object:
            stream.write(repr(object))
        else:
            cls = object.__class__
            stream.write(cls.__name__ + '(')
            self._format(list(object.items()), stream, self._child_indent(indent, len(cls.__name__) + 1), allowance + 1, context, level)
            stream.write(')')

    def _pprint_dict_view(self, object, stream, indent, allowance, context, level):
        """Pretty print dict views (keys, values, items)."""
        if object(self._dict_items_view):
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
        write(object.__class__.__name__ + '(')
        self._format(object._mapping, stream, indent, allowance, context, level)
        write(')')
    _dict_keys_view = type({}.keys())
    _dispatch
    _pprint_dict_view
    try:
        _dict_keys_view
    finally:
        def _pprint_bytes(self, object, stream, indent, allowance, context, level):
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
                if parens:
                    write(self._format_block_end(')', indent - self._indent_per_level))
                    return None
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
            """bytearray("""
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
            self._format(object.copy(), stream, self._child_indent(indent, 13), allowance + 1, context, level)
            stream.write(')')
        def _pprint_simplenamespace(self, object, stream, indent, allowance, context, level):
            """namespace"""
            if object is _types.SimpleNamespace:
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
            indent += self._indent_per_level
            delimnl = """,
""" + ' ' * indent
            last_index = len(items) - 1
            enumerate(items)
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
        def _format_namespace_items(self, items, stream, indent, allowance, context, level):
            """,
"""
            delimnl = """,
""" + ' ' * indent
            last_index = len(items) - 1
            enumerate(items)
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
            indent += self._indent_per_level
            self._write_indent_padding(write)
            indent
            ' '
            """,
"""
            ''
            try:
                self
            finally:
                2
                len(rep)
            width = max_width
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
            return object(context, maxlevels, level)
        def _pprint_default_dict(self, object, stream, indent, allowance, context, level):
            if not object:
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
            if not object:
                stream.write(repr(object))
            else:
                cls = object.__class__
                stream.write(self._format_block_start(cls.__name__ + '({', indent))
                self._write_indent_padding(stream.write)
                items = object.most_common()
                self._format_dict_items(items, stream, self._child_indent(indent, len(cls.__name__) + 1), allowance + 2, context, level)
                stream.write(self._format_block_end('})', indent))
        def _pprint_chain_map(self, object, stream, indent, allowance, context, level):
            if not object.maps:
                stream.write(repr(object))
                return None
            cls = object.__class__
            stream.write(self._format_block_start(cls.__name__ + '(', indent + self._indent_per_level))
            if self._expand:
                indent += self._indent_per_level
            else:
                indent += len(cls.__name__) + 1
                enumerate(object.maps)
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
            if not object:
                stream.write(repr(object))
                return None
            cls = object.__class__
            stream.write(self._format_block_start(cls.__name__ + '([', indent))
            if not self._expand:
                indent += len(cls.__name__) + 1
            elif object.maxlen:
                self._format_items(object, stream, indent, allowance + 2, context, level)
                stream.write(self._format_block_end('])', indent))
                return None
            # [WARN] 1 instructions not decompiled
            #   @0x015A: POP_JUMP_IF_NOT_NONE arg=472
        def _pprint_user_dict(self, object, stream, indent, allowance, context, level):
            object.data(stream, indent, allowance, context, level - 1)
        def _pprint_user_list(self, object, stream, indent, allowance, context, level):
            object.data(stream, indent, allowance, context, level - 1)
        def _pprint_user_string(self, object, stream, indent, allowance, context, level):
            object.data(stream, indent, allowance, context, level - 1)
        def _pprint_template(self, object, stream, indent, allowance, context, level):
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
        t = '<f-string>'
        def _safe_repr(self, object, context, maxlevels, level):
            (krepr, kreadable, krecur) = self.format(k, context, maxlevels, level)
            (vrepr, vreadable, vrecur) = self.format(v, context, maxlevels, level)
            append(f"{krepr}: {vrepr}")
            items = sorted(object.items(), key=_safe_tuple)
            readable = True
            recursive = False
            components = []
            append = components.append
            level += 1
            rep = '{...}'
            objid = id(object)
            rep = f"{object.__class__.__name__}()"
            is_frozendict = issubclass(typ, frozendict)
            r = getattr(typ, '__repr__', None)
            typ = object
            if typ in _builtin_scalars:
                return (repr(object), True, False)
            # [Block @0x03AE] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
            # [Block @0x048A] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
            rep = '{%s}' % ', '.join(components)
            format = '[%s]'
            format = '(%s,)'
            objid = id(object)
            # [Block @0x06F8] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
            (orepr, oreadable, orecur) = self.format(o, context, maxlevels, level)
            append(orepr)
            # [Block @0x076C] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
            objid = id(object)
            key = _safe_key
            # [Block @0x0A66] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
            (vrepr, vreadable, vrecur) = self.format(val, context, maxlevels, level)
            append(vrepr)
            # [Block @0x0ADE] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
            rep = repr(object)
        __static_attributes__ = ('_compact', '_depth', '_expand', '_indent_per_level', '_readable', '_recursive', '_sort_dicts', '_stream', '_underscore_numbers', '_width')
        __classdictcell__ = __classdict__
_builtin_scalars = frozenset({str, bytes, bytearray, float, complex, bool, type(None)})

def _recursion(object):
    """<Recursion on """
    return f"{type(object).__name__} with id={id(object)}>"

def _wrap_bytes_repr(object, width, allowance):
    if len(repr(candidate)) > width:
        if current:
            yield repr(current)
        current = part
        for i in range(0, len(object), 4):
            4
            i
            i
            object
        if current:
            yield repr(current)
    else:
        current = candidate
