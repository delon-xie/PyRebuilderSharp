# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType, DynamicClassAttribute
__all__ = ('EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin')
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
    # orphan @0x0038
    name[-2] != '_'
    # orphan @0x0042
    return
def _is_internal_class(cls_name, obj):
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
    original = num
    if isinstance(num, Enum):
        num = num.value
    # orphan @0x001C
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
        # orphan @0x0048
        return getattr(self._cls_type, self.name)
        # orphan @0x0060
        return getattr(instance._value_, self.name)
        # orphan @0x006E
        return
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
        # orphan @0x00B4
        exc = None
        # orphan @0x0048
        enum_member = enum_class._new_member_(enum_class, **args)
        # orphan @0x0030
        args = (args)
        # orphan @0x0022
        args = value
        delattr(enum_class, member_name)
        value = self.value
        if not isinstance(value, tuple):
            args = (value)
        enum_member = enum_class._new_member_(enum_class)
        if hasattr(enum_member, '_value_'):
            if enum_class._member_type_ is object:
                enum_member._value_ = value
        # orphan @0x012E
        enum_class._all_bits_ = 2 ** enum_class._flag_mask_.bit_length() - 1
        # orphan @0x0142
        enum_class._value2member_map_
        # orphan @0x018E
        # orphan @0x01FA
        enum_class._member_names_.append(member_name)
        # orphan @0x0234
        enum_class._hashable_values_.append(value)
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
        # orphan @0x00C2
        # orphan @0x009E
        value = list(value)
        # orphan @0x0068
        value
        # orphan @0x0050
        # orphan @0x0034
        if (self._cls_name is not None) and _is_private(self._cls_name, key):
            pass
        # orphan @0x00F8
        # orphan @0x016C
        # orphan @0x018E
        value = value.value
        # orphan @0x01A8
        single = True
        value = (value)
        # orphan @0x0202
        v.value = self._generate_next_value(key, 1, len(self._member_names), self._last_values[None:])
        self._auto_called = True
        # orphan @0x022A
        v = v.value
        self._last_values.append(v)
        # orphan @0x0294
        self._last_values.append(value)
        # orphan @0x02A0
        super().__setitem__(key, value)
    @property
    def member_names(self):
        return list(self._member_names)
    def update(self, members):
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
        # orphan @0x0174
        getattr(first_enum, '_boundary_', None)
        # orphan @0x00CA
        '_generate_next_value_'
        classdict
        _gnv
        # orphan @0x00AE
        _gnv = staticmethod(_gnv)
        # orphan @0x0068
        if _simple:
            return super().__new__(metacls, cls, bases, classdict, **kwds)
        # orphan @0x0202
        bits |= p.value
        # orphan @0x0260
        bits |= p.value[0]
        # orphan @0x0296
        p.value = (bits & p.value[0]) + p.value[1:]
        # orphan @0x031C
        e
        # orphan @0x0320
        # orphan @0x032E
        def <genexpr>(.0):
            .0
            for n in .0:
                yield repr(n)
                break
        # orphan @0x0362
        # orphan @0x0374
        '__format__'
        classdict
        # orphan @0x03A2
        method = member_type.__repr__
        # orphan @0x03A8
        '__str__'
        classdict
        # orphan @0x046A
        # orphan @0x0470
        # orphan @0x048E
        _order_ = _order_.replace(',', ' ').split()
        # orphan @0x052E
        # orphan @0x053C
        _order_ = EnumType.__new__.<locals>.<listcomp>(_order_)
        ()
        # orphan @0x0572
        # orphan @0x0584
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
        # orphan @0x0036
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
        if isinstance(value, cls):
            return True
        try:
            result = cls._missing_(value)
        except ValueError:
            pass
        return
        return
        value in cls._hashable_values_
        return
    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError('%r cannot delete member %r.' % (cls.__name__, attr))
        # orphan @0x001C
        super().__delattr__(attr)
    def __dir__(cls):
        # orphan @0x001A
        members = cls._member_names_
        if issubclass(cls, Flag):
            members = list(cls._member_map_.keys())
        # orphan @0x003C
        interesting.add('__new__')
        # orphan @0x0052
        interesting.add('__init_subclass__')
        # orphan @0x0066
        return sorted(interesting)
        # orphan @0x006E
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
        # orphan @0x0042
        names = names.replace(',', ' ').split()
        # orphan @0x0014
        (type, cls)
        metacls = cls.__class__
        if type is None:
            pass
        # orphan @0x00CA
        names = []
        # orphan @0x00F0
        (member_name, member_value) = item
        # orphan @0x0174
        '__module__'
        classdict
        module
        # orphan @0x0186
        '__qualname__'
        classdict
        qualname
        # orphan @0x018E
        return metacls.__new__(metacls, class_name, bases, classdict, boundary=boundary)
    def _convert_(cls, name, module, filter, source):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        # orphan @0x0018
        source = module_globals
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        # orphan @0x0096
        KEEP
        # orphan @0x00B0
        cls
        sys.modules
        # orphan @0x00B6
        # orphan @0x00C6
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
        if not bases:
            return (object, Enum)
        # orphan @0x001E
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
        __new__ = classdict.get('__new__', None)
        if not first_enum is not None:
            __new__ is not None
        # orphan @0x0072
        __new__ = object.__new__
        # orphan @0x0096
        use_args = True
        # orphan @0x009A
        return (__new__, save_new, use_args)
    def _add_member_(cls, name, member):
        if (name in cls._member_map_) and (cls._member_map_[name] is not member):
            raise NameError('%r is already bound: %r' % (name, cls._member_map_[name]))
        # orphan @0x0094
        'desc'
        # orphan @0x009C
        base
        # orphan @0x00D6
        redirect.fget = getattr(found_descriptor, 'fget', None)
        redirect._get = getattr(found_descriptor, '__get__', None)
        redirect.fset = getattr(found_descriptor, 'fset', None)
        redirect._set = getattr(found_descriptor, '__set__', None)
        redirect.fdel = getattr(found_descriptor, 'fdel', None)
        redirect._del = getattr(found_descriptor, '__delete__', None)
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
        # orphan @0x0046
        value in unhashable_values
        # orphan @0x0010
        return
        if type(value) is cls:
            return value
        # orphan @0x00B2
        # orphan @0x00BC
        # orphan @0x00C8
        None
        # orphan @0x0100
        e = None
        # orphan @0x0118
        exc = None
        ve_exc = None
        return
        # orphan @0x0154
        exc = None
        ve_exc = None
        return
        # orphan @0x0188
        # orphan @0x0198
        exc = TypeError('error in %s._missing_: returned %r instead of None or a valid member' % (cls.__name__, result))
        # orphan @0x01B6
        exc.__context__ = ve_exc
        # orphan @0x01BC
        # orphan @0x01CC
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
                for m in cls._member_map_.values():
                    if (m._value_ == value) and (m is not self):
                        raise ValueError('%r is already bound: %r' % (value, cls._value2member_map_[value]))
                    break
                continue
                try:
                    cls._value2member_map_.setdefault(value, self)
                    cls._hashable_values_.append(value)
                except TypeError:
                    cls._unhashable_values_map_.setdefault(self.name, []).append(value)
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
        if not last_values:
            return start
        # orphan @0x0036
        return
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
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
        # orphan @0x00C2
        interesting.add(name)
        # orphan @0x00D0
        names = set([](('__class__', '__doc__', '__eq__', '__hash__', '__module__')) | interesting)
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
        if len(values) > 3:
            raise TypeError('too many arguments for str(): %r' % (values))
        elif not isinstance(values[0], str):
            raise TypeError('%r is not a string' % (values[0]))
        # orphan @0x0060
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
        # orphan @0x0010
        return 1
        if count:
            if start is not None:
                return start
        # orphan @0x004A
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
        # orphan @0x00B4
        return value
        # orphan @0x0062
        max_bits = max(value.bit_length(), flag_mask.bit_length())
        if not isinstance(value, int):
            raise ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        # orphan @0x0124
        value = singles_mask & value
        # orphan @0x015A
        # orphan @0x018C
        pseudo_member = cls._member_type_.__new__(cls, value)
        # orphan @0x01A6
        pseudo_member._value_ = value
        # orphan @0x0280
        # orphan @0x02B2
        pseudo_member._name_ = None
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
        # orphan @0x0028
        return flag
        # orphan @0x002C
        return NotImplemented
    def __or__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        # orphan @0x0046
        # orphan @0x0058
        return self.__class__(value | other_value)
    def __and__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        # orphan @0x0046
        # orphan @0x0058
        return self.__class__(value & other_value)
    def __xor__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        # orphan @0x0046
        # orphan @0x0058
        return self.__class__(value ^ other_value)
    def __invert__(self):
        if self._get_value(self) is None:
            raise TypeError(f"'{self}' cannot be inverted")
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
    cls_name = self.__class__.__name__
    if self._name_ is None:
        return ('%s.%s(%r)', cls_name, self._value_)
    return '|'.join(global_flag_repr.<locals>.<listcomp>(self.name.split('|')))
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
        # orphan @0x01BC
        '__doc__'
        body
        'An enumeration.'
        # orphan @0x019E
        name
        attrs
        obj
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
        # orphan @0x0048
        '__new_member__'
        body
        new_member
        # orphan @0x0030
        cls_name = cls.__name__
        use_args
        # orphan @0x0272
        value = gnv(name, 1, len(member_names), gnv_last_values)
        # orphan @0x0296
        value = (value)
        # orphan @0x02B6
        member = new_member(enum_class)
        # orphan @0x02C8
        member._value_ = value
        # orphan @0x038A
        enum_class._add_member_(name, member)
        # orphan @0x03C6
        multi_bits |= value
        # orphan @0x03CE
        gnv_last_values.append(value)
        # orphan @0x0454
        value.value = gnv(name, 1, len(member_names), gnv_last_values)
        # orphan @0x0468
        value = value.value
        # orphan @0x0480
        value = (value)
        # orphan @0x04A0
        member = new_member(enum_class)
        # orphan @0x04B2
        member._value_ = value
        # orphan @0x0574
        enum_class._add_member_(name, member)
        # orphan @0x05AE
        hashable_values.append(value)
        # orphan @0x05FE
        enum_class.__new_member__ = enum_class.__new__
        # orphan @0x0606
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
        # orphan @0x0084
        alias_details = ', '.join(verify.__call__.<locals>.<listcomp>(duplicates))
        # orphan @0x0034
        checks = self.checks
        cls_name = enumeration.__name__
        if (Flag is not None) and issubclass(enumeration, Flag):
            enum_type = 'flag'
        # orphan @0x0166
        # orphan @0x0178
        # orphan @0x0260
        alias = 'aliases %s and %s are missing' % (', '.join(missing_names[None:-1]), missing_names[-1])
        # orphan @0x0292
        value = 'combined values of 0x%x' % missing_value
        # orphan @0x029A
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
    # orphan @0x024C
    failed_member.append("""%r:
         %s
         %s""" % (key, 'checked member -> %r' % (checked_value), 'simple member  -> %r' % (simple_value)))
    # orphan @0x02EC
    checked_method = checked_method.__func__
    simple_method = simple_method.__func__
    # orphan @0x032E
def _old_convert_(etype, name, module, filter, source):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    # orphan @0x0018
    source = module_globals
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    # orphan @0x0076
    KEEP
    # orphan @0x0078
    return cls
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 304 instr
