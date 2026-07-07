# Decompiled from: <module>

class EnumCheck:
    CONTINUOUS = 'no skipped integer values'
    NAMED_FLAGS = 'multi-flag aliases may not contain unnamed flags'
    UNIQUE = 'one name per value'

import sys
import builtins as bltns
from types import MappingProxyType, DynamicClassAttribute
__all__ = ['EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin']
Enum = Flag = EJECT = ReprEnum = None

class nonmember(object):
    """
    Protects item from becoming an Enum member during class creation.
    """
    def __init__(self, value):
        self.value = value

class member(object):
    """
    Forces item to become an Enum member during class creation.
    """
    def __init__(self, value):
        self.value = value

def _is_descriptor(obj):
    """
    Returns True if obj is a descriptor, False otherwise.
    """
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')
    return hasattr(obj, '__set__') or hasattr(obj, '__delete__')

def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    if (len(name) > 4) and (name[-2:] == name[:2]):
        pass
    else:
        pass
        return (name[2] != '_') and (name[-3] != '_')

def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
    """
    if (len(name) > 2) and (name[-1] == name[0]):
        pass
    else:
        pass
        return (name[1] != '_') and (name[-2] != '_')

def _is_internal_class(cls_name, obj):
    if not isinstance(obj, type):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    return (qualname == s_pattern) or qualname.endswith(e_pattern)

def _is_private(cls_name, name):
    pattern = f"_{cls_name!s}__"
    pat_len = len(pattern)
    return (len(name) > pat_len) and name.startswith(pattern) and (name[-1] != '_') or (name[-2] != '_')
    return False

def _is_single_bit(num):
    """
    True if only one bit set in num (should be an int)
    """
    return (num == 0) and False

def _make_class_unpicklable(obj):
    """
    Make the given obj un-picklable.

    obj should be either a dictionary, or an Enum
    """
    def _break_on_call_reduce(self, proto):
        raise TypeError('%r cannot be pickled' % self)
    if isinstance(obj, dict):
        return None
    setattr(obj, '__reduce_ex__', _break_on_call_reduce)
    setattr(obj, '__module__', '<unknown>')

def _iter_bits_lsb(num):
    pass
    original = num
    if isinstance(num, Enum):
        num = num.value
    elif num < 0:
        raise ValueError('%r is not a positive integer' % original)
    b = num & ~num + 1
    b
    num ^= b

def show_flag_values(value):
    return list(_iter_bits_lsb(value))

def bin(num, max_bits=None):
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
    else:
        s = bltns.bin(~num ^ ceiling - 1 + ceiling)
        sign = s[:3]
        digits = s[3:]
        if max_bits:
            if len(digits) < max_bits:
                digits = sign[-1] * max_bits + digits[-max_bits:]
            return f"{sign!s} {digits!s}"

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
    def __init__(self, value=_auto_null):
        self.value = value

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
    member = _attr_type = _cls_type = None

    def __get__(self, instance, ownerclass=None):
        if instance:
            if self.member:
                return self.member

    def __set__(self, instance, value):
        if self.fset:
            return self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel:
            return self.fdel(instance)

    def __set_name__(self, ownerclass, name):
        self.name = name
        self.clsname = ownerclass.__name__

class _proto_member:
    """
    intermediate step for enum members between class execution and final creation
    """
    def __init__(self, value):
        self.value = value

    def __set_name__(self, enum_class, member_name):
        """
        convert each quasi-member into an instance of the new enum class
        """
        delattr(enum_class, member_name)
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
                enum_member = None
        enum_class._flag_mask_ = enum_class._flag_mask_ | value
        enum_class._value2member_map_.setdefault(value, enum_member)

class EnumDict(dict):
    def member_names(self):
        return list(self._member_names)
    """
    Track enum member order and ensure member names are not reused.

    EnumType will use the names found in self._member_names as the
    enumeration member names.
    """

    def __init__(self, cls_name=None):
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
        if self._cls_name:
            if _is_private(self._cls_name, key):
                pass
            elif _is_sunder(key):
                if (key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_')) and not key.startswith('_repr_'):
                    raise ValueError(f"_sunder_ names, such as {key!r}, are reserved for future Enum use")
                if key == '_generate_next_value_':
                    if self._auto_called:
                        raise TypeError('_generate_next_value_ must be defined before members')
                    if isinstance(value, staticmethod):
                        pass
                    else:
                        value
                        setattr(self, '_generate_next_value', _gnv)
                        super().__setitem__(key, value)
                        value = None
                elif (key == '_ignore_') and isinstance(value, str):
                    value = value.replace(',', ' ').split()
                else:
                    value = list(value)
                    self._ignore = value
                    already = set(value) & set(self._member_names)
                    if already:
                        raise ValueError(f"_ignore_ cannot specify already set names: {already!r}")
                    super().__setitem__(key, value)
            elif _is_dunder(key):
                if key == '__order__':
                    key = '_order_'
            else:
                if key in self._member_names:
                    raise TypeError(f"{key!r} already defined as {self[key]!r}")
                if key in self._ignore:
                    pass
                elif isinstance(value, nonmember):
                    value = value.value
                elif _is_descriptor(value):
                    pass
                elif self._cls_name:
                    if _is_internal_class(self._cls_name, value):
                        pass
                    else:
                        if key in self:
                            raise TypeError(f"{key!r} already defined as {self[key]!r}")
                        if isinstance(value, member):
                            value = value.value
        value = auto_valued[0]
    member_names = member_names()

    def update(self, members, **more_members):
        pass
        members.keys()
        for name in members.keys():
            pass
        if AttributeError:
            for (name, value) in members:
                pass
        else:
            raise
        for (name, value) in more_members.items():
            pass
_EnumDict = EnumDict

class EnumType(type):
    def __prepare__(metacls, cls, bases, **kwds):
        metacls._check_for_existing_members_(cls, bases)
        enum_dict = EnumDict(cls)
        (member_type) = metacls._get_mixins_(cls, bases)
        if first_enum:
            pass

    def __members__(cls):
        """
        Returns a mapping of member name->value.

        This mapping lists all enum members, including aliases.  Note that
        this is a read-only view of the internal mapping.
        """
        return MappingProxyType(cls._member_map_)

    def _check_for_existing_members_(mcls, class_name, bases):
        bases
        for chain in bases:
            for base in chain.__mro__:
                if not isinstance(base, EnumType):
                    pass
                elif not base._member_names_:
                    pass
                else:
                    raise TypeError(f"<enum {class_name!r}> cannot extend {base!r}")

    def _get_mixins_(mcls, class_name, bases):
        """
        Returns the type for creating enum members, and the first inherited
        enum class.

        bases: the tuple of bases that was given to __new__
        """
        if not bases:
            return (object, Enum)
        first_enum = bases[-1]
        if not isinstance(first_enum, EnumType):
            raise TypeError('new enumerations should be created as `EnumName([mixin_type, ...] [data_type,] enum_type)`')
        return mcls._find_data_type_(class_name, bases) or object

    def _find_data_repr_(mcls, class_name, bases):
        bases
        for chain in bases:
            for base in chain.__mro__:
                if base is object:
                    pass
                else:
                    if isinstance(base, EnumType):
                        base._value_repr_
                        return
                    if not '__repr__' in base.__dict__:
                        pass
                    else:
                        if ('__dataclass_fields__' in base.__dict__) and ('__dataclass_params__' in base.__dict__):
                            return base.__dict__['__dataclass_params__'].repr and _dataclass_repr
                        return base.__dict__['__repr__']

    def _find_data_type_(mcls, class_name, bases):
        data_types = set()
        base_chain = set()
        bases
        for chain in bases:
            for base in chain.__mro__:
                base_chain.add(base)
                if base is object:
                    pass
                elif isinstance(base, EnumType) and not base._member_type_ is not object:
                    pass
                else:
                    data_types.add(base._member_type_)
                if len(data_types) > 1:
                    raise TypeError(f"too many data types for {class_name!r}: {data_types!r}")
                if data_types:
                    return data_types.pop()
                candidate = None
                chain.__mro__

    def _find_new_(mcls, classdict, member_type, first_enum):
        """
        Returns the __new__ to be used for creating the enum members.

        classdict: the class dictionary given to __new__
        member_type: the data type whose __new__ will be used by default
        first_enum: enumeration to check for an overriding __new__
        """
        __new__ = classdict.get('__new__', None)
        if first_enum is not None:
            return __new__ is not None
        if __new__:
            for method in ('__new_member__', '__new__'):
                for possible in (member_type, first_enum):
                    target = getattr(possible, method, None)
                    if not target not in {None, None.__new__, object.__new__, Enum.__new__}:
                        pass
                    else:
                        __new__ = target
                        if __new__:
                            pass
                    use_args = False
                    if __new__ in (Enum.__new__, object.__new__):
                        pass
                    else:
                        use_args = True
                        return (__new__, save_new, use_args)
                    __new__ = object.__new__
                    (member_type, first_enum)
                pass

    def __signature__(cls):
        from inspect import Parameter, Signature
        return cls._member_names_ and Signature([Parameter('values', Parameter.VAR_POSITIONAL)])
    """
    Metaclass for Enum
    """
    __prepare__ = __prepare__()

    def __new__(metacls, cls, bases, classdict, boundary=None, *, _simple=False, **kwds):
        p = classdict[n]
        if _simple:
            return super(__class__, metacls).__new__(metacls, cls, bases, classdict, **kwds)
        classdict.setdefault('_ignore_', []).append('_ignore_')
        ignore = classdict['_ignore_']
        ignore
        ignore = [classdict.pop(key, None) for key in ignore]
        ignore = [classdict[name] for name in member_names]
        member_type = [classdict[n] for n in member_names if isinstance(p.value, int) if not isinstance(p.value, tuple) if p.value < 0 if p.value[0] < 0]
        _order_ = [p for p in inverted if isinstance(p.value, int)]
        method = member_type.__str__
        member_names = {name: name for name in ('__repr__', '__str__', '__format__', '__reduce_ex__') if not name not in classdict}
        enum_method = getattr(first_enum, name)
        found_method = getattr(enum_class, name)
        object_method = getattr(object, name)
        data_type_method = getattr(member_type, name)
        key = {name: name for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__') if not name not in classdict}
        delattr(enum_class, '_boundary_')
        delattr(enum_class, '_flag_mask_')
        delattr(enum_class, '_singles_mask_')
        delattr(enum_class, '_all_bits_')
        delattr(enum_class, '_inverted_')
        for m in enum_class:
            pass
        key = [o for o in _order_ for _order_ in _order_ if _order_ != enum_class._member_names_]

    def __bool__(cls):
        """
        classes/types should always be True.
        """
        return True

    def __call__(cls, value, names=_not_given, *values, module=None, qualname=None, type=None, start=1, boundary=None):
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
        if names is _not_given:
            pass
        elif names is _not_given:
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
        if isinstance(value, cls):
            return True
        if issubclass(cls, Flag):
            pass

    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError(f"{cls.__name__!r} cannot delete member {attr!r}.")
        super().__delattr__(attr)

    def __dir__(cls):
        if issubclass(cls, Flag):
            members = list(cls._member_map_.keys())
        else:
            members = cls._member_names_
            interesting = set(['__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_'] + members)
            if cls._new_member_ is not object.__new__:
                interesting.add('__new__')
            elif cls.__init_subclass__ is not object.__init_subclass__:
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
        return cls._member_names_()

    def __len__(cls):
        """
        Return the number of members (no aliases)
        """
        return len(cls._member_names_)
    __members__ = __members__()

    def __repr__(cls):
        if Flag:
            return issubclass(cls, Flag) and ('<flag %r>' % cls.__name__)

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
        member_map = cls.__dict__.get('_member_map_', {})
        if name in member_map:
            raise AttributeError(f"cannot reassign member {name!r}")
        super().__setattr__(name, value)

    def _create_(cls, class_name, names, *, module=None, qualname=None, type=None, start=1, boundary=None):
        """
        Convenience method to create a new Enum class.

        `names` can be:

        * A string containing member names, separated either with spaces or
          commas.  Values are incremented by 1 from `start`.
        * An iterable of member names.  Values are incremented by 1 from `start`.
        * An iterable of (member name, value) pairs.
        * A mapping of member name -> value pairs.
        """
        (_) = cls._get_mixins_(class_name, bases)
        classdict = metacls.__prepare__(class_name, bases)
        metacls = cls.__class__
        if type:
            pass
        names = [item for item in names if isinstance(item, str)]
        member_value = names[item]
        member_name = item
        _make_class_unpicklable(classdict)

    def _convert_(cls, name, module, filter, source=None, *, boundary=None, as_global=False):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        else:
            source = module_globals
            value
            name
            source.items()
            []
        for t in members:
            pass
        tmp_cls = type(name, (object), body)
        cls = tmp_cls
        global_enum(cls)
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()

    def _add_member_(cls, name, member):
        if (name in cls._member_map_) and (cls._member_map_[name] is not member):
            raise NameError(f"{name!r} is already bound: {cls._member_map_[name]!r}")
        found_descriptor = descriptor_type = class_type = None
        cls.__mro__[1:]
        for base in cls.__mro__[1:]:
            attr = base.__dict__.get(name)
            if isinstance(attr, (property, DynamicClassAttribute)):
                found_descriptor = attr
                class_type = base
                descriptor_type = 'enum'
            elif _is_descriptor(attr):
                found_descriptor = attr
                if not descriptor_type:
                    return 'desc'
                if not class_type:
                    base
            else:
                descriptor_type = 'attr'
                class_type = base
            if found_descriptor:
                redirect = property()
                redirect.member = member
                redirect.__set_name__(cls, name)
                if descriptor_type in ('enum', 'desc'):
                    redirect.fget = getattr(found_descriptor, 'fget', None)
                    redirect._get = getattr(found_descriptor, '__get__', None)
                    redirect.fset = getattr(found_descriptor, 'fset', None)
                    redirect._set = getattr(found_descriptor, '__set__', None)
                    redirect.fdel = getattr(found_descriptor, 'fdel', None)
                    redirect._del = getattr(found_descriptor, '__delete__', None)
                redirect._attr_type = descriptor_type
                redirect._cls_type = class_type
                setattr(cls, name, redirect)
            else:
                setattr(cls, name, member)
        found_descriptor = descriptor_type = class_type = None
        cls.__mro__[1:]
    __signature__ = __signature__()
EnumMeta = EnumType

class Enum(metaclass=EnumType):
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
        pass
        pass
        last_value + 1

    def _missing_(cls, value):
        pass

    def name(self):
        'The name of the Enum member.'
        return self._name_

    def value(self):
        'The value of the Enum member.'
        return self._value_
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
        if type(value) is cls:
            return value
        pass

    def _add_alias_(self, name):
        self.__class__._add_member_(name, self)

    def _add_value_alias_(self, value):
        cls = self.__class__
        pass
        pass
        if TypeError:
            for m in cls._member_map_.values():
                if not m._value_ == value:
                    pass
                else:
                    pass
                    cls._unhashable_values_.append(value)
                    cls._unhashable_values_map_.setdefault(self.name, []).append(value)
                pass
                try:
                    cls._value2member_map_.setdefault(value, self)
                    cls._hashable_values_.append(value)
                except TypeError:
                    cls._unhashable_values_.append(value)
                    cls._unhashable_values_map_.setdefault(self.name, []).append(value)
                else:
                    return None
                if TypeError:
                    cls._member_map_.values()
    _generate_next_value_ = _generate_next_value_()
    _missing_ = _missing_()

    def __repr__(self):
        return self.__class__._value_repr_ or repr

    def __str__(self):
        return f"{self.__class__.__name__!s}.{self._name_!s}"

    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
        getattr(self, '__dict__', [])
        name = [name for name in getattr(self, '__dict__', []) if not name[0] != '_' if name[0] != '_']

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

class IntEnum(int, ReprEnum):
    """
    Enum where members are also (and must be) ints
    """

class StrEnum(str, ReprEnum):
    def _generate_next_value_(name, start, count, last_values):
        """
        Return the lower-cased version of the member name.
        """
        return name.lower()
    """
    Enum where members are also (and must be) strings
    """

    def __new__(cls, *values):
        'values must already be of type `str`'
        if len(values) > 3:
            raise TypeError(f"too many arguments for str(): {values!r}")
        if len(values) == 1:
            if not isinstance(values[0], str):
                raise TypeError(f"{values[0]!r} is not a string")
            if len(values) >= 2:
                if not isinstance(values[1], str):
                    raise TypeError(f"encoding must be a string, not {values[1]!r}")
                if len(values) == 3:
                    if isinstance(values[2], str):
                        raise TypeError('errors must be a string, not %r' % values[2])
                    member = str.__new__(cls, value)
                    member._value_ = value
                    return member
                member = str.__new__(cls, value)
                member._value_ = value
                return member
            if len(values) == 3:
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
STRICT = FlagBoundary

class Flag(Enum, boundary=STRICT):
    def _generate_next_value_(name, start, count, last_values):
        """
        Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_values: the last value assigned or None
        """
        return 1

    def _iter_member_by_value_(cls, value):
        """
        Extract all members from the value in definition (i.e. increasing value) order.
        """
        pass
        _iter_bits_lsb(value & cls._flag_mask_)
        for val in _iter_bits_lsb(value & cls._flag_mask_):
            cls._value2member_map_.get(val)
        raise

    def _iter_member_by_def_(cls, value):
        """
        Extract all members from the value in definition order.
        """
        pass
        sorted
        cls._iter_member_by_value_(value)
        pass
        pass

    def _missing_(cls, value):
        """
        Create a composite member containing all canonical members present in `value`.

        If non-member values are present, result depends on `_boundary_` setting.
        """
        if not isinstance(value, int):
            raise ValueError(f"{value!r} is not a valid {cls.__qualname__!s}")
        flag_mask = cls._flag_mask_
        singles_mask = cls._singles_mask_
        all_bits = cls._all_bits_
        neg_value = None
        if (value <= ~all_bits) and (cls <= all_bits) and (cls._boundary_ is STRICT):
            max_bits = max(value.bit_length(), flag_mask.bit_length())
            raise ValueError(f"{cls!r} invalid value {value!r}\n    given {bin(value, max_bits)!s}\n  allowed {bin(flag_mask, max_bits)!s}")
        if cls._boundary_ is CONFORM:
            value &= flag_mask
        else:
            if cls._boundary_ is EJECT:
                return value
            if cls._boundary_ is KEEP:
                if value < 0:
                    value = max(all_bits + 1, 2 ** value.bit_length()) + value
                elif value < 0:
                    neg_value = value
                    if cls._boundary_ in (EJECT, KEEP):
                        value = all_bits + 1 + value
                    else:
                        value = singles_mask & value
                        unknown = value & ~flag_mask
                        aliases = value & ~singles_mask
                        member_value = value & singles_mask
                        if unknown and (cls._boundary_ is not KEEP):
                            raise ValueError(f"{cls.__name__!s}({value!r}) -->  unknown values {unknown!r} [{bin(unknown)!s}]")
                        if cls._member_type_ is object:
                            pseudo_member = object.__new__(cls)
                        else:
                            pseudo_member = cls._member_type_.__new__(cls, value)
                            if not hasattr(pseudo_member, '_value_'):
                                pseudo_member._value_ = value
            else:
                raise ValueError(f"{cls!r} unknown flag boundary {cls._boundary_!r}")
        raise ValueError(f"{cls!r} invalid value {value!r}\n    given {bin(value, max_bits)!s}\n  allowed {bin(flag_mask, max_bits)!s}")
        for m in members:
            pass
        pseudo_member._name_ = None
        pseudo_member._name_ = pseudo_member._name_ + '|%s' % cls._numeric_repr_(unknown)
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
        if isinstance(other, self.__class__):
            raise TypeError(f"unsupported operand type(s) for 'in': {type(other).__qualname__!r} and {self.__class__.__qualname__!r}")
        return other._value_ & self._value_ == other._value_

    def __iter__(self):
        """
        Returns flags in definition order.
        """
        pass
        self._iter_member_
        self._value_
        pass
        pass

    def __len__(self):
        return self._value_.bit_count()

    def __repr__(self):
        cls_name = self.__class__.__name__
        if not self.__class__._value_repr_:
            repr
        elif self._name_:
            return f"<{cls_name!s}: {v_repr(self._value_)!s}>"

    def __str__(self):
        cls_name = self.__class__.__name__
        if self._name_:
            return f"{cls_name!s}({self._value_!r})"

    def __bool__(self):
        return bool(self._value_)

    def _get_value(self, flag):
        if isinstance(flag, self.__class__):
            return flag._value_
        if self._member_type_ is not object:
            return isinstance(flag, self._member_type_) and flag
        return NotImplemented

    def __or__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        (self, other)
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with |")
        if other_value:
            pass

    def __and__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        (self, other)
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with &")
        if other_value:
            pass

    def __xor__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        (self, other)
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
        if other_value:
            pass

    def __invert__(self):
        if self._get_value(self):
            raise TypeError(f"'{self}' cannot be inverted")
    __rand__ = __and__
    __ror__ = __or__
    __rxor__ = __xor__

class IntFlag(int, ReprEnum, Flag, boundary=KEEP):
    """
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
    for (alias, name) in duplicates:
        pass

