import urllib.request
import json

url = "https://raw.githubusercontent.com/python/cpython/3.13/Lib/opcode.py"
try:
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    
    opname_start = content.find("opname = [")
    opname_end = content.find("]", opname_start) + 1
    opname_str = content[opname_start:opname_end]
    
    print("Python 3.13 opname list:")
    exec(opname_str, globals())
    
    for i, name in enumerate(opname):
        if name and name != 'UNUSED' and name != 'RESERVED':
            print(f"{i:3d}: {name}")
            
except Exception as e:
    print(f"Error: {e}")
