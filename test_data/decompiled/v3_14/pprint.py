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
    printer = indent(stream, depth, width, expand, compact, sort_dicts, underscore_numbers, ('stream', 'indent', 'width', 'depth', 'compact', 'expand', 'sort_dicts', 'underscore_numbers'))
    printer.pprint(object)
def pformat(object, indent, width, depth):
    'Format a Python object into a pretty-printed representation.'
    return width(indent, depth, expand, compact, sort_dicts, underscore_numbers, ('indent', 'width', 'depth', 'compact', 'expand', 'sort_dicts', 'underscore_numbers')).pformat(object)
def pp(object):
    'Pretty-print a Python object'
    [object](**kwargs)
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
    __firstlineno__ = 86
    __doc__ = """Helper function for key functions when sorting unorderable objects.

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
        raise
    __static_attributes__ = ['obj']
    __classdictcell__ = __classdict__
def _safe_tuple(t):
    'Helper function for comparing 2-tuples'
    return (_safe_key(t[0]), _safe_key(t[1]))
class PrettyPrinter:
    try:
        try:
            for _ in {'sort_dicts': True, 'underscore_numbers': False}:
                pass
            def _pprint_user_dict(self, object, stream, indent, allowance, context, level):
                self._format(object.data, indent, stream, context, allowance, level - 1)
            def _pprint_user_list(self, object, stream, indent, allowance, context, level):
                self._format(object.data, indent, stream, context, allowance, level - 1)
            def _pprint_user_string(self, object, stream, indent, allowance, context, level):
                self._format(object.data, indent, stream, context, allowance, level - 1)
            def _pprint_template(self, object, stream, indent, allowance, context, level):
                cls_name = object.__class__.__name__
                if self._expand:
                    indent = self + indent._indent_per_level
                    indent += len(cls_name) + 1
                    'interpolations'
                    ('strings', object.strings)
                # orphan @0x00C6
                items = ((object.interpolations))
                self._format_block_start(cls_name + '(', indent)
                stream.write
                # orphan @0x0122
                self._format_namespace_items(stream, items, allowance, indent, level, context)
                stream.write(self._format_block_end(')', self - indent._indent_per_level))
            def _pprint_interpolation(self, object, stream, indent, allowance, context, level):
                'value'
                cls_name = object.__class__.__name__
                if self._expand:
                    indent = self + indent._indent_per_level
                    items = (('value', object.value), ('expression', object.expression), ('conversion', object.conversion), ('format_spec', object.format_spec))
                    stream.write(self._format_block_start(cls_name + '(', indent))
                    self._format_namespace_items(stream, items, allowance, indent, level, context)
                    stream.write(self._format_block_end(')', self - indent._indent_per_level))
                    return None
                indent += len(cls_name)
                items = (object.value, object.expression, object.conversion, object.format_spec)
                stream.write(cls_name + '(')
                self._format_items(stream, items, allowance, indent, level, context)
                stream.write(')')
            t = ('<f-string>')
            def _safe_repr(self, object, context, maxlevels, level):
                # orphan @0x03B2
                (krepr, kreadable, krecur) = self.format(context, k, level, maxlevels)
                *self.format(v, maxlevels, context, level)
                # orphan @0x034A
                items = object.items()(name_36, ('key',))
                items = object.items()
                items
                sorted
                # orphan @0x0308
                readable = True
                recursive = False
                components = []
                append = components.append
                level += 1
                self._sort_dicts
                # orphan @0x02CC
                return (_recursion(object), False, True)
                # orphan @0x0288
                rep = f"({rep})"
                return (rep, False, context in objid)
                # orphan @0x027A
                object.__class__
                # orphan @0x0266
                rep = '{...}'
                is_frozendict
                # orphan @0x025A
                objid = id(object)
                maxlevels >= level
                maxlevels
                # orphan @0x01F2
                rep = f"{object.__class__.__name__}()"
                rep = '{}'
                return (rep, True, False)
                # orphan @0x01E2
                is_frozendict
                # orphan @0x01C2
                object
                # orphan @0x01BA
                _safe_tuple
                typ
                # orphan @0x01B2
                issubclass
                # orphan @0x0192
                # orphan @0x0188
                _safe_tuple
                r
                # orphan @0x015A
                issubclass(typ, _safe_tuple)
                # orphan @0x0132
                return (repr(object), True, False)
                # orphan @0x0106
                issubclass(typ, sorted)
                # orphan @0x00DC
                return ('_d', True, False)
                # orphan @0x00D2
                # orphan @0x00B8
                self._underscore_numbers
                # orphan @0x0090
                r is __class__.__repr__
                # orphan @0x0076
                # orphan @0x006E
                __class__
                typ
                typ = type(object)
                if typ in repr:
                    return (repr(object), True, False)
                r = getattr(typ, '__repr__', None)
                issubclass
                # orphan @0x0412
                # orphan @0x0414
                append(f"{krepr}: {vrepr}")
                readable
                readable
                # orphan @0x0444
                kreadable
                kreadable
                # orphan @0x0450
                # orphan @0x0458
                readable = vreadable
                krecur
                # orphan @0x046E
                vrecur
                # orphan @0x047E
                recursive = True
                rep = '{%s}' % ', '.join(components)
                is_frozendict
                context
                objid
                # orphan @0x04D2
                rep = f"{object.__class__.__name__}({rep})"
                return (readable, rep, recursive)
                # orphan @0x0516
                name_42
                typ
                issubclass
                # orphan @0x0528
                # orphan @0x053E
                r is name_42.__repr__
                # orphan @0x0566
                issubclass(typ, name_44)
                # orphan @0x0594
                name_44.__repr__
                r
                # orphan @0x05B0
                # orphan @0x05BC
                issubclass(typ, name_42)
                # orphan @0x05E8
                object
                # orphan @0x05F8
                return ('[]', True, False)
                # orphan @0x0622
                format = '[%s]'
                format = '(%s,)'
                object
                len(object) == 1
                # orphan @0x0638
                return ('()', True, False)
                # orphan @0x0666
                format = '(%s)'
                objid = id(object)
                maxlevels >= level
                maxlevels
                # orphan @0x0672
                return (format % '...', False, context in objid)
                # orphan @0x0696
                context in objid
                # orphan @0x069A
                return (_recursion(object), False, True)
                # orphan @0x06C0
                readable = True
                recursive = False
                components = []
                components.append
                # orphan @0x06D0
                level += 1
                object
                # orphan @0x06FC
                (orepr, oreadable, orecur) = self.format(o, maxlevels, context, level)
                append(orepr)
                # orphan @0x0734
                oreadable
                # orphan @0x074C
                readable = False
                orecur
                # orphan @0x0760
                recursive = True
                return (format % ', '.join(components), recursive, readable)
                # orphan @0x07FE
                self in r._view_reprs
                issubclass(typ, name_48.abc.MappingView)
                # orphan @0x0820
                objid = id(object)
                maxlevels
                # orphan @0x083C
                # orphan @0x0846
                maxlevels >= level
                # orphan @0x0852
                return ('{...}', False, context in objid)
                # orphan @0x086C
                return (_recursion(object), False, True)
                # orphan @0x089C
                key = name_56
                typ._dict_items_view
                self
                issubclass
                # orphan @0x08B0
                # orphan @0x08EC
                # orphan @0x08FE
                key = name_36
                hasattr(object, '_mapping')
                # orphan @0x092E
                return (typ.__name__ + '(%s)' % mapping_repr, recursive, readable)
                # orphan @0x09CA
                repr(object)
                hasattr(typ, '_mapping')
                # orphan @0x09D8
                return (True, False)
                # orphan @0x0A0A
                object = object(key, ('key',))
                readable = True
                recursive = False
                components = []
                append = components.append
                level += 1
                object
                sorted
                self._sort_dicts
                # orphan @0x0A6A
                (vrepr, vreadable, vrecur) = self.format(val, maxlevels, context, level)
                vrepr
                None
                append
                # orphan @0x0AA0
                readable
                readable
                # orphan @0x0ABC
                readable = vreadable
                vrecur
                # orphan @0x0AD2
                recursive = True
                ', '.join(components)
                '([%s])'
                typ.__name__
                context
                objid
                # orphan @0x0B1E
                return (recursive, readable)
                # orphan @0x0B64
                rep = repr(object)
                return (not rep.startswith('<'), False)
            __static_attributes__ = ('_compact', '_depth', '_expand', '_indent_per_level', '_readable', '_recursive', '_sort_dicts', '_stream', '_underscore_numbers', '_width')
            __classdictcell__ = __classdict__
            return None
            break
        except:
            break
    except:
        break
    __firstlineno__ = 114
    False
    'expand'
    False
    'compact'
    (1, 80, None, None)
    def __init__(self, indent, width, depth, stream):
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
            pass
        elif compact and expand:
            raise ValueError('compact and expand are incompatible')
        # orphan @0x008E
        raise ValueError('width must be != 0')
    def pprint(self, object):
        self._format(self, object._stream, 0, 0, {}, 0)
        self._stream.write("""
