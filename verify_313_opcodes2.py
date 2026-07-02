import urllib.request

url = "https://raw.githubusercontent.com/python/cpython/3.13/Lib/opcode.py"
try:
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    
    print("Python 3.13 opname list:")
    for line in content.split('\n'):
        if 'opname' in line and '=[' in line:
            # Find the opname list definition
            start = line.find('[')
            end = line.find(']') + 1
            raw = line[start:end]
            # Parse the list
            names = []
            s = raw[1:-1]
            current = ''
            in_string = False
            for c in s:
                if c == "'" and (not current or current[-1] != '\\'):
                    in_string = not in_string
                elif in_string:
                    current += c
                elif c == ',':
                    if current.strip():
                        names.append(current.strip())
                    current = ''
                else:
                    current += c
            if current.strip():
                names.append(current.strip())
            
            for i, name in enumerate(names):
                if name and name != 'UNUSED' and name != 'RESERVED':
                    print(f"{i:3d}: {name}")
            break
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
