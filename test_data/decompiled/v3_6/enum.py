# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType
from types import DynamicClassAttribute
__all__ = ['EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin']
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
        pass
    return hasattr(obj, '__delete__')
def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    if len(name) > 4:
        pass
    return name[-3] != '_'
def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
    """
    if len(name) > 2:
        pass
    return name[-2] != '_'
def _is_internal_class(cls_name, obj):
    if not isinstance(obj, type):
        return False
    qualname = getattr(obj, '__qualname__', '')
    s_pattern = cls_name + '.' + getattr(obj, '__name__', '')
    e_pattern = '.' + s_pattern
    if qualname == s_pattern:
        pass
    else:
        return qualname.endswith(e_pattern)
def _is_private(cls_name, name):
    pattern = '_%s__' % (cls_name)
    pat_len = len(pattern)
    if len(name) > pat_len:
        if name.startswith(pattern) and (name[-1] != '_'):
            pass
        return True
    else:
        return False
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
        setattr(obj, '__reduce_ex__', _break_on_call_reduce)
def _iter_bits_lsb(num):
    original = num
    if isinstance(num, Enum):
        num = num.value
        if num < 0:
            pass
        num = b
        if num:
            b = num & ~num + 1
            yield b
    raise
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
    if (max_bits is not None) and (len(digits) < max_bits):
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
    member = None
    _attr_type = None
    _cls_type = None
    def __get__(self, instance, ownerclass):
        if (instance is None) and (self.member is not None):
            return self.member
        raise AttributeError('%r has no attribute %r' % (ownerclass, self.name))
        return self.fget(instance)
        try:
            return ownerclass._member_map_[self.name]
        except KeyError:
            raise AttributeError('%r has no attribute %r' % (ownerclass, self.name)) from None
        # orphan @0x0048
        return getattr(self._cls_type, self.name)
        # orphan @0x0060
        return getattr(instance._value_, self.name)
        # orphan @0x0084
        raise AttributeError('%r has no attribute %r' % (ownerclass, self.name)) from None
        # orphan @0x009E
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
        # orphan @0x00BA
        value = enum_member._value_
        enum_member._name_ = member_name
        enum_member.__objclass__ = enum_class
        # orphan @0x00AE
        exc = None
        # orphan @0x00A8
        # orphan @0x008E
        new_exc = TypeError('_value_ not set in __new__, unable to create it')
        new_exc.__cause__ = exc
        raise new_exc
        # orphan @0x0086
        # orphan @0x0084
        # orphan @0x006C
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
                pass
            except:
                pass
        except KeyError:
            pass
        # orphan @0x00E0
        # orphan @0x00EA
        # orphan @0x00F6
        # orphan @0x0102
        enum_class._flag_mask_ | value._flag_mask_ = enum_class
        # orphan @0x011A
        # orphan @0x0146
        # orphan @0x014E
        # orphan @0x0158
        # orphan @0x016A
        # orphan @0x016C
        # orphan @0x017E
        enum_member = canonical_member
        # orphan @0x0188
        raise KeyError
        # orphan @0x018E
        # orphan @0x0194
        # orphan @0x0198
        # orphan @0x01A2
        # orphan @0x01B2
        # orphan @0x01C0
        enum_class._member_names_.append(member_name)
        # orphan @0x01D8
        # orphan @0x01DC
        # orphan @0x01E4
        # orphan @0x01F0
        # orphan @0x01FA
        enum_class._member_names_.append(member_name)
        # orphan @0x0206
        # orphan @0x020C
        enum_class._add_member_(member_name, enum_member)
        enum_class._value2member_map_.setdefault(value, enum_member)
        # orphan @0x022A
        # orphan @0x0232
        # orphan @0x0234
        enum_class._hashable_values_.append(value)
        # orphan @0x0242
        # orphan @0x0244
        # orphan @0x024E
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
        # orphan @0x00E0
        # orphan @0x00D4
        # orphan @0x00CE
        raise
        # orphan @0x00C8
        # orphan @0x00C4
        # orphan @0x00AC
        already = set(value) & set(self._member_names)
        # orphan @0x00A8
        # orphan @0x006C
        # orphan @0x0064
        # orphan @0x005A
        # orphan @0x0052
        raise TypeError('_generate_next_value_ must be defined before members')
        # orphan @0x004C
        # orphan @0x0044
        if (self._cls_name is not None) and _is_private(self._cls_name, key) and _is_sunder(key):
            pass
        raise TypeError('%r already defined as %r' % (key, self[key]))
        self._auto_called = True
        v = v.value
        self._last_values.append(v)
        break
        for v in value:
            if isinstance(v, auto):
                non_auto_store = False
                if v.value == _auto_null:
                    pass
        if single:
            value = auto_valued[0]
            try:
                value = t(auto_valued)
            except TypeError:
                pass
        raise ValueError('_sunder_ names, such as %r, are reserved for future Enum use' % (key))
        setattr(self, '_generate_next_value', _gnv)
        # orphan @0x00EA
        key = '_order_'
        # orphan @0x0114
        # orphan @0x0124
        # orphan @0x0186
        # orphan @0x0194
        # orphan @0x0196
        # orphan @0x019A
        non_auto_store = True
        single = False
        # orphan @0x01AE
        single = True
        value = (value)
        # orphan @0x01C4
        # orphan @0x01D2
        # orphan @0x01D8
        auto_valued = []
        t = type(value)
        # orphan @0x026E
        # orphan @0x0272
        # orphan @0x027C
        # orphan @0x02AC
        super().__setitem__(key, value)
    @property
    def member_names(self):
        return list(self._member_names)
    def update(self, members):
        # orphan @0x0024
        # orphan @0x001E
        try:
            for name in name:
                pass
        except AttributeError:
            pass
        # orphan @0x002C
        # orphan @0x0038
        # orphan @0x003A
        # orphan @0x004A
        # orphan @0x0052
        # orphan @0x005C
        # orphan @0x005E
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
        # orphan @0x00CA
        (member_type, first_enum) = metacls._get_mixins_(cls, bases)
        # orphan @0x00AE
        _gnv = staticmethod(_gnv)
        classdict = dict(classdict.items())
        # orphan @0x00A2
        # orphan @0x0084
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
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
        for name in name:
            value = classdict[name]
        if boundary:
            break
        elif (Flag is not None) and bases and issubclass(bases[-1], Flag):
            for n in member_names:
                p = classdict[n]
                if isinstance(p.value, int) and (p.value < 0):
                    inverted.append(p)
                    bits |= p.value
                if (p.value is None) and isinstance(p.value, tuple) and p.value and isinstance(p.value[0], int) and (p.value[0] < 0):
                    inverted.append(p)
                    bits |= p.value[0]
                elif Flag is not None:
                    break
                    if Flag is not None:
                        pass
                break
                for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
                    if name not in classdict:
                        enum_method = getattr(first_enum, name)
                        object_method = getattr(object, name)
                        data_type_method = getattr(member_type, name)
                enum_method = getattr(Flag, name)
                break
                for name in name:
                    pass
                if (Enum is not None) and save_new:
                    pass
                if _order_:
                    _order_ = EnumType.__new__.<locals>.<listcomp>(_order_)
                if isinstance(_order_, str):
                    _order_ = _order_.replace(',', ' ').split()
                    if (Flag is None) and (cls != 'Flag'):
                        pass
                if _order_:
                    _order_ = EnumType.__new__.<locals>.<listcomp>(_order_)
                    if () != _order_._member_names_:
                        raise
                return
        # orphan @0x0278
        # orphan @0x0280
        # orphan @0x0282
        # orphan @0x0292
        p.value = bits & p.value
        p.value = (bits & p.value[0]) + p.value[1:]
        # orphan @0x02C0
        # orphan @0x02C4
        # orphan @0x0308
        # orphan @0x0312
        # orphan @0x0326
        raise
        # orphan @0x032C
        # orphan @0x0332
        def <genexpr>(.0):
            for n in .0:
                yield repr(n)
                break
        # orphan @0x033E
        # orphan @0x0354
        # orphan @0x035E
        # orphan @0x0368
        raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
        # orphan @0x0370
        # orphan @0x037A
        # orphan @0x0396
        method = member_type.__str__
        # orphan @0x03A8
        method = member_type.__repr__
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
        if cls._member_map_ and (names is not _not_given):
            value = (value, names) + values
            return cls.__new__(cls, value)
        elif type is None:
            raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
        # orphan @0x0044
        # orphan @0x0052
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
            return isinstance(result, cls)
        except ValueError:
            pass
        # orphan @0x0036
        # orphan @0x0042
        # orphan @0x004C
        return value in cls._hashable_values_
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
            if isinstance(names, (tuple, list)) and names and isinstance(names[0], str):
                original_names = []
                names = names
                last_values = []
            elif module is None:
                _make_class_unpicklable(classdict)
            try:
                pass
            except AttributeError:
                pass
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
        return
        # orphan @0x0108
        # orphan @0x0114
        module = sys._getframemodulename(2)
        # orphan @0x0124
        # orphan @0x014A
        # orphan @0x015A
        # orphan @0x0188
        # orphan @0x0192
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
            members.sort(key=EnumType._convert_.<locals>.<lambda>)
        body = EnumType._convert_.<locals>.<dictcomp>(members)
        tmp_cls = type(name, (object), body)
        if boundary:
            pass
        global_enum(cls)
        return cls
        # orphan @0x0048
        # orphan @0x0050
        members.sort(key=EnumType._convert_.<locals>.<lambda>)
    @classmethod
    def _check_for_existing_members_(mcls, class_name, bases):
        for chain in bases:
            for base in chain.__mro__:
                if isinstance(base, EnumType) and base._member_names_:
                    pass
                raise
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
        # orphan @0x0026
        # orphan @0x0032
        member_type = object
        return (member_type, first_enum)
    @classmethod
    def _find_data_repr_(mcls, class_name, bases):
        for chain in bases:
            for base in chain.__mro__:
                if base is object:
                    continue
                    if isinstance(base, EnumType):
                        return base._value_repr_
                    return
                if base.__dict__['__dataclass_params__'].repr:
                    pass
            return base.__dict__['__repr__']
        return None
        # orphan @0x003C
        # orphan @0x006A
    @classmethod
    def _find_data_type_(mcls, class_name, bases):
        data_types = set()
        base_chain = set()
        for chain in bases:
            for base in chain.__mro__:
                base_chain.add(base)
                if base is object:
                    continue
                    if isinstance(base, EnumType) and (base._member_type_ is not object):
                        data_types.add(base._member_type_)
                        continue
                        if ('__new__' in base.__dict__) or ('__dataclass_fields__' in base.__dict__) and candidate:
                            return None
                        else:
                            break
                    raise
                    if data_types:
                        return data_types.pop()
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
        __new__ = classdict.get('__new__', None)
        if first_enum is not None:
            for possible in (member_type, first_enum):
                target = getattr(possible, method, None)
                if target not in # Unknown node: SetLiteral:
                    __new__ = target
                return (save_new, use_args)
        else:
            save_new = __new__ is not None
        for method in ('__new_member__', '__new__'):
            pass
        __new__ = object.__new__
        if first_enum is None:
            pass
        # orphan @0x0066
        # orphan @0x0070
        # orphan @0x009A
        use_args = True
    def _add_member_(cls, name, member):
        if (name in cls._member_map_) and (cls._member_map_[name] is not member):
            raise NameError('%r is already bound: %r' % (name, cls._member_map_[name]))
        for base in 1:
            attr = base.__dict__.get(name)
            if (attr is not None) and isinstance(attr, (property, DynamicClassAttribute)):
                found_descriptor = attr
                class_type = base
                descriptor_type = 'enum'
                continue
                if _is_descriptor(attr):
                    found_descriptor = attr
                    if descriptor_type:
                        pass
                    else:
                        descriptor_type = 'desc'
                    break
                    return None
                    class_type = base
                    continue
                redirect._cls_type = class_type
            redirect._set = getattr(found_descriptor, '__set__', None)
            redirect.fdel = getattr(found_descriptor, 'fdel', None)
            redirect = property()
            redirect.member = member
            redirect.__set_name__(cls, name)
            if descriptor_type in ('enum', 'desc'):
                redirect.fget = getattr(found_descriptor, 'fget', None)
                redirect._get = getattr(found_descriptor, '__get__', None)
        found_descriptor = None
        descriptor_type = None
        class_type = None
    @property
    def __signature__(cls):
        from inspect import Parameter
        from inspect import Signature
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
        # orphan @0x008C
        # orphan @0x0082
        return cls[name]
        # orphan @0x0072
        # orphan @0x0070
        # orphan @0x0062
        if type(value) is cls:
            return value
        try:
            return cls._value2member_map_[value]
        except KeyError:
            return
        return cls[name]
        raise TypeError('do not use `super().__new__; call the appropriate __new__ directly') from None
        for (name, unhashable_values) in cls._unhashable_values_map_.items():
            pass
        result = cls._missing_(value)
        try:
            if isinstance(result, cls):
                return result
        finally:
            exc = None
            ve_exc = None
        # orphan @0x0094
        # orphan @0x009A
        # orphan @0x00B6
        raise TypeError('%r has no members defined' % cls)
        # orphan @0x00C2
        exc = None
        # orphan @0x00D6
        # orphan @0x00E0
        exc = e
        result = None
        # orphan @0x00F2
        # orphan @0x00F6
        e = None
        # orphan @0x011E
        # orphan @0x012A
        # orphan @0x0136
        # orphan @0x0142
        return result
        # orphan @0x015C
        ve_exc = ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        # orphan @0x0170
        # orphan @0x017C
        exc = TypeError('error in %s._missing_: returned %r instead of None or a valid member' % (cls.__name__, result))
        # orphan @0x018E
        # orphan @0x019A
        exc.__context__ = ve_exc
        raise exc
        # orphan @0x01A4
    def _add_alias_(self, name):
        self.__class__._add_member_(name, self)
    def _add_value_alias_(self, value):
        # orphan @0x0046
        # orphan @0x003E
        cls = self.__class__
        try:
            if value in cls._value2member_map_:
                if cls._value2member_map_[value] is not self:
                    raise ValueError('%r is already bound: %r' % (value, cls._value2member_map_[value]))
                for m in cls._member_map_.values():
                    if (m._value_ == value) and (m is not self):
                        raise ValueError('%r is already bound: %r' % (value, cls._value2member_map_[value]))
                    break
                    break
                    return None
                continue
                try:
                    cls._value2member_map_.setdefault(value, self)
                    cls._hashable_values_.append(value)
                except TypeError:
                    cls._unhashable_values_.append(value)
            return None
        except TypeError:
            pass
        for m in cls._member_map_.values():
            if (m._value_ == value) and (m is not self):
                raise ValueError('%r is already bound: %r' % (value, cls._value2member_map_[value]))
            break
            break
            return None
        continue
        try:
            cls._value2member_map_.setdefault(value, self)
            cls._hashable_values_.append(value)
        except TypeError:
            cls._unhashable_values_.append(value)
        # orphan @0x00B2
        # orphan @0x00BA
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
        if not last_values:
            return start
        try:
            last_value = sorted(last_values).pop()
        except TypeError:
            raise
            raise TypeError('unable to sort non-numeric values') from None
        try:
            return last_value + 1
        except TypeError:
            pass
        # orphan @0x0022
        raise TypeError('unable to sort non-numeric values') from None
        # orphan @0x0032
        # orphan @0x004A
        # orphan @0x0058
        raise
        # orphan @0x0060
    @classmethod
    def _missing_(cls, value):
        pass
    def __repr__(self):
        if self.__class__._value_repr_:
            return (self._name_, v_repr(self._value_))
        v_repr = repr
    def __str__(self):
        return '%s.%s' % (self.__class__.__name__, self._name_)
    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        # orphan @0x0032
        # orphan @0x0030
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
        elif name not in self._member_map_:
            interesting.add(name)
        elif (name[0] == '_') and isinstance(obj, property) and (obj.fget is not None):
            pass
        # orphan @0x0056
        # orphan @0x00D4
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
        elif not isinstance(values[2], str):
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
        if count or (start is not None):
            return 1
        # orphan @0x002A
        # orphan @0x0032
        raise TypeError('invalid flag value %r' % last_value) from None
        # orphan @0x0046
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
        # orphan @0x00CC
        value = max(all_bits + 1, 2 ** value.bit_length()) + value
        raise ValueError('%r unknown flag boundary %r' % (cls, cls._boundary_))
        # orphan @0x00C4
        # orphan @0x00B6
        return value
        # orphan @0x00A8
        # orphan @0x0064
        max_bits = max(value.bit_length(), flag_mask.bit_length())
        # orphan @0x005A
        # orphan @0x004E
        # orphan @0x004A
        # orphan @0x001C
        flag_mask = cls._flag_mask_
        if not isinstance(value, int):
            raise ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        all_bits = cls._all_bits_
        def <listcomp>(.0):
            for m in m._name_:
                pass
            return
        if not value <= value:
            pass
        raise
        if cls._boundary_ is CONFORM:
            pass
        return pseudo_member
        # orphan @0x00FA
        # orphan @0x00FC
        # orphan @0x0104
        neg_value = value
        # orphan @0x0118
        value = all_bits + 1 + value
        value = singles_mask & value
        # orphan @0x012E
        unknown = value & ~flag_mask
        aliases = value & ~singles_mask
        member_value = value & singles_mask
        # orphan @0x0154
        # orphan @0x015C
        # orphan @0x0170
        raise
        # orphan @0x0176
        # orphan @0x0182
        pseudo_member = object.__new__(cls)
        pseudo_member = cls._member_type_.__new__(cls, value)
        # orphan @0x019C
        # orphan @0x01A8
        # orphan @0x01AC
        # orphan @0x01B4
        # orphan @0x01BA
        members = []
        combined_value = 0
        # orphan @0x01C6
        # orphan @0x01CE
        # orphan @0x01D0
        members.append(m)
        combined_value |= m._value_
        # orphan @0x01EA
        # orphan @0x01F2
        value = member_value | aliases
        # orphan @0x0206
        # orphan @0x0208
        # orphan @0x0218
        # orphan @0x0220
        # orphan @0x0232
        members.append(pm)
        # orphan @0x023E
        combined_value = pm._value_
        # orphan @0x024A
        unknown = value ^ combined_value
        pseudo_member._name_ = '|'.join(Flag._missing_.<locals>.<listcomp>(members))
        # orphan @0x0270
        pseudo_member._name_ = None
        # orphan @0x027E
        # orphan @0x028A
        raise ValueError('%r: no members with value %r' % (cls, unknown))
        # orphan @0x029A
        # orphan @0x02A2
        pseudo_member._name_ + '|%s' % cls._numeric_repr_(unknown)._name_ = pseudo_member
        # orphan @0x02BA
        pseudo_member._name_ = None
        # orphan @0x02C2
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
            return (v_repr(self._value_))
        v_repr = repr
        if self._name_ is None:
            pass
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
        return flag
        # orphan @0x001C
        # orphan @0x0048
        return NotImplemented
    def __or__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        for flag in (self, other):
            if self._get_value(flag) is None:
                pass
            raise
        # orphan @0x0024
        value = self._value_
        # orphan @0x005A
        return self.__class__(value | other_value)
    def __and__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        for flag in (self, other):
            if self._get_value(flag) is None:
                pass
            raise
        # orphan @0x0024
        value = self._value_
        # orphan @0x005A
        return self.__class__(value & other_value)
    def __xor__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        for flag in (self, other):
            if self._get_value(flag) is None:
                pass
            raise
        # orphan @0x0024
        value = self._value_
        # orphan @0x005A
        return self.__class__(value ^ other_value)
    def __invert__(self):
        # orphan @0x001E
        if self._get_value(self) is None:
            raise TypeError(f"'{self}' cannot be inverted")
        self._inverted_ = self.__class__(~self._value_)
        self._inverted_ = self.__class__(self._singles_mask_ & ~self._value_)
        # orphan @0x0028
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
    for (name, member) in enumeration.__members__.items():
        if name != member.name:
            duplicates.append((name, member.name))
    if duplicates:
        alias_details = ', '.join(unique.<locals>.<listcomp>(duplicates))
        raise ValueError('duplicate values found in %r: %s' % (enumeration, alias_details))
    # orphan @0x005E
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
    return _is_single_bit(self._value_) % ('%s.%s', self._name_)
    cls_name = self.__class__.__name__
    if self._name_ is None:
        return ('%s.%s(%r)', cls_name, self._value_)
    return ('|'.join)(global_flag_repr.<locals>.<listcomp>(self.name.split('|')))
    # orphan @0x008A
    name = []
    # orphan @0x008C
    # orphan @0x009A
    name.append(n)
    # orphan @0x00BA
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
    if issubclass(cls, Flag):
        cls.__repr__ = global_flag_repr
        cls.__repr__ = global_enum_repr
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
        # orphan @0x01F0
        found_method = getattr(enum_class, name)
        object_method = getattr(object, name)
        data_type_method = getattr(member_type, name)
        # orphan @0x01E4
        # orphan @0x01E2
        # orphan @0x0048
        # orphan @0x0038
        attrs = {}
        body = {}
        cls_name = cls.__name__
        __new__ = cls.__dict__.get('__new__')
        new_member = __new__.__func__
        gnv = '_generate_next_value_'
        member_names = '_member_names_'
        member_map = '_member_map_'
        value2member_map = '_value2member_map_'
        hashable_values = '_hashable_values_'
        unhashable_values = '_unhashable_values_'
        member_type = '_member_type_'
        if '_value_repr_'(issubclass, Flag):
            enum_class = body('__doc__', type, (cls_name), boundary=body, _simple=True)
            break
            hashable_values.append(value)
            if _is_single_bit(value):
                member_names.append(name)
                single_bits |= value
            for (name, obj) in cls.__dict__.items():
                if name in ('__dict__', '__weakref__'):
                    continue
                    if _is_dunder(name):
                        pass
                    for m in enum_class:
                        contained = m
                    if contained is not None:
                        contained._add_alias_(name)
                        member._name_ = name
                        member.__objclass__ = enum_class
                        member.__init__(value)
                        member._sort_order_ = len(member_names)
                        if name not in ('name', 'value'):
                            pass
                    if _is_sunder(name):
                        pass
                try:
                    contained = value2member_map.get(member._value_)
                except TypeError:
                    contained = None
        setattr(enum_class, name, enum_method)
        enum_class._all_bits_ = 1
        member_list = _simple_enum.<locals>.convert_class.<locals>.<listcomp>(enum_class)
        if member_list != sorted(member_list):
            enum_class._iter_member_ = enum_class._iter_member_by_def_
        # orphan @0x0236
        gnv_last_values = []
        # orphan @0x0248
        single_bits = 0
        multi_bits = 0
        # orphan @0x025C
        # orphan @0x0260
        # orphan @0x0272
        # orphan @0x027E
        value = gnv(name, 1, len(member_names), gnv_last_values)
        # orphan @0x0296
        # orphan @0x02A2
        value = (value)
        member = new_member(enum_class, **value)
        value = value[0]
        member = new_member(enum_class)
        # orphan @0x02C8
        # orphan @0x02D2
        # orphan @0x02EA
        # orphan @0x02F4
        def <listcomp>(.0):
            for m in m._value_:
                pass
            return
        # orphan @0x030A
        # orphan @0x03D2
        multi_bits |= value
        # orphan @0x03DA
        gnv_last_values.append(value)
        # orphan @0x03E4
        # orphan @0x03E8
        enum_class._flag_mask_ = single_bits | multi_bits
        enum_class._singles_mask_ = single_bits
        # orphan @0x0444
        # orphan @0x0448
        # orphan @0x045A
        # orphan @0x0466
        value.value = gnv(name, 1, len(member_names), gnv_last_values)
        value = value.value
        # orphan @0x0486
        # orphan @0x0492
        value = (value)
        member = new_member(enum_class, **value)
        value = value[0]
        member = new_member(enum_class)
        # orphan @0x04B8
        # orphan @0x04C2
        member._value_ = value
        contained = value2member_map.get(member._value_)
        # orphan @0x04DA
        # orphan @0x04E4
        contained = None
        # orphan @0x04FA
        # orphan @0x0502
        # orphan @0x0506
        # orphan @0x050C
        # orphan @0x050E
        # orphan @0x051E
        contained = m
        # orphan @0x0528
        # orphan @0x0530
        # orphan @0x053A
        contained._add_alias_(name)
        # orphan @0x054A
        member.__objclass__ = enum_class
        # orphan @0x0556
        member._sort_order_ = len(member_names)
        # orphan @0x0570
        setattr(enum_class, name, member)
        enum_class._add_member_(name, member)
        # orphan @0x0592
        member_names.append(name)
        gnv_last_values.append(value)
        # orphan @0x05AA
        # orphan @0x05C0
        hashable_values.append(value)
        # orphan @0x05CE
        # orphan @0x05D8
        enum_class._unhashable_values_.append(value)
        enum_class._unhashable_values_map_.setdefault(name, []).append(value)
        # orphan @0x0604
        # orphan @0x0608
        # orphan @0x060A
        # orphan @0x0614
        enum_class.__new_member__ = enum_class.__new__
        # orphan @0x0620
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
        # orphan @0x00BC
        values = set(verify.__call__.<locals>.<genexpr>(enumeration))
        # orphan @0x00B0
        # orphan @0x003E
        checks = self.checks
        cls_name = enumeration.__name__
        if (Flag is not None) and issubclass(enumeration, Flag):
            enum_type = 'flag'
            if issubclass(enumeration, Enum):
                enum_type = 'enum'
            for (name, member) in enumeration.__members__.items():
                if name != member.name:
                    duplicates.append((name, member.name))
                low = max(values)
                high = min(values)
                missing = []
                if enum_type == 'flag':
                    pass
                break
                for val in missed:
                    missing_value |= val
                for (name, alias) in enumeration._member_map_.items():
                    if name in member_names:
                        pass
                    values = list(_iter_bits_lsb(alias.value))
                    missed = verify.__call__.<locals>.<listcomp>(values)
                    if missed:
                        pass
                if missing_names and (len(missing_names) == 1):
                    pass
                value = 'value 0x%x' % missing_value
                value = 'combined values of 0x%x' % missing_value
                raise
                for check in checks:
                    if check is UNIQUE:
                        duplicates = []
                    for i in low:
                        if 2 ** i not in values:
                            missing.append(2 ** i)
                    if missing:
                        raise ValueError('invalid %s %r: missing values %s' % (enum_type, cls_name, ', '.join(verify.__call__.<locals>.<genexpr>(missing)))[None:256])
                    member_names = enumeration._member_names_
                    missing_names = []
                    missing_value = 0
                return enumeration
                alias = 'aliases %s and %s are missing' % (', '.join(missing_names[None:-1]), missing_names[-1])
                if _is_single_bit(missing_value):
                    pass
            if duplicates:
                alias_details = ', '.join(verify.__call__.<locals>.<listcomp>(duplicates))
                raise ValueError('aliases found in %r: %s' % (enumeration, alias_details))
            elif enum_type == 'enum':
                for i in range(low + 1, high):
                    if i not in values:
                        missing.append(i)
        raise
        # orphan @0x0172
        raise Exception('verify: unknown type %r' % enum_type)
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
                            if callable(checked_value):
                                break
                                if checked_value != simple_value:
                                    pass
                                break
                                checked_member_keys = list(checked_member_dict.keys())
                                simple_member_dict = simple_enum[name].__dict__
                                simple_member_keys = list(simple_member_dict.keys())
                                for key in set(checked_member_keys + simple_member_keys):
                                    if (key in ('__module__', '__objclass__', '_inverted_')) and (key not in simple_member_keys):
                                        failed_member.append('missing key %r not in the simple enum member %r' % (key, name))
                                    failed_member.append('extra key %r in simple enum member %r' % (key, name))
                                    checked_value = checked_member_dict[key]
                                    simple_value = simple_member_dict[key]
                                    if checked_value != simple_value:
                                        failed_member.append("""%r:
         %s
         %s""" % (key, 'checked member -> %r' % (checked_value), 'simple member  -> %r' % (simple_value)))
                                if failed_member:
                                    failed.append("""%r member mismatch:
      %s""" % (name, """
      """.join(failed_member)))
                            continue
                            if key == '__doc__':
                                pass
                        break
                elif compressed_checked_value != compressed_simple_value:
                    pass
    raise
    # orphan @0x0166
    failed.sort()
    # orphan @0x0178
    # orphan @0x017C
    failed_member = []
    # orphan @0x018C
    failed.append('missing member from simple enum: %r' % name)
    # orphan @0x01A6
    # orphan @0x02A2
    # orphan @0x02AA
    # orphan @0x02AC
    # orphan @0x02B8
    # orphan @0x02C4
    # orphan @0x02D2
    # orphan @0x02DC
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)
    # orphan @0x0300
    checked_method = checked_method.__func__
    simple_method = simple_method.__func__
    # orphan @0x0316
    # orphan @0x0328
    # orphan @0x0338
    # orphan @0x033C
    # orphan @0x0344
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
        members.sort(key=_old_convert_.<locals>.<lambda>)
    if boundary:
        pass
    else:
        return cls
    # orphan @0x0048
    # orphan @0x0050
    members.sort(key=_old_convert_.<locals>.<lambda>)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 334 instr
