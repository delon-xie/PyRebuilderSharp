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
    for filename in None:
        if not filename.endswith('.pyc'):
            pass
        new_name = match_38.group(1) + '3.8.pyc'
        new_path = os.path.join(compiled_dir, new_name)
        files_to_rename.append((old_path, new_path))
        if not match_310:
            pass
        for (old, new) in conflicts:
            break
            for (old, new) in conflicts:
                print(f"  Removing {os.path.basename(old)}")
                os.remove(old)
        match_38 = re.search('^(.*)38\\.pyc$', filename)
        match_310 = re.search('^(.*)310\\.pyc$', filename)
        if match_38:
            pass
        old_path = os.path.join(compiled_dir, filename)
        new_name = match_310.group(1) + '3.10.pyc'
        new_path = os.path.join(compiled_dir, new_name)
        files_to_rename.append((old_path, new_path))
        for (old_path, new_path) in print(f"Found {len(files_to_rename)} files to rename"):
            if not os.path.exists(new_path):
                conflicts.append((old_path, new_path))
            if conflicts:
                pass
if not True:
    pass
for (old_path, new_path) in files_to_rename:
    print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
    os.rename(old_path, new_path)
    print("""
Done!""")
    return None
# [WARN] 6 instructions not decompiled
#   @0x0074: JUMP_BACKWARD arg=0
#   @0x019A: JUMP_BACKWARD arg=0
#   @0x01AE: JUMP_BACKWARD arg=0
#   @0x027A: JUMP_BACKWARD arg=0
#   @0x0326: JUMP_BACKWARD arg=0
#   @0x04AE: JUMP_BACKWARD arg=1166
# [SUMMARY] 41 blocks · 42 processed · 1 orphan · 308 instr
