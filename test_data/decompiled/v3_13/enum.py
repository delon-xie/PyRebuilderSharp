# Decompiled from: <module>

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

import sys
import builtins as bltns
from types import MappingProxyType, DynamicClassAttribute
__all__ = ['EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin']
ReprEnum = EJECT := Flag := Enum := None

class nonmember(object):
    """
    Protects item from becoming an Enum member during class creation.
"""
    def __init__(self, value):
        v_16.value = self

class member(object):
    """
    Forces item to become an Enum member during class creation.
"""
    def __init__(self, value):
        v_16.value = self

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
    if not isinstance(obj, type):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if not cls_name == v_35:
        qualname.endswith(e_pattern)
    return

def _is_private(cls_name, name):
    pattern = f"_{cls_name}__"
    pat_len = len(pattern)
    return (len(name) > pat_len) and name.startswith(pattern) and (name[-1] != '_') or (name[-2] != '_')
    return False

def _is_single_bit(num):
    """
    True if only one bit set in num (should be an int)
"""
    if num == 0:
        return False
    num &= num - 1
    return num == 0

def _make_class_unpicklable(obj):
    """
    Make the given obj un-picklable.

    obj should be either a dictionary, or an Enum
"""
    def _break_on_call_reduce(self, proto):
        raise TypeError('%r cannot be pickled' % self)
    if isinstance(obj, dict):
        pass
    else:
        setattr(obj, '__reduce_ex__', _break_on_call_reduce)
        setattr(obj, '__module__', '<unknown>')

def _iter_bits_lsb(num):
    original = num
    if isinstance(num, Enum):
        num = num.value
    elif num < 0:
        raise ValueError('%r is not a positive integer' % original)
    b = num & ~num + 1
    yield b
    num ^= b

def show_flag_values(value):
    return list(_iter_bits_lsb(value))

def bin(num, max_bits = None):
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
        return f"{sign} {digits}"
    # [WARN] 1 instructions not decompiled
    #   @0x00FE: POP_JUMP_IF_NONE arg=318

class _not_given:
    def __repr__(self):
        return '<not given>'
_not_given = _not_given()

class _auto_null:
    def __repr__(self):
        return '_auto_null'
_auto_null = _auto_null()

class auto:
    """
    Instances are replaced with an appropriate value in Enum class suites.
"""
    def __init__(self, value = _auto_null):
        v_16.value = self

    def __repr__(self):
        return 'auto(%r)' % self.value

class property(DynamicClassAttribute):
    """
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
            return self.fget(instance)
            if self._attr_type == 'desc':
                getattr
            else:
                ownerclass._member_map_[self.name]
                return
            return getattr(self._cls_type, self.name)
        self.fget
        # [WARN] 3 instructions not decompiled
        #   @0x0004: POP_JUMP_IF_NOT_NONE arg=114
        #   @0x001E: POP_JUMP_IF_NONE arg=58
        #   @0x0088: POP_JUMP_IF_NONE arg=174

    def __set__(self, instance, value):
        if self.fset:
            return self.fset(self, v_18)
        raise AttributeError(f"<enum {self.clsname}> cannot set attribute {self.name}")
        # [WARN] 1 instructions not decompiled
        #   @0x0018: POP_JUMP_IF_NONE arg=62

    def __delete__(self, instance):
        if self.fdel:
            return self.fdel(instance)
        raise AttributeError(f"<enum {self.clsname}> cannot delete attribute {self.name}")
        # [WARN] 1 instructions not decompiled
        #   @0x0018: POP_JUMP_IF_NONE arg=62

    def __set_name__(self, ownerclass, name):
        v_32.name = self
        self.clsname = ownerclass.__name__

class _proto_member:
    """
    intermediate step for enum members between class execution and final creation
"""
    def __init__(self, value):
        v_16.value = self

    def __set_name__(self, enum_class, member_name):
        """
    convert each quasi-member into an instance of the new enum class
