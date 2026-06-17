# Decompiled from: <module>

'Check 3.5 code object reading'
import subprocess
import os
import struct
py35 = os.path.expanduser('~/.pyenv/versions/3.5.10/bin/python')
result = None([py35, '-c', 'import marshal, dis; c=compile(\'a=1\',\'<t>\',\'exec\'); m=marshal.dumps(c); print(len(m)); print(\' \'.join(\'{:02x}\'.format(b) for b in m))'], True, True, ('capture_output', 'text', 'timeout'))
None('3.5 marshal:')
print(result.stdout.strip())
result2 = None([py35, '-c', 'import dis; c=compile(\'a=1\',\'<t>\',\'exec\'); dis.dis(c); print(\'co_code:\', \' \'.join(\'{:02x}\'.format(b) for b in c.co_code))'], True, True, ('capture_output', 'text', 'timeout'))
None("""
Disassembly:""")
print(result2.stdout.strip())
result3 = None([py35, '-c', 'import dis; c=compile(\'a=1\',\'<t>\',\'exec\'); [print(i.offset, i.opname, i.arg) for i in dis.get_instructions(c)]'], True, True, ('capture_output', 'text', 'timeout'))
None("""
Instructions:""")
print(result3.stdout.strip())
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 101 instr
