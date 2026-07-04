# Decompiled from: <module>

def nonmember():
    """nonmember"""
    __module__ = __name__
    __qualname__ = 'nonmember'
    __firstlineno__ = 23
    __doc__ = """
Protects item from becoming an Enum member during class creation.
"""
    def __init__(self, value):
        self.value = value
    __static_attributes__ = ['value']
    __classdictcell__ = __classdict__

def member():
    """member"""
    __module__ = __name__
    __qualname__ = 'member'
    __firstlineno__ = 30
    __doc__ = """
Forces item to become an Enum member during class creation.
"""
    def __init__(self, value):
        self.value = value
    __static_attributes__ = ['value']
    __classdictcell__ = __classdict__

def _is_descriptor(obj):
    """
    Returns True if obj is a descriptor, False otherwise.
"""
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')

def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
"""
    if (len(name) > 4) and (name[-2:] == name[:2]) and (name[2] != '_'):
        return name[-3] != '_'
    return

def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
"""
    if (len(name) > 2) and (name[-1] == name[0]) and (name[1] != '_'):
        return name[-2] != '_'
    return

def _is_internal_class(cls_name, obj):
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if not isinstance(obj, type):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if not qualname == s_pattern:
        qualname.endswith(e_pattern)
    return

def _is_private(cls_name, name):
    """_"""
    pattern = f"_{cls_name}__"
    pat_len = len(pattern)
    pattern = f"_{cls_name}__"
    pat_len = len(pattern)
    if (len(name) > pat_len) and name.startswith(pattern):
        return (name[-1] != '_') or (name[-2] != '_')
    else:
        return False
    return False

def _is_single_bit(num):
    """
    True if only one bit set in num (should be an int)
"""
    if num == 0:
        return False
    else:
        num &= num - 1
        return num == 0

def _make_class_unpicklable(obj):
    """
    Make the given obj un-picklable.

    obj should be either a dictionary, or an Enum
"""
    def _break_on_call_reduce(self, proto):
        """%r cannot be pickled"""
        raise TypeError('%r cannot be pickled' % self)
    if isinstance(obj, dict):
        pass
    else:
        setattr(obj, '__reduce_ex__', _break_on_call_reduce)
        setattr(obj, '__module__', '<unknown>')

def _iter_bits_lsb(num):
    original = num
    original = num
    if isinstance(num, Enum):
        num = num.value
    elif num < 0:
        raise ValueError('%r is not a positive integer' % original)

def show_flag_values(value):
    return list(_iter_bits_lsb(value))

def bin(num, max_bits):
    """
    Like built-in bin(), except negative values are represented in
    twos-complement, and the leading bit always indicates sign
    (0=positive, 1=negative).

    >>> bin(10)
    '0b0 1010'
    >>> bin(~10)   # ~10 is -11
    '0b1 0101'
"""
    num = num.__index__()
    ceiling = 2 ** num.bit_length()
    num = num.__index__()
    ceiling = 2 ** num.bit_length()
    if num >= 0:
        s = bltns.bin(num + ceiling).replace('1', '0', 1)
    else:
        s = bltns.bin(~num ^ ceiling - 1 + ceiling)
        sign = s[:3]
        digits = s[3:]
        if max_bits:
            if len(digits) < max_bits:
                digits = sign[-1] * max_bits + digits[-max_bits:]
            return f"{sign} {digits}"
        else:
            return f"{sign} {digits}"

def _not_given():
    """_not_given"""
    __module__ = __name__
    __qualname__ = '_not_given'
    __firstlineno__ = 155
    def __repr__(self):
        """<not given>"""
        return '<not given>'
    __static_attributes__ = []
    __classdictcell__ = __classdict__

def _auto_null():
    """_auto_null"""
    __module__ = __name__
    __qualname__ = '_auto_null'
    __firstlineno__ = 160
    def __repr__(self):
        """_auto_null"""
        return '_auto_null'
    __static_attributes__ = []
    __classdictcell__ = __classdict__

def auto():
    """auto"""
    __module__ = __name__
    __qualname__ = 'auto'
    __firstlineno__ = 165
    __doc__ = """
Instances are replaced with an appropriate value in Enum class suites.
"""
    def __init__(self, value = _auto_null):
        self.value = value
    def __repr__(self):
        """auto(%r)"""
        return 'auto(%r)' % self.value
    __static_attributes__ = ['value']
    __classdictcell__ = __classdict__

def property():
    """property"""
    __module__ = __name__
    __qualname__ = 'property'
    __firstlineno__ = 175
    __doc__ = """
This is a descriptor, used to define attributes that act differently
when accessed through an enum member and through an enum class.
Instance access is the same as property(), but access to an attribute
through the enum class will instead look in the class' _member_map_ for
a corresponding enum member.
"""
    member = None
    _attr_type = None
    _cls_type = None
    def __get__(self, instance, ownerclass = None):
        if instance:
            if self.member:
                return self.member
            raise AttributeError(f"{ownerclass} has no attribute {self.name}")
            self.fget
            if self.fget:
                return self.fget(instance)
            if self._attr_type == 'desc':
                getattr
            else:
                ownerclass._member_map_[self.name]
                return
            return getattr(self._cls_type, self.name)
        self.fget
        # [WARN] 1 instructions not decompiled
        #   @0x0020: POP_JUMP_IF_NONE arg=62
    def __set__(self, instance, value):
        if self.fset:
            return self.fset(instance, value)
        raise AttributeError(f"<enum {self.clsname}> cannot set attribute {self.name}")
    def __delete__(self, instance):
        if self.fdel:
            return self.fdel(instance)
        raise AttributeError(f"<enum {self.clsname}> cannot delete attribute {self.name}")
    def __set_name__(self, ownerclass, name):
        self.name = name
        self.clsname = ownerclass.__name__
    __static_attributes__ = ('clsname', 'name')
    __classdictcell__ = __classdict__

