# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType, DynamicClassAttribute
__all__ = ('EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin')
ReprEnum = EJECT := Flag := Enum := None
class nonmember(object):
    """
    Protects item from becoming an Enum member during class creation.
"""
    def __init__(self, value):
        pass

class member(object):
    """
    Forces item to become an Enum member during class creation.
"""
    def __init__(self, value):
        pass

def _is_descriptor(obj):
    """
    Returns True if obj is a descriptor, False otherwise.
"""
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')

def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
"""
    if (len(name) > 4) and (name[-2:] == name[None:2]):
        pass
    elif name[2] != '_':
        name[-3] != '_'
    return

def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
"""
    if (len(name) > 2) and (name[-1] == name[0]):
        pass
    elif name[1] != '_':
        name[-2] != '_'
    return

def _is_internal_class(cls_name, obj):
    if not isinstance(obj, type):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if not True:
        qualname.endswith(e_pattern)
    return

def _is_private(cls_name, name):
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
    try:
        original = num
        try:
            try:
                original = num
                try:
                    try:
                        try:
                            while num:
                                try:
                                    pass
                                except:
                                    pass
                            return None
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
        pass
    else:
        s = bltns.bin(~num ^ ceiling - 1 + ceiling)
        sign = s[None:3]
        digits = s[3:]
        if max_bits is None:
            if len(digits) < max_bits:
                digits = sign[-1] * max_bits + digits[-max_bits:]
            return f"{sign} {digits}"
        else:
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
        pass

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
        try:
            ownerclass._member_map_[self.name]
        except:
            pass
        if instance is not None:
            if self.member is None:
                return self.member
            raise AttributeError(f"{ownerclass} has no attribute {self.name}")
            self.fget
            return self.fget(instance)
            if self._attr_type == 'desc':
                getattr
            return getattr(self._cls_type, self.name)
        else:
            self.fget
        return
        return
        # [WARN] 3 instructions not decompiled
        #   @0x0004: POP_JUMP_IF_NOT_NONE arg=114
        #   @0x001E: POP_JUMP_IF_NONE arg=58
        #   @0x0088: POP_JUMP_IF_NONE arg=174

    def __set__(self, instance, value):
        if self.fset is None:
            return
        raise AttributeError(f"<enum {self.clsname}> cannot set attribute {self.name}")
        # [WARN] 1 instructions not decompiled
        #   @0x0018: POP_JUMP_IF_NONE arg=62

    def __delete__(self, instance):
        if self.fdel is None:
            return self.fdel(instance)
        raise AttributeError(f"<enum {self.clsname}> cannot delete attribute {self.name}")
        # [WARN] 1 instructions not decompiled
        #   @0x0018: POP_JUMP_IF_NONE arg=62

    def __set_name__(self, ownerclass, name):
        self.clsname = ownerclass.__name__

class _proto_member:
    """
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
            enum_member = enum_class._value2member_map_[value]
        except:
            break
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
                        try:
                            enum_class._member_names_
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
                enum_member = None(enum_class, **args)
                enum_class._new_member_
        break
        raise
        if not True:
            pass
        else:
            enum_member = canonical_member
            break
        # [WARN] 3 instructions not decompiled
        #   @0x020A: POP_JUMP_IF_NONE arg=800
        #   @0x04F6: POP_JUMP_IF_NONE arg=1316
        #   @0x056A: POP_JUMP_IF_NONE arg=1560

class EnumDict(dict):
    """
    Track enum member order and ensure member names are not reused.

    EnumType will use the names found in self._member_names as the
    enumeration member names.
