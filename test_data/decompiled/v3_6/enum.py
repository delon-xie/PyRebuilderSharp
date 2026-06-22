# Decompiled from: <module>

import sys
import builtins as bltns
from types import MappingProxyType, DynamicClassAttribute
__all__ = ['EnumType', 'EnumMeta', 'EnumDict', 'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 'ReprEnum', 'auto', 'unique', 'property', 'verify', 'member', 'nonmember', 'FlagBoundary', 'STRICT', 'CONFORM', 'EJECT', 'KEEP', 'global_flag_repr', 'global_enum_repr', 'global_str', 'global_enum', 'EnumCheck', 'CONTINUOUS', 'NAMED_FLAGS', 'UNIQUE', 'pickle_by_global_name', 'pickle_by_enum_name', 'show_flag_values', 'bin']
Enum = None
Flag = None
EJECT = None
ReprEnum = None
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
        pass
    elif hasattr(obj, '__set__'):
        pass
    else:
        return hasattr(obj, '__delete__')
def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    return name[-3] != '_'
def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
    """
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
        if name.startswith(pattern):
            pass
    else:
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
        setattr(obj, '__reduce_ex__', _break_on_call_reduce)
        '__module__'
        obj
        setattr
        '__module__'
        obj
        '<unknown>'
        '__reduce_ex__'
        obj
        _break_on_call_reduce
def _iter_bits_lsb(num):
    original = num
    if isinstance(num, Enum):
        num = num.value
        if num < 0:
            original
            '%r is not a positive integer'
            ValueError
        num = b
        if num:
            b = num & ~num + 1
            yield b
            num
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
    member = None
    _attr_type = None
    _cls_type = None
    def __get__(self, instance, ownerclass):
        if (instance is None) and (self.member is not None):
            return self.member
        else:
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
    def __set__(self, instance, value):
        if self.fset is not None:
            return self.fset(instance, value)
        else:
            raise AttributeError('<enum %r> cannot set attribute %r' % (self.clsname, self.name))
    def __delete__(self, instance):
        if self.fdel is not None:
            return self.fdel(instance)
        else:
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
        value = enum_member._value_
        enum_member._name_ = member_name
        enum_member.__objclass__ = enum_class
        new_exc = TypeError('_value_ not set in __new__, unable to create it')
        new_exc.__cause__ = exc
        raise new_exc
        args = (args)
        delattr(enum_class, member_name)
        value = self.value
        if not isinstance(value, tuple):
            args = (value)
            args = value
        enum_member = enum_class._new_member_(enum_class)
        enum_member = enum_class._new_member_(enum_class, **args)
        if not hasattr(enum_member, '_value_'):
            enum_class._member_type_
        enum_class._all_bits_ = 2 ** enum_class._flag_mask_.bit_length() - 1
        try:
            try:
                pass
            except:
                pass
        except KeyError:
            pass
        enum_member = canonical_member
        raise KeyError
        enum_class._member_names_.append(member_name)
        enum_class._member_names_.append(member_name)
        enum_class._hashable_values_.append(value)
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
        raise
        # orphan @0x00C8
        (already)
        already = set(value) & set(self._member_names)
        # orphan @0x0064
        value.__func__
        raise TypeError('_generate_next_value_ must be defined before members')
        if (self._cls_name is not None) and _is_private(self._cls_name, key) and _is_sunder(key):
            key
        raise TypeError('%r already defined as %r' % (key, self[key]))
        break
        for v in value:
            if isinstance(v, auto):
                non_auto_store = False
                if v.value == _auto_null:
                    len
                    1
                    key
                    self._generate_next_value
        if single:
            value = auto_valued[0]
            try:
                value = t(auto_valued)
            except TypeError:
                pass
        raise ValueError('_sunder_ names, such as %r, are reserved for future Enum use' % (key))
        '_repr_'
        key.startswith
        setattr(self, '_generate_next_value', _gnv)
        # orphan @0x00EA
        key = '_order_'
        self._member_names
        # orphan @0x0124
        isinstance(value, nonmember)
        non_auto_store = True
        single = False
        single = True
        value = (value)
        # orphan @0x01C4
        EnumDict.__setitem__.<locals>.<genexpr>(value)
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
_EnumDict = EnumDict
class EnumType(type):
    """
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
        (member_type, first_enum) = metacls._get_mixins_(cls, bases)
        _gnv = staticmethod(_gnv)
        classdict = dict(classdict.items())
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        if _simple:
            return super().__new__(metacls, cls, bases, classdict, **kwds)
        else:
            classdict.setdefault('_ignore_', []).append('_ignore_')
            ignore = classdict['_ignore_']
            ignore
        for key in ignore:
            classdict.pop(key, None)
        member_names = classdict._member_names
        invalid_names = set(member_names) & {'mro', ''}
        if invalid_names:
            raise ValueError('invalid enum member name(s) %s' % ','.join(EnumType.__new__.<locals>.<genexpr>(invalid_names)))
        else:
            member_names
            '_use_args_'
            '_use_args_'
            classdict
            use_args
            '_new_member_'
            classdict
            __new__
        for name in member_names:
            value = classdict[name]
        '_unhashable_values_map_'
        classdict
        {}
        '_unhashable_values_'
        classdict
        []
        '_hashable_values_'
        classdict
        []
        '_value2member_map_'
        classdict
        {}
        '_member_map_'
        classdict
        {}
        '_member_names_'
        classdict
        []
        metacls
        '_member_type_'
        classdict
        member_type
        if boundary:
            break
        else:
            classdict
            0
            '_singles_mask_'
            classdict
            0
            '_flag_mask_'
            classdict
            0
            '_boundary_'
            classdict
            getattr(first_enum, '_boundary_', None)
        if (Flag is not None) and bases and issubclass(bases[-1], Flag):
            for n in member_names:
                p = classdict[n]
                if isinstance(p.value, int) and (p.value < 0):
                    inverted.append(p)
                    bits |= p.value
                if (p.value is None) and isinstance(p.value, tuple):
                    if p.value and isinstance(p.value[0], int) and (p.value[0] < 0):
                        inverted.append(p)
                        bits |= p.value[0]
                    elif Flag is not None:
                        break
                        if Flag is not None:
                            member_list
                    ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__')
                    break
                    for name in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
                        if name not in classdict:
                            enum_method = getattr(first_enum, name)
                            object_method = getattr(object, name)
                            data_type_method = getattr(member_type, name)
                            found_method in (data_type_method, object_method)
                    Flag is not None
                else:
                    name
                    setattr
                enum_method = getattr(Flag, name)
                break
                for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__'):
                    name not in classdict
                if (Enum is not None) and save_new:
                    pass
                if _order_:
                    _order_ = EnumType.__new__.<locals>.<listcomp>(_order_)
                    ()
                _order_ is not None
                if isinstance(_order_, str):
                    _order_ = _order_.replace(',', ' ').split()
                    if Flag is None:
                        pass
                if _order_:
                    _order_ = EnumType.__new__.<locals>.<listcomp>(_order_)
                    if () != _order_._member_names_:
                        raise
                return
        _order_ is not None
        # orphan @0x0292
        p.value = bits & p.value
        p.value = (bits & p.value[0]) + p.value[1:]
        raise
        raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
        method = member_type.__str__
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
        else:
            names is _not_given
        if type is None:
            raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
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
        return value in cls._hashable_values_
    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError('%r cannot delete member %r.' % (cls.__name__, attr))
        # orphan @0x001C
        super().__delattr__(attr)
    def __dir__(cls):
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
        cls._get_mixins_
        metacls = cls.__class__
        if type is None:
            (type, cls)
            (cls)
        classdict = metacls.__prepare__(class_name, bases)
        if isinstance(names, str):
            names = names.replace(',', ' ').split()
            if isinstance(names, (tuple, list)) and names and isinstance(names[0], str):
                original_names = []
                names = names
                last_values = []
                enumerate(original_names)
            elif module is None:
                _make_class_unpicklable(classdict)
                '__module__'
                classdict
                module
            try:
                pass
            except AttributeError:
                pass
        last_values.append(value)
        names.append((name, value))
        for (count, name) in enumerate(original_names):
            first_enum
        if names is None:
            for item in names:
                if isinstance(item, str):
                    member_name = names[item]
                    member_value = item
                    (member_name, member_value) = item
        return
        # orphan @0x0192
        metacls.__new__
    def _convert_(cls, name, module, filter, source):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        # orphan @0x001C
        EnumType._convert_.<locals>.<listcomp>
        ()
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
        elif as_global:
            global_enum(cls)
            cls.__module__
            sys.modules
        return cls
    @classmethod
    def _check_for_existing_members_(mcls, class_name, bases):
        bases
        for chain in bases:
            for base in chain.__mro__:
                if isinstance(base, EnumType) and base._member_names_:
                    '<enum %r> cannot extend %r' % (class_name, base)
                    TypeError
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
        member_type = object
        return (member_type, first_enum)
    @classmethod
    def _find_data_repr_(mcls, class_name, bases):
        bases
        for chain in bases:
            for base in chain.__mro__:
                if base is object:
                    continue
                    if isinstance(base, EnumType):
                        return base._value_repr_
                    else:
                        return
                '__dataclass_params__' in base.__dict__
                if base.__dict__['__dataclass_params__'].repr:
                    _dataclass_repr
            return base.__dict__['__repr__']
        # orphan @0x003C
        '__repr__' in base.__dict__
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
                        continue
                    raise
                    if data_types:
                        return data_types.pop()
                elif candidate:
                    pass
                else:
                    break
                    if candidate:
                        pass
                    else:
                        candidate = base
        if len(data_types) > 1:
            'too many data types for %r: %r'
            TypeError
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
                if target not in {None, None.__new__, object.__new__, Enum.__new__}:
                    __new__ = target
                __new__
                return (save_new, use_args)
        else:
            save_new = __new__ is not None
            if __new__ is None:
                ('__new_member__', '__new__')
            return (save_new, use_args)
        __new__ = object.__new__
        # orphan @0x0094
        False
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
                        redirect
                        descriptor_type
                    else:
                        descriptor_type = 'desc'
                        if class_type:
                            break
                        else:
                            class_type = base
                            continue
                redirect._cls_type = class_type
                setattr
            redirect._set = getattr(found_descriptor, '__set__', None)
            redirect.fdel = getattr(found_descriptor, 'fdel', None)
            redirect
            getattr(found_descriptor, '__delete__', None)
            redirect = property()
            redirect.member = member
            redirect.__set_name__(cls, name)
            if descriptor_type in ('enum', 'desc'):
                redirect.fget = getattr(found_descriptor, 'fget', None)
                redirect._get = getattr(found_descriptor, '__get__', None)
                found_descriptor
                getattr
            return None
        found_descriptor
        found_descriptor = None
        descriptor_type = None
        class_type = None
        1
        cls.__mro__
    @property
    def __signature__(cls):
        from inspect import Parameter, Signature
        if cls._member_names_:
            return Signature([Parameter('values', Parameter.VAR_POSITIONAL)])
        else:
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
        return cls[name]
        if type(value) is cls:
            return value
        try:
            return cls._value2member_map_[value]
        except KeyError:
            return
        return cls[name]
        raise TypeError('do not use `super().__new__; call the appropriate __new__ directly') from None
        for (name, unhashable_values) in cls._unhashable_values_map_.items():
            value
        result = cls._missing_(value)
        try:
            if isinstance(result, cls):
                return result
        finally:
            exc = None
            ve_exc = None
        raise TypeError('%r has no members defined' % cls)
        exc = e
        result = None
        return result
        ve_exc = ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        exc = TypeError('error in %s._missing_: returned %r instead of None or a valid member' % (cls.__name__, result))
        exc.__context__ = ve_exc
        raise exc
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
        cls._member_map_.values()
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
        else:
            last_value = sorted(last_values).pop()
        try:
            return last_value + 1
        except TypeError:
            pass
        raise TypeError('unable to sort non-numeric values') from None
        raise
    @classmethod
    def _missing_(cls, value):
        pass
    def __repr__(self):
        if self.__class__._value_repr_:
            return (self._name_, v_repr(self._value_))
        else:
            v_repr = repr
            self.__class__
            '<%s.%s: %s>'
    def __str__(self):
        return '%s.%s' % (self.__class__.__name__, self._name_)
    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
            getattr(self, '__dict__', [])
        elif name not in self._member_map_:
            interesting.add(name)
        elif (name[0] == '_') and isinstance(obj, property):
            pass
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
            raise TypeError('too many arguments for str(): %r' % (values))
        elif not isinstance(values[0], str):
            raise TypeError('%r is not a string' % (values[0]))
        elif not isinstance(values[2], str):
            raise TypeError('errors must be a string, not %r' % values[2])
        # orphan @0x0060
        (values[1])
        raise
        # orphan @0x0072
        3
        len(values)
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
STRICT = *FlagBoundary
CONFORM = *FlagBoundary
EJECT = *FlagBoundary
KEEP = *FlagBoundary
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
        raise TypeError('invalid flag value %r' % last_value) from None
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
        # orphan @0x00CC
        value = max(all_bits + 1, 2 ** value.bit_length()) + value
        return value
        max_bits = max(value.bit_length(), flag_mask.bit_length())
        flag_mask = cls._flag_mask_
        if not isinstance(value, int):
            raise ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        all_bits = cls._all_bits_
        def <listcomp>(.0):
            .0
            []
            for m in .0:
                pass
            return
        if not value <= value:
            pass
        raise
        if cls._boundary_ is CONFORM:
            value & flag_mask
        cls._boundary_
        neg_value
        return pseudo_member
        neg_value = value
        # orphan @0x0118
        value = all_bits + 1 + value
        value = singles_mask & value
        unknown = value & ~flag_mask
        aliases = value & ~singles_mask
        member_value = value & singles_mask
        # orphan @0x015C
        (cls.__name__, value, unknown, bin(unknown))
        raise
        # orphan @0x0182
        pseudo_member = object.__new__(cls)
        pseudo_member = cls._member_type_.__new__(cls, value)
        members = []
        combined_value = 0
        members.append(m)
        combined_value |= m._value_
        members.append(pm)
        combined_value = pm._value_
        pseudo_member._name_ = None
        raise ValueError('%r: no members with value %r' % (cls, unknown))
        # orphan @0x02BA
        pseudo_member._name_ = None
        # orphan @0x02C2
        cls._value2member_map_
    def __contains__(self, other):
        """
        Returns True if self has at least the same flags set as other.
        """
        if not isinstance(other, self.__class__):
            raise TypeError('unsupported operand type(s) for \'in\': %r and %r' % (type(other).__qualname__, self.__class__.__qualname__))
        else:
            return
        # orphan @0x0026
        other._value_ & self._value_
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
            cls_name
            '<%s: %s>'
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
        return flag
        # orphan @0x001C
        self._member_type_ is not object
        return NotImplemented
    def __or__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        for flag in (self, other):
            if self._get_value(flag) is None:
                flag
                '\''
                TypeError
            raise
        # orphan @0x0024
        value = self._value_
        value is None
        return self.__class__(value | other_value)
    def __and__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        for flag in (self, other):
            if self._get_value(flag) is None:
                flag
                '\''
                TypeError
            raise
        # orphan @0x0024
        value = self._value_
        value is None
        return self.__class__(value & other_value)
    def __xor__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        for flag in (self, other):
            if self._get_value(flag) is None:
                flag
                '\''
                TypeError
            raise
        # orphan @0x0024
        value = self._value_
        value is None
        return self.__class__(value ^ other_value)
    def __invert__(self):
        if self._get_value(self) is None:
            raise TypeError(f"'{self}' cannot be inverted")
        self._inverted_ = self.__class__(~self._value_)
        self._inverted_ = self.__class__(self._singles_mask_ & ~self._value_)
        # orphan @0x0028
        self._boundary_
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
    # orphan @0x003E
    return _is_single_bit(self._value_) % ('%s.%s', self._name_)
    cls_name = self.__class__.__name__
    if self._name_ is None:
        return ('%s.%s(%r)', cls_name, self._value_)
    return ('|'.join)(global_flag_repr.<locals>.<listcomp>(self.name.split('|')))
    name.append(n)
    return '|'.join(name)
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
        cls.__repr__ = global_enum_repr
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
        found_method = getattr(enum_class, name)
        object_method = getattr(object, name)
        data_type_method = getattr(member_type, name)
        attrs = {}
        body = {}
        cls_name = cls.__name__
        __new__ = cls.__dict__.get('__new__')
        __new__
        __new__
        new_member = __new__.__func__
        gnv = '_generate_next_value_'
        member_names = '_member_names_'
        member_map = '_member_map_'
        value2member_map = '_value2member_map_'
        body
        []
        []
        body
        {}
        {}
        body
        {}
        {}
        body
        []
        []
        body
        '_use_args_'._generate_next_value_
        '_use_args_'._generate_next_value_
        body
        hashable_values = '_hashable_values_'
        unhashable_values = '_unhashable_values_'
        member_type = '_member_type_'
        if '_value_repr_'(issubclass, Flag):
            enum_class = body('__doc__', type, (cls_name), boundary=body, _simple=True)
            ('__repr__', '__str__', '__format__', '__reduce_ex__')
            'An enumeration.'
            'An enumeration.'
            break
            hashable_values.append(value)
            if _is_single_bit(value):
                member_names.append(name)
                single_bits |= value
        setattr(enum_class, name, enum_method)
        enum_class._all_bits_ = 1
        member_list = _simple_enum.<locals>.convert_class.<locals>.<listcomp>(enum_class)
        if member_list != sorted(member_list):
            enum_class._iter_member_ = enum_class._iter_member_by_def_
            attrs.items()
        gnv_last_values = []
        value = gnv(name, 1, len(member_names), gnv_last_values)
        # orphan @0x02A2
        value = (value)
        member = new_member(enum_class, **value)
        value = value[0]
        member = new_member(enum_class)
        def <listcomp>(.0):
            .0
            []
            for m in .0:
                pass
            return
        multi_bits |= value
        gnv_last_values.append(value)
        enum_class._flag_mask_ = single_bits | multi_bits
        enum_class._singles_mask_ = single_bits
        value.value = gnv(name, 1, len(member_names), gnv_last_values)
        value = value.value
        # orphan @0x0492
        value = (value)
        member = new_member(enum_class, **value)
        value = value[0]
        member = new_member(enum_class)
        contained = None
        # orphan @0x04FA
        member._value_ in hashable_values
        contained = m
        # orphan @0x053A
        contained._add_alias_(name)
        member.__objclass__ = enum_class
        member._sort_order_ = len(member_names)
        # orphan @0x0570
        setattr(enum_class, name, member)
        enum_class._add_member_(name, member)
        hashable_values.append(value)
        enum_class.__new_member__ = enum_class.__new__
        return enum_class
    return convert_class
EnumCheck = _simple_enum(StrEnum)(__build_class__(EnumCheck, 'EnumCheck'))
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
        # orphan @0x00BC
        values = set(verify.__call__.<locals>.<genexpr>(enumeration))
        2
        len(values)
        checks = self.checks
        cls_name = enumeration.__name__
        if (Flag is not None) and issubclass(enumeration, Flag):
            enum_type = 'flag'
            if issubclass(enumeration, Enum):
                enum_type = 'enum'
                'the \'verify\' decorator only works with Enum and Flag'
                TypeError
            for (name, member) in enumeration.__members__.items():
                if name != member.name:
                    duplicates.append((name, member.name))
                low = max(values)
                high = min(values)
                missing = []
                if enum_type == 'flag':
                    low
                    _high_bit
                    range
                break
                missed
                for val in missed:
                    missing_value |= val
                for (name, alias) in enumeration._member_map_.items():
                    if name in member_names:
                        0
                        alias.value
                    values = list(_iter_bits_lsb(alias.value))
                    missed = verify.__call__.<locals>.<listcomp>(values)
                    if missed:
                        missing_names.append(name)
                if missing_names and (len(missing_names) == 1):
                    0
                    missing_names
                    'alias %s is missing'
                value = 'value 0x%x' % missing_value
                value = 'combined values of 0x%x' % missing_value
                alias
                cls_name
                'invalid Flag %r: %s %s [use enum.show_flag_values(value) for details]'
                ValueError
                value
                raise
                for check in checks:
                    if check is UNIQUE:
                        duplicates = []
                        enumeration.__members__.items()
                    for i in low:
                        if 2 ** i not in values:
                            missing.append(2 ** i)
                        missed
                    if missing:
                        raise ValueError('invalid %s %r: missing values %s' % (enum_type, cls_name, ', '.join(verify.__call__.<locals>.<genexpr>(missing)))[None:256])
                    check
                    member_names = enumeration._member_names_
                    missing_names = []
                    missing_value = 0
                    enumeration._member_map_.items()
                    self
                    self
                    verify.__call__.<locals>.<listcomp>(enumeration)
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
                    value
        raise
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
                        else:
                            break
                    ('simple  -> %r' % (simple_value))
                elif compressed_checked_value != compressed_simple_value:
                    'checked -> %r' % (checked_value)
                    key
                    """%r:
         %s
         %s"""
                    failed.append
            ''
            ' '
            simple_value.replace
    raise
    failed_member = []
    failed.append('missing member from simple enum: %r' % name)
    # orphan @0x01A6
    failed.append
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)
    checked_method = checked_method.__func__
    simple_method = simple_method.__func__
    # orphan @0x0316
    'checked -> %r' % (checked_method)
    failed.append
    # orphan @0x0344
    """
   """.join(failed)
def _old_convert_(etype, name, module, filter, source):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    # orphan @0x001C
    _old_convert_.<locals>.<listcomp>
    ()
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
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 334 instr
