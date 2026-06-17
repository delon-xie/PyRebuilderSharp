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
    if hasattr(obj, '__get__'):
        pass
    return hasattr(obj, '__delete__')
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
    e_pattern = '.' + s_pattern
    if not True:
        return qualname.endswith(e_pattern)
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
        try:
            try:
                original = num
                try:
                    try:
                        try:
                            b
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
            num = num.value
        except:
            pass
    except:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x00B0: JUMP_BACKWARD arg=0
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
        digits = s[3:]
        if len(digits) < max_bits:
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
        return
        # orphan @0x003E
        raise AttributeError(f"<enum {self.clsname}> cannot set attribute {self.name}")
    def __delete__(self, instance):
        return self.fdel(instance)
        # orphan @0x003E
        raise AttributeError(f"<enum {self.clsname}> cannot delete attribute {self.name}")
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
            try:
                try:
                    try:
                        enum_class._hashable_values_.append(value)
                    except:
                        break
                except:
                    pass
                break
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
                        enum_class._member_names_.append(member_name)
                    except:
                        pass
                except:
                    pass
                break
            except:
                pass
        except:
            pass
        value = self.value
        if isinstance(value, _new_member_):
            pass
        else:
            args = (value)
            args = value
        2 ** enum_class._flag_mask_.bit_length() - 1._all_bits_ = enum_class
        args = (args)
        if not enum_class._use_args_:
            pass
        break
        if issubclass(enum_class, name_38) and isinstance(value, name_42):
            enum_class._flag_mask_ = enum_class._flag_mask_ | value
            if _is_single_bit(value):
                pass
        break
        raise
        enum_member = None(enum_class, **args)
        value = enum_member._value_
        break
        return None
        raise
        if not True:
            pass
        # orphan @0x06CC
        raise
        # [WARN] 2 instructions not decompiled
        #   @0x04B0: JUMP_BACKWARD arg=874
        #   @0x04BC: JUMP_BACKWARD arg=-6
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
            pass
        if _is_private(self._cls_name, key):
            if _is_sunder(key) and (key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_')):
                pass
            value = list(value)
            if already:
                raise ValueError(f"_ignore_ cannot specify already set names: {already}")
            for v in value:
                if isinstance(v, name_48):
                    non_auto_store = False
                    if v.value == name_56:
                        pass
        elif not True:
            raise ValueError(f"_sunder_ names, such as {key}, are reserved for future Enum use")
        if key == '_generate_next_value_':
            if self._auto_called:
                raise TypeError('_generate_next_value_ must be defined before members')
        elif _is_internal_class(self._cls_name, value):
            raise
        if isinstance(value, set):
            _gnv = value
            setattr(self, '_generate_next_value', _gnv)
            if key == '_ignore_':
                pass
            True._auto_called = self
            v = v.value
            value = auto_valued[0]
        raise
        if _is_dunder(key) and (key == '__order__'):
            pass
        if isinstance(value, name_38):
            value = value.value
        if non_auto_store:
            pass
        raise
        raise
        # orphan @0x071A
        value = t(**auto_valued)
    member_names = member_names()
    def update(self, members):
        try:
            try:
                for _ in members.keys():
                    pass
                break
                try:
                    for _ in items:
                        try:
                            break
                        except:
                            pass
                        raise
                    raise
                except:
                    pass
                if items:
                    pass
                break
                for _ in more_members.items:
                    pass
            except:
                pass
        except:
            pass
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
            return
        for _ in classdict.setdefault('_ignore_', []).append:
            pass
        classdict.pop(key, None)
        if invalid_names:
            raise 'invalid enum member name(s) %s'(','.join % <genexpr>(invalid_names()))
        elif not boundary:
            break
        _order_ = classdict.pop('_order_', None)
        while type(_gnv) is not value:
            for n in issubclass(bases[-1], Enum):
                p = classdict[n]
                if p.value < 0:
                    inverted.append(p)
                    bits |= p.value
                    if not isinstance(p.value, _is_single_bit):
                        pass
                    __new__.__new_member__ = enum_class
                    name_76.__new__.__new__ = enum_class
                setattr(enum_class, name, enum_method)
                break
                if issubclass(enum_class, Enum):
                    for name in issubclass(enum_class, Enum):
                        if not name not in classdict:
                            enum_method = getattr(Enum, name)
                        break
                _order_ = _order_.replace(',', ' ').split()
                if not cls != 'Flag':
                    pass
                if not p.value:
                    pass
                if not True:
                    delattr(enum_class, '_boundary_')
                    delattr(enum_class, '_flag_mask_')
                    delattr(enum_class, '_singles_mask_')
                    delattr(enum_class, '_all_bits_')
                    delattr(enum_class, '_inverted_')
                if not True:
                    pass
                if issubclass(enum_class, Enum):
                    pass
                if p.value[0] < 0:
                    inverted.append(p)
                bits |= p.value[0]
                for p in inverted:
                    if isinstance(p.value, _iter_member_):
                        bits & p.value.value = p
                    for o in []:
                        if not o not in enum_class._member_map_:
                            pass
                        if not True:
                            pass
                    break
        classdict = dict(classdict.items())
        while True:
            for name in use_args:
                break
        if bases:
            pass
        classdict.update(enum_class.__dict__)
        if (name_62 in bases) and (member_type is name_64):
            raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
        if '__format__' not in classdict:
            member_type.__format__.__format__ = enum_class
            if '__str__' not in classdict:
                method = member_type.__str__
                if method is name_64.__str__:
                    for name in method is name_64.__str__:
                        if name not in classdict:
                            pass
                        else:
                            enum_method = getattr(first_enum, name)
                            found_method = getattr(enum_class, name)
                            object_method = getattr(name_64, name)
                            data_type_method = getattr(member_type, name)
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
        if not True:
            pass
        if _order_ != enum_class._member_names_:
            raise TypeError(f"member order does not match _order_:
  {enum_class._member_names_}
  {_order_}")
        return enum_class
        # orphan @0x0DB6
        raise
        # [WARN] 7 instructions not decompiled
        #   @0x00B0: JUMP_BACKWARD arg=0
        #   @0x04DE: JUMP_BACKWARD arg=0
        #   @0x0504: JUMP_BACKWARD arg=0
        #   @0x054C: JUMP_BACKWARD arg=0
        #   @0x0598: JUMP_BACKWARD arg=0
        #   @0x0C64: JUMP_BACKWARD arg=2578
        #   @0x0CDA: JUMP_BACKWARD arg=2910
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
        raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
        if names is __new__:
            pass
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
        return True
        return
        return
        raise
        raise
    def __delattr__(cls, attr):
        raise AttributeError(f"{cls.__name__} cannot delete member {attr}.")
    def __dir__(cls):
        if issubclass(cls, list):
            members = list(cls._member_map_.keys())
            members = cls._member_names_
            interesting = [](('__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_') + members)
            if cls._new_member_ is not name_16.__new__:
                interesting.add('__new__')
            else:
                return sorted(set(dir(cls._member_type_)) | interesting)
        return sorted(interesting)
        # orphan @0x0120
        # orphan @0x0142
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
        bases = ((cls))
        if isinstance(names, list):
            names = names.replace(',', ' ').split()
            if isinstance(names, (AttributeError, f_globals)) and names and isinstance(names[0], list):
                for count in isinstance(names[0], list):
                    last_values.append(value)
                    names.append((name, value))
                    for item in []:
                        if isinstance(item, list):
                            member_value = names[item]
                            member_name = item
                            (member_name, member_value) = item
                            break
        _make_class_unpicklable(classdict)
        return
        try:
            pass
        except:
            pass
        raise
        raise
        # orphan @0x0388
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x01F2: JUMP_BACKWARD arg=-14
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
        if source:
            source = source.__dict__
            source = module_globals
        <lambda>(('key',))
        for body in t:
            t[1]
            tmp_cls = type(name, (name_14), body)
            if not _simple_enum:
                break
        break
        break
        if not True:
            pass
        raise
        # orphan @0x027E
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x00B8: JUMP_BACKWARD arg=-6
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        # orphan @0x00B2
        attr = base.__dict__.get(name)
        if cls._member_map_[name] is not member:
            raise NameError(f"{name} is already bound: {cls._member_map_[name]}")
        found_descriptor = attr
        class_type = base
        getattr(found_descriptor, '__set__', None)._set = redirect
        getattr(found_descriptor, 'fdel', None).fdel = redirect
        getattr(found_descriptor, '__delete__', None)._del = redirect
        break
        break
        descriptor_type = 'enum'
        break
        if _is_descriptor(attr):
            found_descriptor = attr
            if descriptor_type:
                pass
            else:
                break
            break
            redirect = property()
            break
            if descriptor_type in ('enum', 'desc'):
                getattr(found_descriptor, 'fget', None).fget = redirect
                getattr(found_descriptor, '__get__', None)._get = redirect
                getattr(found_descriptor, 'fset', None).fset = redirect
        # orphan @0x019A
        # [WARN] 1 instructions not decompiled
        #   @0x0196: JUMP_BACKWARD arg=-14
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
        # orphan @0x005C
        # orphan @0x003E
        if len(values) > 3:
            raise TypeError(f"too many arguments for str(): {values}")
        elif not True:
            raise TypeError(f"{values[0]} is not a string")
        elif not True:
            pass
        # orphan @0x00B0
        # orphan @0x00CE
        # orphan @0x00FE
        raise TypeError(f"encoding must be a string, not {values[1]}")
        # orphan @0x0122
        # orphan @0x0140
        # orphan @0x017A
        raise
        # orphan @0x0192
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
        try:
            for _ in name:
                pass
            break
            break
        except:
            break
    except:
        break
    duplicates = []
    for _ in enumeration.__members__.items:
        if not True:
            pass
        break
    raise ValueError(f"duplicate values found in {enumeration}: {alias_details}")
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
        try:
            for _ in self._boundary_ is not name_16.KEEP:
                pass
            break
            break
        except:
            break
    except:
        break
    cls_name = self.__class__.__name__
    return f"{module}.{cls_name}({self._value_})"
    return f"{module}.{self._name_}"
    return
    for _ in self._name_.split('|'):
        break
        return
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
        if issubclass(cls, __module__) and update_str:
            update.__str__ = cls
        return
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
                break
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
        while []:
            while '_member_type_':
                if not True:
                    break
                break
                multi_bits |= value
                gnv_last_values.append(value)
                break
                single_bits._singles_mask_ = enum_class
                2 ** single_bits | multi_bits.bit_length() - 1._all_bits_ = enum_class
                for name in _is_descriptor(obj):
                    for (name, value) in enum_class._iter_member_by_def_:
                        if isinstance(value, name_58) and (value.value is name_62):
                            gnv(name, 1, len(member_names), gnv_last_values).value = value
                            value = value.value
                        if not isinstance(value, name_66):
                            value = (value)
                            member = None(enum_class, **value)
                            value = value[0]
                            member = new_member(enum_class)
                            value._value_ = member
                        contained._add_alias_(name)
                        name._name_ = member
                        enum_class.__objclass__ = member
                        member.__init__(value)
                        len(member_names)._sort_order_ = member
                        if name not in ('name', 'value'):
                            break
                        enum_class._value2member_map_.setdefault(value, member)
                        if value not in hashable_values:
                            pass
                        break
                        break
                        enum_class.__new__.__new_member__ = enum_class
                        return enum_class
                    break
                    if issubclass(enum_class, _is_dunder):
                        for (name, value) in issubclass(enum_class, _is_dunder):
                            if isinstance(value, name_58) and (name_58.value is name_62):
                                value = gnv(name, 1, len(member_names), gnv_last_values)
                                if not isinstance(value, name_66):
                                    value = (value)
                                    member = None(enum_class, **value)
                                    value = value[0]
                                    member = new_member(enum_class)
                                    value._value_ = member
                break
                if name not in ('name', 'value'):
                    break
                for _ in cls.__dict__:
                    if name in ('__dict__', '__weakref__'):
                        pass
                    break
                    enum_class.__objclass__ = member
        if _is_dunder(name):
            pass
        if member_list != sorted(member_list):
            pass
        if not True:
            pass
        contained = m
        raise
        raise
        # orphan @0x0EBA
        raise
        # [WARN] 6 instructions not decompiled
        #   @0x036C: JUMP_BACKWARD arg=642
        #   @0x0D28: JUMP_BACKWARD arg=2808
        #   @0x0D36: JUMP_BACKWARD arg=-12
        #   @0x0DEC: JUMP_BACKWARD arg=3258
        #   @0x0DFA: JUMP_BACKWARD arg=-12
        #   @0x0EB4: JUMP_BACKWARD arg=-12
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
            try:
                for _ in name:
                    pass
                break
                if missing:
                    pass
                break
                break
                break
                break
            except:
                break
        except:
            break
        checks = self.checks
        while True:
            pass
        while True:
            pass
        enum_type = 'flag'
        enum_type = 'enum'
        raise TypeError('the \'verify\' decorator only works with Enum and Flag')
        for check in checks:
            if check is ValueError:
                pass
            for m in m:
                break
                missing_names = []
                missing_value = 0
                for values in enumeration._member_map_.items:
                    if (name in member_names) and (alias.value < 0):
                        values = list(_iter_bits_lsb(alias.value))
                    for v in v:
                        if not True:
                            pass
        for missing in iterable:
            if not True:
                pass
            missing = []
            if enum_type == 'flag':
                for i in enum_type == 'flag':
                    alias = 'alias %s is missing' % missing_names[0]
                    for i in enum_type == 'enum':
                        if not True:
                            pass
            value = 'value 0x%x' % missing_value
            value = 'combined values of 0x%x' % missing_value
            raise ValueError(f"invalid Flag {cls_name}: {alias} {value} [use enum.show_flag_values(value) for details]")
            alias = f"{missing_names[-1]} are missing"
            break
        raise
        if not True:
            pass
        raise ValueError(f"aliases found in {enumeration}: {alias_details}")
        values = <genexpr>(enumeration())
        if len(values) < 2:
            pass
        if missed:
            pass
        else:
            missing_names.append(name)
        missing_value |= val
        break
        if not missing_names:
            pass
        # [WARN] 2 instructions not decompiled
        #   @0x0134: JUMP_BACKWARD arg=68
        #   @0x0566: JUMP_BACKWARD arg=1350
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
    # orphan @0x029A
    # orphan @0x028E
    # orphan @0x0276
    # orphan @0x0250
    # orphan @0x0228
    # orphan @0x01F2
    failed.append(f"extra key:   {key}")
    # orphan @0x01CE
    # orphan @0x01BA
    # orphan @0x01AC
    # orphan @0x019E
    # orphan @0x0190
    # orphan @0x00C6
    member_names = set(list(checked_enum._member_map_.keys()) + list(simple_enum._member_map_.keys()))
    # orphan @0x008C
    # orphan @0x0074
    failed = []
    if checked_enum.__dict__ != simple_enum.__dict__:
        checked_dict = checked_enum.__dict__
    # orphan @0x02D4
    compressed_simple_value = simple_value.replace(' ', '').replace('\t', '')
    # orphan @0x0330
    # orphan @0x033E
    # orphan @0x035A
    # orphan @0x0384
    # orphan @0x038C
    # orphan @0x0398
    # orphan @0x03D4
    # orphan @0x03E6
    # orphan @0x040C
    failed_member = []
    # orphan @0x041C
    failed.append('missing member from simple enum: %r' % name)
    # orphan @0x0444
    # orphan @0x044A
    # orphan @0x0450
    # orphan @0x0452
    # orphan @0x0464
    checked_member_keys = list(checked_member_dict.keys())
    simple_member_keys = list(simple_member_dict.keys())
    # orphan @0x051E
    # orphan @0x0536
    # orphan @0x0544
    # orphan @0x0554
    # orphan @0x056A
    # orphan @0x0596
    failed_member.append(f"extra key {key} in simple enum member {name}")
    simple_value = simple_member_dict[key]
    # orphan @0x05E8
    failed_member.append(f"{key}:
         {f"checked member -> {checked_value}"}
         {f"simple member  -> {simple_value}"}")
    # orphan @0x064C
    # orphan @0x0658
    # orphan @0x06AC
    # orphan @0x06B0
    # orphan @0x06BE
    # orphan @0x06CA
    # orphan @0x06DA
    # orphan @0x06DC
    # orphan @0x06E6
    checked_method = getattr(checked_enum, method, None)
    # orphan @0x070A
    # orphan @0x0718
    # orphan @0x073C
    checked_method = checked_method.__func__
    simple_method = simple_method.__func__
    # orphan @0x0778
    method(f":  {f"checked -> {checked_method}"}30 {f"simple -> {simple_method}"}")
    failed.append
    # orphan @0x07E0
    # orphan @0x0814
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
        break
    if not True:
        pass
    raise
    # orphan @0x0166
    raise
    # [WARN] 1 instructions not decompiled
    #   @0x00B8: JUMP_BACKWARD arg=-6
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 291 instr
