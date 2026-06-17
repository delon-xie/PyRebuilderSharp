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
    if hasattr(obj, '__get__'):
        return
    elif hasattr(obj, '__set__'):
        pass
def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    if (len(name) > 4) or not name[-2:] == name[-2:]:
        return
def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
    """
    if (len(name) > 2) or not name[-1] == name[-1]:
        return
def _is_internal_class(cls_name, obj):
    if not isinstance(obj, type):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if qualname == s_pattern:
        return
def _is_private(cls_name, name):
    pattern = '_%s__' % (cls_name)
    pat_len = len(pattern)
    if (len(name) > pat_len) and name.startswith(pattern) and (name[-1] != '_') or (name[-2] != '_'):
        return True
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
        raise TypeError('%r cannot be pickled' % self)
    if isinstance(obj, dict):
        return None
    setattr(obj, '__reduce_ex__', _break_on_call_reduce)
    setattr(obj, '__module__', '<unknown>')
def _iter_bits_lsb(num):
    original = num
    if isinstance(num, Enum):
        num = num.value
    elif num < 0:
        raise ValueError('%r is not a positive integer' % original)
    # orphan @0x002E
    b = num & ~num + 1
    yield b
    num ^= b
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
    else:
        s = bltns.bin(~num ^ ceiling - 1 + ceiling)
    sign = s[None:3]
    digits = s[3:]
    if (max_bits is not None) and (len(digits) < max_bits):
        digits = sign[-1] * max_bits + digits[-max_bits:]
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
        if (instance is None) and (self.member is not None):
            return self.member
        raise AttributeError('%r has no attribute %r' % (ownerclass, self.name))
        if self.fget is not None:
            return self.fget(instance)
        elif self._attr_type == 'attr':
            return getattr(self._cls_type, self.name)
        elif self._attr_type == 'desc':
            return getattr(instance._value_, self.name)
    def __set__(self, instance, value):
        if self.fset is not None:
            return self.fset(instance, value)
        raise AttributeError('<enum %r> cannot set attribute %r' % (self.clsname, self.name))
    def __delete__(self, instance):
        if self.fdel is not None:
            return self.fdel(instance)
        raise AttributeError('<enum %r> cannot delete attribute %r' % (self.clsname, self.name))
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
        delattr(enum_class, member_name)
        value = self.value
        if not isinstance(value, tuple):
            args = (value)
        else:
            args = value
        if enum_class._member_type_ is tuple:
            args = (args)
        else:
            if not enum_class._use_args_:
                enum_member = enum_class._new_member_(enum_class)
            else:
                enum_member = enum_class._new_member_(enum_class, **args)
            if hasattr(enum_member, '_value_'):
                value = enum_member._value_
                enum_member._name_ = member_name
                enum_member.__objclass__ = enum_class
                enum_member._sort_order_ = len(enum_class._member_names_)
                if (Flag is not None) and issubclass(enum_class, Flag) and isinstance(value, int):
                    enum_class._flag_mask_ | value._flag_mask_ = enum_class
                    if _is_single_bit(value):
                        enum_class._singles_mask_ | value._singles_mask_ = enum_class
                    enum_class._all_bits_ = 2 ** enum_class._flag_mask_.bit_length() - 1
                    try:
                        try:
                            enum_member = enum_class._value2member_map_[value]
                        except:
                            pass
                    except KeyError:
                        enum_class._member_names_.append(member_name)
                    enum_class._add_member_(member_name, enum_member)
                    try:
                        enum_class._value2member_map_.setdefault(value, enum_member)
                        if value not in enum_class._hashable_values_:
                            enum_class._hashable_values_.append(value)
                            return None
                        else:
                            return None
                    finally:
                        pass
        # orphan @0x0140
        TypeError
        # orphan @0x0156
        # orphan @0x0158
        # orphan @0x0168
        enum_member = canonical_member
        # orphan @0x0170
        # orphan @0x0172
        raise KeyError
        # orphan @0x0176
        raise
        # orphan @0x017C
        # orphan @0x0256
        raise
        # orphan @0x02C0
        TypeError
        enum_class._unhashable_values_.append(value)
        enum_class._unhashable_values_map_.setdefault(member_name, []).append(value)
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
        if (self._cls_name is not None) and _is_private(self._cls_name, key):
            pass
        else:
            if _is_sunder(key) and (key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_')) and not key.startswith('_repr_'):
                raise ValueError('_sunder_ names, such as %r, are reserved for future Enum use' % (key))
            else:
                if (key == '_generate_next_value_') and self._auto_called:
                    raise TypeError('_generate_next_value_ must be defined before members')
                elif isinstance(value, staticmethod):
                    pass
                if isinstance(value, str):
                    value = value.replace(',', ' ').split()
                else:
                    value = list(value)
            if key in self._member_names:
                raise TypeError('%r already defined as %r' % (key, self[key]))
            else:
                if key in self._ignore:
                    pass
                if _is_descriptor(value):
                    pass
                if key in self:
                    raise TypeError('%r already defined as %r' % (key, self[key]))
                elif isinstance(value, member):
                    value = value.value
                if _is_internal_class(self._cls_name, value):
                    pass
            if key == '__order__':
                key = '_order_'
        # orphan @0x0226
        # orphan @0x022C
        value = auto_valued[0]
        # orphan @0x0236
        value = t(auto_valued)
        # orphan @0x0244
        TypeError
        raise
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
            pass
        return enum_dict
    def __new__(metacls, cls, bases, classdict):
        if _simple:
            return super().__new__(metacls, cls, bases, classdict, **kwds)
        classdict.setdefault('_ignore_', []).append('_ignore_')
        ignore = classdict['_ignore_']
        for key in ignore:
            classdict.pop(key, None)
        member_names = classdict._member_names
        invalid_names = set(member_names) & # Unknown node: SetLiteral
        if invalid_names:
            raise ValueError('invalid enum member name(s) %s' % ','.join(EnumType.__new__.<locals>.<genexpr>(invalid_names)))
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        if (_gnv is not None) and (type(_gnv) is not staticmethod):
            _gnv = staticmethod(_gnv)
        classdict = dict(classdict.items())
        if _gnv is not None:
            pass
        (member_type, first_enum) = metacls._get_mixins_(cls, bases)
        (__new__, save_new, use_args) = metacls._find_new_(classdict, member_type, first_enum)
        for name in name:
            value = classdict[name]
        if boundary and (Flag is not None) and bases and issubclass(bases[-1], Flag):
            for n in member_names:
                p = classdict[n]
                if isinstance(p.value, int) and (p.value < 0):
                    inverted.append(p)
                else:
                    bits |= p.value
                if isinstance(p.value, tuple) and p.value and isinstance(p.value[0], int) and (p.value[0] < 0):
                    inverted.append(p)
                else:
                    bits |= p.value[0]
        try:
            '_%s__in_progress' % cls(delattr, '_%s__in_progress' % cls)
        except Exception:
            raise
            e = None
            raise
            raise
            e(classdict.__dict__)
            raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
            member_type.__format__.__format__ = '__str__' not in classdict
            method = member_type.__str__
            method.__str__ = method is object.__str__
            method = member_type.__repr__
        break
        if (ReprEnum is not None) and (ReprEnum in bases) and (member_type is object):
            raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
        elif '__format__' not in classdict:
            pass
        elif '__str__' not in classdict:
            method = member_type.__str__
            if method is object.__str__:
                method = member_type.__repr__
            for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
                if name not in classdict:
                    enum_method = getattr(first_enum, name)
                    object_method = getattr(object, name)
                    data_type_method = getattr(member_type, name)
                    if found_method in (data_type_method, object_method):
                        break
            if Flag is not None:
                for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__'):
                    if name not in classdict:
                        enum_method = getattr(Flag, name)
                        break
        def <genexpr>(.0):
            for n in .0:
                yield repr(n)
                break
        raise
        # orphan @0x026A
        # orphan @0x026E
        # orphan @0x0270
        # orphan @0x0280
        p.value = bits & p.value
        # orphan @0x0290
        p.value = (bits & p.value[0]) + p.value[1:]
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
        elif (names is _not_given) and (type is None):
            raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
        elif names is _not_given:
            pass
    def __contains__(cls, value):
        """Return True if `value` is in `cls`.

        `value` is in `cls` if:
        1) `value` is a member of `cls`, or
        2) `value` is the value of one of the `cls`'s members.
        3) `value` is a pseudo-member (flags)
        """
        if isinstance(value, cls):
            return True
        elif issubclass(cls, Flag):
            try:
                result = cls._missing_(value)
            except ValueError:
                pass
            return
        # orphan @0x004C
        # orphan @0x0054
        return
    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError('%r cannot delete member %r.' % (cls.__name__, attr))
        super().__delattr__(attr)
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
        metacls = cls.__class__
        if type is None:
            pass
        (_, first_enum) = cls._get_mixins_(class_name, bases)
        classdict = metacls.__prepare__(class_name, bases)
        if isinstance(names, str):
            names = names.replace(',', ' ').split()
        elif isinstance(names, (tuple, list)) and names and isinstance(names[0], str):
            for (count, name) in enumerate(original_names):
                value = first_enum._generate_next_value_(name, start, count, last_values[None:])
                last_values.append(value)
                names.append((name, value))
        elif names is None:
            names = []
        # orphan @0x013C
        (AttributeError, ValueError, KeyError)
        raise
        # orphan @0x015A
        # orphan @0x0162
        _make_class_unpicklable(classdict)
        # orphan @0x016C
        # orphan @0x0174
        # orphan @0x017C
        # orphan @0x0184
        return metacls.__new__(metacls, class_name, bases, classdict, boundary=boundary)
    def _convert_(cls, name, module, filter, source):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        else:
            source = module_globals
        members = EnumType._convert_.<locals>.<listcomp>(source.items())
        try:
            members.sort(key=EnumType._convert_.<locals>.<lambda>)
        except TypeError:
            pass
        body = EnumType._convert_.<locals>.<dictcomp>(members)
        tmp_cls = type(name, (object), body)
        if boundary and as_global:
            global_enum(cls)
        return cls
    @classmethod
    def _check_for_existing_members_(mcls, class_name, bases):
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
        first_enum = bases[-1]
        if not isinstance(first_enum, EnumType):
            raise TypeError('new enumerations should be created as `EnumName([mixin_type, ...] [data_type,] enum_type)`')
        elif mcls._find_data_type_(class_name, bases):
            return (member_type, first_enum)
    @classmethod
    def _find_data_repr_(mcls, class_name, bases):
        for chain in bases:
            for base in chain.__mro__:
                if base is object:
                    pass
                if ('__repr__' in base.__dict__) and ('__dataclass_fields__' in base.__dict__) and ('__dataclass_params__' in base.__dict__) and base.__dict__['__dataclass_params__'].repr:
                    _dataclass_repr
                    break
                base.__dict__['__repr__']
                break
                base._value_repr_
                break
    @classmethod
    def _find_data_type_(mcls, class_name, bases):
        data_types = set()
        base_chain = set()
        for chain in bases:
            for base in chain.__mro__:
                base_chain.add(base)
                if base is object:
                    pass
                if '__new__' in base.__dict__:
                    if candidate:
                        break
                if candidate:
                    pass
                if base._member_type_ is not object:
                    data_types.add(base._member_type_)
                    break
        if len(data_types) > 1:
            raise TypeError('too many data types for %r: %r' % (class_name, data_types))
        elif data_types:
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
            pass
        elif __new__ is None:
            for method in ('__new_member__', '__new__'):
                for possible in (member_type, first_enum):
                    target = getattr(possible, method, None)
                    if target not in # Unknown node: SetLiteral:
                        __new__ = target
                        break
                if __new__ is not None:
                    break
                if first_enum is None:
                    use_args = False
                use_args = True
                return (__new__, save_new, use_args)
        # orphan @0x0072
        __new__ = object.__new__
    def _add_member_(cls, name, member):
        if name in cls._member_map_:
            if cls._member_map_[name] is not member:
                raise NameError('%r is already bound: %r' % (name, cls._member_map_[name]))
        else:
            found_descriptor = None
            descriptor_type = None
            class_type = None
        for base in cls.__mro__[1:]:
            attr = base.__dict__.get(name)
            if (attr is not None) and isinstance(attr, (property, DynamicClassAttribute)):
                found_descriptor = attr
                class_type = base
                descriptor_type = 'enum'
                break
            elif _is_descriptor(attr):
                found_descriptor = attr
                if descriptor_type and class_type:
                    pass
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
    @property
    def __signature__(cls):
        from inspect import Parameter, Signature
        if cls._member_names_:
            return Signature([Parameter('values', Parameter.VAR_POSITIONAL)])
        return Signature([Parameter('new_class_name', Parameter.POSITIONAL_ONLY), Parameter('names', Parameter.POSITIONAL_OR_KEYWORD), Parameter('module', Parameter.KEYWORD_ONLY, default=None), Parameter('qualname', Parameter.KEYWORD_ONLY, default=None), Parameter('type', Parameter.KEYWORD_ONLY, default=None), Parameter('start', Parameter.KEYWORD_ONLY, default=1), Parameter('boundary', Parameter.KEYWORD_ONLY, default=None)])
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
        if type(value) is cls:
            return value
        try:
            pass
        finally:
            pass
        return
        for (name, member) in cls._member_map_.items():
            if value == member._value_:
                cls[name]
                return
        raise
        if cls._member_map_:
            try:
                pass
            except Exception:
                exc = e
                result = None
        raise TypeError('%r has no members defined' % cls)
        raise TypeError('do not use `super().__new__; call the appropriate __new__ directly') from None
        cls[name]
        return
        # orphan @0x00CC
        result = cls._missing_(value)
        # orphan @0x00FE
        e = None
        raise
        # orphan @0x0108
        # orphan @0x0114
        exc = None
        ve_exc = None
        return
        # orphan @0x0122
        # orphan @0x012A
        # orphan @0x0134
        # orphan @0x013E
        # orphan @0x0148
        exc = None
        ve_exc = None
        return
        # orphan @0x0156
        ve_exc = ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        # orphan @0x0170
        # orphan @0x0178
        raise ve_exc
        # orphan @0x017C
        # orphan @0x0184
        exc = TypeError('error in %s._missing_: returned %r instead of None or a valid member' % (cls.__name__, result))
        # orphan @0x0196
        # orphan @0x01A0
        exc.__context__ = ve_exc
        # orphan @0x01A6
        raise exc
        # orphan @0x01AA
        exc = None
        ve_exc = None
        raise
    def _add_alias_(self, name):
        self.__class__._add_member_(name, self)
    def _add_value_alias_(self, value):
        cls = self.__class__
        try:
            if value in cls._value2member_map_:
                if cls._value2member_map_[value] is not self:
                    raise ValueError('%r is already bound: %r' % (value, cls._value2member_map_[value]))
        except TypeError:
            pass
        try:
            cls._value2member_map_.setdefault(value, self)
            cls._hashable_values_.append(value)
        except TypeError:
            cls._unhashable_values_map_.setdefault(self.name, []).append(value)
        return None
        return None
        # orphan @0x01A2
        raise
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
        try:
            last_value = sorted(last_values).pop()
        except TypeError:
            raise
            raise
            return
        try:
            pass
        except TypeError:
            raise
            raise
        return
        return
        raise
        raise
    @classmethod
    def _missing_(cls, value):
        pass
    def __repr__(self):
        if self.__class__._value_repr_:
            return '<%s.%s: %s>' % (self.__class__.__name__, self._name_, v_repr(self._value_))
    def __str__(self):
        return '%s.%s' % (self.__class__.__name__, self._name_)
    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
        for name in getattr(self, '__dict__', []):
            if (name[0] != '_') and (name not in self._member_map_):
                interesting.add(name)
        for cls in self.__class__.mro():
            for (name, obj) in cls.__dict__.items():
                if name[0] == '_':
                    pass
                if name not in self._member_map_:
                    interesting.add(name)
                if obj.fget is not None:
                    interesting.add(name)
                interesting.discard(name)
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
        if len(values) > 3:
            raise TypeError('too many arguments for str(): %r' % (values))
        elif (len(values) == 1) and not isinstance(values[0], str):
            raise TypeError('%r is not a string' % (values[0]))
        elif (len(values) >= 2) and not isinstance(values[1], str):
            raise TypeError('encoding must be a string, not %r' % (values[1]))
        elif (len(values) == 3) and not isinstance(values[2], str):
            raise TypeError('errors must be a string, not %r' % values[2])
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
        if count:
            last_value = max(last_values)
            try:
                high_bit = _high_bit(last_value)
            except Exception:
                raise
                raise
                return 2 ** (high_bit + 1)
        return 1
        return start
        # orphan @0x0044
        raise
        # orphan @0x0046
        return 2 ** (high_bit + 1)
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
        # orphan @0x004C
        if not isinstance(value, int):
            raise ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        flag_mask = cls._flag_mask_
        singles_mask = cls._singles_mask_
        all_bits = cls._all_bits_
        def <listcomp>(.0):
            for m in m._name_:
                pass
            return
        if value <= value:
            pass
        # orphan @0x01D4
        # orphan @0x01DA
        value = member_value | aliases
        # orphan @0x01EC
        # orphan @0x01EE
        # orphan @0x01FE
        # orphan @0x0206
        # orphan @0x0218
        members.append(pm)
        combined_value |= pm._value_
        # orphan @0x022C
        # orphan @0x022E
        unknown = value ^ combined_value
        pseudo_member._name_ = '|'.join(Flag._missing_.<locals>.<listcomp>(members))
        # orphan @0x0252
        pseudo_member._name_ = None
        # orphan @0x025A
        # orphan @0x0260
        # orphan @0x026C
        raise ValueError('%r: no members with value %r' % (cls, unknown))
        # orphan @0x027C
        # orphan @0x0282
        pseudo_member._name_ + '|%s' % cls._numeric_repr_(unknown)._name_ = pseudo_member
        # orphan @0x029A
    def __contains__(self, other):
        """
        Returns True if self has at least the same flags set as other.
        """
        if not isinstance(other, self.__class__):
            raise TypeError('unsupported operand type(s) for \'in\': %r and %r' % (type(other).__qualname__, self.__class__.__qualname__))
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
        if self.__class__._value_repr_ and (self._name_ is None):
            return '<%s: %s>' % (cls_name, v_repr(self._value_))
        return '<%s.%s: %s>' % (cls_name, self._name_, v_repr(self._value_))
    def __str__(self):
        cls_name = self.__class__.__name__
        if self._name_ is None:
            return '%s(%r)' % (cls_name, self._value_)
        return '%s.%s' % (cls_name, self._name_)
    def __bool__(self):
        return bool(self._value_)
    def _get_value(self, flag):
        if isinstance(flag, self.__class__):
            return flag._value_
        elif (self._member_type_ is not object) and isinstance(flag, self._member_type_):
            return flag
    def __or__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        if value is None:
            for flag in (self, other):
                if self._get_value(flag) is None:
                    raise TypeError(f"'{flag}' cannot be combined with other flags with |")
        return self.__class__(value | other_value)
    def __and__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        if value is None:
            for flag in (self, other):
                if self._get_value(flag) is None:
                    raise TypeError(f"'{flag}' cannot be combined with other flags with &")
        return self.__class__(value & other_value)
    def __xor__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        if value is None:
            for flag in (self, other):
                if self._get_value(flag) is None:
                    raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
        return self.__class__(value ^ other_value)
    def __invert__(self):
        if self._get_value(self) is None:
            raise TypeError(f"'{self}' cannot be inverted")
        elif (self._inverted_ is None) and (self._boundary_ in (EJECT, KEEP)):
            self._inverted_ = self.__class__(~self._value_)
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
    for (name, member) in enumeration.__members__.items():
        if name != member.name:
            duplicates.append((name, member.name))
    if duplicates:
        alias_details = ', '.join(unique.<locals>.<listcomp>(duplicates))
        raise ValueError('duplicate values found in %r: %s' % (enumeration, alias_details))
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
    cls_name = self.__class__.__name__
    if self._name_ is None:
        return ('%s.%s(%r)', cls_name, self._value_)
    elif _is_single_bit(self._value_):
        return ('%s.%s', self._name_)
    elif self._boundary_ is not FlagBoundary.KEEP:
        return '|'.join(global_flag_repr.<locals>.<listcomp>(self.name.split('|')))
def global_str(self):
    """
    use enum_name instead of class.enum_name
    """
    if self._name_ is None:
        cls_name = self.__class__.__name__
        return '%s(%r)' % (cls_name, self._value_)
    return self._name_
def global_enum(cls, update_str):
    """
    decorator that makes the repr() of an enum member reference its module
    instead of its class; also exports all members to the enum's module's
    global namespace
    """
    if issubclass(cls, Flag):
        cls.__repr__ = global_flag_repr
    else:
        cls.__repr__ = global_enum_repr
    if issubclass(cls, ReprEnum) and update_str:
        cls.__str__ = global_str
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
        cls_name = cls.__name__
        __new__ = cls.__dict__.get('__new__')
        if __new__ is not None:
            new_member = __new__.__func__
        attrs = {}
        body = {}
        if __new__ is not None:
            pass
        gnv = '_generate_next_value_'
        member_names = '_member_names_'
        member_map = '_member_map_'
        value2member_map = '_value2member_map_'
        hashable_values = '_hashable_values_'
        unhashable_values = '_unhashable_values_'
        member_type = '_member_type_'
        if '_value_repr_'(issubclass, Flag):
            pass
        for (name, obj) in name:
            if name in ('__dict__', '__weakref__'):
                pass
            if _is_private(cls_name, name):
                pass
            if _is_descriptor(obj):
                pass
        if cls.__dict__.get('__doc__') is None:
            pass
        for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
            if name not in body:
                found_method = getattr(enum_class, name)
                object_method = getattr(object, name)
                data_type_method = getattr(member_type, name)
                if found_method in (data_type_method, object_method):
                    setattr(enum_class, name, enum_method)
        gnv_last_values = []
        if issubclass(enum_class, Flag):
            for (name, value) in attrs.items():
                if isinstance(value, auto) and (auto.value is _auto_null):
                    value = gnv(name, 1, len(member_names), gnv_last_values)
                elif not isinstance(value, tuple):
                    value = (value)
        for (name, value) in attrs.items():
            if isinstance(value, auto) and (value.value is _auto_null):
                value.value = gnv(name, 1, len(member_names), gnv_last_values)
            value = value.value
            if not isinstance(value, tuple):
                value = (value)
            member = new_member(enum_class, **value)
            value = value[0]
            if __new__ is None:
                member._value_ = value
            try:
                contained = value2member_map.get(member._value_)
            except TypeError:
                contained = None
            if contained is not None:
                contained._add_alias_(name)
            else:
                member._name_ = name
                member.__objclass__ = enum_class
                member.__init__(value)
                member._sort_order_ = len(member_names)
            enum_class._add_member_(name, member)
            member_names.append(name)
            gnv_last_values.append(value)
            try:
                enum_class._value2member_map_.setdefault(value, member)
                if value not in hashable_values:
                    hashable_values.append(value)
                else:
                    for (name, value) in attrs.items():
                        if isinstance(value, auto) and (value.value is _auto_null):
                            value.value = gnv(name, 1, len(member_names), gnv_last_values)
                        value = value.value
                        if not isinstance(value, tuple):
                            value = (value)
                        member = new_member(enum_class, **value)
                        value = value[0]
                        if __new__ is None:
                            member._value_ = value
                        try:
                            contained = value2member_map.get(member._value_)
                        except TypeError:
                            contained = None
                        if contained is not None:
                            contained._add_alias_(name)
                        else:
                            member._name_ = name
                            member.__objclass__ = enum_class
                            member.__init__(value)
                            member._sort_order_ = len(member_names)
                        enum_class._add_member_(name, member)
                        setattr(enum_class, name, member)
            except TypeError:
                enum_class._unhashable_values_map_.setdefault(name, []).append(value)
            if '__new__' in body:
                enum_class.__new_member__ = enum_class.__new__
            enum_class.__new__ = Enum.__new__
            return enum_class
            setattr(enum_class, name, member)
        # orphan @0x03C6
        enum_class._flag_mask_ = single_bits | multi_bits
        enum_class._singles_mask_ = single_bits
        enum_class._all_bits_ = 2 ** single_bits | multi_bits.bit_length() - 1
        member_list = _simple_enum.<locals>.convert_class.<locals>.<listcomp>(enum_class)
        # orphan @0x0408
        enum_class._iter_member_ = enum_class._iter_member_by_def_
        # orphan @0x0410
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
        checks = self.checks
        cls_name = enumeration.__name__
        if (Flag is not None) and issubclass(enumeration, Flag):
            enum_type = 'flag'
        elif issubclass(enumeration, Enum):
            enum_type = 'enum'
        else:
            raise TypeError('the \'verify\' decorator only works with Enum and Flag')
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
                pass
            if key not in simple_keys:
                failed.append('missing key: %r' % (key))
            checked_value = checked_dict[key]
            simple_value = simple_dict[key]
            if callable(checked_value):
                pass
            if key == '__doc__':
                compressed_checked_value = checked_value.replace(' ', '').replace('\t', '')
                compressed_simple_value = simple_value.replace(' ', '').replace('\t', '')
                if compressed_checked_value != compressed_simple_value:
                    failed.append("""%r:
         %s
         %s""" % (key, 'checked -> %r' % (checked_value), 'simple  -> %r' % (simple_value)))
            failed.append("""%r:
         %s
         %s""" % (key, 'checked -> %r' % (checked_value), 'simple  -> %r' % (simple_value)))
            failed.append('extra key:   %r' % (key))
    elif failed:
        raise TypeError("""enum mismatch:
   %s""" % """
   """.join(failed))
    # orphan @0x0158
    failed.sort()
    # orphan @0x0164
    # orphan @0x0166
    failed_member = []
    # orphan @0x0174
    failed.append('missing member from simple enum: %r' % name)
    # orphan @0x0184
    # orphan @0x018C
    failed.append('extra member in simple enum: %r' % name)
    # orphan @0x019C
    checked_member_dict = checked_enum[name].__dict__
    checked_member_keys = list(checked_member_dict.keys())
    simple_member_dict = simple_enum[name].__dict__
    simple_member_keys = list(simple_member_dict.keys())
    # orphan @0x01D4
    # orphan @0x01D6
    # orphan @0x01E0
    # orphan @0x01E2
    # orphan @0x01EA
    failed_member.append('missing key %r not in the simple enum member %r' % (key, name))
    # orphan @0x01FE
    # orphan @0x0208
    failed_member.append('extra key %r in simple enum member %r' % (key, name))
    # orphan @0x021C
    checked_value = checked_member_dict[key]
    simple_value = simple_member_dict[key]
    # orphan @0x0236
    failed_member.append("""%r:
         %s
         %s""" % (key, 'checked member -> %r' % (checked_value), 'simple member  -> %r' % (simple_value)))
    # orphan @0x0256
    # orphan @0x0258
    # orphan @0x025E
    failed.append("""%r member mismatch:
      %s""" % (name, """
      """.join(failed_member)))
    # orphan @0x0276
    # orphan @0x0278
    # orphan @0x027C
    # orphan @0x027E
    # orphan @0x028A
    # orphan @0x0296
    # orphan @0x0298
    # orphan @0x02A2
    # orphan @0x02AC
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)
    # orphan @0x02D0
    checked_method = checked_method.__func__
    simple_method = simple_method.__func__
    # orphan @0x02DC
    # orphan @0x02E6
    failed.append('%r:  %-30s %s' % (method, 'checked -> %r' % (checked_method), 'simple -> %r' % (simple_method)))
    # orphan @0x0306
    # orphan @0x030A
def _old_convert_(etype, name, module, filter, source):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    else:
        source = module_globals
    members = _old_convert_.<locals>.<listcomp>(source.items())
    try:
        members.sort(key=_old_convert_.<locals>.<lambda>)
    except TypeError:
        pass
    if boundary:
        return cls
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 304 instr
