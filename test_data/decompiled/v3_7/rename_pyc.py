# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
.0 = [filename for filename in '?' if filename.endswith('.pyc') if match_310]
print(f"Found {len(files_to_rename)} files to rename")
.0 = []
? = [(old_path, new_path) for (old_path, new_path) in '?' if os.path.exists(new_path)]
if .0:
    for (old, new) in .0:
        print(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
print(f"  Removing {os.path.basename(old)}")
os.remove(old)
print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
os.rename(old_path, new_path)
