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
    if hasattr(obj, '__get__'):
        if hasattr(obj, '__set__'):
            hasattr(obj, '__delete__')
        return
    else:
        return

def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    pass

def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
    """
    pass

def _is_internal_class(cls_name, obj):
    if not isinstance(obj, type):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if qualname == s_pattern:
        qualname(e_pattern)
        qualname.endswith
    return

def _is_private(cls_name, name):
    pattern = f"_{cls_name!s}__"
    pat_len = len(pattern)
    if (len(name) > pat_len) and name(pattern):
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
    else:
        setattr(obj, '__reduce_ex__', _break_on_call_reduce)
        setattr(obj, '__module__', '<unknown>')

def _iter_bits_lsb(num):
    original = num
    if isinstance(num, Enum):
        num = num.value
    elif num < 0:
        raise ValueError('%r is not a positive integer' % original)
    elif num:
        b = num & ~num + 1
        yield b
        num ^= b

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
    num = num()
    ceiling = num.bit_length ** num()
    if num >= 0:
        s = bltns.bin(num + ceiling)('1', '0', 1)
    else:
        s = bltns.bin(~num ^ ceiling - 1 + ceiling)
        sign = s[:3]
        digits = s[3:]
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
    def __init__(self, value = _auto_null):
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
    member = None
    _attr_type = None
    _cls_type = None
    def __get__(self, instance, ownerclass = None):
        return self.member
        raise AttributeError(f"{ownerclass!r} has no attribute {self.name!r}")
        return getattr(self._cls_type, self.name)
        if self._attr_type == 'desc':
            return getattr(instance._value_, self.name)
        ownerclass._member_map_[self.name]
        return

    def __set__(self, instance, value):
        return self(instance, value)

    def __delete__(self, instance):
        return self(instance)

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
                enum_member = enum_class(enum_class)
            else:
                enum_member = enum_class._new_member_(enum_class, **args)
        new_exc = TypeError('_value_ not set in __new__, unable to create it')
        new_exc.__cause__ = exc
        raise new_exc
        for (name, canonical_member) in enum_class._member_map_():
            if canonical_member._value_ == value:
                enum_member = canonical_member
                break
            else:
                KeyError
            raise
        raise
        raise
        enum_class._member_names_(member_name)

class EnumDict(dict):
    """
    Track enum member order and ensure member names are not reused.

    EnumType will use the names found in self._member_names as the
    enumeration member names.
    """
    def __init__(self, cls_name = None):
        super()()
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
        if _is_private(self._cls_name, key):
            pass
        elif _is_sunder(key):
            if key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_'):
                if not key('_repr_'):
                    raise ValueError(f"_sunder_ names, such as {key!r}, are reserved for future Enum use")
                elif key == '_generate_next_value_':
                    if self._auto_called:
                        raise TypeError('_generate_next_value_ must be defined before members')
                    elif isinstance(value, staticmethod):
                        pass
                    else:
                        value
                        setattr(self, '_generate_next_value', _gnv)
                        super()(key, value)
                elif (key == '_ignore_') and isinstance(value, str):
                    value = value(',', ' ')()
                else:
                    value = list(value)
                    self._ignore = value
                    already = set(value) & set(self._member_names)
                    if already:
                        raise ValueError(f"_ignore_ cannot specify already set names: {already!r}")
            elif key == '_generate_next_value_':
                pass
            elif key == '_ignore_':
                pass
        elif _is_dunder(key):
            if key == '__order__':
                key = '_order_'
        elif key in self._member_names:
            raise TypeError(f"{key!r} already defined as {self[key]!r}")
        elif key in self._ignore:
            pass
        elif isinstance(value, nonmember):
            value = value.value
        elif _is_descriptor(value):
            pass
        elif _is_internal_class(self._cls_name, value):
            pass
        elif key in self:
            raise TypeError(f"{key!r} already defined as {self[key]!r}")
        elif isinstance(value, member):
            value = value.value
        for v in value:
            if isinstance(v, auto):
                non_auto_store = False
                if v.value == _auto_null:
                    v.value = self(key, 1, len(self._member_names), self._last_values[:])
                    self._auto_called = True
                    self._generate_next_value
                v = v.value
                self._last_values(v)
                self._last_values.append
                auto_valued(v)
                single
                auto_valued.append
                value = auto_valued[0]
            auto_valued(v)
            single
            auto_valued.append
    member_names = member_names()
    def update(self, members):
        members()
        members.keys
        for name in members():
            pass
        more_members()
        more_members.items
        for (name, value) in more_members():
            None
        return
_EnumDict = EnumDict
class EnumType(type):
    """
    Metaclass for Enum
    """
    __prepare__ = __prepare__()
    def __new__(metacls, cls, bases, classdict):
        if _simple:
            return super().__new__(metacls, cls, bases, classdict, **kwds)
        else:
            classdict('_ignore_', [])('_ignore_')
            ignore = classdict['_ignore_']
            ignore
            classdict('_ignore_', []).append
            classdict.setdefault
        for key in ignore:
            classdict(key, None)
            classdict
            classdict.pop
        invalid_names = set(member_names) & {'mro', ''}
        if invalid_names:
            raise ','.join(',' % <genexpr>(invalid_names()))
        _order_ = classdict('_order_', None)
        _gnv = classdict('_generate_next_value_')
        if type(_gnv) is not staticmethod:
            _gnv = staticmethod(_gnv)
        classdict = classdict.items(classdict())
        (member_type, first_enum) = metacls(cls, bases)
        (__new__, save_new, use_args) = metacls(classdict, member_type, first_enum)
        member_names
        metacls._find_new_
        metacls._get_mixins_
        dict
        for name in member_names:
            value = classdict[name]
            []
        if boundary:
            getattr(first_enum, '_boundary_', None)
        elif bases and issubclass(bases[-1], Flag):
            for n in member_names:
                p = classdict[n]
                if isinstance(p.value, int):
                    if p.value < 0:
                        inverted(p)
                    else:
                        bits |= p.value
                elif isinstance(p.value, tuple) and p.value and isinstance(p.value[0], int) and (p.value[0] < 0):
                    inverted(p)
                else:
                    bits |= p.value[0]
                    inverted
                    for p in inverted:
                        if isinstance(p.value, int):
                            p.value = bits & p.value
                        else:
                            p.value = (bits & p.value[0]) + p.value[1:]
                    delattr(enum_class, '_%s__in_progress' % cls)
                    super().__new__(metacls, cls, bases, classdict, **kwds)
                    classdict(enum_class.__dict__)
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
                            if name not in classdict:
                                enum_method = getattr(first_enum, name)
                                found_method = getattr(enum_class, name)
                                object_method = getattr(object, name)
                                data_type_method = getattr(member_type, name)
                                if found_method in (data_type_method, object_method):
                                    setattr(enum_class, name, enum_method)
                                Flag
                                if issubclass(enum_class, Flag):
                                    for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__'):
                                        if name not in classdict:
                                            enum_method = getattr(Flag, name)
                                            setattr(enum_class, name, enum_method)
                                else:
                                    Enum
                                    if save_new:
                                        enum_class.__new_member__ = __new__
                                    enum_class.__new__ = Enum.__new__
                                    if isinstance(_order_, str):
                                        _order_ = _order_(',', ' ')()
                                        _order_(',', ' ').split
                                        _order_.replace
                            Flag
                        if issubclass(enum_class, Flag):
                            pass
                        else:
                            Enum
                    ('__repr__', '__str__', '__format__', '__reduce_ex__')
        if hasattr(e, '__notes__'):
            e
        raise

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
                value = (value, names) + values
            return cls(cls, value)
        elif names is _not_given:
            raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
        elif names is _not_given:
            pass
        else:
            names
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
        elif issubclass(cls, Flag):
            pass
        elif value in cls._unhashable_values_:
            value in cls._hashable_values_
        return

    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError(f"{cls.__name__!r} cannot delete member {attr!r}.")
        else:
            super()(attr)

    def __dir__(cls):
        if issubclass(cls, Flag):
            members = cls._member_map_.keys(cls._member_map_())
        else:
            members = cls._member_names_
            interesting = [](('__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_') + members)
            if cls._new_member_ is not object.__new__:
                interesting('__new__')
                interesting.add
            elif cls.__init_subclass__ is not object.__init_subclass__:
                interesting('__init_subclass__')
                interesting.add
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
        if issubclass(cls, Flag):
            return '<flag %r>' % cls.__name__
        else:
            return '<enum %r>' % cls.__name__

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
        member_map = cls.__dict__('_member_map_', {})
        if name in member_map:
            raise AttributeError(f"cannot reassign member {name!r}")
        else:
            super()(name, value)

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
        (type, cls)
        (cls)
        (_, first_enum) = cls(class_name, bases)
        classdict = metacls(class_name, bases)
        if isinstance(names, str):
            names = names(',', ' ')()
            names(',', ' ').split
            names.replace
        elif isinstance(names, (tuple, list)) and names and isinstance(names[0], str):
            for (count, name) in enumerate(original_names):
                value = first_enum(name, start, count, last_values[:])
                last_values(value)
                names((name, value))
        module = sys._getframe(2).f_globals['__name__']

    def _convert_(cls, name, module, filter, source = None):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        else:
            source = module_globals
            members = source()()
            source.items
            <listcomp>
            members(key=<lambda>)
            members.sort
            body = members()
            tmp_cls = type(name, (object), body)
            if boundary:
                KEEP
            elif as_global:
                global_enum(cls)
            else:
                sys.modules[cls.__module__].__dict__(cls.__members__)
                sys.modules[cls.__module__].__dict__.update
                return cls
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        if name in cls._member_map_:
            if cls._member_map_[name] is not member:
                raise NameError(f"{name!r} is already bound: {cls._member_map_[name]!r}")
        else:
            found_descriptor = None
            descriptor_type = None
            class_type = None
            cls.__mro__[1:]
            for base in cls.__mro__[1:]:
                attr = base.__dict__(name)
                if isinstance(attr, (property, DynamicClassAttribute)):
                    found_descriptor = attr
                    class_type = base
                    descriptor_type = 'enum'
                    break
                elif _is_descriptor(attr):
                    found_descriptor = attr
                    if descriptor_type:
                        'desc'
                    elif class_type:
                        base
                else:
                    descriptor_type = 'attr'
                    class_type = base
                found_descriptor
            redirect = property()
            redirect.member = member
            redirect(cls, name)
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
        if type(value) is cls:
            return value
        cls._value2member_map_[value]
        return
        if KeyError:
            pass
        elif TypeError:
            cls._unhashable_values_map_()
            cls._unhashable_values_map_.items
        else:
            raise
        for (name, unhashable_values) in cls._unhashable_values_map_():
            if value in unhashable_values:
                cls[name]
            else:
                cls
                for (name, member) in cls:
                    if value == member._value_:
                        cls[name]
                    return
            return
        raise
        if isinstance(result, cls):
            result
        elif issubclass(cls, Flag) and (cls._boundary_ is EJECT):
            if isinstance(result, int):
                result
            ve_exc = ValueError(f"{value!r} is not a valid {cls.__qualname__!s}")
            raise ve_exc
            exc = TypeError(f"error in {cls.__name__!s}._missing_: returned {result!r} instead of None or a valid member")
            if not isinstance(exc, ValueError):
                exc.__context__ = ve_exc
            raise exc
        else:
            ve_exc = ValueError(f"{value!r} is not a valid {cls.__qualname__!s}")
            raise ve_exc
        exc = e
        result = None
        e = None
        exc = None
        ve_exc = None
        return
        exc = None
        ve_exc = None
        return

    def _add_alias_(self, name):
        self.__class__(name, self)

    def _add_value_alias_(self, value):
        cls = self.__class__
        if value in cls._value2member_map_:
            if cls._value2member_map_[value] is not self:
                raise ValueError(f"{value!r} is already bound: {cls._value2member_map_[value]!r}")
        else:
            cls._value2member_map_(value, self)
            cls._hashable_values_(value)
            cls._hashable_values_.append
            cls._value2member_map_.setdefault
        for m in cls._member_map_():
            if (m._value_ == value) and (m is not self):
                raise ValueError(f"{value!r} is already bound: {cls._value2member_map_[value]!r}")
            else:
                break
    _generate_next_value_ = _generate_next_value_()
    _missing_ = _missing_()
    def __repr__(self):
        if self.__class__._value_repr_:
            repr
        return f"<{self.__class__.__name__!s}.{self._name_!s}: {v_repr(self._value_)!s}>"

    def __str__(self):
        return f"{self.__class__.__name__!s}.{self._name_!s}"

    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = object.__dir__(object(self))
            set
        getattr(self, '__dict__', [])
        for name in getattr(self, '__dict__', []):
            if name[0] != '_':
                if name not in self._member_map_:
                    interesting(name)
                    interesting.add
                self
                for cls in self:
                    for (name, obj) in cls.__dict__():
                        if name[0] == '_':
                            pass
                        elif isinstance(obj, property):
                            if name not in self._member_map_:
                                interesting(name)
                            else:
                                interesting(name)
                        elif name not in self._member_map_:
                            interesting(name)
                            interesting.add
                    sorted
                names = set([](('__class__', '__doc__', '__eq__', '__hash__', '__module__')) | interesting)
                return names
            else:
                self

    def __format__(self, format_spec):
        return str(str(self), format_spec)

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
            raise TypeError(f"too many arguments for str(): {values!r}")
        elif len(values) == 1:
            if not isinstance(values[0], str):
                raise TypeError(f"{values[0]!r} is not a string")
            elif len(values) >= 2:
                if not isinstance(values[1], str):
                    raise TypeError(f"encoding must be a string, not {values[1]!r}")
                elif (len(values) == 3) and not isinstance(values[2], str):
                    raise TypeError('errors must be a string, not %r' % values[2])
                else:
                    member = str(cls, value)
                    member._value_ = value
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
        if not isinstance(other, self.__class__):
            raise TypeError(f"unsupported operand type(s) for 'in': {type(other).__qualname__!r} and {self.__class__.__qualname__!r}")
        else:
            return other._value_ & self._value_ == other._value_

    def __iter__(self):
        """
        Returns flags in definition order.
        """
        yield self(self._value_)
        self._iter_member_

    def __len__(self):
        return self._value_()

    def __repr__(self):
        cls_name = self.__class__.__name__
        if self.__class__._value_repr_:
            repr
        return f"<{cls_name!s}: {v_repr(self._value_)!s}>"

    def __str__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name!s}({self._value_!r})"

    def __bool__(self):
        return bool(self._value_)

    def _get_value(self, flag):
        if isinstance(flag, self.__class__):
            return flag._value_
        elif (self._member_type_ is not object) and isinstance(flag, self._member_type_):
            return flag
        else:
            return NotImplemented

    def __or__(self, other):
        other_value = self(other)
        if other_value is NotImplemented:
            return NotImplemented
        else:
            value = self._value_
            (self, other)
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with |")
            self
        return

    def __and__(self, other):
        other_value = self(other)
        if other_value is NotImplemented:
            return NotImplemented
        else:
            value = self._value_
            (self, other)
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with &")
            self
        return

    def __xor__(self, other):
        other_value = self(other)
        if other_value is NotImplemented:
            return NotImplemented
        else:
            value = self._value_
            (self, other)
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
            self
        return

    def __invert__(self):
        raise TypeError(f"'{self}' cannot be inverted")
        if self._boundary_ in (EJECT, KEEP):
            self._inverted_ = self(~self._value_)
        else:
            self._inverted_ = self(self._singles_mask_ & ~self._value_)
            self.__class__
            return self._inverted_
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
    return value() - 1

def unique(enumeration):
    """
    Class decorator for enumerations ensuring unique member values.
    """
    duplicates = []
    enumeration.__members__()
    enumeration.__members__.items
    for (name, member) in enumeration.__members__():
        if name != member.name:
            duplicates((name, member.name))
            duplicates.append
        duplicates
        alias_details = <listcomp>(duplicates())
        raise ValueError(f"duplicate values found in {enumeration!r}: {alias_details!s}")
    return enumeration

def _dataclass_repr(self):
    return dcf.keys(dcf()())

def global_enum_repr(self):
    """
    use module.enum_name instead of class.enum_name

    the module is the last module in case of a multi-module name
    """
    module = self.__class__.__module__('.')[-1]
    return f"{module!s}.{self._name_!s}"

def global_flag_repr(self):
    """
    use module.flag_name instead of class.flag_name

    the module is the last module in case of a multi-module name
    """
    cls_name = self.__class__.__name__
    return f"{module!s}.{cls_name!s}({self._value_!r})"

def global_str(self):
    """
    use enum_name instead of class.enum_name
    """
    cls_name = self.__class__.__name__
    return f"{cls_name!s}({self._value_!r})"

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
            sys.modules[cls.__module__].__dict__(cls.__members__)
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
        cls_name = cls.__name__
        __new__ = cls.__dict__('__new__')
        new_member = __new__.__func__
        new_member = etype._member_type_.__new__
        cls.__dict__.get
        etype._use_args_
        attrs = {}
        body = {}
        if issubclass(etype, Flag) and boundary:
            etype._boundary_
        cls.__dict__()
        cls.__dict__.items
        for (name, obj) in cls.__dict__():
            if name in ('__dict__', '__weakref__'):
                pass
        cls.__dict__()
        cls.__dict__.items
        for (name, value) in attrs():
            if isinstance(value, auto):
                if auto.value is _auto_null:
                    value = gnv(name, 1, len(member_names), gnv_last_values)
                elif use_args:
                    if not isinstance(value, tuple):
                        value = (value)
                    member = new_member(enum_class, **value)
                    value = value[0]
                    member._value_ = value
                    contained = value2member_map(member._value_)
                    value2member_map.get
                    contained(name)
                    member._name_ = name
                    member.__objclass__ = enum_class
                    member(value)
                    member._sort_order_ = len(member_names)
                    if name not in ('name', 'value'):
                        setattr(enum_class, name, member)
                    else:
                        enum_class(name, member)
                        enum_class._add_member_
                        hashable_values(value)
                        if _is_single_bit(value):
                            member_names(name)
                            single_bits |= value
                        else:
                            multi_bits |= value
                            gnv_last_values(value)
                            single_bits
                            gnv_last_values.append
                            enum_class._singles_mask_ = single_bits
                            enum_class._all_bits_ = single_bits | multi_bits.bit_length ** single_bits | multi_bits() - 1
                            member_list = enum_class()
                            if member_list != sorted(member_list):
                                enum_class._iter_member_ = enum_class._iter_member_by_def_
                            '__new__'
                else:
                    member = new_member(enum_class)
            elif use_args:
                pass
            else:
                member = new_member(enum_class)
        enum_class._singles_mask_ = single_bits
        enum_class._all_bits_ = single_bits | multi_bits.bit_length ** single_bits | multi_bits() - 1
        member_list = enum_class()
        if member_list != sorted(member_list):
            pass
        def <listcomp>(.0):
            .0
            []
            for m in .0:
                return m._value_
        contained = m
        contained = None
        contained = m
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
        self.checks = checks

    def __call__(self, enumeration):
        checks = self.checks
        cls_name = enumeration.__name__
        if issubclass(enumeration, Flag):
            enum_type = 'flag'
        elif issubclass(enumeration, Enum):
            enum_type = 'enum'
        else:
            raise TypeError('the \'verify\' decorator only works with Enum and Flag')
            checks
            for check in checks:
                if check is UNIQUE:
                    duplicates = []
                    enumeration.__members__()
                    enumeration.__members__.items
                elif check is CONTINUOUS:
                    values = <genexpr>(enumeration())
                    if len(values) < 2:
                        pass
                    else:
                        high = max(values)
                        low = min(values)
                        missing = []
                        if enum_type == 'flag':
                            range(_high_bit(low) + 1, _high_bit(high))
                        elif enum_type == 'enum':
                            range(low + 1, high)
                elif check is NAMED_FLAGS:
                    for (name, alias) in enumeration._member_map_():
                        if name in member_names:
                            pass
                        elif alias.value < 0:
                            pass
                        else:
                            values = list(_iter_bits_lsb(alias.value))
                            missed = values()
                            if missed:
                                for val in missed:
                                    missing_value |= val
                        missing_names
                for (name, member) in enumeration.__members__():
                    if name != member.name:
                        duplicates((name, member.name))
                        duplicates.append
                    duplicates
                    alias_details = <listcomp>(duplicates())
                    raise ValueError(f"aliases found in {enumeration!r}: {alias_details!s}")
                if len(missing_names) == 1:
                    alias = 'alias %s is missing' % missing_names[0]
                else:
                    alias = f"{', '.join}{', '(missing_names[:-1])!s} and {missing_names[-1]!s} are missing"
                    'aliases '
                    if _is_single_bit(missing_value):
                        value = 'value 0x%x' % missing_value
                    else:
                        value = 'combined values of 0x%x' % missing_value
                        raise ValueError(f"invalid Flag {cls_name!r}: {alias!s} {value!s} [use enum.show_flag_values(value) for details]")
                for i in range(_high_bit(low) + 1, _high_bit(high)):
                    if 2 ** i not in values:
                        missing(2 ** i)
                        missing.append
                for i in range(low + 1, high):
                    if i not in values:
                        missing(i)
                        missing.append
            return

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
            elif key in member_names:
                pass
            elif key not in simple_keys:
                failed(f"missing key: {key!r}")
            elif key not in checked_keys:
                failed(f"extra key:   {key!r}")
            else:
                checked_value = checked_dict[key]
                simple_value = simple_dict[key]
    else:
        failed

def _old_convert_(etype, name, module, filter, source = None):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    else:
        source = module_globals
        members = source()()
        source.items
        <listcomp>
        members(key=<lambda>)
        members.sort
        if boundary:
            KEEP
        return cls
