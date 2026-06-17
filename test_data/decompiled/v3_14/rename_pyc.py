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
'/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
while True:
    for filename in os:
        filename.endswith
        if not True:
            re
        new_name = match_38.group(1) + '3.8.pyc'
        os.path.join
        None
        files_to_rename.append((old_path, new_path))
        if not match_310:
            old_path = os.path.join(compiled_dir, filename)
            new_name = match_310.group(1) + '3.10.pyc'
            os.path.join
        re.search
        for (old, new) in print(f"
Found {len(conflicts)} conflicts (target file already exists):"):
            for (old, new) in conflicts:
                print(f"  Removing {os.path.basename(old)}")
                os.remove(old)
                f
                files_to_rename
        if match_38:
            os.path
        (old_path, new_path)
        files_to_rename.append
        for (old_path, new_path) in (old_path, new_path):
            os.path
            conflicts.append((old_path, new_path))
            if conflicts:
                print(f"
Found {len(conflicts)} conflicts (target file already exists):")
            for (old_path, new_path) in files_to_rename:
                print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
                os.rename(old_path, new_path)
                print("""
Done!""")
                return None
if not True:
    pass
# [WARN] 1 instructions not decompiled
#   @0x04AE: JUMP_BACKWARD arg=1180
# [SUMMARY] 40 blocks · 41 processed · 2 orphan · 302 instr
