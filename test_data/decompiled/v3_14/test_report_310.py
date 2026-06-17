# Decompiled from: <module>

import re
import sub
name_3 = ['python3', 'tests/run_tests.py'](True, True, '/Users/admin/codes/Tools/PyRebuild/ref/pycdc', ('capture_output', 'text', 'cwd'))
name_6 = name_3.name_4.name_5("""
""")
None(None)
None('Python 3.10 版本测试报告')
None(None)
name_8 = name_7
name_9 = name_7
def remove_ansi(text):
    '\\x1b\\[[0-9;]*m'
    return re.sub(None, '\\x1b\\[[0-9;]*m', '')
name_11 = False
def remove_ansi(text):
    '\\x1b\\[[0-9;]*m'
    return re.sub(None, '\\x1b\\[[0-9;]*m', '')
for _ in name_6:
    name_14 = None(name_13)
    name_16 = name_14.name_15()
    if name_16.name_17('*** '):
        if name_10:
            if name_11:
                None(f"✗ {name_10}")
                name_9 = name_7 + name_9
            None(f"✓ {name_10}")
            name_11 = False
            if None in name_16:
                name_11 = True
    if not None in name_14:
        pass
    name_11 = True
    if not None in name_14:
        if not None in name_14:
            pass
if name_10:
    if name_11:
        None(f"✗ {name_10}")
        name_9 = name_7 + name_9
    None(f"✓ {name_10}")
    None(None)
    None(f"{None}{name_8}{None}{name_9}{None}")
    None(None)
# [SUMMARY] 26 blocks · 27 processed · 0 orphan · 215 instr
