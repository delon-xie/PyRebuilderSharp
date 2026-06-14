#!/usr/bin/env python3
"""
whitebox_test.py — 白盒反编译测试工具

单个文件白盒测试管道:
  1. 编译 .py → .pyc (指定 Python 版本)
  2. 反编译 .pyc → 源代码
  3. diff 对比原始 .py
  4. 输出差异报告

用法:
  python3 whitebox_test.py <input_dir> <filename> [version]
  
示例:
  python3 whitebox_test.py ../test_data/input abc.py 3.10
  python3 whitebox_test.py ../test_data/input abc.py all    # 2.7-3.14 全部版本
"""

import subprocess, os, sys, tempfile, re
from pathlib import Path

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_PROJECT = os.path.join(PROJECT_DIR, "src/PyRebuilderSharp.Cli")
INPUT_DIR = os.path.join(PROJECT_DIR, "test_data/input")
COMPILED_DIR = os.path.join(PROJECT_DIR, "test_data/compiled")

# 可用的 Python 版本（通过 pyenv 管理）
PYTHON_VERSIONS = ["2.7", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]

def get_python(version):
    """获取指定版本 Python 可执行文件路径"""
    pyenv_root = os.environ.get("PYENV_ROOT", os.path.expanduser("~/.pyenv"))
    versions_dir = os.path.join(pyenv_root, "versions")
    # 查找匹配版本前缀的 pyenv 目录（如 "3.10" 匹配 "3.10.20"）
    if os.path.exists(versions_dir):
        for d in sorted(os.listdir(versions_dir), reverse=True):
            if d.startswith(version):
                candidate = os.path.join(versions_dir, d, "bin/python")
                if os.path.exists(candidate):
                    return candidate
    # 回退到 PATH 查找
    r = subprocess.run(["which", f"python{version}"], capture_output=True, text=True)
    if r.returncode == 0:
        return r.stdout.strip()
    return f"python{version}"

def compile_file(source_path, version, output_path):
    """编译单个 .py 文件为 .pyc"""
    py = get_python(version)
    code = f"""
import py_compile, sys
try:
    py_compile.compile({repr(source_path)}, {repr(output_path)}, doraise=True)
    print("OK")
except py_compile.PyCompileError as e:
    print(f"FAIL: {{e}}")
"""
    r = subprocess.run([py, "-c", code], capture_output=True, text=True, timeout=30)
    if "FAIL" in r.stdout:
        return False, r.stdout.strip()
    return True, r.stdout.strip()

def decompile_file(pyc_path):
    """反编译 .pyc 文件"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        out_path = f.name
    
    r = subprocess.run(
        ["dotnet", "run", "--project", CLI_PROJECT, "-c", "Release", "--", pyc_path],
        capture_output=True, text=True, timeout=60,
        cwd=PROJECT_DIR
    )
    
    # 只保存 stdout（源代码），丢弃 stderr（警告/调试信息）
    with open(out_path, 'w') as f:
        f.write(r.stdout)
    
    return out_path

def strip_known_diffs(text):
    """移除已知的不可消除差异（版权注释、反编译头等）"""
    lines = text.split('\n')
    filtered = []
    for line in lines:
        # 跳过反编译头
        if line.startswith('# Decompiled from:'):
            continue
        # 跳过孤儿块注释
        if line.strip().startswith('# orphan @'):
            continue
        # 跳过 SUMMARY
        if line.strip().startswith('# [SUMMARY]'):
            continue
        # 跳过版权注释
        if line.strip().startswith('# Copyright'):
            continue
        if line.strip().startswith('# Licensed to'):
            continue
        filtered.append(line)
    return '\n'.join(filtered)

def diff_files(original_path, decompiled_path):
    """diff 对比"""
    with open(original_path) as f:
        original = f.read()
    with open(decompiled_path) as f:
        decompiled = f.read()
    
    # 去除不可比差异
    original_clean = strip_known_diffs(original)
    decompiled_clean = strip_known_diffs(decompiled)
    
    # 写临时文件用于 diff
    with tempfile.NamedTemporaryFile(mode='w', suffix='.orig', delete=False) as f:
        f.write(original_clean)
        orig_tmp = f.name
    with tempfile.NamedTemporaryFile(mode='w', suffix='.decomp', delete=False) as f:
        f.write(decompiled_clean)
        dec_tmp = f.name
    
    r = subprocess.run(
        ["diff", orig_tmp, dec_tmp],
        capture_output=True, text=True, timeout=10
    )
    
    os.unlink(orig_tmp)
    os.unlink(dec_tmp)
    
    return r.returncode, r.stdout

def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print("用法: whitebox_test.py <filename> [version]")
        print("       whitebox_test.py abc.py 3.10")
        sys.exit(1)
    
    filename = args[0]
    version = args[1] if len(args) > 1 else "3.10"
    
    # 文件名路径
    source_path = os.path.join(INPUT_DIR, filename)
    if not os.path.exists(source_path):
        # 尝试 test_data/input/ 下
        alt = os.path.join(PROJECT_DIR, "test_data/input", filename)
        if os.path.exists(alt):
            source_path = alt
        else:
            print(f"❌ Source not found: {source_path}")
            sys.exit(1)
    
    if version == "all":
        versions = PYTHON_VERSIONS
    else:
        versions = [version]
    
    for ver in versions:
        base = os.path.splitext(filename)[0]
        pyc_path = os.path.join(COMPILED_DIR, f"{base}.{ver}.pyc")
        
        print(f"\n{'='*60}")
        print(f"📦 {filename}  →  Python {ver}")
        print(f"{'='*60}")
        
        # 1. 编译
        print(f"  编译...", end=" ", flush=True)
        ok, msg = compile_file(source_path, ver, pyc_path)
        if not ok:
            print(f"❌ {msg}")
            continue
        print(f"✅")
        
        # 2. 反编译
        print(f"  反编译...", end=" ", flush=True)
        dec_file = decompile_file(pyc_path)
        
        # 统计行数
        with open(dec_file) as f:
            dec_lines = f.read().count('\n')
        with open(source_path) as f:
            src_lines = f.read().count('\n')
        print(f"✅ ({dec_lines} 行, 源: {src_lines} 行)")
        
        # 3. diff
        rc, diff_output = diff_files(source_path, dec_file)
        if rc == 0:
            print(f"  diff: ✅ 一致")
        else:
            diff_lines = diff_output.count('\n')
            print(f"  diff: ⚠️ {diff_lines} 行差异")
            # 显示前 30 行 diff
            for line in diff_output.split('\n')[:30]:
                print(f"    {line}")
        
        os.unlink(dec_file)

if __name__ == "__main__":
    main()
