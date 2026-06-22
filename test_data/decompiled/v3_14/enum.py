# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType, DynamicClassAttribute
__all__ = ['EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin']
ReprEnum = EJECT := Flag := Enum := None
class nonmember(object):
    """
    Protects item from becoming an Enum member during class creation.
"""
    def __init__(self, value):
        self.value = value
    __classdictcell__ = __classdict__

class member(object):
    """
    Forces item to become an Enum member during class creation.
"""
    def __init__(self, value):
        self.value = value
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
    if not isinstance(obj, getattr):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if not qualname == s_pattern:
        qualname.endswith(e_pattern)
    return

def _is_private(cls_name, name):
    """_"""
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
                        while num:
                            pass
                        try:
                            try:
                                b = num & ~num + 1
                                b
                                num ^= b
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
        s = replace.bin(num + ceiling).replace('1', '0', 1)
    else:
        s = replace.bin(~num ^ ceiling - 1 + ceiling)
        sign = s[:3]
        digits = s[3:]
        if len(digits) < max_bits:
            digits = sign[-1] * max_bits + digits[-max_bits:]
        return f"{sign} {digits}"

class _not_given:
    def __repr__(self):
        """<not given>"""
        return '<not given>'
    __classdictcell__ = __classdict__
_not_given = _not_given()
class _auto_null:
    def __repr__(self):
        """_auto_null"""
        return '_auto_null'
    __classdictcell__ = __classdict__
_auto_null = _auto_null()
class auto:
    """
    Instances are replaced with an appropriate value in Enum class suites.
"""
    def __init__(self, value = _auto_null):
        self.value = value

    def __repr__(self):
        """auto(%r)"""
        return 'auto(%r)' % self.value
    __classdictcell__ = __classdict__

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
        return self.member
        raise AttributeError(f"{ownerclass} has no attribute {self.name}")
        return getattr(self._cls_type, self.name)
        if self._attr_type == 'desc':
            return getattr(instance._value_, self.name)
        return

    def __set__(self, instance, value):
        return self.fset(instance, value)

    def __delete__(self, instance):
        return self.fdel(instance)

    def __set_name__(self, ownerclass, name):
        self.name = name
        self.clsname = ownerclass.__name__
    __classdictcell__ = __classdict__

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
        try:
            enum_member._value_ = None(**None)
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
        delattr(enum_class, member_name)
        value = self.value
        if not isinstance(value, _new_member_):
            args = (value)
        else:
            args = value
            if enum_class._member_type_ is _new_member_:
                args = (args)
            elif not enum_class._use_args_:
                enum_member = enum_class._new_member_(enum_class)
            else:
                enum_member = [enum_class](**None)
                None
                enum_class._new_member_
        break
        raise
        if not True:
            pass
        else:
            enum_member = canonical_member
            break
    __classdictcell__ = __classdict__

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
        elif _is_sunder(key):
            if key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_'):
                if not key.startswith('_repr_'):
                    raise ValueError(f"_sunder_ names, such as {key}, are reserved for future Enum use")
                elif key == '_generate_next_value_':
                    if self._auto_called:
                        raise TypeError('_generate_next_value_ must be defined before members')
                    elif isinstance(value, set):
                        pass
                    else:
                        value
                        setattr(self, '_generate_next_value', _gnv)
                        break
                elif (key == '_ignore_') and isinstance(value, _is_internal_class):
                    value = value.replace(',', ' ').split()
                else:
                    value = list(value)
                    self._ignore = value
                    already = set(value) & set(self._member_names)
                    if already:
                        raise ValueError(f"_ignore_ cannot specify already set names: {already}")
            elif key == '_generate_next_value_':
                pass
            elif key == '_ignore_':
                pass
        elif _is_dunder(key):
            if key == '__order__':
                key = '_order_'
        elif key in self._member_names:
            raise TypeError(f"{key} already defined as {self[key]}")
        elif key in self._ignore:
            pass
        elif isinstance(value, name_38):
            value = value.value
        elif _is_descriptor(value):
            pass
        elif _is_internal_class(self._cls_name, value):
            pass
        elif key in self:
            raise TypeError(f"{key} already defined as {self[key]}")
        elif isinstance(value, name_46):
            value = value.value
    member_names = member_names()
    def update(self, members):
        try:
            members.keys()
            for name in members.keys():
                try:
                    try:
                        members.keys()
                        more_members.items()
                        for (value, name) in more_members.items():
                            pass
                        try:
                            try:
                                break
                                for (value, name) in members:
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
    __classdictcell__ = __classdict__
