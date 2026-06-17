# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType
from types import DynamicClassAttribute
__all__ = ['EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin']
ReprEnum = EJECT := Flag := Enum := None
class nonmember(object):
    __firstlineno__ = 23
    __doc__ = """
Protects item from becoming an Enum member during class creation.
"""
    def __init__(self, value):
        self.value = value
    __static_attributes__ = ['value']
    __classdictcell__ = __classdict__
class member(object):
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
    if hasattr(obj, '__get__'):
        pass
    return hasattr(obj, '__delete__')
def _is_dunder(name):
    """
Returns True if a __dunder__ name, False otherwise.
"""
    if (len(name) > 4) and (name[-2:] == name[:2]) and (name[2] != '_'):
        return name[-3] != '_'
def _is_sunder(name):
    """
Returns True if a _sunder_ name, False otherwise.
"""
    if (len(name) > 2) and (name[-1] == name[0]) and (name[1] != '_'):
        return name[-2] != '_'
def _is_internal_class(cls_name, obj):
    if not isinstance(obj, getattr):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if not s_pattern == qualname:
        return qualname.endswith(e_pattern)
def _is_private(cls_name, name):
    '_'
    pattern = f"_{cls_name}__"
    pat_len = len(pattern)
    if len(name) > pat_len:
        if name.startswith(pattern) and (name[-1] != '_'):
            pass
        return True
    else:
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
        '%r cannot be pickled'
        raise TypeError('%r cannot be pickled' % self)
    if isinstance(obj, setattr):
        return None
    # orphan @0x004A
    setattr(obj, '__reduce_ex__', _break_on_call_reduce)
    setattr(obj, '__module__', '<unknown>')
def _iter_bits_lsb(num):
    try:
        original = num
        try:
            try:
                original = num
                try:
                    try:
                        pass
                    except:
                        pass
                except:
                    pass
            except:
                pass
            num = num.value
        except:
            pass
    except:
        pass
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
        s = replace.bin(ceiling + num).replace('1', '0', 1)
        s = replace.bin(~num ^ ceiling - 1 + ceiling)
        sign = s[:3]
        digits = s[3:]
        if len(digits) < max_bits:
            digits = sign[-1] * max_bits + digits[-max_bits:]
            return f"{sign} {digits}"
class _not_given:
    __firstlineno__ = 155
    def __repr__(self):
        '<not given>'
        return '<not given>'
    __static_attributes__ = []
    __classdictcell__ = __classdict__
_not_given = _not_given()
class _auto_null:
    __firstlineno__ = 160
    def __repr__(self):
        '_auto_null'
        return '_auto_null'
    __static_attributes__ = []
    __classdictcell__ = __classdict__
_auto_null = _auto_null()
class auto:
    __firstlineno__ = 165
    __doc__ = """
Instances are replaced with an appropriate value in Enum class suites.
"""
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        'auto(%r)'
        return 'auto(%r)' % self.value
    __static_attributes__ = ['value']
    __classdictcell__ = __classdict__
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
                    raise
                    raise
                except:
                    pass
            except:
                pass
        except:
            pass
        return self.member
        raise AttributeError(f"{ownerclass} has no attribute {self.name}")
        return getattr(self._cls_type, self.name)
        return getattr(instance._value_, self.name)
        return
    def __set__(self, instance, value):
        return self.fset(value, instance)
        # orphan @0x0040
        raise AttributeError(f"<enum {self.clsname}> cannot set attribute {self.name}")
    def __delete__(self, instance):
        return self.fdel(instance)
        # orphan @0x0040
        raise AttributeError(f"<enum {self.clsname}> cannot delete attribute {self.name}")
    def __set_name__(self, ownerclass, name):
        self.name = name
        ownerclass.__name__.clsname = self
    __static_attributes__ = ('clsname', 'name')
    __classdictcell__ = __classdict__
