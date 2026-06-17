# Decompiled from: <module>

name_0 = 'Show actual decompiled output for 3.5, 3.6, 3.7'
import name_1
import name_2
name_5 = name_1.name_3.name_4('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
name_6 = name_1.name_3.name_4('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
for _ in name_12:
    name_9 = name_1.name_3.name_8(name_6, f"test_expr_basic.{name_7}.pyc")
    name_11 = None(['dotnet', 'run', '--project', name_5, '--', name_9], True, True, ('capture_output', 'text', 'timeout'))
    None(f"
=== {name_7} ===")
    if name_11.name_13:
        pass
    break
    if not name_11.name_14:
        pass
    else:
        None(f"{None}{name_11.name_14 + None}")
return None
# [WARN] 1 instructions not decompiled
#   @0x019A: JUMP_BACKWARD arg=280
# [SUMMARY] 9 blocks · 10 processed · 0 orphan · 100 instr
