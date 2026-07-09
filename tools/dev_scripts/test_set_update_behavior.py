import sys
import marshal
import dis

code = """
def test():
    s = set()
    s.update([1, 2])
"""

compiled = compile(code, '<test>', 'exec')

print("=== Python", sys.version_info[:2], "bytecode ===")
dis.dis(compiled.co_consts[0])
