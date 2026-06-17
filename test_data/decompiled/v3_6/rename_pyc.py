# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
for filename in os.listdir(compiled_dir):
    if filename.endswith('.pyc'):
        match_38 = re.search('^(.*)38\\.pyc$', filename)
        match_310 = re.search('^(.*)310\\.pyc$', filename)
        if match_38:
            pass
        break
        for (old_path, new_path) in files_to_rename:
            if os.path.exists(new_path):
                .0.append((old_path, new_path))
            break
            for (old_path, new_path) in files_to_rename:
                pass
            print("""
Done!""")
        if .0:
            for (old, new) in .0:
                print(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
    new_name = match_38.group(1) + '3.8.pyc'
    new_path = os.path.join(compiled_dir, new_name)
    files_to_rename.append((old_path, new_path))
    continue
    if match_310:
        old_path = os.path.join(compiled_dir, filename)
        new_name = match_310.group(1) + '3.10.pyc'
    files_to_rename.append((old_path, new_path))
    for (old, new) in .0:
        print(f"  Removing {os.path.basename(old)}")
        os.remove(old)
    files_to_rename = <lambda>(files_to_rename)
    print(f"
Renaming {len(files_to_rename)} files...")
# [SUMMARY] 26 blocks · 27 processed · 0 orphan · 259 instr
