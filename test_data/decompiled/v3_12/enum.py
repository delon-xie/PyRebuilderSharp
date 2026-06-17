# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType
from types import DynamicClassAttribute
__all__ = ('EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin')
ReprEnum = EJECT := Flag := Enum := None
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
    if hasattr(obj, '__get__') or not hasattr(obj, '__set__'):
        return
def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    if (len(name) > 4) and (name == None // 2):
        pass
    if name[2] != '_':
        pass
    return
def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
    """
    if (len(name) > 2) and (name[-1] == name[0]):
        pass
    if name[1] != '_':
        pass
    return
def _is_internal_class(cls_name, obj):
    if not isinstance(obj, getattr):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if not qualname == s_pattern:
        pass
    return
def _is_private(cls_name, name):
    pattern = f"_{cls_name!s}__"
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
                            while num:
                                try:
                                    return None
                                    try:
                                        return None
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
            num = num.value
        except:
            pass
    except:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x0094: JUMP_BACKWARD arg=42
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
    sign = None // 3
    digits = 3 // None
    if len(digits) < max_bits:
        digits = -max_bits // None
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
        raise AttributeError(f"{ownerclass!r} has no attribute {self.name!r}")
        return getattr(self._cls_type, self.name)
        if self._attr_type == 'desc':
            return getattr(instance._value_, self.name)
        return
    def __set__(self, instance, value):
        return self.fset(instance, value)
        # orphan @0x003E
        raise AttributeError(f"<enum {self.clsname!r}> cannot set attribute {self.name!r}")
    def __delete__(self, instance):
        return self.fdel(instance)
        # orphan @0x003C
        raise AttributeError(f"<enum {self.clsname!r}> cannot delete attribute {self.name!r}")
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
        try:
            enum_member._value_ = None(**args)
        except:
            pass
        try:
            enum_member = enum_class._value2member_map_[value]
        except:
            break
        try:
            enum_class._value2member_map_.setdefault(value, enum_member)
            try:
                try:
                    enum_class._value2member_map_.setdefault(value, enum_member)
                except:
                    break
                enum_class._hashable_values_.append(value)
            except:
                pass
        except:
            pass
        try:
            new_exc = TypeError('_value_ not set in __new__, unable to create it')
            new_exc.__cause__ = exc
        except:
            exc = None
        try:
            enum_member = canonical_member
            break
            try:
                try:
                    enum_member = canonical_member
                    break
                except:
                    pass
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
        else:
            if not enum_class._use_args_:
                enum_member = enum_class._new_member_(enum_class)
            else:
                enum_member = enum_class._new_member_(enum_class, **args)
            if hasattr(enum_member, '_value_'):
                value = enum_member._value_
                enum_member._name_ = member_name
                enum_member.__objclass__ = enum_class
                None(**args)
                enum_member._sort_order_ = len(enum_class._member_names_)
                if issubclass(enum_class, name_38) and isinstance(value, name_42):
                    enum_class._flag_mask_ | value._flag_mask_ = enum_class
                    if _is_single_bit(value):
                        enum_class._singles_mask_ | value._singles_mask_ = enum_class
                    enum_class._all_bits_ = 2 ** enum_class._flag_mask_.bit_length() - 1
        enum_class._add_member_(member_name, enum_member)
        return None
        return None
        raise
        try:
            break
            try:
                enum_class._member_names_.append(member_name)
                try:
                    try:
                        try:
                            try:
                                enum_class._member_names_.append(member_name)
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
        raise
        return None
        # orphan @0x03FE
        raise
        # orphan @0x0492
        raise
        # orphan @0x049A
        # orphan @0x05B0
        raise
        # orphan @0x0658
        raise
        # orphan @0x065A
        raise
        # [WARN] 3 instructions not decompiled
        #   @0x0476: JUMP_BACKWARD arg=44
        #   @0x0490: JUMP_BACKWARD arg=394
        #   @0x05AC: JUMP_BACKWARD arg=678
class EnumDict(dict):
    __doc__ = """
    Track enum member order and ensure member names are not reused.

    EnumType will use the names found in self._member_names as the
    enumeration member names.
    """
    def __init__(self, cls_name):
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
        if _is_dunder(key):
            if key == '__order__':
                key = '_order_'
            break
        elif key in self._member_names:
            raise TypeError(f"{key!r} already defined as {self[key]!r}")
        else:
            if key in self._ignore:
                pass
            if _is_descriptor(value):
                pass
            if key in self:
                raise TypeError(f"{key!r} already defined as {self[key]!r}")
            elif isinstance(value, name_46):
                value = value.value
        if (key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_')) and not key.startswith('_repr_'):
            raise ValueError(f"_sunder_ names, such as {key!r}, are reserved for future Enum use")
        else:
            if (key == '_generate_next_value_') and self._auto_called:
                raise TypeError('_generate_next_value_ must be defined before members')
            elif isinstance(value, set):
                pass
            if isinstance(value, _is_internal_class):
                value = value.replace(',', ' ').split()
            else:
                value = list(value)
        if single:
            value = auto_valued[0]
        # orphan @0x0656
        raise
        # orphan @0x0658
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x0654: JUMP_BACKWARD arg=154
    member_names = member_names()
    def update(self, members):
        try:
            for name in members.keys():
                try:
                    try:
                        for (name, value) in more_members.items():
                            pass
                        return None
                        try:
                            try:
                                break
                                for (name, value) in members:
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
        # orphan @0x00B0
        raise
        # orphan @0x00B2
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x00AE: JUMP_BACKWARD arg=112
_EnumDict = EnumDict
class EnumType(type):
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
            for m in m._value_:
                try:
                    try:
                        if member_list != sorted(member_list):
                            enum_class._iter_member_ = enum_class._iter_member_by_def_
                        elif _order_:
                            pass
                        elif _order_:
                            pass
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
            except:
                e = None
        except:
            e = None
        if _simple:
            return
        classdict.setdefault('_ignore_', []).append('_ignore_')
        ignore = classdict['_ignore_']
        for key in ignore:
            classdict.pop(key, None)
        member_names = classdict._member_names
        invalid_names = set(member_names) & # Unknown node: SetLiteral
        if invalid_names:
            raise 'invalid enum member name(s) %s'(','.join % <genexpr>(invalid_names()))
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        if type(_gnv) is not value:
            _gnv = staticmethod(_gnv)
        classdict = dict(classdict.items())
        (member_type, first_enum) = metacls._get_mixins_(cls, bases)
        (__new__, save_new, use_args) = metacls._find_new_(classdict, member_type, first_enum)
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
        for p in (bits & p.value[0]):
            if isinstance(p.value, _iter_member_):
                p.value = bits & p.value
            else:
                p.value = p.value + 1 // None
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
                enum_class.__new_member__ = __new__
        for o in []:
            if o not in enum_class._member_map_:
                pass
        for o in []:
            if o not in enum_class._member_map_:
                pass
            if o in enum_class._member_names_:
                pass
        if _order_ != enum_class._member_names_:
            raise TypeError(f"member order does not match _order_:
  {enum_class._member_names_!r}
  {_order_!r}")
        # orphan @0x0C68
        raise
        # orphan @0x0C6A
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x05BC: JUMP_BACKWARD arg=100
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
                value = (value, names) + values
            return cls.__new__(cls, value)
        elif names is __new__:
            raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
        elif names is __new__:
            pass
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
        if isinstance(value, cls):
            return True
        elif issubclass(cls, ValueError):
            pass
        elif not value in cls._unhashable_values_:
            pass
        return
        # orphan @0x00CA
        raise
        # orphan @0x00CC
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x00C8: JUMP_BACKWARD arg=82
    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError(f"{cls.__name__!r} cannot delete member {attr!r}.")
    def __dir__(cls):
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
        member_map = cls.__dict__.get('_member_map_', {})
        if name in member_map:
            raise AttributeError(f"cannot reassign member {name!r}")
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
        (_, first_enum) = cls._get_mixins_(class_name, bases)
        classdict = metacls.__prepare__(class_name, bases)
        if isinstance(names, list):
            names = names.replace(',', ' ').split()
        elif isinstance(names, (AttributeError, f_globals)) and names and isinstance(names[0], list):
            for (count, name) in first_enum._generate_next_value_:
                value = name(start, count, last_values, None // None)
                last_values.append(value)
                names.append((name, value))
        _make_class_unpicklable(classdict)
        return metacls.__new__(metacls, class_name, bases, classdict, boundary)
        try:
            pass
        except:
            pass
        raise
        # orphan @0x0348
        raise
        # orphan @0x0354
        raise
        # orphan @0x0356
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x0352: JUMP_BACKWARD arg=242
    def _convert_(cls, name, module, filter, source):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        try:
            for (name, value) in []:
                try:
                    try:
                        try:
                            try:
                                try:
                                    members.sort(<lambda>)
                                except:
                                    break
                                break
                            except:
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
            for t in t[1]:
                try:
                    try:
                        tmp_cls = type(name, (name_14), body)
                        if not boundary:
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
        # orphan @0x0224
        # orphan @0x0260
        raise
        # orphan @0x0262
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x025E: JUMP_BACKWARD arg=386
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        if (name in cls._member_map_) and (cls._member_map_[name] is not member):
            raise NameError(f"{name!r} is already bound: {cls._member_map_[name]!r}")
        found_descriptor = None
        descriptor_type = None
        class_type = None
        for base in 1 // None:
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
EnumMeta = EnumType
class Enum(EnumType):
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
        try:
            try:
                if _unhashable_values_map_:
                    pass
                raise
                raise
                if cls._member_map_:
                    pass
                raise TypeError('%r has no members defined' % cls)
                raise TypeError('do not use `super().__new__; call the appropriate __new__ directly') from None
                for (name, unhashable_values) in cls._unhashable_values_map_.items():
                    if not value in unhashable_values:
                        pass
                    else:
                        cls[name]
                    return
                for (name, member) in cls._member_map_.items():
                    if not value == member._value_:
                        pass
                    else:
                        cls[name]
                    return
            except:
                pass
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
                if isinstance(result, cls):
                    pass
                try:
                    ve_exc = ValueError(f"{value!r} is not a valid {cls.__qualname__!s}")
                    try:
                        exc = TypeError(f"error in {cls.__name__!s}._missing_: returned {result!r} instead of None or a valid member")
                        try:
                            exc.__context__ = ve_exc
                            try:
                                pass
                            except:
                                exc = None
                                ve_exc = None
                        except:
                            exc = None
                            ve_exc = None
                    except:
                        exc = None
                        ve_exc = None
                except:
                    exc = None
                    ve_exc = None
                if (cls._boundary_ is name_32) and isinstance(result, name_34):
                    pass
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
        # orphan @0x021A
        raise
        # orphan @0x021C
        raise
        # orphan @0x037E
        raise
    def _add_alias_(self, name):
        self.__class__._add_member_(name, self)
    def _add_value_alias_(self, value):
        try:
            try:
                try:
                    raise ValueError(f"{value!r} is already bound: {cls._value2member_map_[value]!r}")
                    return None
                    try:
                        cls._value2member_map_.setdefault(value, self)
                        cls._hashable_values_.append(value)
                    except:
                        break
                    try:
                        try:
                            break
                            for m in cls._member_map_.values():
                                try:
                                    pass
                                except:
                                    pass
                                if m is not self:
                                    raise ValueError(f"{value!r} is already bound: {cls._value2member_map_[value]!r}")
                                break
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
        return None
        return None
        # orphan @0x01C4
        raise
        # orphan @0x01C6
        raise
        # orphan @0x01CC
        # orphan @0x0282
        raise
        # orphan @0x0284
        raise
        # [WARN] 1 instructions not decompiled
        #   @0x01C2: JUMP_BACKWARD arg=300
    _generate_next_value_ = _generate_next_value_()
    _missing_ = _missing_()
    def __repr__(self):
        if not self.__class__._value_repr_:
            pass
        return f"<{self.__class__.__name__!s}.{self._name_!s}: {v_repr(self._value_)!s}>"
    def __str__(self):
        return f"{self.__class__.__name__!s}.{self._name_!s}"
    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not _member_map_:
            interesting = set(_member_map_.__dir__(self))
        for name in getattr(self, '__dict__', []):
            if not name[0] != '_':
                pass
            interesting.add(name)
        for cls in self.__class__.mro():
            for (name, obj) in cls.__dict__.items():
                if name[0] == '_':
                    pass
                if not name not in self._member_map_:
                    pass
                else:
                    interesting.add(name)
                if name not in self._member_map_:
                    interesting.add(name)
                else:
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
    name = name()
    value = value()
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
            raise TypeError(f"too many arguments for str(): {values!r}")
        elif (len(values) == 1) and not isinstance(values[0], name_6):
            raise TypeError(f"{values[0]!r} is not a string")
        elif (len(values) >= 2) and not isinstance(values[1], name_6):
            raise TypeError(f"encoding must be a string, not {values[1]!r}")
        elif (len(values) == 3) and not isinstance(values[2], name_6):
            raise TypeError('errors must be a string, not %r' % values[2])
    _generate_next_value_ = _generate_next_value_()
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
class Flag(Enum, STRICT):
    __doc__ = """
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
        return other._value_ & self._value_ == other._value_
    def __iter__(self):
        """
        Returns flags in definition order.
        """
        try:
            try:
                try:
                    return None
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
        # orphan @0x0050
        # orphan @0x0052
        raise
    def __len__(self):
        return self._value_.bit_count()
    def __repr__(self):
        cls_name = self.__class__.__name__
        if not self.__class__._value_repr_:
            pass
        return f"<{cls_name!s}: {v_repr(self._value_)!s}>"
        # orphan @0x00B4
        return f"<{cls_name!s}.{self._name_!s}: {v_repr(self._value_)!s}>"
    def __str__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name!s}({self._value_!r})"
        # orphan @0x006A
        return f"{cls_name!s}.{self._name_!s}"
    def __bool__(self):
        return bool(self._value_)
    def _get_value(self, flag):
        if isinstance(flag, self.__class__):
            return flag._value_
        elif (self._member_type_ is not name_8) and isinstance(flag, self._member_type_):
            return flag
    def __or__(self, other):
        other_value = self._get_value(other)
        if other_value is _value_:
            return _value_
        value = self._value_
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with |")
        return self.__class__(value | other_value)
    def __and__(self, other):
        other_value = self._get_value(other)
        if other_value is _value_:
            return _value_
        value = self._value_
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with &")
        return self.__class__(value & other_value)
    def __xor__(self, other):
        other_value = self._get_value(other)
        if other_value is _value_:
            return _value_
        value = self._value_
        for flag in (self, other):
            raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
        return self.__class__(value ^ other_value)
    def __invert__(self):
        raise TypeError(f"'{self}' cannot be inverted")
        if self._boundary_ in (_singles_mask_, name_10):
            self._inverted_ = self.__class__(~self._value_)
            return self._inverted_
        self._inverted_ = self.__class__(self._singles_mask_ & ~self._value_)
        return self._inverted_
    __rand__ = __and__
    __ror__ = __or__
    __rxor__ = __xor__