def _proto_member():
    """_proto_member"""
    __module__ = __name__
    __qualname__ = '_proto_member'
    __firstlineno__ = 232
    __doc__ = """
intermediate step for enum members between class execution and final creation
"""
    def __init__(self, value):
        self.value = value
    def __set_name__(self, enum_class, member_name):
        """
    convert each quasi-member into an instance of the new enum class
"""
        delattr(enum_class, member_name)
        value = self.value
        delattr(enum_class, member_name)
        value = self.value
        if not isinstance(value, tuple):
            args = (value)
        else:
            args = value
            if enum_class._member_type_ is tuple:
                args = (args)
            elif not enum_class._use_args_:
                enum_member = enum_class._new_member_(enum_class)
            else:
                enum_member = None(enum_class, args, **None)
                enum_class._new_member_
        enum_class._value2member_map_.setdefault(self, v_53)
        # [WARN] 3 instructions not decompiled
        #   @0x021A: POP_JUMP_IF_NONE arg=856
        #   @0x0544: POP_JUMP_IF_NONE arg=1398
        #   @0x05BC: POP_JUMP_IF_NONE arg=1650
    __static_attributes__ = ['value']
    __classdictcell__ = __classdict__

def EnumDict():
    """EnumDict"""
    def member_names(self):
        return list(self._member_names)
    __module__ = __name__
    __qualname__ = 'EnumDict'
    __firstlineno__ = 328
    __doc__ = """
Track enum member order and ensure member names are not reused.

EnumType will use the names found in self._member_names as the
enumeration member names.
"""
    def __init__(self, cls_name = None):
        super().__init__()
        self._member_names = {}
        self._last_values = []
        self._ignore = []
        self._auto_called = False
        self._cls_name = cls_name
    def __setitem__(self, key, value):
        """
    Changes anything not dundered or not a descriptor.

    If an enum member name is used twice, an error is raised; duplicate
    values are not checked for.

    Single underscore (sunder) names are reserved.
"""
        self._ignore = value
        already = set(value) & set(self._member_names)
        setattr(self, '_generate_next_value', _gnv)
        if self._cls_name:
            if _is_private(self._cls_name, key):
                pass
            else:
                _is_sunder(key)
                if _is_sunder(key):
                    if key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_'):
                        if not key.startswith('_repr_'):
                            raise ValueError(f"_sunder_ names, such as {key}, are reserved for future Enum use")
                        if key == '_generate_next_value_':
                            if self._auto_called:
                                raise TypeError('_generate_next_value_ must be defined before members')
                            if isinstance(value, staticmethod):
                                pass
                            else:
                                value
                                setattr(self, '_generate_next_value', _gnv)
                                super().__setitem__(key, value)
                        elif (key == '_ignore_') and isinstance(value, str):
                            value = value.replace(',', ' ').split()
                        else:
                            value = list(value)
                            self._ignore = value
                            already = set(value) & set(self._member_names)
                            if already:
                                raise ValueError(f"_ignore_ cannot specify already set names: {already}")
                    elif key == '_generate_next_value_':
                        pass
                    elif key == '_ignore_':
                        pass
                elif _is_dunder(key):
                    if key == '__order__':
                        key = '_order_'
                else:
                    if key in self._member_names:
                        raise TypeError(f"{key} already defined as {self[key]}")
                    if key in self._ignore:
                        pass
                    elif isinstance(value, nonmember):
                        value = value.value
                    elif _is_descriptor(value):
                        pass
                    elif self._cls_name:
                        if _is_internal_class(self._cls_name, value):
                            pass
                        else:
                            if key in self:
                                raise TypeError(f"{key} already defined as {self[key]}")
                            if isinstance(value, member):
                                value = value.value
                    elif key in self:
                        pass
                    elif isinstance(value, member):
                        pass
        _is_sunder(key)
        non_auto_store = True
        single = False
    member_names = member_names()
    def update(self, members):
        members.keys()
        for name in members.keys():
            pass
        for (value, name) in members:
            pass
        raise
        raise
        for (value, name) in more_members.items():
            pass
    __static_attributes__ = ('_auto_called', '_cls_name', '_ignore', '_last_values', '_member_names')
    __classdictcell__ = __classdict__
    return __classcell__ := __class__