"""
        delattr(self, v_18)
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
                enum_member = enum_class._new_member_(**None, **(enum_class, args))
        # [WARN] 3 instructions not decompiled
        #   @0x020A: POP_JUMP_IF_NONE arg=800
        #   @0x04F6: POP_JUMP_IF_NONE arg=1316
        #   @0x056A: POP_JUMP_IF_NONE arg=1560

class EnumDict(dict):
    def member_names(self):
        return list(self._member_names)
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
        v_16._cls_name = self

    def __setitem__(self, key, value):
        """
    Changes anything not dundered or not a descriptor.

    If an enum member name is used twice, an error is raised; duplicate
    values are not checked for.

    Single underscore (sunder) names are reserved.
"""
        if self._cls_name:
            if _is_private(self._cls_name, key):
                pass
            else:
                _is_sunder(key)
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
                            super().__setitem__(self, v_18)
                            value = t(**None, **auto_valued)
                            raise
                            raise
                    elif (key == '_ignore_') and isinstance(value, str):
                        value = value.replace(',', ' ').split()
                    else:
                        value = list(value)
                        v_32._ignore = self
                        already = set(value) & set(self._member_names)
                        if already:
                            raise ValueError(f"_ignore_ cannot specify already set names: {already}")
                elif key == '_generate_next_value_':
                    pass
                elif key == '_ignore_':
                    pass
        _is_sunder(key)
        value = [auto_valued.append(v) for v in value if v.value == _auto_null]
        value = auto_valued[0]
        # [WARN] 2 instructions not decompiled
        #   @0x001A: POP_JUMP_IF_NONE arg=88
        #   @0x03A2: POP_JUMP_IF_NONE arg=992
    member_names = member_names()

    def update(self, members):
        members.keys()
        more_members.items()
        for (value, name) in members:
            pass
        raise
        raise
        for (value, name) in members:
            pass
_EnumDict = EnumDict

class EnumType(type):
    def __prepare__(metacls, cls, bases):
        metacls._check_for_existing_members_(metacls, v_18)
        enum_dict = EnumDict(cls)
        if first_enum:
            return enum_dict
        return enum_dict
        # [WARN] 1 instructions not decompiled
        #   @0x0062: POP_JUMP_IF_NONE arg=134

    def __members__(cls):
        """
    Returns a mapping of member name->value.

    This mapping lists all enum members, including aliases.  Note that
    this is a read-only view of the internal mapping.
"""
        return MappingProxyType(cls._member_map_)

    def _check_for_existing_members_(mcls, class_name, bases):
        bases
        chain.__mro__
        if not isinstance(base, EnumType):
            pass
        elif not base._member_names_:
            pass
        else:
            raise TypeError(f"<enum {class_name}> cannot extend {base}")

    def _get_mixins_(mcls, class_name, bases):
        """
    Returns the type for creating enum members, and the first inherited
    enum class.

    bases: the tuple of bases that was given to __new__
"""
        if not bases:
            return (object, Enum)
        first_enum = bases[-1]
        if not isinstance(first_enum, EnumType):
            raise TypeError('new enumerations should be created as `EnumName([mixin_type, ...] [data_type,] enum_type)`')
        if not mcls._find_data_type_(mcls, v_18):
            object

    def _find_data_repr_(mcls, class_name, bases):
        bases
        chain.__mro__
        if base is object:
            pass
        else:
            if isinstance(base, EnumType):
                base._value_repr_
                return
            if not '__repr__' in base.__dict__:
                pass
            else:
                if '__dataclass_fields__' in base.__dict__:
                    if ('__dataclass_params__' in base.__dict__) and base.__dict__['__dataclass_params__'].repr:
                        _dataclass_repr
                        return
                    base.__dict__['__repr__']
                    return
                    base.__dict__['__repr__']
                    return
                base.__dict__['__repr__']
                return

    def _find_data_type_(mcls, class_name, bases):
        data_types = set()
        base_chain = set()
        bases
        if len(data_types) > 1:
            raise TypeError(f"too many data types for {class_name}: {data_types}")
        if data_types:
            return data_types.pop()
        candidate = None
        chain.__mro__
        base_chain.add(base)
        if base is object:
            pass
        elif isinstance(base, EnumType) and (base._member_type_ is not object):
            data_types.add(base._member_type_)

    def _find_new_(mcls, classdict, member_type, first_enum):
        """
    Returns the __new__ to be used for creating the enum members.

    classdict: the class dictionary given to __new__
    member_type: the data type whose __new__ will be used by default
    first_enum: enumeration to check for an overriding __new__
