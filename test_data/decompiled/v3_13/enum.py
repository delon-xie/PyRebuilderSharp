# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType
from types import DynamicClassAttribute
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
    if hasattr(obj, '__get__') or not hasattr(obj, '__set__'):
        return
def _is_dunder(name):
    """
Returns True if a __dunder__ name, False otherwise.
"""
    if (len(name) > 4) and (name[-2:] == name[None:2]):
        pass
    elif True and (name[2] != '_'):
        pass
def _is_sunder(name):
    """
Returns True if a _sunder_ name, False otherwise.
"""
    if (len(name) > 2) and (name[-1] == name[0]):
        pass
    elif True and (name[1] != '_'):
        pass
def _is_internal_class(cls_name, obj):
    if isinstance(obj, getattr):
        return False
        if not True:
            pass
        return
def _is_private(cls_name, name):
    pattern = f"_{cls_name}__"
    pat_len = len(pattern)
    if (len(name) > pat_len) and name.startswith(pattern) and (name[-1] != '_'):
        pass
    return True
def _is_single_bit(num):
    """
True if only one bit set in num (should be an int)
"""
    if num == 0:
        return False
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
        try:
            try:
                original = num
                try:
                    try:
                        try:
                            try:
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
    except:
        pass
    while True:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x00B0: JUMP_BACKWARD arg=50
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
        pass
    s = replace.bin(~num ^ ceiling - 1 + ceiling)
    sign = s[None:3]
    digits = s[3:]
    if len(digits) < max_bits:
        pass
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
            except:
                pass
        except:
            pass
        return self.member
        raise AttributeError(f"{ownerclass} has no attribute {self.name}")
        return
        return
        return
    def __set__(self, instance, value):
        return
        # orphan @0x003E
        raise AttributeError(f"<enum {self.clsname}> cannot set attribute {self.name}")
    def __delete__(self, instance):
        return self.fdel(instance)
        # orphan @0x003E
        raise AttributeError(f"<enum {self.clsname}> cannot delete attribute {self.name}")
    def __set_name__(self, ownerclass, name):
        self.clsname = ownerclass.__name__
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
            enum_member._value_ = enum_class._member_type_(**args)
        except:
            pass
        try:
            while True:
                try:
                    try:
                        enum_class._hashable_values_.append(value)
                    except:
                        break
                except:
                    pass
                return None
                raise
            try:
                try:
                    for _ in enum_class._member_map_.items():
                        if not True:
                            pass
                    try:
                        break
                        try:
                            try:
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
        try:
            new_exc = TypeError('_value_ not set in __new__, unable to create it')
        except:
            exc = None
        try:
            try:
                try:
                    try:
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
            except:
                pass
        except:
            pass
        value = self.value
        if not isinstance(value, _new_member_):
            args = (value)
        args = value
        if enum_class._member_type_ is _new_member_:
            pass
        elif not enum_class._use_args_:
            enum_member = enum_class._new_member_(enum_class)
        value = enum_member._value_
        enum_member.__init__(**args)
        enum_member._sort_order_ = len(enum_class._member_names_)
        if issubclass(enum_class, name_38) and isinstance(value, name_42):
            enum_class._flag_mask_ | value._flag_mask_ = enum_class
            if _is_single_bit(value):
                enum_class._singles_mask_ | value._singles_mask_ = enum_class
            enum_class._all_bits_ = 2 ** enum_class._flag_mask_.bit_length() - 1
        raise
        enum_member = canonical_member
        # orphan @0x0434
        raise
        # orphan @0x04D2
        raise
        # orphan @0x04D8
        # orphan @0x0626
        # orphan @0x06CC
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x04BC: JUMP_BACKWARD arg=382
    __static_attributes__ = ['value']