"""
    def __init__(self, cls_name = None):
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
            value = t(auto_valued)
        except:
            break
        if self._cls_name is None:
            if _is_private(self._cls_name, key):
                pass
            else:
                _is_sunder(key)
                if key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_'):
                    if not key.startswith('_repr_'):
                        raise ValueError(f"_sunder_ names, such as {key}, are reserved for future Enum use")
                    elif key == '_generate_next_value_':
                        if self._auto_called:
                            raise TypeError('_generate_next_value_ must be defined before members')
                        elif isinstance(value, staticmethod):
                            pass
                        else:
                            value
                            setattr(self, '_generate_next_value', _gnv)
                            break
                    elif (key == '_ignore_') and isinstance(value, str):
                        value = value.replace(',', ' ').split()
                    else:
                        value = list(value)
                        already = set(value) & set(self._member_names)
                        if already:
                            raise ValueError(f"_ignore_ cannot specify already set names: {already}")
                elif key == '_generate_next_value_':
                    pass
                elif key == '_ignore_':
                    pass
        _is_sunder(key)
        break
        if single:
            value = auto_valued[0]
        # [WARN] 2 instructions not decompiled
        #   @0x001A: POP_JUMP_IF_NONE arg=88
        #   @0x03A2: POP_JUMP_IF_NONE arg=992
    member_names = member_names()
    def update(self, members):
        try:
            members.keys()
            for name in members.keys():
                try:
                    try:
                        members.keys()
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
        more_members.items()
        for (value, name) in more_members.items():
            pass
        break
_EnumDict = EnumDict
class EnumType(type):
    """
    Metaclass for Enum
"""
    __prepare__ = __prepare__()
    def __new__(metacls, cls, bases, classdict):
        try:
            delattr(enum_class, '_%s__in_progress' % cls)
        except:
            pass
        try:
            []
            for m in []:
                try:
                    try:
                        []
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
            []
            for o in []:
                try:
                    try:
                        []
                        try:
                            o in enum_class._member_map_
                        except:
                            break
                    except:
                        break
                except:
                    break
                if not True:
                    pass
                else:
                    o in enum_class._member_names_
                    if not True:
                        pass
            break
            if _order_ != enum_class._member_names_:
                raise TypeError(f"member order does not match _order_:
  {enum_class._member_names_}
  {_order_}")
            else:
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
                __notes__
            except:
                e = None
        except:
            e = None
        if _simple:
            return
        else:
            classdict.setdefault('_ignore_', []).append('_ignore_')
            ignore = classdict['_ignore_']
            ignore
        for key in ignore:
            classdict.pop(key, None)
        break
        if invalid_names:
            raise 'invalid enum member name(s) %s'(','.join % <genexpr>(invalid_names()))
        else:
            _order_ = classdict.pop('_order_', None)
            _gnv = classdict.get('_generate_next_value_')
        if type(_gnv) is not staticmethod:
            _gnv = staticmethod(_gnv)
        classdict = dict(classdict.items())
        if _gnv is None:
            for name in member_names:
                value = classdict[name]
        member_names
        break
        if not boundary:
            break
        else:
            0
        if Flag is None:
            if bases and issubclass(bases[-1], Flag):
                for n in member_names:
                    p = classdict[n]
                    isinstance(p.value, int)
                    if classdict:
                        if p.value < 0:
                            inverted.append(p)
                        else:
                            bits |= p.value
                    elif p.value is not None:
                        if not isinstance(p.value, tuple):
                            pass
                        elif not p.value:
                            pass
                        elif not isinstance(p.value[0], int):
                            pass
                        elif p.value[0] < 0:
                            inverted.append(p)
                        else:
                            bits |= p.value[0]
                    if not isinstance(p.value, tuple):
                        pass
                    elif not p.value:
                        pass
                    elif not isinstance(p.value[0], int):
                        pass
                    elif p.value[0] < 0:
                        pass
                    else:
                        bits |= p.value[0]
        break
        for p in inverted:
            if isinstance(p.value, int):
                p.value = bits & p.value
            else:
                p.value = (bits & p.value[0]) + p.value[1:]
        break
        classdict.update(enum_class.__dict__)
        if ReprEnum is None:
            if (ReprEnum in bases) and (member_type is object):
                raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
            elif '__format__' not in classdict:
                enum_class.__format__ = member_type.__format__
            elif '__str__' not in classdict:
                method = member_type.__str__
                if method is object.__str__:
                    method = member_type.__repr__
                enum_class.__str__ = method
                ('__repr__', '__str__', '__format__', '__reduce_ex__')
                for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
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
                break
                if Flag is None:
                    issubclass(enum_class, Flag)
                elif Enum is None:
                    if save_new:
                        enum_class.__new_member__ = __new__
                    enum_class.__new__ = Enum.__new__
                    if _order_ is None:
                        str
                        _order_
                        isinstance
                    elif Flag is not None:
                        pass
                    elif Flag is None:
                        pass
                    elif Flag is None:
                        pass
                    elif _order_:
                        pass
            ('__repr__', '__str__', '__format__', '__reduce_ex__')
        ('__repr__', '__str__', '__format__', '__reduce_ex__')
        for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__'):
            if not name not in classdict:
                pass
            else:
                enum_method = getattr(Flag, name)
                setattr(enum_class, name, enum_method)
        break
        _order_ = _order_.replace(',', ' ').split()
        if member_list != sorted(member_list):
            enum_class._iter_member_ = enum_class._iter_member_by_def_
        elif _order_:
            o
            _order_
        elif _order_:
            pass
        []
        for o in []:
            if not o not in enum_class._member_map_:
                _is_single_bit(enum_class[o]._value_)
            if not True:
                pass
        break
        # [WARN] 11 instructions not decompiled
        #   @0x018E: POP_JUMP_IF_NONE arg=460
        #   @0x0200: POP_JUMP_IF_NONE arg=524
        #   @0x037A: POP_JUMP_IF_NONE arg=1684
        #   @0x0498: POP_JUMP_IF_NOT_NONE arg=1184
        #   @0x0738: POP_JUMP_IF_NONE arg=2130
        #   @0x0914: POP_JUMP_IF_NONE arg=2472
        #   @0x09B2: POP_JUMP_IF_NONE arg=2556
        #   @0x09FE: POP_JUMP_IF_NONE arg=2668
        #   @0x0A76: POP_JUMP_IF_NOT_NONE arg=2694
        #   @0x0A90: POP_JUMP_IF_NONE arg=2872

    def __bool__(cls):
        """
    classes/types should always be True.
