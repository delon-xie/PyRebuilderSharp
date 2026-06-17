# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType
from types import DynamicClassAttribute
__all__ = ('EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin')
class nonmember:
    'nonmember'
    __module__ = __name__
    __qualname__ = 'nonmember'
    __doc__ = """
    Protects item from becoming an Enum member during class creation.
    """
    def __init__(self, value):
        self.value = value
class member:
    'member'
    __module__ = __name__
    __qualname__ = 'member'
    __doc__ = """
    Forces item to become an Enum member during class creation.
    """
    def __init__(self, value):
        self.value = value
def _is_descriptor(obj):
    """
    Returns True if obj is a descriptor, False otherwise.
    """
    if hasattr(obj, '__get__'):
        if hasattr(obj, '__set__'):
            return hasattr(obj, '__delete__')
def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    if not len(name) > 4:
        if not name[-2:] == name[-2:]:
            pass
    # orphan @0x0032
    # orphan @0x0034
    # orphan @0x0040
    return name[-3] != '_'
    # orphan @0x007E
    # orphan @0x008A
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
    if hasattr(obj, '__get__'):
        if hasattr(obj, '__set__'):
            return hasattr(obj, '__delete__')
def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    if not len(name) > 4:
        if not name[-2:] == name[-2:]:
            pass
    # orphan @0x0032
    # orphan @0x0034
    # orphan @0x0040
    return name[-3] != '_'
    # orphan @0x007E
    # orphan @0x008A
