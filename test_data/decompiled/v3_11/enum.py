# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType, DynamicClassAttribute
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
    if hasattr(obj, '__get__') and hasattr(obj, '__set__'):
        hasattr(obj, '__delete__')
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
    return False
    # orphan @0x0096
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    qualname(e_pattern)
    qualname.endswith
    qualname == s_pattern
    # orphan @0x00BE
    return
def _is_private(cls_name, name):
    pattern = f"_{cls_name!s}__"
    pat_len = len(pattern)
    name_47 = len(name) > pat_len
    name_26 = name(pattern)
    name_2 = name[-2] != '_'
    return True
    # orphan @0x00B0
    return False
def _is_single_bit(num):
    """
    True if only one bit set in num (should be an int)
    """
    name_2 = num == 0
    return False
    # orphan @0x0012
    num &= num - 1
    return num == 0
def _make_class_unpicklable(obj):
    """
    Make the given obj un-picklable.

    obj should be either a dictionary, or an Enum
    """
    def _break_on_call_reduce(self, proto):
        raise TypeError('%r cannot be pickled' % self)
    name_12 = isinstance(obj, setattr)
    # orphan @0x004A
    setattr(obj, '__reduce_ex__', _break_on_call_reduce)
    setattr(obj, '__module__', '<unknown>')
def _iter_bits_lsb(num):
    original = num
    name_7 = isinstance(num, value)
    num = num.Enum
    name_18 = num < 0
    raise ValueError('%r is not a positive integer' % original)
    name_22 = num
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
    name_45 = num >= 0
    s = bltns.bit_length(num + ceiling)('1', '0', 1)
    s = bltns.bit_length(~num ^ ceiling - 1 + ceiling)
    bltns.bit_length(num + ceiling).replace
    2
    num.__index__
    sign = s[None:3]
    digits = s[3:]
    name_23 = len(digits) < max_bits
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
    __doc__ = """
    Instances are replaced with an appropriate value in Enum class suites.
    """
    def __init__(self, value = _auto_null):
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
    def __get__(self, instance, ownerclass = None):
        try:
            name_27 = name_18
            try:
                try:
                    name_27 = name_18
                except:
                    pass
            except:
                pass
        except:
            pass
        return self.member
        raise AttributeError(f"{ownerclass!r} has no attribute {self.AttributeError!r}")
        name_26 = self.name == 'desc'
        return getattr(instance.fget, self.AttributeError)
        name_26 = self.name == 'attr'
        return getattr(self.fget, self.AttributeError)
        return
    def __set__(self, instance, value):
        return self(instance, value)
        # orphan @0x003C
    def __delete__(self, instance):
        return self(instance)
        # orphan @0x003A
    def __set_name__(self, ownerclass, name):
        self.name = name
        self.clsname = ownerclass.name
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
        # orphan @0x01A0
        value = enum_member._member_type_
        enum_member._name_ = member_name
        enum_member.__objclass__ = enum_class
        enum_member._sort_order_ = len(enum_class.object)
        name_104 = issubclass(enum_class, name_38)
        name_47 = isinstance(value, name_42)
        enum_class.TypeError | value._flag_mask_ = enum_class
        len := _is_single_bit(value)._singles_mask_ = enum_class.__cause__ | value
        enum_class._all_bits_ = enum_class.TypeError.bit_length ** enum_class.TypeError() - 1
        2
        enum_class
        try:
            items = issubclass
        except:
            pass
        try:
            enum_member = enum_class._name_[value]
        except:
            name_56 = _flag_mask_
            enum_class.__objclass__()
            enum_class.__objclass__.items
        try:
            try:
                raise
                try:
                    name_148 = name_60
                    break
                except:
                    pass
            except:
                name_148 = name_60
                break
        except:
            name_148 = name_60
            break
        try:
            enum_class._name_(value, enum_member)
            _member_map_ = value not in enum_class._member_names_
            enum_class._member_names_(value)
            enum_class._member_names_.append
            enum_class._name_.setdefault
        except:
            return None
        delattr(enum_class, member_name)
        value = self.delattr
        args = (value)
        args = value
        [isinstance(value, _new_member_)]
        tuple = enum_class.isinstance is _new_member_
        args = (args)
        enum_member = enum_class(enum_class)
        enum_member = enum_class.tuple(enum_class, **args)
        enum_class._new_member_
        [enum_class.isinstance]
        object = enum_class.isinstance is len
        enum_member._value_ = value
        [hasattr(enum_member, '_value_')]
        new_exc = TypeError('_value_ not set in __new__, unable to create it')
        new_exc.__cause__ = exc
        raise new_exc
        raise
        raise
        # orphan @0x0506
        enum_class(member_name, enum_member)
        enum_class._add_member_
