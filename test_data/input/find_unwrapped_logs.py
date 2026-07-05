#!/usr/bin/env python3
"""Find ALL Console.Error.WriteLine in src/ that are NOT behind VerboseErrors or Diag.Verbose."""
import os, re

src_dir = "/Users/admin/codes/Tools/PyRebuilderSharp/src"
exempt_files = {"Diag.cs"}  # Diag itself

# For each file, find Console.Error.WriteLine and check if it's in a VerboseErrors scope
# We do a simple line-by-line scan keeping track of the nearest preceding condition

issues = []
for root, dirs, files in os.walk(src_dir):
    for fname in sorted(files):
        if not fname.endswith(".cs") or fname in exempt_files:
            continue
        fpath = os.path.join(root, fname)
        with open(fpath) as f:
            lines = f.readlines()
        
        # Scan for Console.Error.WriteLine preceded by a conditional
        verbose_scope_depth = 0
        brace_depth = 0
        # Track VerboseErrors scope using a stack-like approach
        condition_stack = []  # list of bool per indentation level
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            sn = stripped
            
            if "VerboseErrors" in sn or "Diag.Verbose" in sn:
                # This line has the condition check. Next line might start the if block.
                verbose_scope_depth = brace_depth + 1  # guess next level
            
            if "Console.Error.WriteLine" in sn and not sn.startswith("//"):
                # Check if preceding lines (up to 5 back or current scope) have a gate
                has_gate = False
                for j in range(max(0, i-8), i):
                    if "VerboseErrors" in lines[j] or "_options.VerboseErrors" in lines[j] or "Diag.Verbose" in lines[j]:
                        # Check if this condition's scope is still active
                        # Simplification: if the condition is within 6 lines and indentation-wise reasonable
                        has_gate = True
                        break
                
                if not has_gate:
                    # Also check the Console.Error.WriteLine in non-debug paths (TIMEOUT, WARN, etc.)
                    if any(tag in sn for tag in ["ORPHAN_CLASSIFY", "TRY_DBG", "TRY_FROM_ET", "ET_ELSE", "BSI_ET",
                                                  "DECOMP_TRACE", "PARSER_DEBUG", "GET_ITER", "MF_DEBUG",
                                                  "BUILD_FOR_LOOP", "COMP_DETECT", "COMP_LAMBDA",
                                                  "ORPHAN", "SUMMARY", "WARN", "ET_DUMP"]):
                        issues.append((fpath, i+1, sn[:120]))

print(f"UNWRAPPED DEBUG Console.Error.WriteLine: {len(issues)}")
for fpath, ln, ctx in issues:
    print(f"  {os.path.basename(fpath)}:{ln}: {ctx}")
