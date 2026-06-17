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
            try:
                if str:
                    pass
            except:
                pass
        except:
            pass
        return
        return
    __static_attributes__ = ['obj']
    __classdictcell__ = __classdict__
def _safe_tuple(t):
    'Helper function for comparing 2-tuples'
    return (_safe_key(t[0]), _safe_key(t[1]))
class PrettyPrinter:
    try:
        try:
            for _ in (1, 80, None, None):
                pass
            def _pprint_user_list(self, object, stream, indent, allowance, context, level):
                self._format(object.data, indent, stream, context, allowance, level - 1)
            def _pprint_user_string(self, object, stream, indent, allowance, context, level):
                self._format(object.data, indent, stream, context, allowance, level - 1)
            def _pprint_template(self, object, stream, indent, allowance, context, level):
                cls_name = object.__class__.__name__
                if self._expand:
                    indent = self + indent._indent_per_level
                    indent += len(cls_name) + 1
                    items = (('strings', object.strings), ('interpolations', object.interpolations))
                self._format_namespace_items(stream, items, allowance, indent, level, context)
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
                # orphan @0x01BE
                indent += len(cls_name)
                items = (object.value, object.expression, object.conversion, object.format_spec)
                stream.write(cls_name + '(')
                self._format_items(stream, items, allowance, indent, level, context)
                stream.write(')')
            t = ('<f-string>')
            def _safe_repr(self, object, context, maxlevels, level):
                # orphan @0x03B2
                (krepr, kreadable, krecur) = self.format(context, k, level, maxlevels)
                (vrepr, vreadable, vrecur) = self.format(v, maxlevels, context, level)
                append(f"{krepr}: {vrepr}")
                # orphan @0x038A
                items = object.items()
                # orphan @0x0348
                readable = True
                recursive = False
                components = []
                append = components.append
                level += 1
                items = object.items()(name_36, ('key',))
                # orphan @0x02DA
                return (False, True)
                # orphan @0x02CA
                # orphan @0x0278
                rep = f"{object.__class__.__name__}({rep})"
                return (rep, False, context in objid)
                # orphan @0x0264
                rep = '{...}'
                # orphan @0x025E
                # orphan @0x0258
                # orphan @0x0236
                objid = id(object)
                # orphan @0x01F0
                rep = f"{object.__class__.__name__}()"
                rep = '{}'
                return (rep, True, False)
                # orphan @0x01E0
                # orphan @0x01C0
                # orphan @0x01B0
                # orphan @0x0186
                # orphan @0x0158
                # orphan @0x0130
                return (repr(object), True, False)
                # orphan @0x0106
                # orphan @0x00DA
                return ('_d', True, False)
                # orphan @0x00B6
                # orphan @0x008E
                r = getattr(typ, '__repr__', None)
                # orphan @0x002C
                return (repr(object), True, False)
                # orphan @0x0000
                typ = type(object)
                # orphan @0x0442
                # orphan @0x044E
                # orphan @0x0456
                readable = vreadable
                # orphan @0x046C
                # orphan @0x047C
                # orphan @0x0482
                recursive = True
                rep = '{%s}' % ', '.join(components)
                # orphan @0x04D0
                rep = f"{object.__class__.__name__}({rep})"
                return (readable, rep, recursive)
                # orphan @0x053C
                # orphan @0x055E
                # orphan @0x0564
                # orphan @0x056C
                # orphan @0x0574
                # orphan @0x0592
                # orphan @0x05BA
                # orphan @0x05BE
                # orphan @0x05E6
                # orphan @0x05F6
                return ('[]', True, False)
                # orphan @0x0620
                format = '[%s]'
                format = '(%s,)'
                # orphan @0x0636
                return ('()', True, False)
                # orphan @0x0664
                format = '(%s)'
                objid = id(object)
                # orphan @0x0670
                return (format % '...', False, context in objid)
                # orphan @0x0698
                return (_recursion(object), False, True)
                # orphan @0x06FC
                readable = True
                recursive = False
                components = []
                append = components.append
                level += 1
                o = object
                (orepr, oreadable, orecur) = self.format(o, maxlevels, context, level)
                append(orepr)
                # orphan @0x0744
                # orphan @0x074A
                readable = False
                # orphan @0x075E
                # orphan @0x0766
                return (format % ', '.join(components), recursive, readable)
                # orphan @0x07FC
                # orphan @0x081E
                objid = id(object)
                # orphan @0x0844
                # orphan @0x0850
                return ('{...}', False, context in objid)
                # orphan @0x086A
                return (_recursion(object), False, True)
                # orphan @0x08A8
                key = name_56
                # orphan @0x08AE
                # orphan @0x08F6
                # orphan @0x08FC
                key = name_36
                # orphan @0x092C
                # orphan @0x093E
                return (typ.__name__ + '(%s)' % mapping_repr, recursive, readable)
                # orphan @0x09C8
                return (repr(object), True, False)
                # orphan @0x0A08
                object = object(key, ('key',))
                readable = True
                recursive = False
                # orphan @0x0A34
                components = []
                append = components.append
                level += 1
                # orphan @0x0A6A
                (vrepr, vreadable, vrecur) = self.format(val, maxlevels, context, level)
                append(vrepr)
                # orphan @0x0ABA
                readable = vreadable
                # orphan @0x0AD0
                recursive = True
                # orphan @0x0AF4
                # orphan @0x0B1E
                return (recursive, readable)
                # orphan @0x0B4C
                rep = repr(object)
                # orphan @0x0B62
                # orphan @0x0B94
                return
            __static_attributes__ = ('_compact', '_depth', '_expand', '_indent_per_level', '_readable', '_recursive', '_sort_dicts', '_stream', '_underscore_numbers', '_width')
            __classdictcell__ = __classdict__
            return None
            break
        except:
            break
    except:
        break
    __firstlineno__ = 114
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
        # orphan @0x007E
        # orphan @0x0066
        raise ValueError('depth must be > 0')
        # orphan @0x0052
        indent = int(indent)
        width = int(width)
        if indent < 0:
            raise ValueError('indent must be >= 0')
        raise
        if compact and expand:
            raise ValueError('compact and expand are incompatible')
        # orphan @0x008C
        # orphan @0x00DA
        self._depth = depth
        self._indent_per_level = indent
        self._width = width
        # orphan @0x00FE
        self._stream = stream
        _underscore_numbers.stdout._stream = self
        # orphan @0x0148
        bool(expand)._expand = self
        self._sort_dicts = sort_dicts
        self._underscore_numbers = underscore_numbers
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
        # orphan @0x00EE
        rep = self._repr(context, object, level)
        max_width = self._width - indent - allowance
        p = self._dispatch.get(type(object).__repr__, None)
        objid = id(object)
        if context in objid:
            stream.write(_recursion(object))
            True._recursive = self
            False._readable = self
            return None
        from dataclasses import is_dataclass
        p(object, self, indent, stream, context, allowance, level + 1)
        # orphan @0x01B0
        # orphan @0x01DC
        # orphan @0x0214
        # orphan @0x024C
        # orphan @0x0296
        self._pprint_dataclass(stream, object, allowance, indent, level, context + 1)
        return None
        # orphan @0x03EE
        stream.write(rep)
    def _format_block_start(self, start_str, indent):
        """
"""
        if self._expand:
            return f"{start_str}
{' ' * indent}"
        # orphan @0x0042
        return start_str
    def _format_block_end(self, end_str, indent):
        """
"""
        if self._expand:
            return f"
{' ' * indent}{end_str}"
        # orphan @0x0042
        return end_str
    def _child_indent(self, indent, prefix_len):
        if self._expand:
            return indent
        # orphan @0x002A
        return prefix_len + indent
    def _write_indent_padding(self, write):
        if self._expand and (self._indent_per_level > 0):
            write(self._indent_per_level * ' ')
            return None
        # orphan @0x0082
    def _pprint_dataclass(self, object, stream, indent, allowance, context, level):
        try:
            try:
                for _ in f:
                    pass
                break
            except:
                break
        except:
            break
        from dataclasses import fields as dataclass_fields
        cls_name = object.__class__.__name__
        if self._expand:
            indent = self + indent._indent_per_level
            indent += len(cls_name) + 1
        if not True:
            pass
        break
        self._format_namespace_items(stream, items, allowance, indent, level, context)
        # [WARN] 1 instructions not decompiled
        #   @0x00F6: JUMP_BACKWARD arg=390
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
        if isinstance(self, object._dict_items_view):
            key = write
            key = __class__
            write = stream.write
        elif len(object) and self._sort_dicts:
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
    def _pprint_set(self, object, stream, indent, allowance, context, level):
        # orphan @0x0086
        typ = object.__class__
        stream.write(self._format_block_start('{', indent))
        endchar = '}'
        if not len(object):
            stream.write(repr(object))
            return None
        endchar = '})'
        if not self._expand:
            indent += len(typ.__name__) + 1
            object = object(name_18, ('key',))
        # orphan @0x0202
        stream.write(self._format_block_end(indent, endchar))
    def _pprint_str(self, object, stream, indent, allowance, context, level):
        # orphan @0x0190
        max_width1 = allowance - max_width1
        # orphan @0x0148
        rep = repr(line)
        # orphan @0x00C4
        indent += 1
        allowance += 1
        # orphan @0x00B8
        # orphan @0x0094
        chunks = []
        lines = object.splitlines(True)
        # orphan @0x003A
        write(repr(object))
        return None
        # orphan @0x0000
        write = stream.write
        # orphan @0x01C0
        # orphan @0x01E0
        # orphan @0x01E4
        import re
        parts = re.findall('\\S*\\s*', line)
        # orphan @0x0222
        raise None
        # orphan @0x0228
        # orphan @0x0244
        raise None
        # orphan @0x024A
        # orphan @0x0252
        max_width2 = max_width
        current = ''
        # orphan @0x028C
        candidate = current + part
        # orphan @0x02D2
        # orphan @0x0300
        max_width2 -= allowance
        # orphan @0x0344
        # orphan @0x0346
        # orphan @0x0354
        chunks.append(repr(current))
        current = part
        current = candidate
        # orphan @0x03AC
        # orphan @0x03DC
        # orphan @0x0410
        write(rep)
        return None
        # orphan @0x0432
        # orphan @0x0446
        # orphan @0x047E
        # orphan @0x048A
        # orphan @0x0490
        write("""
""" + ' ' * indent)
        write(rep)
        # orphan @0x04E2
        write(self._format_block_end(')', self - indent._indent_per_level))
    def _pprint_bytes(self, object, stream, indent, allowance, context, level):
        # orphan @0x00B2
        indent += 1
        allowance += 1
        write(self._format_block_start('(', indent))
        delim = ''
        # orphan @0x009C
        # orphan @0x0078
        parens = level == 1
        # orphan @0x0038
        write(repr(object))
        return None
        # orphan @0x0000
        write = stream.write
        # orphan @0x015A
        write(delim)
        write(rep)
        # orphan @0x018A
        # orphan @0x019E
        # orphan @0x01AC
        # orphan @0x01C6
        write(self._format_block_end(')', self - indent._indent_per_level))
    def _pprint_bytearray(self, object, stream, indent, allowance, context, level):
        'bytearray('
        write = stream.write
        write(self._format_block_start('bytearray(', indent))
        if self._expand:
            write(' ' * self._indent_per_level)
            recursive_indent = self + indent._indent_per_level
            recursive_indent = indent + 10
            self._pprint_bytes(bytes(object), recursive_indent, stream, allowance + 1, level, context + 1)
            write(self._format_block_end(')', indent))
    def _pprint_mappingproxy(self, object, stream, indent, allowance, context, level):
        'mappingproxy('
        stream.write('mappingproxy(')
        self._format(object.copy(), stream, self._child_indent(indent, 13), allowance + 1, context, level)
        stream.write(')')
    def _pprint_simplenamespace(self, object, stream, indent, allowance, context, level):
        'namespace'
        if type(object) is SimpleNamespace.SimpleNamespace:
            cls_name = 'namespace'
            cls_name = object.__class__.__name__
        indent = self + indent._indent_per_level
        indent += len(cls_name) + 1
        items = object.__dict__.items()
        # orphan @0x012A
        self._format_namespace_items(stream, items, allowance, indent, context, level)
    def _format_dict_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        # orphan @0x009C
        last = last_index == i
        rep = self._repr(context, key, level)
        write(rep)
        write(': ')
        # orphan @0x0000
        write = stream.write
        indent = self + indent._indent_per_level
        delimnl = """,
""" + ' ' * indent
        last_index = len(items) - 1
        # orphan @0x015E
        # orphan @0x0182
        write(delimnl)
        # orphan @0x01BA
        write(',')
    def _format_namespace_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        # orphan @0x0078
        last = last_index == i
        write(key)
        write('=')
        # orphan @0x0000
        write = stream.write
        delimnl = """,
""" + ' ' * indent
        last_index = len(items) - 1
        # orphan @0x00CA
        write('...')
        # orphan @0x0148
        # orphan @0x016C
        write(delimnl)
        # orphan @0x01A4
        write(',')
    def _format_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        try:
            next_ent = next(it)
        except:
            pass
        try:
            next_ent = next(it)
        except:
            last = True
        write = stream.write
        indent = self + indent._indent_per_level
        self._write_indent_padding(write)
        delimnl = """,
""" + ' ' * indent
        delim = ''
        last = False
        if not last:
            ent = next_ent
        if self._compact:
            w = len(rep) + 2
            if width < w:
                width = max_width
                if delim:
                    delim = delimnl
                    if width >= w:
                        width -= w
                        write(delim)
                        delim = ', '
                        write(rep)
                        write(delim)
                        delim = delimnl
                        if last and last:
                            pass
                        write(',')
                        return None
        return None
        raise
        raise
        raise
    def _repr(self, object, context, level):
        if readable:
            pass
        else:
            False._readable = self
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
        indent += len(cls.__name__) + 1
        stream.write(f"{cls.__name__}({rdf},
{' ' * indent}")
        self._pprint_dict(stream, object, allowance, indent + 1, context, level)
        stream.write(')')
        # orphan @0x00CE
        rdf = self._repr(object.default_factory, level, context)
        cls = object.__class__
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
        # orphan @0x0036
        stream.write(repr(object))
        return None
        # orphan @0x0000
        while True:
            pass
        # orphan @0x012E
        cls = object.__class__
        stream.write(self._format_block_start(cls.__name__ + '(', self + indent._indent_per_level))
        # orphan @0x0142
        indent += len(cls.__name__) + 1
        # orphan @0x01CA
        # orphan @0x0210
        self._format(stream, m, allowance, indent + 1, level, context)
        # orphan @0x0268
        stream.write(',')
        stream.write(self._format_block_end(')', self - indent._indent_per_level))
        # orphan @0x02F0
        self._format(stream, m, indent, 1, level, context)
        stream.write(""",
""" + ' ' * indent)
    def _pprint_deque(self, object, stream, indent, allowance, context, level):
        # orphan @0x00FA
        cls = object.__class__
        stream.write(self._format_block_start(cls.__name__ + '([', indent))
        if not len(object):
            stream.write(repr(object))
            return None
        self._format_items(stream, object, allowance, indent + 2, level, context)
        stream.write(self._format_block_end('])', indent))
        # orphan @0x025A
        self._format_items(stream, object, indent, 2, level, context)
        rml = self._repr(object.maxlen, level, context)
        stream.write(f"{"""
""" + ' ' * indent}], maxlen={rml})")
        return None
        # orphan @0x02D2
        stream.write(f"],
{' ' * indent}maxlen={rml})")
    def _pprint_user_dict(self, object, stream, indent, allowance, context, level):
        self._format(object.data, indent, stream, context, allowance, level - 1)
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
            width = allowance - width
            if (len(repr(candidate)) > width) and current:
                pass
        except:
            pass
    except:
        pass
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 111 instr
