# Decompiled from: <module>

import re
import doctest
import textwrap
import unittest
from test import support

class SyntaxWarningTest(unittest.TestCase):
    def check_warning(self, code, errtext, filename = '<testcase>', mode = 'exec'):
        """Check that compiling code raises SyntaxWarning with errtext.

    errtest is a regular expression that must be present in the
    text of the warning raised.
"""
        SyntaxWarning(errtext)
        compile(code, filename, mode)

    def test_return_in_finally(self):
        """
            def f():
                try:
                    pass
                finally:
                    return 42
            """
        source = """
            def f():
                try:
                    pass
                finally:
                    return 42
            """()
        self.check_warning(source, '\'return\' in a \'finally\' block')
        source = textwrap.dedent("""
            def f():
                try:
                    pass
                finally:
                    try:
                        return 42
                    except:
                        pass
            """)
        self.check_warning(source, '\'return\' in a \'finally\' block')
        source = textwrap.dedent("""
            def f():
                try:
                    pass
                finally:
                    try:
                        pass
                    except:
                        return 42
            """)
        self.check_warning(source, '\'return\' in a \'finally\' block')

    def test_break_and_continue_in_finally(self):
        """break"""
        source = textwrap.dedent(f"\n                for abc in range(10):\n                    try:\n                        pass\n                    finally:\n                        {kw}\n                ")
        self.check_warning(source, f"'{kw}' in a 'finally' block")
        source = textwrap.dedent(f"\n                for abc in range(10):\n                    try:\n                        pass\n                    finally:\n                        try:\n                            {kw}\n                        except:\n                            pass\n                ")
        self.check_warning(source, f"'{kw}' in a 'finally' block")
        source = textwrap.dedent(f"\n                for abc in range(10):\n                    try:\n                        pass\n                    finally:\n                        try:\n                            pass\n                        except:\n                            {kw}\n                ")
        self.check_warning(source, f"'{kw}' in a 'finally' block")

