# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
os.listdir(compiled_dir)
conflicts = [filename for filename in os.listdir(compiled_dir) if filename.endswith('.pyc') if match_310]
# [Block @0x00E0] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
conflicts.append((old_path, new_path))
# [Block @0x0122] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
print(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
# [Block @0x0160] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
print(f"  Removing {os.path.basename(old)}")
os.remove(old)
# [Block @0x01B2] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
os.rename(old_path, new_path)
