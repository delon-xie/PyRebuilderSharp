#!/usr/bin/env python3
"""
deep_quality_scan.py — 深层质量扫描（超越 diff 比率）

扫描反编译输出中的语义错误模式：
  1. For-loop 迭代表达式混乱（for x in comparison）
  2. Orphan raise（# orphan → raise）
  3. while True: pass（未解析跳转）
  4. <genexpr>/<setcomp>/<listcomp>/<dictcomp> artifacts
  5. 通用 ast.parse 可解析性
  6. try/except 块结构完整性

Usage:
  python3 tools/deep_quality_scan.py
  python3 tools/deep_quality_scan.py --json  # JSON output
"""

import ast, os, sys, re, glob, collections, json

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECOMPILED_DIR = os.path.join(PROJECT_DIR, "test_data/decompiled")
INPUT_DIR = os.path.join(PROJECT_DIR, "test_data/input")

VERSIONS = ["2.7", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]

def ver_tag(ver):
    return f"v{ver.replace('.', '_')}"

def main():
    results = {
        "semantic": {
            "for_iter_confusion": [],
            "orphan_raises": [],
            "while_true_pass": [],
            "bare_iterable": [],
            "comp_expr_artifacts": [],  # <genexpr>, <setcomp>, <listcomp>, <dictcomp>
        },
        "parse": {
            "by_version": {},
            "failure_categories": collections.Counter(),
        },
        "summary": {}
    }
    
    total_ok = total_fail = total_files = 0
    genexpr_files = set()
    
    for ver in VERSIONS:
        vt = ver_tag(ver)
        d = os.path.join(DECOMPILED_DIR, vt)
        if not os.path.exists(d):
            continue
        
        ver_ok = ver_fail = 0
        ver_files = []
        
        for py_file in sorted(glob.glob(os.path.join(d, "*.py"))):
            bn = os.path.basename(py_file)
            total_files += 1
            
            try:
                with open(py_file) as f:
                    lines = f.readlines()
            except Exception:
                ver_fail += 1
                continue
            
            content = "".join(lines)
            
            # ---- Semantic Scan ----
            for i, line in enumerate(lines):
                s = line.rstrip()
                s_stripped = s.strip()
                line_no = i + 1
                
                # For-loop iterable confusion
                if s_stripped.startswith("for ") and " in " in s_stripped:
                    after_in = s_stripped.split(" in ", 1)[1].strip()
                    if after_in.endswith(":"):
                        after_in = after_in[:-1].strip()
                    if re.search(r'\b(?:<|>|==|!=|<=|>=)\b', after_in):
                        results["semantic"]["for_iter_confusion"].append(
                            (f"{bn}@{ver}", line_no, s_stripped))
                    
                    if after_in in ("iterable", "iterable:"):
                        results["semantic"]["bare_iterable"].append(
                            (f"{bn}@{ver}", line_no, s_stripped))
                
                # Orphan raises
                if s_stripped == "raise":
                    ctx = lines[max(0, i-3):i]
                    if any(l.strip().startswith("# orphan") for l in ctx):
                        results["semantic"]["orphan_raises"].append(
                            (f"{bn}@{ver}", line_no))
                
                # while True: pass
                if "while True:" in s and "pass" in s:
                    results["semantic"]["while_true_pass"].append(
                        (f"{bn}@{ver}", line_no, s_stripped))
            
            # Compiled expression artifacts
            for pattern, name in [("<genexpr>", "genexpr"), ("<setcomp>", "setcomp"),
                                   ("<listcomp>", "listcomp"), ("<dictcomp>", "dictcomp")]:
                if f"def {pattern}" in content:
                    results["semantic"]["comp_expr_artifacts"].append(
                        (f"{bn}@{ver}", name))
                    genexpr_files.add(f"{bn}@{ver}")
            
            # ---- Parse Check ----
            try:
                ast.parse(content)
                ver_ok += 1
            except SyntaxError as e:
                ver_fail += 1
                # Categorize failure
                msg = e.msg[:60]
                if "<genexpr>" in content or "<setcomp>" in content or "<listcomp>" in content or "<dictcomp>" in content:
                    cat = "<comp_expr> artifact"
                elif "except" in msg.lower() or "finally" in msg.lower():
                    cat = "try/except structure"
                elif "unterminated" in msg.lower():
                    cat = "unterminated string"
                elif "decimal literal" in msg.lower():
                    cat = "decimal literal format"
                else:
                    cat = "other"
                results["parse"]["failure_categories"][cat] += 1
        
        results["parse"]["by_version"][ver] = {
            "ok": ver_ok, "fail": ver_fail, "total": ver_ok + ver_fail
        }
        total_ok += ver_ok
        total_fail += ver_fail
    
    results["summary"] = {
        "total_files": total_files,
        "total_ok": total_ok,
        "total_fail": total_fail,
        "parse_rate": f"{total_ok/max(total_files,1)*100:.0f}%",
        "for_iter_confusion": len(results["semantic"]["for_iter_confusion"]),
        "orphan_raises": len(results["semantic"]["orphan_raises"]),
        "while_true_pass": len(results["semantic"]["while_true_pass"]),
        "bare_iterable": len(results["semantic"]["bare_iterable"]),
        "comp_expr_artifacts": len(results["semantic"]["comp_expr_artifacts"]),
        "genexpr_unique_files": len(genexpr_files),
    }
    
    # Convert counters to dict for JSON
    results["parse"]["failure_categories"] = dict(results["parse"]["failure_categories"])
    
    # Print report
    json_mode = "--json" in sys.argv
    
    if json_mode:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return
    
    print("=" * 60)
    print("DEEP QUALITY SCAN REPORT")
    print("=" * 60)
    print(f"Files scanned: {total_files}")
    print(f"Parse OK:      {total_ok} ({total_ok/max(total_files,1)*100:.0f}%)")
    print(f"Parse FAIL:    {total_fail} ({total_fail/max(total_files,1)*100:.0f}%)")
    print()
    
    print("--- Semantic Issues ---")
    for key, label in [("for_iter_confusion", "For-loop iterable confusion"),
                        ("orphan_raises", "Orphan raises"),
                        ("while_true_pass", "while True: pass"),
                        ("bare_iterable", "Bare 'iterable' variable"),
                        ("comp_expr_artifacts", "Comp expression artifacts")]:
        items = results["semantic"][key]
        if items:
            print(f"  ❌ {label}: {len(items)}")
            for item in items[:5]:
                print(f"    {item}")
        else:
            print(f"  ✅ {label}: 0")
    print()
    
    print("--- Parse Failure Categories ---")
    for cat, count in sorted(results["parse"]["failure_categories"].items(), key=lambda x: -x[1]):
        print(f"  {count:3d}x  {cat}")
    print()
    
    print("--- By Version ---")
    for ver in VERSIONS:
        if ver in results["parse"]["by_version"]:
            pd = results["parse"]["by_version"][ver]
            print(f"  {ver}: {pd['ok']}/{pd['total']} ({pd['ok']/max(pd['total'],1)*100:.0f}%)")
    
    print()
    if not any(results["semantic"][k] for k in ["for_iter_confusion", "orphan_raises", "while_true_pass"]):
        print("✅ ALL SEMANTIC ERROR PATTERNS CLEAR")
    else:
        print("❌ SEMANTIC ERRORS DETECTED — see above")


if __name__ == "__main__":
    main()
