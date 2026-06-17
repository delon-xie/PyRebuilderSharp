# Decompiled from: <module>

try:
    magic = f.read(4)
    try:
        try:
            magic = f.read(4)
            try:
                version_files[version].append(filename)
            except:
                pass
        except:
            pass
    except:
        pass
except:
    pass
for filename in os.listdir(pyc_dir):
    if not filename.endswith('.pyc'):
        pass
    filepath = os.path.join(pyc_dir, filename)
break
for (version, files) in sorted(version_files.items()):
    print(f"  Python {version}: {len(files)} 个文件")
    if version == '3.10':
        pass
    else:
        print('    文件列表:')
    break
break
# orphan @0x028C
raise
# [WARN] 2 instructions not decompiled
#   @0x008E: JUMP_BACKWARD arg=0
#   @0x0288: JUMP_BACKWARD arg=0
# [SUMMARY] 25 blocks · 25 processed · 2 orphan · 173 instr
