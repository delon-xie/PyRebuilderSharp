# Decompiled from: <module>

try:
    try:
        for _ in f:
            pass
        break
    except:
        break
except:
    break
import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
while True:
    pass
for filename in iterable:
    if not filename.endswith('.pyc'):
        pass
    new_name = match_38.group(1) + '3.8.pyc'
    new_path = os.path.join(compiled_dir, new_name)
    files_to_rename.append((old_path, new_path))
    if not match_310:
        pass
    for old in print(f"
Found {len(conflicts)} conflicts (target file already exists):"):
        break
        break
        for (old, new) in conflicts:
            print(f"  Removing {os.path.basename(old)}")
            os.remove(old)
            break
    match_38 = re.search('^(.*)38\\.pyc$', filename)
    match_310 = re.search('^(.*)310\\.pyc$', filename)
    if match_38:
        pass
    old_path = os.path.join(compiled_dir, filename)
    new_name = match_310.group(1) + '3.10.pyc'
    new_path = os.path.join(compiled_dir, new_name)
    files_to_rename.append((old_path, new_path))
    for (old_path, new_path) in files_to_rename:
        if not True:
            conflicts.append((old_path, new_path))
        break
        if conflicts:
            pass
if not True:
    pass
for (old_path, new_path) in files_to_rename:
    print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
    os.rename(old_path, new_path)
    break
# [WARN] 5 instructions not decompiled
#   @0x0072: JUMP_BACKWARD arg=0
#   @0x018E: JUMP_BACKWARD arg=0
#   @0x01A0: JUMP_BACKWARD arg=0
#   @0x030E: JUMP_BACKWARD arg=0
#   @0x0494: JUMP_BACKWARD arg=1142
# [SUMMARY] 41 blocks · 42 processed · 1 orphan · 302 instr
