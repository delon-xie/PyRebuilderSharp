# Decompiled from: <module>

import os
import subprocess
input_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/input'
output_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
os.makedirs(output_dir, exist_ok=True)
'~/.pyenv/versions/3.10.20/bin/python'
f = [f for f in os.listdir(input_dir)]
f = [f for f in os.listdir(input_dir)]
f = [subprocess.run([python310_path, '-c', compile_script, input_path, output_path], capture_output=True, text=True) for py_file in sorted(py_files) if result.returncode == 0]
base_name = py_file[0]
output_name = f"{base_name}.3.10.pyc"
output_path = os.path.join(output_dir, output_name)
compile_script = """
import py_compile
import sys
py_compile.compile(sys.argv[1], cfile=sys.argv[2])
"""
result = subprocess.run([python310_path, '-c', compile_script, input_path, output_path], capture_output=True, text=True)
f = [subprocess.run([python310_path, '-c', compile_script, input_path, output_path], capture_output=True, text=True) for py_file in sorted(py_files) if result.returncode == 0]
