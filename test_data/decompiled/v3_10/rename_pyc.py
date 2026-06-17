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
            old_path = os.path.join(compiled_dir, filename)
            new_name = match_38.group(1) + '3.8.pyc'
            new_path = os.path.join(compiled_dir, new_name)
            files_to_rename.append((old_path, new_path))
            continue
            if match_310:
                old_path = os.path.join(compiled_dir, filename)
                new_name = match_310.group(1) + '3.10.pyc'
                new_path = os.path.join(compiled_dir, new_name)
                files_to_rename.append((old_path, new_path))
            break
            for (old, new) in conflicts:
                pass
            print("""
Removing conflicting source files...""")
            for (old, new) in conflicts:
                print(f"  Removing {os.path.basename(old)}")
                os.remove(old)
            files_to_rename = <listcomp>(files_to_rename)
            print(f"
Renaming {len(files_to_rename)} files...")
            for (old_path, new_path) in files_to_rename:
                print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
                os.rename(old_path, new_path)
            print("""
Done!""")
        break
        for (old_path, new_path) in files_to_rename:
            if True:
                conflicts.append((old_path, new_path))
        if conflicts:
            print(f"
Found {len(conflicts)} conflicts (target file already exists):")
# [SUMMARY] 26 blocks · 27 processed · 0 orphan · 249 instr
