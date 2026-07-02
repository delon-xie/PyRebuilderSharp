#!/usr/bin/env python3
"""
batch_compile_pyc.py — 批量编译所有 .py 测试文件到各版本 .pyc

用法: python3 batch_compile_pyc.py
输出: compiled/<test_name>.<version>.pyc

使用 ~/.pyenv/versions/ 下的所有可用 Python 版本编译。
"""

import os
import sys
import subprocess

INPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'input')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'compiled')
PYENV_ROOT = os.path.expanduser("~/.pyenv/versions")

PYTHON_VERSIONS = [
    ("2.7.18", "2.7"),
    ("3.5.10", "3.5"),
    ("3.6.15", "3.6"),
    ("3.7.17", "3.7"),
    ("3.8.20", "3.8"),
    ("3.9.25", "3.9"),
    ("3.10.20", "3.10"),
    ("3.11.15", "3.11"),
    ("3.12.13", "3.12"),
    ("3.13.12", "3.13"),
    ("3.14.3", "3.14"),
]

compile_script = """
import py_compile, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    py_compile.compile(src, cfile=dst, doraise=True)
    size = len(open(dst, 'rb').read())
    print('OK:' + str(size))
except Exception as e:
    print('FAIL:' + str(e))
"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    py_files = []
    for root, dirs, files in os.walk(INPUT_DIR):
        for f in files:
            if f.endswith('.py') and not f.startswith('_'):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, INPUT_DIR)
                py_files.append((full_path, rel_path))
    
    py_files.sort()
    print(f"找到 {len(py_files)} 个 .py 测试文件")
    
    available_pythons = []
    for ver_full, ver_tag in PYTHON_VERSIONS:
        py = os.path.join(PYENV_ROOT, ver_full, "bin", "python")
        if os.path.isfile(py):
            available_pythons.append((ver_full, ver_tag, py))
        else:
            print(f"SKIP {ver_full} (not found)")
    
    print(f"可用 Python 版本: {len(available_pythons)}")
    
    total_compiled = 0
    total_skipped = 0
    total_failed = 0
    
    for full_path, rel_path in py_files:
        basename = os.path.splitext(rel_path)[0].replace('/', '.')
        
        for ver_full, ver_tag, py in available_pythons:
            outc = os.path.join(OUTPUT_DIR, f"{basename}.{ver_tag}.pyc")
            
            if os.path.exists(outc):
                total_skipped += 1
                continue
            
            print(f"COMPILE {ver_tag}: {basename} ", end="")
            sys.stdout.flush()
            
            result = subprocess.run(
                [py, "-c", compile_script, full_path, outc],
                capture_output=True, text=True, timeout=60
            )
            
            out = (result.stdout + result.stderr).strip()
            if out.startswith('OK'):
                print(f"OK ({out.split(':')[1]} bytes)")
                total_compiled += 1
            else:
                print(f"FAIL: {out}")
                total_failed += 1
    
    print(f"\n完成:")
    print(f"  编译成功: {total_compiled}")
    print(f"  跳过(已存在): {total_skipped}")
    print(f"  编译失败: {total_failed}")

if __name__ == '__main__':
    main()
