# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType, DynamicClassAttribute
__all__ = ['EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin']
Enum = None
Flag = None
EJECT = None
ReprEnum = None
class nonmember(object):
    __doc__ = """
    Protects item from becoming an Enum member during class creation.
    """
    def __init__(self, value):
        self.value = value
class member(object):
    __doc__ = """
    Forces item to become an Enum member during class creation.
    """
    def __init__(self, value):
        self.value = value
def _is_descriptor(obj):
    """
    Returns True if obj is a descriptor, False otherwise.
    """
    if hasattr(obj, '__get__') and hasattr(obj, '__set__'):
        hasattr(obj, '__delete__')
    # orphan @0x001C
    return
def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    if (len(name) > 4) and not name[-2:] == name[-2:]:
        pass
    # orphan @0x002E
    # orphan @0x0032
    # orphan @0x0034
    name[2] != '_'
    # orphan @0x0040
    name[-3] != '_'
    # orphan @0x004A
    return
def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
    """
    if (len(name) > 2) and not name[-1] == name[-1]:
        pass
    # orphan @0x0026
    # orphan @0x002A
    # orphan @0x002C
    name[1] != '_'
    # orphan @0x0038
    name[-2] != '_'
    # orphan @0x0042
    return
def _is_internal_class(cls_name, obj):
    # orphan @0x000E
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    qualname == s_pattern
    if not isinstance(obj, type):
        return False
    # orphan @0x003E
    qualname.endswith(e_pattern)
    # orphan @0x0046
    return
def _is_private(cls_name, name):
    pattern = '_%s__' % (cls_name)
    pat_len = len(pattern)
    if (len(name) > pat_len) and name.startswith(pattern) and (name[-1] != '_'):
        if name[-2] != '_':
            return True
    # orphan @0x0044
    return False
def _is_single_bit(num):
    """
    True if only one bit set in num (should be an int)
    """
    if num == 0:
        return False
    # orphan @0x000C
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
    # orphan @0x0024
    setattr(obj, '__reduce_ex__', _break_on_call_reduce)
    setattr(obj, '__module__', '<unknown>')
def _iter_bits_lsb(num):
    # orphan @0x0014
    num < 0
    original = num
    if isinstance(num, Enum):
        num = num.value
    # orphan @0x001C
    # orphan @0x0028
    num
    # orphan @0x002C
    b = num & ~num + 1
    yield b
    num ^= b
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
    if num >= 0:
        s = bltns.bin(num + ceiling).replace('1', '0', 1)
    # orphan @0x0036
    s = bltns.bin(~num ^ ceiling - 1 + ceiling)
    # orphan @0x004E
    sign = s[None:3]
    digits = s[3:]
    max_bits is not None
    # orphan @0x006E
    len(digits) < max_bits
    # orphan @0x007A
    digits = sign[-1] * max_bits + digits[-max_bits:]
    # orphan @0x0094
    return '%s %s' % (sign, digits)
class _not_given:
    def __repr__(self):
        return '<not given>'
_not_given = _not_given()
class _auto_null:
    def __repr__(self):
        return '_auto_null'
_auto_null = _auto_null()
class auto:
    __doc__ = """
    Instances are replaced with an appropriate value in Enum class suites.
    """
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'auto(%r)' % self.value
class property(DynamicClassAttribute):
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
    def __get__(self, instance, ownerclass):
        # orphan @0x0018
        if (instance is None) and (self.member is not None):
            return self.member
        elif self.fget is not None:
            return self.fget(instance)
        # orphan @0x003E
        self._attr_type == 'attr'
        # orphan @0x0048
        return getattr(self._cls_type, self.name)
        # orphan @0x0056
        self._attr_type == 'desc'
        # orphan @0x0060
        return getattr(instance._value_, self.name)
        # orphan @0x006E
        return
        # orphan @0x0086
        # orphan @0x00A0
        # orphan @0x00A4
    def __set__(self, instance, value):
        if self.fset is not None:
            return self.fset(instance, value)
        # orphan @0x0016
    def __delete__(self, instance):
        if self.fdel is not None:
            return self.fdel(instance)
        # orphan @0x0014
    def __set_name__(self, ownerclass, name):
        self.name = name
        self.clsname = ownerclass.__name__
class _proto_member:
    __doc__ = """
    intermediate step for enum members between class execution and final creation
    """
    def __init__(self, value):
        self.value = value
    def __set_name__(self, enum_class, member_name):
        """
        convert each quasi-member into an instance of the new enum class
        """
        # orphan @0x0048
        enum_member = enum_class._new_member_(enum_class, **args)
        # orphan @0x0036
        enum_class._use_args_
        # orphan @0x0030
        args = (args)
        # orphan @0x0026
        enum_class._member_type_ is tuple
        # orphan @0x0022
        args = value
        delattr(enum_class, member_name)
        value = self.value
        if not isinstance(value, tuple):
            args = (value)
        enum_member = enum_class._new_member_(enum_class)
        if hasattr(enum_member, '_value_'):
            enum_class._singles_mask_ | value._singles_mask_ = enum_class
        try:
            pass
        except Exception:
            pass
        value = enum_member._value_
        enum_member._name_ = member_name
        enum_member.__objclass__ = enum_class
        enum_member._sort_order_ = len(enum_class._member_names_)
        if (Flag is not None) and issubclass(enum_class, Flag) and isinstance(value, int):
            enum_class._flag_mask_ | value._flag_mask_ = enum_class
            if _is_single_bit(value):
                pass
        exc = None
        enum_member._value_ = value
        # orphan @0x012A
        enum_class._all_bits_ = 2 ** enum_class._flag_mask_.bit_length() - 1
        # orphan @0x013E
        enum_member = enum_class._value2member_map_[value]
        # orphan @0x0150
        # orphan @0x015A
        enum_class._member_map_.items()
        # orphan @0x016A
        # orphan @0x016C
        canonical_member._value_ == value
        # orphan @0x017E
        enum_member = canonical_member
        # orphan @0x018C
        # orphan @0x0190
        # orphan @0x0194
        # orphan @0x0196
        # orphan @0x019A
        # orphan @0x01A4
        Flag is None
        # orphan @0x01B4
        issubclass(enum_class, Flag)
        # orphan @0x01C0
        enum_class._member_names_.append(member_name)
        # orphan @0x01CE
        Flag is not None
        # orphan @0x01D8
        issubclass(enum_class, Flag)
        # orphan @0x01E4
        isinstance(value, int)
        # orphan @0x01F0
        _is_single_bit(value)
        # orphan @0x01FA
        enum_class._member_names_.append(member_name)
        # orphan @0x0206
        # orphan @0x020A
        # orphan @0x020C
        enum_class._add_member_(member_name, enum_member)
        enum_class._value2member_map_.setdefault(value, enum_member)
        value not in enum_class._hashable_values_
        # orphan @0x0234
        enum_class._hashable_values_.append(value)
        # orphan @0x0240
        # orphan @0x0244
        # orphan @0x024E
        enum_class._unhashable_values_.append(value)
        enum_class._unhashable_values_map_.setdefault(member_name, []).append(value)
        # orphan @0x0278
class EnumDict(dict):
    __doc__ = """
    Track enum member order and ensure member names are not reused.

    EnumType will use the names found in self._member_names as the
    enumeration member names.
    """
    def __init__(self, cls_name):
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
        # orphan @0x00E4
        key = '_order_'
        # orphan @0x00DC
        key == '__order__'
        # orphan @0x00D4
        _is_dunder(key)
        # orphan @0x00D2
        # orphan @0x00C2
        # orphan @0x00A6
        self._ignore = value
        already = set(value) & set(self._member_names)
        already
        # orphan @0x009E
        value = list(value)
        # orphan @0x008C
        value = value.replace(',', ' ').split()
        # orphan @0x0082
        isinstance(value, str)
        # orphan @0x007A
        key == '_ignore_'
        # orphan @0x006A
        setattr(self, '_generate_next_value', _gnv)
        # orphan @0x0068
        value
        # orphan @0x0062
        value.__func__
        # orphan @0x0058
        isinstance(value, staticmethod)
        # orphan @0x0050
        # orphan @0x004A
        self._auto_called
        # orphan @0x0042
        key == '_generate_next_value_'
        # orphan @0x0034
        # orphan @0x002A
        key.startswith('_repr_')
        # orphan @0x0022
        key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_')
        # orphan @0x001A
        _is_sunder(key)
        if (self._cls_name is not None) and _is_private(self._cls_name, key):
            pass
        # orphan @0x00E8
        # orphan @0x00EC
        key in self._member_names
        # orphan @0x00F8
        # orphan @0x010E
        # orphan @0x0110
        key in self._ignore
        # orphan @0x011E
        # orphan @0x0120
        isinstance(value, nonmember)
        # orphan @0x012C
        value = value.value
        # orphan @0x0136
        _is_descriptor(value)
        # orphan @0x0142
        # orphan @0x0144
        self._cls_name is not None
        # orphan @0x0150
        _is_internal_class(self._cls_name, value)
        # orphan @0x0160
        # orphan @0x0162
        key in self
        # orphan @0x016C
        # orphan @0x0180
        # orphan @0x0182
        isinstance(value, member)
        # orphan @0x018E
        value = value.value
        # orphan @0x0194
        non_auto_store = True
        single = False
        isinstance(value, auto)
        # orphan @0x01A8
        single = True
        value = (value)
        # orphan @0x01B2
        isinstance(value, tuple)
        # orphan @0x01BE
        any(EnumDict.__setitem__.<locals>.<genexpr>(value))
        # orphan @0x01D2
        auto_valued = []
        t = type(value)
        value
        # orphan @0x01E2
        # orphan @0x01E4
        isinstance(v, auto)
        # orphan @0x01F2
        non_auto_store = False
        v.value == _auto_null
        # orphan @0x0202
        v.value = self._generate_next_value(key, 1, len(self._member_names), self._last_values[None:])
        self._auto_called = True
        # orphan @0x022A
        v = v.value
        self._last_values.append(v)
        # orphan @0x023C
        auto_valued.append(v)
        # orphan @0x024A
        single
        # orphan @0x0250
        value = auto_valued[0]
        # orphan @0x025A
        value = t(auto_valued)
        # orphan @0x0268
        # orphan @0x0272
        # orphan @0x0284
        # orphan @0x0286
        non_auto_store
        key
        self._member_names
        None
        # orphan @0x0296
        self._last_values.append(value)
        # orphan @0x02A2
        super().__setitem__(key, value)
    @property
    def member_names(self):
        return list(self._member_names)
    def update(self, members):
        # orphan @0x001C
        try:
            for name in members.keys():
                pass
        except AttributeError:
            pass
        more_members.items()
        for (name, value) in more_members.items():
            pass
_EnumDict = EnumDict
class EnumType(type):
    __doc__ = """
    Metaclass for Enum
    """
    @classmethod
    def __prepare__(metacls, cls, bases):
        metacls._check_for_existing_members_(cls, bases)
        enum_dict = EnumDict(cls)
        (member_type, first_enum) = metacls._get_mixins_(cls, bases)
        if first_enum is not None:
            '_generate_next_value_'
            enum_dict
            getattr(first_enum, '_generate_next_value_', None)
        # orphan @0x003C
        return enum_dict
    def __new__(metacls, cls, bases, classdict):
        # orphan @0x01CE
        p = classdict[n]
        isinstance(p.value, int)
        # orphan @0x01CC
        # orphan @0x01C0
        bits = 0
        inverted = []
        member_names
        # orphan @0x01B0
        issubclass(bases[-1], Flag)
        # orphan @0x01AA
        bases
        # orphan @0x017A
        Flag is not None
        '_inverted_'
        classdict
        None
        '_all_bits_'
        classdict
        0
        '_singles_mask_'
        classdict
        0
        '_flag_mask_'
        classdict
        0
        '_boundary_'
        classdict
        # orphan @0x0170
        getattr(first_enum, '_boundary_', None)
        # orphan @0x0122
        boundary
        '_value_repr_'
        classdict
        metacls._find_data_repr_(cls, bases)
        '_member_type_'
        classdict
        member_type
        '_unhashable_values_map_'
        classdict
        {}
        '_unhashable_values_'
        classdict
        []
        '_hashable_values_'
        classdict
        []
        '_value2member_map_'
        classdict
        {}
        '_member_map_'
        classdict
        {}
        '_member_names_'
        classdict
        []
        # orphan @0x0108
        value = classdict[name]
        name
        classdict
        _proto_member(value)
        # orphan @0x0106
        # orphan @0x00CE
        (member_type, first_enum) = metacls._get_mixins_(cls, bases)
        (__new__, save_new, use_args) = metacls._find_new_(classdict, member_type, first_enum)
        member_names
        '_use_args_'
        classdict
        use_args
        '_new_member_'
        classdict
        __new__
        # orphan @0x00C6
        '_generate_next_value_'
        classdict
        _gnv
        # orphan @0x00B2
        classdict = dict(classdict.items())
        _gnv is not None
        # orphan @0x00AA
        _gnv = staticmethod(_gnv)
        # orphan @0x009E
        type(_gnv) is not staticmethod
        # orphan @0x0080
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        _gnv is not None
        # orphan @0x0064
        # orphan @0x004A
        member_names = classdict._member_names
        invalid_names = set(member_names) & {'mro', ''}
        invalid_names
        # orphan @0x003A
        classdict.pop(key, None)
        # orphan @0x0038
        # orphan @0x001A
        classdict.setdefault('_ignore_', []).append('_ignore_')
        ignore = classdict['_ignore_']
        ignore
        if _simple:
            return super().__new__(metacls, cls, bases, classdict, **kwds)
        # orphan @0x01E6
        p.value < 0
        # orphan @0x01F2
        inverted.append(p)
        # orphan @0x01FE
        bits |= p.value
        # orphan @0x0208
        # orphan @0x020A
        p.value is None
        # orphan @0x0216
        # orphan @0x0218
        isinstance(p.value, tuple)
        # orphan @0x0226
        p.value
        # orphan @0x022E
        isinstance(p.value[0], int)
        # orphan @0x0240
        p.value[0] < 0
        # orphan @0x0250
        inverted.append(p)
        # orphan @0x025C
        bits |= p.value[0]
        # orphan @0x026A
        # orphan @0x026E
        inverted
        # orphan @0x0272
        # orphan @0x0274
        isinstance(p.value, int)
        # orphan @0x0284
        p.value = bits & p.value
        # orphan @0x0292
        p.value = (bits & p.value[0]) + p.value[1:]
        # orphan @0x02B2
        # orphan @0x02B6
        '_%s__in_progress' % cls(delattr, '_%s__in_progress' % cls)
        yield from False
        enum_class
        super().__new__(metacls, cls, bases, classdict, **kwds)
        '_%s__in_progress' % cls
        classdict
        True
        # orphan @0x02F8
        # orphan @0x0302
        hasattr(e, '__notes__')
        # orphan @0x0316
        e
        # orphan @0x031A
        # orphan @0x031C
        # orphan @0x0320
        def <genexpr>(.0):
            .0
            for n in .0:
                yield repr(n)
                break
        # orphan @0x032C
        # orphan @0x032E
        ReprEnum is not None
        # orphan @0x0344
        ReprEnum in bases
        # orphan @0x034E
        member_type is object
        # orphan @0x0358
        # orphan @0x0360
        '__format__' not in classdict
        # orphan @0x036A
        '__format__'
        classdict
        # orphan @0x037C
        '__str__' not in classdict
        # orphan @0x0386
        method = member_type.__str__
        method is object.__str__
        # orphan @0x0398
        method = member_type.__repr__
        # orphan @0x039E
        '__str__'
        classdict
        # orphan @0x03AE
        ('__repr__', '__str__', '__format__', '__reduce_ex__')
        # orphan @0x03B2
        # orphan @0x03B4
        name not in classdict
        # orphan @0x03C0
        enum_method = getattr(first_enum, name)
        object_method = getattr(object, name)
        data_type_method = getattr(member_type, name)
        found_method in (data_type_method, object_method)
        # orphan @0x03F6
        # orphan @0x0406
        Flag is not None
        # orphan @0x0410
        # orphan @0x041C
        ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__')
        # orphan @0x0420
        # orphan @0x0422
        name not in classdict
        # orphan @0x042E
        enum_method = getattr(Flag, name)
        name
        classdict
        enum_method
        # orphan @0x0450
        Enum is not None
        # orphan @0x045A
        save_new
        # orphan @0x0460
        # orphan @0x0466
        # orphan @0x046E
        _order_ is not None
        # orphan @0x0478
        isinstance(_order_, str)
        # orphan @0x0484
        _order_ = _order_.replace(',', ' ').split()
        # orphan @0x0494
        Flag is None
        # orphan @0x049E
        cls != 'Flag'
        # orphan @0x04A8
        Flag is not None
        # orphan @0x04B2
        # orphan @0x04BE
        # orphan @0x04F2
        Flag is not None
        # orphan @0x04FC
        # orphan @0x0508
        member_list != sorted(member_list)
        # orphan @0x0524
        # orphan @0x052C
        _order_
        # orphan @0x0532
        _order_ = EnumType.__new__.<locals>.<listcomp>(_order_)
        ()
        # orphan @0x0544
        _order_
        # orphan @0x054A
        _order_ = EnumType.__new__.<locals>.<listcomp>(_order_)
        () != _order_._member_names_
        # orphan @0x0568
        # orphan @0x057A
        return
    def __bool__(cls):
        """
        classes/types should always be True.
        """
        return True
    def __call__(cls, value, names):
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
        # orphan @0x001A
        return cls.__new__(cls, value)
        if cls._member_map_ and (names is not _not_given):
            value = (value, names) + values
        # orphan @0x0026
        names is _not_given
        # orphan @0x002E
        type is None
        # orphan @0x0036
        # orphan @0x0044
        names is _not_given
        value
        cls._create_
        # orphan @0x0052
        None
        # orphan @0x0056
        names
        # orphan @0x0058
        return
    def __contains__(cls, value):
        """Return True if `value` is in `cls`.

        `value` is in `cls` if:
        1) `value` is a member of `cls`, or
        2) `value` is the value of one of the `cls`'s members.
        3) `value` is a pseudo-member (flags)
        """
        # orphan @0x000E
        issubclass(cls, Flag)
        if isinstance(value, cls):
            return True
        try:
            result = cls._missing_(value)
        except ValueError:
            pass
        return
        return
        if value in cls._unhashable_values_:
            value in cls._hashable_values_
        # orphan @0x0056
        return
    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError('%r cannot delete member %r.' % (cls.__name__, attr))
        # orphan @0x001C
        super().__delattr__(attr)
    def __dir__(cls):
        # orphan @0x0020
        interesting = set(['__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_'] + members)
        cls._new_member_ is not object.__new__
        # orphan @0x001A
        members = cls._member_names_
        if issubclass(cls, Flag):
            members = list(cls._member_map_.keys())
        # orphan @0x0050
        interesting.add('__new__')
        # orphan @0x005A
        cls.__init_subclass__ is not object.__init_subclass__
        # orphan @0x0066
        interesting.add('__init_subclass__')
        # orphan @0x0070
        cls._member_type_ is object
        # orphan @0x007A
        return sorted(interesting)
        # orphan @0x0082
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
        return ()(EnumType.__iter__.<locals>.<genexpr>._member_names_)
    def __len__(cls):
        """
        Return the number of members (no aliases)
        """
        return len(cls._member_names_)
    @bltns.property
    def __members__(cls):
        """
        Returns a mapping of member name->value.

        This mapping lists all enum members, including aliases.  Note that
        this is a read-only view of the internal mapping.
        """
        return MappingProxyType(cls._member_map_)
    def __repr__(cls):
        if (Flag is not None) and issubclass(cls, Flag):
            return '<flag %r>' % cls.__name__
        # orphan @0x001C
        return '<enum %r>' % cls.__name__
    def __reversed__(cls):
        """
        Return members in reverse definition order.
        """
        return ()(EnumType.__reversed__.<locals>.<genexpr>(reversed._member_names_))
    def __setattr__(cls, name, value):
        """
        Block attempts to reassign Enum members.

        A simple assignment to the class namespace only changes one of the
        several possible ways to get an Enum member from the Enum class,
        resulting in an inconsistent Enumeration.
        """
        member_map = cls.__dict__.get('_member_map_', {})
        if name in member_map:
            raise AttributeError('cannot reassign member %r' % (name))
        # orphan @0x0024
        super().__setattr__(name, value)
    def _create_(cls, class_name, names):
        """
        Convenience method to create a new Enum class.

        `names` can be:

        * A string containing member names, separated either with spaces or
          commas.  Values are incremented by 1 from `start`.
        * An iterable of member names.  Values are incremented by 1 from `start`.
        * An iterable of (member name, value) pairs.
        * A mapping of member name -> value pairs.
        """
        # orphan @0x008A
        value = first_enum._generate_next_value_(name, start, count, last_values[None:])
        last_values.append(value)
        names.append((name, value))
        # orphan @0x0088
        # orphan @0x0072
        original_names = []
        names = names
        last_values = []
        enumerate(original_names)
        # orphan @0x0064
        isinstance(names[0], str)
        # orphan @0x0060
        names
        # orphan @0x0052
        isinstance(names, (tuple, list))
        # orphan @0x0042
        names = names.replace(',', ' ').split()
        # orphan @0x001A
        (_, first_enum) = cls._get_mixins_(class_name, bases)
        classdict = metacls.__prepare__(class_name, bases)
        isinstance(names, str)
        # orphan @0x0014
        (type, cls)
        metacls = cls.__class__
        if type is None:
            pass
        # orphan @0x00C2
        names is None
        # orphan @0x00CA
        names = []
        # orphan @0x00CE
        names
        # orphan @0x00D2
        # orphan @0x00D4
        isinstance(item, str)
        # orphan @0x00E0
        member_name = names[item]
        member_value = item
        # orphan @0x00F0
        (member_name, member_value) = item
        # orphan @0x00F8
        member_name
        classdict
        member_value
        # orphan @0x0102
        module is None
        # orphan @0x010C
        module = sys._getframemodulename(2)
        # orphan @0x011C
        # orphan @0x0126
        module = sys._getframe(2).f_globals['__name__']
        # orphan @0x0142
        # orphan @0x0152
        # orphan @0x015C
        # orphan @0x015E
        # orphan @0x0162
        # orphan @0x0164
        module is None
        # orphan @0x016E
        _make_class_unpicklable(classdict)
        # orphan @0x0178
        '__module__'
        classdict
        module
        # orphan @0x0180
        qualname is not None
        # orphan @0x018A
        '__qualname__'
        classdict
        qualname
        # orphan @0x0192
        return metacls.__new__(metacls, class_name, bases, classdict, boundary=boundary)
    def _convert_(cls, name, module, filter, source):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        # orphan @0x001C
        members = EnumType._convert_.<locals>.<listcomp>(source.items())
        members.sort(key=EnumType._convert_.<locals>.<lambda>)
        # orphan @0x0018
        source = module_globals
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        # orphan @0x0048
        # orphan @0x0050
        members.sort(key=EnumType._convert_.<locals>.<lambda>)
        # orphan @0x006A
        # orphan @0x006C
        body = EnumType._convert_.<locals>.<dictcomp>(members)
        tmp_cls = type(name, (object), body)
        boundary
        cls
        _simple_enum
        '__module__'
        body
        module
        # orphan @0x0098
        KEEP
        # orphan @0x009A
        as_global
        # orphan @0x00A8
        global_enum(cls)
        # orphan @0x00B2
        sys.modules[cls.__module__].__dict__.update(cls.__members__)
        # orphan @0x00C8
        return cls
    @classmethod
    def _check_for_existing_members_(mcls, class_name, bases):
        bases
        for chain in bases:
            for base in chain.__mro__:
                if isinstance(base, EnumType) and base._member_names_:
                    raise TypeError('<enum %r> cannot extend %r' % (class_name, base))
    @classmethod
    def _get_mixins_(mcls, class_name, bases):
        """
        Returns the type for creating enum members, and the first inherited
        enum class.

        bases: the tuple of bases that was given to __new__
        """
        # orphan @0x000C
        first_enum = bases[-1]
        isinstance(first_enum, EnumType)
        if not bases:
            return (object, Enum)
        # orphan @0x001E
        # orphan @0x0026
        mcls._find_data_type_(class_name, bases)
        # orphan @0x0032
        object
        # orphan @0x0034
        return (member_type, first_enum)
    @classmethod
    def _find_data_repr_(mcls, class_name, bases):
        bases
        for chain in bases:
            for base in chain.__mro__:
                if base is object:
                    continue
                if isinstance(base, EnumType):
                    base._value_repr_
                    break
                if ('__repr__' in base.__dict__) and ('__dataclass_fields__' in base.__dict__) and ('__dataclass_params__' in base.__dict__) and base.__dict__['__dataclass_params__'].repr:
                    _dataclass_repr
                    break
                base.__dict__['__repr__']
                break
    @classmethod
    def _find_data_type_(mcls, class_name, bases):
        data_types = set()
        base_chain = set()
        bases
        for chain in bases:
            for base in chain.__mro__:
                base_chain.add(base)
                if base is object:
                    continue
                if isinstance(base, EnumType) and (base._member_type_ is not object):
                    data_types.add(base._member_type_)
                    break
                if '__new__' in base.__dict__:
                    if ('__dataclass_fields__' in base.__dict__) and candidate:
                        base
                break
                if candidate:
                    base
        if len(data_types) > 1:
            raise TypeError('too many data types for %r: %r' % (class_name, data_types))
        # orphan @0x00AE
        # orphan @0x00B0
        data_types
        # orphan @0x00B4
        return data_types.pop()
    @classmethod
    def _find_new_(mcls, classdict, member_type, first_enum):
        """
        Returns the __new__ to be used for creating the enum members.

        classdict: the class dictionary given to __new__
        member_type: the data type whose __new__ will be used by default
        first_enum: enumeration to check for an overriding __new__
        """
        # orphan @0x0034
        # orphan @0x002A
        (member_type, first_enum)
        # orphan @0x0028
        # orphan @0x0024
        ('__new_member__', '__new__')
        # orphan @0x001A
        __new__ is None
        __new__ = classdict.get('__new__', None)
        if not first_enum is not None:
            __new__ is not None
        # orphan @0x0036
        target = getattr(possible, method, None)
        target not in {None, None.__new__, object.__new__, Enum.__new__}
        # orphan @0x005A
        __new__ = target
        # orphan @0x0064
        __new__ is not None
        # orphan @0x006C
        # orphan @0x0072
        __new__ = object.__new__
        # orphan @0x0078
        first_enum is None
        # orphan @0x0080
        __new__ in (Enum.__new__, object.__new__)
        # orphan @0x0090
        use_args = False
        # orphan @0x0096
        use_args = True
        # orphan @0x009A
        return (__new__, save_new, use_args)
    def _add_member_(cls, name, member):
        # orphan @0x0072
        found_descriptor = attr
        class_type = base
        descriptor_type = 'enum'
        # orphan @0x0064
        isinstance(attr, (property, DynamicClassAttribute))
        # orphan @0x004E
        attr = base.__dict__.get(name)
        attr is not None
        # orphan @0x004C
        # orphan @0x0032
        found_descriptor = None
        descriptor_type = None
        class_type = None
        cls.__mro__[1:]
        if (name in cls._member_map_) and (cls._member_map_[name] is not member):
            raise NameError('%r is already bound: %r' % (name, cls._member_map_[name]))
        # orphan @0x0084
        _is_descriptor(attr)
        # orphan @0x008C
        found_descriptor = attr
        descriptor_type
        # orphan @0x0094
        'desc'
        # orphan @0x0096
        class_type
        # orphan @0x009C
        base
        # orphan @0x009E
        # orphan @0x00A4
        descriptor_type = 'attr'
        class_type = base
        # orphan @0x00AE
        found_descriptor
        # orphan @0x00B4
        redirect = property()
        redirect.member = member
        redirect.__set_name__(cls, name)
        descriptor_type in ('enum', 'desc')
        # orphan @0x00D6
        redirect.fget = getattr(found_descriptor, 'fget', None)
        redirect._get = getattr(found_descriptor, '__get__', None)
        redirect.fset = getattr(found_descriptor, 'fset', None)
        redirect._set = getattr(found_descriptor, '__set__', None)
        redirect.fdel = getattr(found_descriptor, 'fdel', None)
        redirect._del = getattr(found_descriptor, '__delete__', None)
        # orphan @0x012A
        redirect._attr_type = descriptor_type
        redirect._cls_type = class_type
        setattr(cls, name, redirect)
        # orphan @0x0144
        setattr(cls, name, member)
    @property
    def __signature__(cls):
        # orphan @0x0028
        return Signature([Parameter('new_class_name', Parameter.POSITIONAL_ONLY), Parameter('names', Parameter.POSITIONAL_OR_KEYWORD), Parameter('module', Parameter.KEYWORD_ONLY, default=None), Parameter('qualname', Parameter.KEYWORD_ONLY, default=None), Parameter('type', Parameter.KEYWORD_ONLY, default=None), Parameter('start', Parameter.KEYWORD_ONLY, default=1), Parameter('boundary', Parameter.KEYWORD_ONLY, default=None)])
        from inspect import Parameter, Signature
        if cls._member_names_:
            return Signature([Parameter('values', Parameter.VAR_POSITIONAL)])
EnumMeta = EnumType
class Enum:
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
        # orphan @0x0086
        cls[name]
        return
        # orphan @0x0076
        value == member._value_
        # orphan @0x0074
        # orphan @0x006A
        cls._member_map_.items()
        # orphan @0x0058
        cls[name]
        return
        # orphan @0x004A
        value in unhashable_values
        # orphan @0x0048
        # orphan @0x0038
        cls._unhashable_values_map_.items()
        # orphan @0x0030
        # orphan @0x0026
        # orphan @0x0010
        return
        if type(value) is cls:
            return value
        # orphan @0x0098
        # orphan @0x009C
        # orphan @0x009E
        cls._member_map_
        # orphan @0x00A4
        getattr(cls, '_%s__in_progress' % cls.__name__, False)
        # orphan @0x00B6
        # orphan @0x00C0
        # orphan @0x00CC
        exc = None
        result = cls._missing_(value)
        # orphan @0x00E0
        # orphan @0x00EA
        exc = e
        result = None
        # orphan @0x00FE
        e = None
        # orphan @0x010A
        # orphan @0x010C
        isinstance(result, cls)
        # orphan @0x011A
        return
        # orphan @0x0122
        Flag is not None
        # orphan @0x012C
        issubclass(cls, Flag)
        # orphan @0x0138
        cls._boundary_ is EJECT
        # orphan @0x0144
        isinstance(result, int)
        # orphan @0x0150
        return
        # orphan @0x0158
        ve_exc = ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        result is None
        # orphan @0x0174
        exc is None
        # orphan @0x017E
        # orphan @0x0182
        # orphan @0x0184
        exc is None
        # orphan @0x018E
        exc = TypeError('error in %s._missing_: returned %r instead of None or a valid member' % (cls.__name__, result))
        # orphan @0x01A0
        isinstance(exc, ValueError)
        # orphan @0x01AC
        exc.__context__ = ve_exc
        # orphan @0x01B2
        # orphan @0x01B6
        # orphan @0x01BA
        exc = None
        ve_exc = None
    def _add_alias_(self, name):
        self.__class__._add_member_(name, self)
    def _add_value_alias_(self, value):
        cls = self.__class__
        try:
            if value in cls._value2member_map_:
                if cls._value2member_map_[value] is not self:
                    raise ValueError('%r is already bound: %r' % (value, cls._value2member_map_[value]))
        except TypeError:
            pass
        try:
            cls._value2member_map_.setdefault(value, self)
            cls._hashable_values_.append(value)
        except TypeError:
            pass
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_values: the list of values assigned
        """
        # orphan @0x0022
        # orphan @0x001A
        # orphan @0x0008
        last_value = sorted(last_values).pop()
        if not last_values:
            return start
        # orphan @0x0032
        # orphan @0x0036
        # orphan @0x0038
        return
        # orphan @0x004C
        # orphan @0x0062
        # orphan @0x0066
    @classmethod
    def _missing_(cls, value):
        pass
    def __repr__(self):
        # orphan @0x000A
        return '<%s.%s: %s>' % (self.__class__.__name__, self._name_, v_repr(self._value_))
        if self.__class__._value_repr_:
            repr
    def __str__(self):
        return '%s.%s' % (self.__class__.__name__, self._name_)
    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        # orphan @0x0048
        interesting.add(name)
        # orphan @0x003E
        name not in self._member_map_
        # orphan @0x0030
        name[0] != '_'
        # orphan @0x002E
        # orphan @0x0022
        getattr(self, '__dict__', [])
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
        # orphan @0x0054
        self.__class__.mro()
        # orphan @0x005E
        # orphan @0x0060
        cls.__dict__.items()
        # orphan @0x006C
        # orphan @0x006E
        name[0] == '_'
        # orphan @0x0080
        # orphan @0x0082
        isinstance(obj, property)
        # orphan @0x008C
        obj.fget is not None
        # orphan @0x0096
        name not in self._member_map_
        # orphan @0x00A0
        interesting.add(name)
        # orphan @0x00AC
        interesting.discard(name)
        # orphan @0x00B8
        name not in self._member_map_
        # orphan @0x00C2
        interesting.add(name)
        # orphan @0x00CC
        # orphan @0x00CE
        # orphan @0x00D0
        names = sorted(set(['__class__', '__doc__', '__eq__', '__hash__', '__module__']) | interesting)
        return names
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
    @property
    def name(self):
        """The name of the Enum member."""
        return self._name_
    @property
    def value(self):
        """The value of the Enum member."""
        return self._value_
