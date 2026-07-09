import sys
import dis

code = """
def outer():
    x = []
    def inner():
        s = set()
        s.update(x)
        return s
    return inner
"""

compiled = compile(code, '<test>', 'exec')
inner_code = compiled.co_consts[0].co_consts[0]

print(f"=== Python {sys.version_info.major}.{sys.version_info.minor} inner bytecode ===")
dis.dis(inner_code)

print(f"\n=== co_varnames: {inner_code.co_varnames} ===")
print(f"co_cellvars: {inner_code.co_cellvars}")
print(f"co_freevars: {inner_code.co_freevars}")