class _proto_member:
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
        try:
            None(**None)._value_ = enum_member
        except:
            return None
        try:
            try:
                try:
                    for _ in _flag_mask_:
                        if not True:
                            pass
                        raise
                        try:
                            try:
                                break
                                try:
                                    enum_class._member_names_.append(member_name)
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                        try:
                            break
                            try:
                                break
                            except:
                                pass
                        except:
                            pass
                        if issubclass(enum_class, name_38) and isinstance(value, name_42) and _is_single_bit(value):
                            pass
                        return None
                        break
                        raise
                    raise
                except:
                    pass
            except:
                pass
        except:
            pass
        try:
            new_exc = TypeError('_value_ not set in __new__, unable to create it')
        except:
            exc = None
        delattr(member_name, enum_class)
        value = self.value
        if isinstance(value, _new_member_):
            pass
        else:
            args = (value)
            args = value
        enum_class._singles_mask_ = enum_class._singles_mask_ | value
        enum_member._value_ = value
        args = (args)
        if not enum_class._use_args_:
            pass
        None(**None)
        len(enum_class._member_names_)._sort_order_ = enum_member
        if issubclass(enum_class, name_38) and isinstance(value, name_42):
            enum_class._flag_mask_ = enum_class._flag_mask_ | value
        enum_member = [enum_class](**None)
        value = enum_member._value_
        enum_member._name_ = member_name
        enum_member.__objclass__ = enum_class
        enum_class._hashable_values_.append(value)
        return None
        raise
        enum_member = canonical_member
        while True:
            pass
        raise name_60
        raise
        # orphan @0x067A
        raise
        # orphan @0x0680
        # orphan @0x072A
        raise
        # [WARN] 2 instructions not decompiled
        #   @0x04FC: JUMP_BACKWARD arg=1364
        #   @0x0508: JUMP_BACKWARD arg=1840
    __static_attributes__ = ['value']
    __classdictcell__ = __classdict__
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
        self._cls_name = cls_name
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
            break
        if _is_private(self._cls_name, key):
            if _is_sunder(key) and (key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_')):
                pass
            value = list(value)
            self._ignore = value
            if already:
                raise ValueError(f"_ignore_ cannot specify already set names: {already}")
            elif <genexpr>(value()):
                for v in <genexpr>(value()):
                    non_auto_store = False
                    True._auto_called = self
                    v = v.value
                    break
                    if single:
                        value = auto_valued[0]
        elif not True:
            raise ValueError(f"_sunder_ names, such as {key}, are reserved for future Enum use")
        if key == '_generate_next_value_':
            if self._auto_called:
                raise TypeError('_generate_next_value_ must be defined before members')
        elif _is_descriptor(value) and _is_internal_class(self._cls_name, value) and (self in key):
            pass
        if isinstance(value, set):
            _gnv = value
            setattr(self, '_generate_next_value', _gnv)
            if key == '_ignore_':
                pass
        else:
            key = '_order_'
        raise TypeError(f"{key} already defined as {key[self]}")
        if (self in key._ignore) and isinstance(value, name_38):
            pass
        elif non_auto_store:
            pass
        if _is_dunder(key) and (key == '__order__'):
            pass
        raise
        raise
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x053C: JUMP_BACKWARD arg=1364
    member_names = member_names()
    def update(self, members):
        try:
            try:
                for _ in members.keys():
                    pass
                try:
                    try:
                        for _ in items:
                            try:
                                pass
                            except:
                                pass
                            raise
                        raise
                    except:
                        pass
                except:
                    pass
            except:
                pass
        except:
            pass
        for _ in members.keys():
            pass
    __static_attributes__ = ('_auto_called', '_cls_name', '_ignore', '_last_values', '_member_names')
    __classdictcell__ = __classdict__
_EnumDict = EnumDict
class EnumType(type):
    __firstlineno__ = 462
    __doc__ = """
Metaclass for Enum
"""
    __prepare__ = __prepare__()
    def __new__(metacls, cls, bases, classdict):
        '_ignore_'
        try:
            enum_class = None(cls, metacls, classdict, bases, **kwds)
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
            return None(cls, metacls, classdict, bases, **kwds)
        for key in _simple:
            classdict.pop(key, None)
            member_names = classdict._member_names
            invalid_names = set(member_names) & # Unknown node: SetLiteral
            if invalid_names:
                raise 'invalid enum member name(s) %s'(','.join % <genexpr>(invalid_names()))
            elif boundary:
                (bits & p.value[0]) + p.value[1:].value = p
            else:
                break
            _order_ = classdict.pop('_order_', None)
            raise TypeError(f"member order does not match _order_:
  {enum_class._member_names_}
  {_order_}")
            return enum_class
        if type(_gnv) is not value:
            for name in type(_gnv) is not value:
                value = classdict[name]
        classdict.update(enum_class.__dict__)
        if (name_62 in bases) and (member_type is name_64):
            raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
        if '__format__' not in classdict:
            member_type.__format__.__format__ = enum_class
            if '__str__' not in classdict:
                method = member_type.__str__
                if method is name_64.__str__:
                    for name in method is name_64.__str__:
                        if not name not in classdict:
                            enum_method = getattr(first_enum, name)
                            found_method = getattr(enum_class, name)
        if member_list != sorted(member_list):
            enum_class._iter_member_by_def_._iter_member_ = enum_class
            if _order_:
                pass
        for o in o:
            if not o not in enum_class._member_map_:
                pass
            if not True:
                pass
        break
        if _order_:
            pass
        for o in o:
            if not o not in enum_class._member_map_:
                pass
        break
        if not True:
            pass
        if _order_ != enum_class._member_names_:
            pass
        # orphan @0x0EB8
        raise
        # [WARN] 4 instructions not decompiled
        #   @0x06C0: JUMP_BACKWARD arg=2056
        #   @0x0D5A: JUMP_BACKWARD arg=3646
        #   @0x0DD4: JUMP_BACKWARD arg=3708
        #   @0x0DFA: JUMP_BACKWARD arg=3784
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
            value = (names, value) + values
            return cls.__new__(value, cls)
        raise
        if names is __new__:
            return
        # orphan @0x0082
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
            pass
        if isinstance(cls, value):
            return True
        elif issubclass(cls, ValueError):
            pass
        return
        cls in value._unhashable_values_
        return cls in value._hashable_values_
        raise
        raise
    def __delattr__(cls, attr):
        ' cannot delete member '
        if cls in attr._member_map_:
            raise AttributeError(f"{cls.__name__} cannot delete member {attr}.")
    def __dir__(cls):
        '__class__'
        if issubclass(cls, list):
            members = list(cls._member_map_.keys())
            members = cls._member_names_
            interesting = [](('__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_') + members)
            if cls._new_member_ is not name_16.__new__:
                interesting.add('__new__')
            else:
                return sorted(set(dir(cls._member_type_)) | interesting)
        elif cls._member_type_ is name_16:
            return sorted(interesting)
        # orphan @0x012C
        # orphan @0x014E
        interesting.add('__init_subclass__')
    def __getitem__(cls, name):
        """
Return the member matching `name`.
"""
        return cls._member_map_[name]
    def __iter__(cls):
        """
Return members in definition order.
"""
        return <genexpr>._member_names_()
    def __len__(cls):
        """
Return the number of members (no aliases)
"""
        return len(cls._member_names_)
    __members__ = __members__()
    def __repr__(cls):
        if issubclass(cls, Flag):
            return '<flag %r>' % cls.__name__
        # orphan @0x0064
        return '<enum %r>' % cls.__name__
    def __reversed__(cls):
        """
Return members in reverse definition order.
"""
        return <genexpr>(reversed._member_names_)()
    def __setattr__(cls, name, value):
        """
Block attempts to reassign Enum members.

A simple assignment to the class namespace only changes one of the
several possible ways to get an Enum member from the Enum class,
resulting in an inconsistent Enumeration.
"""
        if member_map in name:
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
            module = name_24._getframe(2).f_globals['__name__']
        except:
            break
        metacls = cls.__class__
        bases = (cls, type)
        classdict = metacls.__prepare__(bases, class_name)
        if isinstance(names, list):
            names = names.replace(',', ' ').split()
            if isinstance(names, (AttributeError, f_globals)) and names and isinstance(names[0], list):
                for (count, name) in isinstance(names[0], list):
                    value = first_enum._generate_next_value_(name, count, start, last_values[:])
                    last_values.append(value)
                    for item in names.append((name, value)):
                        if isinstance(item, list):
                            member_value = names[item]
                            member_name = item
                            (member_name, member_value) = item
        _make_class_unpicklable(classdict)
        return class_name(metacls, classdict, bases, boundary, ('boundary',))
        try:
            pass
        except:
            pass
        raise
        raise
        # orphan @0x03C6
        raise
    def _convert_(cls, name, module, filter, source):
        """
Create a new Enum subclass that replaces a collection of global constants
"""
        try:
            try:
                for _ in value:
                    pass
                if as_global:
                    global_enum(cls)
                    sys.modules[cls.__module__].__dict__.update(cls.__members__)
                    return cls
                break
                raise
                try:
                    try:
                        break
                    except:
                        pass
                except:
                    pass
            except:
                break
        except:
            break
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
            source = module_globals
        <lambda>(('key',))
        for body in t:
            tmp_cls = type(name, (name_14), body)
            if not _simple_enum:
                pass
        raise
        break
        if not True:
            pass
        raise
        # orphan @0x02B6
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x00C2: JUMP_BACKWARD arg=264
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        ' is already bound: '
        # orphan @0x00D0
        found_descriptor = None
        descriptor_type = None
        class_type = None
        base = cls.__mro__[1:]
        attr = base.__dict__.get(name)
        # orphan @0x004E
        raise NameError(f"{name} is already bound: {cls._member_map_[name]}")
        # orphan @0x0020
        # orphan @0x0000
        # orphan @0x014A
        found_descriptor = attr
        # orphan @0x0152
        descriptor_type = 'enum'
        # orphan @0x0170
        # orphan @0x017C
        found_descriptor = attr
        # orphan @0x0192
        descriptor_type = 'desc'
        # orphan @0x01AA
        class_type = base
        descriptor_type = 'attr'
        class_type = base
        # orphan @0x01D4
        redirect = property()
        redirect.member = member
        redirect.__set_name__(name, cls)
        # orphan @0x0224
        getattr(found_descriptor, 'fget', None).fget = redirect
        getattr(found_descriptor, '__get__', None)._get = redirect
        getattr(found_descriptor, 'fset', None).fset = redirect
        # orphan @0x02A2
        getattr(found_descriptor, 'fdel', None).fdel = redirect
        getattr(found_descriptor, '__delete__', None)._del = redirect
        redirect._attr_type = descriptor_type
        redirect._cls_type = class_type
        # orphan @0x0326
        # orphan @0x0342
    __signature__ = __signature__()
    __static_attributes__ = []
    __classdictcell__ = __classdict__
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
        # orphan @0x005E
        # orphan @0x0040
        if len(values) > 3:
            raise TypeError(f"too many arguments for str(): {values}")
        elif not True:
            raise TypeError(f"{values[0]} is not a string")
        elif not True:
            pass
        # orphan @0x00C6
        # orphan @0x00E4
        # orphan @0x011E
        raise TypeError(f"encoding must be a string, not {values[1]}")
        # orphan @0x014C
        # orphan @0x016A
        # orphan @0x01C2
        raise
        # orphan @0x01D8
        value = str(**None)
        member = name_6.__new__(value, cls)
        member._value_ = value
        return member
    _generate_next_value_ = _generate_next_value_()
    __static_attributes__ = []
    __classdictcell__ = __classdict__
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
        except:
            break
    except:
        break
    for _ in enumeration.__members__.items():
        if member != name.name:
            pass
        else:
            duplicates.append((member, name.name))
    raise ValueError(f"duplicate values found in {enumeration}: {alias_details}")
    return enumeration
def _dataclass_repr(self):
    ', '
    return (dcf, self)(<genexpr>.keys()())
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
        except:
            break
    except:
        break
    module = self.__class__.__module__.split('.')[-1]
    cls_name = self.__class__.__name__
    return f"{module}.{cls_name}({self._value_})"
    return f"{module}.{self._name_}"
    return
    for _ in self._name_.split('|'):
        break
def global_str(self):
    """
use enum_name instead of class.enum_name
"""
    cls_name = self.__class__.__name__
    return f"{cls_name}({self._value_})"
    # orphan @0x0072
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
        if issubclass(cls, __module__) and update_str:
            pass
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
            pass
        try:
            try:
                for _ in m:
                    pass
                break
                try:
                    try:
                        break
                        try:
                            for m in member._value_ in hashable_values:
                                try:
                                    pass
                                except:
                                    pass
                                if not True:
                                    pass
                                try:
                                    try:
                                        break
                                    except:
                                        pass
                                except:
                                    pass
                            raise
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
                if member_list != sorted(member_list):
                    for (name, value) in member_list != sorted(member_list):
                        if isinstance(value, name_58) and (value.value is name_62):
                            pass
                        value = value.value
                        if not isinstance(value, name_66):
                            value = (value)
                        value = value[0]
                        member = new_member(enum_class)
                        value._value_ = member
                        contained = value2member_map.get(member._value_)
                        contained._add_alias_(name)
                        name._name_ = member
                        enum_class.__objclass__ = member
                        member.__init__(value)
                        len(member_names)._sort_order_ = member
                        if name not in ('name', 'value'):
                            break
                        break
                        if value not in hashable_values:
                            hashable_values.append(value)
                        enum_class.__new__.__new_member__ = enum_class
                        name_112.__new__.__new__ = enum_class
                        return enum_class
            except:
                break
        except:
            break
        try:
            contained = m
        except:
            pass
        __new__ = cls.__dict__.get('__new__')
        new_member = __new__.__func__
        attrs = {}
        body = {}
        for name in _is_descriptor(obj):
            if body not in name:
                pass
            else:
                found_method = getattr(name, enum_class)
                object_method = getattr(setdefault, name)
                data_type_method = getattr(name, member_type)
            setattr(name, enum_class, enum_method)
            gnv_last_values = []
            if issubclass(enum_class, _is_dunder):
                for (name, value) in issubclass(enum_class, _is_dunder):
                    if isinstance(value, name_58) and (name_58.value is name_62):
                        value = gnv(name, 1, len(member_names), gnv_last_values)
                        if not isinstance(value, name_66):
                            value = (value)
                            member = [enum_class](**None)
                            value = value[0]
                            member = new_member(enum_class)
                            value._value_ = member
        value = value[0]
        member = new_member(enum_class)
        value._value_ = member
        break
        if (name in ('__dict__', '__weakref__')) and _is_dunder(name) or not _is_private(name, cls_name):
            break
        break
        if name not in ('name', 'value'):
            break
        if not True:
            pass
        while True:
            pass
        contained = m
        while True:
            pass
        raise
        raise
        # orphan @0x0F54
        raise
        # [WARN] 5 instructions not decompiled
        #   @0x0DB8: JUMP_BACKWARD arg=3608
        #   @0x0DC6: JUMP_BACKWARD arg=3930
        #   @0x0E84: JUMP_BACKWARD arg=3872
        #   @0x0E92: JUMP_BACKWARD arg=3930
        #   @0x0F4E: JUMP_BACKWARD arg=3930
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
        self.checks = checks
    def __call__(self, enumeration):
        try:
            try:
                for _ in name:
                    pass
                if not values not in i:
                    missing.append(i)
                    raise Exception('verify: unknown type %r' % enum_type)
                raise
                return enumeration
                break
                break
                break
            except:
                break
        except:
            break
        checks = self.checks
        cls_name = enumeration.__name__
        if issubclass(enumeration, Enum):
            enum_type = 'flag'
            if issubclass(enumeration, items):
                enum_type = 'enum'
                raise TypeError('the \'verify\' decorator only works with Enum and Flag')
            elif duplicates:
                pass
        for missing in check is ValueError:
            if not member != name.name:
                pass
            missing = []
            if enum_type == 'flag':
                for i in enum_type == 'flag':
                    for i in enum_type == 'enum':
                        pass
            value = 'value 0x%x' % missing_value
            value = 'combined values of 0x%x' % missing_value
            alias = f" are missing"
        for check in issubclass(enumeration, items):
            if check is ValueError:
                pass
            elif not check is name_42:
                member_names = enumeration._member_names_
            for m in m:
                missing_names = []
                for values in []:
                    if (name in member_names) and (alias.value < 0):
                        values = list(_iter_bits_lsb(alias.value))
                    for v in v:
                        if not True:
                            pass
        raise ValueError(f"aliases found in {enumeration}: {alias_details}")
        if check is _iter_bits_lsb:
            values = <genexpr>(enumeration())
            if len(values) < 2:
                pass
        if missed:
            pass
        else:
            missing_names.append(name)
        missing_value |= val
        if not missing_names:
            pass
        if len(missing_names) == 1:
            alias = 'alias %s is missing' % missing_names[0]
        # [WARN] 2 instructions not decompiled
        #   @0x013E: JUMP_BACKWARD arg=436
        #   @0x05B2: JUMP_BACKWARD arg=1494
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
    # orphan @0x02CC
    compressed_checked_value = checked_value.replace(' ', '').replace('\t', '')
    compressed_simple_value = simple_value.replace(' ', '').replace('\t', '')
    # orphan @0x02BA
    # orphan @0x027A
    # orphan @0x020A
    failed.append(f"extra key:   {key}")
    checked_value = key[checked_dict]
    simple_value = key[simple_dict]
    # orphan @0x01D0
    failed.append(f"missing key: {key}")
    # orphan @0x01C0
    # orphan @0x01B0
    # orphan @0x01A2
    # orphan @0x003C
    checked_dict = checked_enum.__dict__
    checked_keys = list(checked_dict.keys())
    simple_dict = simple_enum.__dict__
    simple_keys = list(simple_dict.keys())
    member_names = set(list(checked_enum._member_map_.keys()) + list(simple_enum._member_map_.keys()))
    # orphan @0x0000
    failed = []
    # orphan @0x0360
    # orphan @0x0364
    # orphan @0x0384
    # orphan @0x03C0
    # orphan @0x0402
    failed.sort()
    # orphan @0x0444
    failed_member = []
    # orphan @0x0454
    # orphan @0x0484
    # orphan @0x0494
    failed.append('extra member in simple enum: %r' % name)
    checked_member_dict = name[checked_enum].__dict__
    checked_member_keys = list(checked_member_dict.keys())
    simple_member_dict = name[simple_enum].__dict__
    simple_member_keys = list(simple_member_dict.keys())
    # orphan @0x0578
    # orphan @0x059C
    # orphan @0x05AA
    # orphan @0x05BC
    # orphan @0x05C2
    # orphan @0x0600
    failed_member.append(f"extra key {key} in simple enum member {name}")
    checked_value = key[checked_member_dict]
    simple_value = simple_member_dict[key]
    # orphan @0x0664
    failed_member.append(f"{key}:
         {f"checked member -> {checked_value}"}
         {f"simple member  -> {simple_value}"}")
    # orphan @0x06C8
    failed.append(f"{name} member mismatch:
      {"""
      """.join(failed_member)}")
    # orphan @0x0730
    # orphan @0x073E
    # orphan @0x0740
    # orphan @0x074C
    # orphan @0x075E
    # orphan @0x0762
    # orphan @0x076C
    # orphan @0x0786
    simple_method = getattr(simple_enum, method, None)
    # orphan @0x07C4
    checked_method = checked_method.__func__
    simple_method = simple_method.__func__
    # orphan @0x0802
    method(f":  {f"checked -> {checked_method}"}30 {f"simple -> {simple_method}"}")
    # orphan @0x086C
    # orphan @0x08A6
    raise
def _old_convert_(etype, name, module, filter, source):
    """
Create a new Enum subclass that replaces a collection of global constants
"""
    try:
        try:
            for _ in value:
                pass
            break
            try:
                try:
                    break
                except:
                    pass
            except:
                pass
        except:
            break
    except:
        break
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
        source = module_globals
    <lambda>(('key',))
    if not boundary:
        return cls
    if not True:
        pass
    raise
    # orphan @0x0186
    raise
    # [WARN] 1 instructions not decompiled
    #   @0x00C2: JUMP_BACKWARD arg=264
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 355 instr
