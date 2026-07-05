import py_compile
import sys

# 创建一个包含列表推导式的测试文件
test_code = """
def foo():
    return [x + 1 for x in range(10)]
"""

with open('/tmp/test_comp.py', 'w') as f:
    f.write(test_code)

py_compile.compile('/tmp/test_comp.py', '/tmp/test_comp.pyc', optimize=0)
print(f"Python version: {sys.version}")
print("Test file compiled successfully")
