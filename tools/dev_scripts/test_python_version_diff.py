import subprocess
import sys

print(f"当前 Python 版本: {sys.version}")

# 测试不同 Python 版本的字节码
test_code = '''
import dis

def outer(fillvalue):
    def decorating_function(user_function):
        repr_running = set()
        def wrapper(self):
            key = id(self)
            if key in repr_running:
                return '...'
            repr_running.add(key)
            try:
                result = user_function(self)
            finally:
                repr_running.discard(key)
            return result
        return wrapper
    return decorating_function

df = outer(None)
print("=== decorating_function ===")
print(f"co_varnames: {df.__code__.co_varnames}")
print(f"co_cellvars: {df.__code__.co_cellvars}")
print(f"co_freevars: {df.__code__.co_freevars}")
dis.dis(df, show_caches=True)
'''

with open('/tmp/test_bytecode.py', 'w') as f:
    f.write(test_code)

# 尝试用不同版本的 Python 运行
for python_cmd in ['python3.13', 'python3.14', 'python3']:
    try:
        result = subprocess.run([python_cmd, '/tmp/test_bytecode.py'], 
                              capture_output=True, text=True)
        print(f"\n{'='*60}")
        print(f"=== 使用 {python_cmd} ===")
        print(result.stdout)
        if result.stderr:
            print(f"错误: {result.stderr}")
    except FileNotFoundError:
        print(f"\n{'='*60}")
        print(f"=== {python_cmd} 不可用 ===")
