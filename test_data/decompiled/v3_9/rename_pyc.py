# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
for filename in match_310:
    if filename.endswith('.pyc'):
        match_38 = re.search('^(.*)38\\.pyc$', filename)
        match_310 = re.search('^(.*)310\\.pyc$', filename)
        if match_38:
            old_path = os.path.join(compiled_dir, filename)
            new_name = match_38.group(1) + '3.8.pyc'
            new_path = os.path.join(compiled_dir, new_name)
            files_to_rename.append((old_path, new_path))
    if match_310:
        old_path = os.path.join(compiled_dir, filename)
        new_name = match_310.group(1) + '3.10.pyc'
        new_path = os.path.join(compiled_dir, new_name)
        files_to_rename.append((old_path, new_path))
print(f"Found {len(files_to_rename)} files to rename")
conflicts = []
for (old_path, new_path) in os.path.exists(new_path):
    if os.path.exists(new_path):
        conflicts.append((old_path, new_path))
if conflicts:
    for (old, new) in conflicts:
        print(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
# orphan @0x0154
print("""
Removing conflicting source files...""")
# orphan @0x0160
# orphan @0x0162
print(f"  Removing {os.path.basename(old)}")
os.remove(old)
# orphan @0x018C
files_to_rename = <listcomp>(files_to_rename)
# orphan @0x019A
print(f"
Renaming {len(files_to_rename)} files...")
# orphan @0x01B2
# orphan @0x01B4
print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
os.rename(old_path, new_path)
# orphan @0x01EE
print("""
Done!""")
return None
# [SUMMARY] 23 blocks · 15 processed · 8 orphan · 249 instr
