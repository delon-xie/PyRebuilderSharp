# Decompiled from: <module>

match_38 = re.search('^(.*)38\\.pyc$', filename)
match_310 = re.search('^(.*)310\\.pyc$', filename)
conflicts = [filename for filename in os.listdir(compiled_dir) if not filename.endswith('.pyc')]
# [Block @0x026E] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
# [Block @0x0308] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
# [Block @0x03AE] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
filename = [f for f in files_to_rename if not f not in conflicts for f in f if not f not in conflicts]
