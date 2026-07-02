#!/usr/bin/env python3
"""
unify_pyc_names.py — 统一 .pyc 文件版本命名规则
"""

import os
import re

COMPILED_DIR = os.path.join(os.path.dirname(__file__), '..', 'compiled')

def parse_filename(filename):
    """解析文件名，提取 test_name 和版本信息"""
    name_without_ext = os.path.splitext(filename)[0]
    
    match = re.match(r'^(.+)\.cpython-(\d+)$', name_without_ext)
    if match:
        ver_str = match.group(2)
        major = ver_str[0]
        minor = ver_str[1:]
        return match.group(1), f"{major}.{minor}"
    
    parts = name_without_ext.split('.')
    
    if len(parts) >= 3:
        if parts[-2].isdigit() and parts[-1].isdigit():
            ver = f"{parts[-2]}.{parts[-1]}"
            if ver.startswith('3.') or ver == '2.7':
                return '.'.join(parts[:-2]), ver
    
    if len(parts) >= 2:
        last_part = parts[-1]
        if len(last_part) == 2 and last_part.isdigit():
            if last_part.startswith('3'):
                return '.'.join(parts[:-1]), f"3.{last_part[1]}"
            elif last_part == '27':
                return '.'.join(parts[:-1]), '2.7'
        elif len(last_part) == 3 and last_part.startswith('3'):
            return '.'.join(parts[:-1]), f"3.{last_part[1:]}"
    
    match = re.match(r'^(.+?)(\d{2,3})$', name_without_ext)
    if match:
        ver_str = match.group(2)
        test_name = match.group(1).rstrip('.')
        if ver_str.startswith('3'):
            if len(ver_str) == 2:
                return test_name, f"3.{ver_str[1]}"
            elif len(ver_str) == 3:
                return test_name, f"3.{ver_str[1:]}"
        elif ver_str == '27':
            return test_name, '2.7'
    
    return name_without_ext, None

def main():
    os.chdir(os.path.dirname(__file__))
    compiled_dir = COMPILED_DIR
    
    if not os.path.exists(compiled_dir):
        print(f"ERROR: Compiled directory not found: {compiled_dir}")
        return
    
    files = os.listdir(compiled_dir)
    pyc_files = [f for f in files if f.endswith('.pyc')]
    
    renamed_count = 0
    skipped_count = 0
    errors = []
    
    for filename in pyc_files:
        test_name, version = parse_filename(filename)
        
        if version is None:
            errors.append(f"无法解析版本: {filename}")
            continue
        
        expected_name = f"{test_name}.{version}.pyc"
        current_path = os.path.join(compiled_dir, filename)
        expected_path = os.path.join(compiled_dir, expected_name)
        
        if filename == expected_name:
            skipped_count += 1
            continue
        
        if os.path.exists(expected_path):
            print(f"WARNING: {expected_name} 已存在，跳过 {filename}")
            continue
        
        os.rename(current_path, expected_path)
        print(f"RENAME: {filename} -> {expected_name}")
        renamed_count += 1
    
    print(f"\n完成:")
    print(f"  重命名: {renamed_count}")
    print(f"  跳过(已标准格式): {skipped_count}")
    if errors:
        print(f"  错误: {len(errors)}")
        for e in errors[:20]:
            print(f"    {e}")
        if len(errors) > 20:
            print(f"    ... 还有 {len(errors) - 20} 个错误")

if __name__ == '__main__':
    main()
