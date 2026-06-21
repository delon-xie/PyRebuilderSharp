# Decompiled from: <module>

try:
    []
    for f in []:
        try:
            try:
                []
            except:
                break
        except:
            break
    print(f"
Renaming {len(files_to_rename)} files...")
    files_to_rename
    for (old_path, new_path) in files_to_rename:
        print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
        os.rename(old_path, new_path)
    print("""
Done!""")
    return None
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
print(f"Found {len(files_to_rename)} files to rename")
conflicts = []
files_to_rename
for (old_path, new_path) in files_to_rename:
    if not os.path.exists(new_path):
        pass
    else:
        conflicts.append((old_path, new_path))
if conflicts:
    for (old, new) in conflicts:
        print(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
print("""
Removing conflicting source files...""")
conflicts
for (old, new) in conflicts:
    print(f"  Removing {os.path.basename(old)}")
    os.remove(old)
f
files_to_rename
# [WARN] 11 instructions not decompiled
#   @0x0066: JUMP_BACKWARD arg=42
#   @0x0176: JUMP_BACKWARD arg=314
#   @0x017C: JUMP_BACKWARD arg=320
#   @0x023E: JUMP_BACKWARD arg=514
#   @0x02B0: JUMP_BACKWARD arg=68
#   @0x02D8: JUMP_BACKWARD arg=108
#   @0x0396: JUMP_BACKWARD arg=144
#   @0x0426: JUMP_BACKWARD arg=122
#   @0x0444: JUMP_BACKWARD arg=16
#   @0x044A: JUMP_BACKWARD arg=22
# [SUMMARY] 34 blocks · 34 processed · 0 orphan · 291 instr