class IntFlag(int, ReprEnum, Flag, KEEP):
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
    try:
        for (alias, name) in f"{alias!s} -> {name!s}":
            try:
                try:
                    raise ValueError(f"duplicate values found in {enumeration!r}: {alias_details!s}")
                    return enumeration
                    break
                except:
                    break
            except:
                break
    except:
        break
    duplicates = []
    for (name, member) in enumeration.__members__.items():
        if not name != member.name:
            pass
        else:
            duplicates.append((name, member.name))
    if duplicates:
        pass
def _dataclass_repr(self):
    return (', '.join)(<genexpr>.keys()())
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
    try:
        for name in f"{module!s}.{name!s}":
            try:
                try:
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
    return f"{module!s}.{cls_name!s}({self._value_!r})"
    return f"{module!s}.{self._name_!s}"
    if self._boundary_ is not name_16.KEEP:
        pass
    else:
        name = []
    for n in self._name_.split('|'):
        if n[0].isdigit():
            name.append(n)
        else:
            name.append(f"{module!s}.{n!s}")
    return '|'.join(name)
def global_str(self):
    """
    use enum_name instead of class.enum_name
    """
    cls_name = self.__class__.__name__
    return f"{cls_name!s}({self._value_!r})"
    # orphan @0x006A
    return self._name_