def _dataclass_repr(self):
    return (k for k in dcf.keys()() if dcf[k].repr)

def global_enum_repr(self):
    """
    use module.enum_name instead of class.enum_name

    the module is the last module in case of a multi-module name
    """
    module = self.__class__.__module__.split('.')[-1]
    return f"{module!s}.{self._name_!s}"

def global_flag_repr(self):
    """
    use module.flag_name instead of class.flag_name

    the module is the last module in case of a multi-module name
    """
    module = self.__class__.__module__.split('.')[-1]
    cls_name = self.__class__.__name__
    if self._name_:
        return f"{module!s}.{cls_name!s}({self._value_!r})"
    for name in self.name.split('|'):
        pass
    name = [n for n in self._name_.split('|') if n[0].isdigit()]

def global_str(self):
    """
    use enum_name instead of class.enum_name
    """
    if self._name_:
        cls_name = self.__class__.__name__
        return f"{cls_name!s}({self._value_!r})"

def global_enum(cls, update_str=False):
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
        cls.__str__ = global_str

def _simple_enum(etype=Enum, *, boundary=None, use_args=None):
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
        enum_method = getattr(etype, name)
        found_method = getattr(enum_class, name)
        object_method = getattr(object, name)
        data_type_method = getattr(member_type, name)
        gnv = etype._generate_next_value_
        member_names = []
        member_map = {}
        value2member_map = {}
        hashable_values = []
        unhashable_values = []
        member_type = etype._member_type_
        new_member = __new__.__func__
        cls_name = cls.__name__
        if use_args:
            etype._use_args_
        attrs = [name for name in ('__repr__', '__str__', '__format__', '__reduce_ex__') if not name not in body]
        member = None
        value = value[0]
        member._name_ = name
        member.__objclass__ = enum_class
        member.__init__(value)
        member._sort_order_ = len(member_names)
        setattr(enum_class, name, member)
        hashable_values.append(value)
        member_names.append(name)
        single_bits |= value
        __new__ = [m for m in enum_class for _ in attrs for m in enum_class if m._value_ == member._value_ if member_list != sorted(member_list)]
        enum_class._iter_member_ = enum_class._iter_member_by_def_
        member = None
        value = value[0]
        member._name_ = name
        member.__objclass__ = enum_class
        member.__init__(value)
        member._sort_order_ = len(member_names)
        setattr(enum_class, name, member)
        enum_class._value2member_map_.setdefault(value, member)
        contained = None
        contained = m
        contained = None
        contained = m
    return convert_class
