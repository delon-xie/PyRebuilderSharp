# Decompiled from: <module>

name_0 = 'Run AST comparison for test_control_flow across all versions'
import name_1
import name_2
import name_3
name_6 = name_1.name_4.name_5('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
name_7 = name_1.name_4.name_5('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
name_8 = name_1.name_4.name_5('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
name_12 = name_10.name_11()
name_10 := None(name_8)()(None, None, None)
name_15 = name_3.name_14(None(name_12), ('indent',))
name_16 = None
for _ in name_21:
    name_19 = name_1.name_4.name_18(name_7, 'test_control_flow.%s.pyc' % name_17)
    if not name_1.name_4.name_20(name_19):
        None('⏭ %s: no pyc' % name_17)
    else:
        name_23 = None(['dotnet', 'run', '--project', name_6, '--', name_19], True, True, ('capture_output', 'text', 'timeout'))
        name_25 = name_3.name_14(None(name_23.name_24), ('indent',))
        name_26 = name_15 == name_25
    if name_26:
        pass
    break
    if not name_26:
        for _ in name_27(name_28(name_15.name_29("""
"""), name_25.name_29("""
"""))):
            if not name_31 == name_32:
                pass
            else:
                None(f"  Line {name_30}: expected={name_31}
           actual=  {name_32}")
                name_21
return None
if not True:
    pass
raise
if name_33:
    None(f"❌ {name_17}: parse error: {name_34}")
    None('  Output: %s' % (name_23.name_24 + None))
    name_34 = None
    name_34 = None
raise
# [SUMMARY] 24 blocks · 25 processed · 0 orphan · 263 instr
