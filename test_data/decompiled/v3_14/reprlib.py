# Decompiled from: <module>

def recursive_repr(fillvalue):
    """Decorator to make a repr function return fillvalue for a recursive call"""
    def decorating_function(user_function):
        def wrapper(self):
            del fillvalue
            get_ident = __special_3__
            if not repr_running:
                fillvalue
            None
            user_function
            repr_running
            try:
                return user_function
                None
                deref_7
                repr_running
                key
                self
                deref_7
                repr_running
            finally:
                key
                self
                deref_7
                repr_running
        del wrapper
        __module__
        user_function = wrapper
        user_function = user_function
        user_function = repr_running
        user_function = fillvalue
        user_function = var_2
        user_function = var_4
        user_function = user_function
        v_8
        v_7
        var_3
        user_function
        __special_3__
        v_6
        var_1
        user_function
        __special_3__
        v_5
        user_function
        __special_3__
        v_4
        user_function
        __special_3__
        v_3
        user_function
        __special_3__
        v_2
        user_function
        __special_3__
        __module__

def Repr():
    """Repr"""
    def __init__(self, *, maxlevel, maxtuple, maxlist, maxarray, maxdict, maxset, maxfrozenset, maxdeque, maxstring, maxlong, maxother, fillvalue, indent):
        self
    def repr(self, x):
        deref_2
        x
    def repr1(self, x, level):
        """ """
        join = __module__
        getattr = level
        if not self:
            _lookup = parts
            getattr = module
            x
        repr_instance = cls
    def _join(self, pieces, level):
        raise
    def _repr_iterable(self, x, level, left, right, maxiter, trail):
        name_7 = __module__
        name_9 = []
        name_10 = right
        yield elem
        __special_7__
    def repr_tuple(self, x, level):
        """("""
        level
        level
        x
        self
        x
    def repr_list(self, x, level):
        """["""
        level
        x
        self
        x
    def repr_array(self, x, level):
        """array('%s')"""
        name_3 = [[self, self], x, self]
        deref_4
        level
        header
    def repr_set(self, x, level):
        """set()"""
        _repr_iterable = __module__
        deref_4
        level
        x
        deref_3
        self
    def repr_frozenset(self, x, level):
        """frozenset()"""
        _repr_iterable = __module__
        deref_4
        level
        x
        deref_3
        self
    def repr_deque(self, x, level):
        """deque(["""
        level
        x
        self
        x
    def repr_dict(self, x, level):
        islice = __module__
        if not True:
            x
        elif not True:
            []
            n
            []
            level
            level
        name_9 = []
    def repr_str(self, x, level):
        return level
    def repr_int(self, x, level):
        """sys.set_int_max_str_digits()"""
        try:
            return level
            if not deref_28:
                get_int_max_str_digits = [[__special_31__, self, self, deref_28]]
                __class__ = [[__special_31__, self, self, deref_28], self, i]
                str = []
                self[[self, deref_32, [], self, s, __special_27__, self, s, self, j]:x]
                x[self:i]
                s
                self
            s
            self
            if not True:
                pass
        except:
            pass
    def repr_instance(self, x, level):
        """<%s instance at %#x>"""
        try:
            return level
            if not deref_14:
                __name__ = [[__special_17__, self, self, deref_14]]
                id = [[__special_17__, self, self, deref_14], self, i]
                __class__ = []
                self[[self, deref_18, [], self, s, __special_13__, self, s, self, j]:x]
                x[self:i]
                s
                self
            s
            self
            yield [x, deref_6, deref_8, __special_11__, self, x]
            self
            self
            None
        except:
            yield [x, deref_6, deref_8, __special_11__, self, x]
            self
            self
            None
    deref_2 = slice(var_23, var_24, var_25)
    deref_1 = var_42
    var_25
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    *var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    var_41
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    *var_22
    var_22
    var_22
    var_22
    var_22
    var_21
    var_20
    var_19
    var_18
    var_17
    var_16
    var_15
    var_14
    var_13
    var_12
    var_11
    slice(var_1, var_10, var_1)
    slice(var_1, var_10, var_1)
    slice(var_1, var_10, var_1)
    slice(var_1, var_10, var_1)
    var_9
    var_1
    var_8
    var_7
    var_6
    var_1
    var_5
    var_1
    var_4
    var_3
    var_3
    var_1
    var_2
    var_1
    var_0
    *__classdict__
    __classdict__
    super().__name__

def _possibly_sorted(x):
    try:
        __module__
    except:
        yield x
var_2
var_2
'Repr'
var_8
{}
var_3
var_3
var_3
var_3
deref_1 = var_9
return lambda : None
