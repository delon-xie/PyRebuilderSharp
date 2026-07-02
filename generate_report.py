#!/usr/bin/env python3
import json
from collections import defaultdict
from pathlib import Path

REPORTS_DIR = Path("docs")

def load_results():
    with open(REPORTS_DIR / "baseline_results.json", 'r') as f:
        return json.load(f)

def analyze_results(results):
    by_version = defaultdict(list)
    by_category = defaultdict(list)
    version_stats = defaultdict(lambda: {"total": 0, "ok": 0, "syntax_error": 0, "runtime_error": 0, "control_block_anomaly": 0, "orphan_block": 0, "decompile_failure": 0})
    
    for result in results:
        version = result["version"]
        category = result["error_category"]
        
        by_version[version].append(result)
        by_category[category].append(result)
        
        version_stats[version]["total"] += 1
        version_stats[version][category] += 1
    
    return by_version, by_category, version_stats

def generate_markdown(results, by_version, by_category, version_stats):
    versions = sorted(version_stats.keys(), key=lambda v: (float(v.split('.')[0]), float(v.split('.')[1])))
    
    md = "# 白盒测试基线评估报告\n\n"
    md += f"**生成时间**: 2026-07-02\n"
    md += f"**测试文件总数**: {len(results)}\n\n"
    
    md += "## 一、总体概览\n\n"
    md += "### 1.1 版本分布\n\n"
    md += "| Python 版本 | 文件数 | 完全通过 | 语法错误 | 运行时错误 | 控制块异常 | 孤儿块 | 反编译失败 |\n"
    md += "|------------|--------|----------|----------|------------|------------|--------|------------|\n"
    
    total_ok = 0
    total_files = len(results)
    
    for version in versions:
        stats = version_stats[version]
        ok_count = stats["ok"]
        total_ok += ok_count
        md += f"| {version} | {stats['total']} | {ok_count} | {stats['syntax_error']} | {stats['runtime_error']} | {stats['control_block_anomaly']} | {stats['orphan_block']} | {stats['decompile_failure']} |\n"
    
    md += f"| **总计** | {total_files} | - | - | - | - | - |\n\n"
    
    md += f"### 1.2 总体通过率\n\n"
    md += f"- **完全通过**: {total_ok}/{total_files} ({(total_ok/total_files*100):.1f}%)\n"
    md += f"- **语法错误**: {len(by_category.get('syntax_error', []))} ({(len(by_category.get('syntax_error', []))/total_files*100):.1f}%)\n"
    md += f"- **运行时错误**: {len(by_category.get('runtime_error', []))} ({(len(by_category.get('runtime_error', []))/total_files*100):.1f}%)\n"
    md += f"- **控制块异常**: {len(by_category.get('control_block_anomaly', []))} ({(len(by_category.get('control_block_anomaly', []))/total_files*100):.1f}%)\n"
    md += f"- **孤儿块**: {len(by_category.get('orphan_block', []))} ({(len(by_category.get('orphan_block', []))/total_files*100):.1f}%)\n"
    md += f"- **反编译失败**: {len(by_category.get('decompile_failure', []))} ({(len(by_category.get('decompile_failure', []))/total_files*100):.1f}%)\n\n"
    
    md += "## 二、按优先级分类的问题分析\n\n"
    md += "### 2.1 控制块异常（最高优先级）\n\n"
    control_issues = by_category.get('control_block_anomaly', [])
    md += f"**影响文件数**: {len(control_issues)}\n\n"
    if control_issues:
        md += "| 文件 | 版本 | 问题类型 |\n"
        md += "|------|------|----------|\n"
        for issue in control_issues[:20]:
            patterns = issue.get('patterns', [])
            pattern_types = ', '.join([p['type'] for p in patterns])
            md += f"| {issue['filename']} | {issue['version']} | {pattern_types} |\n"
        if len(control_issues) > 20:
            md += f"| ... | ... | 共 {len(control_issues)} 个文件 |\n"
    
    md += "\n### 2.2 语法错误\n\n"
    syntax_issues = by_category.get('syntax_error', [])
    md += f"**影响文件数**: {len(syntax_issues)}\n\n"
    if syntax_issues:
        md += "| 文件 | 版本 | 错误详情 |\n"
        md += "|------|------|----------|\n"
        for issue in syntax_issues[:20]:
            error = issue.get('syntax_error', '')[:50]
            md += f"| {issue['filename']} | {issue['version']} | {error} |\n"
        if len(syntax_issues) > 20:
            md += f"| ... | ... | 共 {len(syntax_issues)} 个文件 |\n"
    
    md += "\n### 2.3 孤儿块\n\n"
    orphan_issues = by_category.get('orphan_block', [])
    md += f"**影响文件数**: {len(orphan_issues)}\n\n"
    if orphan_issues:
        md += "| 文件 | 版本 | 问题类型 |\n"
        md += "|------|------|----------|\n"
        for issue in orphan_issues[:20]:
            patterns = issue.get('patterns', [])
            pattern_types = ', '.join([p['type'] for p in patterns])
            md += f"| {issue['filename']} | {issue['version']} | {pattern_types} |\n"
        if len(orphan_issues) > 20:
            md += f"| ... | ... | 共 {len(orphan_issues)} 个文件 |\n"
    
    md += "\n### 2.4 运行时错误\n\n"
    runtime_issues = by_category.get('runtime_error', [])
    md += f"**影响文件数**: {len(runtime_issues)}\n\n"
    if runtime_issues:
        md += "| 文件 | 版本 | 错误详情 |\n"
        md += "|------|------|----------|\n"
        for issue in runtime_issues[:20]:
            error = issue.get('runtime_error', '')[:50]
            md += f"| {issue['filename']} | {issue['version']} | {error} |\n"
        if len(runtime_issues) > 20:
            md += f"| ... | ... | 共 {len(runtime_issues)} 个文件 |\n"
    
    md += "\n### 2.5 反编译失败\n\n"
    decompile_issues = by_category.get('decompile_failure', [])
    md += f"**影响文件数**: {len(decompile_issues)}\n\n"
    if decompile_issues:
        md += "| 文件 | 版本 | 错误详情 |\n"
        md += "|------|------|----------|\n"
        for issue in decompile_issues[:20]:
            error = issue.get('decompile_error', '')[:50]
            md += f"| {issue['filename']} | {issue['version']} | {error} |\n"
        if len(decompile_issues) > 20:
            md += f"| ... | ... | 共 {len(decompile_issues)} 个文件 |\n"
    
    md += "\n## 三、问题模式统计\n\n"
    pattern_counts = defaultdict(int)
    for result in results:
        for pattern in result.get('patterns', []):
            pattern_counts[pattern['type']] += pattern['count']
    
    md += "| 问题模式 | 出现次数 | 严重程度 |\n"
    md += "|----------|----------|----------|\n"
    severity_map = {
        "try_no_except_finally": "高",
        "for_empty": "高",
        "empty_try": "高",
        "orphan_raise": "中",
        "bare_elem": "中",
        "bare_list": "中",
        "stray_pass": "低"
    }
    for pattern_type, count in sorted(pattern_counts.items(), key=lambda x: -x[1]):
        severity = severity_map.get(pattern_type, "未知")
        md += f"| {pattern_type} | {count} | {severity} |\n"
    
    md += "\n## 四、修复计划\n\n"
    md += "### 4.1 P0 - 紧急修复（影响面大）\n\n"
    md += "1. **修复 Python 3.13/3.14 列表推导式和 for 循环重构**\n"
    md += "   - 问题: `_repr_iterable` 等函数出现 `elem`, `[]`, `for _ in []` 等异常输出\n"
    md += "   - 原因: `LOAD_FAST_AND_CLEAR` 和超级指令处理不完整\n"
    md += "   - 影响: 3.13/3.14 的 reprlib 等核心库函数\n"
    md += "\n2. **修复 try 块无 except/finally 问题**\n"
    md += "   - 问题: 反编译输出包含 `try:` 但没有 except/finally\n"
    md += "   - 原因: 异常表解析和控制流图重建不完整\n"
    md += "   - 影响: 所有版本的异常处理\n"
    md += "\n### 4.2 P1 - 重要修复（控制块异常）\n\n"
    md += "3. **修复 for 循环空迭代器问题**\n"
    md += "   - 问题: `for _ in []:` 空循环\n"
    md += "   - 原因: 列表推导式重构失败\n"
    md += "\n4. **修复孤儿 raise 语句**\n"
    md += "   - 问题: 独立的 `raise` 语句\n"
    md += "   - 原因: 异常处理块重构不完整\n"
    md += "\n### 4.3 P2 - 次要修复（孤儿块）\n\n"
    md += "5. **清理裸表达式**\n"
    md += "   - 问题: `elem`, `[]` 等裸表达式\n"
    md += "   - 原因: 栈机状态管理问题\n"
    md += "\n6. **清理多余 pass 语句**\n"
    md += "   - 问题: 控制流语句前的多余 pass\n"
    md += "\n### 4.4 P3 - 优化（反编译失败）\n\n"
    md += "7. **处理特殊 .pyc 文件**\n"
    md += "   - 问题: 部分文件反编译失败\n"
    md += "   - 原因: 可能是 Python 2.5/2.6 等旧版本或特殊格式\n"
    md += "\n## 五、详细问题列表\n\n"
    md += "### 5.1 Python 3.14 问题\n\n"
    py314_issues = [r for r in results if r['version'] == '3.14' and r['error_category'] != 'ok']
    md += f"**问题文件数**: {len(py314_issues)}\n\n"
    if py314_issues:
        md += "| 文件 | 类别 |\n"
        md += "|------|------|\n"
        for issue in py314_issues[:30]:
            md += f"| {issue['filename']} | {issue['error_category']} |\n"
        if len(py314_issues) > 30:
            md += f"| ... | 共 {len(py314_issues)} 个文件 |\n"
    
    md += "\n### 5.2 Python 3.13 问题\n\n"
    py313_issues = [r for r in results if r['version'] == '3.13' and r['error_category'] != 'ok']
    md += f"**问题文件数**: {len(py313_issues)}\n\n"
    if py313_issues:
        md += "| 文件 | 类别 |\n"
        md += "|------|------|\n"
        for issue in py313_issues[:30]:
            md += f"| {issue['filename']} | {issue['error_category']} |\n"
        if len(py313_issues) > 30:
            md += f"| ... | 共 {len(py313_issues)} 个文件 |\n"
    
    return md

def main():
    results = load_results()
    by_version, by_category, version_stats = analyze_results(results)
    md = generate_markdown(results, by_version, by_category, version_stats)
    
    report_path = REPORTS_DIR / "baseline_evaluate_report_20260702_1.md"
    with open(report_path, 'w') as f:
        f.write(md)
    
    print(f"报告已生成: {report_path}")

if __name__ == "__main__":
    main()