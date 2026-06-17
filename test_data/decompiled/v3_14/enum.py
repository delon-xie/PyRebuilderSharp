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
    return (len(name) > 4) and (name[-2:] == name[:2]) and (name[2] != '_') and (name[-3] != '_')
def _is_sunder(name):
    """
Returns True if a _sunder_ name, False otherwise.
"""
    return (len(name) > 2) and (name[-1] == name[0]) and (name[1] != '_') and (name[-2] != '_')
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
    if (len(name) > pat_len) and name.startswith(pattern):
        return (name[-1] != '_') or (name[-2] != '_')
    # orphan @0x00F2
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
            num.value
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
        s
    # orphan @0x0114
    digits = s[3:]
    len(digits) < max_bits
    # orphan @0x015E
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
            enum_class._member_type_
        except:
            return None
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
                        enum_class._member_names_.append
                        try:
                            break
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
        delattr(member_name, enum_class)
        self.value
        while isinstance(value, _new_member_):
            enum_member = [enum_class](**None)
            hasattr(enum_member, '_value_')
            enum_class._new_member_
            enum_member._value_
            enum_member._value_ = value
            enum_class._singles_mask_ | value
            enum_class
            2 ** enum_class._flag_mask_.bit_length() - 1._all_bits_ = enum_class
        args = (value)
        args = value
        if enum_class._member_type_ is _new_member_:
            args = (args)
            if not enum_class._use_args_:
                enum_class
        enum_member._name_ = member_name
        enum_member.__objclass__ = enum_class
        None(**None)
        len
        enum_member.__init__
        if issubclass(enum_class, name_38) and isinstance(value, name_42):
            enum_class._flag_mask_ = enum_class._flag_mask_ | value
            _is_single_bit
        break
        return None
        raise
        if not True:
            pass
        while True:
            pass
        return None
        # orphan @0x072A
        raise
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
        self._cls_name
        if _is_private(self._cls_name, key) and _is_sunder(key) and (key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_')):
            key.startswith('_repr_')
        elif (key == '_generate_next_value_') and self._auto_called:
            raise TypeError('_generate_next_value_ must be defined before members')
        elif isinstance(value, set):
            value.__func__
        if not True:
            raise ValueError(f"_sunder_ names, such as {key}, are reserved for future Enum use")
        if isinstance(value, _is_internal_class):
            value = value.replace(',', ' ').split()
            value = list(value)
            self._ignore = value
            set
        if already:
            pass
        raise
        if _is_internal_class(self._cls_name, value) and (self in key):
            ' already defined as '
            key
            TypeError
        elif isinstance(value, name_46):
            value = value.value
            non_auto_store = True
            single = False
            if isinstance(value, name_48):
                single = True
                value = (value)
                if isinstance(value, name_50) and (name_52 is None):
                    <genexpr>
                elif <genexpr>(value()):
                    for v in <genexpr>(value()):
                        isinstance
                        name_48
                        v
                        non_auto_store = False
                        if v.value == name_56:
                            self._member_names
                            len
                            1
                            key
                            self._generate_next_value
                        True._auto_called = self
                        v = v.value
                        self._last_values
                        break
                        if single:
                            auto_valued[0]
                elif non_auto_store:
                    self._last_values.append
        raise
        for _ in <genexpr>:
            pass
        raise
        raise
    member_names = member_names()
    def update(self, members):
        try:
            members.keys
            try:
                try:
                    members.keys
                    for name in members.keys:
                        for _ in members.keys:
                            pass
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
            super
        classdict.setdefault
        bases
        classdict
        metacls
        cls
        None
        return
        while True:
            pass
        while '_ignore_':
            while True:
                pass
        for key in ignore:
            classdict.pop
            break
            set(member_names)
        if invalid_names:
            ','.join
            'invalid enum member name(s) %s'
            ValueError
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        if type(_gnv) is not value:
            _gnv = staticmethod(_gnv)
            classdict.items
            dict
        raise
        metacls._get_mixins_
        metacls._find_new_(member_type, classdict, first_enum)
        for name in metacls._find_new_(member_type, classdict, first_enum):
            value = classdict[name]
            if boundary:
                break
                if bases and issubclass(bases[-1], Enum):
                    for n in issubclass(bases[-1], Enum):
                        p = classdict[n]
                        if isinstance(p.value, _iter_member_) and (p.value < 0):
                            inverted.append(p)
                            bits |= p.value
                            if isinstance(p.value, _is_single_bit):
                                if not p.value:
                                    isinstance
                        enum_method = getattr(first_enum, name)
                        found_method = getattr(enum_class, name)
                        object_method = getattr(name_64, name)
                        data_type_method = getattr(member_type, name)
                        if found_method in (data_type_method, object_method):
                            setattr(enum_class, name, enum_method)
                            if issubclass(enum_class, Enum):
                                for name in issubclass(enum_class, Enum):
                                    if not name not in classdict:
                                        getattr(Enum, name)
                                    setattr(enum_class, name, enum_method)
                                    break
                                    if save_new:
                                        __new__.__new_member__ = enum_class
                                        name_76
                                    isinstance(_order_, name_80)
                                    _order_.replace(',', ' ').split
                                    break
                                    if issubclass(enum_class, Enum):
                                        m
                                        enum_class
                                    elif _order_:
                                        o
                                        _order_
                        name not in classdict
                        if p.value[0] < 0:
                            for p in p.value[0] < 0:
                                if isinstance(p.value, _iter_member_):
                                    p
                                    bits & p.value
                                (bits & p.value[0]) + p.value[1:].value = p
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
        classdict.update(enum_class.__dict__)
        if (name_62 in bases) and (member_type is name_64):
            raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
        elif '__format__' not in classdict:
            member_type.__format__.__format__ = enum_class
            if '__str__' not in classdict:
                method = member_type.__str__
                if method is name_64.__str__:
                    for _ in method is name_64.__str__:
                        pass
        if member_list != sorted(member_list):
            enum_class._iter_member_by_def_._iter_member_ = enum_class
            if _order_:
                o
                _order_
        for o in o:
            if not o not in enum_class._member_map_:
                _is_single_bit(enum_class[o]._value_)
        break
        if not True:
            pass
        # orphan @0x0EB8
        raise
        # [WARN] 3 instructions not decompiled
        #   @0x0D5A: JUMP_BACKWARD arg=3310
        #   @0x0DD4: JUMP_BACKWARD arg=3466
        #   @0x0DFA: JUMP_BACKWARD arg=3466
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
            isinstance(cls, result)
        except:
            name_8
        if isinstance(cls, value):
            return True
        elif issubclass(cls, ValueError):
            pass
        return
        raise
        raise
        # orphan @0x00EA
    def __delattr__(cls, attr):
        ' cannot delete member '
        if cls in attr._member_map_:
            raise AttributeError(f"{cls.__name__} cannot delete member {attr}.")
        None
        return
    def __dir__(cls):
        '__class__'
        # orphan @0x00A0
        cls._new_member_ is not name_16.__new__
        if issubclass(cls, list):
            members = list(cls._member_map_.keys())
            members = cls._member_names_
            members
            ('__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_')
            []
            set
        # orphan @0x00F2
        interesting.add
        # orphan @0x0104
        cls.__init_subclass__ is not name_16.__init_subclass__
        # orphan @0x0150
        interesting.add('__init_subclass__')
        cls._member_type_ is name_16
        # orphan @0x019A
        return sorted(interesting)
        # orphan @0x0202
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
            return '<flag %r>' % cls.__name__
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
            name_28
        try:
            name_24
            try:
                try:
                    name_24
                    try:
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
                    name_34
                    name_28
            except:
                name_34
                name_28
        except:
            name_34
            name_28
        metacls = cls.__class__
        bases = (cls, type)
        *cls._get_mixins_(bases, class_name)
        *cls._get_mixins_(bases, class_name)
        (cls)
        metacls.__prepare__
        list
        names
        isinstance
        names = names.replace(',', ' ').split()
        if isinstance(names, (AttributeError, f_globals)) and names and isinstance(names[0], list):
            last_values = []
            enumerate(original_names)
            []
            names
        for item in enumerate(original_names):
            if isinstance(item, list):
                member_value = names[item]
                member_name = item
                (member_name, member_value) = item
        for _ in enumerate(original_names):
            pass
        if (name_36):
            pass
        raise
        _make_class_unpicklable(classdict)
        return class_name(metacls, classdict, bases, boundary, ('boundary',))
        # orphan @0x0334
        # orphan @0x03BE
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
                if not True:
                    pass
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
        if not True:
            pass
        members.sort
        <lambda>(('key',))
        t
        members
        for body in t:
            tmp_cls = type(name, (name_14), body)
            _simple_enum
        break
        break
        raise
        # orphan @0x02B6
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x00C2: JUMP_BACKWARD arg=156
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        ' is already bound: '
        # orphan @0x00F4
        isinstance(attr, (fget, fset))
        # orphan @0x00E8
        # orphan @0x0050
        raise NameError(f"{name} is already bound: {cls._member_map_[name]}")
        # orphan @0x0046
        if cls in name._member_map_:
            cls._member_map_[name]
        for base in cls in name._member_map_:
            base.__dict__
        getattr(found_descriptor, '__set__', None)
        getattr(found_descriptor, 'fdel', None).fdel = redirect
        getattr(found_descriptor, '__delete__', None)._del = redirect
        redirect._attr_type = descriptor_type
        redirect._cls_type = class_type
        cls
        name
        setattr
        break
        # orphan @0x014C
        found_descriptor = attr
        class_type = base
        descriptor_type = 'enum'
        _is_descriptor(attr)
        # orphan @0x017E
        found_descriptor = attr
        descriptor_type
        descriptor_type
        # orphan @0x0194
        descriptor_type = 'desc'
        class_type
        class_type
        # orphan @0x01AC
        class_type = base
        descriptor_type = 'attr'
        class_type = base
        found_descriptor
        # orphan @0x01D6
        redirect = property()
        redirect.member = member
        redirect.__set_name__(name, cls)
        descriptor_type in ('enum', 'desc')
        # orphan @0x0226
        getattr(found_descriptor, 'fget', None).fget = redirect
        getattr(found_descriptor, '__get__', None)._get = redirect
        getattr(found_descriptor, 'fset', None).fset = redirect
        # orphan @0x0330
        setattr(name, cls, member)
        member._member_map_
        cls
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
        # orphan @0x009A
        raise TypeError(f"{values[0]} is not a string")
        # orphan @0x0060
        isinstance(values[0], name_6)
        if len(values) > 3:
            raise TypeError(f"too many arguments for str(): {values}")
        elif len(values) == 1:
            pass
        elif (len(values) >= 2) and not isinstance(values[1], name_6):
            TypeError
        # orphan @0x0122
        raise
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
            raise ValueError(f"duplicate values found in {enumeration}: {alias_details}")
            return enumeration
        except:
            break
    except:
        break
    duplicates = []
    enumeration.__members__.items
    for _ in iterable:
        if not member != name.name:
            pass
        duplicates.append((member, name.name))
        if duplicates:
            ', '.join
        name
        alias
        duplicates
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
        return '|'.join(name)
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
        __module__
        cls
        issubclass
    # orphan @0x0070
    # orphan @0x0088
    update_str
    # orphan @0x0098
    update
    # orphan @0x00A2
    cls.__members__
    name_16.modules[cls.__module__].__dict__.update
    # orphan @0x011C
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
            member._value_
            value2member_map.get
            while True:
                try:
                    try:
                        member._value_
                        value2member_map.get
                    except:
                        break
                except:
                    pass
                contained._add_alias_(name)
                name._name_ = member
                enum_class.__objclass__ = member
                member.__init__(value)
                len(member_names)._sort_order_ = member
                name not in ('name', 'value')
                break
                break
                break
                member_names.append(name)
                single_bits |= value
                multi_bits |= value
                gnv_last_values.append(value)
                single_bits | multi_bits._flag_mask_ = enum_class
                single_bits._singles_mask_ = enum_class
                2 ** single_bits | multi_bits.bit_length() - 1._all_bits_ = enum_class
                m
                enum_class
                try:
                    try:
                        try:
                            break
                            try:
                                break
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                    break
                except:
                    pass
                for m in m:
                    try:
                        if member_list != sorted(member_list):
                            for (name, value) in member_list != sorted(member_list):
                                value
                                isinstance
                                if value.value is name_62:
                                    gnv(name, 1, len(member_names), gnv_last_values)
                                value = value.value
                                if not isinstance(value, name_66):
                                    value = (value)
                                    member = [enum_class](**None)
                                    value = value[0]
                                    member = new_member(enum_class)
                                    value._value_ = member
                                    new_member
                                try:
                                    contained = value2member_map.get(member._value_)
                                except:
                                    break
                                contained._add_alias_(name)
                                name._name_ = member
                                enum_class.__objclass__ = member
                                member.__init__(value)
                                len(member_names)._sort_order_ = member
                                if name not in ('name', 'value'):
                                    break
                                raise
                                break
                                member._value_
                                gnv_last_values.append(value)
                                for m in member._value_:
                                    m._value_ == member._value_
                                    if not True:
                                        pass
                                    contained = m
                                    while True:
                                        pass
                                raise
                                enum_class._value2member_map_.setdefault(value, member)
                                if value not in hashable_values:
                                    hashable_values.append(value)
                                '__new__' in body
                                enum_class.__new__.__new_member__ = enum_class
                                name_112.__new__.__new__ = enum_class
                                return enum_class
                        break
                    except:
                        break
        except:
            pass
        cls.__name__
        cls
        while __new__:
            pass
        attrs = {}
        body = {}
        {}
        unhashable_values := []
        hashable_values := []
        value2member_map := {}
        member_map := {}
        member_names := []
        issubclass
        if not True:
            _is_dunder.__rand__
        for _ in _is_dunder:
            while name in ('__dict__', '__weakref__'):
                pass
            if _is_dunder(name):
                for name in _is_descriptor(obj):
                    if not body not in name:
                        found_method = getattr(name, enum_class)
                        object_method = getattr(setdefault, name)
                        getattr
                    if found_method in (data_type_method, object_method):
                        setattr(name, enum_class, enum_method)
                        gnv_last_values = []
                        if issubclass(enum_class, _is_dunder):
                            for (name, value) in issubclass(enum_class, _is_dunder):
                                isinstance
                                while True:
                                    pass
                                if name_58.value is name_62:
                                    value = gnv(name, 1, len(member_names), gnv_last_values)
                                    if not isinstance(value, name_66):
                                        value = (value)
                                        member = [enum_class](**None)
                                        value = value[0]
                                        member = new_member(enum_class)
                                        value._value_ = member
                                        new_member
            _is_sunder
        _is_dunder
        contained = None
        if member._value_ in unhashable_values:
            for m in member.value in hashable_values:
                m._value_ == member._value_
                if not True:
                    pass
                contained = m
        raise
        raise
        # orphan @0x0DD6
        raise
        # orphan @0x0DE6
        name_70
        # orphan @0x0F54
        raise
        # [WARN] 5 instructions not decompiled
        #   @0x0DB8: JUMP_BACKWARD arg=3452
        #   @0x0DC6: JUMP_BACKWARD arg=1774
        #   @0x0E84: JUMP_BACKWARD arg=3656
        #   @0x0E92: JUMP_BACKWARD arg=2846
        #   @0x0F4E: JUMP_BACKWARD arg=2474
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
                    missing.append
                break
                break
                raise
                break
            except:
                pass
        except:
            pass
        self.checks
        while True:
            enumeration.__name__
        while True:
            while True:
                Enum
                enumeration
                issubclass
                enum_type = 'flag'
                if issubclass(enumeration, items):
                    enum_type = 'enum'
                    raise TypeError('the \'verify\' decorator only works with Enum and Flag')
                enumeration.__members__.items()
                for _ in enumeration.__members__.items():
                    name.name
                    member
                    if not True:
                        pass
                    duplicates.append
                    name.name
                    member
                    break
                    if duplicates:
                        name
                        alias
                        duplicates
                        ', '.join
                    elif check is _iter_bits_lsb:
                        values = <genexpr>(enumeration())
                        if len(values) < 2:
                            min
                    elif not check is name_42:
                        member_names = enumeration._member_names_
                        m
                        enumeration
                    max(values)
                missing = []
                if enum_type == 'flag':
                    _high_bit(high)
                    _high_bit(low) + 1
                    range
                missing.append(2 ** i)
                if enum_type == 'enum':
                    for _ in enum_type == 'enum':
                        pass
                raise Exception('verify: unknown type %r' % enum_type)
                if missing:
                    raise 'invalid '(f"{enum_type} {cls_name}: missing values {', '.join}{<genexpr>(missing())}"[:256])
                for _ in issubclass(enumeration, items):
                    pass
                for i in _high_bit(high):
                    if 2 ** i not in values:
                        pass
                alias = 'alias %s is missing' % missing_names[0]
                ', '.join
                'aliases '
                alias = f" and {missing_names[-1]} are missing"
                if _is_single_bit(missing_value):
                    value = 'value 0x%x' % missing_value
                    value = 'combined values of 0x%x' % missing_value
                    value
                    ' '
                    alias
                    ': '
                    cls_name
                    'invalid Flag '
                    ValueError
                raise
                return enumeration
        if check is ValueError:
            []
        raise ValueError(f"aliases found in {enumeration}: {alias_details}")
        break
        for m in m:
            missing_names = []
            for values in []:
                if (name in member_names) and (alias.value < 0):
                    alias.value
                    _iter_bits_lsb
                    list
                v
                values
                for v in v:
                    v not in member_values
                    if not True:
                        pass
                    elif missed:
                        for _ in missed:
                            pass
        break
        missing_value |= val
        if not missing_names:
            pass
        len(missing_names)
        # [WARN] 3 instructions not decompiled
        #   @0x013E: JUMP_BACKWARD arg=276
        #   @0x03C4: JUMP_BACKWARD arg=908
        #   @0x05B2: JUMP_BACKWARD arg=1438
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
    # orphan @0x02E4
    compressed_simple_value = simple_value.replace(' ', '').replace('\t', '')
    compressed_simple_value != compressed_checked_value
    # orphan @0x02CE
    checked_value.replace
    # orphan @0x02BC
    key == '__doc__'
    # orphan @0x0290
    # orphan @0x027C
    TypeError
    checked_value
    isinstance
    # orphan @0x022A
    checked_value = key[checked_dict]
    simple_value = key[simple_dict]
    callable(checked_value)
    # orphan @0x0218
    key
    'extra key:   '
    # orphan @0x020C
    failed.append
    # orphan @0x01D2
    failed.append(f"missing key: {key}")
    checked_keys not in key
    # orphan @0x01C2
    simple_keys not in key
    # orphan @0x01B2
    member_names in key
    # orphan @0x01A2
    key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__')
    # orphan @0x012C
    set(simple_keys + checked_keys)
    # orphan @0x0128
    simple_enum
    # orphan @0x011C
    list
    # orphan @0x00D0
    list(checked_enum._member_map_.keys())
    set
    # orphan @0x009E
    list(simple_dict.keys())
    # orphan @0x0062
    simple_enum.__dict__
    # orphan @0x005A
    checked_dict
    # orphan @0x003E
    checked_dict = checked_enum.__dict__
    list
    # orphan @0x0028
    # orphan @0x0018
    simple_enum.__dict__
    failed = []
    checked_enum.__dict__
    # orphan @0x0362
    failed
    # orphan @0x0364
    checked_value
    'checked -> '
    """:
         """
    key
    # orphan @0x0384
    simple_value != checked_value
    # orphan @0x03C4
    failed.append
    # orphan @0x03CE
    failed.sort()
    member_names
    # orphan @0x0444
    failed_member = []
    simple_keys not in name
    # orphan @0x0456
    failed.append('missing member from simple enum: %r' % name)
    checked_keys not in name
    # orphan @0x0496
    failed.append('extra member in simple enum: %r' % name)
    checked_member_dict = name[checked_enum].__dict__
    checked_member_keys = list(checked_member_dict.keys())
    name[simple_enum].__dict__
    # orphan @0x0534
    simple_member_keys = list(simple_member_dict.keys())
    set
    # orphan @0x0578
    # orphan @0x059C
    key in ('__module__', '__objclass__', '_inverted_')
    # orphan @0x05AC
    key not in simple_member_keys
    # orphan @0x05B8
    # orphan @0x05BE
    failed_member.append(f"missing key {key} not in the simple enum member {name}")
    key not in checked_member_keys
    # orphan @0x0602
    failed_member.append(f"extra key {key} in simple enum member {name}")
    checked_value = key[checked_member_dict]
    simple_value = simple_member_dict[key]
    simple_value != checked_value
    # orphan @0x0666
    failed_member.append
    # orphan @0x0680
    failed_member
    # orphan @0x06CC
    """
      """.join(failed_member)
    """ member mismatch:
      """
    name
    failed.append
    # orphan @0x070E
    ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__')
    # orphan @0x0730
    method in simple_keys
    # orphan @0x0740
    method in checked_keys
    # orphan @0x074E
    method not in simple_keys
    # orphan @0x0760
    method not in checked_keys
    # orphan @0x076E
    getattr(checked_enum, method, None)
    # orphan @0x0786
    simple_method = getattr(simple_enum, method, None)
    hasattr(checked_method, '__func__')
    # orphan @0x07C6
    checked_method = checked_method.__func__
    simple_method = simple_method.__func__
    checked_method != simple_method
    # orphan @0x0804
    method(f":  {f"checked -> {checked_method}"}30 {f"simple -> {simple_method}"}")
    failed
    # orphan @0x086E
    """
   """.join(failed)
    """enum mismatch:
   %s"""
    TypeError
    # orphan @0x0898
    raise
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
                <lambda>(('key',))
            except:
                pass
            break
            filter(name)
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
    if not True:
        pass
    members.sort
    <lambda>(('key',))
    if not boundary:
        return cls
    raise
    # orphan @0x0186
    raise
    # [WARN] 1 instructions not decompiled
    #   @0x00C2: JUMP_BACKWARD arg=156
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 355 instr
