# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
os.listdir(compiled_dir)
conflicts = [filename for filename in os.listdir(compiled_dir) if filename.endswith('.pyc')]
print(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
print(f"  Removing {os.path.basename(old)}")
os.remove(old)
print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
os.rename(old_path, new_path)