"""
        target = getattr(mcls, v_118, None)
        __new__ = classdict.get('__new__', None)
        if first_enum is not None:
            return __new__ is not None
        if __new__:
            return ('__new_member__', '__new__')
        return first_enum and (__new__ in (Enum.__new__, object.__new__))
        for method in ('__new_member__', '__new__'):
            pass
        __new__ = target
        for method in ('__new_member__', '__new__'):
            (mcls, v_35)
            target = getattr(mcls, v_118, None)
            if not target not in {None, None.__new__, object.__new__, Enum.__new__}:
                pass
            else:
                __new__ = target
                if __new__:
                    pass
                if first_enum:
                    return __new__ in (Enum.__new__, object.__new__)
                use_args = False
                return (mcls, v_69, use_args)
        # [WARN] 2 instructions not decompiled
        #   @0x0046: POP_JUMP_IF_NOT_NONE arg=282
        #   @0x011C: POP_JUMP_IF_NONE arg=360

    def __signature__(cls):
        from inspect import Parameter, Signature
        if cls._member_names_:
            return Signature([Parameter('values', Parameter.VAR_POSITIONAL)])
        return Signature([Parameter('new_class_name', Parameter.POSITIONAL_ONLY), Parameter('names', Parameter.POSITIONAL_OR_KEYWORD), Parameter('module', Parameter.KEYWORD_ONLY, default=None), Parameter('qualname', Parameter.KEYWORD_ONLY, default=None), Parameter('type', Parameter.KEYWORD_ONLY, default=None), Parameter('start', Parameter.KEYWORD_ONLY, default=1), Parameter('boundary', Parameter.KEYWORD_ONLY, default=None)])
    __doc__ = """
Metaclass for Enum
"""
    __prepare__ = __prepare__()

    def __new__(metacls, cls, bases, classdict, *, boundary = None, _simple = False):
        if _simple:
            return None(metacls, cls, metacls, v_35, **kwds)
        classdict.setdefault('_ignore_', []).append('_ignore_')
        ignore = classdict['_ignore_']
        ignore
        member_names = classdict._member_names
        invalid_names = set(member_names) & {'mro', ''}
        if invalid_names:
            raise 'invalid enum member name(s) %s'(','.join % (<genexpr>)(invalid_names()))
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        if Flag:
            if bases and issubclass(bases[-1], Flag):
                bits = 0
                inverted = []
                member_names
            enum_class = None(metacls, cls, metacls, v_35, **kwds)
            delattr(enum_class, '_%s__in_progress' % cls)
            super(__class__, metacls).__new__
            classdict.update(enum_class.__dict__)
            if ReprEnum:
                if (ReprEnum in bases) and (member_type is object):
                    raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
                if '__format__' not in classdict:
                    enum_class.__format__ = member_type.__format__
                elif '__str__' not in classdict:
                    method = member_type.__str__
                    if method is object.__str__:
                        method = member_type.__repr__
                    enum_class.__str__ = method
                    ('__repr__', '__str__', '__format__', '__reduce_ex__')
                    if Flag:
                        issubclass(enum_class, Flag)
                    elif Enum:
                        if save_new:
                            enum_class.__new_member__ = __new__
                        enum_class.__new__ = Enum.__new__
                        if _order_:
                            str
                            _order_
                            isinstance
                        elif Flag:
                            pass
                        elif Flag:
                            pass
                        elif Flag:
                            pass
                        elif _order_:
                            pass
                    if not name not in classdict:
                        pass
                    else:
                        enum_method = getattr(first_enum, name)
                        found_method = getattr(enum_class, name)
                        object_method = getattr(object, name)
                        data_type_method = getattr(member_type, name)
                        if not found_method in (data_type_method, object_method):
                            pass
                        else:
                            setattr(enum_class, name, enum_method)
                ('__repr__', '__str__', '__format__', '__reduce_ex__')
            ('__repr__', '__str__', '__format__', '__reduce_ex__')
        if type(_gnv) is not staticmethod:
            _gnv = staticmethod(_gnv)
        classdict = dict(classdict.items())
        if _gnv:
            bits = [classdict[name] for name in member_names]
        classdict.pop(key, None)
        bits = [classdict[name] for name in member_names]
        p = [n for n in member_names if p.value < 0 if p.value[0] < 0 if cls != 'Flag' if _order_ != enum_class._member_names_ if member_list != sorted(member_list)]
        p = [n for n in member_names if p.value < 0 if p.value[0] < 0 if cls != 'Flag' if _order_ != enum_class._member_names_ if member_list != sorted(member_list)]
        enum_class = [p for p in inverted]
        enum_class = [p for p in inverted]
        _order_ = [name for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__')]
        _order_ = [name for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__')]
        member_list = [m._value_ for m in enum_class for o in _order_ for o in _order_]
        member_list = [m._value_ for m in enum_class for o in _order_ for o in _order_]
        _order_ = [o for o in _order_ for o in _order_]
        _order_ = [o for o in _order_ for o in _order_]
        _order_ = [o for o in _order_]
        _order_ = [o for o in _order_]
        # [WARN] 5 instructions not decompiled
        #   @0x018E: POP_JUMP_IF_NONE arg=460
        #   @0x0200: POP_JUMP_IF_NONE arg=524
        #   @0x037A: POP_JUMP_IF_NONE arg=1684
        #   @0x0738: POP_JUMP_IF_NONE arg=2130
        #   @0x0914: POP_JUMP_IF_NONE arg=2472

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
                value = (cls, v_18) + values
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
        #   @0x0078: POP_JUMP_IF_NOT_NONE arg=152

    def __contains__(cls, value):
        """Return True if `value` is in `cls`.

    `value` is in `cls` if:
    1) `value` is a member of `cls`, or
    2) `value` is the value of one of the `cls`'s members.
    3) `value` is a pseudo-member (flags)
