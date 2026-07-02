import dis
import sys

print(f"Python version: {sys.version}")

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
print("\n=== decorating_function ===")
dis.dis(df, show_caches=True)
print(f"\nco_varnames: {df.__code__.co_varnames}")
print(f"co_cellvars: {df.__code__.co_cellvars}")
print(f"co_freevars: {df.__code__.co_freevars}")
print(f"co_nlocals: {df.__code__.co_nlocals}")

# 打印所有 LOAD_FAST_AND_CLEAR 指令的索引
code = bytes(df.__code__.co_code)
print("\n=== LOAD_FAST_AND_CLEAR 索引 ===")
for i in range(0, len(code), 2):
    op = code[i]
    arg = code[i+1] if i+1 < len(code) else 0
    if op == 156:  # LOAD_FAST_AND_CLEAR
        print(f"索引 {arg}")
