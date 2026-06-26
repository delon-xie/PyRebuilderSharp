#!/usr/bin/env python3
"""Survey 30 D-class decompiled files and classify diff categories."""

import subprocess
import os
import re
import json

BASE = "/Users/admin/codes/Tools/PyRebuilderSharp"
INPUT = os.path.join(BASE, "test_data/input")
DECOMPILED = os.path.join(BASE, "test_data/decompiled")

# 30 files to survey
FILES = [
    # reprlib across versions
    ("reprlib.py", "v3_10"), ("reprlib.py", "v3_11"), ("reprlib.py", "v3_12"),
    ("reprlib.py", "v3_13"), ("reprlib.py", "v3_14"),
    # pprint (only v3_14 available)
    ("pprint.py", "v3_14"),
    # functools across versions
    ("functools.py", "v3_10"), ("functools.py", "v3_11"), ("functools.py", "v3_12"),
    ("functools.py", "v3_13"), ("functools.py", "v3_14"),
    # enum across versions
    ("enum.py", "v3_10"), ("enum.py", "v3_11"), ("enum.py", "v3_12"),
    ("enum.py", "v3_13"), ("enum.py", "v3_14"),
    # abc across versions
    ("abc.py", "v3_10"), ("abc.py", "v3_11"), ("abc.py", "v3_12"),
    ("abc.py", "v3_13"), ("abc.py", "v3_14"),
    # Additional D-class files
    ("check_35_fields.py", "v3_10"), ("check_35_fields.py", "v3_11"),
    ("check_35_fields.py", "v3_12"), ("check_35_fields.py", "v3_13"),
    ("check_py27_magic.py", "v3_10"), ("check_py27_magic.py", "v3_11"),
    ("test_for_try.py", "v3_11"), ("test_for_try.py", "v3_12"),
    ("match_simple.py", "v3_10"), ("match_simple.py", "v3_11"),
]

def get_diff(fname, version):
    orig = os.path.join(INPUT, fname)
    dec = os.path.join(DECOMPILED, version, fname)
    if not os.path.exists(orig) or not os.path.exists(dec):
        return None
    r = subprocess.run(["diff", "-u", orig, dec], capture_output=True, text=True, timeout=10)
    return r.stdout