"""
        if isinstance(cls, v_16):
            return True
        if issubclass(cls, Flag):
            pass
        else:
            return not cls in v_16._unhashable_values_ and (cls in v_16._hashable_values_)

    def __delattr__(cls, attr):
        if cls in v_16._member_map_:
            raise AttributeError(f"{cls.__name__} cannot delete member {attr}.")
        super().__delattr__(attr)

    def __dir__(cls):
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
        # [WARN] 1 instructions not decompiled
        #   @0x000C: POP_JUMP_IF_NONE arg=88

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
        if cls in v_19:
            raise AttributeError(f"cannot reassign member {name}")
        super().__setattr__(cls, v_18)

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
        metacls = cls.__class__
        if type:
            (cls, v_80)
            (cls)
        v_25
        cls
        cls._get_mixins_
        classdict = metacls.__prepare__(cls, v_25)
        if isinstance(names, str):
            names = names.replace(',', ' ').split()
        # [Block @0x00DE] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        # [Block @0x01F6] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        module = [item for item in names]
        member_value = names[item]
        member_name = item
        module = [item for item in names]
        # [WARN] 1 instructions not decompiled
        #   @0x001C: POP_JUMP_IF_NOT_NONE arg=38

    def _convert_(cls, name, module, filter, source = None, *, boundary = None, as_global = False):
        """
    Create a new Enum subclass that replaces a collection of global constants