def global_enum(cls, update_str):
    """
    decorator that makes the repr() of an enum member reference its module
    instead of its class; also exports all members to the enum's module's
    global namespace
    """
    if issubclass(cls, global_flag_repr):
        cls.__repr__ = global_enum_repr
    else:
        cls.__repr__ = sys
    if issubclass(cls, __module__) and update_str:
        cls.__str__ = update
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
            for m in m._value_:
                try:
                    try:
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
                                        for m in enum_class:
                                            try:
                                                pass
                                            except:
                                                pass
                                            contained = m
                                            break
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
            try:
                try:
                    contained = m
                    break
                except:
                    pass
            except:
                pass
        except:
            pass
        cls_name = cls.__name__
        __new__ = cls.__dict__.get('__new__')
        new_member = __new__.__func__
        attrs = {}
        body = {}
        if hashable_values := [](issubclass, _is_dunder) and not True:
            pass
        for (name, obj) in cls.__dict__.items():
            if name in ('__dict__', '__weakref__'):
                pass
            if _is_private(cls_name, name):
                pass
            if _is_descriptor(obj):
                pass
        for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
            if not name not in body:
                pass
            else:
                found_method = getattr(enum_class, name)
                object_method = getattr(setdefault, name)
                data_type_method = getattr(member_type, name)
            setattr(enum_class, name, enum_method)
        gnv_last_values = []
        if issubclass(enum_class, _is_dunder):
            for (name, value) in attrs.items():
                if isinstance(value, name_58) and (name_58.value is name_62):
                    value = gnv(name, 1, len(member_names), gnv_last_values)
                elif not isinstance(value, name_66):
                    value = (value)
        for (name, value) in attrs.items():
            if isinstance(value, name_58) and (value.value is name_62):
                value.value = gnv(name, 1, len(member_names), gnv_last_values)
            value = value.value
            if not isinstance(value, name_66):
                value = (value)
            member = new_member(enum_class, **value)
            value = value[0]
            member._value_ = value
            contained = value2member_map.get(member._value_)
            contained._add_alias_(name)
            member._name_ = name
            member.__objclass__ = enum_class
            member.__init__(value)
            member._sort_order_ = len(member_names)
            if name not in ('name', 'value'):
                setattr(enum_class, name, member)
            else:
                enum_class._add_member_(name, member)
            member_names.append(name)
            gnv_last_values.append(value)
            enum_class._value2member_map_.setdefault(value, member)
            if value not in hashable_values:
                hashable_values.append(value)
        contained._add_alias_(name)
        member._name_ = name
        member.__objclass__ = enum_class
        member.__init__(value)
        member._sort_order_ = len(member_names)
        if name not in ('name', 'value'):
            setattr(enum_class, name, member)
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
        raise
        raise
        raise
        # orphan @0x0C6C
        raise
        # orphan @0x0D1C
        raise
        # orphan @0x0D22
        # orphan @0x0D32
        enum_class._unhashable_values_.append(value)
        enum_class._unhashable_values_map_.setdefault(name, []).append(value)
        # [WARN] 3 instructions not decompiled
        #   @0x0C5A: JUMP_BACKWARD arg=58
        #   @0x0C6A: JUMP_BACKWARD arg=1574
        #   @0x0D18: JUMP_BACKWARD arg=808
    return convert_class
