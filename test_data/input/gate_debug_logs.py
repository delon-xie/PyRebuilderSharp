#!/usr/bin/env python3
"""Gate all Console.Error.WriteLine debug calls behind _options.VerboseErrors"""
import re

path = "/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Builders/AstBuilder.cs"

with open(path, 'r') as f:
    content = f.read()
    lines = content.split('\n')

# Strategy: find each line containing Console.Error.WriteLine
# Check if it's already inside a VerboseErrors block
# If not, wrap the call(s)

modified_lines = list(lines)
i = 0
changes = []

while i < len(modified_lines):
    line = modified_lines[i]
    stripped = line.lstrip()
    
    if 'Console.Error.WriteLine' in stripped:
        # Check if already wrapped (look back up to 5 lines)
        already_wrapped = False
        for j in range(max(0, i-5), i):
            if '_options.VerboseErrors' in modified_lines[j]:
                already_wrapped = True
                break
        
        if not already_wrapped:
            indent = line[:len(line) - len(line.lstrip())]
            
            # Check if this line ends the call (with ;) 
            if stripped.rstrip().endswith(');'):
                # Single line - just wrap it
                modified_lines[i] = f"{indent}if (_options.VerboseErrors)\n{indent}{{\n{line}\n{indent}}}"
                changes.append(f"L{i+1}: wrap single-line")
                # Skip past the 3 lines we just inserted
                # (modified_lines gets re-indexed, but we continue with i)
            else:
                # Multi-line - find the closing ); 
                start_idx = i
                paren_depth = stripped.count('(') - stripped.count(')')
                while paren_depth > 0 and i < len(modified_lines) - 1:
                    i += 1
                    stripped_i = modified_lines[i].lstrip()
                    paren_depth += stripped_i.count('(') - stripped_i.count(')')
                end_idx = i
                
                # Wrap from start to end
                modified_lines[start_idx] = f"{indent}if (_options.VerboseErrors)\n{indent}{{\n{modified_lines[start_idx]}"
                modified_lines[end_idx] = modified_lines[end_idx] + f"\n{indent}}}"
                changes.append(f"L{start_idx+1}-L{end_idx+1}: wrap multi-line ({end_idx-start_idx+1} lines)")
    i += 1

print(f"Changes: {len(changes)}")
for c in changes:
    print(f"  {c}")

new_content = "\n".join(modified_lines)
with open(path, 'w') as f:
    f.write(new_content)
print(f"\nWritten {path}")
print(f"Total lines: {len(modified_lines)}")
