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
            while j < len(lines) and j < i + 30:
                next_line = lines[j]
                
                # 检查是否是下一个测试（以 *** 开头）
                if next_line.startswith('***'):
                    break
                
                # 检查是否是文件行（以空格开头并包含 .pyc）
                if next_line.strip().startswith(' ') and '.pyc' in next_line:
                    # 提取版本号（支持多种格式）
                    version_match = re.search(r'\.(\d+\.\d+)\.pyc', next_line)
                    if version_match:
                        version = version_match.group(1)
                        
                        # 只统计 3.7-3.10 版本
                        if version in ['3.7', '3.8', '3.9', '3.10']:
                            version_stats[version]['total'] += 1
                            if status == 'PASS':
                                version_stats[version]['passed'] += 1
                            else:
                                version_stats[version]['failed'] += 1
                
                j += 1
    
    i += 1

# 打印统计结果
print("=" * 70)
print("Python 3.7-3.10 版本测试通过率统计")
print("=" * 70)
print(f"{'版本':<12} {'通过':<10} {'失败':<10} {'总计':<10} {'通过率':<12}")
print("-" * 70)

total_passed = 0
total_failed = 0
total = 0

for version in sorted(version_stats.keys()):
    stats = version_stats[version]
    t = stats['total']
    p = stats['passed']
    f = stats['failed']
    rate = (p / t * 100) if t > 0 else 0
    
    total_passed += p
    total_failed += f
    total += t
    
    print(f"Python {version:<5} {p:<10} {f:<10} {t:<10} {rate:>8.1f}%")

print("-" * 70)
overall_rate = (total_passed / total * 100) if total > 0 else 0
print(f"{'总计':<12} {total_passed:<10} {total_failed:<10} {total:<10} {overall_rate:>8.1f}%")
print("=" * 70)
