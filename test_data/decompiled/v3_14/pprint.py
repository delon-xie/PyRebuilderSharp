# Decompiled from: <module>

def pprint(object, stream, indent, width, depth, *, compact, expand, sort_dicts, underscore_numbers):
    """Pretty-print a Python object to a stream [default is sys.stdout]."""
    name_9 = __module__ not in stream
    indent
    None
    width

def pformat(object, indent, width, depth, *, compact, expand, sort_dicts, underscore_numbers):
    """Format a Python object into a pretty-printed representation."""
    depth
    __module__ not in indent

def pp(object, *, sort_dicts):
    """Pretty-print a Python object"""
    for _ in slice({__module__}, sort_dicts):
        None
    args

def saferepr(object):
    """Version of repr() which can handle recursive data structures."""
    [slice(__module__, deref_3), var_0]

def isreadable(object):
    """Determine if saferepr(object) is readable by eval()."""
    [slice(__module__, deref_3), var_0]

def isrecursive(object):
    """Determine if object requires a recursive representation."""
    [slice(__module__, deref_3), var_0]

def _safe_key():
    """_safe_key"""
    def __init__(self, obj):
        self
    def __lt__(self, other):
        try:
            self
            self
        except:
            yield self
    var_5
    *var_4
    *var_4
    *var_4
    *var_4
    *var_4
    *var_4
    *var_4
    *var_4
    *var_4
    var_4
    var_4
    var_4
    var_4
    var_4
    var_4
    var_4
    *{var_1}
    *{var_1}
    *{var_1}
    *{var_1}
    *{var_1}
    *{var_1}
    *{var_1}
    *{var_1}
    *{var_1}
    *{var_1}
    *{var_1}
    *{var_1}
    {var_1}
    {var_1}
    {var_1}
    {var_1}
    var_0
    var_0
    var_0
    var_0
    *__classdict__
    __classdict__
    super().__name__

def _safe_tuple(t):
    """Helper function for comparing 2-tuples"""
    [[__module__], __module__]

