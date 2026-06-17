# Decompiled from: <module>

'Check Python 2.7 .pyc format'
import os
import subprocess
print('Compile result:', result.stdout, result.stderr)
data = open('/tmp/test_py27.pyc', 'rb').read()
print('Length:', len(data))
print('Full bytes:', ' '.join(<genexpr>(data)))
print('Python 2.7 magic:', result2.stdout.strip())
print('Marshal dump:', result3.stdout)
if result3.stderr:
    print('Stderr:', result3.stderr)
# [SUMMARY] 3 blocks · 4 processed · 0 orphan · 118 instr