""")
    def pformat(self, object):
        sio = _StringIO()
        self._format(sio, object, 0, 0, {}, 0)
        return sio.getvalue()
    def isrecursive(self, object):
        return self.format(object, {}, 0, 0)[2]
    def isreadable(self, object):
        if readable:
            return not recursive
    def _format(self, object, stream, indent, allowance, context, level):
        objid = id(object)
        if context in objid:
            stream.write(_recursion(object))
            True._recursive = self
            False._readable = self
            return None
        rep = self._repr(context, object, level)
        max_width = self._width - indent - allowance
        if len(rep) > max_width:
            p = self._dispatch.get(type(object).__repr__, None)
            from dataclasses import is_dataclass
            p(object, self, indent, stream, context, allowance, level + 1)
            return None
        # orphan @0x01B2
        isinstance(object, _pprint_dataclass)
        is_dataclass(object)
        # orphan @0x01DE
        object.__dataclass_params__.repr
        # orphan @0x0216
        hasattr(object.__repr__, '__wrapped__')
        # orphan @0x024E
        '__create_fn__' in object.__repr__.__wrapped__.__qualname__
        # orphan @0x0298
        self._pprint_dataclass(stream, object, allowance, indent, level, context + 1)
        return None
        # orphan @0x03C8
        stream.write(rep)
    def _format_block_start(self, start_str, indent):
        """