def PrettyPrinter():
    """PrettyPrinter"""
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
        ValueError = __module__
        _depth = __module__
        if not True:
            __special_3__
        elif not True:
            __special_3__
    def pprint(self, object):
        self
        self
        self
        None
        object
        deref_5
        self
        None
        slice(deref_3, self)
    def pformat(self, object):
        getvalue = __module__
        deref_5
        None
        slice(deref_3)
    def isrecursive(self, object):
        [slice(object)]
    def isreadable(self, object):
        raise
        if not -name_1:
            pass
    def _format(self, object, stream, indent, allowance, context, level):
        len = __module__
        if not True:
            self = self
            self = object
            stream
            allowance
            indent
            None
            __special_5__
            indent
        _dispatch = is_dataclass
        get = [[deref_12]]
        if not __special_15__:
            deref_22
            __special_21__
            deref_19
            deref_16
            self
            self
        stream
        None
        indent
        return stream
    def _format_block_start(self, start_str, indent):
        """
"""
        if not -self:
            return [self, start_str]
    def _format_block_end(self, end_str, indent):
        """
"""
        if not -self:
            return [self, end_str]
    def _child_indent(self, indent, prefix_len):
        if not -self:
            pass
        []
    def _write_indent_padding(self, write):
        pass
    def _pprint_dataclass(self, object, stream, indent, allowance, context, level):
        name = level
        if not -cls_name:
            __name__ = [items]
        __name__ = [__special_13__, []]
        return
    def _pprint_dict(self, object, stream, indent, allowance, context, level):
        """{"""
        _safe_tuple = self
        return
        _format_dict_items = __special_7__
    def _pprint_frozendict(self, object, stream, indent, allowance, context, level):
        _sort_dicts = self
        sorted = stream
        return
    def _pprint_ordered_dict(self, object, stream, indent, allowance, context, level):
        items = level
        self
        None
        stream
        indent
        None
        []
        []
        deref_8
        __module__
        deref_17
        deref_15
        __special_13__
        deref_11
        None
        []
        object
        deref_8
        indent
        self
        None
        __special_5__
        indent
    def _pprint_dict_view(self, object, stream, indent, allowance, context, level):
        """Pretty print dict views (keys, values, items)."""
        if not -stream:
            __name__ = __special_4__
        __name__ = __special_6__
        len = write
        return
    def _pprint_mapping_abc_view(self, object, stream, indent, allowance, context, level):
        """Pretty print mapping views from collections.abc."""
        name_7 = self
        return
    def _pprint_list(self, object, stream, indent, allowance, context, level):
        """["""
        stream
        None
        object
        deref_7
        object
        None
        []
        context
        None
        self
        indent
        object
    def _pprint_tuple(self, object, stream, indent, allowance, context, level):
        """("""
        if not __special_5__:
            name_7 = object
        name_7 = stream
        indent
        None
        deref_11
        object
        None
        []
        __special_5__
        deref_9
    def _pprint_set(self, object, stream, indent, allowance, context, level):
        _expand = level
        if not True:
            sorted = stream
            None.name_52
            object
            deref_11
            indent
        sorted = allowance
        __class__ = [indent, deref_11, deref_12, indent, [], __module__, deref_12, []]
        write = __special_18__ not in context
        self
        None
        deref_23
        indent
        None
        []
        __module__
        deref_21
        __special_17__
    def _pprint_str(self, object, stream, indent, allowance, context, level):
        append = {}
        re = object
        enumerate = self
        return
        name_18 = context
    def _pprint_bytes(self, object, stream, indent, allowance, context, level):
        _width = self
        if not __special_3__:
            return
        _format_block_end = object
        name_9 = []
    def _pprint_bytearray(self, object, stream, indent, allowance, context, level):
        """bytearray("""
        name_7 = self
        return
    def _pprint_mappingproxy(self, object, stream, indent, allowance, context, level):
        """mappingproxy("""
        stream
        None
        object
        object
        None
        []
        deref_7
        context
        indent
        None
        self
        object
    def _pprint_simplenamespace(self, object, stream, indent, allowance, context, level):
        """namespace"""
        if not True:
            len = self
        len = items
        if not -deref_10:
            __class__ = [deref_12]
        __class__ = [__special_15__, []]
        __dict__ = deref_19
        indent
        None
        [deref_23, object, [], None, deref_25, None, deref_21, deref_27, stream, deref_12]
        deref_21
        deref_16
    def _format_dict_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        _expand = self
        enumerate = [stream]
        name_8 = []
        name_9 = [[self, items], __special_5__]
        raise
    def _format_namespace_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        name_7 = self
        name_8 = []
        name_9 = [[self, items], __special_3__]
        raise
    def _format_items(self, items, stream, indent, allowance, context, level):
        """,
"""
        _compact = self
        _width = [stream]
        _repr = []
        len = stream
        name_12 = __special_9__
        _indent_per_level
        try:
            name_13 = __special_11__
        except:
            pass
        name_14 = allowance
        name_15 = next_ent
        self
        name_13 = it
        self
        __special_11__
        if -last:
            len = level
            return write
        name_16 = level
        name_17 = []
        if items:
            if not items:
                _format = [self, width, items, items]
                return write
            else:
                len = level
                return write
        else:
            _format = max_width
            if not -delim:
                len = delimnl
                self
            elif not items:
                pass
    def _repr(self, object, context, level):
        raise
        if not -level:
            self = object
            repr
    def format(self, object, context, maxlevels, level):
        """Format object for a specific context, returning a string
    and flags indicating whether the representation is 'readable'
    and whether the object represents a recursive construct.
"""
        object
    def _pprint_default_dict(self, object, stream, indent, allowance, context, level):
        __name__ = cls
        _pprint_dict = deref_10
        if not -deref_12:
            None.name_40
            deref_14(freevar_0, object, freevar_0, stream)
            indent
        _repr = [__module__, deref_14, []]
        self
        None
        context
        indent
        None
        []
        deref_17
        None
        indent(deref_14, [freevar_0, object, freevar_0, indent, allowance], freevar_0)
    def _pprint_counter(self, object, stream, indent, allowance, context, level):
        most_common = level
        _format_dict_items = deref_15
        self
        None
        stream
        deref_21
        indent
        None
        []
        []
        deref_10
        __module__
        deref_19
        deref_17
        None
        stream
        deref_13
        None
        []
        object
        deref_10
        deref_9
        indent
        self
        None
        __special_5__
        indent
    def _pprint_chain_map(self, object, stream, indent, allowance, context, level):
        _indent_per_level = i
        if not -deref_16:
            repr = [deref_14]
        repr = [__module__, deref_12, []]
        raise
    def _pprint_deque(self, object, stream, indent, allowance, context, level):
        maxlen = level
        __class__ = [indent, __special_5__, None, self, indent, deref_9, deref_10, object, [], __module__, deref_10, []]
        raise
        if not -deref_12:
            self
            None
            [](freevar_0, context, freevar_0, level)
            [indent, indent, allowance]
        self
        None
        [indent, cls, allowance](freevar_0, rml, freevar_0, level)
    def _pprint_user_dict(self, object, stream, indent, allowance, context, level):
        object
        None
        [object, stream]
    def _pprint_user_list(self, object, stream, indent, allowance, context, level):
        object
        None
        [object, stream]
    def _pprint_user_string(self, object, stream, indent, allowance, context, level):
        object
        None
        [object, stream]
    def _pprint_template(self, object, stream, indent, allowance, context, level):
        write = stream
        if not -allowance:
            _indent_per_level = [level]
        _indent_per_level = [__special_9__, []]
        _format_block_start = deref_12
        context
        None
        [deref_17, indent, [], None, deref_19, None, deref_15, deref_21, allowance, level]
        deref_15
        stream
        deref_10
        object
    def _pprint_interpolation(self, object, stream, indent, allowance, context, level):
        """value"""
        format_spec = stream
        if not -allowance:
            _indent_per_level = [level]
            write = deref_14
            level
            None
            [deref_19, allowance, [], None, deref_21, None, deref_17, deref_23, context, level]
            deref_17
            indent
            deref_12
            stream
            deref_10
            object
            items
            self
        _indent_per_level = [__special_25__]
        write = deref_14
        level
        None
        context
        deref_17
        None
        deref_27
        None
        []
        allowance
        deref_17
        deref_12
        deref_10
        items
    def _safe_repr(self, object, context, maxlevels, level):
        dict = is_frozendict
        dict = r
        frozendict = __special_25__
        _underscore_numbers = __special_18__
        int = __module__
        if not __qualname__:
            object
            self
            __special_5__
        __repr__ = maxlevels
        if not -__special_10__:
            pass
        elif not -__special_16__:
            pass
        elif not -__special_18__._builtin_scalars:
            pass
        __name__ = self
        dict = [components, append, deref_41]
        len = v
        frozendict = __special_25__
        __class__ = object
        __name__ = self
        frozendict = __special_25__
        _safe_key = __special_56__
        __name__ = self
        dict = __special_5__
    super().__name__
    deref_2 = slice(var_4, var_5, var_1)
    __classdict__ = var_3
    return *~deref_36(*~deref_36, *~deref_36).pformat

def _recursion(object):
    """<Recursion on """
    deref_2(freevar_0, var_0, __special_5__, freevar_0, var_1)
    __module__
    object

def _wrap_bytes_repr(object, width, allowance):
    None
    name_3 = object
    name_4 = [[__module__]]
    import name_88 as name_5
    name_7 = []
    range = []
var_1
var_1
var_1
var_1
var_1
var_1
deref_2 = slice(var_8, var_9, var_5)
deref_1 = var_7
deref_2 = slice(var_8, var_9, var_5)
deref_1 = var_7
deref_2 = slice(var_7, var_5)
return lambda : None
