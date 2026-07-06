# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
os.listdir(compiled_dir)
conflicts = [filename for filename in os.listdir(compiled_dir) if filename.endswith('.pyc')]
# [Block @0x00E0] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
# [Block @0x0120] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
print(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
# [Block @0x015C] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
print(f"  Removing {os.path.basename(old)}")
os.remove(old)
# [Block @0x01AC] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
os.rename(old_path, new_path)
