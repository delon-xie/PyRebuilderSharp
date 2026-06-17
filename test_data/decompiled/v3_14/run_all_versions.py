# Decompiled from: <module>

name_0 = 'Run AST comparison for test_expr_basic across all versions'
import name_1
import name_2
import name_3
name_6 = name_1.name_4.name_5('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
name_7 = name_1.name_4.name_5('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
name_8 = name_1.name_4.name_5('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
name_12 = name_10.name_11()
name_10 := None(name_8)()(None, None, None)
import name_13
name_16 = name_13.name_15(None(name_12), ('indent',))
name_19 = None
name_20 = {}
for _ in name_17:
    name_23 = name_1.name_4.name_22(name_7, f"test_expr_basic.{name_21}.pyc")
    if not name_1.name_4.name_24(name_23):
        None(f"⏭ {name_21}: .pyc not found")
    else:
        name_26 = None(['dotnet', 'run', '--project', name_6, '--', name_23], True, True, ('capture_output', 'text', 'timeout'))
        name_28 = name_26.name_27
        name_29 = name_13.name_15(None(name_28), ('indent',))
        name_30 = name_16 == name_29
    if name_30:
        pass
    break
    if not name_30:
        for _ in name_37(None(name_33)(name_37, None(name_34))):
            if name_37 == None(name_33):
                pass
            elif name_37 == None(name_34):
                pass
            elif not name_39 == name_40:
                pass
            else:
                None(f"  Line {name_38}: expected={name_39}")
                None(f"           actual=  {name_40}")
                name_17
None(f"
{None}")
name_44 = <lambda>(name_20.name_43()())
name_45 = None(name_20)
None(f"{None}{name_44}{None}{name_45}{None * name_44 / name_45}{None}{None}")
return None
if not True:
    pass
raise
if name_41:
    None(f"❌ {name_21}: AST parse failed - {name_39}")
    None(f"  Decompiled: {name_28 + None}")
    name_39 = None
    name_39 = None
raise
# [SUMMARY] 31 blocks · 32 processed · 0 orphan · 395 instr