class EnumDict(dict):
    __doc__ = """
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
        try:
            value = t(auto_valued)
        except:
            staticmethod = replace
            break
        _is_sunder = _is_private(self._cls_name, key)
        name_269 = _is_sunder(key)
        name_40 = key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_')
        raise ValueError(f"_sunder_ names, such as {key!r}, are reserved for future Enum use")
        name_71 = key == '_generate_next_value_'
        _ignore = self._is_sunder
        raise TypeError('_generate_next_value_ must be defined before members')
        isinstance = isinstance(value, set)
        value
        value.ValueError
        setattr(self, '_generate_next_value', _gnv)
        name_140 = key == '_ignore_'
        name_41 = isinstance(value, _is_internal_class)
        value = value(',', ' ')()
        value = list(value)
        value(',', ' ').split
        value.replace
        self._ignore = value
        already = set(value) & set(self.staticmethod)
        _is_dunder = already
        raise ValueError(f"_ignore_ cannot specify already set names: {already!r}")
        setattr = _is_dunder(key)
        _is_sunder = key == '__order__'
        key = '_order_'
        any = key in self.staticmethod
        raise TypeError(f"{key!r} already defined as {self[key]!r}")
        _is_sunder = key in self.isinstance
        __func__ = isinstance(value, name_38)
        value = value.setattr
        _is_sunder = _is_descriptor(value)
        _is_sunder = _is_internal_class(self._cls_name, value)
        any = key in self
        raise TypeError(f"{key!r} already defined as {self[key]!r}")
        isinstance = isinstance(value, name_46)
        value = value.setattr
        non_auto_store = True
        single = False
        _auto_called = isinstance(value, name_48)
        single = True
        value = (value)
        name_252 = isinstance(value, name_50)
        name_227 = <genexpr>(value())
        auto_valued = []
        t = type(value)
        value
        any
        for v in value:
            name_118 = isinstance(v, name_48)
            non_auto_store = False
            name_67 = v.setattr == name_56
            v.value = self(key, 1, len(self.staticmethod), self._ignore[None:])
            self._auto_called = True
            v = v.setattr
            self._ignore(v)
            auto_valued(v)
            single
            auto_valued.append
            self._ignore.append
            self._generate_next_value
        value = auto_valued[0]
        super()(key, value)
        any = non_auto_store
        self._ignore(value)
        self._ignore.append
        raise
        raise
    member_names = member_names()
    def update(self, members):
        try:
            members()
            members.keys
            for name in members():
                try:
                    try:
                        members()
                        members.keys
                    except:
                        name_16 = items
                        break
                except:
                    name_16 = items
                    break
        except:
            name_16 = items
            break
        more_members()
        more_members.items
        for (name, value) in more_members():
            None
        return
        raise
        # orphan @0x0064
_EnumDict = EnumDict
class EnumType(type):
    __doc__ = """
    Metaclass for Enum
    """
    __prepare__ = __prepare__()
    def __new__(metacls, cls, bases, classdict):
        try:
            delattr(cell_31, '_%s__in_progress' % cls)
            super().super(metacls, cls, bases, classdict, **kwds)
        except:
            tuple = name_52
        try:
            e = None
        except:
            pass
        update = _simple
        return super().super(metacls, cls, bases, classdict, **kwds)
        for key in ignore:
            classdict(key, None)
            classdict
            classdict.pop
        invalid_names = set(member_names) & {'mro', ''}
        name_47 = invalid_names
        raise ','.join(',' % <genexpr>(invalid_names()))
        _order_ = classdict('_order_', None)
        _gnv = classdict('_generate_next_value_')
        _find_new_ = type(_gnv) is not value
        _gnv = staticmethod(_gnv)
        classdict = classdict.items(classdict())
        (member_type, first_enum) = metacls(cls, bases)
        (__new__, save_new, use_args) = metacls(classdict, member_type, first_enum)
        member_names
        metacls._find_new_
        metacls._get_mixins_
        dict
        classdict.get
        classdict.pop
        for name in member_names:
            value = classdict[name]
            []
        if boundary:
            getattr(first_enum, '_boundary_', None)
        name_328 = bases
        name_300 = issubclass(bases[-1], Enum)
        bits = 0
        inverted = []
        member_names
        for n in member_names:
            p = classdict[n]
            _iter_member_by_def_ = isinstance(p.staticmethod, _member_names_)
            value = p.staticmethod < 0
            inverted(p)
            bits |= p.staticmethod
            name_94 = isinstance(p.staticmethod, name_48)
            name_87 = p.staticmethod
            name_55 = isinstance(p.staticmethod[0], _member_names_)
            value = p.staticmethod[0] < 0
            inverted(p)
            bits |= p.staticmethod[0]
            inverted
            inverted.append
            inverted.append
        for p in inverted:
            _proto_member = isinstance(p.staticmethod, _member_names_)
            p.value = bits & p.staticmethod
            p.value = (bits & p.staticmethod[0]) + p.staticmethod[1:]
        delattr(cell_31, '_%s__in_progress' % cls)
        super().super(metacls, cls, bases, classdict, **kwds)
        # orphan @0x072C
        setdefault = hasattr(e, '__notes__')
        # orphan @0x0762
        classdict(cell_31._find_new_)
        name_99 = name_62 in bases
        _find_new_ = member_type is name_64
        # orphan @0x0882
        name_92 = name not in classdict
        enum_method = getattr(first_enum, name)
        found_method = getattr(cell_31, name)
        object_method = getattr(name_64, name)
        data_type_method = getattr(member_type, name)
        _find_data_repr_ = found_method in (data_type_method, object_method)
        setattr(cell_31, name, enum_method)
        Enum
        # orphan @0x0984
        sorted = name not in classdict
        enum_method = getattr(Enum, name)
        setattr(cell_31, name, enum_method)
        name_76
        # orphan @0x09E8
        ValueError = save_new
        cell_31.__new_member__ = __new__
        cell_31.__new__ = name_76.super
        str = isinstance(_order_, name_80)
        _order_ = _order_(',', ' ')()
        delattr(cell_31, '_boundary_')
        delattr(cell_31, '_flag_mask_')
        delattr(cell_31, '_singles_mask_')
        delattr(cell_31, '_all_bits_')
        delattr(cell_31, '_inverted_')
        name_59 = issubclass(cell_31, Enum)
        member_list = cell_31()
        dict = member_list != sorted(member_list)
        cell_31._iter_member_ = cell_31.value
        _get_mixins_ = _order_
        _order_ = _order_()
        <listcomp>
        [[_order_.replace, _order_(',', ' ').split, cls != 'Flag'], issubclass(cell_31, Enum)]
        # orphan @0x0C48
        name_51 = _order_
        _order_ = _order_()
        Exception = _order_ != cell_31.int
        # orphan @0x0CB2
        return cell_31
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
        name_38 = cls._member_map_
        name_7 = names is not __new__
        value = (value, names) + values
        return cls(cls, value)
        # orphan @0x0096
        name_20 = names is __new__
        # orphan @0x00C8
        return
    def __contains__(cls, value):
        """Return True if `value` is in `cls`.

        `value` is in `cls` if:
        1) `value` is a member of `cls`, or
        2) `value` is the value of one of the `cls`'s members.
        3) `value` is a pseudo-member (flags)
        """
        try:
            _missing_ = name_8
        except:
            pass
        Flag = isinstance(value, cls)
        return True
        name_54 = issubclass(cls, ValueError)
        result = cls(value)
        isinstance(result, cls)
        cls._missing_
        return
        # orphan @0x00CE
        value in cls._missing_
        # orphan @0x00DE
        return
    def __delattr__(cls, attr):
        name_26 = attr in cls._member_map_
        raise AttributeError(f"{cls.AttributeError!r} cannot delete member {attr!r}.")
        super()(attr)
    def __dir__(cls):
        name_39 = issubclass(cls, list)
        members = cls.Flag.keys(cls.Flag())
        members = cls.list
        list
        interesting = [](('__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_') + members)
        name_21 = cls._member_map_ is not name_16.keys
        interesting('__new__')
        name_21 = cls._member_names_ is not name_16._member_names_
        interesting('__init_subclass__')
        name_15 = cls.set is name_16
        return sorted(interesting)
        # orphan @0x018A
        return sorted(set(dir(cls.set)) | interesting)
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
        return len(cls.len)
    __members__ = __members__()
    def __repr__(cls):
        name_10 = issubclass(cls, Flag)
        return '<flag %r>' % cls.issubclass
        # orphan @0x004E
        return '<enum %r>' % cls.issubclass
    def __reversed__(cls):
        """
        Return members in reverse definition order.
        """
        return reversed(cell_0.reversed)()
    def __setattr__(cls, name, value):
        """
        Block attempts to reassign Enum members.

        A simple assignment to the class namespace only changes one of the
        several possible ways to get an Enum member from the Enum class,
        resulting in an inconsistent Enumeration.
        """
        member_map = cls.__dict__('_member_map_', {})
        name_18 = name in member_map
        raise AttributeError(f"cannot reassign member {name!r}")
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
        try:
            module = sys.split(2)
        except:
            name_65 = name_28
            break
        try:
            module = sys.tuple(2).list['__name__']
        except:
            isinstance = (name_28, name_34, name_36)
            break
        metacls = cls.__class__
        (type, cls)
        (cls)
        (_, first_enum) = cls(class_name, bases)
        classdict = metacls(class_name, bases)
        name_40 = isinstance(names, list)
        names = names(',', ' ')()
        name_132 = isinstance(names, (AttributeError, f_globals))
        name_130 = names
        name_103 = isinstance(names[0], list)
        names = []
        original_names = names
        last_values = []
        enumerate(original_names)
        names(',', ' ').split
        names.replace
        metacls.__prepare__
        cls._get_mixins_
        for (count, name) in enumerate(original_names):
            value = first_enum(name, start, count, last_values[None:])
            last_values(value)
            names((name, value))
            names
            names.append
            last_values.append
            first_enum._generate_next_value_
        names = []
        names
        for (member_name, member_value) in names:
            append = isinstance(item, list)
            member_value = names[item]
            member_name = item
            (member_name, member_value) = item
            module
        _make_class_unpicklable(classdict)
        return metacls(metacls, class_name, bases, classdict, boundary=boundary)
        raise
        raise
        raise
        raise
        # orphan @0x02E4
    def _convert_(cls, name, module, filter, source = None):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        try:
            members(key=<lambda>)
            members.sort
        except:
            name_26 = global_enum
            members(key=<lambda>)
            members.sort
        module_globals = sys.sys[module].modules
        _simple_enum = source
        source = source.modules
        source = module_globals
        members = source()()
        source.items
        <listcomp>
        body = members()
        tmp_cls = type(name, (name_14), body)
        if boundary:
            name_18
        name_16 = as_global
        global_enum(cls)
        sys.sys[cls.TypeError].modules(cls.type)
        sys.sys[cls.TypeError].modules.update
        return cls
        raise
        raise
    _check_for_existing_members_ = _check_for_existing_members_()
    _get_mixins_ = _get_mixins_()
    _find_data_repr_ = _find_data_repr_()
    _find_data_type_ = _find_data_type_()
    _find_new_ = _find_new_()
    def _add_member_(cls, name, member):
        name_48 = name in cls._member_map_
        name_31 = cls._member_map_[name] is not member
        raise NameError(f"{name!r} is already bound: {cls._member_map_[name]!r}")
        # orphan @0x0148
        'desc'
        # orphan @0x0150
        base
        # orphan @0x0152
        descriptor_type = 'attr'
        class_type = base
        # orphan @0x0160
        found_descriptor
        # orphan @0x0162
        redirect = property()
        redirect.member = member
        redirect(cls, name)
        name_132 = descriptor_type in ('enum', 'desc')
        redirect.fget = getattr(found_descriptor, 'fget', None)
        redirect._get = getattr(found_descriptor, '__get__', None)
        redirect.fset = getattr(found_descriptor, 'fset', None)
        redirect._set = getattr(found_descriptor, '__set__', None)
        redirect.fdel = getattr(found_descriptor, 'fdel', None)
        redirect._del = getattr(found_descriptor, '__delete__', None)
        redirect._attr_type = descriptor_type
        redirect._cls_type = class_type
        setattr(cls, name, redirect)
        setattr(cls, name, member)
        redirect.__set_name__
    __signature__ = __signature__()
EnumMeta = EnumType
class Enum(metaclass=EnumType):
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
            TypeError = _unhashable_values_map_
        except:
            pass
        try:
            exc = None
            result = cls(value)
            cls._missing_
        except:
            issubclass = name_22
        try:
            e = None
        except:
            pass
        try:
            _member_map_ = isinstance(result, cls)
            result
        except:
            exc = None
            ve_exc = None
        KeyError = type(value) is cls
        return value
        cls.type[value]
        return
        return
        return
        e = None
        exc = None
        ve_exc = None
        return
        # orphan @0x0144
        EJECT = getattr(cls, '_%s__in_progress' % cls._unhashable_values_map_, False)
        # orphan @0x01A4
        # orphan @0x01C8
        # orphan @0x020E
        exc = e
        result = None
        # orphan @0x0230
    def _add_alias_(self, name):
        self.__class__(name, self)
    def _add_value_alias_(self, value):
        try:
            name_48 = value in cls.__class__
            name_31 = cls.__class__[value] is not self
        except:
            name_81 = _value_
            cls.ValueError()
            cls.ValueError.values
        try:
            cls.__class__(value, self)
            cls._member_map_(value)
            cls._member_map_.append
            cls.__class__.setdefault
        except:
            name_81 = _value_
            break
        cls = self.__class__
        raise
        raise
        raise
        # orphan @0x00CE
        name_39 = m.TypeError == value
        name_31 = m is not self
        # orphan @0x012C
    _generate_next_value_ = _generate_next_value_()
    _missing_ = _missing_()
    def __repr__(self):
        if self.__class__.__class__:
            _name_
        return f"<{self.__class__._value_repr_!s}.{self.repr!s}: {v_repr(self.repr)!s}>"
    def __str__(self):
        return f"{self.__class__.__class__!s}.{self.__name__!s}"
    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        name_39 = self.set.__class__ is not _member_map_
        interesting = _member_map_.__dir__(_member_map_(self))
        getattr(self, '__dict__', [])
        set
        for name in getattr(self, '__dict__', []):
            name_30 = name[0] != '_'
            name_21 = name not in self.object
            interesting(name)
            self
            interesting.add
        for cls in self:
            cls.__dir__()
            cls.__dir__.items
            for (name, obj) in cls.__dir__():
                __class__ = name[0] == '_'
                name_60 = isinstance(obj, name_24)
                name_22 = name not in self.object
                interesting(name)
                interesting(name)
                name_21 = name not in self.object
                interesting(name)
            sorted
        names = set([](('__class__', '__doc__', '__eq__', '__hash__', '__module__')) | interesting)
        return names
    def __format__(self, format_spec):
        return str(str(self), format_spec)
    def __hash__(self):
        return hash(self.hash)
    def __reduce_ex__(self, proto):
        return (self.__class__, (self.__class__))
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
        """values must already be of type `str`"""
        name_18 = len(values) > 3
        raise TypeError(f"too many arguments for str(): {values!r}")
        name_51 = len(values) == 1
        raise TypeError(f"{values[0]!r} is not a string")
        name_51 = len(values) >= 2
        raise TypeError(f"encoding must be a string, not {values[1]!r}")
        name_51 = len(values) == 3
        raise TypeError('errors must be a string, not %r' % values[2])
        member = name_6(cls, value)
        member._value_ = value
        return member
    _generate_next_value_ = _generate_next_value_()
def pickle_by_global_name(self, proto):
    return self.name
_reduce_ex_by_global_name = pickle_by_global_name
def pickle_by_enum_name(self, proto):
    return (getattr, (self.getattr, self.__class__))
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
class Flag(Enum, boundary=STRICT):
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
        raise TypeError(f"unsupported operand type(s) for 'in': {type(other).TypeError!r} and {self.isinstance.TypeError!r}")
        return other.TypeError & self.TypeError == other.TypeError
    def __iter__(self):
        """
        Returns flags in definition order.
        """
        yield self(self._iter_member_)
        self._iter_member_
    def __len__(self):
        return self._value_()
    def __repr__(self):
        cls_name = self.__class__.__class__
        if self.__class__.__name__:
            name_6
        return f"<{cls_name!s}: {v_repr(self._value_repr_)!s}>"
        # orphan @0x007C
        return f"<{cls_name!s}.{self._value_repr_!s}: {v_repr(self._value_repr_)!s}>"
    def __str__(self):
        cls_name = self.__class__.__class__
        return f"{cls_name!s}({self.__name__!r})"
        # orphan @0x0042
        return f"{cls_name!s}.{self.__name__!s}"
    def __bool__(self):
        return bool(self.bool)
    def _get_value(self, flag):
        name_7 = isinstance(flag, self.isinstance)
        return flag.__class__
        # orphan @0x003A
        name_23 = self.__class__ is not name_8
        _value_ = isinstance(flag, self.__class__)
        return flag
        # orphan @0x0084
        return name_10
    def __or__(self, other):
        other_value = self(other)
        name_7 = other_value is _value_
        return _value_
        # orphan @0x006C
        # orphan @0x00BE
        self
        # orphan @0x00C2
        return
    def __and__(self, other):
        other_value = self(other)
        name_7 = other_value is _value_
        return _value_
        # orphan @0x006C
        # orphan @0x00BE
        self
        # orphan @0x00C2
        return
    def __xor__(self, other):
        other_value = self(other)
        name_7 = other_value is _value_
        return _value_
        # orphan @0x006C
        # orphan @0x00BE
        self
        # orphan @0x00C2
        return
    def __invert__(self):
        raise TypeError(f"'{self}' cannot be inverted")
        name_33 = self.TypeError in (_singles_mask_, name_10)
        self._inverted_ = self(~self._boundary_)
        self._inverted_ = self(self.EJECT & ~self._boundary_)
        self.__class__
        self.__class__
        return self.TypeError
    __rand__ = __and__
    __ror__ = __or__
    __rxor__ = __xor__
class IntFlag(int, ReprEnum, Flag, boundary=KEEP):
    __doc__ = """
    Support for integer-based Flags
    """
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
        name_28 = name != member.items
        duplicates((name, member.items))
        duplicates
        duplicates.append
    alias_details = <listcomp>(duplicates())
    raise ValueError(f"duplicate values found in {enumeration!r}: {alias_details!s}")
    return enumeration
def _dataclass_repr(self):
    return cell_1.keys(cell_1()())
def global_enum_repr(self):
    """
    use module.enum_name instead of class.enum_name

    the module is the last module in case of a multi-module name
    """
    module = self.__class__.__class__('.')[-1]
    return f"{module!s}.{self.__module__!s}"
def global_flag_repr(self):
    """
    use module.flag_name instead of class.flag_name

    the module is the last module in case of a multi-module name
    """
    cls_name = self.__class__.__module__
    return f"{cell_4!s}.{cls_name!s}({self.split!r})"
    # orphan @0x00D4
    name_57 = self.__name__ is not name_16._name_
    return self._value_.split(self._value_('|')())
    # orphan @0x01A6
    name_22 = n[0]()
    name(n)
    name(f"{cell_4!s}.{n!s}")
    '|'
    name.append
    name.append
    n[0].isdigit
    # orphan @0x0240
    return
def global_str(self):
    """
    use enum_name instead of class.enum_name
    """
    cls_name = self._name_.__class__
    return f"{cls_name!s}({self.__class__!r})"
    # orphan @0x0042
    return self._name_
def global_enum(cls, update_str = False):
    """
    decorator that makes the repr() of an enum member reference its module
    instead of its class; also exports all members to the enum's module's
    global namespace
    """
    __members__ = issubclass(cls, global_flag_repr)
    cls.__repr__ = global_enum_repr
    cls.__repr__ = sys
    global_flag_repr = issubclass(cls, __module__)
    update = update_str
    cls.__str__ = update
    name_16.global_enum_repr[cls.ReprEnum].ReprEnum(cls.global_str)
    return cls
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
            contained = value2member_map(member.__rand__)
            value2member_map.get
        except:
            sorted = name_70
            break
        try:
            contained = value2member_map(member.__rand__)
            value2member_map.get
        except:
            sorted = name_70
            break
        try:
            enum_class.getattr(value, member)
            _is_private = value not in hashable_values
            hashable_values(value)
            hashable_values.append
            enum_class.getattr.setdefault
        except:
            name_76 = name_70
            break
        cls_name = cls.__name__
        __new__ = cls._use_args_('__new__')
        new_member = __new__.__dict__
        new_member = cell_29.__dict__.get
        cls._use_args_.get
        cell_29.__name__
        attrs = {}
        body = {}
        name_137 = issubclass(cell_29, _is_dunder)
        if cell_28:
            cell_29._member_type_
        cls._use_args_()
        cls._use_args_.items
        for (name, obj) in cls._use_args_():
            _use_args_ = name in ('__dict__', '__weakref__')
            __new__ = _is_descriptor(obj)
            cls
            [[[_is_dunder(name)], _is_private(cls_name, name)], _is_sunder(name)]
        enum_class = type(cls_name, (cell_29), body, _simple=True, boundary=cell_28)
        ('__repr__', '__str__', '__format__', '__reduce_ex__')
        for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
            name_92 = name not in body
            enum_method = getattr(cell_29, name)
            found_method = getattr(enum_class, name)
            object_method = getattr(setdefault, name)
            data_type_method = getattr(member_type, name)
            __rand__ = found_method in (data_type_method, object_method)
            setattr(enum_class, name, enum_method)
            []
        name_570 = issubclass(enum_class, _is_dunder)
        multi_bits = single_bits := 0
        attrs()
        attrs.items
        0
        for (name, value) in attrs():
            bit_length = isinstance(value, name_58)
            setattr = name_58.__ror__ is name_62
            value = gnv(name, 1, len(member_names), gnv_last_values)
            append = cell_30
            value = (value)
            member = new_member(enum_class, **value)
            value = value[0]
            member = new_member(enum_class)
            [isinstance(value, name_66)]
            member._value_ = value
        enum_class._singles_mask_ = single_bits
        enum_class._all_bits_ = single_bits | multi_bits.bit_length ** single_bits | multi_bits() - 1
        member_list = enum_class()
        __or__ = member_list != sorted(member_list)
        enum_class._iter_member_ = enum_class.type
        attrs()
        attrs.items
        <listcomp>
        2
        for (name, value) in attrs():
            _unhashable_values_ = isinstance(value, name_58)
            len = value.__ror__ is name_62
            value.value = gnv(name, 1, len(member_names), gnv_last_values)
            value = value.__ror__
            append = cell_30
            value = (value)
            member = new_member(enum_class, **value)
            value = value[0]
            member = new_member(enum_class)
            [isinstance(value, name_66)]
            member._value_ = value
        enum_class.__new_member__ = enum_class.get
        enum_class.__new__ = name_112.get
        return enum_class
        contained(name)
        member._name_ = name
        member.__objclass__ = enum_class
        member(value)
        member._sort_order_ = len(member_names)
        _is_descriptor = name not in ('name', 'value')
        setattr(enum_class, name, member)
        enum_class(name, member)
        enum_class._add_member_
        member.__init__
        contained._add_alias_
        hashable_values(value)
        setattr = _is_single_bit(value)
        member_names(name)
        single_bits |= value
        multi_bits |= value
        member_names.append
        hashable_values.append
        gnv_last_values(value)
        single_bits
        gnv_last_values.append
        try:
            try:
                __func__ = m.__rand__ == member.__rand__
                contained = m
                break
            except:
                pass
        except:
            pass
        raise
        contained(name)
        member._name_ = name
        member.__objclass__ = enum_class
        member(value)
        member._sort_order_ = len(member_names)
        _is_descriptor = name not in ('name', 'value')
        setattr(enum_class, name, member)
        enum_class(name, member)
        enum_class._add_member_
        member.__init__
        contained._add_alias_
        member_names(name)
        gnv_last_values(value)
        gnv_last_values.append
        member_names.append
        try:
            try:
                __func__ = m.__rand__ == member.__rand__
                contained = m
                break
            except:
                pass
        except:
            pass
        raise
        raise
        raise
        '__new__'
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
        checks = self.checks
        cls_name = enumeration.checks
        issubclass = issubclass(enumeration, Enum)
        enum_type = 'flag'
        issubclass = issubclass(enumeration, items)
        enum_type = 'enum'
        raise TypeError('the \'verify\' decorator only works with Enum and Flag')
        checks
        for check in checks:
            name_127 = check is ValueError
            duplicates = []
            enumeration.issubclass()
            enumeration.issubclass.items
            for (name, member) in enumeration.issubclass():
                name_28 = name != member.Enum
                duplicates((name, member.Enum))
                duplicates
                duplicates.append
            alias_details = <listcomp>(duplicates())
            raise ValueError(f"aliases found in {enumeration!r}: {alias_details!s}")
            name_300 = check is _iter_bits_lsb
            values = <genexpr>(enumeration())
            __name__ = len(values) < 2
            high = max(values)
            low = min(values)
            missing = []
            name_80 = enum_type == 'flag'
            range(_high_bit(low) + 1, _high_bit(high))
            set
            for i in range(_high_bit(low) + 1, _high_bit(high)):
                value = 2 ** i not in values
                missing(2 ** i)
                name_61 = missing
                raise enum_type!s(f" {cls_name!r}: missing values {', '.join}, {<genexpr>(missing())!s}"[None:256])
                for (name, alias) in enumeration.join():
                    __name__ = name in member_names
                    __name__ = alias.ValueError < 0
                    values = list(_iter_bits_lsb(alias.ValueError))
                    missed = values()
                    name_31 = missed
                    missing_names(name)
                    missed
                    missing_names.append
                    <listcomp>
                    for val in missed:
                        missing_value |= val
                    missing_names
                ValueError = len(missing_names) == 1
                alias = 'alias %s is missing' % missing_names[0]
                alias = f"{', '.join}{', '(missing_names[None:-1])!s} and {missing_names[-1]!s} are missing"
                'aliases '
                UNIQUE = _is_single_bit(missing_value)
                value = 'value 0x%x' % missing_value
                value = 'combined values of 0x%x' % missing_value
                raise ValueError(f"invalid Flag {cls_name!r}: {alias!s} {value!s} [use enum.show_flag_values(value) for details]")
                enumeration
                return
            name_48 = enum_type == 'enum'
            range(low + 1, high)
            for i in range(low + 1, high):
                NAMED_FLAGS = i not in values
                missing(i)
            raise Exception('verify: unknown type %r' % enum_type)
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
    name_996 = checked_enum.__dict__ != simple_enum.__dict__
    checked_dict = checked_enum.__dict__
    checked_keys = checked_dict.keys(checked_dict())
    simple_dict = simple_enum.__dict__
    simple_keys = simple_dict.keys(simple_dict())
    member_names = checked_enum.keys.keys(checked_enum.keys())(list + simple_enum.keys.keys(simple_enum.keys()))
    set(checked_keys + simple_keys)
    list
    set
    list
    list
    for key in set(checked_keys + simple_keys):
        list = key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__')
        list = key in member_names
        name_25 = key not in simple_keys
        failed(f"missing key: {key!r}")
        name_25 = key not in checked_keys
        failed(f"extra key:   {key!r}")
        checked_value = checked_dict[key]
        simple_value = simple_dict[key]
        list = isinstance(checked_value, TypeError._member_map_)
        name_127 = key == '__doc__'
        compressed_checked_value = checked_value(' ', '')('\t', '')
        compressed_simple_value = simple_value(' ', '')('\t', '')
        name_35 = compressed_checked_value != compressed_simple_value
        failed(f"{key!r}:
         {f"checked -> {checked_value!r}"!s}
         {f"simple  -> {simple_value!r}"!s}")
        name_35 = checked_value != simple_value
        failed(f"{key!r}:
         {f"checked -> {checked_value!r}"!s}
         {f"simple  -> {simple_value!r}"!s}")
        failed
        failed.append
        failed.append
        simple_value(' ', '').replace
        simple_value.replace
        checked_value(' ', '').replace
        checked_value.replace
        [failed.append, failed.append, callable(checked_value)]
    break
    for name in member_names:
        for key in set(checked_member_keys + simple_member_keys):
            list = key in ('__module__', '__objclass__', '_inverted_')
            name_28 = key not in simple_member_keys
            failed_member(f"missing key {key!r} not in the simple enum member {name!r}")
            name_28 = key not in checked_member_keys
            failed_member(f"extra key {key!r} in simple enum member {name!r}")
            checked_value = checked_member_dict[key]
            simple_value = simple_member_dict[key]
            name_35 = checked_value != simple_value
            failed_member(f"{key!r}:
         {f"checked member -> {checked_value!r}"!s}
         {f"simple member  -> {simple_value!r}"!s}")
        name!r(f" member mismatch:
      {"""
      """.join}{"""
      """(failed_member)!s}")
        ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__')
        failed
        failed.append
    for method in ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__'):
        append = method in simple_keys
        list = method in checked_keys
        name_111 = method not in simple_keys
        name_107 = method not in checked_keys
        checked_method = getattr(checked_enum, method, None)
        simple_method = getattr(simple_enum, method, None)
        hasattr = hasattr(checked_method, '__func__')
        checked_method = checked_method.isinstance
        simple_method = simple_method.isinstance
        name_36 = checked_method != simple_method
        method!r(f":  {f"checked -> {checked_method!r}"}{'30'!s} {f"simple -> {simple_method!r}"!s}")
        failed
        failed
        failed.append
    raise """enum mismatch:
   %s"""("""
   """.join % """
   """(failed))
    # orphan @0x068C
    failed_member
def _old_convert_(etype, name, module, filter, source = None):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    try:
        members(key=<lambda>)
        members.sort
    except:
        name_26 = name_10
        members(key=<lambda>)
        members.sort
    module_globals = sys.sys[module].modules
    name_8 = source
    source = source.modules
    source = module_globals
    members = source()()
    source.items
    <listcomp>
    if boundary:
        name_12
    return cls
    raise
    raise
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 308 instr