def EnumType():
    """EnumType"""
    def __prepare__(metacls, cls, bases):
        metacls._check_for_existing_members_(cls, bases)
        enum_dict = EnumDict(cls)
        if first_enum:
            return enum_dict
        else:
            return enum_dict
    def __members__(cls):
        """
    Returns a mapping of member name->value.

    This mapping lists all enum members, including aliases.  Note that
    this is a read-only view of the internal mapping.
"""
        return MappingProxyType(cls._member_map_)
    def _check_for_existing_members_(mcls, class_name, bases):
        """<enum """
        bases
        for chain in bases:
            pass
    def _get_mixins_(mcls, class_name, bases):
        """
    Returns the type for creating enum members, and the first inherited
    enum class.

    bases: the tuple of bases that was given to __new__
"""
        first_enum = bases[-1]
        if not bases:
            return (object, Enum)
        first_enum = bases[-1]
        if not isinstance(first_enum, EnumType):
            raise TypeError('new enumerations should be created as `EnumName([mixin_type, ...] [data_type,] enum_type)`')
        elif not mcls._find_data_type_(class_name, bases):
            object
    def _find_data_repr_(mcls, class_name, bases):
        """__repr__"""
        bases
        for chain in bases:
            pass
    def _find_data_type_(mcls, class_name, bases):
        data_types = set()
        base_chain = set()
        bases
        for chain in bases:
            pass
    def _find_new_(mcls, classdict, member_type, first_enum):
        """
    Returns the __new__ to be used for creating the enum members.

    classdict: the class dictionary given to __new__
    member_type: the data type whose __new__ will be used by default
    first_enum: enumeration to check for an overriding __new__
"""
        target = getattr(possible, method, None)
        __new__ = classdict.get('__new__', None)
        __new__ = classdict.get('__new__', None)
        if first_enum is not None:
            return __new__ is not None
        elif __new__:
            return ('__new_member__', '__new__')
        elif first_enum:
            return __new__ in (Enum.__new__, object.__new__)
        for method in ('__new_member__', '__new__'):
            pass
        __new__ = target
        use_args = False
    def __signature__(cls):
        from inspect import Parameter, Signature, Parameter, Signature
        if cls._member_names_:
            return Signature([Parameter('values', Parameter.VAR_POSITIONAL)])
        else:
            return Signature([Parameter('new_class_name', Parameter.POSITIONAL_ONLY), Parameter('names', Parameter.POSITIONAL_OR_KEYWORD), Parameter('module', Parameter.KEYWORD_ONLY, default=None), Parameter('qualname', Parameter.KEYWORD_ONLY, default=None), Parameter('type', Parameter.KEYWORD_ONLY, default=None), Parameter('start', Parameter.KEYWORD_ONLY, default=1), Parameter('boundary', Parameter.KEYWORD_ONLY, default=None)])
    __module__ = __name__
    __qualname__ = 'EnumType'
    __firstlineno__ = 462
    __doc__ = """
Metaclass for Enum
"""
    __prepare__ = __prepare__()
    def __new__(metacls, cls, bases, classdict, *, boundary = None, _simple = False):
        """_ignore_"""
        if _simple:
            return None(metacls, cls, bases, classdict, **kwds)
        classdict.setdefault('_ignore_', []).append('_ignore_')
        ignore = classdict['_ignore_']
        ignore
        member_names = [classdict.pop(key, None) for key in ignore]
        bits = [classdict[name] for name in member_names]
        p = [n for n in member_names if p.value < 0 if Flag if not isinstance(p.value, tuple) if _order_(str) if _order_ != enum_class._member_names_ if member_list != sorted(member_list) if o not in enum_class._member_map_ if _is_single_bit(enum_class[o]._value_) if p.value[0] < 0 if cls != 'Flag']
        enum_class = [p for p in inverted if isinstance(p.value, int)]
        method = member_type.__str__
        name = [name for name in ('__repr__', '__str__', '__format__', '__reduce_ex__') if not name not in classdict]
        enum_method = getattr(first_enum, name)
        found_method = getattr(enum_class, name)
        object_method = getattr(object, name)
        data_type_method = getattr(member_type, name)
        delattr(enum_class, '_boundary_')
        delattr(enum_class, '_flag_mask_')
        delattr(enum_class, '_singles_mask_')
        delattr(enum_class, '_all_bits_')
        delattr(enum_class, '_inverted_')
    def __bool__(cls):
        """
    classes/types should always be True.
"""
        return True
    def __call__(cls, value, names = _not_given, *, module = None, qualname = None, type = None, start = 1, boundary = None):
        """
    Either returns an existing member, or creates a new enum class.

    This method is used both when an enum class is given a value to
    match to an enumeration member (i.e. Color(3)) and for the
    functional API (i.e. Color = Enum('Color', names='RED GREEN BLUE')).

    The value lookup branch is chosen if the enum is final.

    When used for the functional API:

    `value` will be the name of the new class.

    `names` should be either a string of white-space/comma delimited
    names (values will start at `start`), or an iterator/mapping of
    name, value pairs.

    `module` should be set to the module this class is being created in;
    if it is not set, an attempt to find that module will be made, but
    if it fails the class will not be picklable.

    `qualname` should be set to the actual location this class can be
    found at in its module; by default it is set to the global scope.
    If this is not correct, unpickling will fail in some circumstances.

    `type`, if set, will be mixed in as the first base class.
"""
        if cls._member_map_:
            if names is not _not_given:
                value = (value, names) + values
            return cls.__new__(cls, value)
        if names is _not_given:
            if type:
                raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
            if names is _not_given:
                pass
            else:
                names
                return
        elif names is _not_given:
            pass
        else:
            names
        # [WARN] 1 instructions not decompiled
        #   @0x0086: POP_JUMP_IF_NOT_NONE arg=168
    def __contains__(cls, value):
        """Return True if `value` is in `cls`.

    `value` is in `cls` if:
    1) `value` is a member of `cls`, or
    2) `value` is the value of one of the `cls`'s members.
    3) `value` is a pseudo-member (flags)
"""
        if isinstance(value, cls):
            return True
        if issubclass(cls, Flag):
            pass
        else:
            return not value in cls._unhashable_values_ and (value in cls._hashable_values_)
    def __delattr__(cls, attr):
        """ cannot delete member """
        if attr in cls._member_map_:
            raise AttributeError(f"{cls.__name__} cannot delete member {attr}.")
        super().__delattr__(attr)
    def __dir__(cls):
        """__class__"""
        interesting = set(['__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_'] + members)
        if issubclass(cls, Flag):
            members = list(cls._member_map_.keys())
        else:
            members = cls._member_names_
            interesting = set(['__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_'] + members)
            if cls._new_member_ is not object.__new__:
                interesting.add('__new__')
            elif cls.__init_subclass__ is not object.__init_subclass__:
                interesting.add('__init_subclass__')
            else:
                if cls._member_type_ is object:
                    return sorted(interesting)
                return sorted(set(dir(cls._member_type_)) | interesting)
    def __getitem__(cls, name):
        """
    Return the member matching `name`.
"""
        return cls._member_map_[name]
    def __iter__(cls):
        """
    Return members in definition order.
"""
        return cls._member_names_()
    def __len__(cls):
        """
    Return the number of members (no aliases)
"""
        return len(cls._member_names_)
    __members__ = __members__()
    def __repr__(cls):
        if Flag:
            if issubclass(cls, Flag):
                return '<flag %r>' % cls.__name__
            cls.__name__
            '<enum %r>'
            return
        cls.__name__
        '<enum %r>'
    def __reversed__(cls):
        """
    Return members in reverse definition order.
"""
        return reversed(cls._member_names_)()
    def __setattr__(cls, name, value):
        """
    Block attempts to reassign Enum members.

    A simple assignment to the class namespace only changes one of the
    several possible ways to get an Enum member from the Enum class,
    resulting in an inconsistent Enumeration.
"""
        member_map = cls.__dict__.get('_member_map_', {})
        member_map = cls.__dict__.get('_member_map_', {})
        if name in member_map:
            raise AttributeError(f"cannot reassign member {name}")
        super().__setattr__(name, value)
    def _create_(cls, class_name, names, *, module = None, qualname = None, type = None, start = 1, boundary = None):
        """
    Convenience method to create a new Enum class.

    `names` can be:

    * A string containing member names, separated either with spaces or
  commas.  Values are incremented by 1 from `start`.
    * An iterable of member names.  Values are incremented by 1 from `start`.
    * An iterable of (member name, value) pairs.
    * A mapping of member name -> value pairs.
"""
        classdict = metacls.__prepare__(class_name, bases)
        metacls = cls.__class__
        if type:
            (type, cls)
            (cls)
        bases
        class_name
        cls._get_mixins_
        classdict = metacls.__prepare__(class_name, bases)
        if isinstance(names, str):
            names = names.replace(',', ' ').split()
        # [Block @0x00E2] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        module = [item for item in names if isinstance(item, str)]
        member_value = names[item]
        member_name = item
    def _convert_(cls, name, module, filter, source = None, *, boundary = None, as_global = False):
        """
    Create a new Enum subclass that replaces a collection of global constants
"""
        module_globals = sys.modules[module].__dict__
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        else:
            source = module_globals
            value
            name
            source.items()
            []
            # [Block @0x009C] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
            raise
            members.sort(key=lambda t: t[0])
            raise
            raise
            raise
        for t in members:
            pass
        tmp_cls = type(name, (object), body)
        cls = tmp_cls()
        global_enum(cls)
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        """ is already bound: """
        if name in cls._member_map_:
            if cls._member_map_[name] is not member:
                raise NameError(f"{name} is already bound: {cls._member_map_[name]}")
        else:
            found_descriptor = None
            descriptor_type = None
            class_type = None
            cls.__mro__[1:]
            for base in cls.__mro__[1:]:
                attr = base.__dict__.get(name)
                if attr:
                    if isinstance(attr, (property, DynamicClassAttribute)):
                        found_descriptor = attr
                        class_type = base
                        descriptor_type = 'enum'
                    elif _is_descriptor(attr):
                        found_descriptor = attr
                        if not descriptor_type:
                            return 'desc'
                        if not class_type:
                            base
                    else:
                        descriptor_type = 'attr'
                        class_type = base
                if descriptor_type in ('enum', 'desc'):
                    redirect.fget = getattr(found_descriptor, 'fget', None)
                    redirect._get = getattr(found_descriptor, '__get__', None)
                    redirect.fset = getattr(found_descriptor, 'fset', None)
                    redirect._set = getattr(found_descriptor, '__set__', None)
                    redirect.fdel = getattr(found_descriptor, 'fdel', None)
                    redirect._del = getattr(found_descriptor, '__delete__', None)
                redirect._attr_type = descriptor_type
                redirect._cls_type = class_type
                setattr(cls, name, redirect)
                if isinstance(attr, (property, DynamicClassAttribute)):
                    pass
                elif _is_descriptor(attr):
                    pass
                else:
                    descriptor_type = 'attr'
                    class_type = base
                if found_descriptor:
                    redirect = property()
                    redirect.member = member
                    redirect.__set_name__(cls, name)
                    descriptor_type in ('enum', 'desc')
                else:
                    setattr(cls, name, member)
        redirect._attr_type = descriptor_type
        redirect._cls_type = class_type
        setattr(cls, name, redirect)
        # [WARN] 1 instructions not decompiled
        #   @0x010A: POP_JUMP_IF_NOT_NONE arg=276
    __signature__ = __signature__()
    __static_attributes__ = []
    __classdictcell__ = __classdict__
    return __classcell__ := __class__