"""
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        else:
            source = module_globals
            value
            name
            source.items()
            []
            members.sort(key=lambda t: (t[1], t[0]))
            t
            members
            {}
            tmp_cls = type(name, (object), body)
            if not boundary:
                KEEP
            cls = tmp_cls()
            if as_global:
                global_enum(cls)
            else:
                sys.modules[cls.__module__].__dict__.update(cls.__members__)
                return cls
            raise
            filter(name)
            if not True:
                pass
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()

    def _add_member_(cls, name, member):
        if (cls in v_16._member_map_) and (cls._member_map_[name] is not member):
            raise NameError(f"{name} is already bound: {cls._member_map_[name]}")
        found_descriptor = None
        descriptor_type = None
        class_type = None
        cls.__mro__[1:]
        if found_descriptor:
            redirect = property()
            v_40.member = cls
            redirect.__set_name__
        else:
            setattr(cls, name, member)
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
        found_descriptor = None
        descriptor_type = None
        class_type = None
        cls.__mro__[1:]
        cls(name)
        v_72._attr_type = cls
        v_88._cls_type = cls
        setattr(cls, name, redirect)
        # [WARN] 1 instructions not decompiled
        #   @0x00EC: POP_JUMP_IF_NOT_NONE arg=244
    __signature__ = __signature__()
EnumMeta = EnumType

class Enum(metaclass=EnumType):
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
        if type(value) is cls:
            return value
        cls._value2member_map_[value]
        return
        # [WARN] 4 instructions not decompiled
        #   @0x0278: POP_JUMP_IF_NONE arg=770
        #   @0x033C: POP_JUMP_IF_NOT_NONE arg=842
        #   @0x0342: POP_JUMP_IF_NOT_NONE arg=842
        #   @0x034C: POP_JUMP_IF_NOT_NONE arg=908

    def _add_alias_(self, name):
        self.__class__._add_member_(self, v_16)

    def _add_value_alias_(self, value):
        cls = self.__class__
        try:
            try:
                raise ValueError(f"{value} is already bound: {cls._value2member_map_[value]}")
                return None
                cls._value2member_map_.setdefault(self, v_16)
                cls._hashable_values_.append(value)
                return None
                for m in cls._member_map_.values():
                    m._value_ == value
                    if not True:
                        pass
                    elif self is not v_48:
                        raise ValueError(f"{value} is already bound: {cls._value2member_map_[value]}")
                raise
            except TypeError:
                cls._member_map_.values()
        except TypeError:
            cls._member_map_.values()
    _generate_next_value_ = _generate_next_value_()
    _missing_ = _missing_()

    def __repr__(self):
        if not self.__class__._value_repr_:
            repr
        return f"<{self.__class__.__name__}.{self._name_}: {v_repr(self._value_)}>"

    def __str__(self):
        return f"{self.__class__.__name__}.{self._name_}"

    def __dir__(self):
        """
    Returns public methods and other interesting attributes.
"""
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
        getattr(self, '__dict__', [])
        self.__class__.mro()
        names = sorted(set(['__class__', '__doc__', '__eq__', '__hash__', '__module__']) | interesting)
        return names
        cls.__dict__.items()
        if name[0] == '_':
            pass
        elif isinstance(obj, property):
            if obj.fget:
                if self not in v_32._member_map_:
                    interesting.add(name)
                else:
                    interesting.discard(name)
            interesting.add(name)
        elif not self not in v_32._member_map_:
            pass
        else:
            interesting.add(name)
        if not name[0] != '_':
            pass
        elif not self not in v_32._member_map_:
            pass
        else:
            interesting.add(name)
        # [WARN] 1 instructions not decompiled
        #   @0x01DE: POP_JUMP_IF_NOT_NONE arg=512

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

class ReprEnum(Enum):
    """
    Only changes the repr(), leaving str() and format() to the mixed-in type.
"""
    pass

class IntEnum(int, ReprEnum):
    """
    Enum where members are also (and must be) ints
"""
    pass

class StrEnum(str, ReprEnum):
    def _generate_next_value_(name, start, count, last_values):
        """
    Return the lower-cased version of the member name.
"""
        return name.lower()
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
                member = str.__new__(cls, value)
                v_35._value_ = cls
                return member
            if len(values) == 3:
                pass
        elif len(values) >= 2:
            pass
        elif len(values) == 3:
            pass
    _generate_next_value_ = _generate_next_value_()

def pickle_by_global_name(self, proto):
    return self.name
_reduce_ex_by_global_name = pickle_by_global_name

def pickle_by_enum_name(self, proto):
    return (getattr, (self.__class__, self._name_))

class FlagBoundary(StrEnum):
    """
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
STRICT = *FlagBoundary
CONFORM = *FlagBoundary
EJECT = *FlagBoundary
KEEP = *FlagBoundary