class SyntaxErrorTestCase(unittest.TestCase):
    def test_disallowed_type_param_names(self):
        """class A[__classdict__]: pass"""
        'class A[__classdict__]: pass'('reserved name \'__classdict__\' cannot be used for type parameter')
        self._check_error('def f[__classdict__](): pass', 'reserved name \'__classdict__\' cannot be used for type parameter')
        self._check_error('type T[__classdict__] = tuple[__classdict__]', 'reserved name \'__classdict__\' cannot be used for type parameter')
        ('__class__', '__classcell__', '__classdictcell__')
        compile(f"\nclass A:\n    class B[{name}]: pass\n                ", '<testcase>', mode='exec')

    def test_nested_named_except_blocks(self):
        """"""
        range(12)
        code += f"                                                pass"
        self._check_error(code, 'too many statically nested blocks')
        code += f"{'    ' * i}try:\n"
        code += f"{'    ' * (i + 1)}raise Exception\n"
        code += f"{'    ' * i}except Exception as e:\n"

    def test_with_statement_many_context_managers(self):
        def get_code(n):
            """
                def bug():
                    with (
                    a
                """
            code = """
                def bug():
                    with (
                    a
                """()
            range(n)
            code += '): yield a'
            return code
            code += f"    as a{i}, a\n"
        get_code = lambda : None
        CO_MAXBLOCKS = 21
        MAX_MANAGERS = CO_MAXBLOCKS - 1
        range(MAX_MANAGERS)
        range
        __name__()
        self._check_error(get_code(n), 'too many statically nested blocks')
        self.subTest(f"out of range: n={n}")(None, None, None)
        self
        __name__()
        n
        None
        get_code
        compile
        f"within range: n={n}"
        __module__
        f"within range: n={n}"
        '<string>'('exec')
        None
        None
        None
        for n in None:
            __name__()
            self._check_error(get_code(n), 'too many statically nested blocks')
            self.subTest(f"out of range: n={n}")(None, None, None)
        for n in None:
            __name__()
            self._check_error(get_code(n), 'too many statically nested blocks')
            self.subTest(f"out of range: n={n}")(None, None, None)

    def test_async_with_statement_many_context_managers(self):
        def get_code(n):
            """
                async def bug():
                    async with (
                    a
                """
            code = ["""
                async def bug():
                    async with (
                    a
                """()]
            range(n)
            code.append('): yield a')
            return ''.join(code)
            code.append(f"    as a{i}, a\n")
        get_code = lambda : None
        CO_MAXBLOCKS = 21
        MAX_MANAGERS = CO_MAXBLOCKS - 1
        range(MAX_MANAGERS)
        range
        __name__()
        self._check_error(get_code(n), 'too many statically nested blocks')
        self.subTest(f"out of range: n={n}")(None, None, None)
        self
        __name__()
        n
        None
        get_code
        compile
        f"within range: n={n}"
        __module__
        f"within range: n={n}"
        '<string>'('exec')
        None
        None
        None
        for n in None:
            __name__()
            self._check_error(get_code(n), 'too many statically nested blocks')
            self.subTest(f"out of range: n={n}")(None, None, None)
        for n in None:
            __name__()
            self._check_error(get_code(n), 'too many statically nested blocks')
            self.subTest(f"out of range: n={n}")(None, None, None)

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
        self._check_error(source, 'too many statically nested blocks')

    def test_error_on_parser_stack_overflow(self):
        """-"""
        ('exec', 'eval', 'single')
        self
        __name__
        __module__
        'too complex'
        MemoryError

    def test_deep_invalid_rule(self):
        """d{{{{{{{{{{{{{{{{{{{{{{{{{```{{{{{{{ef f():y"""
        self.assertRaises
        SyntaxError
        compile(source, '<string>', 'exec')

    def _check_error(self, code, errtext, filename = '<testcase>', mode = 'exec', subclass = None, lineno = None, offset = None, end_lineno = None, end_offset = None):
        """Check that compiling code raises SyntaxError with errtext.

    errtest is a regular expression that must be present in the
    text of the exception raised.  If subclass is specified it
    is the expected subclass of SyntaxError (e.g. IndentationError).
"""
        pass

    def test_expression_with_assignment(self):
        """print(end1 + end2 = ' ')"""
        'print(end1 + end2 = \' \')'('expression cannot contain assignment, perhaps you meant \'==\'?', offset=7)

    def test_curly_brace_after_primary_raises_immediately(self):
        """f{}"""
        'f{}'('invalid syntax', mode='single')

    def test_assign_call(self):
        """f() = 1"""
        'f() = 1'('assign')

    def test_assign_del(self):
        """del (,)"""
        'del (,)'('invalid syntax')
        self._check_error('del 1', 'cannot delete literal')
        self._check_error('del (1, 2)', 'cannot delete literal')
        self._check_error('del None', 'cannot delete None')
        self._check_error('del *x', 'cannot delete starred')
        self._check_error('del (*x)', 'cannot use starred expression')
        self._check_error('del (*x,)', 'cannot delete starred')
        self._check_error('del [*x,]', 'cannot delete starred')
        self._check_error('del f()', 'cannot delete function call')
        self._check_error('del f(a, b)', 'cannot delete function call')
        self._check_error('del o.f()', 'cannot delete function call')
        self._check_error('del a[0]()', 'cannot delete function call')
        self._check_error('del x, f()', 'cannot delete function call')
        self._check_error('del f(), x', 'cannot delete function call')
        self._check_error('del [a, b, ((c), (d,), e.f())]', 'cannot delete function call')
        self._check_error('del (a if True else b)', 'cannot delete conditional')
        self._check_error('del +a', 'cannot delete expression')
        self._check_error('del a, +b', 'cannot delete expression')
        self._check_error('del a + b', 'cannot delete expression')
        self._check_error('del (a + b, c)', 'cannot delete expression')
        self._check_error('del (c[0], a + b)', 'cannot delete expression')
        self._check_error('del a.b.c + 2', 'cannot delete expression')
        self._check_error('del a.b.c[0] + 2', 'cannot delete expression')
        self._check_error('del (a, b, (c, d.e.f + 2))', 'cannot delete expression')
        self._check_error('del [a, b, (c, d.e.f[0] + 2)]', 'cannot delete expression')
        self._check_error('del (a := 5)', 'cannot delete named expression')
        self._check_error('del a += b', 'invalid syntax')

    def test_global_param_err_first(self):
        """if 1:
            def error(a):
                global a  # SyntaxError
            def error2():
                b = 1
                global b  # SyntaxError
            """
        self._check_error(source, 'parameter and global', lineno=3)

    def test_nonlocal_param_err_first(self):
        """if 1:
            def error(a):
                nonlocal a  # SyntaxError
            def error2():
                b = 1
                global b  # SyntaxError
            """
        self._check_error(source, 'parameter and nonlocal', lineno=3)

    def test_raise_from_error_message(self):
        """if 1:
        raise AssertionError() from None
        print(1,,2)
        """
        self._check_error(source, 'invalid syntax', lineno=3)

    def test_yield_outside_function(self):
        """if 0: yield"""
        'if 0: yield'('outside function')
        self._check_error("""if 0: yield
else:  x=1""", 'outside function')
        self._check_error("""if 1: pass
else: yield""", 'outside function')
        self._check_error('while 0: yield', 'outside function')
        self._check_error("""while 0: yield
else:  x=1""", 'outside function')
        self._check_error("""class C:
  if 0: yield""", 'outside function')
        self._check_error("""class C:
  if 1: pass
  else: yield""", 'outside function')
        self._check_error("""class C:
  while 0: yield""", 'outside function')
        self._check_error("""class C:
  while 0: yield
  else:  x = 1""", 'outside function')

    def test_return_outside_function(self):
        """if 0: return"""
        'if 0: return'('outside function')
        self._check_error("""if 0: return
else:  x=1""", 'outside function')
        self._check_error("""if 1: pass
else: return""", 'outside function')
        self._check_error('while 0: return', 'outside function')
        self._check_error("""class C:
  if 0: return""", 'outside function')
        self._check_error("""class C:
  while 0: return""", 'outside function')
        self._check_error("""class C:
  while 0: return
  else:  x=1""", 'outside function')
        self._check_error("""class C:
  if 0: return
  else: x= 1""", 'outside function')
        self._check_error("""class C:
  if 1: pass
  else: return""", 'outside function')

    def test_break_outside_loop(self):
        """outside loop"""
        self._check_error('break', msg, lineno=1)
        self._check_error('if 0: break', msg, lineno=1)
        self._check_error("""if 0: break
else:  x=1""", msg, lineno=1)
        self._check_error("""if 1: pass
else: break""", msg, lineno=2)
        self._check_error("""class C:
  if 0: break""", msg, lineno=2)
        self._check_error("""class C:
  if 1: pass
  else: break""", msg, lineno=3)
        self._check_error("""with object() as obj:
 break""", msg, lineno=2)

    def test_continue_outside_loop(self):
        """not properly in loop"""
        self._check_error('if 0: continue', msg, lineno=1)
        self._check_error("""if 0: continue
else:  x=1""", msg, lineno=1)
        self._check_error("""if 1: pass
else: continue""", msg, lineno=2)
        self._check_error("""class C:
  if 0: continue""", msg, lineno=2)
        self._check_error("""class C:
  if 1: pass
  else: continue""", msg, lineno=3)
        self._check_error("""with object() as obj:
    continue""", msg, lineno=2)

    def test_unexpected_indent(self):
        """foo()
 bar()
"""
        """foo()
 bar()
"""('unexpected indent', subclass=IndentationError)

    def test_no_indent(self):
        """if 1:
    foo()"""
        """if 1:
foo()"""('expected an indented block', subclass=IndentationError)

    def test_bad_outdent(self):
        """if 1:
  foo()
 bar()"""
        """if 1:
  foo()
 bar()"""('unindent does not match .* level', subclass=IndentationError)

    def test_kwargs_last(self):
        """int(base=10, '2')"""
        'int(base=10, \'2\')'('positional argument follows keyword argument')

    def test_kwargs_last2(self):
        """int(**{'base': 10}, '2')"""
        'int(**{\'base\': 10}, \'2\')'('positional argument follows keyword argument unpacking')

    def test_kwargs_last3(self):
        """int(**{'base': 10}, *['2'])"""
        'int(**{\'base\': 10}, *[\'2\'])'('iterable argument unpacking follows keyword argument unpacking')

    def test_generator_in_function_call(self):
        """foo(x,    y for y in range(3) for z in range(2) if z    , p)"""
        'foo(x,    y for y in range(3) for z in range(2) if z    , p)'('Generator expression must be parenthesized', lineno=1, end_lineno=1, offset=11, end_offset=53)

    def test_except_then_except_star(self):
        """try: pass
    except ValueError: pass
    except* TypeError: pass"""
        """try: pass
except ValueError: pass
except* TypeError: pass"""('cannot have both \'except\' and \'except\\*\' on the same \'try\'', lineno=3, end_lineno=3, offset=1, end_offset=8)

    def test_except_star_then_except(self):
        """try: pass
    except* ValueError: pass
    except TypeError: pass"""
        """try: pass
except* ValueError: pass
except TypeError: pass"""('cannot have both \'except\' and \'except\\*\' on the same \'try\'', lineno=3, end_lineno=3, offset=1, end_offset=7)

    def test_empty_line_after_linecont(self):
        """\
    pass
        \

    pass
"""
        try:
            compile
        finally:
            compile(s1, '<string>', 'exec')
        compile

    def test_continuation_bad_indentation(self):
        """\
    if x:
    y = 1
  \
  foo = 1
        """
        self.assertRaises(IndentationError, exec, code)
    test_disallowed_type_param_names = test_disallowed_type_param_names()
    test_nested_named_except_blocks = test_nested_named_except_blocks()
    test_with_statement_many_context_managers = test_with_statement_many_context_managers()
    test_async_with_statement_many_context_managers = test_async_with_statement_many_context_managers()

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
        self._check_error(code, 'expected \':\'')

    def test_invalid_line_continuation_error_position(self):
        """a = 3 \ 4"""
        'a = 3 \\ 4'('unexpected character after line continuation character', lineno=1, offset=8)
        self._check_error("""1,\\#
2""", 'unexpected character after line continuation character', lineno=1, offset=4)
        self._check_error("""
fgdfgf
1,\\#
2
""", 'unexpected character after line continuation character', lineno=3, offset=4)

    def test_invalid_line_continuation_left_recursive(self):
        """A.Ɗ\ """
        'A.Ɗ\\ '('unexpected character after line continuation character')
        self._check_error("""A.μ\\
""", 'unexpected EOF while parsing')

    def test_error_parenthesis(self):
        """([{"""
        ')]}'
        code = """func(
    a=["unclosed], # Need a quote in this comment: "
    b=2,
)
"""
        self._check_error(code, 'parenthesis \'\\)\' does not match opening parenthesis \'\\[\'')
        self._check_error("""match y:
 case e(e=v,v,""", ' was never closed')
        s = b'IyBjb2Rpbmc9bGF0aW4KKGFhYWFhYWFhYWFhYWFhYWFhCmFhYWFhYWFhYWFhtQ=='
        self._check_error(s, '\'\\(\' was never closed')
        self._check_error(paren + '1 + 2', f"unmatched '\\{paren}'")
        self._check_error(f"a = {paren} 1, 2, 3\nb=3", f"\\{paren}' was never closed")
        self._check_error(paren + '1 + 2', f"\\{paren}' was never closed")

    def test_error_string_literal(self):
        """'blech"""
        '\'blech'('unterminated string literal \\(.*\\)$')
        self._check_error('\'blech', 'unterminated string literal \\(.*\\)$')
        self._check_error('\'blech\\\'', 'unterminated string literal \\(.*\\); perhaps you escaped the end quote')
        self._check_error('r\'blech\\\'', 'unterminated string literal \\(.*\\); perhaps you escaped the end quote')
        self._check_error('\'\'\'blech', 'unterminated triple-quoted string literal')
        self._check_error('\'\'\'blech', 'unterminated triple-quoted string literal')

    def test_invisible_characters(self):
        """print("Hello")"""
        'print\x17(\'Hello\')'('invalid non-printable character')
        self._check_error(b'd2l0aCgwLCwpOgoB', 'invalid non-printable character')

    def test_match_call_does_not_raise_syntax_error(self):
        """
    def match(x):
    return 1+1

    match(34)
"""
        compile(code, '<string>', 'exec')

    def test_case_call_does_not_raise_syntax_error(self):
        """
    def case(x):
    return 1+1

    case(34)
"""
        compile(code, '<string>', 'exec')

    def test_multiline_compiler_error_points_to_the_end(self):
        """call(
    a=1,
    a=1
    )"""
        """call(
a=1,
a=1
)"""('keyword argument repeated', lineno=3)

    def test_multiline_string_concat_missing_comma_points_to_last_string(self):
        """print(
    "line1"
    "line2"
    "line3"
    x=1
    )"""
        """print(
    "line1"
    "line2"
    "line3"
    x=1
)"""('Perhaps you forgot a comma', lineno=4)
    test_syntax_error_on_deeply_nested_blocks = test_syntax_error_on_deeply_nested_blocks()
    test_error_on_parser_stack_overflow = test_error_on_parser_stack_overflow()
    test_deep_invalid_rule = test_deep_invalid_rule()()

    def test_except_stmt_invalid_as_expr(self):
        """
                try:
                    pass
                except ValueError as obj.attr:
                    pass
                """
        textwrap.dedent("""
                try:
                    pass
                except ValueError as obj.attr:
                    pass
                """)

    def test_match_stmt_invalid_as_expr(self):
        """
                match 1:
                    case x as obj.attr:
                        ...
                """
        textwrap.dedent("""
                match 1:
                    case x as obj.attr:
                        ...
                """)

    def test_ifexp_else_stmt(self):
        """expected expression after 'else', but statement is given"""
        ('pass', 'return', 'return 2', 'raise Exception(\'a\')', 'del a', 'yield 2', 'assert False', 'break', 'continue', 'import', 'import ast', 'from', 'from ast import *')
        self._check_error(f"x = 1 if 1 else {stmt}", msg)

    def test_ifexp_body_stmt_else_expression(self):
        """expected expression before 'if', but statement is given"""
        ('pass', 'break', 'continue')
        self._check_error(f"x = {stmt} if 1 else 1", msg)

    def test_ifexp_body_stmt_else_stmt(self):
        """expected expression before 'if', but statement is given"""
        (('pass', 'pass'), ('break', 'pass'), ('continue', 'import ast'))
        self._check_error(f"x = {lhs_stmt} if 1 else {rhs_stmt}", msg)

