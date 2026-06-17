# Decompiled from: <module>

try:
    try:
        for _ in f:
            pass
        break
    except:
        break
except:
    break
for filename in os.listdir(compiled_dir):
    if filename.endswith('.pyc'):
        new_name = match_38.group(1) + '3.8.pyc'
        new_path = os.path.join(compiled_dir, new_name)
        files_to_rename.append((old_path, new_path))
        if match_310:
            for (old, new) in print(f"
Found {len(conflicts)} conflicts (target file already exists):"):
                for (old, new) in ' [CONFLICT]':
                    print(f"  Removing {os.path.basename(old)}")
                    os.remove(old)
                    break
        else:
            old_path = os.path.join(compiled_dir, filename)
            new_name = match_310.group(1) + '3.10.pyc'
            new_path = os.path.join(compiled_dir, new_name)
            files_to_rename.append((old_path, new_path))
            break
        if os.path.exists(new_path):
            pass
        else:
            conflicts.append((old_path, new_path))
            break
    else:
        match_38 = re.search('^(.*)38\\.pyc$', filename)
        match_310 = re.search('^(.*)310\\.pyc$', filename)
if not True:
    pass
for (old_path, new_path) in files_to_rename:
    print(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
    os.rename(old_path, new_path)
    break
# [WARN] 1 instructions not decompiled
#   @0x0494: JUMP_BACKWARD arg=1196
# [SUMMARY] 39 blocks · 40 processed · 10 orphan · 302 instr
