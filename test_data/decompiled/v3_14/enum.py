# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType, DynamicClassAttribute
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
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')
def _is_dunder(name):
    """
Returns True if a __dunder__ name, False otherwise.
"""
    if (len(name) > 4) and (name[-2:] == name[:2]):
        pass
    if name[2] != '_':
        name[-3] != '_'
    return
def _is_sunder(name):
    """
Returns True if a _sunder_ name, False otherwise.
"""
    if (len(name) > 2) and (name[-1] == name[0]):
        pass
    if name[1] != '_':
        name[-2] != '_'
    return
def _is_internal_class(cls_name, obj):
    if not isinstance(obj, getattr):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if not s_pattern == qualname:
        qualname.endswith(e_pattern)
    return
def _is_private(cls_name, name):
    """_"""
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
    if isinstance(obj, setattr):
        return None
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
                        while num:
                            pass
                        try:
                            try:
                                b = num & ~num + 1
                                b
                                num = b ^ num
                            except:
                                pass
                            return None
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
    #   @0x00C8: JUMP_BACKWARD arg=128
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
    else:
        s = replace.bin(~num ^ ceiling - 1 + ceiling)
    sign = s[:3]
    digits = s[3:]
    if len(digits) < max_bits:
        digits = sign[-1] * max_bits + digits[-max_bits:]
    return f"{sign} {digits}"
class _not_given:
    __firstlineno__ = 155
    def __repr__(self):
        """<not given>"""
        return '<not given>'
    __static_attributes__ = []
    __classdictcell__ = __classdict__
