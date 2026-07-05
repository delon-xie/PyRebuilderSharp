# Decompiled from: <module>

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
    pass
    if hasattr(obj, '__get__'):
        return
    pass
    if hasattr(obj, '__set__'):
        pass
    hasattr(obj, '__delete__')

def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    pass
    if not len(name) > 4:
        name[-2:]
        name[-2:]
        name[:2]
    return

def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
    """
    pass
    if not len(name) > 2:
        name[-1]
        name[-1]
        name[0]
    return

def _is_internal_class(cls_name, obj):
    pass
    if not isinstance(obj, type):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if qualname == s_pattern:
        return
    qualname.endswith(e_pattern)

def _is_private(cls_name, name):
    pattern = '_%s__' % (cls_name)
    pat_len = len(pattern)
    pattern = '_%s__' % (cls_name)
    pat_len = len(pattern)
    if len(name) > pat_len:
        pass
        if name.startswith(pattern):
            pass
            if name[-1] != '_':
                return True
            pass
            if name[-2] != '_':
                pass
            return False
        return False
    return False

def _is_single_bit(num):
    """
    True if only one bit set in num (should be an int)
    """
    pass
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
        pass
    else:
        setattr(obj, '__reduce_ex__', _break_on_call_reduce)
        setattr(obj, '__module__', '<unknown>')

def _iter_bits_lsb(num):
    original = num
    original = num
    if isinstance(num, Enum):
        num = num.value
    pass
    if num < 0:
        raise ValueError('%r is not a positive integer' % original)
    pass
    while num:
        b = num & ~num + 1
        yield b
        num ^= b
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
    num = num.__index__()
    ceiling = 2 ** num.bit_length()
    if num >= 0:
        s = bltns.bin(num + ceiling).replace('1', '0', 1)
    else:
        s = bltns.bin(~num ^ ceiling - 1 + ceiling)
        sign = s[:3]
        digits = s[3:]
        if max_bits is not None:
            pass
            if len(digits) < max_bits:
                digits = sign[-1] * max_bits + digits[-max_bits:]
            return '%s %s' % (sign, digits)
        return '%s %s' % (sign, digits)
    sign = s[:3]
    digits = s[3:]

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
    def __init__(self, value):
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

    def __get__(self, instance, ownerclass):
        pass
        if instance is None:
            pass
            if self.member is not None:
                return self.member
            raise AttributeError('%r has no attribute %r' % (ownerclass, self.name))
            pass
            if self.fget is not None:
                return self.fget(instance)
            pass
            if self._attr_type == 'attr':
                return getattr(self._cls_type, self.name)
            pass
            if self._attr_type == 'desc':
                return getattr(instance._value_, self.name)
            return
        pass
        if self.fget is not None:
            pass
        pass
        if self._attr_type == 'attr':
            pass
        pass
        if self._attr_type == 'desc':
            pass
        try:
            pass
        except KeyError:
            raise
            raise
        return
        return

    def __set__(self, instance, value):
        pass
        if self.fset is not None:
            return self.fset(instance, value)
        raise AttributeError('<enum %r> cannot set attribute %r' % (self.clsname, self.name))

    def __delete__(self, instance):
        pass
        if self.fdel is not None:
            return self.fdel(instance)
        raise AttributeError('<enum %r> cannot delete attribute %r' % (self.clsname, self.name))

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
        delattr(enum_class, member_name)
        value = self.value
        if not isinstance(value, tuple):
            args = (value)
        else:
            args = value
            pass
            if enum_class._member_type_ is tuple:
                args = (args)
            pass
            if not enum_class._use_args_:
                enum_member = enum_class._new_member_(enum_class)
            else:
                pass
                pass
                if hasattr(enum_member, '_value_'):
                    value = enum_member._value_
                    enum_member._name_ = member_name
                    enum_member.__objclass__ = enum_class
                    enum_member._sort_order_ = len(enum_class._member_names_)
                    if Flag is not None:
                        pass
                        if issubclass(enum_class, Flag):
                            pass
                            if isinstance(value, int):
                                enum_class._flag_mask_ = enum_class._flag_mask_ | value
                                if _is_single_bit(value):
                                    enum_class._singles_mask_ = enum_class._singles_mask_ | value
                                enum_class._all_bits_ = 2 ** enum_class._flag_mask_.bit_length() - 1
                                try:
                                    try:
                                        enum_member = enum_class._value2member_map_[value]
                                    except:
                                        pass
                                    pass
                                except KeyError:
                                    enum_class._member_names_.append(member_name)
                                enum_class._add_member_(member_name, enum_member)
                                enum_class._value2member_map_.setdefault(value, enum_member)
                                if value not in enum_class._hashable_values_:
                                    enum_class._hashable_values_.append(value)
                                    return None
                                return None
                            enum_class._all_bits_ = 2 ** enum_class._flag_mask_.bit_length() - 1
                        try:
                            try:
                                enum_member = enum_class._value2member_map_[value]
                            except:
                                pass
                            pass
                        except KeyError:
                            enum_class._member_names_.append(member_name)
                    try:
                        try:
                            enum_member = enum_class._value2member_map_[value]
                        except:
                            pass
                        pass
                    except KeyError:
                        enum_class._member_names_.append(member_name)
                else:
                    pass
                    if enum_class._member_type_ is object:
                        enum_member._value_ = value
                    else:
                        try:
                            pass
                        except Exception:
                            new_exc = TypeError('_value_ not set in __new__, unable to create it')
                            new_exc.__cause__ = exc
                            raise new_exc
                            exc = None
                            raise
                            raise
                            value = enum_member._value_
                            enum_member._name_ = member_name
                            enum_member.__objclass__ = enum_class
                            enum_member._sort_order_ = len(enum_class._member_names_)
                            enum_member = enum_class._value2member_map_[value]
                            yield from issubclass(enum_class, Flag)
                            enum_class._all_bits_ = 2 ** enum_class._flag_mask_.bit_length() - 1
                            enum_class._flag_mask_ = enum_class._flag_mask_ | value
                            enum_class._singles_mask_ = enum_class._singles_mask_ | value
        for (name, canonical_member) in enum_class._member_map_.items():
            pass
            if canonical_member._value_ == value:
                enum_member = canonical_member
            else:
                pass
            pass
            enum_class._add_member_(member_name, enum_member)
            enum_class._value2member_map_.setdefault(value, enum_member)
            if value not in enum_class._hashable_values_:
                enum_class._hashable_values_.append(value)
                return None
            return None
        enum_member = canonical_member
        enum_class._add_member_(member_name, enum_member)
        enum_class._value2member_map_.setdefault(value, enum_member)

class EnumDict(dict):
    """
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
        self._ignore = value
        already = set(value) & set(self._member_names)
        setattr(self, '_generate_next_value', _gnv)
        pass
        if self._cls_name is not None:
            pass
            if _is_private(self._cls_name, key):
                pass
            pass
            if _is_sunder(key):
                pass
                if key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_'):
                    pass
                    if not key.startswith('_repr_'):
                        raise ValueError('_sunder_ names, such as %r, are reserved for future Enum use' % (key))
                    pass
                    if key == '_generate_next_value_':
                        pass
                        if self._auto_called:
                            raise TypeError('_generate_next_value_ must be defined before members')
                        pass
                        if isinstance(value, staticmethod):
                            pass
                        else:
                            value
                            setattr(self, '_generate_next_value', _gnv)
                            super().__setitem__(key, value)
                    else:
                        pass
                        if key == '_ignore_':
                            pass
                            if isinstance(value, str):
                                value = value.replace(',', ' ').split()
                            else:
                                value = list(value)
                                self._ignore = value
                                already = set(value) & set(self._member_names)
                                if already:
                                    raise ValueError('_ignore_ cannot specify already set names: %r' % (already))
                                pass
                        pass
                pass
                if key == '_generate_next_value_':
                    pass
                else:
                    pass
                    if key == '_ignore_':
                        pass
                    pass
            else:
                pass
                if _is_dunder(key):
                    pass
                    if key == '__order__':
                        key = '_order_'
                    pass
                else:
                    pass
                    if key in self._member_names:
                        raise TypeError('%r already defined as %r' % (key, self[key]))
                    pass
                    if key in self._ignore:
                        pass
                    else:
                        pass
                        if isinstance(value, nonmember):
                            value = value.value
                        else:
                            pass
                            if _is_descriptor(value):
                                pass
                            else:
                                pass
                                if self._cls_name is not None:
                                    pass
                                    if _is_internal_class(self._cls_name, value):
                                        pass
                                    pass
                                    if key in self:
                                        raise TypeError('%r already defined as %r' % (key, self[key]))
                                    pass
                                    if isinstance(value, member):
                                        value = value.value
                                    non_auto_store = True
                                    single = False
                                    if isinstance(value, auto):
                                        single = True
                                        value = (value)
                                    pass
                                    if isinstance(value, tuple):
                                        pass
                                        if any(lambda x: x(value)):
                                            _gnv = [auto_valued.append(v) for v in value if isinstance(v, auto) if v.value == _auto_null]
                                        pass
                                        if non_auto_store:
                                            self._last_values.append(value)
                                        super().__setitem__(key, value)
                                    pass
                                    if non_auto_store:
                                        pass
                                    super().__setitem__(key, value)
                                pass
                                if key in self:
                                    pass
                                pass
                                if isinstance(value, member):
                                    pass
                                non_auto_store = True
                                single = False
                                if isinstance(value, auto):
                                    pass
                                pass
                                if isinstance(value, tuple):
                                    pass
                                pass
                                if non_auto_store:
                                    pass
                                super().__setitem__(key, value)
        pass
        if _is_sunder(key):
            pass
        else:
            pass
            if _is_dunder(key):
                pass
            else:
                pass
                if key in self._member_names:
                    pass
                pass
                if key in self._ignore:
                    pass
                else:
                    pass
                    if isinstance(value, nonmember):
                        pass
                    else:
                        pass
                        if _is_descriptor(value):
                            pass
                        else:
                            pass
                            if self._cls_name is not None:
                                pass
                            pass
                            if key in self:
                                pass
                            pass
                            if isinstance(value, member):
                                pass
                            non_auto_store = True
                            single = False
                            if isinstance(value, auto):
                                pass
                            pass
                            if isinstance(value, tuple):
                                pass
                            pass
                            if non_auto_store:
                                pass
                            super().__setitem__(key, value)
        non_auto_store = True
        single = False
        auto_valued.append(v)
        value = auto_valued[0]
        value = t(auto_valued)

    @property
    def member_names(self):
        return list(self._member_names)

    def update(self, members):
        pass
        more_members.items()
        for (name, value) in more_members.items():
            pass