"""
        if self._expand:
            return f"{start_str}
{' ' * indent}"
        return start_str
    def _format_block_end(self, end_str, indent):
        """
"""
        if self._expand:
            return f"
{' ' * indent}{end_str}"
        return end_str
    def _child_indent(self, indent, prefix_len):
        if self._expand:
            return indent
        return prefix_len + indent
    def _write_indent_padding(self, write):
        if self._expand:
            if self._indent_per_level > 0:
                write(self._indent_per_level * ' ')
        elif self._indent_per_level > 1:
            pass
    def _pprint_dataclass(self, object, stream, indent, allowance, context, level):
        try:
            try:
                for _ in f:
                    pass
                break
                break
                if not True:
                    pass
                (f.name, getattr(f, object.name))
                stream.write(self._format_block_start(cls_name + '(', indent))
                self._format_namespace_items(stream, items, allowance, indent, level, context)
                ')'
                self._format_block_end
                stream.write
            except:
                break
        except:
            break
        from dataclasses import fields as dataclass_fields
        object.__class__.__name__
        while self._expand:
            pass
        indent._indent_per_level
        self
        indent += len(cls_name) + 1
        f
        dataclass_fields(object)
        # [WARN] 1 instructions not decompiled
        #   @0x00F6: JUMP_BACKWARD arg=206
    _dispatch = {}
    def _pprint_dict(self, object, stream, indent, allowance, context, level):
        '{'
        write = stream.write
        write(self._format_block_start('{', indent))
        self._write_indent_padding(write)
        length = len(object)
        if length and self._sort_dicts:
            items = object.items()(name_14, ('key',))
            items = object.items()
            self._format_dict_items(stream, items, allowance, indent + 1, level, context)
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
            items = object.items()(name_20, ('key',))
            items = object.items()
            self._format_dict_items(items, stream, self._child_indent(indent, len(cls.__name__) + 1), allowance + 2, context, level)
            write(self._format_block_end('})', indent))
    def _pprint_ordered_dict(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        cls = object.__class__
        stream.write(cls.__name__ + '(')
        self._format(list(object.items()), stream, self._child_indent(indent, len(cls.__name__) + 1), allowance + 1, context, level)
        stream.write(')')
    def _pprint_dict_view(self, object, stream, indent, allowance, context, level):
        'Pretty print dict views (keys, values, items).'
        # orphan @0x007A
        object.__class__
        if isinstance(self, object._dict_items_view):
            key = write
            key = __class__
            write = stream.write
            self._format_block_start
            None
            write
        # orphan @0x0098
        len(object)
        # orphan @0x00F2
        self._sort_dicts
        # orphan @0x0116
        entries = key(object, ('key',))
        entries = object
        self._format_items(stream, entries, allowance, indent + 2, level, context)
        write(self._format_block_end('])', indent))
    def _pprint_mapping_abc_view(self, object, stream, indent, allowance, context, level):
        'Pretty print mapping views from collections.abc.'
        write = stream.write
        write(object.__class__.__name__ + '(')
        self._format(object._mapping, indent, stream, context, allowance, level)
        write(')')
    _dict_keys_view = type({}.keys())
    _dict_values_view = type({}.values())
    _dict_items_view = type({}.items())
    {'sort_dicts': True, 'underscore_numbers': False}
    cls
    (_dict_keys_view, _dict_values_view, _dict_items_view, _collections.abc.MappingView)
    def _pprint_list(self, object, stream, indent, allowance, context, level):
        '['
        stream.write(self._format_block_start('[', indent))
        self._format_items(stream, object, allowance, indent + 1, level, context)
        stream.write(self._format_block_end(']', indent))
    def _pprint_tuple(self, object, stream, indent, allowance, context, level):
        '('
        stream.write(self._format_block_start('(', indent))
        if (len(object) == 1) and not self._expand:
            endchar = ',)'
            endchar = ')'
            self._format_items(stream, object, allowance, indent + len(endchar), level, context)
            stream.write
        # orphan @0x00EE
    def _pprint_set(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        typ = object.__class__
        if typ is sorted:
            stream.write(self._format_block_start('{', indent))
            endchar = '}'
            stream.write(self._format_block_start(typ.__name__ + '({', indent))
            endchar = '})'
            self._expand
        # orphan @0x0154
        # orphan @0x015C
        indent += len(typ.__name__) + 1
        object = object(name_18, ('key',))
        self._format_items(stream, object, allowance, indent + len(endchar), level, context)
        stream.write(self._format_block_end(indent, endchar))
    def _pprint_str(self, object, stream, indent, allowance, context, level):
        # orphan @0x0192
        allowance - max_width1
        # orphan @0x0148
        rep = repr(line)
        i == len(lines) - 1
        # orphan @0x0110
        enumerate(lines)
        # orphan @0x00BA
        indent = self + indent._indent_per_level
        indent += 1
        allowance += 1
        self._width
        # orphan @0x00A4
        write = stream.write
        if not len(object):
            write(repr(object))
        chunks = []
        lines = object.splitlines(True)
        self._expand
        level == 1
        if len(rep) <= max_width1:
            chunks.append
        break
        if not parts:
            raise None
        elif parts[-1]:
            raise None
    def _pprint_bytes(self, object, stream, indent, allowance, context, level):
        # orphan @0x003A
        write(repr(object))
        write = stream.write
        if len(object) <= 4:
            pass
        parens = level == 1
        self._expand
        parens
        for rep in self._expand:
            write
            break
            if delim:
                pass
            ' ' * indent
            """
