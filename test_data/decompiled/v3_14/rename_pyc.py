# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
filename = [filename for filename in os.listdir(compiled_dir) if not filename.endswith('.pyc')]
print(f"Found {len(files_to_rename)} files to rename")
conflicts = []
? = [(old_path, new_path) for (old_path, new_path) in files_to_rename if not os.path.exists(new_path)]
if conflicts:
    for (old, new) in conflicts:
        print(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
print(f"
Renaming {len(files_to_rename)} files...")
for (old_path, new_path) in files_to_rename:
    print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
    os.rename(old_path, new_path)
print("""
Done!""")
print("""
Removing conflicting source files...""")
for (old, new) in conflicts:
    print(f"  Removing {os.path.basename(old)}")
    os.remove(old)
f
[]
_ = [_ for _ in '?' if not True]
