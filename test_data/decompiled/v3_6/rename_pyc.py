# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
os.listdir(compiled_dir)
.0 = [filename for filename in os.listdir(compiled_dir) if filename.endswith('.pyc') if match_310]
.0.append((old_path, new_path))
print(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
print(f"  Removing {os.path.basename(old)}")
os.remove(old)
print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
os.rename(old_path, new_path)
