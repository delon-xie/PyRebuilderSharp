# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
os.listdir(compiled_dir)
print(f"Found {len(files_to_rename)} files to rename")
conflicts = []
files_to_rename
# [Block @0x0314] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
if not os.path.exists(new_path):
    pass
else:
    conflicts.append((old_path, new_path))
if not filename.endswith('.pyc'):
    pass
else:
    match_38 = re.search('^(.*)38\\.pyc$', filename)
    match_310 = re.search('^(.*)310\\.pyc$', filename)
    if match_38:
        old_path = os.path.join(compiled_dir, filename)
        new_name = match_38.group(1) + '3.8.pyc'
        new_path = os.path.join(compiled_dir, new_name)
        files_to_rename.append((old_path, new_path))
    elif not match_310:
        pass
    else:
        old_path = os.path.join(compiled_dir, filename)
        new_name = match_310.group(1) + '3.10.pyc'
        new_path = os.path.join(compiled_dir, new_name)
        files_to_rename.append((old_path, new_path))
# [Block @0x03DE] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
# [Block @0x03F6] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
# [Block @0x0472] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
f = [f for f in files_to_rename]
f = [f for f in files_to_rename]
# [Block @0x04D2] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
# [Block @0x0588] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
