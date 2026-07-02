# Decompiled from: <module>

def SyntaxWarningTest():
    """SyntaxWarningTest"""
    def check_warning(self, code, errtext, filename, mode):
        """Check that compiling code raises SyntaxWarning with errtext.

    errtest is a regular expression that must be present in the
    text of the warning raised.
"""
        yield
        yield
        try:
            None
            __special_5__
            None
        finally:
            None
        code
        None
        None
        None
    def test_return_in_finally(self):
        """
            def f():
                try:
                    pass
                finally:
                    return 42
            """
        return deref_2
    def test_break_and_continue_in_finally(self):
        """break"""
        import name_147 as dedent
        return source
    deref_1 = var_6
    var_5
    **var_4
    **var_4
    **var_4
    **var_4
    **var_4
    **var_4
    **var_4
    **var_4
    *var_4
    *var_4
    *var_4
    *var_4
    *var_4
    *var_4
    ****var_0
    ****var_0
    ****var_0
    ****var_0
    ****var_0
    ****var_0
    ***var_0
    ***var_0
    ***var_0
    ***var_0
    **var_0
    **var_0
    **var_0
    *__classdict__
    *__classdict__
    *super().__name__

def SyntaxErrorTestCase():
    """SyntaxErrorTestCase"""
    def _check_error(self, code, errtext, filename, mode, subclass, lineno, offset, end_lineno, end_offset):
        """Check that compiling code raises SyntaxError with errtext.

    errtest is a regular expression that must be present in the
    text of the exception raised.  If subclass is specified it
    is the expected subclass of SyntaxError (e.g. IndentationError).
"""
        try:
            None
            __module__
        except:
            pass
        filename
        None
        code
        filename
    def test_expression_with_assignment(self):
        """print(end1 + end2 = ' ')"""
        var_2
        None
        var_0 not in var_1
        self
        deref_1
    def test_curly_brace_after_primary_raises_immediately(self):
        """f{}"""
        var_3
        None
        var_1 not in var_2
        var_0
        self
        deref_1
    def test_assign_call(self):
        """f() = 1"""
        var_1
        None
        var_0
        self
        deref_1
    def test_assign_del(self):
        """del (,)"""
        var_35
        None
        var_0
        var_34
        deref_1
        None
        var_33
        var_32
        deref_1
        None
        var_23
        var_31
        deref_1
        None
        var_23
        var_30
        deref_1
        None
        var_23
        var_29
        deref_1
        None
        var_23
        var_28
        deref_1
        None
        var_23
        var_27
        deref_1
        None
        var_23
        var_26
        deref_1
        None
        var_23
        var_25
        deref_1
        None
        var_23
        var_24
        deref_1
        None
        var_23
        var_22
        deref_1
        None
        var_21
        var_20
        deref_1
        None
        var_13
        var_19
        deref_1
        None
        var_13
        var_18
        deref_1
        None
        var_13
        var_17
        deref_1
        None
        var_13
        var_16
        deref_1
        None
        var_13
        var_15
        deref_1
        None
        var_13
        var_14
        deref_1
        None
        var_13
        var_12
        deref_1
        None
        var_7
        var_11
        deref_1
        None
        var_7
        var_10
        deref_1
        None
        var_9
        var_8
        deref_1
        None
        var_7
        var_6
        deref_1
        None
        var_5
        var_4
        deref_1
        None
        var_2
        var_3
        deref_1
        None
        var_2
        var_1
        deref_1
        None
        var_0
        self
        deref_1
    def test_global_param_err_first(self):
        """if 1:
            def error(a):
                global a  # SyntaxError
            def error2():
                b = 1
                global b  # SyntaxError
            """
        name_1 = self
        var_1
        None
        source not in var_0
        source
    def test_nonlocal_param_err_first(self):
        """if 1:
            def error(a):
                nonlocal a  # SyntaxError
            def error2():
                b = 1
                global b  # SyntaxError
            """
        name_1 = self
        var_1
        None
        source not in var_0
        source
    def test_raise_from_error_message(self):
        """if 1:
        raise AssertionError() from None
        print(1,,2)
        """
        name_1 = self
        var_1
        None
        source not in var_0
        source
    def test_yield_outside_function(self):
        """if 0: yield"""
        var_9
        None
        var_0
        var_8
        deref_1
        None
        var_0
        var_7
        deref_1
        None
        var_0
        var_6
        deref_1
        None
        var_0
        var_5
        deref_1
        None
        var_0
        var_4
        deref_1
        None
        var_0
        var_3
        deref_1
        None
        var_0
        var_2
        deref_1
        None
        var_0
        var_1
        deref_1
        None
        var_0
        self
        deref_1
    def test_return_outside_function(self):
        """if 0: return"""
        var_9
        None
        var_0
        var_8
        deref_1
        None
        var_0
        var_7
        deref_1
        None
        var_0
        var_6
        deref_1
        None
        var_0
        var_5
        deref_1
        None
        var_0
        var_4
        deref_1
        None
        var_0
        var_3
        deref_1
        None
        var_0
        var_2
        deref_1
        None
        var_0
        var_1
        deref_1
        None
        var_0
        self
        deref_1
    def test_break_outside_loop(self):
        """outside loop"""
        name_1 = self
        var_7
        None
        var_6 not in var_0
        msg
        None
        var_5 not in var_0
        msg
        None
        var_4 not in var_0
        msg
        None
        var_3 not in var_0
        msg
        None
        var_2 not in var_0
        msg
        None
        var_1 not in var_0
        msg
        None
        msg not in var_0
        msg
    def test_continue_outside_loop(self):
        """not properly in loop"""
        name_1 = self
        var_6
        None
        var_5 not in var_0
        msg
        None
        var_4 not in var_0
        msg
        None
        var_3 not in var_0
        msg
        None
        var_2 not in var_0
        msg
        None
        var_1 not in var_0
        msg
        None
        msg not in var_0
        msg
    def test_unexpected_indent(self):
        """foo()
 bar()
"""
        var_2
        None
        __qualname__ not in var_1
        var_0
        self
        deref_1
    def test_no_indent(self):
        """if 1:
    foo()"""
        var_2
        None
        __qualname__ not in var_1
        var_0
        self
        deref_1
    def test_bad_outdent(self):
        """if 1:
  foo()
 bar()"""
        var_2
        None
        __qualname__ not in var_1
        var_0
        self
        deref_1
    def test_kwargs_last(self):
        """int(base=10, '2')"""
        var_1
        None
        var_0
        self
        deref_1
    def test_kwargs_last2(self):
        """int(**{'base': 10}, '2')"""
        var_1
        None
        var_0
        self
        deref_1
    def test_kwargs_last3(self):
        """int(**{'base': 10}, *['2'])"""
        var_1
        None
        var_0
        self
        deref_1
    def test_generator_in_function_call(self):
        """foo(x,    y for y in range(3) for z in range(2) if z    , p)"""
        var_2
        None
        var_0 not in var_1
        self
        deref_1
    def test_except_then_except_star(self):
        """try: pass
    except ValueError: pass
    except* TypeError: pass"""
        var_2
        None
        var_0 not in var_1
        self
        deref_1
    def test_except_star_then_except(self):
        """try: pass
    except* ValueError: pass
    except TypeError: pass"""
        var_2
        None
        var_0 not in var_1
        self
        deref_1
    def test_empty_line_after_linecont(self):
        """\
    pass
        \

    pass
"""
        SyntaxError = self
        try:
            None
            s1
            s
            __module__
        except:
            pass
        fail = var_0
        name_3 = var_1
        None
        s1
        s
        __module__
        None
        s1
        s
        __module__
        var_3
    def test_continuation_bad_indentation(self):
        """\
    if x:
    y = 1
  \
  foo = 1
        """
        IndentationError = self
        code
        None
        __special_4__
        __qualname__
        code
    def test_disallowed_type_param_names(self):
        """class A[__classdict__]: pass"""
        import name_21 as compile
        var_7
        var_4
        name(__special_3__, var_2, var_3)
        var_1
        name
        None
        name
        var_0
        name
        None
        name
        self
        name
    def test_nested_named_except_blocks(self):
        """"""
        _check_error = self
        import name_67 as name_2
        _check_error = [[code](i)]
        _check_error = [[code, []](var_0)]
        _check_error = [[code](var_1)]
        _check_error = [var_5(var_2)]
        var_4
        None
        var_3
        deref_3
    def test_with_statement_many_context_managers(self):
        def get_code(n):
            """
                def bug():
                    with (
                    a
                """
            return i
        _check_error = []
        import name_60 as name_4
        yield
        yield
        try:
            return __special_5__
            import name_65 as name_4
            yield n
            yield None
            try:
                return deref_7
                n
                n
                n
                None
                var_1
                None
                None
            finally:
                None
            None
            None
        finally:
            None
            None
            None
    def test_async_with_statement_many_context_managers(self):
        def get_code(n):
            """
                async def bug():
                    async with (
                    a
                """
            return i
        _check_error = []
        import name_60 as join
        yield
        yield
        try:
            return __special_5__
            import name_65 as join
            yield n
            yield None
            try:
                return deref_7
                n
                n
                n
                None
                var_1
                None
                None
            finally:
                None
            None
            None
        finally:
            None
            None
            None
    def test_barry_as_flufl_with_syntax_errors(self):
        """
    def func1():
    if a != b:
        raise ValueError

    def func2():
    try
        return 1
    finally:
        pass
"""
        name_1 = self
        var_0
        None
        code
        code
    def test_invalid_line_continuation_error_position(self):
        """a = 3 \ 4"""
        var_4
        None
        var_0 not in var_1
        var_3
        deref_1
        None
        var_0 not in var_1
        var_2
        deref_1
        None
        var_0 not in var_1
        self
        deref_1
    def test_invalid_line_continuation_left_recursive(self):
        """A.Ɗ\ """
        var_3
        None
        var_2
        var_1
        deref_1
        None
        var_0
        self
        deref_1
    def test_error_parenthesis(self):
        """([{"""
        import name_32 as name_1
        import name_29 as name_1
        import name_32 as name_1
        name_2 = var_5
        name_3 = var_9
        var_11
        None
        var_10
        paren
        None
        var_8
        var_7
        paren
        None
        var_6
        paren
        paren
    def test_error_string_literal(self):
        """'blech"""
        var_8
        None
        var_6
        var_7
        deref_1
        None
        var_6
        var_5
        deref_1
        None
        var_3
        var_4
        deref_1
        None
        var_3
        var_2
        deref_1
        None
        var_0
        var_1
        deref_1
        None
        var_0
        self
        deref_1
    def test_invisible_characters(self):
        """print("Hello")"""
        var_2
        None
        var_0
        var_1
        deref_1
        None
        var_0
        self
        deref_1
    def test_match_call_does_not_raise_syntax_error(self):
        """
    def match(x):
    return 1+1

    match(34)
"""
        name_1 = self
        var_1
        None
        var_0
        code
        __module__
    def test_case_call_does_not_raise_syntax_error(self):
        """
    def case(x):
    return 1+1

    case(34)
"""
        name_1 = self
        var_1
        None
        var_0
        code
        __module__
    def test_multiline_compiler_error_points_to_the_end(self):
        """call(
    a=1,
    a=1
    )"""
        var_2
        None
        var_0 not in var_1
        self
        deref_1
    def test_multiline_string_concat_missing_comma_points_to_last_string(self):
        """print(
    "line1"
    "line2"
    "line3"
    x=1
    )"""
        var_2
        None
        var_0 not in var_1
        self
        deref_1
    def test_syntax_error_on_deeply_nested_blocks(self):
        """
    while 1:
 while 2:
  while 3:
   while 4:
    while 5:
     while 6:
      while 8:
       while 9:
        while 10:
         while 11:
          while 12:
           while 13:
            while 14:
             while 15:
              while 16:
               while 17:
                while 18:
                 while 19:
                  while 20:
                   while 21:
                    while 22:
                     while 23:
                      break
"""
        name_1 = self
        var_0
        None
        source
        source
    def test_error_on_parser_stack_overflow(self):
        """-"""
        assertRaisesRegex = []
        import name_90 as MemoryError
        yield
        yield
        try:
            yield None
            yield
        finally:
            None
        None
        None
    def test_deep_invalid_rule(self):
        """d{{{{{{{{{{{{{{{{{{{{{{{{{```{{{{{{{ef f():y"""
        SyntaxError = self
        yield
        yield
        try:
            None
            var_0
            source
            __special_5__
            None
        finally:
            None
        var_1
        None
        None
        None
    def test_except_stmt_invalid_as_expr(self):
        """
                try:
                    pass
                except ValueError as obj.attr:
                    pass
                """
        return deref_4
    def test_match_stmt_invalid_as_expr(self):
        """
                match 1:
                    case x as obj.attr:
                        ...
                """
        return deref_4
    def test_ifexp_else_stmt(self):
        """expected expression after 'else', but statement is given"""
        name_1 = self
        import name_24 as name_2
        stmt
    def test_ifexp_body_stmt_else_expression(self):
        """expected expression before 'if', but statement is given"""
        name_1 = self
        import name_25 as name_2
        var_0
    def test_ifexp_body_stmt_else_stmt(self):
        """expected expression before 'if', but statement is given"""
        name_1 = self
        raise
    deref_1 = var_48
    return deref_90

