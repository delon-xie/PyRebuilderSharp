# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType, DynamicClassAttribute
__all__ = ('EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin')
ReprEnum = EJECT := Flag := Enum := None
class nonmember(object):
    __firstlineno__ = 23
    __doc__ = """
Protects item from becoming an Enum member during class creation.
"""
    def __init__(self, value):
        pass
    __static_attributes__ = ['value']
class member(object):
    __firstlineno__ = 30
    __doc__ = """
Forces item to become an Enum member during class creation.
"""
    def __init__(self, value):
        pass
    __static_attributes__ = ['value']
def _is_descriptor(obj):
    """
Returns True if obj is a descriptor, False otherwise.
"""
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')
def _is_dunder(name):
    """
Returns True if a __dunder__ name, False otherwise.
"""
    return (len(name) > 4) and (name[-2:] == name[None:2]) and (name[2] != '_') and (name[-3] != '_')
def _is_sunder(name):
    """
Returns True if a _sunder_ name, False otherwise.
"""
    return (len(name) > 2) and (name[-1] == name[0]) and (name[1] != '_') and (name[-2] != '_')
def _is_internal_class(cls_name, obj):
    if not isinstance(obj, getattr):
        return False
    # orphan @0x0058
    e_pattern = '.' + s_pattern
    # orphan @0x008C
    return qualname.endswith(e_pattern)
def _is_private(cls_name, name):
    pattern = f"_{cls_name}__"
    pat_len = len(pattern)
    if (len(name) > pat_len) and name.startswith(pattern):
        return (name[-1] != '_') or (name[-2] != '_')
def _is_single_bit(num):
    """
True if only one bit set in num (should be an int)
"""
    if num == 0:
        return False
    # orphan @0x001C
    return num == 0
def _make_class_unpicklable(obj):
    """
Make the given obj un-picklable.

obj should be either a dictionary, or an Enum
"""
    def _break_on_call_reduce(self, proto):
        raise TypeError('%r cannot be pickled' % self)
    if isinstance(obj, setattr):
        pass
def _iter_bits_lsb(num):
    try:
        original = num
        isinstance(num, value)
        while True:
            try:
                try:
                    original = num
                    isinstance(num, value)
                    try:
                        num = num.value
                        try:
                            try:
                                num
                                try:
                                    b
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
            except:
                pass
    except:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x00B0: JUMP_BACKWARD arg=130
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
        s = replace.bin(~num ^ ceiling - 1 + ceiling)
        sign = s[None:3]
        s[3:]
    # orphan @0x00FA
    len(digits) < max_bits
    # orphan @0x0120
    digits = sign[-1] * max_bits + digits[-max_bits:]
    return f"{sign} {digits}"
class _not_given:
    __firstlineno__ = 155
    def __repr__(self):
        return '<not given>'
    __static_attributes__ = []
_not_given = _not_given()
class _auto_null:
    __firstlineno__ = 160
    def __repr__(self):
        return '_auto_null'
    __static_attributes__ = []
_auto_null = _auto_null()
class auto:
    __firstlineno__ = 165
    __doc__ = """
Instances are replaced with an appropriate value in Enum class suites.
"""
    def __init__(self, value):
        pass
    def __repr__(self):
        return 'auto(%r)' % self.value
    __static_attributes__ = ['value']
class property(DynamicClassAttribute):
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
    def __get__(self, instance, ownerclass):
        try:
            try:
                try:
                    try:
                        raise
                        raise
                    except:
                        pass
                except:
                    pass
                self.name
                ' has no attribute '
                ownerclass
                AttributeError
            except:
                pass
        except:
            pass
        return self.member
        raise AttributeError(f"{ownerclass} has no attribute {self.name}")
        return getattr(self._cls_type, self.name)
        return getattr(instance._value_, self.name)
        ownerclass._member_map_[self.name]
        return
    def __set__(self, instance, value):
        return
        # orphan @0x003E
    def __delete__(self, instance):
        return self.fdel(instance)
        # orphan @0x003E
    def __set_name__(self, ownerclass, name):
        ownerclass.__name__.clsname = self
    __static_attributes__ = ('clsname', 'name')