_not_given = _not_given()
class _auto_null:
    __firstlineno__ = 160
    def __repr__(self):
        """_auto_null"""
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
        """auto(%r)"""
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
            ownerclass._member_map_[self.name]
        except:
            pass
        return self.member
        raise AttributeError(f"{ownerclass} has no attribute {self.name}")
        return getattr(self._cls_type, self.name)
        if self._attr_type == 'desc':
            return getattr(instance._value_, self.name)
        return
        # orphan @0x0206
    def __set__(self, instance, value):
        return self.fset(value, instance)
        # orphan @0x0040
    def __delete__(self, instance):
        return self.fdel(instance)
        # orphan @0x0040
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
            enum_class._member_type_
        except:
            pass
        try:
            enum_member = enum_class._value2member_map_[value]
        except:
            enum_class._member_map_.items()
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
            break
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
        delattr(member_name, enum_class)
        value = self.value
        if not isinstance(value, _new_member_):
            args = (value)
        else:
            args = value
        if enum_class._member_type_ is _new_member_:
            args = (args)
        else:
            if not enum_class._use_args_:
                enum_member = enum_class._new_member_(enum_class)
            else:
                enum_member = [enum_class](**None)
                None
                enum_class._new_member_
            if hasattr(enum_member, '_value_'):
                value = enum_member._value_
                enum_member._name_ = member_name
                enum_member.__objclass__ = enum_class
                None(**None)
                len(enum_class._member_names_)._sort_order_ = enum_member
                if issubclass(enum_class, name_38) and isinstance(value, name_42):
                    enum_class._flag_mask_ = enum_class._flag_mask_ | value
                    if _is_single_bit(value):
                        enum_class._singles_mask_ = enum_class._singles_mask_ | value
                    2 ** enum_class._flag_mask_.bit_length() - 1._all_bits_ = enum_class
        break
        raise
        if not True:
            pass
        # orphan @0x047E
        # orphan @0x051C
        # orphan @0x0728
        # orphan @0x072A
        # [WARN] 2 instructions not decompiled
        #   @0x04FC: JUMP_BACKWARD arg=1232
        #   @0x0508: JUMP_BACKWARD arg=898
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
            pass
        if _is_dunder(key):
            if key == '__order__':
                key = '_order_'
            break
        elif self in key._member_names:
            raise TypeError(f"{key} already defined as {key[self]}")
        else:
            if self in key._ignore:
                pass
            if _is_descriptor(value):
                pass
            if self in key:
                raise TypeError(f"{key} already defined as {key[self]}")
            elif isinstance(value, name_46):
                value = value.value
        if (key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_')) and not key.startswith('_repr_'):
            raise ValueError(f"_sunder_ names, such as {key}, are reserved for future Enum use")
        else:
            if (key == '_generate_next_value_') and self._auto_called:
                raise TypeError('_generate_next_value_ must be defined before members')
            elif isinstance(value, set):
                pass
            else:
                value
            if isinstance(value, _is_internal_class):
                value = value.replace(',', ' ').split()
            else:
                value = list(value)
        # orphan @0x07D6
        # orphan @0x07D8
        # [WARN] 2 instructions not decompiled
        #   @0x053C: JUMP_BACKWARD arg=1322
        #   @0x06EC: JUMP_BACKWARD arg=1428
    member_names = member_names()
    def update(self, members):
        try:
            members.keys()
            for name in members.keys():
                try:
                    try:
                        members.keys()
                        more_members.items()
                        for _ in more_members.items():
                            pass
                        return None
                        try:
                            try:
                                break
                                for _ in members:
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
        except:
            pass
        # orphan @0x00BC
        # orphan @0x00BE
        # [WARN] 3 instructions not decompiled
        #   @0x003E: JUMP_BACKWARD arg=36
        #   @0x0078: JUMP_BACKWARD arg=102
        #   @0x00B0: JUMP_BACKWARD arg=158
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
        """_ignore_"""
        try:
            enum_class = None(cls, metacls, classdict, bases, **kwds)
            delattr(enum_class, '_%s__in_progress' % cls)
        except:
            pass
        try:
            []
            for m in []:
                try:
                    try:
                        []
                        if member_list != sorted(member_list):
                            enum_class._iter_member_by_def_._iter_member_ = enum_class
                        elif _order_:
                            o
                            _order_
                        elif _order_:
                            o
                            _order_
                        break
                        break
                        break
                    except:
                        break
                except:
                    break
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
                __notes__
            except:
                e = None
        except:
            e = None
        if _simple:
            return None(cls, metacls, classdict, bases, **kwds)
        classdict.setdefault('_ignore_', []).append('_ignore_')
        ignore = classdict['_ignore_']
        ignore
        for key in ignore:
            classdict.pop(key, None)
        member_names = classdict._member_names
        invalid_names = set(member_names) & {'mro', ''}
        if invalid_names:
            raise 'invalid enum member name(s) %s'(','.join % <genexpr>(invalid_names()))
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        if type(_gnv) is not value:
            _gnv = staticmethod(_gnv)
        classdict = dict(classdict.items())
        (__new__, save_new, use_args) = metacls._find_new_(member_type, classdict, first_enum)
        member_names
        *metacls._get_mixins_(bases, cls)
        *metacls._get_mixins_(bases, cls)
        for name in member_names:
            value = classdict[name]
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
        inverted
        for p in inverted:
            if isinstance(p.value, _iter_member_):
                bits & p.value.value = p
            else:
                (bits & p.value[0]) + p.value[1:].value = p
        classdict.update(enum_class.__dict__)
        if (name_62 in bases) and (member_type is name_64):
            raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
        elif '__format__' not in classdict:
            member_type.__format__.__format__ = enum_class
        elif '__str__' not in classdict:
            method = member_type.__str__
            if method is name_64.__str__:
                method = member_type.__repr__
            method.__str__ = enum_class
            ('__repr__', '__str__', '__format__', '__reduce_ex__')
            for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
                if not name not in classdict:
                    pass
                else:
                    enum_method = getattr(first_enum, name)
                    found_method = getattr(enum_class, name)
                    object_method = getattr(name_64, name)
                    data_type_method = getattr(member_type, name)
                setattr(enum_class, name, enum_method)
            if issubclass(enum_class, Enum):
                for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__'):
                    if not name not in classdict:
                        pass
                    else:
                        enum_method = getattr(Enum, name)
                        setattr(enum_class, name, enum_method)
            elif save_new:
                __new__.__new_member__ = enum_class
        []
        for o in []:
            if not o not in enum_class._member_map_:
                _is_single_bit(enum_class[o]._value_)
            if not True:
                pass
        []
        for o in []:
            if not o not in enum_class._member_map_:
                o in enum_class._member_map_
            if not True:
                pass
            else:
                o in enum_class._member_names_
            if not True:
                pass
        if _order_ != enum_class._member_names_:
            raise TypeError(f"member order does not match _order_:
  {enum_class._member_names_}
  {_order_}")
        # orphan @0x0EB6
        # orphan @0x0EB8
        # [WARN] 22 instructions not decompiled
        #   @0x00BA: JUMP_BACKWARD arg=144
        #   @0x02CA: JUMP_BACKWARD arg=662
        #   @0x04A4: JUMP_BACKWARD arg=1030
        #   @0x04CE: JUMP_BACKWARD arg=1030
        #   @0x0532: JUMP_BACKWARD arg=1030
        #   @0x055A: JUMP_BACKWARD arg=1030
        #   @0x05AC: JUMP_BACKWARD arg=1030
        #   @0x0604: JUMP_BACKWARD arg=1030
        #   @0x063E: JUMP_BACKWARD arg=1030
        #   @0x06C0: JUMP_BACKWARD arg=1610
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
        if cls._member_map_:
            if names is not __new__:
                value = (names, value) + values
            return cls.__new__(value, cls)
        elif names is __new__:
            raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
        elif names is __new__:
            pass
        else:
            names
    def __contains__(cls, value):
        """Return True if `value` is in `cls`.

`value` is in `cls` if:
1) `value` is a member of `cls`, or
2) `value` is the value of one of the `cls`'s members.
3) `value` is a pseudo-member (flags)
"""
        try:
            result = cls._missing_(value)
            isinstance(cls, result)
        except:
            pass
        if isinstance(cls, value):
            return True
        elif issubclass(cls, ValueError):
            pass
        return
        # orphan @0x00F0
        # orphan @0x00F2
    def __delattr__(cls, attr):
        """ cannot delete member """
        if cls in attr._member_map_:
            raise AttributeError(f"{cls.__name__} cannot delete member {attr}.")
    def __dir__(cls):
        """__class__"""
        if issubclass(cls, list):
            members = list(cls._member_map_.keys())
        else:
            members = cls._member_names_
        interesting = [](('__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_') + members)
        if cls._new_member_ is not name_16.__new__:
            interesting.add('__new__')
        elif cls.__init_subclass__ is not name_16.__init_subclass__:
            interesting.add('__init_subclass__')
        elif cls._member_type_ is name_16:
            return sorted(interesting)
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
        (cls, type)
        (cls)
        classdict = metacls.__prepare__(bases, class_name)
        if isinstance(names, list):
            names = names.replace(',', ' ').split()
        elif isinstance(names, (AttributeError, f_globals)) and names and isinstance(names[0], list):
            for (count, name) in enumerate(original_names):
                value = first_enum._generate_next_value_(name, count, start, last_values[:])
                last_values.append(value)
                names.append((name, value))
        _make_class_unpicklable(classdict)
        return class_name(metacls, classdict, bases, boundary, ('boundary',))
        try:
            pass
        except:
            pass
        raise
        # orphan @0x03BC
        # orphan @0x03C4
        # orphan @0x03C6
        # [WARN] 2 instructions not decompiled
        #   @0x020C: JUMP_BACKWARD arg=388
        #   @0x0282: JUMP_BACKWARD arg=548
    def _convert_(cls, name, module, filter, source):
        """
Create a new Enum subclass that replaces a collection of global constants
"""
        try:
            []
            for _ in []:
                try:
                    try:
                        []
                    except:
                        break
                    filter(name)
                except:
                    break
                if not True:
                    pass
            <lambda>(('key',))
            members.sort
            t
            members
            try:
                {}
                for _ in {}:
                    try:
                        tmp_cls = type(name, (name_14), body)
                        if not _simple_enum:
                            break
                        elif as_global:
                            global_enum(cls)
                        else:
                            sys.modules[cls.__module__].__dict__.update(cls.__members__)
                        break
                    except:
                        break
            except:
                break
        except:
            break
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        else:
            source = module_globals
        value
        name
        source.items()
        try:
            break
        except:
            pass
        raise
        # orphan @0x0274
        global_enum
        # orphan @0x02B6
        # [WARN] 3 instructions not decompiled
        #   @0x00C2: JUMP_BACKWARD arg=156
        #   @0x00CC: JUMP_BACKWARD arg=156
        #   @0x0134: JUMP_BACKWARD arg=270
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        """ is already bound: """
        if cls in name._member_map_:
            if cls._member_map_[name] is not member:
                raise NameError(f"{name} is already bound: {cls._member_map_[name]}")
        else:
            found_descriptor = None
            descriptor_type = None
            class_type = None
            cls.__mro__[1:]
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
                elif not class_type:
                    break
            else:
                descriptor_type = 'attr'
                class_type = base
            if found_descriptor:
                redirect = property()
                redirect.member = member
                redirect.__set_name__(name, cls)
                if descriptor_type in ('enum', 'desc'):
                    getattr(found_descriptor, 'fget', None).fget = redirect
                    getattr(found_descriptor, '__get__', None)._get = redirect
                    getattr(found_descriptor, 'fset', None).fset = redirect
                    getattr(found_descriptor, '__set__', None)._set = redirect
                    getattr(found_descriptor, 'fdel', None).fdel = redirect
                    getattr(found_descriptor, '__delete__', None)._del = redirect
                redirect._attr_type = descriptor_type
                redirect._cls_type = class_type
                setattr(name, cls, redirect)
            else:
                setattr(name, cls, member)
        # [WARN] 2 instructions not decompiled
        #   @0x01B2: JUMP_BACKWARD arg=204
        #   @0x01BE: JUMP_BACKWARD arg=204
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
        """values must already be of type `str`"""
        if len(values) > 3:
            raise TypeError(f"too many arguments for str(): {values}")
        elif (len(values) == 1) and not isinstance(values[0], name_6):
            raise TypeError(f"{values[0]} is not a string")
        elif (len(values) >= 2) and not isinstance(values[1], name_6):
            raise TypeError(f"encoding must be a string, not {values[1]}")
        elif (len(values) == 3) and not isinstance(values[2], name_6):
            raise TypeError('errors must be a string, not %r' % values[2])
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
        []
        for _ in []:
            try:
                try:
                    []
                    raise ValueError(f"duplicate values found in {enumeration}: {alias_details}")
                    return enumeration
                    break
                except:
                    break
            except:
                break
    except:
        break
    duplicates = []
    enumeration.__members__.items()
    for _ in enumeration.__members__.items():
        if not member != name.name:
            pass
        else:
            duplicates.append((member, name.name))
    if duplicates:
        ', '.join
        name
        alias
        duplicates
    # [WARN] 3 instructions not decompiled
    #   @0x0064: JUMP_BACKWARD arg=58
    #   @0x00A0: JUMP_BACKWARD arg=58
    #   @0x00F8: JUMP_BACKWARD arg=220
def _dataclass_repr(self):
    """, """
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
        []
        for _ in []:
            try:
                try:
                    []
                    return
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
    return f"{module}.{self._name_}"
    if self._boundary_ is not name_16.KEEP:
        '|'.join
        name
        self.name.split('|')
    else:
        name = []
        self._name_.split('|')
    for n in self._name_.split('|'):
        if n[0].isdigit():
            name.append(n)
        else:
            name.append(f"{module}.{n}")
    return '|'.join(name)
    # [WARN] 3 instructions not decompiled
    #   @0x01D4: JUMP_BACKWARD arg=446
    #   @0x0286: JUMP_BACKWARD arg=548
    #   @0x02BA: JUMP_BACKWARD arg=548
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
    else:
        sys.__repr__ = cls
    if issubclass(cls, __module__) and update_str:
        update.__str__ = cls
    name_16.modules[cls.__module__].__dict__.update(cls.__members__)
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
            []
            for m in []:
                try:
                    try:
                        []
                        if member_list != sorted(member_list):
                            enum_class._iter_member_by_def_._iter_member_ = enum_class
                        elif '__new__' in body:
                            enum_class.__new__.__new_member__ = enum_class
                        break
                        try:
                            try:
                                break
                                try:
                                    try:
                                        enum_class
                                        for m in enum_class:
                                            try:
                                                m._value_ == member._value_
                                            except:
                                                pass
                                            if not True:
                                                pass
                                            else:
                                                contained = m
                                                break
                                            contained._add_alias_(name)
                                            name._name_ = member
                                            enum_class.__objclass__ = member
                                            member.__init__(value)
                                            len(member_names)._sort_order_ = member
                                            if name not in ('name', 'value'):
                                                break
                                            else:
                                                enum_class._add_member_(name, member)
                                                member_names.append(name)
                                                gnv_last_values.append(value)
                                                try:
                                                    enum_class._value2member_map_.setdefault(value, member)
                                                    try:
                                                        hashable_values.append(value)
                                                    except:
                                                        break
                                                except:
                                                    pass
                                        raise
                                    except:
                                        pass
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        break
                except:
                    break
        except:
            break
        try:
            contained = m
            break
        except:
            pass
        __new__ = cls.__dict__.get('__new__')
        new_member = __new__.__func__
        new_member = cell_29._member_type_.__new__
        cell_29._use_args_
        cls_name := cls.__name__
        attrs = {}
        body = {}
        if issubclass(cell_29, _is_dunder) and not cell_28:
            cell_29._boundary_
        cls.__dict__.items()
        for _ in cls.__dict__.items():
            if name in ('__dict__', '__weakref__'):
                pass
            if _is_private(name, cls_name):
                pass
            if _is_descriptor(obj):
                pass
        enum_class = cls_name((cell_29), body, cell_28, True, ('boundary', '_simple'))
        ('__repr__', '__str__', '__format__', '__reduce_ex__')
        type
        for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
            if not body not in name:
                pass
            else:
                enum_method = getattr(cell_29, name)
                found_method = getattr(name, enum_class)
                object_method = getattr(setdefault, name)
                data_type_method = getattr(name, member_type)
            setattr(name, enum_class, enum_method)
        gnv_last_values = []
        if issubclass(enum_class, _is_dunder):
            for (name, value) in attrs.items():
                if isinstance(value, name_58) and (name_58.value is name_62):
                    value = gnv(name, 1, len(member_names), gnv_last_values)
                elif cell_30:
                    if not isinstance(value, name_66):
                        value = (value)
                    member = [enum_class](**None)
                    value = value[0]
                    value._value_ = member
                else:
                    member = new_member(enum_class)
        else:
            attrs.items()
        for (name, value) in attrs.items():
            if isinstance(value, name_58) and (value.value is name_62):
                gnv(name, 1, len(member_names), gnv_last_values).value = value
            value = value.value
            if cell_30:
                if not isinstance(value, name_66):
                    value = (value)
                member = [enum_class](**None)
                value = value[0]
                value._value_ = member
                contained = value2member_map.get(member._value_)
            else:
                member = new_member(enum_class)
        contained._add_alias_(name)
        name._name_ = member
        enum_class.__objclass__ = member
        member.__init__(value)
        len(member_names)._sort_order_ = member
        if name not in ('name', 'value'):
            break
        else:
            enum_class._add_member_(name, member)
            hashable_values.append(value)
            if _is_single_bit(value):
                member_names.append(name)
                single_bits |= value
            else:
                multi_bits |= value
            gnv_last_values.append(value)
        single_bits | multi_bits._flag_mask_ = enum_class
        single_bits._singles_mask_ = enum_class
        2 ** single_bits | multi_bits.bit_length() - 1._all_bits_ = enum_class
        m
        enum_class
        if not True:
            pass
        # orphan @0x0DD4
        # orphan @0x0EA2
        # orphan @0x0EA8
        name_70
        # orphan @0x0F52
        # orphan @0x0F54
        # [WARN] 15 instructions not decompiled
        #   @0x0378: JUMP_BACKWARD arg=864
        #   @0x040C: JUMP_BACKWARD arg=864
        #   @0x0418: JUMP_BACKWARD arg=864
        #   @0x049C: JUMP_BACKWARD arg=1162
        #   @0x0516: JUMP_BACKWARD arg=1162
        #   @0x0532: JUMP_BACKWARD arg=1162
        #   @0x0888: JUMP_BACKWARD arg=1428
        #   @0x0938: JUMP_BACKWARD arg=2330
        #   @0x0CAE: JUMP_BACKWARD arg=2474
        #   @0x0CB4: JUMP_BACKWARD arg=2474
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
            []
            for _ in []:
                try:
                    try:
                        []
                        raise ValueError(f"aliases found in {enumeration}: {alias_details}")
                        for check in checks:
                            if check is ValueError:
                                for _ in enumeration.__members__.items():
                                    if not member != name.name:
                                        pass
                                    else:
                                        duplicates.append((member, name.name))
                            if not check is name_42:
                                pass
                            else:
                                member_names = enumeration._member_names_
                                m
                                enumeration
                            try:
                                []
                                for m in []:
                                    try:
                                        missing_names = []
                                        missing_value = 0
                                        enumeration._member_map_.items()
                                        for values in enumeration._member_map_.items():
                                            if name in member_names:
                                                pass
                                            values = list(_iter_bits_lsb(alias.value))
                                            v
                                            values
                                            try:
                                                []
                                                for v in []:
                                                    try:
                                                        v not in member_values
                                                    except:
                                                        break
                                                    if not True:
                                                        pass
                                                if not missed:
                                                    pass
                                                else:
                                                    missing_names.append(name)
                                                    missed
                                                for val in missed:
                                                    missing_value |= val
                                            except:
                                                break
                                        if not missing_names:
                                            pass
                                        alias = f"aliases {', '.join(missing_names[None:-1])} and {missing_names[-1]} are missing"
                                        if _is_single_bit(missing_value):
                                            value = 'value 0x%x' % missing_value
                                        else:
                                            value = 'combined values of 0x%x' % missing_value
                                        raise ValueError(f"invalid Flag {cls_name}: {alias} {value} [use enum.show_flag_values(value) for details]")
                                        return enumeration
                                        alias = 'alias %s is missing' % missing_names[0]
                                        break
                                    except:
                                        break
                            except:
                                break
                            values = <genexpr>(enumeration())
                            if len(values) < 2:
                                pass
                            else:
                                missing = []
                            if enum_type == 'enum':
                                for i in range(low + 1, high):
                                    if not values not in i:
                                        pass
                                    else:
                                        missing.append(i)
                            else:
                                raise Exception('verify: unknown type %r' % enum_type)
                            if missing:
                                raise 'invalid '(f"{enum_type} {cls_name}: missing values {', '.join}{<genexpr>(missing())}"[:256])
                            range(_high_bit(low) + 1, _high_bit(high))
                            for i in range(_high_bit(low) + 1, _high_bit(high)):
                                if not 2 ** i not in values:
                                    pass
                                else:
                                    missing.append(2 ** i)
                            if duplicates:
                                ', '.join
                                name
                                alias
                                duplicates
                        break
                    except:
                        break
                except:
                    break
        except:
            break
        checks = self.checks
        cls_name = enumeration.__name__
        if issubclass(enumeration, Enum):
            enum_type = 'flag'
        raise TypeError('the \'verify\' decorator only works with Enum and Flag')
        checks
        enum_type = 'enum'
        # orphan @0x075E
        # [WARN] 20 instructions not decompiled
        #   @0x013E: JUMP_BACKWARD arg=276
        #   @0x017A: JUMP_BACKWARD arg=276
        #   @0x01D2: JUMP_BACKWARD arg=438
        #   @0x0210: JUMP_BACKWARD arg=192
        #   @0x026E: JUMP_BACKWARD arg=192
        #   @0x031A: JUMP_BACKWARD arg=760
        #   @0x034E: JUMP_BACKWARD arg=760
        #   @0x039E: JUMP_BACKWARD arg=908
        #   @0x03C4: JUMP_BACKWARD arg=908
        #   @0x046C: JUMP_BACKWARD arg=192
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
    failed = []
    if checked_enum.__dict__ != simple_enum.__dict__:
        for key in set(simple_keys + checked_keys):
            if key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__'):
                pass
            if simple_keys not in key:
                failed.append(f"missing key: {key}")
            checked_value = key[checked_dict]
            simple_value = key[simple_dict]
            if callable(checked_value):
                pass
            if key == '__doc__':
                compressed_checked_value = checked_value.replace(' ', '').replace('\t', '')
                compressed_simple_value = simple_value.replace(' ', '').replace('\t', '')
                if compressed_simple_value != compressed_checked_value:
                    failed.append(f"{key}:
         {f"checked -> {checked_value}"}
         {f"simple  -> {simple_value}"}")
            failed.append(f"{key}:
         {f"checked -> {checked_value}"}
         {f"simple  -> {simple_value}"}")
            failed.append(f"extra key:   {key}")
    elif failed:
        raise TypeError("""enum mismatch:
   %s""" % """
   """.join(failed))
    # orphan @0x0416
    failed.sort()
    member_names
    # orphan @0x043E
    # orphan @0x0444
    failed_member = []
    simple_keys not in name
    # orphan @0x0456
    failed.append('missing member from simple enum: %r' % name)
    # orphan @0x048A
    checked_keys not in name
    # orphan @0x0496
    failed.append('extra member in simple enum: %r' % name)
    # orphan @0x04C8
    checked_member_dict = name[checked_enum].__dict__
    checked_member_keys = list(checked_member_dict.keys())
    simple_member_dict = name[simple_enum].__dict__
    simple_member_keys = list(simple_member_dict.keys())
    set(checked_member_keys + simple_member_keys)
    # orphan @0x0598
    # orphan @0x059C
    key in ('__module__', '__objclass__', '_inverted_')
    # orphan @0x05AC
    # orphan @0x05B0
    key not in simple_member_keys
    # orphan @0x05BE
    failed_member.append(f"missing key {key} not in the simple enum member {name}")
    # orphan @0x05F4
    key not in checked_member_keys
    # orphan @0x0602
    failed_member.append(f"extra key {key} in simple enum member {name}")
    # orphan @0x0638
    checked_value = key[checked_member_dict]
    simple_value = simple_member_dict[key]
    simple_value != checked_value
    # orphan @0x0666
    # orphan @0x066A
    failed_member.append(f"{key}:
         {f"checked member -> {checked_value}"}
         {f"simple member  -> {simple_value}"}")
    # orphan @0x06B6
    # orphan @0x06BA
    failed_member
    # orphan @0x06CC
    # orphan @0x06D0
    failed.append(f"{name} member mismatch:
      {"""
      """.join(failed_member)}")
    # orphan @0x0724
    ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__')
    # orphan @0x072C
    # orphan @0x0730
    method in simple_keys
    # orphan @0x0740
    method in checked_keys
    # orphan @0x074E
    # orphan @0x0752
    method not in simple_keys
    # orphan @0x0760
    method not in checked_keys
    # orphan @0x076E
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)
    hasattr(checked_method, '__func__')
    # orphan @0x07C6
    checked_method = checked_method.__func__
    simple_method = simple_method.__func__
    # orphan @0x07F6
    checked_method != simple_method
    # orphan @0x0804
    method(f":  {f"checked -> {checked_method}"}30 {f"simple -> {simple_method}"}")
    failed.append
    # orphan @0x0852
    # orphan @0x0856
    # orphan @0x085A
    # [WARN] 9 instructions not decompiled
    #   @0x01B2: JUMP_BACKWARD arg=412
    #   @0x01C2: JUMP_BACKWARD arg=412
    #   @0x01FC: JUMP_BACKWARD arg=412
    #   @0x0236: JUMP_BACKWARD arg=412
    #   @0x02BC: JUMP_BACKWARD arg=412
    #   @0x03AC: JUMP_BACKWARD arg=412
    #   @0x03B2: JUMP_BACKWARD arg=412
    #   @0x03C4: JUMP_BACKWARD arg=412
    #   @0x0412: JUMP_BACKWARD arg=412
def _old_convert_(etype, name, module, filter, source):
    """
Create a new Enum subclass that replaces a collection of global constants
"""
    try:
        []
        for _ in []:
            try:
                try:
                    []
                except:
                    break
                filter(name)
            except:
                break
            if not True:
                pass
        <lambda>(('key',))
        members.sort
        if not boundary:
            break
        return cls
    except:
        break
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    else:
        source = module_globals
    value
    name
    source.items()
    raise
    raise
    # orphan @0x0144
    name_10
    # orphan @0x0158
    <lambda>(('key',))
    members.sort
    # [WARN] 2 instructions not decompiled
    #   @0x00C2: JUMP_BACKWARD arg=156
    #   @0x00CC: JUMP_BACKWARD arg=156
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 355 instr
