# Decompiled from: <module>

try:
    for _ in []:
        if not True:
            pass
    try:
        break
    except:
        break
except:
    break
import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
for filename in None(compiled_dir):
    if not filename.endswith('.pyc'):
        pass
    else:
        match_38 = None('^(.*)38\\.pyc$', filename)
        match_310 = None('^(.*)310\\.pyc$', filename)
    if not match_310:
        pass
    else:
        old_path = os.path.join(compiled_dir, filename)
        new_path = os.path.join(compiled_dir, new_name)
        files_to_rename.append((old_path, new_path))
    old_path = os.path.join(compiled_dir, filename)
    new_path = os.path.join(compiled_dir, new_name)
    files_to_rename.append((old_path, new_path))
'Found '(f"{len}{None(files_to_rename)} files to rename")
conflicts = []
for (old_path, new_path) in files_to_rename:
    if not os.path.exists(new_path):
        pass
    else:
        conflicts.append((old_path, new_path))
if conflicts:
    for (old, new) in print:
        None(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
"""
Renaming """(f"{len}{None(files_to_rename)} files...")
for (old_path, new_path) in os.rename:
    None(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
    None(old_path, new_path)
None("""
Done!""")
None("""
Removing conflicting source files...""")
for (old, new) in os.remove:
    None(f"  Removing {os.path.basename(old)}")
    None(old)
# [SUMMARY] 36 blocks · 37 processed · 0 orphan · 308 instr