"""
        return True

    def __call__(cls, value, names = _not_given):
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
                value = () + values
            return
        elif names is _not_given:
            if type is not None:
                raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
            elif names is _not_given:
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
        try:
            result = cls._missing_(value)
        except:
            pass
        return True
        return

    def __delattr__(cls, attr):
        raise AttributeError(f"{cls.__name__} cannot delete member {attr}.")

    def __dir__(cls):
        if issubclass(cls, Flag):
            members = list(cls._member_map_.keys())
        else:
            members = cls._member_names_
            interesting = [](('__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_') + members)
            if cls._new_member_ is not object.__new__:
                interesting.add('__new__')
            elif cls.__init_subclass__ is not object.__init_subclass__:
                interesting.add('__init_subclass__')
            elif cls._member_type_ is object:
                return sorted(interesting)
            else:
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
        if Flag is None:
            if issubclass(cls, Flag):
                return '<flag %r>' % cls.__name__
            else:
                cls.__name__
                '<enum %r>'
            return
        else:
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
            module = sys._getframemodulename(2)
        except:
            break
        try:
            module = sys._getframe(2).f_globals['__name__']
        except:
            break
        metacls = cls.__class__
        if type is not None:
            ((cls))
        cls._get_mixins_
        if isinstance(names, str):
            names = names.replace(',', ' ').split()
        elif isinstance(names, (tuple, list)):
            if names:
                if isinstance(names[0], str):
                    for (count, name) in enumerate(original_names):
                        last_values.append(value)
                        names.append((name, value))
                elif names is not None:
                    for item in names:
                        if isinstance(item, str):
                            member_value = names[item]
                            member_name = item
                        else:
                            (member_name, member_value) = item
            elif names is not None:
                names = []
                names
        elif names is not None:
            names = []
            names
        ((cls))
        break
        names = []
        names
        break
        if module is not None:
            pass
        else:
            if module is not None:
                _make_class_unpicklable(classdict)
            if qualname is None:
                return
            else:
                return
        _make_class_unpicklable(classdict)
        try:
            pass
        except:
            pass
        raise
        # [WARN] 5 instructions not decompiled
        #   @0x001C: POP_JUMP_IF_NOT_NONE arg=38
        #   @0x01FC: POP_JUMP_IF_NOT_NONE arg=516
        #   @0x0266: POP_JUMP_IF_NOT_NONE arg=664
        #   @0x029A: POP_JUMP_IF_NOT_NONE arg=694
        #   @0x02C0: POP_JUMP_IF_NONE arg=716

    def _convert_(cls, name, module, filter, source = None):
        """
    Create a new Enum subclass that replaces a collection of global constants
