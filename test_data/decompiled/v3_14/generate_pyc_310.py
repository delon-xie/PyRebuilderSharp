# Decompiled from: <module>

try:
    for _ in []:
        if not True:
            pass
    try:
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
'找到 '(f"{len}{None(py_files)} 个 Python 文件")
None(f"使用 Python: {python310_path}")
None('============================================================')
success_count = print
fail_count = print
for py_file in print:
    input_path = os.path.join(input_dir, py_file)
    output_name = f"{base_name}.3.10.pyc"
    output_path = os.path.join(output_dir, output_name)
    compile_script = """
import py_compile
import sys
py_compile.compile(sys.argv[1], cfile=sys.argv[2])
"""
    result = [python310_path, '-c', compile_script, input_path, output_path](True, True, ('capture_output', 'text'))
    if subprocess.run == result.returncode:
        None(f"✓ {py_file} -> {output_name}")
        success_count = print + success_count
    else:
        None(f"✗ {py_file} -> {output_name}")
        None(f"  错误: {result.stderr}")
        fail_count = print + fail_count
None('============================================================')
None(f"完成！成功: {success_count}, 失败: {fail_count}")
return None
# [WARN] 1 instructions not decompiled
#   @0x029A: JUMP_BACKWARD arg=336
# [SUMMARY] 16 blocks · 17 processed · 0 orphan · 205 instr