def Enum():
    """Enum"""
    def _generate_next_value_(name, start, count, last_values):
        """
    Generate the next value when not given.

    name: the name of the member
    start: the initial start value or None
    count: the number of existing members
    last_values: the list of values assigned
"""
        if not last_values:
            return start
        last_value = sorted(last_values).pop()
        last_value + 1
        return
    def _missing_(cls, value):
        pass
    def name(self):
        """The name of the Enum member."""
        return self._name_
    def value(self):
        """The value of the Enum member."""
        return self._value_
    __module__ = __name__
    __qualname__ = 'Enum'
    __firstlineno__ = 1137
    __doc__ = """
Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access:

  >>> Color.RED
  <Color.RED: 1>

- value lookup:

  >>> Color(1)
  <Color.RED: 1>

- name lookup:

  >>> Color['RED']
  <Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.
"""
    def __new__(cls, value):
        """_%s__in_progress"""
        if type(value) is cls:
            return value
        cls._value2member_map_[value]
        return
        # [WARN] 4 instructions not decompiled
        #   @0x02B2: POP_JUMP_IF_NONE arg=836
        #   @0x037E: POP_JUMP_IF_NOT_NONE arg=912
        #   @0x0386: POP_JUMP_IF_NOT_NONE arg=912
        #   @0x0392: POP_JUMP_IF_NOT_NONE arg=980
    def _add_alias_(self, name):
        self.__class__._add_member_(name, self)
    def _add_value_alias_(self, value):
        """ is already bound: """
        cls = self.__class__
        if value in cls._value2member_map_:
            pass
        else:
            cls._value2member_map_.setdefault(self, v_16)
            cls._hashable_values_.append(value)
    _generate_next_value_ = _generate_next_value_()
    _missing_ = _missing_()
    def __repr__(self):
        """<"""
        if not self.__class__._value_repr_:
            repr
        return f"<{self.__class__.__name__}.{self._name_}: {v_repr(self._value_)}>"
    def __str__(self):
        """."""
        return f"{self.__class__.__name__}.{self._name_}"
    def __dir__(self):
        """
    Returns public methods and other interesting attributes.
"""
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
        getattr(self, '__dict__', [])
        cls = [name for name in getattr(self, '__dict__', []) if not name[0] != '_' if name[0] != '_']
        names = [cls for cls in self.__class__.mro() if name[0] == '_']
    def __format__(self, format_spec):
        return str.__format__(str(self), format_spec)
    def __hash__(self):
        return hash(self._name_)
    def __reduce_ex__(self, proto):
        return (self.__class__, (self._value_))
    def __deepcopy__(self, memo):
        return self
    def __copy__(self):
        return self
    name = name()
    value = value()
    __static_attributes__ = []
    __classdictcell__ = __classdict__

