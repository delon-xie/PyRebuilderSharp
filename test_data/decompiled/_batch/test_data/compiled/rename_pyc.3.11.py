# Decompiled from: <module>

import os
import re
compiled_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
files_to_rename = []
os.listdir(compiled_dir)
conflicts = [filename for filename in os.listdir(compiled_dir) if filename.endswith('.pyc')]
# [Block @0x032E] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
# [Block @0x03D8] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