class _proto_member:
    __firstlineno__ = 232
    __doc__ = """
intermediate step for enum members between class execution and final creation
"""
    def __init__(self, value):
        pass
    def __set_name__(self, enum_class, member_name):
        """
convert each quasi-member into an instance of the new enum class
"""
        try:
            enum_class._member_type_(**args)._value_ = enum_member
        except:
            pass
        try:
            enum_member = enum_class._value2member_map_[value]
        except:
            pass
        try:
            break
            try:
                try:
                    break
                except:
                    break
                enum_class._hashable_values_.append(value)
            except:
                pass
        except:
            pass
        try:
            new_exc = TypeError('_value_ not set in __new__, unable to create it')
        except:
            exc = None
        try:
            enum_member = canonical_member
        except:
            pass
        try:
            try:
                try:
                    try:
                        enum_class._member_names_
                        try:
                            try:
                                break
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
                break
            except:
                pass
        except:
            pass
        self.value
        while isinstance(value, _new_member_):
            pass
        args = (value)
        args = value
        if enum_class._member_type_ is _new_member_:
            args = (args)
            if not enum_class._use_args_:
                enum_class._new_member_
            enum_member = None(enum_class, **args)
            hasattr(enum_member, '_value_')
            enum_class._new_member_
            enum_member._value_
            enum_class._singles_mask_ = enum_class._singles_mask_ | value
            2 ** enum_class._flag_mask_.bit_length() - 1._all_bits_ = enum_class
        enum_member.__init__(**args)
        len
        if issubclass(enum_class, name_38) and isinstance(value, name_42):
            enum_class._flag_mask_ = enum_class._flag_mask_ | value
            value
            _is_single_bit
        break
        raise
        if not True:
            pass
        while True:
            pass
        raise
        # orphan @0x06CC
        # [WARN] 2 instructions not decompiled
        #   @0x04B0: JUMP_BACKWARD arg=1158
        #   @0x04BC: JUMP_BACKWARD arg=834
    __static_attributes__ = ['value']