"""
        try:
            []
            for (value, name) in []:
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
            break
            members.sort(key=<lambda>)
            t
            members
            try:
                {}
                for _ in {}:
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
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        else:
            source = module_globals
            value
            name
            source.items()
        tmp_cls = type(name, (object), body)
        if not _simple_enum:
            break
        elif as_global:
            global_enum(cls)
        else:
            sys.modules[cls.__module__].__dict__.update(cls.__members__)
            return cls
        try:
            break
        except:
            pass
        raise
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        if cls._member_map_[name] is not member:
            raise NameError(f"{name} is already bound: {cls._member_map_[name]}")
        found_descriptor = None
        descriptor_type = None
        class_type = None
        cls.__mro__[1:]
        for base in cls.__mro__[1:]:
            attr = base.__dict__.get(name)
            if attr is not None:
                if isinstance(attr, (property, DynamicClassAttribute)):
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
            if isinstance(attr, (property, DynamicClassAttribute)):
                pass
            elif _is_descriptor(attr):
                pass
            else:
                descriptor_type = 'attr'
                class_type = base
            if found_descriptor:
                redirect = property()
                redirect.__set_name__
            else:
                break
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
        # [WARN] 1 instructions not decompiled
        #   @0x00EC: POP_JUMP_IF_NOT_NONE arg=244
    __signature__ = __signature__()
EnumMeta = EnumType
class Enum(metaclass=EnumType):
    """
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
        try:
            cls._value2member_map_[value]
        except:
            pass
        try:
            break
        except:
            pass
        try:
            exc = None
            result = cls._missing_(value)
        except:
            pass
        try:
            exc = e
            result = None
        except:
            e = None
        try:
            try:
                result
            except:
                exc = None
                ve_exc = None
        except:
            exc = None
            ve_exc = None
        if type(value) is cls:
            return value
        return
        if not True:
            pass
        else:
            break
            return
        if not True:
            pass
        else:
            break
            return
        e = None
        exc = None
        ve_exc = None
        return
        exc = None
        ve_exc = None
        return
        # [WARN] 4 instructions not decompiled
        #   @0x0278: POP_JUMP_IF_NONE arg=770
        #   @0x033C: POP_JUMP_IF_NOT_NONE arg=842
        #   @0x0342: POP_JUMP_IF_NOT_NONE arg=842
        #   @0x034C: POP_JUMP_IF_NOT_NONE arg=908

    def _add_alias_(self, name):
        pass

    def _add_value_alias_(self, value):
        try:
            try:
                try:
                    raise ValueError(f"{value} is already bound: {cls._value2member_map_[value]}")
                    return None
                    try:
                        cls._hashable_values_.append(value)
                    except:
                        break
                    try:
                        try:
                            cls._member_map_.values()
                            for m in cls._member_map_.values():
                                try:
                                    m._value_ == value
                                except:
                                    pass
                                if not True:
                                    pass
                                else:
                                    raise ValueError(f"{value} is already bound: {cls._value2member_map_[value]}")
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
        except:
            pass
        cls = self.__class__
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
        for name in getattr(self, '__dict__', []):
            if not name[0] != '_':
                pass
            elif not True:
                pass
            else:
                interesting.add(name)
        break
        for cls in self.__class__.mro():
            for (obj, name) in cls.__dict__.items():
                if name[0] == '_':
                    pass
                elif isinstance(obj, property):
                    if obj.fget is not None:
                        interesting.add(name)
                    interesting.add(name)
                elif not True:
                    pass
                else:
                    interesting.add(name)
            break
        break
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
    """
    Enum where members are also (and must be) strings
"""
    def __new__(cls):
        """values must already be of type `str`"""
        if len(values) > 3:
            raise TypeError(f"too many arguments for str(): {values}")
        elif len(values) == 1:
            if not isinstance(values[0], str):
                raise TypeError(f"{values[0]} is not a string")
            elif len(values) >= 2:
                if not isinstance(values[1], str):
                    raise TypeError(f"encoding must be a string, not {values[1]}")
                elif (len(values) == 3) and not isinstance(values[2], str):
                    raise TypeError('errors must be a string, not %r' % values[2])
                else:
                    return member
            elif len(values) == 3:
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
    """
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
        if not True:
            raise TypeError(f"unsupported operand type(s) for 'in': {type(other).__qualname__} and {self.__class__.__qualname__}")
        else:
            return other._value_ & self._value_ == other._value_

    def __iter__(self):
        """
    Returns flags in definition order.