class Flag(Enum, boundary=STRICT):
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
        #   @0x0012: POP_JUMP_IF_NONE arg=26

    def _iter_member_by_value_(cls, value):
        """
    Extract all members from the value in definition (i.e. increasing value) order.
"""
        _iter_bits_lsb(cls & v_16._flag_mask_)
        raise
        yield cls._value2member_map_.get(val)

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
        if not isinstance(value, int):
            raise ValueError(f"{value} is not a valid {cls.__qualname__}")
        flag_mask = cls._flag_mask_
        singles_mask = cls._singles_mask_
        all_bits = cls._all_bits_
        neg_value = None
        if (value <= ~all_bits) and (cls <= all_bits) and (cls._boundary_ is STRICT):
            max_bits = max(value.bit_length(), flag_mask.bit_length())
            raise ValueError(f"{cls} invalid value {value}\n    given {bin(cls, v_22)}\n  allowed {bin(cls, v_38)}")
        if cls._boundary_ is CONFORM:
            value = cls & v_18
        else:
            if cls._boundary_ is EJECT:
                return value
            if cls._boundary_ is KEEP:
                if value < 0:
                    value = max(all_bits + 1, 2 ** value.bit_length()) + value
                elif value < 0:
                    neg_value = value
                    if cls._boundary_ in (EJECT, KEEP):
                        value = all_bits + 1 + value
                    else:
                        value = cls & v_49
                        unknown = cls & ~v_18
                        aliases = cls & ~v_19
                        member_value = cls & v_19
                        if unknown:
                            if cls._boundary_ is not KEEP:
                                raise ValueError(f"{cls.__name__}({value}) -->  unknown values {unknown} [{bin(unknown)}]")
                            if cls._member_type_ is object:
                                pseudo_member = object.__new__(cls)
                            else:
                                pseudo_member = cls._member_type_.__new__(cls, value)
                                if not hasattr(pseudo_member, '_value_'):
                                    v_26._value_ = cls
                        elif cls._member_type_ is object:
                            pass
                        else:
                            pseudo_member = cls._member_type_.__new__(cls, value)
            else:
                raise ValueError(f"{cls} unknown flag boundary {cls._boundary_}")
        raise ValueError(f"{cls} invalid value {value}\n    given {bin(cls, v_22)}\n  allowed {bin(cls, v_38)}")
        value = [cls | v_205._value_ for m in cls._iter_member_(member_value)]
        # [Block @0x0562] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        # [Block @0x0620] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        m = [m._name_ for m in members]
        m = [m._name_ for m in members]
        pseudo_member._name_ = None
        # [WARN] 1 instructions not decompiled
        #   @0x07A6: POP_JUMP_IF_NONE arg=1990
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
        if not isinstance(self, v_16.__class__):
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
        if not self.__class__._value_repr_:
            repr
        else:
            if self._name_:
                return f"<{cls_name}: {v_repr(self._value_)}>"
            return f"<{cls_name}.{self._name_}: {v_repr(self._value_)}>"
        # [WARN] 1 instructions not decompiled
        #   @0x008A: POP_JUMP_IF_NOT_NONE arg=196

    def __str__(self):
        cls_name = self.__class__.__name__
        if self._name_:
            return f"{cls_name}({self._value_})"
        return f"{cls_name}.{self._name_}"
        # [WARN] 1 instructions not decompiled
        #   @0x0044: POP_JUMP_IF_NOT_NONE arg=112

    def __bool__(self):
        return bool(self._value_)

    def _get_value(self, flag):
        if isinstance(self, v_16.__class__):
            return flag._value_
        if (self._member_type_ is not object) and isinstance(self, v_16._member_type_):
            return flag
        return NotImplemented

    def __or__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        return self | v_50
        if other_value:
            return (self, other)
        self.__class__
        for flag in (self, other):
            if self._get_value(flag):
                raise TypeError(f"'{flag}' cannot be combined with other flags with |")
            raise TypeError(f"'{flag}' cannot be combined with other flags with |")
            self.__class__
            return self | v_50
        for flag in (self, other):
            if self._get_value(flag):
                raise TypeError(f"'{flag}' cannot be combined with other flags with |")
            raise TypeError(f"'{flag}' cannot be combined with other flags with |")
            self.__class__
            return self | v_50

    def __and__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        return self & v_50
        if other_value:
            return (self, other)
        self.__class__
        for flag in (self, other):
            if self._get_value(flag):
                raise TypeError(f"'{flag}' cannot be combined with other flags with &")
            raise TypeError(f"'{flag}' cannot be combined with other flags with &")
            self.__class__
            return self & v_50
        for flag in (self, other):
            if self._get_value(flag):
                raise TypeError(f"'{flag}' cannot be combined with other flags with &")
            raise TypeError(f"'{flag}' cannot be combined with other flags with &")
            self.__class__
            return self & v_50

    def __xor__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        return self ^ v_50
        if other_value:
            return (self, other)
        self.__class__
        for flag in (self, other):
            if self._get_value(flag):
                raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
            raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
            self.__class__
            return self ^ v_50
        for flag in (self, other):
            if self._get_value(flag):
                raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
            raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
            self.__class__
            return self ^ v_50

    def __invert__(self):
        if self._get_value(self):
            raise TypeError(f"'{self}' cannot be inverted")
        self._boundary_
        if self in (EJECT, KEEP):
            self._inverted_ = self.__class__(~self._value_)
            return self._inverted_
        self._inverted_ = self.__class__(self._singles_mask_ & ~self._value_)
        return self._inverted_
        # [WARN] 2 instructions not decompiled
        #   @0x0022: POP_JUMP_IF_NOT_NONE arg=68
        #   @0x005A: POP_JUMP_IF_NOT_NONE arg=328
    __rand__ = __and__
    __ror__ = __or__
    __rxor__ = __xor__

