# Decompiled from: <module>

'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
import marshal
import struct
import sys
try:
    data = f.read()
pos = 16
raw = data[pos]
'pos '(f"{pos}: type=0x{raw}{'02X'}")
pos += 1
raw = data[pos]
'pos '(f"{pos}: consts type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
raw2 = data[pos]
pos += 1
t2 = raw2 & 127
flags = ''