def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
    """
    if not len(name) > 2:
        if not name[-1] == name[-1]:
            pass
    # orphan @0x002A
    # orphan @0x002C
    # orphan @0x0038
    return name[-2] != '_'
    # orphan @0x006E
    # orphan @0x007A
def _is_internal_class(cls_name, obj):
    # orphan @0x000E
    if not isinstance(obj, type):
        return False
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if qualname == s_pattern:
        return qualname.endswith(e_pattern)
def _is_private(cls_name, name):
    pattern = '_%s__' % (cls_name)
    pat_len = len(pattern)
    if len(name) > pat_len:
        if name.startswith(pattern):
            if not name[-1] != '_':
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
    return num == 0
    # orphan @0x000C
def _make_class_unpicklable(obj):
    """
    Make the given obj un-picklable.

    obj should be either a dictionary, or an Enum
    """
    def _break_on_call_reduce(self, proto):
        raise TypeError('%r cannot be pickled' % self)
    if isinstance(obj, dict):
        return None
    # orphan @0x0026
    setattr(obj, '__reduce_ex__', _break_on_call_reduce)
def _iter_bits_lsb(num):
    original = num
    if isinstance(num, Enum):
        num = num.value
        if num < 0:
            pass
        elif not num:
            return None
    raise
    if num:
        b = num & ~num + 1
        yield b
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
        s = bltns.bin(~num ^ ceiling - 1 + ceiling)
    digits = s[3:]
    if max_bits is not None:
        if len(digits) < max_bits:
            digits = sign[-1] * max_bits + digits[-max_bits:]
            return '%s %s' % (sign, digits)
    # orphan @0x004E
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
    def __get__(self, instance, ownerclass):
        # orphan @0x0018
        raise AttributeError('%r has no attribute %r' % (ownerclass, self.name))
        if instance is None:
            if self.member is not None:
                return self.member
            elif True:
                return self.fget(instance)
        # orphan @0x003E
        # orphan @0x0048
        return getattr(self._cls_type, self.name)
        # orphan @0x0056
        # orphan @0x0060
        return getattr(instance._value_, self.name)
        # orphan @0x006E
        # orphan @0x0122
    def __set__(self, instance, value):
        if self.fset is not None:
            return self.fset(instance, value)
        raise
        # orphan @0x0016
    def __delete__(self, instance):
        if self.fdel is not None:
            return self.fdel(instance)
        raise
        # orphan @0x0014
    def __get__(self, instance, ownerclass):
        # orphan @0x0018
        raise AttributeError('%r has no attribute %r' % (ownerclass, self.name))
        if instance is None:
            if self.member is not None:
                return self.member
            elif True:
                return self.fget(instance)
        # orphan @0x003E
        # orphan @0x0048
        return getattr(self._cls_type, self.name)
        # orphan @0x0056
        # orphan @0x0060
        return getattr(instance._value_, self.name)
        # orphan @0x006E
        # orphan @0x0122
    def __set__(self, instance, value):
        if self.fset is not None:
            return self.fset(instance, value)
        raise
        # orphan @0x0016
    def __delete__(self, instance):
        if self.fdel is not None:
            return self.fdel(instance)
        raise
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
        # orphan @0x00B2
        value = enum_member._value_
        enum_member._name_ = member_name
        enum_member.__objclass__ = enum_class
        enum_member._sort_order_ = len(enum_class._member_names_)
        # orphan @0x00A8
        exc = None
        raise
        # orphan @0x0088
        Exception
        new_exc = TypeError('_value_ not set in __new__, unable to create it')
        new_exc.__cause__ = exc
        raise new_exc
        # orphan @0x0084
        # orphan @0x006E
        enum_member._value_ = value
        # orphan @0x0066
        # orphan @0x0030
        args = (args)
        # orphan @0x0026
        delattr(enum_class, member_name)
        value = self.value
        if not isinstance(value, tuple):
            args = (value)
            args = value
        enum_member = enum_class._new_member_(enum_class)
        enum_member = enum_class._new_member_(enum_class, **args)
        if not hasattr(enum_member, '_value_'):
            pass
        enum_class._all_bits_ = 2 ** enum_class._flag_mask_.bit_length() - 1
        try:
            try:
                enum_member = enum_class._value2member_map_[value]
            except:
                pass
        except KeyError:
            enum_class._member_names_.append(member_name)
            enum_class._member_names_.append(member_name)
        enum_class._add_member_(member_name, enum_member)
        try:
            enum_class._value2member_map_.setdefault(value, enum_member)
            if value not in enum_class._hashable_values_:
                pass
            return
        except TypeError:
            enum_class._unhashable_values_map_.setdefault(member_name, []).append(value)
        raise
        # orphan @0x00E2
        # orphan @0x00E4
        # orphan @0x00EC
        # orphan @0x00F6
        value._flag_mask_ = enum_class._flag_mask_
        # orphan @0x010C
        # orphan @0x0140
        TypeError
        # orphan @0x0156
        # orphan @0x0158
        # orphan @0x0168
        enum_member = canonical_member
        # orphan @0x0172
        raise KeyError
        # orphan @0x0176
        raise
        # orphan @0x017C
        # orphan @0x0210
        # orphan @0x02D8
        # orphan @0x0366
        # orphan @0x0480
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
        # orphan @0x00D2
        # orphan @0x00CA
        raise
        # orphan @0x00C6
        # orphan @0x00C4
        # orphan @0x00A8
        self._ignore = value
        already = set(value) & set(self._member_names)
        # orphan @0x006A
        # orphan @0x0062
        # orphan @0x0058
        # orphan @0x0050
        raise TypeError('_generate_next_value_ must be defined before members')
        # orphan @0x004A
        # orphan @0x0042
        if self._cls_name is not None:
            if _is_private(self._cls_name, key):
                if _is_sunder(key):
                    pass
                raise
                if key in self._ignore:
                    if isinstance(value, nonmember):
                        value = value.value
                        if _is_descriptor(value):
                            if self._cls_name is not None:
                                if _is_internal_class(self._cls_name, value):
                                    if key in self:
                                        pass
                            break
                        else:
                            raise
                            if non_auto_store:
                                self._last_values.append(value)
                    else:
                        TypeError
                elif single:
                    value = auto_valued[0]
                    try:
                        value = t(auto_valued)
                    except TypeError:
                        pass
            elif not True:
                raise ValueError('_sunder_ names, such as %r, are reserved for future Enum use' % (key))
            elif key == '_ignore_':
                if isinstance(value, str):
                    value = value.replace(',', ' ').split()
                    value = list(value)
        elif True:
            pass
        # orphan @0x00DC
        # orphan @0x00E4
        key = '_order_'
        # orphan @0x00F4
        # orphan @0x0196
        # orphan @0x019C
        # orphan @0x01B0
        auto_valued = []
        t = type(value)
        # orphan @0x01C0
        # orphan @0x01C2
        # orphan @0x01C6
        # orphan @0x01CC
        # orphan @0x01D0
        non_auto_store = False
        # orphan @0x01E0
        # orphan @0x01FC
        self._auto_called = True
        v = v.value
        self._last_values.append(v)
        auto_valued.append(v)
        # orphan @0x027C
        # orphan @0x03E8
        # orphan @0x03EA
        # orphan @0x03FC
        # orphan @0x0410
        # orphan @0x04AA
        @property
def member_names(self):
        return list(self._member_names)
    def update(self, members):
        # orphan @0x001C
        try:
            for name in name:
                pass
        except AttributeError:
            pass
        for (name, value) in name:
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
            return enum_dict
    def __new__(metacls, cls, bases, classdict):
        # orphan @0x01CE
        p = classdict[n]
        # orphan @0x01CC
        # orphan @0x01C0
        bits = 0
        inverted = []
        # orphan @0x01B0
        # orphan @0x01AA
        # orphan @0x019C
        # orphan @0x00CA
        (member_type, first_enum) = metacls._get_mixins_(cls, bases)
        # orphan @0x00AE
        _gnv = staticmethod(_gnv)
        classdict = dict(classdict.items())
        # orphan @0x00A2
        # orphan @0x0084
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        # orphan @0x001E
        if _simple:
            return super().__new__(metacls, cls, bases, classdict, **kwds)
        ignore = classdict['_ignore_']
        for key in ignore:
            classdict.pop(key, None)
        member_names = classdict._member_names
        invalid_names = set(member_names) & # Unknown node: SetLiteral
        if invalid_names:
            raise ValueError('invalid enum member name(s) %s' % ','.join(EnumType.__new__.<locals>.<genexpr>(invalid_names)))
        for name in name:
            value = classdict[name]
        if boundary:
            pass
        break
        break
        if ReprEnum is not None:
            if ReprEnum in bases:
                if member_type is object:
                    raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
        # orphan @0x01E6
        # orphan @0x01F0
        inverted.append(p)
        bits = p.value
        # orphan @0x0214
        # orphan @0x0224
        # orphan @0x022C
        # orphan @0x023E
        # orphan @0x024E
        inverted.append(p)
        bits = p.value[0]
        # orphan @0x026A
        # orphan @0x026E
        # orphan @0x0270
        # orphan @0x0280
        p.value = bits & p.value
        p.value = (bits & p.value[0]) + p.value[1:]
        # orphan @0x02B4
        # orphan @0x02FA
        Exception
        # orphan @0x0316
        raise
        # orphan @0x031C
        def <genexpr>(.0):
            for n in .0:
                yield repr(n)
                break
        raise
        # orphan @0x0358
        # orphan @0x0362
        # orphan @0x037E
        method = member_type.__str__
        # orphan @0x0390
        method = member_type.__repr__
        # orphan @0x03AA
        # orphan @0x03AC
        # orphan @0x03B8
        enum_method = getattr(first_enum, name)
        object_method = getattr(object, name)
        data_type_method = getattr(member_type, name)
        # orphan @0x03EC
        # orphan @0x03EE
        # orphan @0x03FE
        # orphan @0x0408
        # orphan @0x0414
        # orphan @0x0418
        # orphan @0x041A
        # orphan @0x0426
        # orphan @0x042A
        # orphan @0x0448
        # orphan @0x0452
        # orphan @0x0458
        # orphan @0x045E
        # orphan @0x0464
        # orphan @0x0470
        # orphan @0x0474
        # orphan @0x047C
        _order_ = _order_.replace(',', ' ').split()
        # orphan @0x048C
        # orphan @0x0494
        # orphan @0x0496
        # orphan @0x04A0
        # orphan @0x04A6
        # orphan @0x04A8
        # orphan @0x04AA
        # orphan @0x04B6
        # orphan @0x04F4
        # orphan @0x0500
        # orphan @0x0510
        # orphan @0x051C
        # orphan @0x052A
        _order_ = EnumType.__new__.<locals>.<listcomp>(_order_)
        # orphan @0x053C
        # orphan @0x0542
        _order_ = EnumType.__new__.<locals>.<listcomp>(_order_)
        # orphan @0x0560
        raise
        # orphan @0x0572
        return
        # orphan @0x0626
        # orphan @0x0630
        # orphan @0x06D6
        # orphan @0x0724
        # orphan @0x0726
        # orphan @0x07B2
        # orphan @0x07E8
        # orphan @0x0850
        # orphan @0x085C
        # orphan @0x086A
        # orphan @0x08B6
        # orphan @0x08B8
        # orphan @0x08FC
        # orphan @0x0908
        # orphan @0x0936
        # orphan @0x0956
        # orphan @0x0994
        # orphan @0x09A0
        # orphan @0x0A30
        # orphan @0x0A3C
        # orphan @0x0A40
        # orphan @0x0A66
        # orphan @0x0AB4
        # orphan @0x0AD2
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
            if names is not _not_given:
                value = (value, names) + values
                return cls.__new__(cls, value)
            elif True:
                if type is None:
                    raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
        # orphan @0x0026
        # orphan @0x0044
        # orphan @0x0052
        # orphan @0x0058
        return
        # orphan @0x00A8
    def __contains__(cls, value):
        """Return True if `value` is in `cls`.

        `value` is in `cls` if:
        1) `value` is a member of `cls`, or
        2) `value` is the value of one of the `cls`'s members.
        3) `value` is a pseudo-member (flags)
        """
        # orphan @0x000E
        if isinstance(value, cls):
            return True
        try:
            result = cls._missing_(value)
        except ValueError:
            pass
        return
        return
        if value in cls._unhashable_values_:
            return value in cls._hashable_values_
        # orphan @0x005A
        # orphan @0x0076
    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError('%r cannot delete member %r.' % (cls.__name__, attr))
        # orphan @0x001C
    def __dir__(cls):
        # orphan @0x0020
        if issubclass(cls, Flag):
            members = list(cls._member_map_.keys())
            members = cls._member_names_
        elif cls._new_member_ is not object.__new__:
            interesting.add('__new__')
            if cls.__init_subclass__ is not object.__init_subclass__:
                interesting.add('__init_subclass__')
                if cls._member_type_ is object:
                    return sorted(interesting)
        # orphan @0x006E
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
        if Flag is not None:
            if issubclass(cls, Flag):
                return '<flag %r>' % cls.__name__
        return
        # orphan @0x001C
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
        # orphan @0x001A
        metacls = cls.__class__
        if type is None:
            pass
        classdict = metacls.__prepare__(class_name, bases)
        if isinstance(names, str):
            names = names.replace(',', ' ').split()
            if isinstance(names, (tuple, list)):
                if names:
                    if isinstance(names[0], str):
                        original_names = []
                        names = names
                        last_values = []
                    raise
                    if module is None:
                        _make_class_unpicklable(classdict)
                try:
                    pass
                except AttributeError:
                    ()
        last_values.append(value)
        names.append((name, value))
        for (count, name) in enumerate(original_names):
            pass
        if names is None:
            for item in member_name:
                if isinstance(item, str):
                    member_name = names[item]
                    member_value = item
                    (member_name, member_value) = item
        # orphan @0x0102
        # orphan @0x010A
        module = sys._getframemodulename(2)
        # orphan @0x011A
        AttributeError
        # orphan @0x0174
        # orphan @0x017C
        return metacls.__new__(metacls, class_name, bases, classdict, boundary=boundary)
        # orphan @0x0264
        # orphan @0x0278
        # orphan @0x029A
        # orphan @0x0300
    def _convert_(cls, name, module, filter, source):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        # orphan @0x001C
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
            source = module_globals
        try:
            members.sort(key=EnumType._convert_.<locals>.<lambda>)
        except TypeError:
            pass
        body = EnumType._convert_.<locals>.<dictcomp>(members)
        tmp_cls = type(name, (object), body)
        if boundary:
            if as_global:
                global_enum(cls)
        # orphan @0x00B6
        # orphan @0x00C6
        return cls
        @classmethod
def _check_for_existing_members_(mcls, class_name, bases):
        for chain in bases:
            for base in chain.__mro__:
                if isinstance(base, EnumType):
                    if base._member_names_:
                        raise TypeError('<enum %r> cannot extend %r' % (class_name, base))
        @classmethod
def _get_mixins_(mcls, class_name, bases):
        """
        Returns the type for creating enum members, and the first inherited
        enum class.

        bases: the tuple of bases that was given to __new__
        """
        # orphan @0x000C
        if not bases:
            return (object, Enum)
        elif not isinstance(first_enum, EnumType):
            raise TypeError('new enumerations should be created as `EnumName([mixin_type, ...] [data_type,] enum_type)`')
        # orphan @0x0026
        # orphan @0x0032
        member_type = object
        return (member_type, first_enum)
        # orphan @0x0066
        @classmethod
def _find_data_repr_(mcls, class_name, bases):
        for chain in bases:
            for base in chain.__mro__:
                if base is object:
                    continue
                    if isinstance(base, EnumType):
                        base._value_repr_
                        break
                    elif True:
                        _dataclass_repr
                        break
                elif True:
                    if '__dataclass_fields__' in base.__dict__:
                        if '__dataclass_params__' in base.__dict__:
                            pass
                base.__dict__['__repr__']
                break
        @classmethod
def _find_data_type_(mcls, class_name, bases):
        data_types = set()
        base_chain = set()
        for chain in bases:
            for base in chain.__mro__:
                base_chain.add(base)
                if base is object:
                    continue
                    if isinstance(base, EnumType):
                        if base._member_type_ is not object:
                            data_types.add(base._member_type_)
                            break
                            if not '__new__' in base.__dict__:
                                pass
                        raise
                        if data_types:
                            return data_types.pop()
                elif True:
                    if candidate:
                        break
                        if candidate:
                            candidate = base
        if len(data_types) > 1:
            pass
        @classmethod
def _find_new_(mcls, classdict, member_type, first_enum):
        """
        Returns the __new__ to be used for creating the enum members.

        classdict: the class dictionary given to __new__
        member_type: the data type whose __new__ will be used by default
        first_enum: enumeration to check for an overriding __new__
        """
        # orphan @0x002A
        # orphan @0x0028
        __new__ = classdict.get('__new__', None)
        if not first_enum is not None:
            save_new = __new__ is not None
            if __new__ is None:
                pass
            return (save_new, use_args)
        for possible in (first_enum):
            target = getattr(possible, method, None)
            if target not in # Unknown node: SetLiteral:
                __new__ = target
                break
        if __new__ is not None:
            break
        # orphan @0x0072
        __new__ = object.__new__
        # orphan @0x0078
        # orphan @0x0080
        # orphan @0x0090
        use_args = False
        use_args = True
        # orphan @0x009A
        # orphan @0x0110
        # orphan @0x0126
    def _add_member_(cls, name, member):
        # orphan @0x0032
        found_descriptor = None
        descriptor_type = None
        if name in cls._member_map_:
            if cls._member_map_[name] is not member:
                raise NameError('%r is already bound: %r' % (name, cls._member_map_[name]))
            for base in None:
                attr = base.__dict__.get(name)
                if attr is not None:
                    if isinstance(attr, (property, DynamicClassAttribute)):
                        found_descriptor = attr
                        class_type = base
                        descriptor_type = 'enum'
                        break
                        if _is_descriptor(attr):
                            found_descriptor = attr
                            if descriptor_type:
                                descriptor_type = 'desc'
                                if class_type:
                                    class_type = base
                                    continue
                                break
                    redirect._set = getattr(found_descriptor, '__set__', None)
                    redirect._del = getattr(found_descriptor, '__delete__', None)
            if found_descriptor:
                redirect = property()
                redirect.member = member
                redirect.__set_name__(cls, name)
                if descriptor_type in ('enum', 'desc'):
                    redirect.fget = getattr(found_descriptor, 'fget', None)
                    redirect._get = getattr(found_descriptor, '__get__', None)
        @property
def __signature__(cls):
        # orphan @0x0028
        from inspect import Parameter
        from inspect import Signature
        if cls._member_names_:
            return Signature([Parameter('values', Parameter.VAR_POSITIONAL)])
        return
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
        # orphan @0x0010
        if type(value) is cls:
            return value
        return
        KeyError
        TypeError
        for (name, unhashable_values) in cls._unhashable_values_map_.items():
            if True:
                cls[name]
                return
            raise
            raise TypeError('%r has no members defined' % cls)
            try:
                pass
            except Exception:
                exc = e
                result = None
            try:
                if isinstance(result, cls):
                    exc = None
                    ve_exc = None
                    return
                if Flag is not None:
                    if issubclass(cls, Flag):
                        if cls._boundary_ is EJECT:
                            if isinstance(result, int):
                                exc = None
                                ve_exc = None
                                return
                ve_exc = ValueError('%r is not a valid %s' % (value, cls.__qualname__))
                if True:
                    if exc is None:
                        raise ve_exc
                if exc is None:
                    exc = TypeError('error in %s._missing_: returned %r instead of None or a valid member' % (cls.__name__, result))
                    if not isinstance(exc, ValueError):
                        exc.__context__ = ve_exc
                        raise exc
            finally:
                exc = None
                ve_exc = None
                raise
        for (name, member) in cls._member_map_.items():
            if value == member._value_:
                cls[name]
                return
        raise
        if not cls._member_map_:
            if getattr(cls, '_%s__in_progress' % cls.__name__, False):
                pass
        # orphan @0x00CC
        result = cls._missing_(value)
        # orphan @0x00FE
        e = None
        raise
    def _add_alias_(self, name):
        self.__class__._add_member_(name, self)
    def _add_value_alias_(self, value):
        # orphan @0x003C
        cls = self.__class__
        try:
            if value in cls._value2member_map_:
                if cls._value2member_map_[value] is not self:
                    raise ValueError('%r is already bound: %r' % (value, cls._value2member_map_[value]))
                for m in cls:
                    if m._value_ == value:
                        if m is not self:
                            raise ValueError('%r is already bound: %r' % (value, cls._value2member_map_[value]))
                    break
                raise
                try:
                    cls._value2member_map_.setdefault(value, self)
                    cls._hashable_values_.append(value)
                except TypeError:
                    cls._unhashable_values_map_.setdefault(self.name, []).append(value)
                raise
        except TypeError:
            pass
        # orphan @0x01A2
        @staticmethod
def _generate_next_value_(name, start, count, last_values):
        """
        Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_values: the list of values assigned
        """
        # orphan @0x001A
        TypeError
        raise TypeError('unable to sort non-numeric values') from None
        # orphan @0x0008
        if not last_values:
            return start
        try:
            pass
        except TypeError:
            raise
            raise
        return
        return
        raise
        # orphan @0x0030
        raise
        @classmethod
def _missing_(cls, value):
        pass
    def __repr__(self):
        if self.__class__._value_repr_:
            v_repr = repr
        return (self._name_, v_repr(self._value_))
    def __str__(self):
        return '%s.%s' % (self.__class__.__name__, self._name_)
    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        # orphan @0x0030
        # orphan @0x002E
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
        elif True:
            if name not in self._member_map_:
                interesting.add(name)
            elif True:
                interesting.add(name)
                interesting.discard(name)
                if name not in self._member_map_:
                    interesting.add(name)
        elif not True:
            pass
        # orphan @0x0054
        # orphan @0x005E
        # orphan @0x0060
        # orphan @0x006C
        # orphan @0x006E
        # orphan @0x0080
        # orphan @0x008C
        # orphan @0x00CE
        # orphan @0x00D0
        names = set([](('__class__', '__doc__', '__eq__', '__hash__', '__module__')) | interesting)
        return names
        # orphan @0x0102
        # orphan @0x0144
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
        'The name of the Enum member.'
        return self._name_
        @property
def value(self):
        'The value of the Enum member.'
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
        'values must already be of type `str`'
        # orphan @0x001A
        if len(values) > 3:
            raise TypeError('too many arguments for str(): %r' % (values))
        elif not isinstance(values[0], str):
            raise TypeError('%r is not a string' % (values[0]))
        elif True:
            if not isinstance(values[2], str):
                raise TypeError('errors must be a string, not %r' % values[2])
        # orphan @0x0046
        # orphan @0x0052
        # orphan @0x0060
        # orphan @0x006C
        raise
        # orphan @0x0072
        # orphan @0x009C
        member = str.__new__(cls, value)
        member._value_ = value
        return member
        # orphan @0x00C4
        # orphan @0x00D2
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
        # orphan @0x0010
        return 1
        if not count:
            if start is not None:
                return start
            try:
                high_bit = _high_bit(last_value)
            except Exception:
                raise
                raise
                return 2 ** (high_bit + 1)
            return 2 ** (high_bit + 1)
            raise
        @classmethod
def _iter_member_by_value_(cls, value):
        """
        Extract all members from the value in definition (i.e. increasing value) order.
        """
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
        # orphan @0x00C8
        value = max(all_bits + 1, 2 ** value.bit_length()) + value
        raise ValueError('%r unknown flag boundary %r' % (cls, cls._boundary_))
        # orphan @0x00C0
        # orphan @0x00B6
        # orphan @0x0062
        max_bits = max(value.bit_length(), flag_mask.bit_length())
        # orphan @0x0058
        # orphan @0x004C
        # orphan @0x001C
        flag_mask = cls._flag_mask_
        if not isinstance(value, int):
            raise ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        all_bits = cls._all_bits_
        def <listcomp>(.0):
            for m in m._name_:
                pass
            return
        if value <= value:
            if True:
                pass
            value &= flag_mask
            if cls._boundary_ is EJECT:
                return value
            raise
            if cls._member_type_ is object:
                pseudo_member = object.__new__(cls)
                pseudo_member = cls._member_type_.__new__(cls, value)
        raise
        if cls._boundary_ is CONFORM:
            pass
        elif True:
            pass
        # orphan @0x00F6
        # orphan @0x00FE
        neg_value = value
        # orphan @0x0110
        value = all_bits + 1 + value
        value = singles_mask & value
        # orphan @0x0126
        unknown = value & ~flag_mask
        aliases = value & ~singles_mask
        member_value = value & singles_mask
        # orphan @0x018E
        # orphan @0x0198
        pseudo_member._value_ = value
        # orphan @0x01A2
        # orphan @0x01A4
        # orphan @0x01A8
        # orphan @0x01AA
        combined_value = 0
        # orphan @0x01BA
        # orphan @0x01BC
        members.append(m)
        combined_value = m._value_
        # orphan @0x01D4
        # orphan @0x01DA
        value = member_value | aliases
        # orphan @0x01EC
        # orphan @0x01EE
        # orphan @0x01FE
        # orphan @0x0206
        # orphan @0x0218
        members.append(pm)
        # orphan @0x0224
        combined_value = pm._value_
        # orphan @0x022E
        unknown = value ^ combined_value
        pseudo_member._name_ = '|'.join(Flag._missing_.<locals>.<listcomp>(members))
        # orphan @0x0252
        pseudo_member._name_ = None
        # orphan @0x0260
        # orphan @0x026C
        raise ValueError('%r: no members with value %r' % (cls, unknown))
        # orphan @0x027C
        # orphan @0x0282
        pseudo_member._name_ + '|%s' % cls._numeric_repr_(unknown)._name_ = pseudo_member
        pseudo_member._name_ = None
        # orphan @0x02A2
        pseudo_member = cls._value2member_map_.setdefault(value, pseudo_member)
        # orphan @0x02B0
        # orphan @0x0336
        # orphan @0x034A
        # orphan @0x0408
        # orphan @0x042A
        # orphan @0x0432
        # orphan @0x0444
        # orphan @0x04AC
        # orphan @0x04DC
        # orphan @0x04E8
        # orphan @0x051C
        # orphan @0x057E
    def __contains__(self, other):
        """
        Returns True if self has at least the same flags set as other.
        """
        if not isinstance(other, self.__class__):
            raise TypeError('unsupported operand type(s) for \'in\': %r and %r' % (type(other).__qualname__, self.__class__.__qualname__))
        return
        # orphan @0x0026
    def __iter__(self):
        """
        Returns flags in definition order.
        """
        yield from self._iter_member_(self._value_)
    def __len__(self):
        return self._value_.bit_count()
    def __repr__(self):
        cls_name = self.__class__.__name__
        if self.__class__._value_repr_:
            v_repr = repr
            if self._name_ is None:
                pass
        return (v_repr(self._value_))
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
        elif True:
            return flag
        # orphan @0x0012
        # orphan @0x001C
        # orphan @0x002C
        return NotImplemented
        # orphan @0x0048
    def __or__(self, other):
        # orphan @0x0016
        value = self._value_
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        elif True:
            pass
        # orphan @0x0024
        # orphan @0x0034
        # orphan @0x0036
        # orphan @0x0046
        # orphan @0x0050
        raise
        # orphan @0x0056
        # orphan @0x0058
        return self.__class__(value | other_value)
        # orphan @0x009C
    def __and__(self, other):
        # orphan @0x0016
        value = self._value_
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        elif True:
            pass
        # orphan @0x0024
        # orphan @0x0034
        # orphan @0x0036
        # orphan @0x0046
        # orphan @0x0050
        raise
        # orphan @0x0056
        # orphan @0x0058
        return self.__class__(value & other_value)
        # orphan @0x009C
    def __xor__(self, other):
        # orphan @0x0016
        value = self._value_
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        elif True:
            pass
        # orphan @0x0024
        # orphan @0x0034
        # orphan @0x0036
        # orphan @0x0046
        # orphan @0x0050
        raise
        # orphan @0x0056
        # orphan @0x0058
        return self.__class__(value ^ other_value)
        # orphan @0x009C
    def __invert__(self):
        # orphan @0x001E
        if self._get_value(self) is None:
            raise TypeError(f"'{self}' cannot be inverted")
        elif True:
            self._inverted_ = self.__class__(~self._value_)
            return self._inverted_
        # orphan @0x0028
        # orphan @0x004C
        self._inverted_ = self.__class__(self._singles_mask_ & ~self._value_)
        return self._inverted_
        # orphan @0x008A
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
    for (name, member) in enumeration.__members__.items():
        if name != member.name:
            duplicates.append((name, member.name))
        raise
        return enumeration
    if duplicates:
        alias_details = ', '.join(unique.<locals>.<listcomp>(duplicates))
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
    cls_name = self.__class__.__name__
    if self._name_ is None:
        return ('%s.%s(%r)', cls_name, self._value_)
    return '|'.join(global_flag_repr.<locals>.<listcomp>(self.name.split('|')))
    name = []
    for n in self._name_.split('|'):
        if n[0].isdigit():
            name.append(n)
            break
    return '|'.join(name)
    # orphan @0x004C
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
    if issubclass(cls, Flag):
        cls.__repr__ = global_flag_repr
        cls.__repr__ = global_enum_repr
    elif True:
        if update_str:
            cls.__str__ = global_str
            sys.modules[cls.__module__].__dict__.update(cls.__members__)
            return cls
    # orphan @0x0018
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
        # orphan @0x01AA
        # orphan @0x019A
        # orphan @0x0048
        # orphan @0x0038
        attrs = {}
        body = {}
        cls_name = cls.__name__
        if True:
            __new__ = cls.__dict__.get('__new__')
        elif True:
            new_member = __new__.__func__
        # orphan @0x023C
        # orphan @0x023E
        # orphan @0x0250
        # orphan @0x025C
        value = gnv(name, 1, len(member_names), gnv_last_values)
        # orphan @0x0274
        # orphan @0x0280
        value = (value)
        member = new_member(enum_class, **value)
        value = value[0]
        member = new_member(enum_class)
        # orphan @0x02A8
        # orphan @0x02B2
        member._value_ = value
        contained = value2member_map.get(member._value_)
        # orphan @0x02CA
        TypeError
        def <listcomp>(.0):
            for m in m._value_:
                pass
            return
        # orphan @0x02E8
        # orphan @0x03C6
        enum_class._flag_mask_ = single_bits | multi_bits
        enum_class._singles_mask_ = single_bits
        enum_class._all_bits_ = 2 ** single_bits | multi_bits.bit_length() - 1
        # orphan @0x0502
        # orphan @0x09B8
        # orphan @0x0B84
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
        # orphan @0x00D0
        low = max(values)
        high = min(values)
        missing = []
        # orphan @0x00B2
        values = set(verify.__call__.<locals>.<genexpr>(enumeration))
        # orphan @0x00A8
        # orphan @0x0084
        alias_details = ', '.join(verify.__call__.<locals>.<listcomp>(duplicates))
        raise ValueError('aliases found in %r: %s' % (enumeration, alias_details))
        # orphan @0x0080
        # orphan @0x005E
        # orphan @0x005C
        checks = self.checks
        cls_name = enumeration.__name__
        if Flag is not None:
            if issubclass(enumeration, Flag):
                enum_type = 'flag'
                if issubclass(enumeration, Enum):
                    enum_type = 'enum'
                elif name != member.name:
                    duplicates.append((name, member.name))
                elif True:
                    pass
            return enumeration
            if check is UNIQUE:
                duplicates = []
            for i in _high_bit(low):
                if 2 ** i not in values:
                    missing.append(2 ** i)
                elif True:
                    pass
                alias = 'aliases %s and %s are missing' % (', '.join(missing_names[None:-1]), missing_names[-1])
                if _is_single_bit(missing_value):
                    value = 'value 0x%x' % missing_value
                    value = 'combined values of 0x%x' % missing_value
                raise
            if True:
                for i in range(low + 1, high):
                    if i not in values:
                        missing.append(i)
        raise
        # orphan @0x0156
        raise Exception('verify: unknown type %r' % enum_type)
        # orphan @0x0164
        # orphan @0x0168
        raise ValueError('invalid %s %r: missing values %s' % (enum_type, cls_name, ', '.join(verify.__call__.<locals>.<genexpr>(missing)))[None:256])
        # orphan @0x0192
        # orphan @0x019E
        # orphan @0x01A2
        missing_names = []
        missing_value = 0
        # orphan @0x02FA
        # orphan @0x0434
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
                        continue
                        if key not in checked_keys:
                            failed.append('extra key:   %r' % (key))
                            continue
                            if not callable(checked_value):
                                if isinstance(checked_value, bltns.property):
                                    continue
                                    if key == '__doc__':
                                        pass
                                    break
                                    if checked_value != simple_value:
                                        pass
                                checked_member_keys = list(checked_member_dict.keys())
                                simple_member_dict = simple_enum[name].__dict__
                                simple_member_keys = list(simple_member_dict.keys())
                                for key in set(checked_member_keys + simple_member_keys):
                                    if key in ('__module__', '__objclass__', '_inverted_'):
                                        if key not in simple_member_keys:
                                            failed_member.append('missing key %r not in the simple enum member %r' % (key, name))
                                            if key not in checked_member_keys:
                                                pass
                                if failed_member:
                                    failed.append("""%r member mismatch:
      %s""" % (name, """
      """.join(failed_member)))
                            break
                        break
                    break
                    if checked_value != simple_value:
                        pass
                    elif True:
                        if method not in simple_keys:
                            if method not in checked_keys:
                                checked_method = getattr(checked_enum, method, None)
                                simple_method = getattr(simple_enum, method, None)
                                if hasattr(checked_method, '__func__'):
                                    checked_method = checked_method.__func__
                                    simple_method = simple_method.__func__
                                    if checked_method != simple_method:
                                        pass
                elif compressed_checked_value != compressed_simple_value:
                    pass
            break
    raise
    # orphan @0x0158
    failed.sort()
    # orphan @0x0164
    # orphan @0x0166
    failed_member = []
    # orphan @0x0174
    failed.append('missing member from simple enum: %r' % name)
    # orphan @0x018C
    # orphan @0x0278
    # orphan @0x027C
    # orphan @0x027E
    # orphan @0x028A
    # orphan @0x0310
    # orphan @0x0316
    # orphan @0x0522
    # orphan @0x063E
def _old_convert_(etype, name, module, filter, source):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    # orphan @0x001C
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
        source = module_globals
    try:
        members.sort(key=_old_convert_.<locals>.<lambda>)
    except TypeError:
        pass
    if boundary:
        return cls
    # orphan @0x00B6
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 304 instr
