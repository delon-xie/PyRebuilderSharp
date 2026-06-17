# Decompiled from: <module>

'Check Python 2.7 .pyc format'
import os
import subprocess
result = os.subprocess.expanduser([os.subprocess('~/.pyenv/versions/2.7.18/bin/python'), '-c', 'import py_compile; py_compile.compile(\'/tmp/test_py27.py\', cfile=\'/tmp/test_py27.pyc\', doraise=True)'], True, True)
print('Compile result:', result.path, result.path)
data = open('/tmp/test_py27.pyc', 'rb')()
print('Length:', len(data))
' '.join(' ', <genexpr>(data()))
result2 = os.subprocess.expanduser([os.subprocess('~/.pyenv/versions/2.7.18/bin/python'), '-c', 'import imp; m = imp.get_magic(); print(\' \'.join(\'{:02x}\'.format(ord(b)) for b in m))'], True, True)
'Python 2.7 magic:'(result2.path.strip, result2.path())
result3 = os.subprocess.expanduser([os.subprocess('~/.pyenv/versions/2.7.18/bin/python'), '-c', """
import marshal, dis
code = marshal.loads(open('/tmp/test_py27.pyc', 'rb').read()[8:])
print('Code type:', type(code))
print('co_argcount:', code.co_argcount)
print('co_nlocals:', code.co_nlocals)
print('co_stacksize:', code.co_stacksize)
print('co_flags:', code.co_flags)
print('co_code:', repr(code.co_code))
print('co_consts:', repr(code.co_consts))
print('co_names:', repr(code.co_names))
print('co_varnames:', repr(code.co_varnames))
print('co_filename:', repr(code.co_filename))
print('co_name:', repr(code.co_name))
print('co_firstlineno:', code.co_firstlineno)
dis.disassemble(code)
     """], True, True)
print('Marshal dump:', result3.path)
name_19 = result3.path
print('Stderr:', result3.path)
return None
return None
# [SUMMARY] 2 blocks · 3 processed · 0 orphan · 146 instr
