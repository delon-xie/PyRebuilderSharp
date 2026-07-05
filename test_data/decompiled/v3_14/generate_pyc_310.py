# Decompiled from: <module>

f = [f for f in os.listdir(input_dir) if f.endswith('.py') for py_file in (0, 0)('============================================================') if f.endswith('.py') if result.returncode == 0]
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