def ReprEnum():
    """ReprEnum"""
    __module__ = __name__
    __qualname__ = 'ReprEnum'
    __firstlineno__ = 1362
    __doc__ = """
Only changes the repr(), leaving str() and format() to the mixed-in type.
"""
    __static_attributes__ = []

def IntEnum():
    """IntEnum"""
    __module__ = __name__
    __qualname__ = 'IntEnum'
    __firstlineno__ = 1368
    __doc__ = """
Enum where members are also (and must be) ints
"""
    __static_attributes__ = []

def StrEnum():
    """StrEnum"""
    def _generate_next_value_(name, start, count, last_values):
        """
    Return the lower-cased version of the member name.
"""
        return name.lower()
    __module__ = __name__
    __qualname__ = 'StrEnum'
    __firstlineno__ = 1374
    __doc__ = """
Enum where members are also (and must be) strings
"""
    def __new__(cls):
        """values must already be of type `str`"""
        if len(values) > 3:
            raise TypeError(f"too many arguments for str(): {values}")
        if len(values) == 1:
            if not isinstance(values[0], str):
                raise TypeError(f"{values[0]} is not a string")
            if len(values) >= 2:
                if not isinstance(values[1], str):
                    raise TypeError(f"encoding must be a string, not {values[1]}")
                if (len(values) == 3) and not isinstance(values[2], str):
                    raise TypeError('errors must be a string, not %r' % values[2])
                value = str(**values, **None)
                member = str.__new__(cls, value)
                member._value_ = value
                return member
            if len(values) == 3:
                pass
        elif len(values) >= 2:
            pass
        elif len(values) == 3:
            pass
    _generate_next_value_ = _generate_next_value_()
    __static_attributes__ = []
    __classdictcell__ = __classdict__

