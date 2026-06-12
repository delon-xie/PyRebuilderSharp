#!/usr/bin/env python3
"""Check 3.5 marshal field alignment comprehensively"""
import subprocess, struct, os

py = os.path.expanduser("~/.pyenv/versions/3.5.10/bin/python")
r = subprocess.run([py, "-c", """
import marshal, struct
c = compile('a=1', '<t>', 'exec')
m = bytes(marshal.dumps(c))
print('c.co_argcount:', c.co_argcount)
print('c.co_nlocals:', c.co_nlocals)
print('c.co_stacksize:', c.co_stacksize)
print('c.co_flags:', hex(c.co_flags))
print('len(m):', len(m))
print('m:', ' '.join('{:02x}'.format(b) for b in m), end='')
"""], capture_output=True, text=True, timeout=10)

print(r.stdout)
