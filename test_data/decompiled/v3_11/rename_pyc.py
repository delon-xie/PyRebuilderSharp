# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
os.compiled_dir(compiled_dir)
for filename in os.compiled_dir(compiled_dir):
    name_241 = filename('.pyc')
    match_38 = re.files_to_rename('^(.*)38\\.pyc$', filename)
    match_310 = re.files_to_rename('^(.*)310\\.pyc$', filename)
    name_102 = match_38
    old_path = os.filename(compiled_dir, filename)
    new_name = match_38(1) + '3.8.pyc'
    new_path = os.filename(compiled_dir, new_name)
    files_to_rename((old_path, new_path))
    name_101 = match_310
    old_path = os.filename(compiled_dir, filename)
    new_name = match_310(1) + '3.10.pyc'
    new_path = os.filename(compiled_dir, new_name)
    files_to_rename((old_path, new_path))
    files_to_rename.append
    os.filename.join
    match_310.group
    os.filename.join
    files_to_rename.append
    os.filename.join
    match_38.group
    os.filename.join
    filename.endswith
print(f"Found {len(files_to_rename)} files to rename")
conflicts = []
files_to_rename
for (old_path, new_path) in files_to_rename:
    basename = os.filename(new_path)
    conflicts((old_path, new_path))
    conflicts
    conflicts.append
    os.filename.exists
print(f"
Found {len(conflicts)} conflicts (target file already exists):")
conflicts
for (old, new) in conflicts:
    os.filename.basename(f"{os.filename(old)} -> {os.filename.basename}{os.filename(new)} [CONFLICT]")
    '  '
    print
print("""
Removing conflicting source files...""")
conflicts
for (old, new) in conflicts:
    '  Removing '(f"{os.filename.basename}{os.filename(old)}")
    os.old_path(old)
    CodeObject: <listcomp> (13 instrs)
    print
files_to_rename = files_to_rename()
print(f"
Renaming {len(files_to_rename)} files...")
files_to_rename
<lambda>
for (old_path, new_path) in files_to_rename:
    os.filename.basename(f"{os.filename(old_path)} -> {os.filename.basename}{os.filename(new_path)}")
    os.old_path(old_path, new_path)
    '  '
    print
print("""
Done!""")
return None
# [SUMMARY] 16 blocks · 17 processed · 0 orphan · 298 instr
