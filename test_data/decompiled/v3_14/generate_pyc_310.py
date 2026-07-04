# Decompiled from: <module>

import os
import subprocess
input_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/input'
output_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
os.makedirs(output_dir, exist_ok=True)
python310_path = os.path.expanduser('~/.pyenv/versions/3.10.20/bin/python')
f
os.listdir(input_dir)
[]
f = [f for f in os.listdir(input_dir) if f.endswith('.py') for py_file in 0(0)('============================================================') if f.endswith('.py') if result.returncode == 0]
raise
input_path = os.path.join(input_dir, py_file)
base_name = os.path.splitext(py_file)[0]
output_name = f"{base_name}.3.10.pyc"
output_path = os.path.join(output_dir, output_name)
compile_script = """
import py_compile
import sys
py_compile.compile(sys.argv[1], cfile=sys.argv[2])
"""
result = subprocess.run([python310_path, '-c', compile_script, input_path, output_path], capture_output=True, text=True)
