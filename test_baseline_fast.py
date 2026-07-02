#!/usr/bin/env python3
import os
import sys
import subprocess
import py_compile
import tempfile
import json
import re
from pathlib import Path

TEST_DATA_DIR = Path("test_data/compiled")
REPORTS_DIR = Path("docs")
REPORTS_DIR.mkdir(exist_ok=True)

DECOMPILER_PATH = "src/PyRebuilderSharp.CLI/PyRebuilderSharp.CLI.csproj"

KNOWN_PATTERNS = {
    "orphan_raise": re.compile(r"(?<!\n)^\s*raise(?!\s+)", re.MULTILINE),
    "bare_elem": re.compile(r"(?<!\w)\belem\b(?!\s*=)", re.MULTILINE),
    "bare_list": re.compile(r"(?<!\w)\[\]\s*(?!=)", re.MULTILINE),
    "empty_try": re.compile(r"try:\s*\n\s*(?!except|finally)", re.MULTILINE),
    "try_no_except_finally": re.compile(r"try:\s*\n(?:(?!except|finally).)*?(?=\n\s*return|\n\s*def|\Z)", re.DOTALL),
    "for_empty": re.compile(r"for\s+\w+\s+in\s+\[\]:", re.MULTILINE),
    "stray_pass": re.compile(r"(?<!\n)\s*pass\s*(?=\n\s*(?:if|for|while|return|def))", re.MULTILINE),
}

KEY_FILES = [
    "reprlib.3.14.pyc",
    "reprlib.3.13.pyc",
    "reprlib.3.12.pyc",
    "reprlib.3.11.pyc",
    "reprlib.3.10.pyc",
    "pprint.3.14.pyc",
    "pprint.3.13.pyc",
    "test_with_simple.3.14.pyc",
    "test_with_simple.3.13.pyc",
    "test_with_simple.3.12.pyc",
    "test_with_simple.3.11.pyc",
    "test_with_simple.3.10.pyc",
    "test_with_pass.3.14.pyc",
    "test_with_pass.3.13.pyc",
    "test_with_pass.3.12.pyc",
    "test_with_pass.3.11.pyc",
    "test_try.3.13.pyc",
    "test_break_for.3.14.pyc",
    "test_break_for.3.13.pyc",
    "test_break_for.3.12.pyc",
    "test_break_for.3.11.pyc",
    "test_minimal_if.3.14.pyc",
    "test_minimal_if.3.13.pyc",
    "test_minimal_if.3.12.pyc",
    "test_minimal_if.3.11.pyc",
    "test_syntax.3.14.pyc",
    "test_syntax.3.13.pyc",
    "test_syntax.3.12.pyc",
    "test_syntax.3.11.pyc",
    "test_yield_simple.3.13.pyc",
    "test_for_try.3.12.pyc",
    "test_try_for2.3.12.pyc",
    "abc.3.14.pyc",
    "abc.3.13.pyc",
    "abc.3.12.pyc",
    "enum.3.14.pyc",
    "enum.3.13.pyc",
    "mixed5_out.3.14.pyc",
    "mixed5_out.3.13.pyc",
    "mixed5_out.3.12.pyc",
    "mixed5_out.3.11.pyc",
    "expr_test.3.14.pyc",
    "expr_test.3.13.pyc",
    "expr_test.3.12.pyc",
    "expr_test.3.11.pyc",
    "run_lv2.3.14.pyc",
    "run_lv2.3.13.pyc",
    "run_lv2.3.12.pyc",
    "debug_blocks.3.14.pyc",
    "debug_blocks.3.13.pyc",
    "debug_blocks.3.12.pyc",
    "compare_ast.3.14.pyc",
    "compare_ast.3.13.pyc",
    "compare_ast.3.12.pyc",
    "test_with_deref.3.14.pyc",
    "test_with_deref.3.13.pyc",
    "test_h_only.3.14.pyc",
]

def decompile_file(pyc_path, output_path):
    try:
        result = subprocess.run(
            ["dotnet", "run", "--project", DECOMPILER_PATH, "--", "-f", str(pyc_path), "-o", str(output_path)],
            capture_output=True, text=True, timeout=120
        )
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def check_syntax(file_path):
    try:
        py_compile.compile(str(file_path), doraise=True)
        return True, None
    except py_compile.PyCompileError as e:
        return False, str(e)

def check_import(file_path):
    try:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        sys.path.insert(0, str(file_path.parent))
        __import__(module_name)
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        if str(file_path.parent) in sys.path:
            sys.path.remove(str(file_path.parent))

def scan_patterns(content):
    issues = []
    for pattern_name, pattern in KNOWN_PATTERNS.items():
        matches = pattern.findall(content)
        if matches:
            issues.append({
                "type": pattern_name,
                "count": len(matches),
                "examples": matches[:3]
            })
    return issues

def extract_version(filename):
    match = re.search(r"\.3\.(\d+)\.pyc$", filename)
    if match:
        return f"3.{match.group(1)}"
    match = re.search(r"\.2\.7\.pyc$", filename)
    if match:
        return "2.7"
    return "unknown"

def classify_error(syntax_ok, runtime_ok, patterns):
    if not syntax_ok:
        return "syntax_error"
    if not runtime_ok:
        return "runtime_error"
    has_control_flow = any(p["type"] in ["try_no_except_finally", "for_empty", "empty_try"] for p in patterns)
    if has_control_flow:
        return "control_block_anomaly"
    has_orphan = any(p["type"] in ["orphan_raise", "bare_elem", "bare_list", "stray_pass"] for p in patterns)
    if has_orphan:
        return "orphan_block"
    return "ok"

def main():
    results = []
    total_files = len(KEY_FILES)
    
    print(f"Testing {total_files} key files")
    
    for i, filename in enumerate(KEY_FILES, 1):
        pyc_path = TEST_DATA_DIR / filename
        if not pyc_path.exists():
            print(f"[{i}/{total_files}] Skipping {filename} (not found)")
            continue
        
        print(f"[{i}/{total_files}] Processing {filename}")
        
        version = extract_version(filename)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            output_path = Path(f.name)
        
        decompile_ok, decompile_err = decompile_file(pyc_path, output_path)
        
        if not decompile_ok:
            results.append({
                "filename": filename,
                "version": version,
                "decompile_ok": False,
                "decompile_error": decompile_err,
                "syntax_ok": False,
                "runtime_ok": False,
                "error_category": "decompile_failure",
                "patterns": [],
                "snippet": ""
            })
            os.unlink(output_path)
            continue
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        syntax_ok, syntax_err = check_syntax(output_path)
        runtime_ok, runtime_err = check_import(output_path) if syntax_ok else (False, "Syntax error")
        
        patterns = scan_patterns(content)
        error_category = classify_error(syntax_ok, runtime_ok, patterns)
        
        snippet = content[:500] if len(content) > 500 else content
        
        results.append({
            "filename": filename,
            "version": version,
            "decompile_ok": True,
            "decompile_error": "",
            "syntax_ok": syntax_ok,
            "syntax_error": syntax_err,
            "runtime_ok": runtime_ok,
            "runtime_error": runtime_err,
            "error_category": error_category,
            "patterns": patterns,
            "snippet": snippet
        })
        
        os.unlink(output_path)
    
    with open(REPORTS_DIR / "baseline_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {REPORTS_DIR / 'baseline_results.json'}")
    
    return results

if __name__ == "__main__":
    main()