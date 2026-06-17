# Decompiled from: <module>

name_0 = 'Minimal 3.5 test'
import name_1
import name_2
name_5 = name_2.name_3.name_4('~/.pyenv/versions/3.5.10/bin/python')
name_6 = name_2.name_3.name_4('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
name_8 = None([name_5, '-c', 'import py_compile; py_compile.compile(\'/tmp/t1.py\', cfile=\'/tmp/t1.35.pyc\', doraise=True)'], True, True, ('capture_output', 'text', 'timeout'))
name_9 = None(['dotnet', 'run', '--project', name_2.name_3.name_4('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', '/tmp/t1.35.pyc'], True, True, ('capture_output', 'text', 'timeout'))
None('STDOUT:', name_9.name_11 + None)
None(None, name_9.name_12 + None)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 76 instr
