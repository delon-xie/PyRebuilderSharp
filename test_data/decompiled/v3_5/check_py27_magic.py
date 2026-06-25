# Decompiled from: <module>

"""Check Python 2.7 .pyc format"""
import os
import subprocess
print('Compile result:', result.stdout, result.stderr)
data = open('/tmp/test_py27.pyc', 'rb').read()
print('Length:', len(data))
print('Python 2.7 magic:', result2.stdout.strip())
print('Marshal dump:', result3.stdout)
if result3.stderr:
    return print('Stderr:', result3.stderr)
