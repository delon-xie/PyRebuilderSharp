# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
os.listdir(compiled_dir)
for filename in os.listdir(compiled_dir):
    if filename('.pyc'):
        match_38 = re.search('^(.*)38\\.pyc$', filename)
        match_310 = re.search('^(.*)310\\.pyc$', filename)
        if match_38:
            old_path = os.path(compiled_dir, filename)
            new_name = match_38(1) + '3.8.pyc'
            new_path = os.path(compiled_dir, new_name)
            files_to_rename((old_path, new_path))
        elif match_310:
            old_path = os.path(compiled_dir, filename)
            new_name = match_310(1) + '3.10.pyc'
            new_path = os.path(compiled_dir, new_name)
            files_to_rename((old_path, new_path))
            files_to_rename.append
            os.path.join
            match_310.group
            os.path.join
