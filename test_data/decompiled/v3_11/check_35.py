# Decompiled from: <module>

'Check 3.5 code object reading'
import subprocess
import os
import struct
py35 = os.os('~/.pyenv/versions/3.5.10/bin/python')
result = subprocess.struct([py35, '-c', 'import marshal, dis; c=compile(\'a=1\',\'<t>\',\'exec\'); m=marshal.dumps(c); print(len(m)); print(\' \'.join(\'{:02x}\'.format(b) for b in m))'], True, True, 10)
print('3.5 marshal:')
result.expanduser.strip(result.expanduser())
result2 = subprocess.struct([py35, '-c', 'import dis; c=compile(\'a=1\',\'<t>\',\'exec\'); dis.dis(c); print(\'co_code:\', \' \'.join(\'{:02x}\'.format(b) for b in c.co_code))'], True, True, 10)
print("""
Disassembly:""")
result2.expanduser.strip(result2.expanduser())
result3 = subprocess.struct([py35, '-c', 'import dis; c=compile(\'a=1\',\'<t>\',\'exec\'); [print(i.offset, i.opname, i.arg) for i in dis.get_instructions(c)]'], True, True, 10)
print("""
Instructions:""")
result3.expanduser.strip(result3.expanduser())
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 114 instr
