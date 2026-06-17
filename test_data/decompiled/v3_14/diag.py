# Decompiled from: <module>

name_0 = 'Diagnose 3.7 decompilation - test module-level code'
import name_1
import name_2
name_5 = name_1.name_3.name_4('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
name_6 = name_1.name_3.name_4('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.7.pyc')
name_8 = None(['dotnet', 'run', '--project', name_5, '--', name_6], True, True, ('capture_output', 'text', 'timeout'))
None('STDOUT:', name_8.name_10)
None('STDERR:', name_8.name_11)
name_12 = name_1.name_3.name_4('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.5.pyc')
name_13 = None(['dotnet', 'run', '--project', name_5, '--', name_12], True, True, ('capture_output', 'text', 'timeout'))
None('3.5 STDOUT:', name_13.name_10 + None)
None(None, name_13.name_11 + None)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 95 instr