def classify_diff_categories(diff_text, fname, version):
    """Analyze diff text and identify which categories apply."""
    categories = {}
    
    lines = diff_text.split('\n')
    added_lines = []
    removed_lines = []
    
    for line in lines:
        if line.startswith('+') and not line.startswith('+++') and not line.startswith('+#'):
            added_lines.append(line[1:])
        elif line.startswith('-') and not line.startswith('---') and not line.startswith('-#'):
            removed_lines.append(line[1:])
    
    # Full diff text for patterns (preserving +/- markers)
    full_diff = diff_text
    
    # --- 1. SEMANTIC_ERROR: Wrong variable resolution, lost control flow ---
    # Look for patterns like try/if blocks being replaced with something else
    sem_evidence = []
    
    # Check if try/except/finally was removed or changed
    orig_try = sum(1 for l in removed_lines if l.strip().startswith('try:'))
    new_try = sum(1 for l in added_lines if l.strip().startswith('try:'))
    if orig_try > new_try and orig_try > 0:
        sem_evidence.append(f"Lost try: orig had {orig_try}, new has {new_try}")
    
    # Check for missing except/finally
    orig_except = sum(1 for l in removed_lines if l.strip().startswith('except'))
    new_except = sum(1 for l in added_lines if l.strip().startswith('except'))
    if orig_except > new_except and orig_except > 0:
        sem_evidence.append(f"Lost except: orig had {orig_except}, new has {new_except}")
    
    # Check for variable name mismatches (e.g., .cell usage)
    if any('.cell' in l for l in added_lines):
        sem_evidence.append("Contains .cell variable reference")
    
    # Check for wrong function calls (e.g., [object](**kwargs) pattern)
    if re.search(r'\[\w+\]\(', diff_text):
        sem_evidence.append("Bracket call syntax [obj](...)")
    
    if sem_evidence:
        categories["SEMANTIC_ERROR"] = sem_evidence[:3]
    
    # --- 2. CALL_EXPR_FRAGMENT: Function call broken into sub-expressions ---
    call_expr_evidence = []
    # Pattern: something like ', '.join(...) becoming ', '( pieces
    for line in added_lines:
        if re.search(r"['\"][,;:.]+['\"]\s*\(", line):
            call_expr_evidence.append(line.strip()[:80])
    if call_expr_evidence:
        categories["CALL_EXPR_FRAGMENT"] = call_expr_evidence[:3]
    
    # --- 3. TRY_EXCEPT_MISSING: try/except/finally blocks entirely missing ---
    try_missing_evidence = []
    # Check if whole try blocks are missing from decompiled output
    # Look for lines where try/except/finally appear in removed but not in added
    # Also check for 'not decompiled' marker
    full_text_combined = '\n'.join(added_lines)
    if 'not decompiled' in full_text_combined or '# [WARN]' in full_text_combined:
        try_missing_evidence.append("not decompiled / [WARN] marker present")
    
    orig_has_try = any(l.strip().startswith('try:') for l in removed_lines)
    new_has_try = any(l.strip().startswith('try:') for l in added_lines)
    if orig_has_try and not new_has_try:
        try_missing_evidence.append("try block present in original, absent in decompiled")
    
    # Check for orphan markers
    if '# orphan' in full_text_combined:
        try_missing_evidence.append("orphan blocks present")
    
    if try_missing_evidence:
        categories["TRY_EXCEPT_MISSING"] = try_missing_evidence[:3]
    
    # --- 4. DEFAULT_PARAMS_LOST: Default parameter values missing ---
    default_params_evidence = []
    # Original had 'def foo(x=None)' -> decompiled has 'def foo(x)'
    for rem, add in zip(removed_lines, added_lines):
        if rem.strip().startswith('def ') and add.strip().startswith('def '):
            # Count params with defaults in original
            orig_params = rem[rem.find('('):rem.find(')')] if ')' in rem else ''
            new_params = add[add.find('('):add.find(')')] if ')' in add else ''
            orig_defaults = orig_params.count('=')
            new_defaults = new_params.count('=')
            if orig_defaults > new_defaults:
                default_params_evidence.append(f"Lost defaults in: {rem.strip()[:60]}")
    if default_params_evidence:
        categories["DEFAULT_PARAMS_LOST"] = default_params_evidence[:3]
    
    # --- 5. KWARG_ORDER: Keyword arguments in reverse order ---
    kwarg_evidence = []
    # Pattern: 'foo(x=1, y=2)' vs 'foo(y=2, x=1)'
    for line in added_lines:
        if '=' in line and '(' in line:
            # Check if kwargs appear in different order
            pass  # Hard to detect automatically
    
    # --- 6. DOCSTRING_FORMAT: 'text' vs """text""" ---
    docstring_evidence = []
    # Original has """...""" docstrings, decompiled has '...' or __doc__ assignment
    for add_line in added_lines:
        stripped = add_line.strip()
        if stripped.startswith("__doc__ = ") or stripped.startswith("__doc__="):
            docstring_evidence.append(stripped[:80])
        elif stripped.startswith("'") and stripped.endswith("'"):
            # Check if this was a docstring replacement
            pass
    # Also check for multi-line -> single-line docstrings
    if '"""' in diff_text:
        # Check original had """ but decompiled uses single quotes
        pass
    
    # Check if original had """ and decompiled has something else
    orig_docstrings = sum(1 for l in removed_lines if '"""' in l)
    new_docstrings = sum(1 for l in added_lines if '"""' in l)
    if '__doc__' in '\n'.join(added_lines):
        docstring_evidence.append("__doc__ = assignment (docstring replaced)")
    if orig_docstrings > 0 and new_docstrings == 0 and '__doc__' not in '\n'.join(added_lines):
        # Might be 'text' vs """text"""
        docstring_evidence.append(f"Lost triple-quoted docstrings (had {orig_docstrings}, now 0)")
    
    if docstring_evidence:
        categories["DOCSTRING_FORMAT"] = docstring_evidence[:3]
    
    # --- 7. BLANK_LINES: Missing blank lines between definitions ---
    blank_lines_evidence = []
    # Count blank line differences
    orig_blanks = sum(1 for l in removed_lines if l.strip() == '')
    new_blanks = sum(1 for l in added_lines if l.strip() == '')
    if orig_blanks > new_blanks:
        blank_lines_evidence.append(f"Missing blank lines: orig had {orig_blanks}, new has {new_blanks}")
    # Also check for functions/classes merged together
    # Look for patterns where a function def immediately follows another without blank line
    if orig_blanks > new_blanks and new_blanks == 0:
        blank_lines_evidence.append("All blank lines removed between definitions")
    
    if blank_lines_evidence:
        categories["BLANK_LINES"] = blank_lines_evidence[:3]
    
    # --- 8. IMPORT_FORMAT: Import grouping/single-line vs multi-line ---
    import_evidence = []
    # Original had multi-line import, decompiled has single line, or vice versa
    orig_imports = [l for l in removed_lines if l.strip().startswith('import ') or l.strip().startswith('from ')]
    new_imports = [l for l in added_lines if l.strip().startswith('import ') or l.strip().startswith('from ')]
    orig_import_count = len(orig_imports)
    new_import_count = len(new_imports)
    if abs(orig_import_count - new_import_count) > 0 and orig_import_count > 0:
        import_evidence.append(f"Import count changed: {orig_import_count} -> {new_import_count}")
        # Show first import diff
        for o, n in zip(orig_imports[:2], new_imports[:2]):
            if o != n:
                import_evidence.append(f"  -{o.strip()[:60]}\n  +{n.strip()[:60]}")
    
    if import_evidence:
        categories["IMPORT_FORMAT"] = import_evidence[:3]
    
    # --- 9. ALL_TUPLE: __all__ list->tuple conversion ---
    all_evidence = []
    if '= [' in diff_text or '= (' in diff_text:
        for rem_line in removed_lines:
            if '__all__' in rem_line:
                for add_line in added_lines:
                    if '__all__' in add_line and add_line != rem_line:
                        all_evidence.append(f"  -{rem_line.strip()[:80]}\n  +{add_line.strip()[:80]}")
    if all_evidence:
        categories["ALL_TUPLE"] = all_evidence[:3]
    
    # --- 10. HEADER: Copyright header replaced ---
    header_evidence = []
    if '# Decompiled from:' in diff_text:
        header_evidence.append("Header: # Decompiled from: tag present")
    # Check if copyright was removed
    for rem_line in removed_lines:
        if 'Copyright' in rem_line or 'Licensed' in rem_line:
            header_evidence.append(f"Copyright/license header removed: {rem_line.strip()[:60]}")
    if header_evidence:
        categories["HEADER"] = header_evidence[:3]
    
    # --- 11. FUNC_CALL_SYNTAX: Wrong function call syntax ---
    func_call_evidence = []
    for add_line in added_lines:
        if re.search(r'\[.*?\]\(.*?\)', add_line):
            func_call_evidence.append(add_line.strip()[:80])
    # Check for wrong super() calls
    for add_line in added_lines:
        if 'super(' in add_line and ').' in add_line:
            pass  # Normal
        if 'super(' in add_line and re.search(r'super\([^)]*\)\s*\.', add_line):
            pass
    for add_line in added_lines:
        if re.search(r'\[\w+\]\(', add_line):
            func_call_evidence.append(add_line.strip()[:80])
    
    if func_call_evidence:
        categories["FUNC_CALL_SYNTAX"] = func_call_evidence[:3]
    
    # --- 12. VARIABLE_NAME: Wrong variable names ---
    var_evidence = []
    for add_line in added_lines:
        if '.cell' in add_line:
            var_evidence.append(add_line.strip()[:80])
        if re.search(r'\bvar\d+\b', add_line):
            var_evidence.append(add_line.strip()[:80])
    # Check for generic variable names
    for add_line in added_lines:
        if re.search(r'\b(v\d+|tmp\d*|_var\d*)\b', add_line):
            var_evidence.append(add_line.strip()[:80])
    
    if var_evidence:
        categories["VARIABLE_NAME"] = var_evidence[:3]
    
    return categories