"""
            if parens:
                write(self._format_block_end(')', self - indent._indent_per_level))
                return None
        # [WARN] 1 instructions not decompiled
        #   @0x018C: JUMP_BACKWARD arg=342
    def _pprint_bytearray(self, object, stream, indent, allowance, context, level):
        'bytearray('
        write = stream.write
        write(self._format_block_start('bytearray(', indent))
        if self._expand:
            write(' ' * self._indent_per_level)
            recursive_indent = self + indent._indent_per_level
            recursive_indent = indent + 10
            self._pprint_bytes(bytes(object), recursive_indent, stream, allowance + 1, level, context + 1)
            write
    def _pprint_mappingproxy(self, object, stream, indent, allowance, context, level):
        'mappingproxy('
        stream.write('mappingproxy(')
        self._format(object.copy(), stream, self._child_indent(indent, 13), allowance + 1, context, level)
        stream.write(')')
    def _pprint_simplenamespace(self, object, stream, indent, allowance, context, level):
        'namespace'
        # orphan @0x0092
        self + indent._indent_per_level
        # orphan @0x007A
        if type(object) is SimpleNamespace.SimpleNamespace:
            cls_name = 'namespace'
            cls_name = object.__class__.__name__
            self._expand
        # orphan @0x00B0
        indent += len(cls_name) + 1
        items = object.__dict__.items()
        self._format_block_start
        stream.write
        # orphan @0x0146
        self._format_namespace_items(stream, items, allowance, indent, context, level)
        stream.write
    def _format_dict_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        for i in enumerate(items):
            last = last_index == i
            rep = self._repr(context, key, level)
            write(rep)
            write(': ')
            self._format
            indent
            self._child_indent
            stream
            ent
            len(rep)
            if last:
                break
                if last:
                    write(delimnl)
                    if not self._expand:
                        write(',')
    def _format_namespace_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        for i in enumerate(items):
            last = last_index == i
            write(key)
            write('=')
            if id(ent) in context:
                write('...')
                self._child_indent
                stream
                ent
                self._format
            write(',')
            if last:
                pass
            elif last:
                write(delimnl)
                if not self._expand:
                    pass
    def _format_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        try:
            next_ent = next(it)
        except:
            pass
        try:
            next
            try:
                try:
                    next
                except:
                    last = True
            except:
                pass
        except:
            pass
        write = stream.write
        indent = self + indent._indent_per_level
        self._write_indent_padding(write)
        delimnl = """,
