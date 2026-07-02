#!/usr/bin/env python3
"""
verify_pyc_matrix.py — 验证测试数据完整性
"""

import os
import glob

COMPILED_DIR = os.path.join(os.path.dirname(__file__), '..', 'compiled')
INPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'input')

EXPECTED_VERSIONS = [
    "2.7", "3.5", "3.6", "3.7", "3.8", "3.9",
    "3.10", "3.11", "3.12", "3.13", "3.14",
]

def main():
    py_files = []
    for root, dirs, files in os.walk(INPUT_DIR):
        for f in files:
            if f.endswith('.py') and not f.startswith('_'):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, INPUT_DIR)
                basename = os.path.splitext(rel_path)[0].replace('/', '.')
                py_files.append(basename)
    
    py_files.sort()
    
    existing_pyc = {}
    for pyc_file in glob.glob(os.path.join(COMPILED_DIR, '*.pyc')):
        filename = os.path.basename(pyc_file)
        name_without_ext = os.path.splitext(filename)[0]
        parts = name_without_ext.split('.')
        if len(parts) >= 3 and parts[-2].isdigit() and parts[-1].isdigit():
            ver = f"{parts[-2]}.{parts[-1]}"
            test_name = '.'.join(parts[:-2])
            if test_name not in existing_pyc:
                existing_pyc[test_name] = set()
            existing_pyc[test_name].add(ver)
    
    print(f"测试文件数: {len(py_files)}")
    print(f"已编译 .pyc 覆盖测试数: {len(existing_pyc)}")
    print(f"期望版本: {', '.join(EXPECTED_VERSIONS)}")
    print()
    
    missing_count = 0
    for test_name in py_files:
        available = existing_pyc.get(test_name, set())
        missing = [v for v in EXPECTED_VERSIONS if v not in available]
        if missing:
            print(f"  {test_name}: 缺少 {', '.join(missing)}")
            missing_count += len(missing)
    
    print(f"\n总计缺少: {missing_count} 个版本")
    
    print("\n版本分布统计:")
    for ver in EXPECTED_VERSIONS:
        count = sum(1 for versions in existing_pyc.values() if ver in versions)
        print(f"  {ver}: {count} 个测试")

if __name__ == '__main__':
    main()
