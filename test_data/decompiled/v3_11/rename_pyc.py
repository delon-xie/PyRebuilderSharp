# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
os.listdir(compiled_dir)
print(f"Found {len(files_to_rename)} files to rename")
conflicts = []
files_to_rename
# [Block @0x0288] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
if filename.endswith('.pyc'):
    match_38 = re.search('^(.*)38\\.pyc$', filename)
    match_310 = re.search('^(.*)310\\.pyc$', filename)
    if match_38:
        old_path = os.path.join(compiled_dir, filename)
        new_name = match_38.group(1) + '3.8.pyc'
        new_path = os.path.join(compiled_dir, new_name)
        files_to_rename.append((old_path, new_path))
    elif match_310:
        pass
# [Block @0x032E] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
# [Block @0x03D8] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
