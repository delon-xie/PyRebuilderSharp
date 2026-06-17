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
    printer.pprint(object)
def pformat(object, indent, width, depth):
    'Format a Python object into a pretty-printed representation.'
    return
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
        pass
    def __lt__(self, other):
        try:
            try:
                if str:
                    pass
                return
            except:
                pass
        except:
            pass
        return
    __static_attributes__ = ['obj']
    __classdictcell__ = __classdict__
def _safe_tuple(t):
    'Helper function for comparing 2-tuples'
    return (_safe_key(t[0]), _safe_key(t[1]))
class PrettyPrinter:
    try:
        for _ in # Unknown node: SetLiteral:
            try:
                try:
                    def _pprint_list(self, object, stream, indent, allowance, context, level):
                        '['
                        stream.write(self._format_block_start('[', indent))
                        stream.write(self._format_block_end(']', indent))
                    def _pprint_tuple(self, object, stream, indent, allowance, context, level):
                        '('
                        stream.write(self._format_block_start('(', indent))
                        if (len(object) == 1) and not self._expand:
                            endchar = ',)'
                        endchar = ')'
                    def _pprint_set(self, object, stream, indent, allowance, context, level):
                        # orphan @0x0086
                        typ = object.__class__
                        stream.write(self._format_block_start('{', indent))
                        endchar = '}'
                        if not len(object):
                            stream.write(repr(object))
                        return
                        # orphan @0x00CE
                        stream.write(self._format_block_start(typ.__name__ + '({', indent))
                        endchar = '})'
                        # orphan @0x015A
                        # orphan @0x01A0
                        # orphan @0x01A2
                        object = object(name_18, ('key',))
                    def _pprint_str(self, object, stream, indent, allowance, context, level):
                        # orphan @0x01A0
                        # orphan @0x0190
                        # orphan @0x0148
                        rep = repr(line)
                        # orphan @0x0140
                        # orphan @0x0102
                        # orphan @0x00F2
                        # orphan @0x00DE
                        indent += 1
                        # orphan @0x00B8
                        # orphan @0x0094
                        chunks = []
                        lines = object.splitlines(True)
                        write = stream.write
                        if not len(object):
                            write(repr(object))
                        return
                        # orphan @0x01C0
                        chunks.append(rep)
                        # orphan @0x01E6
                        import re
                        parts = re.findall('\\S*\\s*', line)
                        # orphan @0x0222
                        # orphan @0x0226
                        raise
                        # orphan @0x0228
                        # orphan @0x0244
                        # orphan @0x0248
                        raise
                        # orphan @0x024A
                        parts.pop()
                        max_width2 = max_width
                        current = ''
                        # orphan @0x0286
                        # orphan @0x028C
                        candidate = current + part
                        # orphan @0x02D2
                        # orphan @0x0300
                        # orphan @0x0312
                        # orphan @0x0344
                        # orphan @0x0354
                        # orphan @0x0388
                        current = part
                        # orphan @0x0390
                        current = candidate
                        # orphan @0x039A
                        # orphan @0x03AC
                        # orphan @0x03B2
                        chunks.append(repr(current))
                        # orphan @0x03EE
                        # orphan @0x0410
                        write(rep)
                        # orphan @0x0424
                        return
                        # orphan @0x0432
                        # orphan @0x0462
                        # orphan @0x0478
                        # orphan @0x047E
                        # orphan @0x0490
                        # orphan @0x04BC
                        write(rep)
                        # orphan @0x04D2
                        # orphan @0x04E2
                        # orphan @0x0536
                        return
                    def _pprint_bytes(self, object, stream, indent, allowance, context, level):
                        # orphan @0x009C
                        # orphan @0x0078
                        parens = level == 1
                        write = stream.write
                        if len(object) <= 4:
                            write(repr(object))
                        return
                        # orphan @0x00C2
                        indent += 1
                        # orphan @0x00D6
                        allowance += 1
                        # orphan @0x0116
                        delim = ''
                        # orphan @0x0154
                        # orphan @0x015A
                        write(delim)
                        write(rep)
                        # orphan @0x018A
                        # orphan @0x018E
                        delim = """
""" + ' ' * indent
                        # orphan @0x01B4
                        # orphan @0x01C6
                        # orphan @0x021A
                        return
                    def _pprint_bytearray(self, object, stream, indent, allowance, context, level):
                        'bytearray('
                        write = stream.write
                        write(self._format_block_start('bytearray(', indent))
                        if self._expand:
                            write(' ' * self._indent_per_level)
                        recursive_indent = indent + 10
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
                        if self._expand:
                            pass
                        indent += len(cls_name) + 1
                        items = object.__dict__.items()
                        stream.write(self._format_block_start(cls_name + '(', indent))
                    def _format_dict_items(self, items, stream, indent, allowance, context, level):
                        """,
"""
                        write = stream.write
                        delimnl = """,
""" + ' ' * indent
                        last_index = len(items) - 1
                        for i in enumerate(items):
                            write(rep)
                            write(': ')
                            if last:
                                pass
                            break
                            if not last:
                                write(delimnl)
                            write(',')
                    def _format_namespace_items(self, items, stream, indent, allowance, context, level):
                        """,
"""
                        write = stream.write
                        delimnl = """,
""" + ' ' * indent
                        last_index = len(items) - 1
                        for i in enumerate(items):
                            write(key)
                            write('=')
                            if id(ent) in context:
                                write('...')
                            elif last:
                                pass
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
                        self._write_indent_padding(write)
                        delimnl = """,
""" + ' ' * indent
                        delim = ''
                        while last:
                            return None
                        ent = next_ent
                        if self._compact:
                            w = len(rep) + 2
                            if width < w:
                                width = max_width
                                if delim:
                                    pass
                                elif width >= w:
                                    width -= w
                                    write(delim)
                                    delim = ', '
                                    write(rep)
                        raise
                        try:
                            pass
                        except:
                            pass
                        raise
                        # orphan @0x02B0
                        return
                        # orphan @0x02F6
                        # orphan @0x02FA
                        raise
                        # [WARN] 4 instructions not decompiled
                        #   @0x01EE: JUMP_BACKWARD arg=262
                        #   @0x0252: JUMP_BACKWARD arg=362
                        #   @0x027A: JUMP_BACKWARD arg=402
                        #   @0x028E: JUMP_BACKWARD arg=422
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
                        return
                    def _pprint_default_dict(self, object, stream, indent, allowance, context, level):
                        if not len(object):
                            stream.write(repr(object))
                        return
                        # orphan @0x00CE
                        cls = object.__class__
                        stream.write(f"{cls.__name__}({rdf}, ")
                        # orphan @0x0116
                        indent += len(cls.__name__) + 1
                        stream.write(f"{cls.__name__}({rdf},
{' ' * indent}")
                        # orphan @0x01B8
                        stream.write(')')
                    def _pprint_counter(self, object, stream, indent, allowance, context, level):
                        # orphan @0x005C
                        cls = object.__class__
                        stream.write(self._format_block_start(cls.__name__ + '({', indent))
                        self._write_indent_padding(stream.write)
                        items = object.most_common()
                        self._format_dict_items(items, stream, self._child_indent(indent, len(cls.__name__) + 1), allowance + 2, context, level)
                        stream.write(self._format_block_end('})', indent))
                        return None
                        if not len(object):
                            stream.write(repr(object))
                        return
                    def _pprint_chain_map(self, object, stream, indent, allowance, context, level):
                        if not len(object.maps):
                            stream.write(repr(object))
                        return
                        # orphan @0x012E
                        cls = object.__class__
                        indent = self._expand + var_48._indent_per_level
                        # orphan @0x0154
                        indent += len(cls.__name__) + 1
                        # orphan @0x019C
                        # orphan @0x01C4
                        # orphan @0x01CA
                        # orphan @0x0210
                        # orphan @0x0268
                        # orphan @0x028A
                        # orphan @0x02F0
                        stream.write(""",
""" + ' ' * indent)
                    def _pprint_deque(self, object, stream, indent, allowance, context, level):
                        # orphan @0x00FA
                        cls = object.__class__
                        stream.write(self._format_block_start(cls.__name__ + '([', indent))
                        if not len(object):
                            stream.write(repr(object))
                        return
                        # orphan @0x0140
                        stream.write(self._format_block_end('])', indent))
                        return None
                        # orphan @0x025A
                        stream.write(f"{"""
""" + ' ' * indent}], maxlen={rml})")
                        # orphan @0x02AC
                        return
                        # orphan @0x02AE
                        stream.write(f"],
{' ' * indent}maxlen={rml})")
                    def _pprint_user_dict(self, object, stream, indent, allowance, context, level):
                        pass
                    def _pprint_user_list(self, object, stream, indent, allowance, context, level):
                        pass
                    def _pprint_user_string(self, object, stream, indent, allowance, context, level):
                        pass
                    def _pprint_template(self, object, stream, indent, allowance, context, level):
                        cls_name = object.__class__.__name__
                        if self._expand:
                            pass
                        indent += len(cls_name) + 1
                        items = (('strings', object.strings), ('interpolations', object.interpolations))
                        stream.write(self._format_block_start(cls_name + '(', indent))
                    def _pprint_interpolation(self, object, stream, indent, allowance, context, level):
                        'value'
                        cls_name = object.__class__.__name__
                        if self._expand:
                            items = (('value', object.value), ('expression', object.expression), ('conversion', object.conversion), ('format_spec', object.format_spec))
                            stream.write(self._format_block_start(cls_name + '(', indent))
                        return
                        # orphan @0x01BE
                        indent += len(cls_name)
                        items = (object.value, object.expression, object.conversion, object.format_spec)
                        stream.write(cls_name + '(')
                        stream.write(')')
                    t = ('<f-string>')
                    def _safe_repr(self, object, context, maxlevels, level):
                        # orphan @0x03B2
                        append(f"{krepr}: {vrepr}")
                        # orphan @0x03AC
                        # orphan @0x03AA
                        # orphan @0x0388
                        items = object.items()
                        # orphan @0x0348
                        readable = True
                        recursive = False
                        components = []
                        append = components.append
                        level += 1
                        items = object.items()(name_36, ('key',))
                        # orphan @0x02E6
                        return
                        # orphan @0x02CA
                        # orphan @0x02BE
                        return
                        # orphan @0x02B0
                        # orphan @0x0278
                        # orphan @0x0264
                        rep = '{...}'
                        # orphan @0x0258
                        objid = id(object)
                        # orphan @0x0232
                        return
                        # orphan @0x022A
                        # orphan @0x0224
                        rep = '{}'
                        # orphan @0x01F0
                        rep = f"{object.__class__.__name__}()"
                        # orphan @0x01E0
                        # orphan @0x01B0
                        is_frozendict = issubclass(typ, _safe_tuple)
                        # orphan @0x0186
                        # orphan @0x0158
                        # orphan @0x0130
                        # orphan @0x0104
                        return (repr(object), True, False)
                        # orphan @0x00E8
                        return
                        # orphan @0x00DA
                        # orphan @0x00B6
                        # orphan @0x008E
                        r = getattr(typ, '__repr__', None)
                        typ = type(object)
                        if typ in repr:
                            pass
                        return
                        # orphan @0x0442
                        # orphan @0x0456
                        # orphan @0x045A
                        readable = vreadable
                        # orphan @0x046C
                        # orphan @0x047C
                        # orphan @0x0480
                        recursive = True
                        # orphan @0x048A
                        rep = '{%s}' % ', '.join(components)
                        # orphan @0x04D0
                        # orphan @0x0508
                        # orphan @0x0510
                        return
                        # orphan @0x053C
                        # orphan @0x0564
                        # orphan @0x0592
                        # orphan @0x05BA
                        # orphan @0x05E6
                        # orphan @0x05F6
                        # orphan @0x05FA
                        return
                        # orphan @0x0600
                        format = '[%s]'
                        # orphan @0x0620
                        format = '(%s,)'
                        # orphan @0x0626
                        # orphan @0x0636
                        # orphan @0x063A
                        return
                        # orphan @0x0640
                        format = '(%s)'
                        objid = id(object)
                        # orphan @0x0664
                        # orphan @0x0670
                        # orphan @0x068C
                        return
                        # orphan @0x0698
                        # orphan @0x06B4
                        return
                        # orphan @0x06F6
                        readable = True
                        recursive = False
                        components = []
                        append = components.append
                        level += 1
                        # orphan @0x06FC
                        append(orepr)
                        # orphan @0x074A
                        # orphan @0x074E
                        # orphan @0x075E
                        # orphan @0x0762
                        recursive = True
                        # orphan @0x076C
                        # orphan @0x07A6
                        return
                        # orphan @0x07FC
                        # orphan @0x081E
                        objid = id(object)
                        # orphan @0x0844
                        # orphan @0x0850
                        # orphan @0x085E
                        return
                        # orphan @0x086A
                        # orphan @0x0886
                        return
                        # orphan @0x08FC
                        key = name_56
                        # orphan @0x0908
                        # orphan @0x092C
                        # orphan @0x09A4
                        return
                        # orphan @0x09C8
                        # orphan @0x09E4
                        return
                        # orphan @0x0A08
                        # orphan @0x0A22
                        readable = True
                        recursive = False
                        components = []
                        append = components.append
                        level += 1
                        # orphan @0x0A64
                        # orphan @0x0A6A
                        append(vrepr)
                        # orphan @0x0ABA
                        # orphan @0x0ABE
                        readable = vreadable
                        # orphan @0x0AD0
                        # orphan @0x0AD4
                        recursive = True
                        # orphan @0x0ADE
                        # orphan @0x0B3A
                        return
                        # orphan @0x0B62
                        rep = repr(object)
                        # orphan @0x0B8E
                        return (False)
                    __static_attributes__ = ('_compact', '_depth', '_expand', '_indent_per_level', '_readable', '_recursive', '_sort_dicts', '_stream', '_underscore_numbers', '_width')
                    __classdictcell__ = __classdict__
                    return None
                    break
                except:
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
        indent = int(indent)
        width = int(width)
        if indent < 0:
            pass
        raise
        if depth <= 0:
            pass
        raise
        if not width:
            pass
        raise
        if compact and expand:
            pass
        raise
        self._stream = _underscore_numbers.stdout
        self._compact = bool(compact)
        self._expand = bool(expand)
    def pprint(self, object):
        self._stream.write("""
""")
    def pformat(self, object):
        sio = _StringIO()
        return sio.getvalue()
    def isrecursive(self, object):
        return self.format(object, {}, 0, 0)[2]
    def isreadable(self, object):
        if readable:
            pass
        return
    def _format(self, object, stream, indent, allowance, context, level):
        # orphan @0x00EE
        max_width = self._width - indent - allowance
        p = self._dispatch.get(type(object).__repr__, None)
        from dataclasses import is_dataclass
        return None
        objid = id(object)
        if True:
            stream.write(_recursion(object))
            self._recursive = True
            self._readable = False
        return
        # orphan @0x01B0
        # orphan @0x01DC
        # orphan @0x0214
        # orphan @0x024C
        # orphan @0x0296
        # orphan @0x02DA
        return
        # orphan @0x02DC
        stream.write(rep)
    def _format_block_start(self, start_str, indent):
        """
"""
        if self._expand:
            pass
        return
        # orphan @0x0042
        return start_str
    def _format_block_end(self, end_str, indent):
        """
"""
        if self._expand:
            pass
        return
        # orphan @0x0042
        return end_str
    def _child_indent(self, indent, prefix_len):
        if self._expand:
            pass
        return
        # orphan @0x002A
        return
    def _write_indent_padding(self, write):
        if self._expand and (self._indent_per_level > 0):
            write(self._indent_per_level * ' ')
        return
        # orphan @0x00A2
        write((self._indent_per_level - 1) * ' ')
        # orphan @0x00E6
        return
    def _pprint_dataclass(self, object, stream, indent, allowance, context, level):
        try:
            for _ in (f.name(getattr, var_25.name)):
                try:
                    break
                except:
                    break
                if not True:
                    pass
            stream.write(self._format_block_start(cls_name + '(', indent))
            break
        except:
            break
        from dataclasses import fields as dataclass_fields
        cls_name = object.__class__.__name__
        if self._expand:
            pass
        indent += len(cls_name) + 1
        # [WARN] 1 instructions not decompiled
        #   @0x00F6: JUMP_BACKWARD arg=44
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
        write(self._format_block_end('}', indent))
    def _pprint_frozendict(self, object, stream, indent, allowance, context, level):
        write = stream.write
        cls = object.__class__
        if not len(object):
            write(repr(object))
        return
        # orphan @0x0110
        write(self._format_block_start(cls.__name__ + '({', indent))
        self._write_indent_padding(write)
        items = object.items()(name_20, ('key',))
        # orphan @0x0150
        items = object.items()
        # orphan @0x0172
        self._format_dict_items(items, stream, self._child_indent(indent, len(cls.__name__) + 1), allowance + 2, context, level)
        write(self._format_block_end('})', indent))
    def _pprint_ordered_dict(self, object, stream, indent, allowance, context, level):
        # orphan @0x005C
        cls = object.__class__
        stream.write(cls.__name__ + '(')
        self._format(list(object.items()), stream, self._child_indent(indent, len(cls.__name__) + 1), allowance + 1, context, level)
        stream.write(')')
        return None
        if not len(object):
            stream.write(repr(object))
        return
    def _pprint_dict_view(self, object, stream, indent, allowance, context, level):
        'Pretty print dict views (keys, values, items).'
        if True:
            key = write
        key = __class__
        write = stream.write
        write(self._format_block_start(object.__class__.__name__ + '([', indent))
        if len(object) and self._sort_dicts:
            entries = sorted(var_23, ('key',))
        entries = object
        write(self._format_block_end('])', indent))
    def _pprint_mapping_abc_view(self, object, stream, indent, allowance, context, level):
        'Pretty print mapping views from collections.abc.'
        write = stream.write
        write(object.__class__.__name__ + '(')
        write(')')
    _dict_keys_view = type({}.keys())
    _dict_values_view = type({}.values())
    _dict_items_view = type({}.items())
_builtin_scalars = frozenset(# Unknown node: SetLiteral)
def _recursion(object):
    '<Recursion on '
    return f"<Recursion on {type(object).__name__} with id={id(object)}>"
def _wrap_bytes_repr(object, width, allowance):
    try:
        current = b''
        last = len(object) // 4 * 4
        for i in range(0, len(object), 4):
            try:
                try:
                    current = b''
                    last = len(object) // 4 * 4
                    try:
                        try:
                            try:
                                pass
                            except:
                                return None
                        except:
                            return None
                    except:
                        return None
                except:
                    return None
            except:
                return None
            current = candidate
            break
        if current:
            pass
        return
    except:
        pass
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 111 instr
