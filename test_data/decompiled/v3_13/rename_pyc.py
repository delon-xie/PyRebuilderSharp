# Decompiled from: <module>

try:
    []
    for _ in []:
        try:
            try:
                []
            except:
                break
        except:
            break
        if not True:
            pass
    break
    print(f"
Renaming {len(files_to_rename)} files...")
    files_to_rename
    for (old_path, new_path) in files_to_rename:
        print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
        os.rename(old_path, new_path)
    break
except:
    break
import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
os.listdir(compiled_dir)
for filename in os.listdir(compiled_dir):
    if not filename.endswith('.pyc'):
        pass
    else:
        match_38 = re.search('^(.*)38\\.pyc$', filename)
        match_310 = re.search('^(.*)310\\.pyc$', filename)
    if not match_310:
        pass
    else:
        old_path = os.path.join(compiled_dir, filename)
        new_name = match_310.group(1) + '3.10.pyc'
        new_path = os.path.join(compiled_dir, new_name)
        files_to_rename.append((old_path, new_path))
    old_path = os.path.join(compiled_dir, filename)
    new_name = match_38.group(1) + '3.8.pyc'
    new_path = os.path.join(compiled_dir, new_name)
    files_to_rename.append((old_path, new_path))
break
for (old_path, new_path) in files_to_rename:
    if not os.path.exists(new_path):
        pass
    else:
        conflicts.append((old_path, new_path))
break
if conflicts:
    for (old, new) in conflicts:
        print(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
break
for (old, new) in conflicts:
    print(f"  Removing {os.path.basename(old)}")
    os.remove(old)
break
# [WARN] 11 instructions not decompiled
#   @0x0072: JUMP_BACKWARD arg=62
#   @0x018E: JUMP_BACKWARD arg=62
#   @0x01A0: JUMP_BACKWARD arg=62
#   @0x0264: JUMP_BACKWARD arg=62
#   @0x02E4: JUMP_BACKWARD arg=664
#   @0x030E: JUMP_BACKWARD arg=664
#   @0x03DA: JUMP_BACKWARD arg=844
#   @0x046E: JUMP_BACKWARD arg=1014
#   @0x0494: JUMP_BACKWARD arg=1156
#   @0x049C: JUMP_BACKWARD arg=1156
# [SUMMARY] 35 blocks · 35 processed · 0 orphan · 302 instr
