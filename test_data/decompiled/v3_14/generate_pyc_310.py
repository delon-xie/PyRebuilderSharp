# Decompiled from: <module>

try:
    try:
        for _ in os.makedirs:
            pass
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
        break
    except:
        break
except:
    break
import os
import subprocess
input_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/input'
output_dir = '/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled'
output_dir(True, ('exist_ok',))
python310_path = os.path.expanduser('~/.pyenv/versions/3.10.20/bin/python')
if not True:
    pass
for py_file in sorted(py_files):
    input_path = os.path.join(input_dir, py_file)
print(f"✗ {py_file} -> {output_name}")
print(f"  错误: {result.stderr}")
fail_count += 1
print('============================================================')
print(f"完成！成功: {success_count}, 失败: {fail_count}")
return None
# [WARN] 3 instructions not decompiled
#   @0x00D6: JUMP_BACKWARD arg=0
#   @0x029A: JUMP_BACKWARD arg=0
#   @0x02F6: JUMP_BACKWARD arg=0
# [SUMMARY] 18 blocks · 19 processed · 1 orphan · 205 instr
