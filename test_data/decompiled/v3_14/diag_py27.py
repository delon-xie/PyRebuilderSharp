# Decompiled from: <module>

name_0 = 'Diagnose Python 2.7 decompilation failures by stepping through analysis'
import name_1
import name_2
import name_3
import name_4
name_7 = name_1.name_5.name_6('~/.pyenv/versions/2.7.18/bin/python')
name_8 = '/tmp/py27_diag'
name_8(True, ('exist_ok',))
name_10 = {'expr_simple': """a = 1
b = 2
c = a + b
""", 'expr_func': """def foo():
    return 42
x = foo()
""", 'expr_bool': """x = True
y = False
z = x and y
w = x or y
""", 'expr_all': """# Complete expressions for 2.7
a = 1
b = True
c = None
d = 3.14
e = "hello"
f = x + y
g = x - y
h = x * y
i = x / y
j = -x
k = not x
l = x < y
m = x == y
n = x is y
o = func(x)
p = items[0]
q = items[1:10]
r = obj.attr
s = x if cond else y
"""}
for _ in name_24:
    name_15 = name_1.name_5.name_14(name_8, f"{name_12}.py")
    name_16 = name_1.name_5.name_14(name_8, f"{name_12}.27.pyc")
    name_17 = name_1.name_5.name_14(name_8, f"{name_12}.out.py")
    name_19.name_20(name_13)
    name_19 := None(name_15, 'w')()(None, None, None)
    name_22 = None([name_7, '-c', """import py_compile, sys
py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)""", name_15, name_16], True, True, ('capture_output', 'text', 'timeout'))
    name_23 = None(['dotnet', 'run', '--project', name_1.name_5.name_6('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', name_16, '-o', name_17], True, True, ('capture_output', 'text', 'timeout'))
    None(f"
{None}")
    None(f"Test: {name_12}")
    if not None(name_15, 'w'):
        break
    break
    if name_1.name_5.name_28(name_17):
        name_30 = name_19.name_29().name_26()
        name_19 := None(name_17)()(None, None, None)
        None(f"{name_31}{None(name_30)}{None}{name_30 + None}")
    else:
        None(f"{None}{name_23.name_27 + None}")
return None
if not True:
    pass
raise
if not True:
    pass
raise
# [WARN] 1 instructions not decompiled
#   @0x0470: JUMP_BACKWARD arg=952
# [SUMMARY] 13 blocks · 14 processed · 0 orphan · 284 instr