class ReprEnum(Enum):
    __doc__ = """
    Only changes the repr(), leaving str() and format() to the mixed-in type.
    """
class IntEnum(int, ReprEnum):
    __doc__ = """
    Enum where members are also (and must be) ints
    """
class StrEnum(str, ReprEnum):
    __doc__ = """
    Enum where members are also (and must be) strings
    """
    def __new__(cls):
        """values must already be of type `str`"""
        # orphan @0x001A
        len(values) == 1
        if len(values) > 3:
            raise TypeError('too many arguments for str(): %r' % (values))
        elif not isinstance(values[0], str):
            raise TypeError('%r is not a string' % (values[0]))
        # orphan @0x0046
        len(values) >= 2
        # orphan @0x0052
        isinstance(values[1], str)
        # orphan @0x0060
        # orphan @0x0072
        len(values) == 3
        # orphan @0x007E
        isinstance(values[2], str)
        # orphan @0x008C
        # orphan @0x009C
        member = str.__new__(cls, value)
        member._value_ = value
        return member
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Return the lower-cased version of the member name.
        """
        return name.lower()
def pickle_by_global_name(self, proto):
    return self.name
_reduce_ex_by_global_name = pickle_by_global_name
def pickle_by_enum_name(self, proto):
    return (getattr, (self.__class__, self._name_))
class FlagBoundary(StrEnum):
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
STRICT = *FlagBoundary
CONFORM = *FlagBoundary
EJECT = *FlagBoundary
KEEP = *FlagBoundary
class Flag(Enum):
    __doc__ = """
    Support for flags
    """
    _numeric_repr_ = repr
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_values: the last value assigned or None
        """
        # orphan @0x0014
        last_value = max(last_values)
        high_bit = _high_bit(last_value)
        # orphan @0x0010
        return 1
        if count:
            if start is not None:
                return start
        # orphan @0x002A
        # orphan @0x0032
        # orphan @0x0046
        # orphan @0x004A
        # orphan @0x004C
        return 2 ** (high_bit + 1)
    @classmethod
    def _iter_member_by_value_(cls, value):
        """
        Extract all members from the value in definition (i.e. increasing value) order.
        """
        _iter_bits_lsb(value & cls._flag_mask_)
        for val in _iter_bits_lsb(value & cls._flag_mask_):
            yield cls._value2member_map_.get(val)
            break
    _iter_member_ = _iter_member_by_value_
    @classmethod
    def _iter_member_by_def_(cls, value):
        """
        Extract all members from the value in definition order.
        """
        yield from sorted(cls._iter_member_by_value_(value), key=Flag._iter_member_by_def_.<locals>.<lambda>)
    @classmethod
    def _missing_(cls, value):
        """
        Create a composite member containing all canonical members present in `value`.

        If non-member values are present, result depends on `_boundary_` setting.
        """
        # orphan @0x00E6
        # orphan @0x00CA
        value = max(all_bits + 1, 2 ** value.bit_length()) + value
        # orphan @0x00C2
        value < 0
        # orphan @0x00B8
        cls._boundary_ is KEEP
        # orphan @0x00B4
        return value
        # orphan @0x00AA
        cls._boundary_ is EJECT
        # orphan @0x00A0
        value &= flag_mask
        # orphan @0x0096
        cls._boundary_ is CONFORM
        # orphan @0x0094
        # orphan @0x0062
        max_bits = max(value.bit_length(), flag_mask.bit_length())
        # orphan @0x0058
        cls._boundary_ is STRICT
        # orphan @0x004C
        value & (all_bits ^ flag_mask)
        # orphan @0x0048
        # orphan @0x0046
        # orphan @0x0040
        # orphan @0x001C
        flag_mask = cls._flag_mask_
        singles_mask = cls._singles_mask_
        all_bits = cls._all_bits_
        def <listcomp>(.0):
            .0
            []
            for m in .0:
                pass
            return
        value <= value
        ~all_bits
        if not isinstance(value, int):
            raise ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        # orphan @0x00F8
        value < 0
        # orphan @0x0102
        neg_value = value
        cls._boundary_ in (EJECT, KEEP)
        # orphan @0x0116
        value = all_bits + 1 + value
        # orphan @0x0124
        value = singles_mask & value
        # orphan @0x012C
        unknown = value & ~flag_mask
        aliases = value & ~singles_mask
        member_value = value & singles_mask
        unknown
        # orphan @0x014E
        cls._boundary_ is not KEEP
        # orphan @0x015A
        # orphan @0x0174
        cls._member_type_ is object
        # orphan @0x0180
        pseudo_member = object.__new__(cls)
        # orphan @0x018C
        pseudo_member = cls._member_type_.__new__(cls, value)
        # orphan @0x019A
        hasattr(pseudo_member, '_value_')
        # orphan @0x01A6
        pseudo_member._value_ = value
        # orphan @0x01AC
        member_value
        # orphan @0x01B2
        aliases
        # orphan @0x01B8
        members = []
        combined_value = 0
        cls._iter_member_(member_value)
        # orphan @0x01CA
        # orphan @0x01CC
        members.append(m)
        combined_value |= m._value_
        # orphan @0x01E6
        aliases
        # orphan @0x01EC
        value = member_value | aliases
        cls._member_map_.items()
        # orphan @0x01FE
        # orphan @0x0200
        pm not in members
        # orphan @0x0210
        pm._value_
        # orphan @0x0218
        pm._value_ & value == pm._value_
        # orphan @0x022A
        members.append(pm)
        combined_value |= pm._value_
        # orphan @0x0242
        unknown = value ^ combined_value
        pseudo_member._name_ = '|'.join(Flag._missing_.<locals>.<listcomp>(members))
        combined_value
        # orphan @0x0266
        pseudo_member._name_ = None
        # orphan @0x026E
        unknown
        # orphan @0x0274
        cls._boundary_ is STRICT
        # orphan @0x0280
        # orphan @0x0290
        # orphan @0x0292
        unknown
        # orphan @0x0298
        pseudo_member._name_ + '|%s' % cls._numeric_repr_(unknown)._name_ = pseudo_member
        # orphan @0x02B0
        # orphan @0x02B2
        pseudo_member._name_ = None
        # orphan @0x02B8
        pseudo_member = cls._value2member_map_.setdefault(value, pseudo_member)
        neg_value is not None
        # orphan @0x02D0
        neg_value
        cls._value2member_map_
        pseudo_member
        # orphan @0x02DA
        return pseudo_member
    def __contains__(self, other):
        """
        Returns True if self has at least the same flags set as other.
        """
        if not isinstance(other, self.__class__):
            raise TypeError('unsupported operand type(s) for \'in\': %r and %r' % (type(other).__qualname__, self.__class__.__qualname__))
        # orphan @0x0026
        return other._value_ & self._value_ == other._value_
    def __iter__(self):
        """
        Returns flags in definition order.
        """
        yield from self._iter_member_(self._value_)
    def __len__(self):
        return self._value_.bit_count()
    def __repr__(self):
        # orphan @0x0012
        self._name_ is None
        cls_name = self.__class__.__name__
        if self.__class__._value_repr_:
            repr
        # orphan @0x001E
        return '<%s: %s>' % (cls_name, v_repr(self._value_))
        # orphan @0x0030
        return '<%s.%s: %s>' % (cls_name, self._name_, v_repr(self._value_))
    def __str__(self):
        cls_name = self.__class__.__name__
        if self._name_ is None:
            return '%s(%r)' % (cls_name, self._value_)
        # orphan @0x0020
        return '%s.%s' % (cls_name, self._name_)
    def __bool__(self):
        return bool(self._value_)
    def _get_value(self, flag):
        if isinstance(flag, self.__class__):
            return flag._value_
        # orphan @0x0012
        self._member_type_ is not object
        # orphan @0x001C
        isinstance(flag, self._member_type_)
        # orphan @0x0028
        return flag
        # orphan @0x002C
        return NotImplemented
    def __or__(self, other):
        # orphan @0x0016
        value = self._value_
        value is None
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        # orphan @0x0024
        other_value is None
        # orphan @0x002C
        (self, other)
        # orphan @0x0034
        # orphan @0x0036
        self._get_value(flag) is None
        # orphan @0x0046
        # orphan @0x0056
        # orphan @0x0058
        return self.__class__(value | other_value)
    def __and__(self, other):
        # orphan @0x0016
        value = self._value_
        value is None
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        # orphan @0x0024
        other_value is None
        # orphan @0x002C
        (self, other)
        # orphan @0x0034
        # orphan @0x0036
        self._get_value(flag) is None
        # orphan @0x0046
        # orphan @0x0056
        # orphan @0x0058
        return self.__class__(value & other_value)
    def __xor__(self, other):
        # orphan @0x0016
        value = self._value_
        value is None
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        # orphan @0x0024
        other_value is None
        # orphan @0x002C
        (self, other)
        # orphan @0x0034
        # orphan @0x0036
        self._get_value(flag) is None
        # orphan @0x0046
        # orphan @0x0056
        # orphan @0x0058
        return self.__class__(value ^ other_value)
    def __invert__(self):
        # orphan @0x001E
        self._inverted_ is None
        if self._get_value(self) is None:
            raise TypeError(f"'{self}' cannot be inverted")
        # orphan @0x0028
        self._boundary_ in (EJECT, KEEP)
        # orphan @0x0036
        self._inverted_ = self.__class__(~self._value_)
        # orphan @0x0048
        self._inverted_ = self.__class__(self._singles_mask_ & ~self._value_)
        # orphan @0x005E
        return self._inverted_
    __rand__ = __and__
    __ror__ = __or__
    __rxor__ = __xor__
