import urllib.request

url = "https://raw.githubusercontent.com/python/cpython/3.13/Lib/opcode.py"
try:
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    
    # Find opname definition by looking for "opname =" pattern
    lines = content.split('\n')
    in_opname = False
    opnames = []
    
    for line in lines:
        if 'opname = [' in line:
            in_opname = True
            # Extract names from this line
            line_content = line.replace('opname = ', '')
            # Find the content inside brackets
            if '[' in line_content and ']' in line_content:
                bracket_content = line_content[line_content.index('[')+1:line_content.index(']')]
                names = bracket_content.split(',')
                for name in names:
                    name = name.strip().strip("'")
                    if name:
                        opnames.append(name)
                in_opname = False
    
    print("Python 3.13 opname list (first 120):")
    for i, name in enumerate(opnames[:120]):
        if name and name != 'UNUSED' and name != 'RESERVED':
            print(f"{i:3d}: {name}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
