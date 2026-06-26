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
        return
    if hasattr(obj, '__set__'):
        pass

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
        return
    return qualname.endswith(e_pattern)

def _is_private(cls_name, name):
    pattern = '_%s__' % (cls_name)
    pat_len = len(pattern)
    return (len(name) > pat_len) and name.startswith(pattern) and (name[-1] != '_') or (name[-2] != '_')
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
        sign = s[:3]
        digits = s[3:]
        if max_bits is not None:
            if len(digits) < max_bits:
                digits = sign[-1] * max_bits + digits[-max_bits:]
            return '%s %s' % (sign, digits)
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
        if instance is None:
            if self.member is not None:
                return self.member
            raise AttributeError('%r has no attribute %r' % (ownerclass, self.name))
            if self.fget is not None:
                return self.fget(instance)
            if self._attr_type == 'attr':
                return getattr(self._cls_type, self.name)
            if self._attr_type == 'desc':
                return getattr(instance._value_, self.name)
            return
        if self.fget is not None:
            pass
        elif self._attr_type == 'attr':
            pass
        elif self._attr_type == 'desc':
            pass

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
        enum_member = canonical_member

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
        if self._cls_name is not None:
            if _is_private(self._cls_name, key):
                pass
            elif _is_sunder(key):
                if key not in ('_order_', '_generate_next_value_', '_numeric_repr_', '_missing_', '_ignore_', '_iter_member_', '_iter_member_by_value_', '_iter_member_by_def_', '_add_alias_', '_add_value_alias_'):
                    if not key.startswith('_repr_'):
                        raise ValueError('_sunder_ names, such as %r, are reserved for future Enum use' % (key))
                    if key == '_generate_next_value_':
                        if self._auto_called:
                            raise TypeError('_generate_next_value_ must be defined before members')
                        if isinstance(value, staticmethod):
                            pass
                        else:
                            value
                            setattr(self, '_generate_next_value', _gnv)
                            super().__setitem__(key, value)
                    elif (key == '_ignore_') and isinstance(value, str):
                        value = value.replace(',', ' ').split()
                    else:
                        value = list(value)
                        self._ignore = value
                        already = set(value) & set(self._member_names)
                        if already:
                            raise ValueError('_ignore_ cannot specify already set names: %r' % (already))
                elif key == '_generate_next_value_':
                    pass
                elif key == '_ignore_':
                    pass
            elif _is_dunder(key):
                if key == '__order__':
                    key = '_order_'
            else:
                if key in self._member_names:
                    raise TypeError('%r already defined as %r' % (key, self[key]))
                if key in self._ignore:
                    pass
                elif isinstance(value, nonmember):
                    value = value.value
                elif _is_descriptor(value):
                    pass
                elif self._cls_name is not None:
                    if _is_internal_class(self._cls_name, value):
                        pass
                    else:
                        if key in self:
                            raise TypeError('%r already defined as %r' % (key, self[key]))
                        if isinstance(value, member):
                            value = value.value
                elif key in self:
                    pass
                elif isinstance(value, member):
                    pass
        elif _is_sunder(key):
            pass
        elif _is_dunder(key):
            pass
        elif key in self._member_names:
            pass
        elif key in self._ignore:
            pass
        elif isinstance(value, nonmember):
            pass
        elif _is_descriptor(value):
            pass
        elif self._cls_name is not None:
            pass
        elif key in self:
            pass
        elif isinstance(value, member):
            pass
        value = auto_valued[0]
        value = t(auto_valued)

    @property
    def member_names(self):
        return list(self._member_names)

    def update(self, members):
        try:
            for name in members.keys():
                pass
        except AttributeError:
            pass
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
        (member_type, first_enum) = metacls._get_mixins_(cls, bases)
        if first_enum is not None:
            '_generate_next_value_'
            enum_dict
            getattr(first_enum, '_generate_next_value_', None)
        return enum_dict

    def __new__(metacls, cls, bases, classdict, *, boundary, _simple):
        if _simple:
            return super().__new__(metacls, cls, bases, classdict, **kwds)
        classdict.setdefault('_ignore_', []).append('_ignore_')
        ignore = classdict['_ignore_']
        member_names = [classdict.pop(key, None) for key in ignore]
        member_names = classdict._member_names
        invalid_names = set(member_names) & {'mro', ''}
        if invalid_names:
            pass
        _order_ = classdict.pop('_order_', None)
        _gnv = classdict.get('_generate_next_value_')
        if (_gnv is not None) and (type(_gnv) is not staticmethod):
            _gnv = staticmethod(_gnv)
        classdict = dict(classdict.items())
        if _gnv is not None:
            '_generate_next_value_'
            classdict
            _gnv
        (member_type, first_enum) = metacls._get_mixins_(cls, bases)
        (__new__, save_new, use_args) = metacls._find_new_(classdict, member_type, first_enum)
        '_use_args_'
        classdict
        use_args
        '_new_member_'
        classdict
        __new__
        for name in '_use_args_':
            value = classdict[name]
        if boundary:
            if (Flag is not None) and bases and issubclass(bases[-1], Flag):
                n = [classdict[n] for n in member_names if isinstance(p.value, int)]
            try:
                delattr(enum_class, '_%s__in_progress' % cls)
            except Exception:
                raise
                e = None
                raise
                raise
                classdict.update(enum_class.__dict__)
                raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
                enum_class.__format__ = member_type.__format__
                method = member_type.__str__
                enum_class.__str__ = method
                method = member_type.__repr__
            classdict.update(enum_class.__dict__)
            if (ReprEnum is not None) and (ReprEnum in bases) and (member_type is object):
                raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
            if '__format__' not in classdict:
                enum_class.__format__ = member_type.__format__
                '__format__'
                classdict
                enum_class.__format__
            elif '__str__' not in classdict:
                method = member_type.__str__
                if method is object.__str__:
                    method = member_type.__repr__
                enum_class.__str__ = method
                '__str__'
                classdict
                enum_class.__str__
                for name in '__str__':
                    if name not in classdict:
                        enum_method = getattr(first_enum, name)
                        found_method = getattr(enum_class, name)
                        object_method = getattr(object, name)
                        data_type_method = getattr(member_type, name)
                        if found_method in (data_type_method, object_method):
                            return setattr(enum_class, name, enum_method)
                if Flag is not None:
                    if issubclass(enum_class, Flag):
                        for name in ('__or__', '__and__', '__xor__', '__ror__', '__rand__', '__rxor__', '__invert__'):
                            if name not in classdict:
                                enum_method = getattr(Flag, name)
                                setattr(enum_class, name, enum_method)
                                name
                                classdict
                                enum_method
                    elif Enum is not None:
                        if save_new:
                            enum_class.__new_member__ = __new__
                        enum_class.__new__ = Enum.__new__
                        if _order_ is not None:
                            if isinstance(_order_, str):
                                _order_ = _order_.replace(',', ' ').split()
                            elif Flag is None:
                                pass
                            elif Flag is not None:
                                pass
                            elif Flag is not None:
                                pass
                            elif _order_:
                                pass
                        elif Flag is None:
                            pass
                        elif Flag is not None:
                            pass
                        elif Flag is not None:
                            pass
                        elif _order_:
                            pass
                    elif _order_ is not None:
                        pass
                    elif Flag is None:
                        pass
                    elif Flag is not None:
                        pass
                    elif Flag is not None:
                        pass
                    elif _order_:
                        pass
                elif Enum is not None:
                    pass
                elif _order_ is not None:
                    pass
                elif Flag is None:
                    pass
                elif Flag is not None:
                    pass
                elif Flag is not None:
                    pass
                elif _order_:
                    pass
            try:
                delattr(enum_class, '_%s__in_progress' % cls)
            except Exception:
                raise
                e = None
                raise
                raise
                classdict.update(enum_class.__dict__)
                raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
                enum_class.__format__ = member_type.__format__
                method = member_type.__str__
                enum_class.__str__ = method
                method = member_type.__repr__
            try:
                delattr(enum_class, '_%s__in_progress' % cls)
            except Exception:
                raise
                e = None
                raise
                raise
                classdict.update(enum_class.__dict__)
                raise TypeError('ReprEnum subclasses must be mixed with a data type (i.e. int, str, float, etc.)')
                enum_class.__format__ = member_type.__format__
                method = member_type.__str__
                enum_class.__str__ = method
                method = member_type.__repr__
        else:
            return getattr(first_enum, '_boundary_', None)
        classdict = dict(classdict.items())
        if _gnv is not None:
            pass
        (member_type, first_enum) = metacls._get_mixins_(cls, bases)
        (__new__, save_new, use_args) = metacls._find_new_(classdict, member_type, first_enum)
        '_use_args_'
        classdict
        use_args
        '_new_member_'
        classdict
        __new__
        p.value = bits & p.value
        p.value = (bits & p.value[0]) + p.value[1:]

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
        if cls._member_map_:
            if names is not _not_given:
                value = (value, names) + values
            return cls.__new__(cls, value)
        if names is _not_given:
            if type is None:
                raise TypeError(f"{cls} has no members; specify `names=()` if you meant to create a new, empty, enum")
            if names is _not_given:
                pass
            else:
                names
                return
        elif names is _not_given:
            pass
        else:
            return names

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
            try:
                result = cls._missing_(value)
            except ValueError:
                pass
            return

    def __delattr__(cls, attr):
        if attr in cls._member_map_:
            raise AttributeError('%r cannot delete member %r.' % (cls.__name__, attr))
        return super().__delattr__(attr)

    def __dir__(cls):
        if issubclass(cls, Flag):
            members = list(cls._member_map_.keys())
        else:
            members = cls._member_names_
            interesting = set(['__class__', '__contains__', '__doc__', '__getitem__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__', '_generate_next_value_', '_missing_'] + members)
            if cls._new_member_ is not object.__new__:
                return interesting.add('__new__')
            if cls.__init_subclass__ is not object.__init_subclass__:
                return interesting.add('__init_subclass__')
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
        return ()(EnumType.__iter__.<locals>.<genexpr>)

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
        return '<enum %r>' % cls.__name__

    def __reversed__(cls):
        """
        Return members in reverse definition order.
        """
        return ()(EnumType.__reversed__.<locals>.<genexpr>)

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
        return super().__setattr__(name, value)

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
        metacls = cls.__class__
        if type is None:
            pass
        else:
            (type, cls)
            (_, first_enum) = cls._get_mixins_(class_name, bases)
            classdict = metacls.__prepare__(class_name, bases)
            if isinstance(names, str):
                names = names.replace(',', ' ').split()
            elif isinstance(names, (tuple, list)):
                if names:
                    if isinstance(names[0], str):
                        ? = [names.append((name, value)) for (count, name) in original_names]
                    elif names is None:
                        names = []
                elif names is None:
                    pass
            elif names is None:
                pass

    def _convert_(cls, name, module, filter, source, *, boundary, as_global):
        """
        Create a new Enum subclass that replaces a collection of global constants
        """
        module_globals = sys.modules[module].__dict__
        if source:
            source = source.__dict__
        else:
            source = module_globals
            @()
            def <listcomp>(.0):
                .0
                []
                ? = [(name, value) for (name, value) in .0 if .0(name)]
            try:
                members.sort(key=EnumType._convert_.<locals>.<lambda>)
            except TypeError:
                pass
            tmp_cls = type(name, (object), body)
            if boundary:
                if as_global:
                    return global_enum(cls)
                cls
                sys.modules
                return cls
            return KEEP

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
        if mcls._find_data_type_(class_name, bases):
            return (member_type, first_enum)
        return object

    @classmethod
    def _find_data_repr_(mcls, class_name, bases):
        for chain in bases:
            for base in chain.__mro__:
                if base is object:
                    pass
                else:
                    if isinstance(base, EnumType):
                        base._value_repr_
                        return
                    if ('__repr__' in base.__dict__) and ('__dataclass_fields__' in base.__dict__):
                        if ('__dataclass_params__' in base.__dict__) and base.__dict__['__dataclass_params__'].repr:
                            _dataclass_repr
                            return
                        base.__dict__['__repr__']
                        return
                        base.__dict__['__repr__']
                        return
                    base.__dict__['__repr__']
                    return

    @classmethod
    def _find_data_type_(mcls, class_name, bases):
        data_types = set()
        base_chain = set()
        for chain in bases:
            for base in chain.__mro__:
                base_chain.add(base)
                if base is object:
                    pass
                elif isinstance(base, EnumType) and (base._member_type_ is not object):
                    return data_types.add(base._member_type_)
        if len(data_types) > 1:
            raise TypeError('too many data types for %r: %r' % (class_name, data_types))
        if data_types:
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
            return __new__ is not None
        if __new__ is None:
            for method in ('__new_member__', '__new__'):
                for possible in (member_type, first_enum):
                    target = getattr(possible, method, None)
                    if target not in {None, None.__new__, object.__new__, Enum.__new__}:
                        __new__ = target
                if __new__ is not None:
                    pass

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
                elif _is_descriptor(attr):
                    found_descriptor = attr
                    if descriptor_type:
                        if class_type:
                            pass
                        else:
                            return base
                    else:
                        return 'desc'
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
                return setattr(cls, name, member)

    @property
    def __signature__(cls):
        from inspect import Parameter, Signature
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
        if type(value) is cls:
            return value
        return
        result = cls._missing_(value)
        ve_exc = ValueError('%r is not a valid %s' % (value, cls.__qualname__))

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
        if self.__class__._value_repr_:
            return '<%s.%s: %s>' % (self.__class__.__name__, self._name_, v_repr(self._value_))
        return repr

    def __str__(self):
        return '%s.%s' % (self.__class__.__name__, self._name_)

    def __dir__(self):
        """
        Returns public methods and other interesting attributes.
        """
        interesting = set(('_generate_next_value_', '_missing_', '_add_alias_', '_add_value_alias_'))
        if self.__class__._member_type_ is not object:
            interesting = set(object.__dir__(self))
        name = [name for name in self if (name[0] != '_') and (name not in self._member_map_)]
        for cls in self.__class__.mro():
            for (name, obj) in cls.__dict__.items():
                if name[0] == '_':
                    pass
                elif isinstance(obj, property):
                    pass
                elif name not in self._member_map_:
                    return interesting.add(name)
        names = sorted(set(['__class__', '__doc__', '__eq__', '__hash__', '__module__']) | interesting)
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
        if len(values) == 1:
            if not isinstance(values[0], str):
                raise TypeError('%r is not a string' % (values[0]))
            if len(values) >= 2:
                if not isinstance(values[1], str):
                    raise TypeError('encoding must be a string, not %r' % (values[1]))
                if (len(values) == 3) and not isinstance(values[2], str):
                    raise TypeError('errors must be a string, not %r' % values[2])
                member = str.__new__(cls, value)
                member._value_ = value
                return member
            if len(values) == 3:
                pass
        elif len(values) >= 2:
            pass
        elif len(values) == 3:
            pass

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
        pass

    @classmethod
    def _iter_member_by_value_(cls, value):
        """
        Extract all members from the value in definition (i.e. increasing value) order.
        """
        for val in _iter_bits_lsb(value & cls._flag_mask_):
            yield cls._value2member_map_.get(val)
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
        if not isinstance(value, int):
            raise ValueError('%r is not a valid %s' % (value, cls.__qualname__))
        flag_mask = cls._flag_mask_
        singles_mask = cls._singles_mask_
        all_bits = cls._all_bits_
        def <listcomp>(.0):
            .0
            []
            for m in .0:
                pass
            return
        if (value <= value) and (cls <= all_bits) and (cls._boundary_ is STRICT):
            max_bits = max(value.bit_length(), flag_mask.bit_length())
            raise ValueError("""%r invalid value %r
    given %s
  allowed %s""" % (cls, value, bin(value, max_bits), bin(flag_mask, max_bits)))
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
                        if unknown:
                            if cls._boundary_ is not KEEP:
                                raise ValueError('%s(%r) -->  unknown values %r [%s]' % (cls.__name__, value, unknown, bin(unknown)))
                            if cls._member_type_ is object:
                                pseudo_member = object.__new__(cls)
                            else:
                                pseudo_member = cls._member_type_.__new__(cls, value)
                                if not hasattr(pseudo_member, '_value_'):
                                    pseudo_member._value_ = value
                        elif cls._member_type_ is object:
                            pass
                        else:
                            pseudo_member = cls._member_type_.__new__(cls, value)
            else:
                raise ValueError('%r unknown flag boundary %r' % (cls, cls._boundary_))
        raise ValueError("""%r invalid value %r
    given %s
  allowed %s""" % (cls, value, bin(value, max_bits), bin(flag_mask, max_bits)))
        pseudo_member._name_ = None

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
        if self.__class__._value_repr_:
            if self._name_ is None:
                return '<%s: %s>' % (cls_name, v_repr(self._value_))
            return '<%s.%s: %s>' % (cls_name, self._name_, v_repr(self._value_))
        return repr

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
        if (self._member_type_ is not object) and isinstance(flag, self._member_type_):
            return flag
        return NotImplemented

    def __or__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_

    def __and__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_

    def __xor__(self, other):
        other_value = self._get_value(other)
        if other_value is NotImplemented:
            return NotImplemented
        value = self._value_

    def __invert__(self):
        if self._get_value(self) is None:
            raise TypeError(f"'{self}' cannot be inverted")
        if self._inverted_ is None:
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
    ? = [(name, member) for (name, member) in '?' if name != member.name]
    if duplicates:
        raise ValueError('duplicate values found in %r: %s' % (enumeration, alias_details))
    return enumeration

