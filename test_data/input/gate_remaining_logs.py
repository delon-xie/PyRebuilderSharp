#!/usr/bin/env python3
"""Replace debug Console.Error.WriteLine with Diag.WriteLine in PycReader, ControlFlowScanner, StackMachine"""

import re

files_replacements = {
    "/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Readers/PycReader.cs": [
        # Line 868: PARSER_DEBUG
        (r'^\s*Console\.Error\.WriteLine\(\$"\[PARSER_DEBUG\]', 
         '                    if (Diag.Verbose)\n                        Console.Error.WriteLine($"[PARSER_DEBUG]'),
        # Line 977: DECOMP_TRACE stage=PARSE
        (r'^\s*Console\.Error\.WriteLine\(\$"\[DECOMP_TRACE\] stage=PARSE', 
         '            if (Diag.Verbose)\n                Console.Error.WriteLine($"[DECOMP_TRACE] stage=PARSE'),
        # Line 989: DECOMP_TRACE jump_target
        (r'^\s*Console\.Error\.WriteLine\(\$"\[DECOMP_TRACE\] stage=PARSE jump_target', 
         '                if (Diag.Verbose)\n                    Console.Error.WriteLine($"[DECOMP_TRACE] stage=PARSE jump_target'),
        # Line 997: DECOMP_TRACE cache entries  
        (r'^\s*Console\.Error\.WriteLine\(\$"\[DECOMP_TRACE\] stage=PARSE offset=0x.*cache entries"\);',
         '                if (Diag.Verbose)\n                    Console.Error.WriteLine($"'),
    ],
    "/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Scanners/ControlFlowScanner.cs": [
        # Line 141: CFG loop_candidate
        (r'^\s*Console\.Error\.WriteLine\(\$"\[DECOMP_TRACE\] stage=CFG loop_candidate', 
         '                    Console.Error.WriteLine($"[DECOMP_TRACE] stage=CFG loop_candidate'),
        # Line 145: CFG loop_body_block
        (r'^\s*Console\.Error\.WriteLine\(\$"\[DECOMP_TRACE\] stage=CFG loop_body_block', 
         '                        Console.Error.WriteLine($"[DECOMP_TRACE] stage=CFG loop_body_block'),
        # Line 150: CFG loop_type
        (r'^\s*Console\.Error\.WriteLine\(\$"\[DECOMP_TRACE\] stage=CFG loop_type', 
         '                    Console.Error.WriteLine($"[DECOMP_TRACE] stage=CFG loop_type'),
        # Line 157: CFG forIterBlock_found
        (r'^\s*Console\.Error\.WriteLine\(\$"\[DECOMP_TRACE\] stage=CFG forIterBlock_found', 
         '                        Console.Error.WriteLine($"[DECOMP_TRACE] stage=CFG forIterBlock_found'),
    ],
    "/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Builders/StackMachine.cs": [
        # Line 1639: GET_ITER
        (r'^\s*Console\.Error\.WriteLine\(\$"\[GET_ITER\]', 
         '                    if (Diag.Verbose)\n                        Console.Error.WriteLine($"[GET_ITER]'),
        # Line 1685: MF_DEBUG
        (r'^\s*Console\.Error\.WriteLine\(\$"\[MF_DEBUG\]', 
         '                            if (Diag.Verbose)\n                                Console.Error.WriteLine($"[MF_DEBUG]'),
    ],
}

for filepath, patterns in files_replacements.items():
    with open(filepath, 'r') as f:
        content = f.read()
    
    changed = False
    for pattern, replacement in patterns:
        # Use a simple string replacement approach since regex might be tricky with special chars
        # Find the exact line and replace
        lines = content.split('\n')
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Get the target prefix from the replacement (the original Console.Error.WriteLine part)
            # Actually let's just do line-by-line matching
            if stripped.startswith('Console.Error.WriteLine($') and ('[DECOMP_TRACE]' in stripped or '[PARSER_DEBUG]' in stripped or '[GET_ITER]' in stripped or '[MF_DEBUG]' in stripped):
                # Skip if already wrapped (look back a few lines)
                already_wrapped = False
                for j in range(max(0, i-3), i):
                    if 'Diag.Verbose' in lines[j] or '_options.VerboseErrors' in lines[j]:
                        already_wrapped = True
                        break
                
                if already_wrapped:
                    continue
                
                indent = line[:len(line) - len(line.lstrip())]
                # Wrap with Diag.Verbose check
                lines[i] = f"{indent}if (Diag.Verbose)\n{indent}{{\n{line}\n{indent}}}"
                changed = True
                print(f"  {filepath.split('/')[-1]} L{i+1}: wrapped")
    
    if changed:
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))
        print(f"✅ {filepath.split('/')[-1]}")
    else:
        print(f"⚠️  {filepath.split('/')[-1]}: no changes")