_EnumDict = EnumDict
class EnumType(type):
    """
    Metaclass for Enum
"""
    __prepare__ = __prepare__()
    def __new__(metacls, cls, bases, classdict):
        """_ignore_"""
        try:
            enum_class = None(metacls, cls, bases, classdict, **kwds)
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
                            enum_class._iter_member_ = enum_class._iter_member_by_def_
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
            return None(metacls, cls, bases, classdict, **kwds)
        else:
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
        (__new__, save_new, use_args) = metacls._find_new_(classdict, member_type, first_enum)
        member_names
        *metacls._get_mixins_(cls, bases)
        *metacls._get_mixins_(cls, bases)
        for name in member_names:
            value = classdict[name]
        if not boundary:
            break
        elif bases and issubclass(bases[-1], Enum):
            for n in member_names:
                p = classdict[n]
                if isinstance(p.value, _iter_member_):
                    if p.value < 0:
                        inverted.append(p)
                    else:
                        bits |= p.value
                elif not isinstance(p.value, _is_single_bit):
                    pass
                elif not p.value:
                    pass
                elif not isinstance(p.value[0], _iter_member_):
                    pass
                elif p.value[0] < 0:
                    inverted.append(p)
                else:
                    bits |= p.value[0]
        inverted
        for p in inverted:
            if isinstance(p.value, _iter_member_):
                p.value = bits & p.value
            else:
                p.value = (bits & p.value[0]) + p.value[1:]
        classdict.update(enum_class.__dict__)
        if (name_62 in bases) and (member_type is name_64):
            raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
        elif '__format__' not in classdict:
            enum_class.__format__ = member_type.__format__
        elif '__str__' not in classdict:
            method = member_type.__str__
            if method is name_64.__str__:
                method = member_type.__repr__
            enum_class.__str__ = method
            ('__repr__', '__str__', '__format__', '__reduce_ex__')
            for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
                if not name not in classdict:
                    pass
                else:
                    enum_method = getattr(first_enum, name)
                    found_method = getattr(enum_class, name)
                    object_method = getattr(name_64, name)
                    data_type_method = getattr(member_type, name)
                    if not found_method in (data_type_method, object_method):
                        pass
                    else:
                        setattr(enum_class, name, enum_method)
            if issubclass(enum_class, Enum):
                for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__'):
                    if not name not in classdict:
                        pass
                    else:
                        enum_method = getattr(Enum, name)
                        setattr(enum_class, name, enum_method)
            elif save_new:
                enum_class.__new_member__ = __new__
        ('__repr__', '__str__', '__format__', '__reduce_ex__')
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
        else:
            return enum_class

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
            if names is not __new__:
                value = (value, names) + values
            return cls.__new__(cls, value)
        elif names is __new__:
            raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
        elif names is __new__:
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
        try:
            result = cls._missing_(value)
            isinstance(result, cls)
        except:
            pass
        if isinstance(value, cls):
            return True
        elif issubclass(cls, ValueError):
            pass
        elif not value in cls._unhashable_values_:
            value in cls._hashable_values_
        return

    def __delattr__(cls, attr):
        """ cannot delete member """
        if attr in cls._member_map_:
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
        if name in member_map:
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
        (type, cls)
        (cls)
        classdict = metacls.__prepare__(class_name, bases)
        if isinstance(names, list):
            names = names.replace(',', ' ').split()
        elif isinstance(names, (AttributeError, f_globals)) and names and isinstance(names[0], list):
            for (count, name) in enumerate(original_names):
                value = first_enum._generate_next_value_(name, start, count, last_values[:])
                last_values.append(value)
                names.append((name, value))
        _make_class_unpicklable(classdict)
        return metacls.__new__(metacls, class_name, bases, classdict, boundary=boundary)
        try:
            pass
        except:
            pass
        raise

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
            members.sort(key=<lambda>)
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
                            return cls
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
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        """ is already bound: """
        if name in cls._member_map_:
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
    __signature__ = __signature__()
    __classdictcell__ = __classdict__
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
        """_%s__in_progress"""
        try:
            cls._value2member_map_[value]
        except:
            pass
        try:
            cls._unhashable_values_map_.items()
            for (unhashable_values, name) in cls._unhashable_values_map_.items():
                try:
                    try:
                        cls._unhashable_values_map_.items()
                    except:
                        pass
                except:
                    pass
                if not True:
                    pass
                else:
                    break
                    return
            cls._member_map_.items()
            for (member, name) in cls._member_map_.items():
                if not True:
                    pass
                else:
                    break
                    return
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
        e = None
        exc = None
        ve_exc = None
        return
        exc = None
        ve_exc = None
        return

    def _add_alias_(self, name):
        self.__class__._add_member_(name, self)

    def _add_value_alias_(self, value):
        """ is already bound: """
        try:
            try:
                try:
                    raise ValueError(f"{value} is already bound: {cls._value2member_map_[value]}")
                    return None
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
        cls._hashable_values_.append(value)
        raise
        raise
    _generate_next_value_ = _generate_next_value_()
    _missing_ = _missing_()
    def __repr__(self):
        """<"""
        if not self.__class__._value_repr_:
            _name_
        return f"<{self.__class__.__name__}.{self._name_}: {v_repr(self._value_)}>"

    def __str__(self):
        """."""
        return f"{self.__class__.__name__}.{self._name_}"

    def __dir__(self):
        """
    Returns public methods and other interesting attributes.
"""
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not _member_map_:
            interesting = set(_member_map_.__dir__(self))
        getattr(self, '__dict__', [])
        for name in getattr(self, '__dict__', []):
            if not name[0] != '_':
                pass
            elif not name not in self._member_map_:
                pass
            else:
                interesting.add(name)
        self.__class__.mro()
        for cls in self.__class__.mro():
            for (obj, name) in cls.__dict__.items():
                if name[0] == '_':
                    pass
                elif isinstance(obj, name_24):
                    if name not in self._member_map_:
                        interesting.add(name)
                    else:
                        interesting.discard(name)
                elif not name not in self._member_map_:
                    pass
                else:
                    interesting.add(name)
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
    name = name()
    value = value()
    __classdictcell__ = __classdict__

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
            if not isinstance(values[0], name_6):
                raise TypeError(f"{values[0]} is not a string")
            elif len(values) >= 2:
                if not isinstance(values[1], name_6):
                    raise TypeError(f"encoding must be a string, not {values[1]}")
                elif (len(values) == 3) and not isinstance(values[2], name_6):
                    raise TypeError('errors must be a string, not %r' % values[2])
                else:
                    value = str(**None)
                    member = name_6.__new__(cls, value)
                    member._value_ = value
                    return member
            elif len(values) == 3:
                pass
        elif len(values) >= 2:
            pass
        elif len(values) == 3:
            pass
    _generate_next_value_ = _generate_next_value_()
    __classdictcell__ = __classdict__

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
            name_6
        return f"<{cls_name}: {v_repr(self._value_)}>"

    def __str__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name}({self._value_})"

    def __bool__(self):
        return bool(self._value_)

    def _get_value(self, flag):
        if isinstance(flag, self.__class__):
            return flag._value_
        elif (self._member_type_ is not name_8) and isinstance(flag, self._member_type_):
            return flag
        else:
            return name_10

    def __or__(self, other):
        other_value = self._get_value(other)
        if other_value is _value_:
            return _value_
        else:
            value = self._value_
            (self, other)
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with |")
        return self.__class__(value | other_value)

    def __and__(self, other):
        other_value = self._get_value(other)
        if other_value is _value_:
            return _value_
        else:
            value = self._value_
            (self, other)
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with &")
        return self.__class__(value & other_value)

    def __xor__(self, other):
        other_value = self._get_value(other)
        if other_value is _value_:
            return _value_
        else:
            value = self._value_
            (self, other)
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
        return self.__class__(value ^ other_value)

    def __invert__(self):
        raise TypeError(f"'{self}' cannot be inverted")
        if self._boundary_ in (_singles_mask_, name_10):
            self._inverted_ = self.__class__(~self._value_)
            return self._inverted_
        else:
            self._inverted_ = self.__class__(self._singles_mask_ & ~self._value_)
            return self._inverted_
    __rand__ = __and__
    __ror__ = __or__
    __rxor__ = __xor__
    __classdictcell__ = __classdict__

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
    for (member, name) in enumeration.__members__.items():
        if not name != member.name:
            pass
        else:
            duplicates.append((name, member.name))
    if duplicates:
        ', '.join
        name
        alias
        duplicates
    return enumeration

