#!/usr/bin/env python3
import os
import re

compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'

# 获取所有需要重命名的文件
files_to_rename = []

for filename in os.listdir(compiled_dir):
    if filename.endswith('.pyc'):
        # 匹配 *38.pyc 或 *310.pyc 格式
        match_38 = re.search(r'^(.*)38\.pyc$', filename)
        match_310 = re.search(r'^(.*)310\.pyc$', filename)
        
        if match_38:
            old_path = os.path.join(compiled_dir, filename)
            new_name = match_38.group(1) + '3.8.pyc'
            new_path = os.path.join(compiled_dir, new_name)
            files_to_rename.append((old_path, new_path))
        elif match_310:
            old_path = os.path.join(compiled_dir, filename)
            new_name = match_310.group(1) + '3.10.pyc'
            new_path = os.path.join(compiled_dir, new_name)
            files_to_rename.append((old_path, new_path))

print(f"Found {len(files_to_rename)} files to rename")

# 先检查是否有重名冲突
conflicts = []
for old_path, new_path in files_to_rename:
    if os.path.exists(new_path):
        conflicts.append((old_path, new_path))

if conflicts:
    print(f"\nFound {len(conflicts)} conflicts (target file already exists):")
    for old, new in conflicts:
        print(f"  {os.path.basename(old)} -> {os.path.basename(new)} [CONFLICT]")
    
    # 移除冲突的源文件（按规则重名的pyc文件）
    print("\nRemoving conflicting source files...")
    for old, new in conflicts:
        print(f"  Removing {os.path.basename(old)}")
        os.remove(old)
    
    # 从列表中移除已处理的冲突文件
    files_to_rename = [f for f in files_to_rename if f not in conflicts]

# 执行重命名
print(f"\nRenaming {len(files_to_rename)} files...")
for old_path, new_path in files_to_rename:
    print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
    os.rename(old_path, new_path)

print("\nDone!")