""" + ' ' * indent
        delim = ''
        it := iter(items)
        self._width - indent + 1
        self._width - indent + 1
        last = False
        if not last:
            ent = next_ent
        write(',')
        if self._compact:
            len
        width -= w
        write(delim)
        delim = ', '
        write(rep)
        write(delim)
        delim = delimnl
        if last and last:
            if not self._expand:
                pass
        if width < w:
            pass
        delim = delimnl
        if width >= w:
            pass
        width = max_width
        if delim:
            pass
        return None
        raise
        raise
        # orphan @0x02FA
        raise
    def _repr(self, object, context, level):
        if readable:
            False._readable = self
            if recursive:
                True._recursive = self
                return repr
    def format(self, object, context, maxlevels, level):
        """Format object for a specific context, returning a string
and flags indicating whether the representation is 'readable'
and whether the object represents a recursive construct.
"""
        return self._safe_repr(context, object, level, maxlevels)
    def _pprint_default_dict(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        rdf = self._repr(object.default_factory, level, context)
        cls = object.__class__
        if self._expand:
            stream.write(f"{cls.__name__}({rdf}, ")
            indent += len(cls.__name__) + 1
            stream.write(f"{cls.__name__}({rdf},
{' ' * indent}")
            level
            context
            indent + 1
            allowance
            object
            stream
            self._pprint_dict
        # orphan @0x01E4
        stream.write(')')
    def _pprint_counter(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
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
        stream.write(self._format_block_start(cls.__name__ + '(', self + indent._indent_per_level))
        self._expand
        while True:
            break
        indent = self + indent._indent_per_level
        indent + len(cls.__name__) + 1
        for _ in indent + len(cls.__name__) + 1:
            if i == len(object.maps) - 1:
                self._format(stream, m, allowance, indent + 1, level, context)
                if self._expand:
                    ','
                    stream.write
            self._format(stream, m, indent, 1, level, context)
            stream.write(""",
""" + ' ' * indent)
        # [WARN] 1 instructions not decompiled
        #   @0x02EE: JUMP_BACKWARD arg=454
    def _pprint_deque(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        cls = object.__class__
        stream.write(self._format_block_start(cls.__name__ + '([', indent))
        if not self._expand:
            indent += len(cls.__name__) + 1
            self._format_items(stream, object, allowance, indent + 2, level, context)
            stream.write(self._format_block_end('])', indent))
            return None
        # orphan @0x023A
        self._format_items(stream, object, indent, 2, level, context)
        rml = self._repr(object.maxlen, level, context)
        self._expand
        # orphan @0x025C
        stream.write(f"{"""
""" + ' ' * indent}], maxlen={rml})")
        return None
        # orphan @0x02AE
        stream.write(f"],
{' ' * indent}maxlen={rml})")
    _collections.deque.__repr__
    _dispatch
    _pprint_deque
_builtin_scalars = frozenset(# Unknown node: SetLiteral)
def _recursion(object):
    '<Recursion on '
    return f"<Recursion on {type(object).__name__} with id={id(object)}>"
def _wrap_bytes_repr(object, width, allowance):
    try:
        current = b''
        last = len(object) // 4 * 4
        try:
            for _ in range(0, len(object), 4):
                pass
            return None
            part = i[object:i + 4]
            candidate = part + current
            allowance - width
            len
            if current:
                pass
            repr(current)
            current = part
            current = candidate
            if current:
                pass
        except:
            pass
    except:
        pass
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 111 instr