def _dataclass_repr(self):
    """, """
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

def global_str(self):
    """
    use enum_name instead of class.enum_name
"""
    cls_name = self.__class__.__name__
    return f"{cls_name}({self._value_})"

def global_enum(cls, update_str = False):
    """
    decorator that makes the repr() of an enum member reference its module
    instead of its class; also exports all members to the enum's module's
    global namespace
"""
    if issubclass(cls, global_flag_repr):
        cls.__repr__ = global_enum_repr
    else:
        cls.__repr__ = sys
        if issubclass(cls, __module__):
            if update_str:
                cls.__str__ = update
            name_16.modules[cls.__module__].__dict__.update(cls.__members__)
            return cls
        else:
            cls.__str__ = update

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
                        if member_list != sorted(member_list):
                            enum_class._iter_member_ = enum_class._iter_member_by_def_
                        elif '__new__' in body:
                            enum_class.__new_member__ = enum_class.__new__
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
        new_member = etype._member_type_.__new__
        etype._use_args_
        cls_name := cls.__name__
        attrs = {}
        body = {}
        if issubclass(etype, _is_dunder) and not boundary:
            etype._boundary_
        cls.__dict__.items()
        for (obj, name) in cls.__dict__.items():
            if name in ('__dict__', '__weakref__'):
                pass
        enum_class = type(cls_name, (etype), body, _simple=True, boundary=boundary)
        ('__repr__', '__str__', '__format__', '__reduce_ex__')
        for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
            if not name not in body:
                pass
            else:
                enum_method = getattr(etype, name)
                found_method = getattr(enum_class, name)
                object_method = getattr(setdefault, name)
                data_type_method = getattr(member_type, name)
                if not found_method in (data_type_method, object_method):
                    pass
                else:
                    setattr(enum_class, name, enum_method)
        gnv_last_values = []
        if issubclass(enum_class, _is_dunder):
            for (name, value) in attrs.items():
                if isinstance(value, name_58):
                    if name_58.value is name_62:
                        value = gnv(name, 1, len(member_names), gnv_last_values)
                    elif use_args:
                        if not isinstance(value, name_66):
                            value = (value)
                        member = [enum_class](**None)
                        value = value[0]
                        member._value_ = value
                    else:
                        member = new_member(enum_class)
                elif use_args:
                    pass
                else:
                    member = new_member(enum_class)
        else:
            attrs.items()
            for (name, value) in attrs.items():
                if isinstance(value, name_58):
                    if value.value is name_62:
                        value.value = gnv(name, 1, len(member_names), gnv_last_values)
                    value = value.value
                    if use_args:
                        if not isinstance(value, name_66):
                            value = (value)
                        member = [enum_class](**None)
                        value = value[0]
                        member._value_ = value
                        contained = value2member_map.get(member._value_)
                    else:
                        member = new_member(enum_class)
                elif use_args:
                    pass
                else:
                    member = new_member(enum_class)
        cls.__dict__.items()
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
        enum_class._flag_mask_ = single_bits | multi_bits
        enum_class._singles_mask_ = single_bits
        enum_class._all_bits_ = 2 ** single_bits | multi_bits.bit_length() - 1
        m
        enum_class
        if not True:
            pass
        else:
            contained = m
            break
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
        try:
            []
            for (name, alias) in []:
                try:
                    try:
                        []
                        raise ValueError(f"aliases found in {enumeration}: {alias_details}")
                        for check in checks:
                            if check is ValueError:
                                for (member, name) in enumeration.__members__.items():
                                    if not name != member.name:
                                        pass
                                    else:
                                        duplicates.append((name, member.name))
                            elif check is _iter_bits_lsb:
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
                                            if not i not in values:
                                                pass
                                            else:
                                                missing.append(i)
                                    else:
                                        raise Exception('verify: unknown type %r' % enum_type)
                                        if missing:
                                            raise 'invalid '(f"{enum_type} {cls_name}: missing values {', '.join}{<genexpr>(missing())}"[:256])
                            elif not check is name_42:
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
                                            for (alias, name) in enumeration._member_map_.items():
                                                if name in member_names:
                                                    pass
                                                elif alias.value < 0:
                                                    pass
                                                else:
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
                                            elif len(missing_names) == 1:
                                                alias = 'alias %s is missing' % missing_names[0]
                                            else:
                                                alias = f"aliases {', '.join(missing_names[None:-1])} and {missing_names[-1]} are missing"
                                                if _is_single_bit(missing_value):
                                                    value = 'value 0x%x' % missing_value
                                                else:
                                                    value = 'combined values of 0x%x' % missing_value
                                                    raise ValueError(f"invalid Flag {cls_name}: {alias} {value} [use enum.show_flag_values(value) for details]")
                                                    return enumeration
                                            break
                                        except:
                                            break
                                except:
                                    break
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
        elif issubclass(enumeration, items):
            enum_type = 'enum'
        else:
            raise TypeError('the \'verify\' decorator only works with Enum and Flag')
            checks
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
        for key in set(checked_keys + simple_keys):
            if key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__'):
                pass
            elif key in member_names:
                pass
            elif key not in simple_keys:
                failed.append(f"missing key: {key}")
            elif key not in checked_keys:
                failed.append(f"extra key:   {key}")
            else:
                checked_value = checked_dict[key]
                simple_value = simple_dict[key]
    elif failed:
        raise TypeError("""enum mismatch:
   %s""" % """
   """.join(failed))
    failed_member = []
    failed.append('missing member from simple enum: %r' % name)
    failed.append('extra member in simple enum: %r' % name)
    checked_value = checked_member_dict[key]
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