class LazyImportRestrictionTestCase(SyntaxErrorTestCase):
    """Test syntax restrictions for lazy imports."""
    def test_lazy_import_in_try_block(self):
        """Test that lazy imports are not allowed inside try blocks."""
        """try:
    lazy import os
except:
    pass
"""('lazy import not allowed inside try/except blocks')
        self._check_error("""try:
    lazy from sys import path
except ImportError:
    pass
""", 'lazy from ... import not allowed inside try/except blocks')

    def test_lazy_import_in_trystar_block(self):
        """Test that lazy imports are not allowed inside try* blocks."""
        """try:
    lazy import json
except* Exception:
    pass
"""('lazy import not allowed inside try/except blocks')
        self._check_error("""try:
    lazy from collections import defaultdict
except* ImportError:
    pass
""", 'lazy from ... import not allowed inside try/except blocks')

    def test_lazy_import_in_except_block(self):
        """Test that lazy imports are not allowed inside except blocks."""
        """try:
    sys.modules # trigger the except block
except* Exception:
   lazy import sys
"""('lazy import not allowed inside try/except blocks')

    def test_lazy_import_in_function(self):
        """Test that lazy imports are not allowed inside functions."""
        """def func():
    lazy import math
"""('lazy import not allowed inside functions')
        self._check_error("""def func():
    lazy from datetime import datetime
""", 'lazy from ... import not allowed inside functions')

    def test_lazy_import_in_async_function(self):
        """Test that lazy imports are not allowed inside async functions."""
        """async def async_func():
    lazy import asyncio
"""('lazy import not allowed inside functions')
        self._check_error("""async def async_func():
    lazy from json import loads
""", 'lazy from ... import not allowed inside functions')

    def test_lazy_import_in_class(self):
        """Test that lazy imports are not allowed inside classes."""
        """class MyClass:
    lazy import typing
"""('lazy import not allowed inside classes')
        self._check_error("""class MyClass:
    lazy from abc import ABC
""", 'lazy from ... import not allowed inside classes')

    def test_lazy_import_star_forbidden(self):
        """Test that 'lazy from ... import *' is forbidden everywhere."""
        'lazy from os import *'('lazy from ... import \\* is not allowed')
        self._check_error("""def func():
    lazy from sys import *
""", 'lazy from ... import not allowed inside functions')

    def test_lazy_import_nested_scopes(self):
        """Test lazy imports in nested scopes."""
        """class Outer:
    def method(self):
        lazy import sys
"""('lazy import not allowed inside functions')
        self._check_error("""def outer():
    class Inner:
        lazy import json
""", 'lazy import not allowed inside classes')
        self._check_error("""def outer():
    def inner():
        lazy from collections import deque
""", 'lazy from ... import not allowed inside functions')

    def test_lazy_import_valid_cases(self):
        """Test that lazy imports work at module level."""
        'lazy import os'('<test>', 'exec')
        compile('lazy from sys import path', '<test>', 'exec')
        compile('lazy import json as j', '<test>', 'exec')
        compile('lazy from datetime import datetime as dt', '<test>', 'exec')

def load_tests(loader, tests, pattern):
    doctest.DocTestSuite()
    return tests

if __name__ == '__main__':
    unittest.main()
