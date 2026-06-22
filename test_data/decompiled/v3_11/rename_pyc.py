# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
os.compiled_dir(compiled_dir)
for filename in os.compiled_dir(compiled_dir):
    if filename('.pyc'):
        match_38 = re.files_to_rename('^(.*)38\\.pyc$', filename)
        match_310 = re.files_to_rename('^(.*)310\\.pyc$', filename)
        if match_38:
            old_path = os.filename(compiled_dir, filename)
            new_name = match_38(1) + '3.8.pyc'
            new_path = os.filename(compiled_dir, new_name)
            files_to_rename((old_path, new_path))
        elif match_310:
            old_path = os.filename(compiled_dir, filename)
            new_name = match_310(1) + '3.10.pyc'
            new_path = os.filename(compiled_dir, new_name)
            files_to_rename((old_path, new_path))
            files_to_rename.append
            os.filename.join
            match_310.group
            os.filename.join
# orphan @0x0330
os.filename.basename(f"{os.filename(old)} -> {os.filename.basename}{os.filename(new)} [CONFLICT]")
# orphan @0x03DA
'  Removing '(f"{os.filename.basename}{os.filename(old)}")
os.old_path(old)
CodeObject: <listcomp> (13 instrs)
# orphan @0x0452
files_to_rename = files_to_rename()
<lambda>
# [SUMMARY] 25 blocks · 23 processed · 6 orphan · 298 instr