class IntFlag(int, ReprEnum, Flag):
    __doc__ = """
    Support for integer-based Flags
    """
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
    for (name, member) in enumeration.__members__.items():
        if name != member.name:
            duplicates.append((name, member.name))
    if duplicates:
        alias_details = ', '.join(unique.<locals>.<listcomp>(duplicates))
        raise ValueError('duplicate values found in %r: %s' % (enumeration, alias_details))
    # orphan @0x005A
    return enumeration
def _dataclass_repr(self):
    return
def global_enum_repr(self):
    """
    use module.enum_name instead of class.enum_name

    the module is the last module in case of a multi-module name
    """
    module = self.__class__.__module__.split('.')[-1]
    return '%s.%s' % (module, self._name_)
def global_flag_repr(self):
    """
    use module.flag_name instead of class.flag_name

    the module is the last module in case of a multi-module name
    """
    # orphan @0x003E
    return ('%s.%s', self._name_)
    # orphan @0x0034
    _is_single_bit(self._value_)
    cls_name = self.__class__.__name__
    if self._name_ is None:
        return ('%s.%s(%r)', cls_name, self._value_)
    return '|'.join(global_flag_repr.<locals>.<listcomp>(self.name.split('|')))
    # orphan @0x004C
    self._boundary_ is not FlagBoundary.KEEP
    # orphan @0x0078
    name = []
    self._name_.split('|')
    # orphan @0x0088
    # orphan @0x008A
    n[0].isdigit()
    # orphan @0x0098
    name.append(n)
    # orphan @0x00A4
    # orphan @0x00B8
    return '|'.join(name)
