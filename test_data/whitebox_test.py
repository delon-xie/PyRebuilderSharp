#!/usr/bin/env python3
"""白盒测试脚本：批量反编译 .pyc 并检测问题"""
import subprocess
import os
import sys
import re
from collections import defaultdict

COMPILED_DIR = "test_data/compiled"
DECOMPILED_DIR = "test_data/whitebox_output"
DOTNET_CMD = ["dotnet", "src/PyRebuilderSharp.Cli/bin/Release/net10.0/PyRebuilderSharp.Cli.dll"]
BUILD_CMD = ["dotnet", "build", "-c", "Release"]

# 代表性测试文件（覆盖各控制结构）
TEST_FILES = [
    # 基础表达式
    "actual_expr", "expr_test", "expr_bs", "return_test",
    # if/else
    "if_else", "test_minimal_if", "name_main_guard", "name_main_else",
    # 循环
    "loop_else", "loop_else_simple", "test_break_for", "test_continue_for",
    "test_just_for", "actual_lv2",
    # try/except
    "test_try", "test_try_simple", "test_try_complex", "try_else",
    "l2_exception", "test_for_try",
    # with
    "test_with",
    # 函数
    "test_simple_def", "test_multi_func", "defaults_test", "l4_function",
    # class
    "test_cls", "test_cls2", "l5_class",
    # comprehension
    "test_comp", "test_nested_comp", "test_simple_comp",
    # yield/gen
    "test_yield_gen", "test_yield_simple",
    # match
    "match_simple", "match_full",
    # async
    "test_async",
    # levels
    "l0_basic", "l1_control", "l3_lambda", "l6_advanced",
    "l7_edge", "l8_complex", "l9_ultimate",
    # 标准库
    "abc", "enum", "functools", "reprlib", "dataclasses",
]

VERSIONS = ["2.7", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]


def build():
    """构建项目"""
    print("Building project...")
    result = subprocess.run(BUILD_CMD, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print("BUILD FAILED:")
        print(result.stderr[-2000:])
        return False
    print("Build OK")
    return True


def decompile(pyc_path):
    """反编译单个 pyc 文件，返回 (源代码, 错误列表)"""
    try:
        result = subprocess.run(
            DOTNET_CMD + [pyc_path],
            capture_output=True, text=True, timeout=30,
            cwd=os.getcwd()
        )
        stdout = result.stdout
        stderr = result.stderr
        # 从 stdout 提取源代码部分（跳过调试日志）
        lines = []
        for line in stdout.split('\n'):
            # 跳过调试日志行
            if line.startswith('[') and ']' in line:
                continue
            lines.append(line)
        source = '\n'.join(lines).strip()
        errors = []
        for line in stderr.split('\n'):
            if 'Error' in line or 'Exception' in line or 'error' in line.lower():
                if 'warning' not in line.lower():
                    errors.append(line.strip())
        return source, errors
    except subprocess.TimeoutExpired:
        return "", ["TIMEOUT"]
    except Exception as e:
        return "", [str(e)]


def check_syntax(source):
    """检查反编译输出的语法是否合法"""
    try:
        compile(source, '<decompiled>', 'exec')
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} (line {e.lineno})"