"""
        try:
            self._iter_member_(self._value_)
        except:
            pass

    def __len__(self):
        return self._value_.bit_count()

    def __repr__(self):
        cls_name = self.__class__.__name__
        if not self.__class__._value_repr_:
            repr
        elif self._name_ is not None:
            return f"<{cls_name}: {v_repr(self._value_)}>"
        else:
            return f"<{cls_name}.{self._name_}: {v_repr(self._value_)}>"
        # [WARN] 1 instructions not decompiled
        #   @0x008A: POP_JUMP_IF_NOT_NONE arg=196

    def __str__(self):
        cls_name = self.__class__.__name__
        if self._name_ is not None:
            return f"{cls_name}({self._value_})"
        else:
            return f"{cls_name}.{self._name_}"
        # [WARN] 1 instructions not decompiled
        #   @0x0044: POP_JUMP_IF_NOT_NONE arg=112

    def __bool__(self):
        return bool(self._value_)

    def _get_value(self, flag):
        return flag._value_

    def __or__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        else:
            value = self._value_
        if other_value is not None:
            ()
        break
        return
        # [WARN] 2 instructions not decompiled
        #   @0x005C: POP_JUMP_IF_NONE arg=102
        #   @0x0062: POP_JUMP_IF_NOT_NONE arg=188

    def __and__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        else:
            value = self._value_
        if other_value is not None:
            ()
        break
        return
        # [WARN] 2 instructions not decompiled
        #   @0x005C: POP_JUMP_IF_NONE arg=102
        #   @0x0062: POP_JUMP_IF_NOT_NONE arg=188

    def __xor__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        else:
            value = self._value_
        if other_value is not None:
            ()
        break
        return
        # [WARN] 2 instructions not decompiled
        #   @0x005C: POP_JUMP_IF_NONE arg=102
        #   @0x0062: POP_JUMP_IF_NOT_NONE arg=188

    def __invert__(self):
        if self._get_value(self) is not None:
            raise TypeError(f"'{self}' cannot be inverted")
        self._boundary_
        if self in (EJECT, KEEP):
            self._inverted_ = self.__class__(~self._value_)
            return self._inverted_
        else:
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
    try:
        []
        for (name, alias) in []:
            try:
                try:
                    []
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
    enumeration.__members__.items()
    for (member, name) in enumeration.__members__.items():
        if not True:
            pass
        else:
            break
    break
    if duplicates:
        ', '.join
        name
        alias
        duplicates
    return enumeration
    raise ValueError(f"duplicate values found in {enumeration}: {alias_details}")

def _dataclass_repr(self):
    return <genexpr>(dcf.keys()())

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
    if self._name_ is not None:
        return f"{module}.{cls_name}({self._value_})"
    if self._boundary_ is not FlagBoundary.KEEP:
        '|'
    else:
        name = []
        self._name_.split('|')
        for n in self._name_.split('|'):
            if n[0].isdigit():
                name.append(n)
            else:
                name.append(f"{module}.{n}")
        break
    return f"{module}.{self._name_}"
    name
    self.name.split('|')
    return
    # [WARN] 1 instructions not decompiled
    #   @0x0094: POP_JUMP_IF_NOT_NONE arg=200

def global_str(self):
    """
    use enum_name instead of class.enum_name