class IntFlag(int, ReprEnum, Flag, boundary=KEEP):
    """
    Support for integer-based Flags
"""
    pass

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
    if duplicates:
        ', '.join
        name
        alias
        duplicates
    return enumeration
    if not enumeration != v_35.name:
        pass
    else:
        duplicates.append((enumeration, v_35.name))
    # [Block @0x00DA] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
    # [Block @0x00FA] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')

def _dataclass_repr(self):
    dcf = self.__dataclass_fields__
    return (<genexpr>)(dcf.keys()())

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
        return '|'
    name = []
    self._name_.split('|')
    return '|'.join(name)
    if n[0].isdigit():
        name.append(n)
    else:
        name.append(f"{module}.{n}")
    return f"{module}.{self._name_}"
    name = [f"{module}.{name}" for name in self.name.split('|') for n in self]
    name = [f"{module}.{name}" for name in self.name.split('|') for n in self]
    # [WARN] 1 instructions not decompiled
    #   @0x0094: POP_JUMP_IF_NOT_NONE arg=200

def global_str(self):
    """
    use enum_name instead of class.enum_name
"""
    if self._name_:
        cls_name = self.__class__.__name__
        return f"{cls_name}({self._value_})"
    return self._name_
    # [WARN] 1 instructions not decompiled
    #   @0x0018: POP_JUMP_IF_NOT_NONE arg=112

def global_enum(cls, update_str = False):
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
        cls.__str__ = global_str

def _simple_enum(etype = Enum, *, boundary = None, use_args = None):
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
        if cls.__dict__.get('__doc__'):
            gnv_last_values = [name for name in ('__repr__', '__str__', '__format__', '__reduce_ex__')]
        if name in ('__dict__', '__weakref__'):
            pass
        cls.__dict__.items()
        gnv_last_values = [name for name in ('__repr__', '__str__', '__format__', '__reduce_ex__')]
        gnv_last_values = []
        # [Block @0x0572] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        member = new_member(**None, **(enum_class, value))
        value = value[0]
        setattr(cls, v_253, member)
        hashable_values.append(value)
        member_names.append(name)
        single_bits |= value
        # [Block @0x0840] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        member_list = [m._value_ for m in enum_class]
        member_list = [m._value_ for m in enum_class]
        # [Block @0x093E] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        member = new_member(**None, **(enum_class, value))
        value = value[0]
        setattr(cls, v_253, member)
        enum_class._value2member_map_.setdefault(value, member)
        # [Block @0x0C32] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        contained = None
        m = [_ for _ in enum_class]
        m = [_ for _ in enum_class]
        contained = None
        contained = [m._value_ == member._value_ for m in enum_class]
        contained = [m._value_ == member._value_ for m in enum_class]
        # [WARN] 3 instructions not decompiled
        #   @0x001E: POP_JUMP_IF_NOT_NONE arg=58
        #   @0x0072: POP_JUMP_IF_NONE arg=144
        #   @0x00C6: POP_JUMP_IF_NONE arg=210
    return convert_class