def analyze_output(source, filename, version):
    """分析反编译输出中的问题"""
    issues = []
    lines = source.split('\n')

    # 1. 语法检查
    ok, msg = check_syntax(source)
    if not ok:
        issues.append(("SYNTAX_ERROR", msg))

    # 2. 检测冗余代码模式
    # 2a. 重复的 pass 语句
    pass_count = sum(1 for l in lines if l.strip() == 'pass')
    if pass_count > 3:
        issues.append(("REDUNDANT_PASS", f"出现 {pass_count} 个 pass 语句"))

    # 2b. 裸表达式（可能是未正确处理的语句）
    bare_exprs = []
    for i, l in enumerate(lines):
        stripped = l.strip()
        if stripped and not stripped.startswith('#') and not stripped.startswith('def ') \
           and not stripped.startswith('class ') and not stripped.startswith('if ') \
           and not stripped.startswith('elif ') and not stripped.startswith('else:') \
           and not stripped.startswith('for ') and not stripped.startswith('while ') \
           and not stripped.startswith('try:') and not stripped.startswith('except') \
           and not stripped.startswith('finally:') and not stripped.startswith('return ') \
           and not stripped.startswith('import ') and not stripped.startswith('from ') \
           and not stripped.startswith('yield ') and not stripped.startswith('raise ') \
           and not stripped.startswith('with ') and not stripped.startswith('async ') \
           and not stripped.startswith('@') and not stripped.startswith('"""') \
           and not stripped.startswith("'''") and not stripped.startswith('#') \
           and '=' not in stripped and ':' not in stripped \
           and not stripped.startswith('pass') and not stripped.startswith('break') \
           and not stripped.startswith('continue') and not stripped.startswith('global ') \
           and not stripped.startswith('nonlocal ') and not stripped.startswith('assert ') \
           and not stripped.startswith('del ') and not stripped == '...' \
           and not stripped.startswith('match ') and not stripped.startswith('case '):
            # 可能是裸表达式
            if re.match(r'^[A-Za-z_]\w*$', stripped) or re.match(r'^[A-Za-z_]\w*\.', stripped):
                bare_exprs.append((i+1, stripped))
    if bare_exprs:
        issues.append(("BARE_EXPR", f"裸表达式: {bare_exprs[:3]}"))

    # 2c. 重复的 return None
    return_none_count = sum(1 for l in lines if l.strip() == 'return None')
    if return_none_count > 1:
        issues.append(("REDUNDANT_RETURN", f"出现 {return_none_count} 个 return None"))

    # 2d. 检测多余的 raise 语句
    raise_count = sum(1 for l in lines if l.strip() == 'raise')
    if raise_count > 2:
        issues.append(("REDUNDANT_RAISE", f"出现 {raise_count} 个裸 raise 语句"))

    # 2e. 检测 e = None 模式（try/except 清理代码泄漏）
    e_none_count = sum(1 for l in lines if re.match(r'^\s+\w+\s*=\s*None\s*$', l))
    if e_none_count > 1:
        issues.append(("CLEANUP_LEAK", f"出现 {e_none_count} 个变量=None 清理语句"))

    # 3. 检测控制结构完整性
    # 3a. try 块后缺少 except/finally
    try_lines = [i for i, l in enumerate(lines) if l.strip() == 'try:']
    for tl in try_lines:
        # 检查后续是否有 except 或 finally
        found_handler = False
        for j in range(tl+1, min(tl+50, len(lines))):
            if lines[j].strip().startswith('except') or lines[j].strip() == 'finally:':
                found_handler = True
                break
            if lines[j].strip() and not lines[j].startswith(' ') and not lines[j].startswith('\t'):
                break
        if not found_handler:
            issues.append(("TRY_NO_HANDLER", f"try 块(行{tl+1})后缺少 except/finally"))

    # 3b. 空 try 体
    for i, l in enumerate(lines):
        if l.strip() == 'try:' and i+1 < len(lines):
            next_line = lines[i+1].strip()
            if next_line == 'pass' or next_line == '':
                issues.append(("EMPTY_TRY", f"try 体为空(行{i+1})"))

    # 3c. else 块内容检查（try 的 else）
    for i, l in enumerate(lines):
        if l.strip() == 'else:' and i > 0:
            # 检查是否是 try 的 else（前文有 except）
            has_except_before = any(lines[j].strip().startswith('except') for j in range(max(0, i-20), i))
            if has_except_before:
                # else 块不应包含 finally 的内容
                for j in range(i+1, min(i+10, len(lines))):
                    if 'finally' in lines[j] and lines[j].strip().startswith('print'):
                        issues.append(("ELSE_CONTAINS_FINALLY", f"else 块(行{i+1})可能包含 finally 代码"))
                        break

    # 4. 检测 }} 等格式错误
    for i, l in enumerate(lines):
        if '}}' in l or '{{' in l:
            issues.append(("FORMAT_ERROR", f"格式错误(行{i+1}): {l.strip()}"))

    # 5. 检测未闭合的字符串
    for i, l in enumerate(lines):
        # 简单检查：行中有奇数个引号
        dq = l.count('"') - l.count('\\"')
        sq = l.count("'") - l.count("\\'")
        if dq % 2 != 0 and not l.strip().startswith('#') and '"""' not in l and "'''" not in l:
            issues.append(("UNCLOSED_STRING", f"可能未闭合字符串(行{i+1}): {l.strip()[:60]}"))

    return issues


