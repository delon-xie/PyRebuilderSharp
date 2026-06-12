#!/usr/bin/env python3
"""Check 3.5 code object reading"""
import subprocess, os, struct

py35 = os.path.expanduser("~/.pyenv/versions/3.5.10/bin/python")

# Create minimal test
result = subprocess.run([py35, "-c",
    "import marshal, dis; c=compile('a=1','<t>','exec'); m=marshal.dumps(c); print(len(m)); print(' '.join('{:02x}'.format(b) for b in m))"],
    capture_output=True, text=True, timeout=10)

print("3.5 marshal:")
print(result.stdout.strip())

# Also check bytecode format
result2 = subprocess.run([py35, "-c",
    "import dis; c=compile('a=1','<t>','exec'); dis.dis(c); print('co_code:', ' '.join('{:02x}'.format(b) for b in c.co_code))"],
    capture_output=True, text=True, timeout=10)

print("\nDisassembly:")
print(result2.stdout.strip())

# Check instruction format: is it 2-byte or variable?
result3 = subprocess.run([py35, "-c",
    "import dis; c=compile('a=1','<t>','exec'); [print(i.offset, i.opname, i.arg) for i in dis.get_instructions(c)]"],
    capture_output=True, text=True, timeout=10)

print("\nInstructions:")
print(result3.stdout.strip())