_EnumDict = EnumDict

class EnumType(type):
    """
    Metaclass for Enum
    """
    @classmethod
    def __prepare__(metacls, cls, bases):
        metacls._check_for_existing_members_(cls, bases)
        enum_dict = EnumDict(cls)
        member_type, first_enum = metacls._get_mixins_(cls, bases)
        metacls._check_for_existing_members_(cls, bases)
        enum_dict = EnumDict(cls)
        member_type, first_enum = metacls._get_mixins_(cls, bases)
        if first_enum is not None:
            '_generate_next_value_'
            enum_dict
            getattr(first_enum, '_generate_next_value_', None)
        return enum_dict

    def __new__(metacls, cls, bases, classdict, *, boundary, _simple):
        p = classdict[n]
        value = classdict[name]
        classdict = dict(classdict.items())
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        member_names = classdict._member_names
        invalid_names = set(member_names) & {'mro', ''}
        pass
        if _simple:
            return super().__new__(metacls, cls, bases, classdict, **kwds)
        classdict.setdefault('_ignore_', []).append('_ignore_')
        ignore = classdict['_ignore_']
        ignore
        ignore = [classdict.pop(key, None) for key in ignore]
        ignore = [classdict[name] for name in member_names]
        _gnv = [classdict[n] for n in member_names if isinstance(p.value, int) if p.value < 0 if p.value[0] < 0]
        inverted.append(p)
        bits |= p.value
        inverted.append(p)
        member_names = [p for p in inverted if isinstance(p.value, int)]
        p.value = bits & p.value
        p.value = (bits & p.value[0]) + p.value[1:]
        delattr(enum_class, '_%s__in_progress' % cls)
        yield from classdict
        classdict.update(enum_class.__dict__)
        method = member_type.__str__
        _order_ = [name for name in ('__repr__', '__str__', '__format__', '__reduce_ex__') if name not in classdict]
        enum_method = getattr(first_enum, name)
        found_method = getattr(enum_class, name)
        object_method = getattr(object, name)
        data_type_method = getattr(member_type, name)
        key = [name for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__') if name not in classdict]
        delattr(enum_class, '_boundary_')
        delattr(enum_class, '_flag_mask_')
        delattr(enum_class, '_singles_mask_')
        delattr(enum_class, '_all_bits_')
        delattr(enum_class, '_inverted_')

    def __bool__(cls):
        """
        classes/types should always be True.
        """
        return True

    def __call__(cls, value, names, *, module, qualname, type, start, boundary):
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
        pass
        if cls._member_map_:
            pass
            if names is not _not_given:
                value = (value, names) + values
            return cls.__new__(cls, value)
        pass
        if names is _not_given:
            pass
            if type is None:
                raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
            pass
            if names is _not_given:
                pass
            else:
                names
                return
        pass
        if names is _not_given:
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
        pass
        if isinstance(value, cls):
            return True
        pass
        if issubclass(cls, Flag):
            result = cls._missing_(value)
        ValueError
        raise
        if value in cls._unhashable_values_:
            pass
        value in cls._hashable_values_

    def __delattr__(cls, attr):
        pass
        if attr in cls._member_map_:
            raise AttributeError('%r cannot delete member %r.' % (cls.__name__, attr))
        super().__delattr__(attr)

    def __dir__(cls):
        interesting = set(['__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_'] + members)
        pass
        if issubclass(cls, Flag):
            members = list(cls._member_map_.keys())
        else:
            members = cls._member_names_
            interesting = set(['__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_'] + members)
            if cls._new_member_ is not object.__new__:
                interesting.add('__new__')
            pass
            if cls.__init_subclass__ is not object.__init_subclass__:
                interesting.add('__init_subclass__')
            pass
            if cls._member_type_ is object:
                return sorted(interesting)
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
        return (name for name in cls._member_names_)

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
        pass
        if Flag is not None:
            pass
            if issubclass(cls, Flag):
                return '<flag %r>' % cls.__name__
            return '<enum %r>' % cls.__name__
        return '<enum %r>' % cls.__name__

    def __reversed__(cls):
        """
        Return members in reverse definition order.
        """
        return (name for name in reversed(cls._member_names_))

    def __setattr__(cls, name, value):
        """
        Block attempts to reassign Enum members.

        A simple assignment to the class namespace only changes one of the
        several possible ways to get an Enum member from the Enum class,
        resulting in an inconsistent Enumeration.
        """
        member_map = cls.__dict__.get('_member_map_', {})
        member_map = cls.__dict__.get('_member_map_', {})
        if name in member_map:
            raise AttributeError('cannot reassign member %r' % (name))
        super().__setattr__(name, value)

    def _create_(cls, class_name, names, *, module, qualname, type, start, boundary):
        """
        Convenience method to create a new Enum class.

        `names` can be:

        * A string containing member names, separated either with spaces or
          commas.  Values are incremented by 1 from `start`.
        * An iterable of member names.  Values are incremented by 1 from `start`.
        * An iterable of (member name, value) pairs.
        * A mapping of member name -> value pairs.
        """
        _, first_enum = cls._get_mixins_(class_name, bases)
        classdict = metacls.__prepare__(class_name, bases)
        metacls = cls.__class__
        metacls = cls.__class__
        if type is None:
            pass
        else:
            (type, cls)
            _, first_enum = cls._get_mixins_(class_name, bases)
            classdict = metacls.__prepare__(class_name, bases)
            if isinstance(names, str):
                names = names.replace(',', ' ').split()
            # [Block @0x0052] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        names = [item for item in names if isinstance(item, str)]
        member_name = names[item]
        member_value = item
        module = sys._getframemodulename(2)
        _make_class_unpicklable(classdict)

    def _convert_(cls, name, module, filter, source, *, boundary, as_global):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        module_globals = sys.modules[module].__dict__
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        else:
            source = module_globals
            members = lambda _: None(source.items())
            members.sort(key=lambda t: (t[1], t[0]))
            body = {t: t for t in iterable}
            tmp_cls = type(name, (object), body)
            if boundary:
                pass
                if as_global:
                    global_enum(cls)
                else:
                    cls
                    sys.modules
                    pass
                    return cls
            else:
                KEEP

    @classmethod
    def _check_for_existing_members_(mcls, class_name, bases):
        bases
        for chain in bases:
            for base in chain.__mro__:
                pass
                if isinstance(base, EnumType):
                    pass
                    if base._member_names_:
                        raise TypeError('<enum %r> cannot extend %r' % (class_name, base))
                    pass
                pass
            pass

    @classmethod
    def _get_mixins_(mcls, class_name, bases):
        """
        Returns the type for creating enum members, and the first inherited
        enum class.

        bases: the tuple of bases that was given to __new__
        """
        first_enum = bases[-1]
        pass
        if not bases:
            return (object, Enum)
        first_enum = bases[-1]
        if not isinstance(first_enum, EnumType):
            raise TypeError('new enumerations should be created as `EnumName([mixin_type, ...] [data_type,] enum_type)`')
        pass
        if mcls._find_data_type_(class_name, bases):
            return (member_type, first_enum)
        object

    @classmethod
    def _find_data_repr_(mcls, class_name, bases):
        bases
        for chain in bases:
            for base in chain.__mro__:
                pass
                if base is object:
                    pass
                else:
                    pass
                    if isinstance(base, EnumType):
                        base._value_repr_
                        return
                    pass
                    if '__repr__' in base.__dict__:
                        pass
                        if '__dataclass_fields__' in base.__dict__:
                            pass
                            if '__dataclass_params__' in base.__dict__:
                                pass
                                if base.__dict__['__dataclass_params__'].repr:
                                    _dataclass_repr
                                    return
                                base.__dict__['__repr__']
                                return
                            base.__dict__['__repr__']
                            return
                        base.__dict__['__repr__']
                        return
                    pass
            pass

    @classmethod
    def _find_data_type_(mcls, class_name, bases):
        data_types = set()
        base_chain = set()
        bases
        for chain in bases:
            for base in chain.__mro__:
                base_chain.add(base)
                if base is object:
                    pass
                else:
                    pass
                    if isinstance(base, EnumType):
                        pass
                        if base._member_type_ is not object:
                            data_types.add(base._member_type_)
                        else:
                            pass
                    else:
                        pass
                        if '__new__' in base.__dict__:
                            pass
                            if candidate:
                                pass
                            else:
                                base
                        else:
                            pass
                            if '__dataclass_fields__' in base.__dict__:
                                pass
                            else:
                                pass
                                if candidate:
                                    pass
                                else:
                                    base
            pass

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
            return __new__ is not None
        pass
        if __new__ is None:
            for method in ('__new_member__', '__new__'):
                for possible in (member_type, first_enum):
                    target = getattr(possible, method, None)
                    if target not in {None, None.__new__, object.__new__, Enum.__new__}:
                        __new__ = target
                    else:
                        pass
                pass
                if __new__ is not None:
                    pass
                else:
                    pass
                pass
                if first_enum is None:
                    use_args = False
                else:
                    pass
                    if __new__ in (Enum.__new__, object.__new__):
                        pass
                    else:
                        use_args = True
                        return (__new__, save_new, use_args)
        pass
        if first_enum is None:
            pass
        else:
            pass
            if __new__ in (Enum.__new__, object.__new__):
                pass
            else:
                use_args = True

    def _add_member_(cls, name, member):
        pass
        if name in cls._member_map_:
            pass
            if cls._member_map_[name] is not member:
                raise NameError('%r is already bound: %r' % (name, cls._member_map_[name]))
        else:
            found_descriptor = descriptor_type = class_type = None
            cls.__mro__[1:]
            for base in cls.__mro__[1:]:
                attr = base.__dict__.get(name)
                if attr is not None:
                    pass
                    if isinstance(attr, (property, DynamicClassAttribute)):
                        found_descriptor = attr
                        class_type = base
                        descriptor_type = 'enum'
                    else:
                        pass
                        if _is_descriptor(attr):
                            found_descriptor = attr
                            if descriptor_type:
                                pass
                                if class_type:
                                    pass
                                else:
                                    base
                            else:
                                return 'desc'
                        else:
                            descriptor_type = 'attr'
                            class_type = base
                            pass
                pass
        redirect = property()
        redirect.member = member
        redirect.__set_name__(cls, name)
        redirect._attr_type = descriptor_type
        redirect._cls_type = class_type
        setattr(cls, name, redirect)

    @property
    def __signature__(cls):
        from inspect import Parameter, Signature, Parameter, Signature
        if cls._member_names_:
            return Signature([Parameter('values', Parameter.VAR_POSITIONAL)])
        return Signature([Parameter('new_class_name', Parameter.POSITIONAL_ONLY), Parameter('names', Parameter.POSITIONAL_OR_KEYWORD), Parameter('module', Parameter.KEYWORD_ONLY, default=None), Parameter('qualname', Parameter.KEYWORD_ONLY, default=None), Parameter('type', Parameter.KEYWORD_ONLY, default=None), Parameter('start', Parameter.KEYWORD_ONLY, default=1), Parameter('boundary', Parameter.KEYWORD_ONLY, default=None)])
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
        pass
        if type(value) is cls:
            return value
        return
        for (name, member) in cls._member_map_.items():
            pass
            if value == member._value_:
                cls[name]
                return
            pass
        result = cls._missing_(value)
        ve_exc = ValueError('%r is not a valid %s' % (value, cls.__qualname__))

    def _add_alias_(self, name):
        self.__class__._add_member_(name, self)

    def _add_value_alias_(self, value):
        cls = self.__class__
        cls = self.__class__
        if value in cls._value2member_map_:
            pass
            if cls._value2member_map_[value] is not self:
                raise ValueError('%r is already bound: %r' % (value, cls._value2member_map_[value]))
        else:
            pass
        try:
            cls._value2member_map_.setdefault(value, self)
            cls._hashable_values_.append(value)
        except TypeError:
            cls._unhashable_values_map_.setdefault(self.name, []).append(value)

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_values: the list of values assigned
        """
        pass
        if not last_values:
            return start
        last_value = sorted(last_values).pop()
        try:
            pass
        except TypeError:
            raise
            raise
        return
        return

    @classmethod
    def _missing_(cls, value):
        pass

    def __repr__(self):
        pass
        if self.__class__._value_repr_:
            return '<%s.%s: %s>' % (self.__class__.__name__, self._name_, v_repr(self._value_))
        repr

    def __str__(self):
        return '%s.%s' % (self.__class__.__name__, self._name_)

    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
        getattr(self, '__dict__', [])
        name = [name for name in getattr(self, '__dict__', []) if name[0] != '_']
        # [Block @0x005E] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        interesting.add(name)
        interesting.discard(name)

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
        'values must already be of type `str`'
        pass
        if len(values) > 3:
            raise TypeError('too many arguments for str(): %r' % (values))
        pass
        if len(values) == 1:
            pass
            if not isinstance(values[0], str):
                raise TypeError('%r is not a string' % (values[0]))
            pass
            if len(values) >= 2:
                pass
                if not isinstance(values[1], str):
                    raise TypeError('encoding must be a string, not %r' % (values[1]))
                pass
                if len(values) == 3:
                    pass
                    if not isinstance(values[2], str):
                        raise TypeError('errors must be a string, not %r' % values[2])
                    member = str.__new__(cls, value)
                    member._value_ = value
                    return member
                member = str.__new__(cls, value)
                member._value_ = value
                return member
            pass
            if len(values) == 3:
                pass
            member = str.__new__(cls, value)
            member._value_ = value
            return member
        pass
        if len(values) >= 2:
            pass
        pass
        if len(values) == 3:
            pass
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
STRICT, CONFORM, EJECT, KEEP = FlagBoundary

class Flag(Enum, boundary=STRICT):
    """
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
        pass
        if count:
            last_value = max(last_values)
            try:
                high_bit = _high_bit(last_value)
            except Exception:
                raise
                raise
                return 2 ** (high_bit + 1)
        else:
            pass
            if start is not None:
                return start
            return 1

    @classmethod
    def _iter_member_by_value_(cls, value):
        """
        Extract all members from the value in definition (i.e. increasing value) order.
        """
        _iter_bits_lsb(value & cls._flag_mask_)
        for val in _iter_bits_lsb(value & cls._flag_mask_):
            yield cls._value2member_map_.get(val)
    _iter_member_ = _iter_member_by_value_

    @classmethod
    def _iter_member_by_def_(cls, value):
        """
        Extract all members from the value in definition order.
        """
        yield from sorted(cls._iter_member_by_value_(value), key=lambda m: m._sort_order_)

    @classmethod
    def _missing_(cls, value):
        """
        Create a composite member containing all canonical members present in `value`.

        If non-member values are present, result depends on `_boundary_` setting.
        """
        pass
        if not isinstance(value, int):
            raise ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        flag_mask = cls._flag_mask_
        singles_mask = cls._singles_mask_
        all_bits = cls._all_bits_
        neg_value = None
        value
        value
        ~all_bits
        pass
        pass
        pass
        pass
        if cls._boundary_ is STRICT:
            max_bits = max(value.bit_length(), flag_mask.bit_length())
            raise ValueError("""%r invalid value %r
    given %s
  allowed %s""" % (cls, value, bin(value, max_bits), bin(flag_mask, max_bits)))
        pass
        if cls._boundary_ is CONFORM:
            value &= flag_mask
        else:
            pass
            if cls._boundary_ is EJECT:
                return value
            pass
            if cls._boundary_ is KEEP:
                pass
                if value < 0:
                    value = max(all_bits + 1, 2 ** value.bit_length()) + value
                pass
                pass
                if value < 0:
                    neg_value = value
                    if cls._boundary_ in (EJECT, KEEP):
                        value = all_bits + 1 + value
                    else:
                        value = singles_mask & value
                        unknown = value & ~flag_mask
                        aliases = value & ~singles_mask
                        member_value = value & singles_mask
                        if unknown:
                            pass
                            if cls._boundary_ is not KEEP:
                                raise ValueError('%s(%r) -->  unknown values %r [%s]' % (cls.__name__, value, unknown, bin(unknown)))
                            pass
                            if cls._member_type_ is object:
                                pseudo_member = object.__new__(cls)
                            else:
                                pseudo_member = cls._member_type_.__new__(cls, value)
                                pass
                                if not hasattr(pseudo_member, '_value_'):
                                    pseudo_member._value_ = value
                                pass
                                if member_value:
                                    flag_mask = [combined_value | m._value_ for m in cls._iter_member_(member_value)]
                                else:
                                    pass
                                    if aliases:
                                        pass
                                    else:
                                        pseudo_member._name_ = None
                                        pseudo_member = cls._value2member_map_.setdefault(value, pseudo_member)
                                        if neg_value is not None:
                                            neg_value
                                            cls._value2member_map_
                                            pseudo_member
                                        return pseudo_member
                        pass
                        if cls._member_type_ is object:
                            pass
                        else:
                            pseudo_member = cls._member_type_.__new__(cls, value)
                unknown = value & ~flag_mask
                aliases = value & ~singles_mask
                member_value = value & singles_mask
                if unknown:
                    pass
                pass
                if cls._member_type_ is object:
                    pass
                else:
                    pseudo_member = cls._member_type_.__new__(cls, value)
            else:
                raise ValueError('%r unknown flag boundary %r' % (cls, cls._boundary_))
        unknown = value & ~flag_mask
        aliases = value & ~singles_mask
        member_value = value & singles_mask
        # [Block @0x01EC] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        pseudo_member._name_ = None
        pseudo_member = cls._value2member_map_.setdefault(value, pseudo_member)

    def __contains__(self, other):
        """
        Returns True if self has at least the same flags set as other.
        """
        pass
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
        if self.__class__._value_repr_:
            pass
            if self._name_ is None:
                return '<%s: %s>' % (cls_name, v_repr(self._value_))
            return '<%s.%s: %s>' % (cls_name, self._name_, v_repr(self._value_))
        repr

    def __str__(self):
        cls_name = self.__class__.__name__
        cls_name = self.__class__.__name__
        if self._name_ is None:
            return '%s(%r)' % (cls_name, self._value_)
        return '%s.%s' % (cls_name, self._name_)

    def __bool__(self):
        return bool(self._value_)

    def _get_value(self, flag):
        pass
        if isinstance(flag, self.__class__):
            return flag._value_
        pass
        if self._member_type_ is not object:
            pass
            if isinstance(flag, self._member_type_):
                return flag
            return NotImplemented
        return NotImplemented

    def __or__(self, other):
        value = self._value_
        other_value = self._get_value(other)
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        if value is None:
            for flag in (self, other):
                pass
                if self._get_value(flag) is None:
                    raise TypeError(f"'{flag}' cannot be combined with other flags with |")
                pass
        else:
            pass
            if other_value is None:
                pass
            return self.__class__(value | other_value)

    def __and__(self, other):
        value = self._value_
        other_value = self._get_value(other)
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        if value is None:
            for flag in (self, other):
                pass
                if self._get_value(flag) is None:
                    raise TypeError(f"'{flag}' cannot be combined with other flags with &")
                pass
        else:
            pass
            if other_value is None:
                pass
            return self.__class__(value & other_value)

    def __xor__(self, other):
        value = self._value_
        other_value = self._get_value(other)
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_
        if value is None:
            for flag in (self, other):
                pass
                if self._get_value(flag) is None:
                    raise TypeError(f"'{flag}' cannot be combined with other flags with ^")
                pass
        else:
            pass
            if other_value is None:
                pass
            return self.__class__(value ^ other_value)

    def __invert__(self):
        pass
        if self._get_value(self) is None:
            raise TypeError(f"'{self}' cannot be inverted")
        pass
        if self._inverted_ is None:
            pass
            if self._boundary_ in (EJECT, KEEP):
                self._inverted_ = self.__class__(~self._value_)
                return self._inverted_
            self._inverted_ = self.__class__(self._singles_mask_ & ~self._value_)
            return self._inverted_
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
    return value.bit_length() - 1

def unique(enumeration):
    """
    Class decorator for enumerations ensuring unique member values.
    """
    duplicates = []
    enumeration.__members__.items()
    # [Block @0x000E] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')

def _dataclass_repr(self):
    return (self, ', '.join)((k for k in dcf.keys() if dcf.keys()[k].repr))

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
    cls_name = self.__class__.__name__
    if self._name_ is None:
        return '%s.%s(%r)' % (module, cls_name, self._value_)
    pass
    if _is_single_bit(self._value_):
        return '%s.%s' % (module, self._name_)
    pass
    if self._boundary_ is not FlagBoundary.KEEP:
        return ('|'.join)([name for name in self.name.split('|')])
    name = []
    self._name_.split('|')
    name = [n for n in self._name_.split('|') if n[0].isdigit()]
    name.append('%s.%s' % (module, n))

def global_str(self):
    """
    use enum_name instead of class.enum_name
    """
    pass
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
    pass
    if issubclass(cls, Flag):
        cls.__repr__ = global_flag_repr
    else:
        cls.__repr__ = global_enum_repr
        pass
        if issubclass(cls, ReprEnum):
            pass
            if update_str:
                cls.__str__ = global_str
            sys.modules[cls.__module__].__dict__.update(cls.__members__)
            return cls
        cls.__str__ = global_str

def _simple_enum(etype, *, boundary, use_args):
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
        enum_method = getattr(cls_name, name)
        found_method = getattr(enum_class, name)
        object_method = getattr(object, name)
        data_type_method = getattr(member_type, name)
        attrs = {}
        body = {}
        __new__ = cls.__dict__.get('__new__')
        cls_name = cls.__name__
        cls_name = cls.__name__
        if __new__ is None:
            __new__
            cls_name._use_args_
        __new__ = cls.__dict__.get('__new__')
        if __new__ is not None:
            new_member = __new__.__func__
        else:
            new_member = cls_name._member_type_.__new__
            attrs = {}
            body = {}
            if __new__ is not None:
                '__new_member__'
                body
                new_member
            gnv = '_generate_next_value_'
            member_names = '_member_names_'
            member_map = '_member_map_'
            value2member_map = '_value2member_map_'
            hashable_values = '_hashable_values_'
            unhashable_values = '_unhashable_values_'
            member_type = '_member_type_'
            if issubclass(cls_name, Flag):
                pass
                if cls:
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
                else:
                    cls_name._boundary_
            cls.__dict__.items()
            # [Block @0x0152] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        gnv = [name for name in ('__repr__', '__str__', '__format__', '__reduce_ex__') if name not in body]
        gnv_last_values = []
        # [Block @0x023C] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        value = value[0]
        contained = value2member_map.get(member._value_)
        contained = m
        contained._add_alias_(name)
        member._name_ = name
        member.__objclass__ = enum_class
        member.__init__(value)
        member._sort_order_ = len(member_names)
        setattr(enum_class, name, member)
        hashable_values.append(value)
        member_names.append(name)
        single_bits |= value
        gnv_last_values.append(value)
        # [Block @0x041A] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        value = value[0]
        contained = value2member_map.get(member._value_)
        contained = m
        contained._add_alias_(name)
        member._name_ = name
        member.__objclass__ = enum_class
        member.__init__(value)
        member._sort_order_ = len(member_names)
        setattr(enum_class, name, member)
        member_names.append(name)
        gnv_last_values.append(value)
        enum_class._value2member_map_.setdefault(value, member)
    return convert_class

@_simple_enum(StrEnum)
class EnumCheck:
    """
    various conditions to check an enumeration for
    """
    CONTINUOUS = 'no skipped integer values'
    NAMED_FLAGS = 'multi-flag aliases may not contain unnamed flags'
    UNIQUE = 'one name per value'
CONTINUOUS, NAMED_FLAGS, UNIQUE = EnumCheck

class verify:
    """
    Check an enumeration for various constraints. (see EnumCheck)
    """
    def __init__(self):
        self.checks = checks

    def __call__(self, enumeration):
        low = max(values)
        high = min(values)
        missing = []
        checks = self.checks
        cls_name = enumeration.__name__
        checks = self.checks
        cls_name = enumeration.__name__
        if Flag is not None:
            pass
            if issubclass(enumeration, Flag):
                enum_type = 'flag'
            pass
            if issubclass(enumeration, Enum):
                enum_type = 'enum'
            else:
                raise TypeError('the \'verify\' decorator only works with Enum and Flag')
                checks
                # [Block @0x0040] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        pass
        if issubclass(enumeration, Enum):
            pass
        else:
            raise TypeError('the \'verify\' decorator only works with Enum and Flag')
        enum_type = [i for i in range(_high_bit(low) + 1, _high_bit(high)) if 2 ** i not in values]
        enum_type = [i for i in range(low + 1, high) if i not in values]
        # [Block @0x01C4] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
        missing_value |= val
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
    checked_value = checked_dict[key]
    simple_value = simple_dict[key]
    failed = []
    failed = []
    if checked_enum.__dict__ != simple_enum.__dict__:
        name = [key for key in set(checked_keys + simple_keys) if key in ('__module__', '_member_map_', '_value2member_map_', '__doc__', '__static_attributes__', '__firstlineno__') if checked_value != simple_value if compressed_checked_value != compressed_simple_value]
    pass
    if failed:
        raise TypeError("""enum mismatch:
   %s""" % """
   """.join(failed))
    name = [[] for name in member_names if name not in simple_keys if failed_member if checked_value != simple_value for name in member_names if name not in simple_keys if failed_member if checked_method != simple_method]
    failed_member = []
    failed.append('missing member from simple enum: %r' % name)
    failed.append('extra member in simple enum: %r' % name)
    failed_member.append('missing key %r not in the simple enum member %r' % (key, name))
    failed_member.append('extra key %r in simple enum member %r' % (key, name))
    checked_value = checked_member_dict[key]
    simple_value = simple_member_dict[key]
    checked_value = [method for method in ('__str__', '__repr__', '__reduce_ex__', '__format__', '__getnewargs_ex__', '__getnewargs__', '__reduce_ex__', '__reduce__') if method in simple_keys if method not in simple_keys if checked_method != simple_method]
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)

def _old_convert_(etype, name, module, filter, source, *, boundary):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    module_globals = sys.modules[module].__dict__
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    else:
        source = module_globals
        members = lambda _: None(source.items())
        members.sort(key=lambda t: (t[1], t[0]))
        pass
        if boundary:
            return cls
        KEEP