def global_str(self):
    """
    use enum_name instead of class.enum_name
    """
    if self._name_ is None:
        cls_name = self.__class__.__name__
        return '%s(%r)' % (cls_name, self._value_)
    # orphan @0x0020
    return self._name_
def global_enum(cls, update_str):
    """
    decorator that makes the repr() of an enum member reference its module
    instead of its class; also exports all members to the enum's module's
    global namespace
    """
    # orphan @0x0012
    cls.__repr__ = global_enum_repr
    if issubclass(cls, Flag):
        cls.__repr__ = global_flag_repr
    # orphan @0x0018
    issubclass(cls, ReprEnum)
    # orphan @0x0022
    update_str
    # orphan @0x0026
    cls.__str__ = global_str
    # orphan @0x002C
    sys.modules[cls.__module__].__dict__.update(cls.__members__)
    return cls
def _simple_enum(etype):
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
        # orphan @0x01EA
        found_method = getattr(enum_class, name)
        object_method = getattr(object, name)
        data_type_method = getattr(member_type, name)
        found_method in (data_type_method, object_method)
        # orphan @0x01DE
        name not in body
        # orphan @0x01DC
        # orphan @0x01C4
        ('__repr__', '__str__', '__format__', '__reduce_ex__')
        # orphan @0x01BC
        '__doc__'
        body
        'An enumeration.'
        # orphan @0x01AA
        cls.__dict__.get('__doc__') is None
        # orphan @0x01A6
        # orphan @0x019E
        name
        attrs
        obj
        # orphan @0x0194
        name
        body
        obj
        # orphan @0x018A
        _is_descriptor(obj)
        # orphan @0x0180
        _is_sunder(name)
        # orphan @0x0174
        _is_private(cls_name, name)
        # orphan @0x016A
        _is_dunder(name)
        # orphan @0x0168
        # orphan @0x0156
        name in ('__dict__', '__weakref__')
        # orphan @0x0154
        # orphan @0x014A
        cls.__dict__.items()
        # orphan @0x00DE
        '__invert__'
        body
        Flag.__invert__
        '__rand__'
        body
        Flag.__rand__
        '__rxor__'
        body
        Flag.__rxor__
        '__ror__'
        body
        Flag.__ror__
        '__and__'
        body
        Flag.__and__
        '__xor__'
        body
        Flag.__xor__
        '__or__'
        body
        Flag.__or__
        '_inverted_'
        body
        None
        '_singles_mask_'
        body
        None
        '_all_bits_'
        body
        None
        '_flag_mask_'
        body
        None
        '_boundary_'
        body
        # orphan @0x00DA
        # orphan @0x00D6
        # orphan @0x0050
        gnv = '_generate_next_value_'
        member_names = '_member_names_'
        member_map = '_member_map_'
        value2member_map = '_value2member_map_'
        hashable_values = '_hashable_values_'
        unhashable_values = '_unhashable_values_'
        member_type = '_member_type_'
        '_value_repr_'(issubclass, Flag)
        body
        body._value_repr_
        '_unhashable_values_map_'._member_type_
        '_unhashable_values_map_'._member_type_
        body
        {}
        body
        []
        []
        body
        []
        []
        body
        {}
        {}
        body
        {}
        {}
        body
        []
        []
        body
        '_use_args_'._generate_next_value_
        '_use_args_'._generate_next_value_
        body
        '_new_member_'
        body
        new_member
        # orphan @0x0048
        '__new_member__'
        body
        new_member
        # orphan @0x0038
        attrs = {}
        body = {}
        __new__ is not None
        # orphan @0x0030
        # orphan @0x0028
        new_member = __new__.__func__
        # orphan @0x0014
        __new__ = cls.__dict__.get('__new__')
        __new__ is not None
        cls_name = cls.__name__
        use_args
        # orphan @0x0220
        setattr(enum_class, name, enum_method)
        # orphan @0x0230
        gnv_last_values = []
        issubclass(enum_class, Flag)
        # orphan @0x0240
        single_bits = 0
        multi_bits = 0
        attrs.items()
        # orphan @0x0250
        # orphan @0x0254
        isinstance(value, auto)
        # orphan @0x0266
        auto.value is _auto_null
        # orphan @0x0272
        value = gnv(name, 1, len(member_names), gnv_last_values)
        # orphan @0x0284
        # orphan @0x028A
        isinstance(value, tuple)
        # orphan @0x0296
        value = (value)
        # orphan @0x029C
        member = new_member(enum_class, **value)
        value = value[0]
        # orphan @0x02B4
        member = new_member(enum_class)
        # orphan @0x02BC
        __new__ is None
        # orphan @0x02C6
        member._value_ = value
        # orphan @0x02CC
        contained = value2member_map.get(member._value_)
        # orphan @0x02DE
        # orphan @0x02E8
        def <listcomp>(.0):
            .0
            []
            for m in .0:
                pass
            return
        member._value_ in unhashable_values
        # orphan @0x02FE
        member.value in hashable_values
        # orphan @0x030A
        enum_class
        # orphan @0x030E
        # orphan @0x0310
        m._value_ == member._value_
        # orphan @0x0320
        contained = m
        # orphan @0x032E
        # orphan @0x0332
        # orphan @0x0334
        contained is not None
        # orphan @0x033E
        contained._add_alias_(name)
        # orphan @0x034A
        member._name_ = name
        member.__objclass__ = enum_class
        member.__init__(value)
        member._sort_order_ = len(member_names)
        name not in ('name', 'value')
        # orphan @0x0374
        setattr(enum_class, name, member)
        name
        member_map
        member
        # orphan @0x038A
        enum_class._add_member_(name, member)
        # orphan @0x0396
        hashable_values.append(value)
        _is_single_bit(value)
        value
        value2member_map
        member
        # orphan @0x03B2
        member_names.append(name)
        single_bits |= value
        # orphan @0x03C6
        multi_bits |= value
        # orphan @0x03CE
        gnv_last_values.append(value)
        # orphan @0x03D8
        # orphan @0x03DC
        enum_class._flag_mask_ = single_bits | multi_bits
        enum_class._singles_mask_ = single_bits
        enum_class._all_bits_ = 2 ** single_bits | multi_bits.bit_length() - 1
        member_list = _simple_enum.<locals>.convert_class.<locals>.<listcomp>(enum_class)
        member_list != sorted(member_list)
        # orphan @0x041E
        enum_class._iter_member_ = enum_class._iter_member_by_def_
        # orphan @0x042A
        attrs.items()
        # orphan @0x0432
        # orphan @0x0436
        isinstance(value, auto)
        # orphan @0x0448
        value.value is _auto_null
        # orphan @0x0454
        value.value = gnv(name, 1, len(member_names), gnv_last_values)
        # orphan @0x0468
        value = value.value
        # orphan @0x046E
        # orphan @0x0474
        isinstance(value, tuple)
        # orphan @0x0480
        value = (value)
        # orphan @0x0486
        member = new_member(enum_class, **value)
        value = value[0]
        # orphan @0x049E
        member = new_member(enum_class)
        # orphan @0x04A6
        __new__ is None
        # orphan @0x04B0
        member._value_ = value
        # orphan @0x04B6
        contained = value2member_map.get(member._value_)
        # orphan @0x04C8
        # orphan @0x04D2
        contained = None
        member._value_ in unhashable_values
        # orphan @0x04E8
        member._value_ in hashable_values
        # orphan @0x04F4
        enum_class
        # orphan @0x04F8
        # orphan @0x04FA
        m._value_ == member._value_
        # orphan @0x050A
        contained = m
        # orphan @0x0518
        # orphan @0x051C
        # orphan @0x051E
        contained is not None
        # orphan @0x0528
        contained._add_alias_(name)
        # orphan @0x0534
        member._name_ = name
        member.__objclass__ = enum_class
        member.__init__(value)
        member._sort_order_ = len(member_names)
        name not in ('name', 'value')
        # orphan @0x055E
        setattr(enum_class, name, member)
        name
        member_map
        member
        # orphan @0x0574
        enum_class._add_member_(name, member)
        # orphan @0x0580
        member_names.append(name)
        gnv_last_values.append(value)
        enum_class._value2member_map_.setdefault(value, member)
        value not in hashable_values
        # orphan @0x05AE
        hashable_values.append(value)
        # orphan @0x05B8
        # orphan @0x05BC
        # orphan @0x05C6
        enum_class._unhashable_values_.append(value)
        enum_class._unhashable_values_map_.setdefault(name, []).append(value)
        # orphan @0x05F0
        # orphan @0x05F2
        # orphan @0x05F6
        '__new__' in body
        # orphan @0x0600
        enum_class.__new_member__ = enum_class.__new__
        # orphan @0x0608
        enum_class.__new__ = Enum.__new__
        return enum_class
    return convert_class