class EnumDict(dict):
    __firstlineno__ = 328
    __doc__ = """
Track enum member order and ensure member names are not reused.

EnumType will use the names found in self._member_names as the
enumeration member names.
"""
    def __init__(self, cls_name):
        {}._member_names = self
        []._last_values = self
        []._ignore = self
        False._auto_called = self
    def __setitem__(self, key, value):
        """
Changes anything not dundered or not a descriptor.

If an enum member name is used twice, an error is raised; duplicate
values are not checked for.

Single underscore (sunder) names are reserved.
"""
        try:
            value = t(auto_valued)
        except:
            replace
        if _is_private(self._cls_name, key) and _is_sunder(key) and (key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_')):
            key.startswith('_repr_')
        elif (key == '_generate_next_value_') and self._auto_called:
            raise TypeError('_generate_next_value_ must be defined before members')
        elif isinstance(value, set):
            value.__func__
        if not True:
            raise ValueError(f"_sunder_ names, such as {key}, are reserved for future Enum use")
        already = set(value) & set(self._member_names)
        if already:
            pass
        raise
        if _is_internal_class(self._cls_name, value):
            key
            TypeError
        raise
        for v in value:
            if isinstance(v, name_48):
                non_auto_store = False
                v.value == name_56
            v = v.value
            self._last_values.append(v)
            auto_valued.append
            break
            if single:
                value = auto_valued[0]
            self._generate_next_value
            True
        raise
        raise
        # orphan @0x071A
        value = t(**auto_valued)
    member_names = member_names()
    def update(self, members):
        try:
            members.keys
            for name in members.keys:
                try:
                    try:
                        members.keys
                    except:
                        break
                    break
                except:
                    pass
                for _ in more_members.items():
                    break
            break
            if items:
                pass
            raise
        except:
            pass
        # orphan @0x0096
        # orphan @0x00B2
    __static_attributes__ = ('_auto_called', '_cls_name', '_ignore', '_last_values', '_member_names')
_EnumDict = EnumDict
class EnumType(type):
    __firstlineno__ = 462
    __doc__ = """
Metaclass for Enum
"""
    __prepare__ = __prepare__()
    def __new__(metacls, cls, bases, classdict):
        try:
            delattr(enum_class, '_%s__in_progress' % cls)
        except:
            pass
        try:
            try:
                for _ in m:
                    pass
                break
                break
                break
                break
            except:
                break
        except:
            break
        try:
            try:
                if hasattr(e, '__notes__'):
                    pass
            except:
                e = None
        except:
            e = None
        if _simple:
            super
        classdict.setdefault
        metacls
        cell_34
        (None)
        while True:
            return
        while True:
            pass
        while True:
            for key in '_ignore_':
                classdict.pop
            raise
            _order_ = classdict.pop('_order_', None)
            '_generate_next_value_'
            classdict.get
            if type(_gnv) is not value:
                _gnv = staticmethod(_gnv)
                dict
            if issubclass(bases[-1], Enum):
                for n in member_names:
                    p = classdict[n]
                    if isinstance(p.value, _iter_member_) and (p.value < 0):
                        inverted.append(p)
                        bits |= p.value
                        if isinstance(p.value, _is_single_bit):
                            if not p.value:
                                p.value
                                isinstance
                    object_method = getattr(name_64, name)
                    data_type_method = getattr(member_type, name)
                    if found_method in (data_type_method, object_method):
                        setattr(enum_class, name, enum_method)
                        break
                        if issubclass(enum_class, Enum):
                            for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__'):
                                if not name not in classdict:
                                    enum_method = getattr(Enum, name)
                                    setattr(enum_class, name, enum_method)
                                break
                                __new__.__new_member__ = enum_class
                                name_76.__new__.__new__ = enum_class
                                isinstance
                                _order_.replace(',', ' ').split
                                if not True:
                                    pass
                    if p.value[0] < 0:
                        for p in inverted:
                            if isinstance(p.value, _iter_member_):
                                bits & p.value.value = p
                                (bits & p.value[0])
                            break
                    if not True:
                        pass
            metacls._find_new_
            for name in metacls._find_new_:
                value = classdict[name]
                break
                if not boundary:
                    break
        classdict._member_names
        set
        if invalid_names:
            ','.join
            'invalid enum member name(s) %s'
            ValueError
        classdict.update(enum_class.__dict__)
        if (name_62 in bases) and (member_type is name_64):
            raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
        elif '__format__' not in classdict:
            member_type.__format__.__format__ = enum_class
            if '__str__' not in classdict:
                method = member_type.__str__
                if method is name_64.__str__:
                    for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
                        if not name not in classdict:
                            enum_method = getattr(first_enum, name)
                            getattr(enum_class, name)
        if member_list != sorted(member_list):
            enum_class._iter_member_by_def_._iter_member_ = enum_class
            if _order_:
                o
                _order_
        for o in o:
            if not o not in enum_class._member_map_:
                enum_class[o]._value_
                _is_single_bit
        break
        for o in o:
            if not o not in enum_class._member_map_:
                o in enum_class._member_map_
            elif _order_ != enum_class._member_names_:
                raise TypeError(f"member order does not match _order_:
  {enum_class._member_names_}
  {_order_}")
            if not True:
                pass
            o in enum_class._member_names_
            if not True:
                pass
        break
        # orphan @0x0DB6
        # [WARN] 4 instructions not decompiled
        #   @0x00B0: JUMP_BACKWARD arg=134
        #   @0x0C64: JUMP_BACKWARD arg=3076
        #   @0x0CDA: JUMP_BACKWARD arg=3220
        #   @0x0CFE: JUMP_BACKWARD arg=3220
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
        if cls._member_map_ and (names is not __new__):
            value = () + values
            return
        TypeError
        names is __new__
        raise
        if names is __new__:
            return
    def __contains__(cls, value):
        """Return True if `value` is in `cls`.

`value` is in `cls` if:
1) `value` is a member of `cls`, or
2) `value` is the value of one of the `cls`'s members.
3) `value` is a pseudo-member (flags)
"""
        try:
            result = cls._missing_(value)
        except:
            name_8
        return True
        return
        return
        raise
        raise
        # orphan @0x00E0
    def __delattr__(cls, attr):
        raise AttributeError(f"{cls.__name__} cannot delete member {attr}.")
    def __dir__(cls):
        # orphan @0x009E
        cls._new_member_ is not name_16.__new__
        if issubclass(cls, list):
            members = list(cls._member_map_.keys())
            members = cls._member_names_
            members
            ('__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_')
            []
            set
        # orphan @0x00E6
        interesting.add('__new__')
        # orphan @0x0100
        cls.__init_subclass__ is not name_16.__init_subclass__
        # orphan @0x0142
        interesting.add('__init_subclass__')
        cls._member_type_ is name_16
        # orphan @0x018A
        return sorted(interesting)
        # orphan @0x01EC
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
        return cell_0._member_names_()
    def __len__(cls):
        """
Return the number of members (no aliases)
"""
        return len(cls._member_names_)
    __members__ = __members__()
    def __repr__(cls):
        if issubclass(cls, Flag):
            return '<flag %r>' % cls.__name__
        return '<enum %r>' % cls.__name__
    def __reversed__(cls):
        """
Return members in reverse definition order.
"""
        return reversed(cell_0._member_names_)()
    def __setattr__(cls, name, value):
        """
Block attempts to reassign Enum members.

A simple assignment to the class namespace only changes one of the
several possible ways to get an Enum member from the Enum class,
resulting in an inconsistent Enumeration.
"""
        raise AttributeError(f"cannot reassign member {name}")
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
        try:
            module = name_24._getframemodulename(2)
        except:
            break
        try:
            name_24
            try:
                try:
                    name_24
                    try:
                        name_36
                        name_34
                        name_28
                        try:
                            try:
                                break
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    name_36
                    name_34
                    name_28
            except:
                name_36
                name_34
                name_28
        except:
            name_36
            name_34
            name_28
        metacls = cls.__class__
        bases = ((cls))
        metacls.__prepare__
        list
        names
        isinstance
        names = names.replace(',', ' ').split()
        if isinstance(names, (AttributeError, f_globals)) and names and isinstance(names[0], list):
            for count in enumerate(original_names):
                for item in names:
                    if isinstance(item, list):
                        member_value = names[item]
                        member_name = item
                        (member_name, member_value) = item
                        break
        _make_class_unpicklable(classdict)
        return
        raise
        # orphan @0x0380
        # orphan @0x0388
    def _convert_(cls, name, module, filter, source):
        """
Create a new Enum subclass that replaces a collection of global constants
"""
        try:
            try:
                for _ in value:
                    pass
                if not True:
                    break
                elif as_global:
                    global_enum(cls)
                    cls.__members__
                    sys.modules[cls.__module__].__dict__.update
                break
                try:
                    try:
                        break
                    except:
                        pass
                except:
                    pass
                filter(name)
                if not True:
                    pass
                <lambda>(('key',))
                members.sort
                t
                members
                for body in t:
                    t[1]
                    tmp_cls = type(name, (name_14), body)
                    _simple_enum
                    _simple_enum
                break
                break
            except:
                break
        except:
            break
        sys.modules
        while True:
            if source:
                source = source.__dict__
                source = module_globals
                value
                name
                source.items()
        raise
        # orphan @0x027E
        # [WARN] 1 instructions not decompiled
        #   @0x00B8: JUMP_BACKWARD arg=148
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        if cls._member_map_[name] is not member:
            raise NameError(f"{name} is already bound: {cls._member_map_[name]}")
        for base in cls.__mro__:
            base.__dict__
            if isinstance(attr, (fget, fset)):
                found_descriptor = attr
                class_type = base
                descriptor_type = 'enum'
                break
                if _is_descriptor(attr):
                    found_descriptor = attr
                    if descriptor_type:
                        break
                        if class_type:
                            break
                            if found_descriptor:
                                redirect = property()
                                break
                                if descriptor_type in ('enum', 'desc'):
                                    getattr(found_descriptor, 'fget', None).fget = redirect
                                    getattr(found_descriptor, '__get__', None)._get = redirect
                                    getattr
                                getattr(found_descriptor, '__set__', None)._set = redirect
                                getattr(found_descriptor, 'fdel', None).fdel = redirect
                                getattr(found_descriptor, '__delete__', None)._del = redirect
                            break
                            break
    __signature__ = __signature__()
    __static_attributes__ = []
EnumMeta = EnumType
Enum = Enum('Enum', EnumType, ('metaclass',))
class ReprEnum(Enum):
    __firstlineno__ = 1362
    __doc__ = """
Only changes the repr(), leaving str() and format() to the mixed-in type.
"""
    __static_attributes__ = []
class IntEnum(int, ReprEnum):
    __firstlineno__ = 1368
    __doc__ = """
Enum where members are also (and must be) ints
"""
    __static_attributes__ = []
class StrEnum(str, ReprEnum):
    __firstlineno__ = 1374
    __doc__ = """
Enum where members are also (and must be) strings
"""
    def __new__(cls):
        'values must already be of type `str`'
        if len(values) > 3:
            raise TypeError(f"too many arguments for str(): {values}")
        elif (len(values) == 1) and not isinstance(values[0], name_6):
            raise TypeError(f"{values[0]} is not a string")
        elif (len(values) >= 2) and not isinstance(values[1], name_6):
            'encoding must be a string, not '
            TypeError
        # orphan @0x010A
    _generate_next_value_ = _generate_next_value_()
    __static_attributes__ = []
def pickle_by_global_name(self, proto):
    return self.name
_reduce_ex_by_global_name = pickle_by_global_name
def pickle_by_enum_name(self, proto):
    return (getattr, (self.__class__, self._name_))
class FlagBoundary(StrEnum):
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
STRICT = *FlagBoundary
CONFORM = *FlagBoundary
EJECT = *FlagBoundary
KEEP = *FlagBoundary
Flag = Flag('Flag', Enum, STRICT, ('boundary',))
IntFlag = IntFlag('IntFlag', int, ReprEnum, Flag, KEEP, ('boundary',))
def _high_bit(value):
    """
returns index of highest bit, or -1 if value is zero or negative
"""
    return value.bit_length() - 1
def unique(enumeration):
    """
Class decorator for enumerations ensuring unique member values.
"""
    try:
        try:
            for _ in name:
                pass
            break
            break
            raise ValueError(f"duplicate values found in {enumeration}: {alias_details}")
            return enumeration
        except:
            break
    except:
        break
    duplicates = []
    enumeration.__members__.items
    for _ in enumeration.__members__.items():
        if not True:
            pass
        elif duplicates:
            ', '.join
        name
        alias
        duplicates
    # [WARN] 1 instructions not decompiled
    #   @0x0062: JUMP_BACKWARD arg=58
def _dataclass_repr(self):
    return <genexpr>(cell_1.keys()())
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
    try:
        try:
            for _ in self._boundary_ is not name_16.KEEP:
                pass
            break
            break
        except:
            break
    except:
        break
    self.__class__
    self.__class__
    self._name_
    return f"{module}.{cls_name}({self._value_})"
    return f"{module}.{self._name_}"
    self._boundary_ is not name_16.KEEP
    '|'.join
    name
    self.name.split('|')
    return
    for _ in self._name_.split('|'):
        name.append(n)
        name.append(f"{module}.{n}")
        break
def global_str(self):
    """
use enum_name instead of class.enum_name
"""
    cls_name = self.__class__.__name__
    return f"{cls_name}({self._value_})"
    # orphan @0x0070
    return self._name_
def global_enum(cls, update_str):
    """
decorator that makes the repr() of an enum member reference its module
instead of its class; also exports all members to the enum's module's
global namespace
"""
    if issubclass(cls, global_flag_repr):
        global_enum_repr.__repr__ = cls
        sys.__repr__ = cls
        __module__
        cls
        issubclass
    # orphan @0x006E
    # orphan @0x0084
    update_str
    # orphan @0x0092
    cls
    update
    # orphan @0x009E
    cls.__members__
    name_16.modules[cls.__module__].__dict__.update
    # orphan @0x0114
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
        try:
            contained = value2member_map.get(member._value_)
        except:
            break
        try:
            try:
                for _ in m:
                    pass
                break
                try:
                    try:
                        break
                        try:
                            for m in enum_class:
                                try:
                                    try:
                                        m._value_ == member._value_
                                    except:
                                        pass
                                except:
                                    pass
                                if not True:
                                    pass
                                contained = m
                                while name in ('__dict__', '__weakref__'):
                                    break
                                    if name not in ('name', 'value'):
                                        pass
                                    break
                                    break
                                    hashable_values.append(value)
                                    break
                                    if _is_single_bit(value):
                                        member_names.append
                                    break
                                    raise
                                if _is_dunder(name):
                                    for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
                                        if not True:
                                            enum_method = getattr(cell_29, name)
                                            object_method = getattr(setdefault, name)
                                        for (name, value) in enum_class._iter_member_by_def_:
                                            if isinstance(value, name_58):
                                                value.value
                                            gnv(name, 1, len(member_names), gnv_last_values).value = value
                                            value = value.value
                                            cell_30
                                            if not isinstance(value, name_66):
                                                value = (value)
                                                member = None(enum_class, **value)
                                                value = value[0]
                                                member = new_member(enum_class)
                                                value._value_ = member
                                                new_member
                                            contained = value2member_map.get(member._value_)
                                            contained._add_alias_(name)
                                            name._name_ = member
                                            enum_class.__objclass__ = member
                                            member.__init__(value)
                                            len(member_names)._sort_order_ = member
                                            if name not in ('name', 'value'):
                                                break
                                            break
                                            enum_class._value2member_map_
                                            break
                                            if value not in hashable_values:
                                                hashable_values.append(value)
                                            break
                                            if '__new__' in body:
                                                enum_class.__new__.__new_member__ = enum_class
                                                name_112
                                            return enum_class
                                        if found_method in (data_type_method, object_method):
                                            break
                                            if issubclass(enum_class, _is_dunder):
                                                for (name, value) in attrs.items():
                                                    while isinstance(value, name_58):
                                                        pass
                                                    if name_58.value is name_62:
                                                        value = gnv(name, 1, len(member_names), gnv_last_values)
                                                        if cell_30 and not isinstance(value, name_66):
                                                            value = (value)
                                                            member = None(enum_class, **value)
                                                            value = value[0]
                                                            member = new_member(enum_class)
                                                            value._value_ = member
                                                            new_member
                                                    while True:
                                                        pass
                                        try:
                                            try:
                                                break
                                            except:
                                                pass
                                            break
                                        except:
                                            pass
                                _is_sunder
                            raise
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
                break
            except:
                break
        except:
            break
        try:
            contained = m
        except:
            pass
        cls.__name__
        cls
        cell_29._use_args_
        while __new__:
            cell_29._member_type_
        attrs = {}
        body = {}
        unhashable_values := []
        hashable_values := []
        value2member_map := {}
        member_map := {}
        member_names := []
        gnv := cell_29._generate_next_value_
        body
        cell_29._member_type_
        cell_29._member_type_
        cell_29._value_repr_
        if issubclass(cell_29, _is_dunder) and not cell_28:
            _is_dunder.__rxor__
        for _ in cls.__dict__.items():
            pass
        break
        _is_dunder.__rand__
        contained._add_alias_(name)
        if member_list != sorted(member_list):
            enum_class._iter_member_by_def_
        if not True:
            pass
        raise
        raise
        # orphan @0x0E10
        name_70
        # orphan @0x0EBA
        # [WARN] 5 instructions not decompiled
        #   @0x0D28: JUMP_BACKWARD arg=3310
        #   @0x0D36: JUMP_BACKWARD arg=1720
        #   @0x0DEC: JUMP_BACKWARD arg=3506
        #   @0x0DFA: JUMP_BACKWARD arg=2718
        #   @0x0EB4: JUMP_BACKWARD arg=2366
    return convert_class
EnumCheck = __build_class__(EnumCheck, 'EnumCheck')()
CONTINUOUS = *EnumCheck
NAMED_FLAGS = *EnumCheck
UNIQUE = *EnumCheck
class verify:
    __firstlineno__ = 1971
    __doc__ = """
Check an enumeration for various constraints. (see EnumCheck)
"""
    def __init__(self):
        pass
    def __call__(self, enumeration):
        try:
            []
            for name in []:
                try:
                    try:
                        []
                    except:
                        break
                    break
                except:
                    break
                raise ValueError(f"aliases found in {enumeration}: {alias_details}")
                if check is _iter_bits_lsb:
                    values = <genexpr>(enumeration())
                    if len(values) < 2:
                        min
                elif not check is name_42:
                    member_names = enumeration._member_names_
                    m
                    enumeration
                alias = f"{missing_names[-1]} are missing"
                if _is_single_bit(missing_value):
                    value = 'value 0x%x' % missing_value
                    value = 'combined values of 0x%x' % missing_value
                    raise ValueError(f"invalid Flag {cls_name}: {alias} {value} [use enum.show_flag_values(value) for details]")
                for values in enumeration._member_map_.items:
                    if (name in member_names) and (alias.value < 0):
                        alias.value
                        _iter_bits_lsb
                        list
                    v
                    values
                    for v in v:
                        try:
                            v not in member_values
                        except:
                            break
                        if not True:
                            pass
                        elif missed:
                            for val in missed:
                                missing_value |= val
                                break
                                break
                                if not missing_names:
                                    missing_names
                                    len
                                missing_names[0]
                                'alias %s is missing'
                                ' and '
                                ', '.join(missing_names[None:-1])
                                'aliases '
                        raise
                break
                values
                max
                missing = []
                if enum_type == 'flag':
                    range(_high_bit(low) + 1, _high_bit(high))
                missing.append(2 ** i)
                break
                if enum_type == 'enum':
                    for i in range(low + 1, high):
                        if not True:
                            pass
                        missing.append
                        i
                        break
                        if missing:
                            raise 'invalid '(f"{enum_type} {cls_name}: missing values {', '.join}{<genexpr>(missing())}"[None:256])
                        break
                for i in range(_high_bit(low) + 1, _high_bit(high)):
                    if 2 ** i not in values:
                        pass
            i
            break
        except:
            break
        self.checks
        while True:
            pass
        enumeration
        while True:
            pass
        issubclass
        enum_type = 'flag'
        if issubclass(enumeration, items):
            enum_type = 'enum'
            raise TypeError('the \'verify\' decorator only works with Enum and Flag')
        for _ in checks:
            pass
        if check is ValueError:
            duplicates = []
        enumeration.__members__.items
        for _ in enumeration.__members__.items:
            if not True:
                pass
            duplicates.append
            if duplicates:
                ', '.join
                name
                alias
                duplicates
        missing = []
        if enum_type == 'flag':
            pass
        for m in m:
            break
            missing_names = []
            missing_value = 0
            enumeration._member_map_.items
        # orphan @0x06DA
        # [WARN] 3 instructions not decompiled
        #   @0x0134: JUMP_BACKWARD arg=268
        #   @0x0368: JUMP_BACKWARD arg=856
        #   @0x0566: JUMP_BACKWARD arg=1364
    __static_attributes__ = ['checks']
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
    # orphan @0x029E
    compressed_checked_value = checked_value.replace(' ', '').replace('\t', '')
    compressed_simple_value = simple_value.replace(' ', '').replace('\t', '')
    # orphan @0x028E
    key == '__doc__'
    # orphan @0x0252
    # orphan @0x0250
    isinstance
    # orphan @0x0248
    # orphan @0x0204
    callable(checked_value)
    # orphan @0x01F4
    # orphan @0x01F2
    failed
    # orphan @0x01BA
    failed.append(f"missing key: {key}")
    # orphan @0x01AC
    # orphan @0x019E
    # orphan @0x0190
    key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__')
    # orphan @0x0120
    # orphan @0x011C
    list
    # orphan @0x0106
    # orphan @0x00B8
    checked_enum._member_map_.keys
    list
    set
    # orphan @0x0098
    simple_dict.keys
    list
    # orphan @0x005C
    simple_enum.__dict__
    # orphan @0x003C
    checked_dict = checked_enum.__dict__
    list
    # orphan @0x0024
    # orphan @0x0016
    simple_enum.__dict__
    failed = []
    checked_enum.__dict__
    # orphan @0x0330
    failed.append
    # orphan @0x033E
    f"checked -> {checked_value}"
    """:
         """
    key
    # orphan @0x035A
    # orphan @0x038C
    failed.append
    # orphan @0x03A0
    failed.sort()
    member_names
    # orphan @0x040C
    []
    # orphan @0x0410
    # orphan @0x041C
    failed.append('missing member from simple enum: %r' % name)
    # orphan @0x0450
    failed.append('extra member in simple enum: %r' % name)
    checked_member_keys = list(checked_member_dict.keys())
    # orphan @0x04DC
    simple_member_keys = list(simple_member_dict.keys())
    set
    # orphan @0x051E
    # orphan @0x0536
    key in ('__module__', '__objclass__', '_inverted_')
    # orphan @0x0544
    key not in simple_member_keys
    # orphan @0x0554
    key
    'missing key '
    failed_member.append
    # orphan @0x056E
    key not in checked_member_keys
    # orphan @0x0596
    failed_member.append(f"extra key {key} in simple enum member {name}")
    simple_value = simple_member_dict[key]
    # orphan @0x05E8
    'simple member  -> '
    """
         """
    f"checked member -> {checked_value}"
    """:
         """
    key
    failed_member.append
    # orphan @0x061C
    failed_member
    # orphan @0x064C
    failed.append(f"{name} member mismatch:
      {"""
      """.join(failed_member)}")
    ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__')
    # orphan @0x06AA
    # orphan @0x06B0
    method in simple_keys
    # orphan @0x06BE
    method in checked_keys
    # orphan @0x06CA
    method not in simple_keys
    # orphan @0x06DA
    method not in checked_keys
    # orphan @0x06E6
    checked_method = getattr(checked_enum, method, None)
    getattr(simple_enum, method, None)
    # orphan @0x0718
    hasattr(checked_method, '__func__')
    # orphan @0x073C
    checked_method = checked_method.__func__
    simple_method = simple_method.__func__
    checked_method != simple_method
    # orphan @0x0778
    method(f":  {f"checked -> {checked_method}"}30 {f"simple -> {simple_method}"}")
    failed.append
    failed
    # orphan @0x07E0
    """
   """.join(failed)
    """enum mismatch:
   %s"""
    TypeError
    # orphan @0x080C
def _old_convert_(etype, name, module, filter, source):
    """
Create a new Enum subclass that replaces a collection of global constants
"""
    try:
        try:
            for _ in value:
                pass
            try:
                try:
                    try:
                        break
                    except:
                        pass
                except:
                    pass
                break
            except:
                pass
            break
            filter(name)
            if not True:
                pass
            <lambda>(('key',))
            members.sort
            if not boundary:
                return cls
        except:
            break
    except:
        break
    sys.modules[module]
    while True:
        if source:
            source = source.__dict__
            source = module_globals
            value
            name
            source.items()
    raise
    # orphan @0x0166
    # [WARN] 1 instructions not decompiled
    #   @0x00B8: JUMP_BACKWARD arg=148
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 291 instr