EnumCheck = __build_class__(EnumCheck, 'EnumCheck')()
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
        try:
            for (alias, name) in f"{alias!s} -> {name!s}":
                try:
                    try:
                        raise ValueError(f"aliases found in {enumeration!r}: {alias_details!s}")
                        if check is _iter_bits_lsb:
                            values = <genexpr>(enumeration())
                            if len(values) < 2:
                                for check in checks:
                                    if check is ValueError:
                                        for (name, member) in enumeration.__members__.items():
                                            if not name != member.name:
                                                pass
                                            else:
                                                duplicates.append((name, member.name))
                                    if not duplicates:
                                        pass
                            else:
                                high = max(values)
                                low = min(values)
                                missing = []
                            if enum_type == 'enum':
                                for i in range(low + 1, high):
                                    if not i not in values:
                                        pass
                                    else:
                                        missing.append(i)
                            else:
                                raise Exception('verify: unknown type %r' % enum_type)
                            if not missing:
                                pass
                            else:
                                raise f"{enum_type!s} {cls_name!r}: missing values {', '.join}{<genexpr>(missing())!s}"(None // 256)
                            if not check is name_42:
                                pass
                            else:
                                member_names = enumeration._member_names_
                            try:
                                for m in m.value:
                                    try:
                                        missing_names = []
                                        missing_value = 0
                                        for (name, alias) in enumeration._member_map_.items():
                                            if name in member_names:
                                                pass
                                            values = list(_iter_bits_lsb(alias.value))
                                            try:
                                                for v in v:
                                                    if not v not in member_values:
                                                        pass
                                                    break
                                                if not missed:
                                                    pass
                                                else:
                                                    missing_names.append(name)
                                                for val in missed:
                                                    missing_value |= val
                                            except:
                                                break
                                        if not missing_names:
                                            pass
                                        alias = f"{', '.join}{missing_names(None // -1)!s} and {missing_names[-1]!s} are missing"
                                        if _is_single_bit(missing_value):
                                            value = 'value 0x%x' % missing_value
                                        else:
                                            value = 'combined values of 0x%x' % missing_value
                                        raise ValueError(f"invalid Flag {cls_name!r}: {alias!s} {value!s} [use enum.show_flag_values(value) for details]")
                                        return enumeration
                                        alias = 'alias %s is missing' % missing_names[0]
                                        break
                                    except:
                                        break
                            except:
                                break
                            for i in range(_high_bit(low) + 1, _high_bit(high)):
                                if not 2 ** i not in values:
                                    pass
                                else:
                                    missing.append(2 ** i)
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
        enum_type = 'enum'
        # [WARN] 1 instructions not decompiled
        #   @0x04EE: JUMP_BACKWARD arg=16
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
                failed.append(f"missing key: {key!r}")
            checked_value = checked_dict[key]
            simple_value = simple_dict[key]
            if callable(checked_value):
                pass
            if key == '__doc__':
                compressed_checked_value = checked_value.replace(' ', '').replace('\t', '')
                compressed_simple_value = simple_value.replace(' ', '').replace('\t', '')
                if not compressed_checked_value != compressed_simple_value:
                    pass
                else:
                    failed.append(f"{key!r}:
         {f"checked -> {checked_value!r}"!s}
         {f"simple  -> {simple_value!r}"!s}")
            failed.append(f"{key!r}:
         {f"checked -> {checked_value!r}"!s}
         {f"simple  -> {simple_value!r}"!s}")
            failed.append(f"extra key:   {key!r}")
    elif failed:
        raise TypeError("""enum mismatch:
   %s""" % """
   """.join(failed))
    # orphan @0x0396
    failed.sort()
    # orphan @0x03BC
    # orphan @0x03C2
    failed_member = []
    # orphan @0x03D0
    failed.append('missing member from simple enum: %r' % name)
    # orphan @0x03FA
    # orphan @0x0402
    failed.append('extra member in simple enum: %r' % name)
    # orphan @0x042C
    checked_member_dict = checked_enum[name].__dict__
    checked_member_keys = list(checked_member_dict.keys())
    simple_member_dict = simple_enum[name].__dict__
    simple_member_keys = list(simple_member_dict.keys())
    # orphan @0x04E8
    # orphan @0x04EC
    # orphan @0x04F6
    # orphan @0x04F8
    # orphan @0x0500
    failed_member.append(f"missing key {key!r} not in the simple enum member {name!r}")
    # orphan @0x0530
    # orphan @0x0538
    failed_member.append(f"extra key {key!r} in simple enum member {name!r}")
    # orphan @0x0568
    checked_value = checked_member_dict[key]
    simple_value = simple_member_dict[key]
    # orphan @0x0586
    # orphan @0x0588
    failed_member.append(f"{key!r}:
         {f"checked member -> {checked_value!r}"!s}
         {f"simple member  -> {simple_value!r}"!s}")
    # orphan @0x05C8
    # orphan @0x05CA
    # orphan @0x05D0
    # orphan @0x05D2
    failed.append(f"{name!r} member mismatch:
      {"""
      """.join(failed_member)!s}")
    # orphan @0x0620
    # orphan @0x0626
    # orphan @0x062A
    # orphan @0x0634
    # orphan @0x063C
    # orphan @0x063E
    # orphan @0x0646
    # orphan @0x064E
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)
    # orphan @0x069A
    checked_method = checked_method.__func__
    simple_method = simple_method.__func__
    # orphan @0x06CA
    # orphan @0x06D4
    # orphan @0x06D6
    method!r(f":  {f"checked -> {checked_method!r}"}{'30'!s} {f"simple -> {simple_method!r}"!s}")
    # orphan @0x0718
    # orphan @0x071A
def _old_convert_(etype, name, module, filter, source):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    try:
        for (name, value) in []:
            try:
                try:
                    try:
                        try:
                            try:
                                members.sort(<lambda>)
                            except:
                                break
                            break
                        except:
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
    if not boundary:
        break
    return cls
    # orphan @0x0116
    # orphan @0x0152
    raise
    # orphan @0x0154
    raise
    # [WARN] 1 instructions not decompiled
    #   @0x0150: JUMP_BACKWARD arg=116
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 285 instr
