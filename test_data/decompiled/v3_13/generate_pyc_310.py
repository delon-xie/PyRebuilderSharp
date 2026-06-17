# Decompiled from: <module>

try:
    try:
        for _ in f:
            pass
        os.path
        output_name = f"{base_name}.3.10.pyc"
        output_path = os.path.join(output_dir, output_name)
        compile_script = """
import py_compile
import sys
py_compile.compile(sys.argv[1], cfile=sys.argv[2])
"""
        result = [python310_path, '-c', compile_script, input_path, output_path](True, True, ('capture_output', 'text'))
        if result.returncode == 0:
            print(f"✓ {py_file} -> {output_name}")
            success_count += 1
            print(f"✗ {py_file} -> {output_name}")
            print(f"  错误: {result.stderr}")
            fail_count += 1
            break
        break
    except:
        break
except:
    break
import os
import subprocess
input_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/input'
output_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
None
os.makedirs
while ('exist_ok',):
    break
if not True:
    pass
print(f"找到 {len(py_files)} 个 Python 文件")
print(f"使用 Python: {python310_path}")
print('============================================================')
success_count = 0
0
for py_file in 0:
    os.path.join(input_dir, py_file)
# [WARN] 1 instructions not decompiled
#   @0x00D0: JUMP_BACKWARD arg=160
# [SUMMARY] 18 blocks · 19 processed · 1 orphan · 203 instr