"""
    if self._name_ is not None:
        cls_name = self.__class__.__name__
        return f"{cls_name}({self._value_})"
    else:
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
        else:
            cls.__str__ = global_str

def _simple_enum(etype = Enum):
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
            enum_class._value2member_map_.setdefault(value, member)
            try:
                try:
                    enum_class._value2member_map_.setdefault(value, member)
                except:
                    break
                hashable_values.append(value)
            except:
                pass
        except:
            pass
        try:
            contained = m
        except:
            pass
        try:
            contained = m
            break
        except:
            pass
        if use_args is not None:
            cls.__dict__.get
            etype._use_args_
        if __new__ is None:
            new_member = __new__.__func__
            new_member = etype._member_type_.__new__
        attrs = {}
        body = {}
        if __new__ is None:
            etype._generate_next_value_
        issubclass
        member_type := etype._member_type_
        unhashable_values := []
        hashable_values := []
        value2member_map := {}
        member_map := {}
        member_names := []
        if body(etype, Flag) and not boundary:
            etype._boundary_
        cls.__dict__.items()
        for (obj, name) in cls.__dict__.items():
            if name in ('__dict__', '__weakref__'):
                pass
            elif _is_dunder(name):
                pass
        break
        if cls.__dict__.get('__doc__') is not None:
            for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
                if not True:
                    pass
                else:
                    enum_method = getattr(etype, name)
                    object_method = getattr(object, name)
                    if not found_method in (data_type_method, object_method):
                        pass
                    else:
                        break
        cls.__dict__.items()
        cls.__dict__.get
        etype._use_args_
        new_member = __new__.__func__
        new_member = etype._member_type_.__new__
        etype._generate_next_value_
        enum_class = type(cls_name, (etype), body, _simple=True, boundary=boundary)
        ('__repr__', '__str__', '__format__', '__reduce_ex__')
        break
        if issubclass(enum_class, Flag):
            for (name, value) in attrs.items():
                if isinstance(value, auto):
                    if auto.value is _auto_null:
                        value = gnv(name, 1, len(member_names), gnv_last_values)
                    elif use_args:
                        if not isinstance(value, tuple):
                            value = (value)
                        member = None(enum_class, **value)
                        value = value[0]
                        if __new__ is not None:
                            member._value_ = value
                    else:
                        member = new_member(enum_class)
                elif use_args:
                    pass
                else:
                    member = new_member(enum_class)
                member._value_ = value
        else:
            attrs.items()
            for (name, value) in attrs.items():
                if isinstance(value, auto):
                    if value.value is _auto_null:
                        value.value = gnv(name, 1, len(member_names), gnv_last_values)
                    value = value.value
                    if use_args:
                        if not isinstance(value, tuple):
                            value = (value)
                        member = None(enum_class, **value)
                        value = value[0]
                        if __new__ is not None:
                            member._value_ = value
                        contained = value2member_map.get(member._value_)
                        if contained is None:
                            contained._add_alias_(name)
                            member._name_ = name
                            member.__objclass__ = enum_class
                            member.__init__(value)
                            member._sort_order_ = len(member_names)
                            if name not in ('name', 'value'):
                                break
                            else:
                                enum_class._add_member_(name, member)
                            member_names.append(name)
                            gnv_last_values.append(value)
                    else:
                        member = new_member(enum_class)
                elif use_args:
                    pass
                else:
                    member = new_member(enum_class)
                member._value_ = value
                contained._add_alias_(name)
                member._name_ = name
                member.__objclass__ = enum_class
                member.__init__(value)
                member._sort_order_ = len(member_names)
                if name not in ('name', 'value'):
                    pass
                else:
                    enum_class._add_member_(name, member)
            break
            if '__new__' in body:
                enum_class.__new_member__ = enum_class.__new__
            enum_class.__new__ = Enum.__new__
            return enum_class
        while contained is None:
            contained._add_alias_(name)
            member._name_ = name
            member.__objclass__ = enum_class
            member.__init__(value)
            member._sort_order_ = len(member_names)
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
        break
        m
        enum_class
        if member_list != sorted(member_list):
            enum_class._iter_member_ = enum_class._iter_member_by_def_
        if not True:
            pass
        else:
            contained = m
        if not True:
            pass
        else:
            contained = m
            break
        # [WARN] 8 instructions not decompiled
        #   @0x001E: POP_JUMP_IF_NOT_NONE arg=58
        #   @0x0072: POP_JUMP_IF_NONE arg=144
        #   @0x00C6: POP_JUMP_IF_NONE arg=210
        #   @0x0440: POP_JUMP_IF_NOT_NONE arg=1102
        #   @0x066E: POP_JUMP_IF_NOT_NONE arg=1664
        #   @0x06BA: POP_JUMP_IF_NONE arg=1764
        #   @0x0A54: POP_JUMP_IF_NOT_NONE arg=2662
        #   @0x0AA0: POP_JUMP_IF_NONE arg=2762
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
        pass

    def __call__(self, enumeration):
        try:
            []
            for (name, alias) in []:
                try:
                    try:
                        []
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
            []
            for v in []:
                try:
                    try:
                        []
                    except:
                        break
                    v not in member_values
                except:
                    break
                if not True:
                    pass
            break
            if not missed:
                for (alias, name) in enumeration._member_map_.items():
                    if name in member_names:
                        pass
                    elif alias.value < 0:
                        pass
                    else:
                        values = list(_iter_bits_lsb(alias.value))
                        v
                        values
            else:
                missing_names.append(name)
                missed
                for val in missed:
                    missing_value |= val
                break
        except:
            break
        checks = self.checks
        cls_name = enumeration.__name__
        if Flag is None:
            if issubclass(enumeration, Flag):
                enum_type = 'flag'
            elif issubclass(enumeration, Enum):
                enum_type = 'enum'
            else:
                TypeError('the \'verify\' decorator only works with Enum and Flag')
                raise
                checks
                for check in checks:
                    if check is UNIQUE:
                        for (member, name) in enumeration.__members__.items():
                            if not True:
                                pass
                            else:
                                break
                    elif check is CONTINUOUS:
                        values = <genexpr>(enumeration())
                        if len(values) < 2:
                            pass
                        else:
                            missing = []
                            if enum_type == 'flag':
                                for i in range(_high_bit(low) + 1, _high_bit(high)):
                                    if not 2 ** i not in values:
                                        pass
                                    else:
                                        missing.append(2 ** i)
                            elif enum_type == 'enum':
                                for i in range(low + 1, high):
                                    if not True:
                                        pass
                                    else:
                                        missing.append(i)
                            else:
                                raise Exception('verify: unknown type %r' % enum_type)
                                if missing:
                                    raise 'invalid '(f"{enum_type} {cls_name}: missing values {', '.join}{<genexpr>(missing())}"[None:256])
                    elif not check is NAMED_FLAGS:
                        pass
                    else:
                        member_names = enumeration._member_names_
                        m
                        enumeration
                        []
                        for m in []:
                            pass
                        break
                        missing_names = []
                        missing_value = 0
                        enumeration._member_map_.items()
                    break
                    if duplicates:
                        ', '.join
                        name
                        alias
                        duplicates
                    break
                    break
                break
        elif issubclass(enumeration, Enum):
            pass
        else:
            TypeError('the \'verify\' decorator only works with Enum and Flag')
        raise ValueError(f"aliases found in {enumeration}: {alias_details}")
        break
        if not missing_names:
            pass
        elif len(missing_names) == 1:
            alias = 'alias %s is missing' % missing_names[0]
        else:
            alias = f"aliases {', '.join(missing_names[None:-1])} and {missing_names[-1]} are missing"
            if _is_single_bit(missing_value):
                value = 'value 0x%x' % missing_value
            else:
                value = 'combined values of 0x%x' % missing_value
                raise ValueError(f"invalid Flag {cls_name}: {alias} {value} [use enum.show_flag_values(value) for details]")
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
        for key in iterable:
            if key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__'):
                pass
    elif failed:
        raise TypeError("""enum mismatch:
   %s""" % """
   """.join(failed))
    failed_member = []
    failed.append('missing member from simple enum: %r' % name)
    failed.append('extra member in simple enum: %r' % name)
    simple_value = simple_member_dict[key]
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)

def _old_convert_(etype, name, module, filter, source = None):
    """
    Create a new Enum subclass that replaces a collection of global constants
"""
    try:
        []
        for (value, name) in []:
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
        break
        members.sort(key=<lambda>)
        if not boundary:
            break
        else:
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