EnumCheck = __build_class__(EnumCheck, 'EnumCheck')()
CONTINUOUS = *EnumCheck
NAMED_FLAGS = *EnumCheck
UNIQUE = *EnumCheck

class verify:
    """
    Check an enumeration for various constraints. (see EnumCheck)
"""
    def __init__(self):
        v_16.checks = self

    def __call__(self, enumeration):
        checks = self.checks
        cls_name = enumeration.__name__
        if Flag:
            if issubclass(enumeration, Flag):
                enum_type = 'flag'
            elif issubclass(enumeration, Enum):
                enum_type = 'enum'
            else:
                TypeError('the \'verify\' decorator only works with Enum and Flag')
                raise
                checks
                return enumeration
                if check is UNIQUE:
                    pass
                elif check is CONTINUOUS:
                    values = (<genexpr>)(enumeration())
                    if len(values) < 2:
                        pass
                    else:
                        missing = []
                        if enum_type == 'flag':
                            pass
                        elif enum_type == 'enum':
                            pass
                        else:
                            raise Exception('verify: unknown type %r' % enum_type)
                            if missing:
                                raise 'invalid '(f"{enum_type} {cls_name}: missing values {', '.join}{(<genexpr>)(missing())}"[:256])
                elif not check is NAMED_FLAGS:
                    pass
                else:
                    member_names = enumeration._member_names_
                    m
                    enumeration
                    []
                    missing_names = []
                    missing_value = 0
                    enumeration._member_map_.items()
                    if not missing_names:
                        pass
                    elif len(missing_names) == 1:
                        alias = 'alias %s is missing' % missing_names[0]
                    else:
                        alias = f"aliases {', '.join(missing_names[:-1])} and {missing_names[-1]} are missing"
                        if _is_single_bit(missing_value):
                            value = 'value 0x%x' % missing_value
                        else:
                            value = 'combined values of 0x%x' % missing_value
                            raise ValueError(f"invalid Flag {cls_name}: {alias} {value} [use enum.show_flag_values(value) for details]")
                    if name in member_names:
                        pass
                    elif alias.value < 0:
                        pass
                    else:
                        values = list(_iter_bits_lsb(alias.value))
                        v
                        values
                        []
                        if not missed:
                            pass
                        else:
                            missing_names.append(name)
                            missed
                            missing_value |= val
                        raise
                        v not in member_values
                        if not True:
                            pass
                    raise
        elif issubclass(enumeration, Enum):
            pass
        else:
            TypeError('the \'verify\' decorator only works with Enum and Flag')
        # [Block @0x01AC] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        # [Block @0x01CC] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        # [WARN] 1 instructions not decompiled
        #   @0x003C: POP_JUMP_IF_NONE arg=112

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
    failed = []
    if checked_enum.__dict__ != simple_enum.__dict__:
        name = [key for key in set(checked_enum + v_70) if key == '__doc__' if checked_enum != v_154]
    elif failed:
        raise TypeError("""enum mismatch:
   %s""" % """
   """.join(failed))
    name = [key for key in set(checked_enum + v_70) if key == '__doc__' if checked_enum != v_154]
    method = [[] for name in member_names if checked_enum != v_154 for key in name if checked_enum != v_154]
    failed_member = []
    failed.append('missing member from simple enum: %r' % name)
    failed.append('extra member in simple enum: %r' % name)
    checked_value = checked_enum[v_248]
    simple_value = simple_member_dict[key]
    method = [[] for name in member_names if checked_enum != v_154 for key in name if checked_enum != v_154]
    simple_method = [method for method in ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__') if checked_method != simple_method]
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)
    simple_method = [method for method in ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__') if checked_method != simple_method]

def _old_convert_(etype, name, module, filter, source = None, *, boundary = None):
    """
    Create a new Enum subclass that replaces a collection of global constants
"""
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    else:
        source = module_globals
        value
        name
        source.items()
        []
        members.sort(key=lambda t: (t[1], t[0]))
        if not boundary:
            KEEP
        return cls
        raise
        filter(name)
        if not True:
            pass