def LazyImportRestrictionTestCase():
    """LazyImportRestrictionTestCase"""
    def test_lazy_import_in_try_block(self):
        """Test that lazy imports are not allowed inside try blocks."""
        var_4
        None
        var_3
        var_2
        deref_1
        None
        var_1
        var_0
        deref_1
    def test_lazy_import_in_trystar_block(self):
        """Test that lazy imports are not allowed inside try* blocks."""
        var_4
        None
        var_3
        var_2
        deref_1
        None
        var_1
        var_0
        deref_1
    def test_lazy_import_in_except_block(self):
        """Test that lazy imports are not allowed inside except blocks."""
        var_2
        None
        var_1
        var_0
        deref_1
    def test_lazy_import_in_function(self):
        """Test that lazy imports are not allowed inside functions."""
        var_4
        None
        var_3
        var_2
        deref_1
        None
        var_1
        var_0
        deref_1
    def test_lazy_import_in_async_function(self):
        """Test that lazy imports are not allowed inside async functions."""
        var_4
        None
        var_3
        var_2
        deref_1
        None
        var_1
        var_0
        deref_1
    def test_lazy_import_in_class(self):
        """Test that lazy imports are not allowed inside classes."""
        var_4
        None
        var_3
        var_2
        deref_1
        None
        var_1
        var_0
        deref_1
    def test_lazy_import_star_forbidden(self):
        """Test that 'lazy from ... import *' is forbidden everywhere."""
        var_4
        None
        var_3
        var_2
        deref_1
        None
        var_1
        var_0
        deref_1
    def test_lazy_import_nested_scopes(self):
        """Test lazy imports in nested scopes."""
        var_6
        None
        var_5
        var_4
        deref_1
        None
        var_3
        var_2
        deref_1
        None
        var_1
        var_0
        deref_1
    def test_lazy_import_valid_cases(self):
        """Test that lazy imports work at module level."""
        var_6
        None
        var_2
        var_1
        var_5
        __module__
        None
        var_2
        var_1
        var_4
        __module__
        None
        var_2
        var_1
        var_3
        __module__
        None
        var_2
        var_1
        var_0
        __module__
    var_12
    **var_11
    **var_11
    **var_11
    **var_11
    **var_11
    **var_11
    **var_11
    **var_11
    **var_11
    **var_11
    **var_11
    **var_11
    **var_11
    **var_11
    **var_11
    *var_11
    *var_11
    *var_11
    *var_11
    *var_11
    *var_11
    *var_11
    *var_11
    *var_11
    *var_11
    *var_11
    *var_11
    *var_11
    **********var_1
    **********var_1
    **********var_1
    **********var_1
    **********var_1
    **********var_1
    **********var_1
    **********var_1
    **********var_1
    **********var_1
    **********var_1
    **********var_1
    **********var_1
    *********var_1
    *********var_1
    *********var_1
    *********var_1
    *********var_1
    *********var_1
    *********var_1
    *********var_1
    *********var_1
    *********var_1
    *********var_1
    ********var_1
    ********var_1
    ********var_1
    ********var_1
    ********var_1
    ********var_1
    ********var_1
    ********var_1
    ********var_1
    ********var_1
    *******var_1
    *******var_1
    *******var_1
    *******var_1
    *******var_1
    *******var_1
    *******var_1
    *******var_1
    *******var_1
    ******var_1
    ******var_1
    ******var_1
    ******var_1
    ******var_1
    ******var_1
    ******var_1
    ******var_1
    *****var_1
    *****var_1
    *****var_1
    *****var_1
    *****var_1
    *****var_1
    *****var_1
    ****var_1
    ****var_1
    ****var_1
    ****var_1
    ****var_1
    ****var_1
    ***var_1
    ***var_1
    ***var_1
    ***var_1
    ***var_1
    **var_1
    **var_1
    **var_1
    **var_1
    *var_1
    *var_1
    *var_1
    *var_0
    *__classdict__
    *__classdict__
    *super().__name__

def load_tests(loader, tests, pattern):
    return deref_4
var_1
*var_1
*var_1
*var_1
*var_1
*var_1
*var_1
return lambda : None
