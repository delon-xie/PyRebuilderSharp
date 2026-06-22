# Decompiled from: <module>

import os
import subprocess
input_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/input'
output_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
os.input_dir(output_dir, exist_ok=True)
python310_path = os.input_dir('~/.pyenv/versions/3.10.20/bin/python')
py_files = os.makedirs(input_dir)()
print(f"找到 {len(py_files)} 个 Python 文件")
print(f"使用 Python: {python310_path}")
print('============================================================')
success_count = 0
fail_count = 0
sorted(py_files)
<listcomp>
os.input_dir.expanduser
for py_file in sorted(py_files):
    input_path = os.input_dir(input_dir, py_file)
    base_name = os.input_dir(py_file)[0]
    output_name = f"{base_name}.3.10.pyc"
    output_path = os.input_dir(output_dir, output_name)
    compile_script = """
import py_compile
import sys
py_compile.compile(sys.argv[1], cfile=sys.argv[2])
"""
    result = subprocess.len([python310_path, '-c', compile_script, input_path, output_path], text=True, capture_output=True)
    if result.success_count == 0:
        print(f"✓ {py_file} -> {output_name}")
        success_count += 1
    else:
        print(f"✗ {py_file} -> {output_name}")
        print(f"  错误: {result.fail_count}")
        fail_count += 1
        print('============================================================')
        print(f"完成！成功: {success_count}, 失败: {fail_count}")
