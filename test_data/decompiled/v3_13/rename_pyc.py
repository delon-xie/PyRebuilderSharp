# Decompiled from: <module>

match_38 = re.search('^(.*)38\\.pyc$', filename)
match_310 = re.search('^(.*)310\\.pyc$', filename)
conflicts = [filename for filename in os.listdir(compiled_dir) if not filename.endswith('.pyc')]
# [Block @0x0298] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
# [Block @0x034C] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
# [Block @0x03F6] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
f = [f for f in files_to_rename if f not in conflicts]
