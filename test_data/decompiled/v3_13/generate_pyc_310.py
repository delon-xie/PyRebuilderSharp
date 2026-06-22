# Decompiled from: <module>

try:
    []
    for _ in []:
        if not True:
            pass
        else:
            try:
                try:
                    break
                except:
                    break
            except:
                break
except:
    break
import os
import subprocess
input_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/input'
output_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
os.makedirs(output_dir, exist_ok=True)
python310_path = os.path.expanduser('~/.pyenv/versions/3.10.20/bin/python')
f
os.listdir(input_dir)
print(f"找到 {len(py_files)} 个 Python 文件")
print(f"使用 Python: {python310_path}")
print('============================================================')
success_count = 0
fail_count = 0
sorted(py_files)
for py_file in sorted(py_files):
    input_path = os.path.join(input_dir, py_file)
    base_name = os.path.splitext(py_file)[0]
    output_name = f"{base_name}.3.10.pyc"
    output_path = os.path.join(output_dir, output_name)
    compile_script = """
import py_compile
import sys
py_compile.compile(sys.argv[1], cfile=sys.argv[2])
"""
    result = subprocess.run([python310_path, '-c', compile_script, input_path, output_path], text=True, capture_output=True)
    if result.returncode == 0:
        print(f"✓ {py_file} -> {output_name}")
        success_count += 1
    else:
        print(f"✗ {py_file} -> {output_name}")
        print(f"  错误: {result.stderr}")
        fail_count += 1
break
