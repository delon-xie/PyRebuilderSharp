import ast, re

content = open('/tmp/pp_fix.py').read()
lines = content.split('\n')
for i in range(944, 955):
    if i < len(lines):
        print(f'{i+1}: {lines[i][:120]}')
print('---')
for i, line in enumerate(lines):
    if '\"\"\"' in line:
        print(f'TQ at {i+1}: {line[:120]}')