def get_diff_ratio(diff_text, orig_path):
    """Calculate diff ratio."""
    added = 0
    removed = 0
    for line in diff_text.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            added += 1
        elif line.startswith('-') and not line.startswith('---'):
            removed += 1
    olines = len(open(orig_path).read().split('\n'))
    ratio = (added + removed) / max(olines, 1)
    return added, removed, ratio, olines

results = []
all_counts = {}

for fname, version in FILES:
    orig_path = os.path.join(INPUT, fname)
    dec_path = os.path.join(DECOMPILED, version, fname)
    
    if not os.path.exists(orig_path) or not os.path.exists(dec_path):
        print(f"SKIP: {fname} {version} - file not found")
        continue
    
    diff_text = get_diff(fname, version)
    if not diff_text:
        print(f"SKIP: {fname} {version} - no diff")
        continue
    
    added, removed, ratio, olines = get_diff_ratio(diff_text, orig_path)
    categories = classify_diff_categories(diff_text, fname, version)
    
    print(f"\n{'='*70}")
    print(f"{fname} ({version}) - +{added}/-{removed} lines, {olines} orig, ratio={ratio*100:.1f}%")
    print(f"{'='*70}")
    
    if not categories:
        print("  No categories detected")
    else:
        for cat, evidence in sorted(categories.items()):
            all_counts[cat] = all_counts.get(cat, 0) + 1
            print(f"  ✅ {cat}")
            for e in evidence[:2]:
                print(f"     {e}")
    
    results.append({
        "file": fname,
        "version": version,
        "added": added,
        "removed": removed,
        "ratio": ratio,
        "categories": list(categories.keys()),
        "evidence": categories
    })

print(f"\n\n{'='*70}")
print("FINAL FREQUENCY COUNT ACROSS ALL SURVEYED FILES")
print(f"{'='*70}")
print(f"Total files surveyed: {len(results)}")
print()
for cat in sorted(all_counts.keys(), key=lambda c: -all_counts[c]):
    print(f"  {all_counts[cat]:3d} / {len(results):3d}  {cat}")

print(f"\n{'='*70}")
print("PER-FILE CATEGORY SUMMARY")
print(f"{'='*70}")
for r in results:
    cats = ", ".join(r["categories"]) if r["categories"] else "(none)"
    print(f"  {r['file']:30s} {r['version']:8s} {cats}")

print(f"\n{'='*70}")
print("DETAILED EVIDENCE DUMP")
print(f"{'='*70}")
for r in results:
    print(f"\n--- {r['file']} ({r['version']}) ---")
    for cat, evidence in r["evidence"].items():
        print(f"  [{cat}]")
        for e in evidence:
            print(f"    {e}")
