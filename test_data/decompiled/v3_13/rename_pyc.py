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
while []:
    os.listdir(compiled_dir)
    for filename in os.listdir(compiled_dir):
        filename.endswith
        if not True:
            re
        new_name = match_38.group(1) + '3.8.pyc'
        os.path.join
        files_to_rename.append((old_path, new_path))
        if not match_310:
            old_path = os.path.join(compiled_dir, filename)
            new_name = match_310.group(1) + '3.10.pyc'
            os.path.join
        '^(.*)38\\.pyc$'
        None
        for (old, new) in print(f"
Found {len(conflicts)} conflicts (target file already exists):"):
            for (old, new) in conflicts:
                print(f"  Removing {os.path.basename(old)}")
                os.remove(old)
                break
        None
        re.search
        files_to_rename.append((old_path, new_path))
        if match_38:
            os.path
        for (old_path, new_path) in files_to_rename.append((old_path, new_path)):
            os.path
            conflicts.append((old_path, new_path))
            break
            if conflicts:
                print(f"
Found {len(conflicts)} conflicts (target file already exists):")
            for (old_path, new_path) in files_to_rename:
                print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
                os.rename(old_path, new_path)
                break
if not True:
    pass
# [WARN] 1 instructions not decompiled
#   @0x0494: JUMP_BACKWARD arg=1156
# [SUMMARY] 41 blocks · 42 processed · 2 orphan · 302 instr