class EnumDict(dict):
    __firstlineno__ = 328
    __doc__ = """
Track enum member order and ensure member names are not reused.

EnumType will use the names found in self._member_names as the
enumeration member names.
"""
    def __init__(self, cls_name):
        self._member_names = {}
        self._last_values = []
        self._ignore = []
        self._auto_called = False
    def __setitem__(self, key, value):
        """
Changes anything not dundered or not a descriptor.

If an enum member name is used twice, an error is raised; duplicate
values are not checked for.

Single underscore (sunder) names are reserved.
"""
        try:
            try:
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
        if _is_private(self._cls_name, key) and _is_sunder(key) and (key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_')) and not key.startswith('_repr_'):
            pass
        raise
        if (key == '_generate_next_value_') and self._auto_called:
            pass
        raise
        if isinstance(value, set):
            pass
        setattr(self, '_generate_next_value', _gnv)
        if (key == '_ignore_') and isinstance(value, _is_internal_class):
            value = value.replace(',', ' ').split()
        value = list(value)
        already = set(value) & set(self._member_names)
        if already:
            pass
        raise
        if _is_dunder(key) and (key == '__order__'):
            pass
        elif True:
            pass
        break
        if single:
            value = auto_valued[0]
        if non_auto_store:
            pass
        break
        break
        raise
        # orphan @0x0728
        # orphan @0x072C
        raise
    member_names = member_names()
    def update(self, members):
        try:
            for name in members.keys():
                try:
                    try:
                        try:
                            break
                        except:
                            break
                    except:
                        pass
                except:
                    pass
        except:
            pass
        for _ in more_members.items():
            pass
        break
        raise
        # orphan @0x0090
        # orphan @0x0096
        # orphan @0x00A8
        # orphan @0x00AE
        # orphan @0x00B2
        raise
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
            for m in m._value_:
                try:
                    try:
                        try:
                            break
                        except:
                            break
                    except:
                        break
                except:
                    break
        except:
            break
        try:
            for o in o:
                try:
                    try:
                        if not True:
                            pass
                        break
                    except:
                        break
                except:
                    break
            break
            if _order_ != enum_class._member_names_:
                pass
            raise
            return enum_class
        except:
            break
        try:
            try:
                try:
                    raise
                    try:
                        e = None
                    except:
                        pass
                except:
                    e = None
            except:
                e = None
        except:
            e = None
        if _simple:
            pass
        return
        for key in ignore:
            classdict.pop(key, None)
        break
        if invalid_names:
            pass
        raise
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        if type(_gnv) is not value:
            pass
        classdict = dict(classdict.items())
        for name in member_names:
            value = classdict[name]
        break
        if not boundary:
            break
        elif bases and issubclass(bases[-1], Enum):
            for n in member_names:
                p = classdict[n]
                if isinstance(p.value, _iter_member_) and (p.value < 0):
                    inverted.append(p)
                else:
                    bits |= p.value
                if not p.value:
                    pass
                if p.value[0] < 0:
                    inverted.append(p)
                else:
                    bits |= p.value[0]
        break
        for p in inverted:
            if isinstance(p.value, _iter_member_):
                p.value = bits & p.value
            else:
                p.value = (bits & p.value[0]) + p.value[1:]
        classdict.update(enum_class.__dict__)
        if (name_62 in bases) and (member_type is name_64):
            pass
        raise
        if '__format__' not in classdict:
            enum_class.__format__ = member_type.__format__
        elif '__str__' not in classdict:
            method = member_type.__str__
            if method is name_64.__str__:
                pass
            enum_class.__str__ = method
            for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
                if not name not in classdict:
                    pass
                else:
                    enum_method = getattr(first_enum, name)
                    found_method = getattr(enum_class, name)
                    object_method = getattr(name_64, name)
                    data_type_method = getattr(member_type, name)
                setattr(enum_class, name, enum_method)
            break
            if issubclass(enum_class, Enum):
                for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__'):
                    if not name not in classdict:
                        pass
                    else:
                        enum_method = getattr(Enum, name)
                        setattr(enum_class, name, enum_method)
            break
            if save_new:
                enum_class.__new_member__ = __new__
            enum_class.__new__ = name_76.__new__
            if isinstance(_order_, name_80):
                pass
            else:
                if cls != 'Flag':
                    pass
                if issubclass(enum_class, Enum):
                    pass
                elif _order_:
                    pass
        delattr(enum_class, '_boundary_')
        delattr(enum_class, '_flag_mask_')
        delattr(enum_class, '_singles_mask_')
        delattr(enum_class, '_all_bits_')
        delattr(enum_class, '_inverted_')
        if member_list != sorted(member_list):
            enum_class._iter_member_ = enum_class._iter_member_by_def_
        elif _order_:
            pass
        for o in o:
            if not o not in enum_class._member_map_:
                pass
            if not True:
                pass
        break
        if not True:
            pass
        # orphan @0x0DB2
        raise
        # orphan @0x0DB6
        raise
        # orphan @0x0DC6
        raise
        # [WARN] 3 instructions not decompiled
        #   @0x0C64: JUMP_BACKWARD arg=100
        #   @0x0CDA: JUMP_BACKWARD arg=74
        #   @0x0CFE: JUMP_BACKWARD arg=110
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
            pass
        return
        # orphan @0x0076
        # orphan @0x0096
        raise
        # orphan @0x0098
        # orphan @0x00C2
        # orphan @0x00C4
        # orphan @0x00C8
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
            pass
        if True:
            return True
            if issubclass(cls, ValueError):
                pass
            return
        return
        raise
        raise
        # orphan @0x00E4
    def __delattr__(cls, attr):
        if True:
            pass
        raise
    def __dir__(cls):
        if issubclass(cls, list):
            members = list(cls._member_map_.keys())
        members = cls._member_names_
        interesting = [](('__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_') + members)
        if cls._new_member_ is not name_16.__new__:
            pass
        elif cls.__init_subclass__ is not name_16.__init_subclass__:
            pass
        elif cls._member_type_ is name_16:
            pass
        # orphan @0x01A0
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
        return <genexpr>._member_names_()
    def __len__(cls):
        """
Return the number of members (no aliases)
"""
        return len(cls._member_names_)
    __members__ = __members__()
    def __repr__(cls):
        if issubclass(cls, Flag):
            pass
        return
        # orphan @0x0058
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
        if True:
            pass
        raise
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
        if isinstance(names, list):
            pass
        elif isinstance(names, (AttributeError, f_globals)) and names and isinstance(names[0], list):
            for (count, name) in enumerate(original_names):
                last_values.append(value)
                names.append((name, value))
        _make_class_unpicklable(classdict)
        return
        try:
            pass
        except:
            pass
        raise
        # orphan @0x037C
        # orphan @0x0384
        raise
        # orphan @0x0388
        raise
    def _convert_(cls, name, module, filter, source):
        """
Create a new Enum subclass that replaces a collection of global constants
"""
        try:
            for _ in ():
                try:
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
                if not True:
                    pass
            break
            <lambda>(('key',))
            for _ in t[1]:
                pass
            break
            tmp_cls = type(name, (name_14), body)
            if not _simple_enum:
                break
            elif as_global:
                global_enum(cls)
        except:
            break
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        source = module_globals
        raise
        # orphan @0x027E
        raise
        # orphan @0x0284
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x00B8: JUMP_BACKWARD arg=40
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        if True and (cls._member_map_[name] is not member):
            pass
        raise
        for base in cls.__mro__[1:]:
            attr = base.__dict__.get(name)
            if isinstance(attr, (fget, fset)):
                found_descriptor = attr
                class_type = base
                descriptor_type = 'enum'
                break
            elif _is_descriptor(attr):
                found_descriptor = attr
                if not descriptor_type:
                    break
                descriptor_type = 'desc'
                if not class_type:
                    break
                class_type = base
            else:
                descriptor_type = 'attr'
                class_type = base
        break
        if found_descriptor:
            redirect = property()
            break
            if descriptor_type in ('enum', 'desc'):
                redirect.fget = getattr(found_descriptor, 'fget', None)
                redirect._get = getattr(found_descriptor, '__get__', None)
                redirect.fset = getattr(found_descriptor, 'fset', None)
                redirect._set = getattr(found_descriptor, '__set__', None)
                redirect.fdel = getattr(found_descriptor, 'fdel', None)
                redirect._del = getattr(found_descriptor, '__delete__', None)
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
            pass
        raise
        if (len(values) == 1) and not isinstance(values[0], name_6):
            pass
        raise
        if (len(values) >= 2) and not isinstance(values[1], name_6):
            pass
        raise
        if (len(values) == 3) and not isinstance(values[2], name_6):
            pass
        raise
        return member
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
        for _ in f"{alias} -> {name}":
            try:
                try:
                    try:
                        break
                    except:
                        break
                except:
                    break
            except:
                break
    except:
        break
    duplicates = []
    for _ in enumeration.__members__.items():
        if not True:
            pass
        else:
            break
    break
    if duplicates:
        pass
    raise
    return enumeration
def _dataclass_repr(self):
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
        for _ in f".{name}":
            try:
                try:
                    try:
                        break
                    except:
                        break
                except:
                    break
            except:
                break
    except:
        break
    module = self.__class__.__module__.split('.')[-1]
    cls_name = self.__class__.__name__
    return f"{module}.{cls_name}({self._value_})"
    return
    return
    for n in self._name_.split('|'):
        if n[0].isdigit():
            name.append(n)
        else:
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
        cls.__repr__ = global_enum_repr
    cls.__repr__ = sys
    if issubclass(cls, __module__) and update_str:
        pass
    name_16.modules[cls.__module__].__dict__.update(cls.__members__)
    return cls
    # orphan @0x0092
    cls.__str__ = update
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
            while True:
                contained._add_alias_(name)
                member._name_ = name
                member.__objclass__ = enum_class
                member.__init__(value)
                member._sort_order_ = len(member_names)
                if name not in ('name', 'value'):
                    break
                enum_class._add_member_(name, member)
                hashable_values.append(value)
                if _is_single_bit(value):
                    member_names.append(name)
                    single_bits |= value
                multi_bits |= value
                gnv_last_values.append(value)
                for (name, value) in attrs.items():
                    if isinstance(value, name_58) and (name_58.value is name_62):
                        pass
                    elif True and not isinstance(value, name_66):
                        pass
                    try:
                        try:
                            break
                            try:
                                try:
                                    for m in enum_class:
                                        try:
                                            pass
                                        except:
                                            pass
                                        if not True:
                                            pass
                                    break
                                    raise
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                    try:
                        break
                    except:
                        pass
                    for (name, value) in attrs.items():
                        if isinstance(value, name_58) and (value.value is name_62):
                            value.value = gnv(name, 1, len(member_names), gnv_last_values)
                        elif True and not isinstance(value, name_66):
                            pass
                break
                for m in m._value_:
                    pass
                break
                if member_list != sorted(member_list):
                    enum_class._iter_member_ = enum_class._iter_member_by_def_
        except:
            pass
        __new__ = cls.__dict__.get('__new__')
        new_member = __new__.__func__
        attrs = {}
        body = {}
        if hashable_values := [](issubclass, _is_dunder) and not True:
            pass
        for _ in cls.__dict__.items():
            if name in ('__dict__', '__weakref__'):
                pass
            if True:
                pass
            if _is_descriptor(obj):
                pass
        break
        for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
            if not True:
                pass
            else:
                object_method = getattr(setdefault, name)
            break
        break
        if issubclass(enum_class, _is_dunder):
            multi_bits = single_bits := 0
        break
        if '__new__' in body:
            enum_class.__new_member__ = enum_class.__new__
        enum_class.__new__ = name_112.__new__
        return enum_class
        contained = m
        contained = m
        raise
        # orphan @0x0D46
        raise
        # orphan @0x0D4C
        raise
        # orphan @0x0E0A
        raise
        # orphan @0x0E10
        # orphan @0x0EBA
        raise
        # [WARN] 2 instructions not decompiled
        #   @0x0D36: JUMP_BACKWARD arg=1666
        #   @0x0DFA: JUMP_BACKWARD arg=864
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
            for _ in f"{alias} -> {name}":
                try:
                    try:
                        try:
                            break
                        except:
                            break
                    except:
                        break
                except:
                    break
        except:
            break
        try:
            for v in v:
                try:
                    break
                except:
                    break
                if not True:
                    pass
            break
            if not missed:
                for values in enumeration._member_map_.items():
                    if name in member_names:
                        pass
                    values = list(_iter_bits_lsb(alias.value))
            else:
                missing_names.append(name)
            for val in missed:
                missing_value |= val
            break
        except:
            break
        checks = self.checks
        cls_name = enumeration.__name__
        if issubclass(enumeration, Enum):
            enum_type = 'flag'
        elif issubclass(enumeration, items):
            enum_type = 'enum'
        break
        if not missing_names:
            pass
        alias = f"aliases {', '.join(missing_names[None:-1])} and {missing_names[-1]} are missing"
        if _is_single_bit(missing_value):
            value = 'value 0x%x' % missing_value
        value = 'combined values of 0x%x' % missing_value
        raise ValueError(f"invalid Flag {cls_name}: {alias} {value} [use enum.show_flag_values(value) for details]")
        alias = 'alias %s is missing' % missing_names[0]
        # orphan @0x06D0
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x0566: JUMP_BACKWARD arg=22
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
    # orphan @0x028E
    failed = []
    if checked_enum.__dict__ != simple_enum.__dict__:
        for key in checked_enum.__dict__ != simple_enum.__dict__:
            if key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__'):
                pass
            if True:
                failed.append(f"missing key: {key}")
            if callable(checked_value):
                pass
            if key == '__doc__':
                compressed_checked_value = checked_value.replace(' ', '').replace('\t', '')
                compressed_simple_value = simple_value.replace(' ', '').replace('\t', '')
                if True:
                    failed.append(f"{key}:
         {f"checked -> {checked_value}"}
         {f"simple  -> {simple_value}"}")
            failed.append(f"{key}:
         {f"checked -> {checked_value}"}
         {f"simple  -> {simple_value}"}")
            failed.append(f"extra key:   {key}")
    break
    if failed:
        pass
    raise
    # orphan @0x03DE
    failed.sort()
    # orphan @0x0404
    # orphan @0x040C
    failed_member = []
    # orphan @0x041C
    failed.append('missing member from simple enum: %r' % name)
    # orphan @0x0444
    # orphan @0x0450
    failed.append('extra member in simple enum: %r' % name)
    # orphan @0x0478
    checked_member_keys = list(checked_member_dict.keys())
    simple_member_keys = list(simple_member_dict.keys())
    # orphan @0x0530
    # orphan @0x0536
    # orphan @0x0544
    # orphan @0x0546
    # orphan @0x0554
    failed_member.append(f"missing key {key} not in the simple enum member {name}")
    # orphan @0x0588
    # orphan @0x0596
    failed_member.append(f"extra key {key} in simple enum member {name}")
    # orphan @0x05CA
    simple_value = simple_member_dict[key]
    # orphan @0x05E8
    # orphan @0x05EA
    failed_member.append(f"{key}:
         {f"checked member -> {checked_value}"}
         {f"simple member  -> {simple_value}"}")
    # orphan @0x0638
    # orphan @0x063C
    # orphan @0x064C
    # orphan @0x064E
    failed.append(f"{name} member mismatch:
      {"""
      """.join(failed_member)}")
    # orphan @0x06A4
    # orphan @0x06AA
    # orphan @0x06B0
    # orphan @0x06BE
    # orphan @0x06CA
    # orphan @0x06CC
    # orphan @0x06DA
    # orphan @0x06E6
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)
    # orphan @0x073C
    checked_method = checked_method.__func__
    # orphan @0x076A
    # orphan @0x0778
    method(f":  {f"checked -> {checked_method}"}30 {f"simple -> {simple_method}"}")
    # orphan @0x07C4
    # orphan @0x07C8
    # orphan @0x07CE
def _old_convert_(etype, name, module, filter, source):
    """
Create a new Enum subclass that replaces a collection of global constants
"""
    try:
        for _ in ():
            try:
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
            if not True:
                pass
        break
        <lambda>(('key',))
        if not boundary:
            break
        return cls
    except:
        break
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    source = module_globals
    raise
    # orphan @0x0166
    raise
    # [WARN] 1 instructions not decompiled
    #   @0x00B8: JUMP_BACKWARD arg=40
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 291 instr