def pickle_by_global_name(self, proto):
    return self.name

def pickle_by_enum_name(self, proto):
    return (getattr, (self.__class__, self._name_))

def FlagBoundary():
    """FlagBoundary"""
    __module__ = __name__
    __qualname__ = 'FlagBoundary'
    __firstlineno__ = 1417
    __doc__ = """
control how out of range values are handled
"strict" -> error is raised             [default for Flag]
"conform" -> extra bits are discarded
"eject" -> lose flag status
"keep" -> keep flag status and all bits [default for IntFlag]
"""
    STRICT = auto()
    CONFORM = auto()
    EJECT = auto()
    KEEP = auto()
    __static_attributes__ = []

def Flag():
    """Flag"""
    def _generate_next_value_(name, start, count, last_values):
        """
    Generate the next value when not given.

    name: the name of the member
    start: the initial start value or None
    count: the number of existing members
    last_values: the last value assigned or None
"""
        if count:
            return 1
        high_bit = _high_bit(last_value)
        return 2 ** (high_bit + 1)
        return start
        # [WARN] 1 instructions not decompiled
        #   @0x0014: POP_JUMP_IF_NONE arg=30
    def _iter_member_by_value_(cls, value):
        """
    Extract all members from the value in definition (i.e. increasing value) order.
"""
        _iter_bits_lsb(value & cls._flag_mask_)
        for val in _iter_bits_lsb(value & cls._flag_mask_):
            yield cls._value2member_map_.get(val)
        raise
    def _iter_member_by_def_(cls, value):
        """
    Extract all members from the value in definition order.
"""
        None
        sorted(cls._iter_member_by_value_(value), key=lambda m: m._sort_order_)
        yield
        raise
    def _missing_(cls, value):
        """
    Create a composite member containing all canonical members present in `value`.

    If non-member values are present, result depends on `_boundary_` setting.
"""
        flag_mask = cls._flag_mask_
        singles_mask = cls._singles_mask_
        all_bits = cls._all_bits_
        neg_value = None
        if not isinstance(value, int):
            raise ValueError(f"{value} is not a valid {cls.__qualname__}")
        flag_mask = cls._flag_mask_
        singles_mask = cls._singles_mask_
        all_bits = cls._all_bits_
        neg_value = None
        if (value <= ~all_bits) and (value <= all_bits) and (cls._boundary_ is STRICT):
            max_bits = max(value.bit_length(), flag_mask.bit_length())
            raise ValueError(f"{cls} invalid value {value}\n    given {bin(value, max_bits)}\n  allowed {bin(flag_mask, max_bits)}")
        elif cls._boundary_ is CONFORM:
            value &= flag_mask
        elif cls._boundary_ is EJECT:
            return value
        elif cls._boundary_ is KEEP:
            if value < 0:
                value = max(all_bits + 1, 2 ** value.bit_length()) + value
            elif value < 0:
                neg_value = value
                if cls._boundary_ in (EJECT, KEEP):
                    value = all_bits + 1 + value
                else:
                    value = singles_mask & value
                    unknown = value & ~flag_mask
                    aliases = value & ~singles_mask
                    member_value = value & singles_mask
                    if unknown:
                        if cls._boundary_ is not KEEP:
                            raise ValueError(f"{cls.__name__}({value}) -->  unknown values {unknown} [{bin(unknown)}]")
                        elif cls._member_type_ is object:
                            pseudo_member = object.__new__(cls)
                        else:
                            pseudo_member = cls._member_type_.__new__(cls, value)
                            if not hasattr(pseudo_member, '_value_'):
                                pseudo_member._value_ = value
                    elif cls._member_type_ is object:
                        pass
                    else:
                        pseudo_member = cls._member_type_.__new__(cls, value)
        else:
            raise ValueError(f"{cls} unknown flag boundary {cls._boundary_}")
        raise ValueError(f"{cls} invalid value {value}\n    given {bin(value, max_bits)}\n  allowed {bin(flag_mask, max_bits)}")
        unknown = value & ~flag_mask
        aliases = value & ~singles_mask
        member_value = value & singles_mask
        # [Block @0x05F8] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        m = [m._name_ for m in members]
        pseudo_member._name_ = None
    __module__ = __name__
    __qualname__ = 'Flag'
    __firstlineno__ = 1432
    __doc__ = """
Support for flags
"""
    _numeric_repr_ = repr
    _generate_next_value_ = _generate_next_value_()
    _iter_member_by_value_ = _iter_member_by_value_()
    _iter_member_ = _iter_member_by_value_
    _iter_member_by_def_ = _iter_member_by_def_()
    _missing_ = _missing_()
    def __contains__(self, other):
        """
    Returns True if self has at least the same flags set as other.
"""
        if not isinstance(other, self.__class__):
            raise TypeError(f"unsupported operand type(s) for 'in': {type(other).__qualname__} and {self.__class__.__qualname__}")
        return other._value_ & self._value_ == other._value_
    def __iter__(self):
        """
    Returns flags in definition order.
"""
        None
        self._iter_member_(self._value_)
        yield
        raise
    def __len__(self):
        return self._value_.bit_count()
    def __repr__(self):
        cls_name = self.__class__.__name__
        cls_name = self.__class__.__name__
        if not self.__class__._value_repr_:
            repr
        else:
            if self._name_:
                return f"<{cls_name}: {v_repr(self._value_)}>"
            return f"<{cls_name}.{self._name_}: {v_repr(self._value_)}>"
    def __str__(self):
        cls_name = self.__class__.__name__
        if self._name_:
            return f"{cls_name}({self._value_})"
        return f"{cls_name}.{self._name_}"
    def __bool__(self):
        return bool(self._value_)
    def _get_value(self, flag):
        if isinstance(flag, self.__class__):
            return flag._value_
        if (self._member_type_ is not object) and isinstance(flag, self._member_type_):
            return flag
        return NotImplemented
    def __or__(self, other):
        other_value = self._get_value(other)
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        return value | other_value
        if other_value:
            return (self, other)
        self.__class__
        for flag in (self, other):
            if self._get_value(flag):
                raise TypeError(f"'{flag}' cannot be combined with other flags with |")
            raise TypeError(f"'{flag}' cannot be combined with other flags with |")
            self.__class__
            return value | other_value
    def __and__(self, other):
        other_value = self._get_value(other)
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        return value & other_value
        if other_value:
            return (self, other)
        self.__class__
        for flag in (self, other):
            if self._get_value(flag):
                raise TypeError(f"'{flag}' cannot be combined with other flags with &")
            raise TypeError(f"'{flag}' cannot be combined with other flags with &")
            self.__class__
            return value & other_value
    def __xor__(self, other):
        other_value = self._get_value(other)
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        return value ^ other_value
        if other_value:
            return (self, other)
        self.__class__
        for flag in (self, other):
            if self._get_value(flag):
                raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
            raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
            self.__class__
            return value ^ other_value
    def __invert__(self):
        if self._get_value(self):
            raise TypeError(f"'{self}' cannot be inverted")
        self._boundary_
        self._inverted_ = self.__class__(~self._value_)
        return self._inverted_
        # [WARN] 1 instructions not decompiled
        #   @0x005C: POP_JUMP_IF_NOT_NONE arg=342
    __rand__ = __and__
    __ror__ = __or__
    __rxor__ = __xor__
    __static_attributes__ = ('_inverted_',)
    __classdictcell__ = __classdict__