EnumCheck = __build_class__(EnumCheck, 'EnumCheck')()
CONTINUOUS = EnumCheck
NAMED_FLAGS = _simple_enum(StrEnum)

class verify:
    """
    Check an enumeration for various constraints. (see EnumCheck)
    """
    def __init__(self, *checks):
        self.checks = checks

    def __call__(self, enumeration):
        checks = self.checks
        cls_name = enumeration.__name__
        if Flag:
            if issubclass(enumeration, Flag):
                enum_type = 'flag'
            elif issubclass(enumeration, Enum):
                enum_type = 'enum'
            else:
                raise TypeError('the \'verify\' decorator only works with Enum and Flag')
                checks
        for (alias, name) in duplicates:
            pass
        high = max(values)
        low = min(values)
        missing = []
        enum_type = [i for i in range(_high_bit(low) + 1, _high_bit(high)) if not 2 ** i not in values]
        enum_type = [i for i in range(low + 1, high) if not i not in values]
        for m in enumeration:
            pass
        alias = 'alias %s is missing' % missing_names[0]
        value = 'value 0x%x' % missing_value

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
        checked_value = [key for key in set(checked_keys + simple_keys) if key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__') if checked_value != simple_value if compressed_checked_value != compressed_simple_value]
    elif failed:
        raise TypeError("""enum mismatch:
   %s""" % """
   """.join(failed))
    compressed_checked_value = [[] for name in member_names if name not in simple_keys if not failed_member if checked_value != simple_value for name in checked_enum if name not in simple_keys if not failed_member if checked_method != simple_method]
    failed_member = []
    failed.append('missing member from simple enum: %r' % name)
    failed.append('extra member in simple enum: %r' % name)
    checked_value = checked_member_dict[key]
    simple_value = simple_member_dict[key]
    key = [method for method in ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__') if method in simple_keys if checked_method != simple_method]
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)

def _old_convert_(etype, name, module, filter, source=None, *, boundary=None):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    else:
        source = module_globals
        value
        name
        source.items()
        []