EnumCheck = _simple_enum(StrEnum)(__build_class__(EnumCheck, 'EnumCheck'))
CONTINUOUS = *EnumCheck
NAMED_FLAGS = *EnumCheck
UNIQUE = *EnumCheck
class verify:
    __doc__ = """
    Check an enumeration for various constraints. (see EnumCheck)
    """
    def __init__(self):
        self.checks = checks
    def __call__(self, enumeration):
        # orphan @0x00D4
        low = max(values)
        high = min(values)
        missing = []
        enum_type == 'flag'
        # orphan @0x00D2
        # orphan @0x00B4
        values = set(verify.__call__.<locals>.<genexpr>(enumeration))
        len(values) < 2
        # orphan @0x00AA
        check is CONTINUOUS
        # orphan @0x00A8
        # orphan @0x0084
        alias_details = ', '.join(verify.__call__.<locals>.<listcomp>(duplicates))
        # orphan @0x0080
        duplicates
        # orphan @0x006E
        duplicates.append((name, member.name))
        # orphan @0x005E
        name != member.name
        # orphan @0x005C
        # orphan @0x004E
        duplicates = []
        enumeration.__members__.items()
        # orphan @0x0044
        check is UNIQUE
        # orphan @0x0040
        # orphan @0x003C
        checks
        # orphan @0x0034
        # orphan @0x002E
        enum_type = 'enum'
        # orphan @0x0024
        issubclass(enumeration, Enum)
        checks = self.checks
        cls_name = enumeration.__name__
        if (Flag is not None) and issubclass(enumeration, Flag):
            enum_type = 'flag'
        # orphan @0x00F4
        range(_high_bit(low) + 1, _high_bit(high))
        # orphan @0x010A
        # orphan @0x010C
        2 ** i not in values
        # orphan @0x011C
        missing.append(2 ** i)
        # orphan @0x012E
        # orphan @0x0130
        enum_type == 'enum'
        # orphan @0x013A
        range(low + 1, high)
        # orphan @0x0148
        # orphan @0x014A
        i not in values
        # orphan @0x0156
        missing.append(i)
        # orphan @0x0164
        # orphan @0x0166
        # orphan @0x0172
        missing
        # orphan @0x0178
        # orphan @0x01A2
        # orphan @0x01A4
        check is NAMED_FLAGS
        # orphan @0x01AC
        member_names = enumeration._member_names_
        missing_names = []
        missing_value = 0
        enumeration._member_map_.items()
        member_values
        verify.__call__.<locals>.<listcomp>(enumeration)
        # orphan @0x01D2
        # orphan @0x01D4
        name in member_names
        # orphan @0x01E6
        # orphan @0x01E8
        alias.value < 0
        # orphan @0x01F6
        # orphan @0x01F8
        values = list(_iter_bits_lsb(alias.value))
        missed = verify.__call__.<locals>.<listcomp>(values)
        missed
        ()
        # orphan @0x021E
        missing_names.append(name)
        missed
        # orphan @0x022C
        # orphan @0x022E
        missing_value |= val
        # orphan @0x023C
        # orphan @0x0240
        missing_names
        # orphan @0x0244
        len(missing_names) == 1
        # orphan @0x0252
        alias = 'alias %s is missing' % missing_names[0]
        # orphan @0x0260
        alias = 'aliases %s and %s are missing' % (', '.join(missing_names[None:-1]), missing_names[-1])
        # orphan @0x027E
        _is_single_bit(missing_value)
        # orphan @0x0288
        value = 'value 0x%x' % missing_value
        # orphan @0x0292
        value = 'combined values of 0x%x' % missing_value
        # orphan @0x029A
        # orphan @0x02AC
        # orphan @0x02AE
        return enumeration
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
        for key in set(checked_keys + simple_keys):
            if key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__'):
                continue
            if key in member_names:
                continue
            if key not in simple_keys:
                failed.append('missing key: %r' % (key))
            if key not in checked_keys:
                failed.append('extra key:   %r' % (key))
            checked_value = checked_dict[key]
            simple_value = simple_dict[key]
            if callable(checked_value):
                if isinstance(checked_value, bltns.property):
                    pass
            if key == '__doc__':
                compressed_checked_value = checked_value.replace(' ', '').replace('\t', '')
                compressed_simple_value = simple_value.replace(' ', '').replace('\t', '')
                if compressed_checked_value != compressed_simple_value:
                    failed.append("""%r:
         %s
         %s""" % (key, 'checked -> %r' % (checked_value), 'simple  -> %r' % (simple_value)))
            if checked_value != simple_value:
                failed.append("""%r:
         %s
         %s""" % (key, 'checked -> %r' % (checked_value), 'simple  -> %r' % (simple_value)))
    # orphan @0x0160
    failed.sort()
    member_names
    # orphan @0x016C
    # orphan @0x0170
    failed_member = []
    name not in simple_keys
    # orphan @0x0180
    failed.append('missing member from simple enum: %r' % name)
    # orphan @0x0190
    name not in checked_keys
    # orphan @0x019A
    failed.append('extra member in simple enum: %r' % name)
    # orphan @0x01AA
    checked_member_dict = checked_enum[name].__dict__
    checked_member_keys = list(checked_member_dict.keys())
    simple_member_dict = simple_enum[name].__dict__
    simple_member_keys = list(simple_member_dict.keys())
    set(checked_member_keys + simple_member_keys)
    # orphan @0x01E2
    # orphan @0x01E4
    key in ('__module__', '__objclass__', '_inverted_')
    # orphan @0x01F2
    # orphan @0x01F6
    key not in simple_member_keys
    # orphan @0x0200
    failed_member.append('missing key %r not in the simple enum member %r' % (key, name))
    # orphan @0x0214
    key not in checked_member_keys
    # orphan @0x021E
    failed_member.append('extra key %r in simple enum member %r' % (key, name))
    # orphan @0x0232
    checked_value = checked_member_dict[key]
    simple_value = simple_member_dict[key]
    checked_value != simple_value
    # orphan @0x024C
    failed_member.append("""%r:
         %s
         %s""" % (key, 'checked member -> %r' % (checked_value), 'simple member  -> %r' % (simple_value)))
    # orphan @0x026C
    # orphan @0x0270
    failed_member
    # orphan @0x0276
    failed.append("""%r member mismatch:
      %s""" % (name, """
      """.join(failed_member)))
    # orphan @0x0292
    ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__')
    # orphan @0x0296
    # orphan @0x0298
    method in simple_keys
    # orphan @0x02A4
    method in checked_keys
    # orphan @0x02B0
    # orphan @0x02B4
    method not in simple_keys
    # orphan @0x02BE
    method not in checked_keys
    # orphan @0x02C8
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)
    hasattr(checked_method, '__func__')
    # orphan @0x02EC
    checked_method = checked_method.__func__
    simple_method = simple_method.__func__
    # orphan @0x02F8
    checked_method != simple_method
    # orphan @0x0302
    failed.append('%r:  %-30s %s' % (method, 'checked -> %r' % (checked_method), 'simple -> %r' % (simple_method)))
    # orphan @0x0324
    # orphan @0x0328
    failed
    # orphan @0x032E
def _old_convert_(etype, name, module, filter, source):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    # orphan @0x001C
    members = _old_convert_.<locals>.<listcomp>(source.items())
    members.sort(key=_old_convert_.<locals>.<lambda>)
    # orphan @0x0018
    source = module_globals
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    # orphan @0x0048
    # orphan @0x0050
    members.sort(key=_old_convert_.<locals>.<lambda>)
    # orphan @0x006A
    # orphan @0x006C
    boundary
    module
    members
    name
    etype
    # orphan @0x0078
    KEEP
    # orphan @0x007A
    return cls
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 334 instr