def IntFlag():
    """IntFlag"""
    __module__ = __name__
    __qualname__ = 'IntFlag'
    __firstlineno__ = 1673
    __doc__ = """
Support for integer-based Flags
"""
    __static_attributes__ = []

def _high_bit(value):
    """
    returns index of highest bit, or -1 if value is zero or negative
"""
    return value.bit_length() - 1

def unique(enumeration):
    """
    Class decorator for enumerations ensuring unique member values.
"""
    duplicates = []
    enumeration.__members__.items()
    # [Block @0x003A] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
    # [Block @0x00DC] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')

def _dataclass_repr(self):
    """, """
    dcf = self.__dataclass_fields__
    return (dcf[k].repr for k in dcf.keys()() if not dcf[k].repr)

def global_enum_repr(self):
    """
    use module.enum_name instead of class.enum_name

    the module is the last module in case of a multi-module name
"""
    module = self.__class__.__module__.split('.')[-1]
    return f"{module}.{self._name_}"

def global_flag_repr(self):
    """
    use module.flag_name instead of class.flag_name

    the module is the last module in case of a multi-module name
"""
    module = self.__class__.__module__.split('.')[-1]
    cls_name = self.__class__.__name__
    if self._name_:
        return f"{module}.{cls_name}({self._value_})"
    if self._boundary_ is not FlagBoundary.KEEP:
        '|'.join
    else:
        name = []
        self._name_.split('|')
        name = [n for n in self._name_.split('|') if n[0].isdigit()]
    return f"{module}.{self._name_}"
    name = [f"{module}.{name}" for name in self.name.split('|') for n in self]

def global_str(self):
    """
    use enum_name instead of class.enum_name
"""
    if self._name_:
        cls_name = self.__class__.__name__
        return f"{cls_name}({self._value_})"
    else:
        return self._name_

def global_enum(cls, update_str):
    """
    decorator that makes the repr() of an enum member reference its module
    instead of its class; also exports all members to the enum's module's
    global namespace
"""
    if issubclass(cls, Flag):
        cls.__repr__ = global_flag_repr
    else:
        cls.__repr__ = global_enum_repr
        if issubclass(cls, ReprEnum):
            if update_str:
                cls.__str__ = global_str
            sys.modules[cls.__module__].__dict__.update(cls.__members__)
            return cls
        else:
            cls.__str__ = global_str

