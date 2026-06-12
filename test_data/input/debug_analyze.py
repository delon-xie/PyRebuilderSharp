#!/usr/bin/env python3
import re
from collections import defaultdict

# 读取测试输出
with open('/tmp/test_full.txt', 'r') as f:
    output = f.read()

# 按版本统计
version_stats = defaultdict(lambda: {'total': 0, 'passed': 0, 'failed': 0})

# 解析测试结果
lines = output.split('\n')
i = 0
debug_count = 0

while i < len(lines):
    line = lines[i]
    
    # 匹配测试结果行
    if '***' in line and ':' in line:
        match = re.search(r'\*\*\*\s+([^:]+):\s+(PASS|FAIL)', line)
        if match:
            test_name = match.group(1)
            status = match.group(2)
            
            # 查找接下来的 pyc 文件行
            j = i + 1
            found_versions = []
            while j < len(lines) and j < i + 30:
                next_line = lines[j]
                
                # 检查是否是下一个测试（以 *** 开头）
                if next_line.startswith('***'):
                    break
                
                # 检查是否是文件行（以空格开头并包含 .pyc）
                if '.pyc' in next_line and not next_line.startswith('***'):
                    # 提取版本号（支持多种格式）
                    version_match = re.search(r'\.(\d+\.\d+)\.pyc', next_line)
                    if version_match:
                        version = version_match.group(1)
                        found_versions.append((version, next_line.strip()))
                
                j += 1
            
            # 统计找到的版本
            if found_versions:
                debug_count += 1
                if debug_count <= 5:  # 只打印前5个
                    print(f"Test: {test_name}, Status: {status}")
                    for v, line_text in found_versions:
                        print(f"  Found version: {v} in: {line_text}")
                    print()
    
    i += 1

print(f"Total tests with versions found: {debug_count}")