def run_tests():
    """运行全部测试"""
    os.makedirs(DECOMPILED_DIR, exist_ok=True)

    results = {}  # (filename, version) -> {source, errors, issues}
    stats = defaultdict(int)
    version_stats = defaultdict(lambda: defaultdict(int))

    total = 0
    skipped = 0

    for fname in TEST_FILES:
        for ver in VERSIONS:
            pyc_path = os.path.join(COMPILED_DIR, f"{fname}.{ver}.pyc")
            if not os.path.exists(pyc_path):
                skipped += 1
                continue

            total += 1
            source, errors = decompile(pyc_path)

            if errors:
                issues = [("RUNTIME_ERROR", e) for e in errors[:3]]
            else:
                issues = analyze_output(source, fname, ver)

            key = (fname, ver)
            results[key] = {
                'source': source,
                'issues': issues,
            }

            # 保存反编译输出
            out_path = os.path.join(DECOMPILED_DIR, f"{fname}.{ver}.py")
            with open(out_path, 'w') as f:
                f.write(source)

            # 统计
            if not issues:
                stats['PASS'] += 1
                version_stats[ver]['PASS'] += 1
            else:
                stats['FAIL'] += 1
                version_stats[ver]['FAIL'] += 1
                for issue_type, _ in issues:
                    stats[issue_type] += 1
                    version_stats[ver][issue_type] += 1

    return results, stats, version_stats, total, skipped


def generate_report(results, stats, version_stats, total, skipped):
    """生成测试报告"""
    report = []
    report.append("=" * 80)
    report.append("PyRebuilderSharp 白盒测试报告")
    report.append("=" * 80)
    report.append("")

    # 1. 总体统计
    report.append("## 1. 总体统计")
    report.append(f"- 测试用例总数: {total}")
    report.append(f"- 跳过(无 pyc): {skipped}")
    report.append(f"- 通过: {stats['PASS']} ({stats['PASS']*100//max(total,1)}%)")
    report.append(f"- 失败: {stats['FAIL']} ({stats['FAIL']*100//max(total,1)}%)")
    report.append("")

    # 2. 各版本通过率
    report.append("## 2. 各版本通过率")
    report.append(f"{'版本':<10} {'通过':>6} {'失败':>6} {'通过率':>8}")
    report.append("-" * 35)
    for ver in VERSIONS:
        p = version_stats[ver]['PASS']
        f = version_stats[ver]['FAIL']
        t = p + f
        rate = f"{p*100//max(t,1)}%" if t > 0 else "N/A"
        report.append(f"{ver:<10} {p:>6} {f:>6} {rate:>8}")
    report.append("")

    # 3. 问题分类统计
    report.append("## 3. 问题分类统计")
    report.append(f"{'问题类型':<30} {'数量':>6}")
    report.append("-" * 40)
    issue_types = [(k, v) for k, v in sorted(stats.items()) if k not in ('PASS', 'FAIL')]
    for itype, count in sorted(issue_types, key=lambda x: -x[1]):
        report.append(f"{itype:<30} {count:>6}")
    report.append("")

    # 4. 失败用例详情
    report.append("## 4. 失败用例详情")
    report.append(f"{'文件':<25} {'版本':<8} {'问题类型':<25} {'详情'}")
    report.append("-" * 90)
    for (fname, ver), data in sorted(results.items()):
        if data['issues']:
            for itype, detail in data['issues']:
                report.append(f"{fname:<25} {ver:<8} {itype:<25} {detail[:50]}")
    report.append("")

    # 5. 代表性输出
    report.append("## 5. 代表性输出")
    representative = [
        ("test_try_simple", "3.14"),
        ("test_try", "3.10"),
        ("test_with", "3.14"),
        ("loop_else", "3.14"),
        ("if_else", "3.14"),
        ("test_cls", "3.14"),
        ("test_comp", "3.14"),
        ("test_async", "3.14"),
        ("l0_basic", "3.14"),
        ("l9_ultimate", "3.14"),
    ]
    for fname, ver in representative:
        key = (fname, ver)
        if key in results:
            report.append(f"### {fname} (Python {ver})")
            source = results[key]['source']
            if source:
                # 只显示前40行
                lines = source.split('\n')[:40]
                report.append("```python")
                report.extend(lines)
                if len(source.split('\n')) > 40:
                    report.append(f"# ... (共 {len(source.split(chr(10)))} 行)")
                report.append("```")
            else:
                report.append("(无输出)")
            if results[key]['issues']:
                for itype, detail in results[key]['issues']:
                    report.append(f"  - [{itype}] {detail}")
            report.append("")

    report.append("=" * 80)
    return '\n'.join(report)


def main():
    if not build():
        sys.exit(1)

    print("Running white-box tests...")
    results, stats, version_stats, total, skipped = run_tests()

    report = generate_report(results, stats, version_stats, total, skipped)

    # 保存报告
    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"test_data/whitebox_report_{date}.md"
    with open(report_path, 'w') as f:
        f.write(report)

    print(report)
    print(f"\n报告已保存到: {report_path}")


if __name__ == '__main__':
    main()