def _simple_enum(etype, *, boundary, use_args):
    """
    Class decorator that converts a normal class into an :class:`Enum`.  No
    safety checks are done, and some advanced behavior (such as
    :func:`__init_subclass__`) is not available.  Enum creation can be faster
    using :func:`_simple_enum`.

    >>> from enum import Enum, _simple_enum
    >>> @_simple_enum(Enum)
    ... class Color:
    ...     RED = auto()
    ...     GREEN = auto()
    ...     BLUE = auto()
    >>> Color
    <enum 'Color'>
"""
    def convert_class(cls):
        enum_method = getattr(etype, name)
        found_method = getattr(enum_class, name)
        object_method = getattr(object, name)
        data_type_method = getattr(member_type, name)
        cls_name = cls.__name__
        if use_args:
            use_args = etype._use_args_
            cls.__dict__.get
        __new__ = '__new__'
        if __new__:
            new_member = __new__.__func__
            new_member = etype._member_type_.__new__
        attrs = {}
        body = {}
        if __new__:
            etype._generate_next_value_
        issubclass
        member_type := etype._member_type_
        unhashable_values := []
        hashable_values := []
        value2member_map := {}
        member_map := {}
        member_names := []
        if etype(Flag) and not boundary:
            etype._boundary_
        cls.__dict__.items()
        # [Block @0x0360] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        cls.__dict__.items()
        gnv_last_values = [name for name in ('__repr__', '__str__', '__format__', '__reduce_ex__') if not name not in body]
        # [Block @0x0594] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        member = None(enum_class, value, **None)
        value = value[0]
        setattr(cls, v_253, member)
        hashable_values.append(value)
        member_names.append(name)
        single_bits |= value
        member_list = [m._value_ for m in enum_class]
        member = None(enum_class, value, **None)
        value = value[0]
        setattr(cls, v_253, member)
        enum_class._value2member_map_.setdefault(value, member)
        contained = None
    return convert_class

def EnumCheck():
    """EnumCheck"""
    __module__ = __name__
    __qualname__ = 'EnumCheck'
    __firstlineno__ = 1960
    __doc__ = """
various conditions to check an enumeration for
"""
    CONTINUOUS = 'no skipped integer values'
    NAMED_FLAGS = 'multi-flag aliases may not contain unnamed flags'
    UNIQUE = 'one name per value'
    __static_attributes__ = []

def verify():
    """verify"""
    __module__ = __name__
    __qualname__ = 'verify'
    __firstlineno__ = 1971
    __doc__ = """
Check an enumeration for various constraints. (see EnumCheck)
"""
    def __init__(self):
        self.checks = checks
    def __call__(self, enumeration):
        missing = []
        checks = self.checks
        cls_name = enumeration.__name__
        if Flag:
            if issubclass(enumeration, Flag):
                enum_type = 'flag'
            elif issubclass(enumeration, Enum):
                enum_type = 'enum'
            else:
                'the \'verify\' decorator only works with Enum and Flag'
                TypeError
                raise
                checks
                # [Block @0x00C0] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        elif issubclass(enumeration, Enum):
            pass
        else:
            'the \'verify\' decorator only works with Enum and Flag'
            TypeError
        missed = [v for v in values if v not in member_values for val in missing_names if v not in member_values]
        alias = 'alias %s is missing' % missing_names[0]
        value = 'value 0x%x' % missing_value
    __static_attributes__ = ['checks']
    __classdictcell__ = __classdict__

def _test_simple_enum(checked_enum, simple_enum):
    """
    A function that can be used to test an enum created with :func:`_simple_enum`
    against the version created by subclassing :class:`Enum`::

    >>> from enum import Enum, _simple_enum, _test_simple_enum
    >>> @_simple_enum(Enum)
    ... class Color:
    ...     RED = auto()
    ...     GREEN = auto()
    ...     BLUE = auto()
    >>> class CheckedColor(Enum):
    ...     RED = auto()
    ...     GREEN = auto()
    ...     BLUE = auto()
    >>> _test_simple_enum(CheckedColor, Color)

    If differences are found, a :exc:`TypeError` is raised.
"""
    checked_value = checked_dict[key]
    simple_value = simple_dict[key]
    failed = []
    failed = []
    if checked_enum.__dict__ != simple_enum.__dict__:
        name = [key for key in set(checked_keys + simple_keys) if key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__') if checked_value != simple_value if compressed_checked_value != compressed_simple_value]
    elif failed:
        raise TypeError("""enum mismatch:
   %s""" % """
   """.join(failed))
    method = [[] for name in member_names if name not in simple_keys if not failed_member if checked_value != simple_value for key in simple_member_dict + list.__dict__ if name not in simple_keys if not failed_member if checked_value != simple_value]
    failed_member = []
    failed.append('missing member from simple enum: %r' % name)
    failed.append('extra member in simple enum: %r' % name)
    checked_value = checked_member_dict[key]
    simple_value = simple_member_dict[key]
    simple_method = [method for method in ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__') if method in simple_keys if checked_method != simple_method]
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)

def _old_convert_(etype, name, module, filter, source, *, boundary):
    """
    Create a new Enum subclass that replaces a collection of global constants
"""
    module_globals = sys.modules[module].__dict__
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    else:
        source = module_globals
        value
        name
        source.items()
        []
        # [Block @0x009C] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        raise
        members.sort(key=lambda t: t[0])
        raise
        raise
# [Block @0x0000] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
