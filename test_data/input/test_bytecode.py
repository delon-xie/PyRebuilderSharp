
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
