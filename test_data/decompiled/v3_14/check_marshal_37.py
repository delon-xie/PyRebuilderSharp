# Decompiled from: <module>

name_0 = 'Check marshal fields for 3.7 code object'
import name_1
import name_2
name_4 = None('a1 = None', '<test>', 'exec')
None('Python 3.7 says:')
'  argcount='(f"{name_4.name_6} nlocals={name_4.name_7} stacksize={name_4.name_8} flags={name_9}{None(name_4.name_10)}")
name_13 = name_2.name_12(None(name_4))
"""
Marshaled ("""(f"{name_14}{None(name_13)} bytes):")
' '.name_15(<genexpr>(name_13 + None()))
None(f"{None + name_13}{None}")
for _ in None:
    name_19 = None(None, name_13, name_17)
    if not name_1.name_18 + name_19 == name_4.name_6:
        pass
    if not True:
        pass
    else:
        None(f"{None}{name_17}{None}")
        break
return None
# [WARN] 3 instructions not decompiled
#   @0x01F2: JUMP_BACKWARD arg=98
#   @0x0226: JUMP_BACKWARD arg=150
#   @0x025A: JUMP_BACKWARD arg=202
# [SUMMARY] 10 blocks · 11 processed · 0 orphan · 199 instr
