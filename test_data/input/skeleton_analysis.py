
import ast, os, re, json
from collections import Counter

PROJECT_DIR = "/Users/admin/codes/Tools/PyRebuilderSharp"
INPUT_DIR = os.path.join(PROJECT_DIR, "test_data/input")
DECOMPILED_DIR = os.path.join(PROJECT_DIR, "test_data/decompiled")
VERSIONS = ["2.7","3.5","3.6","3.7","3.8","3.9","3.10","3.11","3.12","3.13","3.14"]

def ver_tag(v):
    return "v" + v.replace(".", "_")

def analyze(py_file):
    orig_path = os.path.join(INPUT_DIR, py_file)
    if not os.path.exists(orig_path):
        return None
    
    with open(orig_path) as f:
        orig = f.read()
    
    try:
        orig_tree = ast.parse(orig)
        orig_classes = sorted([n.name for n in ast.walk(orig_tree) if isinstance(n, ast.ClassDef)])
        orig_funcs = sorted([n.name for n in ast.walk(orig_tree) if isinstance(n, ast.FunctionDef) and not n.name.startswith("<")])
        orig_try = sum(1 for _ in ast.walk(orig_tree) if isinstance(_, ast.Try))
        orig_if = sum(1 for _ in ast.walk(orig_tree) if isinstance(_, ast.If))
        orig_for = sum(1 for _ in ast.walk(orig_tree) if isinstance(_, ast.For))
        orig_while = sum(1 for _ in ast.walk(orig_tree) if isinstance(_, ast.While))
    except SyntaxError:
        return None
    
    results = {}
    for ver in VERSIONS:
        vt = ver_tag(ver)
        dec_path = os.path.join(DECOMPILED_DIR, vt, py_file)
        if not os.path.exists(dec_path):
            continue
        
        with open(dec_path) as f:
            dec = f.read()
        
        rec = {"ver": ver}
        try:
            dec_tree = ast.parse(dec)
            dec_classes = sorted([n.name for n in ast.walk(dec_tree) if isinstance(n, ast.ClassDef)])
            dec_funcs = sorted([n.name for n in ast.walk(dec_tree) if isinstance(n, ast.FunctionDef) and not n.name.startswith("<")])
            dec_try = sum(1 for _ in ast.walk(dec_tree) if isinstance(_, ast.Try))
            dec_if = sum(1 for _ in ast.walk(dec_tree) if isinstance(_, ast.If))
            dec_for = sum(1 for _ in ast.walk(dec_tree) if isinstance(_, ast.For))
            dec_while = sum(1 for _ in ast.walk(dec_tree) if isinstance(_, ast.While))
            
            rec["parse_ok"] = True
            
            # Class diffs
            if set(dec_classes) != set(orig_classes):
                rec["class_diff"] = {"missing": list(set(orig_classes)-set(dec_classes)), "extra": list(set(dec_classes)-set(orig_classes))}
            
            # Function diffs
            if set(dec_funcs) != set(orig_funcs):
                rec["func_diff"] = {"missing": list(set(orig_funcs)-set(dec_funcs)), "extra": list(set(dec_funcs)-set(orig_funcs))}
            
            # Count diffs
            rec["counts"] = {
                "class": (len(orig_classes), len(dec_classes)),
                "func": (len(orig_funcs), len(dec_funcs)),
                "try": (orig_try, dec_try),
                "if": (orig_if, dec_if),
                "for": (orig_for, dec_for),
                "while": (orig_while, dec_while),
            }
            
        except SyntaxError as e:
            rec["parse_ok"] = False
            rec["parse_error"] = str(e)[:60]
            # Even if parse fails, count class/def by regex
            dec_classes = [l.split("class ")[1].split("(")[0].split(":")[0].strip() for l in dec.split("\n") if l.strip().startswith("class ")]
            dec_funcs = [l.split("def ")[1].split("(")[0].strip() for l in dec.split("\n") if l.strip().startswith("def ") and not l.strip().startswith("def <")]
            rec["regex_counts"] = {"class": len(dec_classes), "func": len(dec_funcs)}
        
        results[ver] = rec
    
    return {"file": py_file, "orig": {"classes": orig_classes, "funcs": orig_funcs, "try": orig_try, "if": orig_if, "for": orig_for, "while": orig_while}, "versions": results}

KEY_FILES = ["abc.py", "enum.py", "functools.py", "reprlib.py"]
for fn in KEY_FILES:
    r = analyze(fn)
    if r is None:
        continue
    print(f"=== {r['file']} ===")
    orig = r['orig']
    print(f"  Original: {orig['try']}t {orig['if']}if {orig['for']}f {orig['while']}w | classes={len(orig['classes'])} funcs={len(orig['funcs'])}")
    
    for ver in VERSIONS:
        if ver not in r['versions']:
            continue
        v = r['versions'][ver]
        if v.get("parse_ok"):
            c = v['counts']
            issues = []
            if c['class'][0] != c['class'][1]: issues.append(f"C{c['class'][0]}->{c['class'][1]}")
            if c['func'][0] != c['func'][1]: issues.append(f"F{c['func'][0]}->{c['func'][1]}")
            if c['try'][0] != c['try'][1]: issues.append(f"T{c['try'][0]}->{c['try'][1]}")
            if issues:
                print(f"  {ver:5s}: ✅parse | {' '.join(issues)}")
            else:
                print(f"  {ver:5s}: ✅ all match")
        else:
            err = v.get("parse_error", "unknown")
            rc = v.get("regex_counts", {})
            rc_str = f" | regex: C={rc.get('class', '?')} F={rc.get('func', '?')}" if rc else ""
            print(f"  {ver:5s}: ❌ {err}{rc_str}")