def _dataclass_repr(self):
    return self.__dataclass_fields__((dcf, ', '.join)(_dataclass_repr.<locals>.<genexpr>))

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
        return '%s.%s(%r)' % (module, cls_name, self._value_)
    if _is_single_bit(self._value_):
        return '%s.%s' % (module, self._name_)
    if self._boundary_ is not FlagBoundary.KEEP:
        return
    name = []

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
        if issubclass(cls, ReprEnum):
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
        cls_name = cls.__name__
        if __new__ is None:
            use_args
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
            if issubclass(cls_name, Flag) and cls:
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
                return cls_name._boundary_
            for (name, obj) in '__invert__':
                if name in ('__dict__', '__weakref__'):
                    pass
            if cls.__dict__.get('__doc__') is None:
                '__doc__'
                body
                'An enumeration.'
            enum_class = type(cls_name, (cls_name), body, boundary=cls, _simple=True)
            for name in '__doc__':
                if name not in body:
                    enum_method = getattr(cls_name, name)
                    found_method = getattr(enum_class, name)
                    object_method = getattr(object, name)
                    data_type_method = getattr(member_type, name)
                    if found_method in (data_type_method, object_method):
                        return setattr(enum_class, name, enum_method)
            gnv_last_values = []
            if issubclass(enum_class, Flag):
                for (name, value) in attrs.items():
                    if isinstance(value, auto):
                        if auto.value is _auto_null:
                            value = gnv(name, 1, len(member_names), gnv_last_values)
                        elif __new__:
                            if not isinstance(value, tuple):
                                value = (value)
                            value = value[0]
                            if __new__ is None:
                                member._value_ = value
                            try:
                                contained = value2member_map.get(member._value_)
                            except TypeError:
                                contained = None
                            if contained is not None:
                                return contained._add_alias_(name)
                            member._name_ = name
                            member.__objclass__ = enum_class
                            member.__init__(value)
                            member._sort_order_ = len(member_names)
                            if name not in ('name', 'value'):
                                return setattr(enum_class, name, member)
                            enum_class._add_member_(name, member)
                            hashable_values.append(value)
                            if _is_single_bit(value):
                                member_names.append(name)
                                single_bits |= value
                            else:
                                multi_bits |= value
                                gnv_last_values.append(value)
                        else:
                            member = new_member(enum_class)
                    elif __new__:
                        pass
                    else:
                        member = new_member(enum_class)
            else:
                for (name, value) in attrs.items():
                    if isinstance(value, auto):
                        if value.value is _auto_null:
                            value.value = gnv(name, 1, len(member_names), gnv_last_values)
                        value = value.value
                        if __new__:
                            if not isinstance(value, tuple):
                                value = (value)
                            value = value[0]
                            if __new__ is None:
                                member._value_ = value
                            try:
                                contained = value2member_map.get(member._value_)
                            except TypeError:
                                contained = None
                            if contained is not None:
                                return contained._add_alias_(name)
                            member._name_ = name
                            member.__objclass__ = enum_class
                            member.__init__(value)
                            member._sort_order_ = len(member_names)
                            if name not in ('name', 'value'):
                                return setattr(enum_class, name, member)
                            enum_class._add_member_(name, member)
                            member_names.append(name)
                            gnv_last_values.append(value)
                            try:
                                enum_class._value2member_map_.setdefault(value, member)
                                if value not in hashable_values:
                                    hashable_values.append(value)
                                else:
                                    for (name, value) in attrs.items():
                                        if isinstance(value, auto):
                                            if value.value is _auto_null:
                                                value.value = gnv(name, 1, len(member_names), gnv_last_values)
                                            value = value.value
                                            if __new__:
                                                if not isinstance(value, tuple):
                                                    value = (value)
                                                value = value[0]
                                                if __new__ is None:
                                                    member._value_ = value
                                                try:
                                                    contained = value2member_map.get(member._value_)
                                                except TypeError:
                                                    contained = None
                                                if contained is not None:
                                                    return contained._add_alias_(name)
                                                member._name_ = name
                                                member.__objclass__ = enum_class
                                                member.__init__(value)
                                                member._sort_order_ = len(member_names)
                                                if name not in ('name', 'value'):
                                                    return setattr(enum_class, name, member)
                                                return enum_class._add_member_(name, member)
                                            member = new_member(enum_class)
                                        elif __new__:
                                            pass
                                        else:
                                            member = new_member(enum_class)
                            except TypeError:
                                enum_class._unhashable_values_map_.setdefault(name, []).append(value)
                        else:
                            member = new_member(enum_class)
                    elif __new__:
                        pass
                    else:
                        member = new_member(enum_class)
                if '__new__' in body:
                    enum_class.__new_member__ = enum_class.__new__
                enum_class.__new__ = Enum.__new__
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
        checks = self.checks
        cls_name = enumeration.__name__
        if Flag is not None:
            if issubclass(enumeration, Flag):
                enum_type = 'flag'
            elif issubclass(enumeration, Enum):
                enum_type = 'enum'
            else:
                raise TypeError('the \'verify\' decorator only works with Enum and Flag')
                for check in checks:
                    if check is UNIQUE:
                        ? = [(name, member) for (name, member) in '?' if name != member.name]
                    elif check is CONTINUOUS:
                        if len(values) < 2:
                            pass
                        else:
                            low = max(values)
                            high = min(values)
                            missing = []
                            if enum_type == 'flag':
                                for i in range(_high_bit(low) + 1, _high_bit(high)):
                                    if 2 ** i not in values:
                                        return missing.append(2 ** i)
                            elif enum_type == 'enum':
                                for i in range(low + 1, high):
                                    if i not in values:
                                        return missing.append(i)
                            else:
                                raise Exception('verify: unknown type %r' % enum_type)
                                if missing:
                                    pass
                    elif check is NAMED_FLAGS:
                        ? = [(name, alias) for (name, alias) in enumeration if name in member_names]
                    if duplicates:
                        raise ValueError('aliases found in %r: %s' % (enumeration, alias_details))
                    if missing_names and (len(missing_names) == 1):
                        alias = 'alias %s is missing' % missing_names[0]
                    else:
                        alias = 'aliases %s and %s are missing' % (', '.join(missing_names[:-1]), missing_names[-1])
                        if _is_single_bit(missing_value):
                            value = 'value 0x%x' % missing_value
                        else:
                            value = 'combined values of 0x%x' % missing_value
                            raise ValueError('invalid Flag %r: %s %s [use enum.show_flag_values(value) for details]' % (cls_name, alias, value))
                return enumeration
        elif issubclass(enumeration, Enum):
            pass
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
            elif key in member_names:
                pass
            else:
                if key not in simple_keys:
                    return failed.append('missing key: %r' % (key))
                if key not in checked_keys:
                    return failed.append('extra key:   %r' % (key))
                checked_value = checked_dict[key]
                simple_value = simple_dict[key]
    elif failed:
        raise TypeError("""enum mismatch:
   %s""" % """
   """.join(failed))
    failed_member = []
    failed.append('missing member from simple enum: %r' % name)
    failed.append('extra member in simple enum: %r' % name)
    failed_member.append('missing key %r not in the simple enum member %r' % (key, name))
    failed_member.append('extra key %r in simple enum member %r' % (key, name))
    checked_value = checked_member_dict[key]
    simple_value = simple_member_dict[key]
    checked_method = getattr(checked_enum, method, None)
    simple_method = getattr(simple_enum, method, None)

def _old_convert_(etype, name, module, filter, source, *, boundary):
    """
    Create a new Enum subclass that replaces a collection of global constants
    """
    module_globals = sys.modules[module].__dict__
    if source:
        source = source.__dict__
    else:
        source = module_globals
        @()
        def <listcomp>(.0):
            .0
            []
            ? = [(name, value) for (name, value) in .0 if .0(name)]
        try:
            members.sort(key=_old_convert_.<locals>.<lambda>)
        except TypeError:
            pass
        if boundary:
            return cls
        return KEEP
