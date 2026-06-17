# Decompiled from: <module>

name_0 = 'Run AST comparison for test_seq_clean across all versions'
import name_1
import name_2
import name_3
import name_4
name_7 = name_1.name_5.name_6('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
name_8 = name_1.name_5.name_6('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
name_9 = name_1.name_5.name_6('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
name_13 = name_11.name_12()
name_11 := None(name_9)()(None, None, None)
name_16 = name_3.name_15(None(name_13), ('indent',))
name_21 = None
name_22 = {}
for _ in name_19:
    name_25 = name_1.name_5.name_24(name_8, 'test_seq_clean.%s.pyc' % name_23)
    if not name_1.name_5.name_26(name_25):
        None('⏭ %s: .pyc not found' % name_23)
    else:
        name_28 = None(['dotnet', 'run', '--project', name_7, '--', name_25], True, True, ('capture_output', 'text', 'timeout'))
        name_30 = name_28.name_29
        name_31 = name_3.name_15(None(name_30), ('indent',))
        name_32 = name_16 == name_31
    if name_32:
        pass
    break
    if not name_32:
        for _ in name_39(None(name_35)(name_39, None(name_36))):
            if name_39 == None(name_35):
                pass
            elif name_39 == None(name_36):
                pass
            elif not name_18 == name_41:
                pass
            else:
                None('  Line %d: expected=%s' % (name_40, name_18))
                None('           actual=  %s' % name_41)
                name_19
name_44 = <lambda>(name_22.name_43()())
name_45 = None(name_22)
name_19(None % (None, name_44, name_45 * name_44 // name_45))
return None
if not True:
    pass
raise
if name_17:
    None('Failed to parse expected source:', name_18)
    name_4.name_20(None)
    name_18 = None
    name_18 = None
raise
if name_17:
    None(f"❌ {name_23}: AST parse failed - {name_18}")
    None('  Decompiled: %s' % (name_30 + None))
    name_18 = None
    name_18 = None
raise
# [SUMMARY] 33 blocks · 34 processed · 0 orphan · 386 instr
