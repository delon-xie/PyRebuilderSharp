# Decompiled from: <module>

'Check Python 2.7 .pyc format'
import os
import subprocess
result = subprocess.run([os.path.expanduser('~/.pyenv/versions/2.7.18/bin/python'), '-c', 'import py_compile; py_compile.compile(\'/tmp/test_py27.py\', cfile=\'/tmp/test_py27.pyc\', doraise=True)'], capture_output=True, text=True)
print('Compile result:', result.stdout, result.stderr)
data = open('/tmp/test_py27.pyc', 'rb').read()
print('Length:', len(data))
print('Full bytes:', ' '.join(<genexpr>(data)))
result2 = subprocess.run([os.path.expanduser('~/.pyenv/versions/2.7.18/bin/python'), '-c', 'import imp; m = imp.get_magic(); print(\' \'.join(\'{:02x}\'.format(ord(b)) for b in m))'], capture_output=True, text=True)
print('Python 2.7 magic:', result2.stdout.strip())
result3 = subprocess.run([os.path.expanduser('~/.pyenv/versions/2.7.18/bin/python'), '-c', """
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
     """], capture_output=True, text=True)
print('Marshal dump:', result3.stdout)
if result3.stderr:
    print('Stderr:', result3.stderr)
