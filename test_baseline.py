#!/usr/bin/env python3
"""
test_baseline.py — 全量白盒测试（基于 baseline_evaluate_all.py 改进版）
"""

import os, sys, subprocess, shutil, tempfile, collections, time, json, re, py_compile
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
CLI_PROJECT = str(PROJECT_DIR / "src/PyRebuilderSharp.CLI/PyRebuilderSharp.CLI.csproj")
INPUT_DIR = PROJECT_DIR / "test_data/input"
COMPILED_DIR = PROJECT_DIR / "test_data/compiled"
DECOMPILED_DIR = PROJECT_DIR / "test_data/decompiled"
REPORTS_DIR = PROJECT_DIR / "docs"
REPORTS_DIR.mkdir(exist_ok=True)

REPORT_DATE = "20260705_1"
REPORT_PATH = str(REPORTS_DIR / f"baseline_evaluate_report_{REPORT_DATE}.md")
RESULTS_PATH = str(REPORTS_DIR / "baseline_results.json")

VERSIONS = ["2.7", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]
KEY_FILES = ["abc.py", "ast.py", "enum.py", "re.py", "functools.py", "contextlib.py", "pprint.py", "dataclasses.py", "reprlib.py"]

KNOWN_PATTERNS = {
    "orphan_raise": re.compile(r"(?<!\n)^\s*raise(?!\s+)", re.MULTILINE),
    "bare_elem": re.compile(r"(?<!\w)\belem\b(?!\s*=)", re.MULTILINE),
    "bare_list": re.compile(r"^\s*\[\]\s*$", re.MULTILINE),
    "empty_try": re.compile(r"try:\s*\n\s*(?:pass\s*\n)?\s*(?=\n|$)", re.MULTILINE),
    "try_no_except_finally": re.compile(r"(?<![a-zA-Z])try:\s*\n(?:(?!except|finally).)*?(?=\n\s*return|\n\s*def|\Z)", re.DOTALL),
    "for_empty": re.compile(r"for\s+\w+\s+in\s+\[\]:", re.MULTILINE),
    "stray_pass": re.compile(r"(?<!\n)\s*pass\s*(?=\n\s*(?:if|for|while|return|def))", re.MULTILINE),
}

def ver_tag(ver):
    return f"v{ver.replace('.', '_')}"

def load_original(filename):
    path = INPUT_DIR / filename
    if path.exists():
        with open(path) as f:
            return f.read()
    return None

def strip_known_diffs(text):
    lines = text.split('\n')
    filtered = []
    for line in lines:
        sl = line.strip()
        if line.startswith('# Decompiled from:'): continue
        if sl.startswith('# orphan @'): continue
        if sl.startswith('# [SUMMARY]'): continue
        if sl.startswith('# Copyright'): continue
        if sl.startswith('# Licensed to'): continue
        filtered.append(line)
    return '\n'.join(filtered)

def diff_u(path1, path2):
    r = subprocess.run(["diff", "-u", path1, path2], capture_output=True, text=True, timeout=10)
    return r.returncode == 0, r.stdout

def count_diff_lines(diff_text):
    added = removed = 0
    for line in diff_text.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            added += 1
        elif line.startswith('-') and not line.startswith('---'):
            removed += 1
    return added, removed

def classify(diff_ratio):
    if diff_ratio <= 0.03:  return "A"
    if diff_ratio <= 0.15:  return "B"
    if diff_ratio <= 0.40:  return "C"
    return "D"

def count_orphans(source):
    return source.count('# orphan @')

def check_syntax(file_path):
    try:
        py_compile.compile(str(file_path), doraise=True)
        return True, None
    except py_compile.PyCompileError as e:
        return False, str(e)

def check_import(file_path):
    try:
        path_obj = Path(file_path)
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        parent_path = str(path_obj.parent)
        sys.path.insert(0, parent_path)
        __import__(module_name)
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        path_obj = Path(file_path)
        parent_path = str(path_obj.parent)
        if parent_path in sys.path:
            sys.path.remove(parent_path)

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

def classify_error(syntax_ok, runtime_ok, patterns):
    has_control_flow = any(p["type"] in ["try_no_except_finally", "for_empty", "empty_try"] for p in patterns)
    if has_control_flow:
        return "control_block_anomaly"
    has_orphan = any(p["type"] in ["orphan_raise", "bare_elem", "bare_list", "stray_pass"] for p in patterns)
    if has_orphan:
        return "orphan_block"
    if not syntax_ok:
        return "syntax_error"
    if not runtime_ok:
        return "runtime_error"
    return "ok"

def main():
    print(f"PyRebuilderSharp 全量白盒测试")
    print(f"工作目录: {PROJECT_DIR}")
    print()

    if DECOMPILED_DIR.exists():
        shutil.rmtree(DECOMPILED_DIR)
    DECOMPILED_DIR.mkdir()
    for ver in VERSIONS:
        (DECOMPILED_DIR / ver_tag(ver)).mkdir()

    print(f"{'='*60}")
    print(f"Phase 1: 批量反编译")
    print(f"{'='*60}")
    batch_out = DECOMPILED_DIR / "_batch"
    batch_out.mkdir()
    t0 = time.time()
    cli_dll = str(PROJECT_DIR / "src/PyRebuilderSharp.Cli/bin/Release/net10.0/PyRebuilderSharp.CLI.dll")
    r = subprocess.run(
        ["dotnet", "exec", cli_dll,
         "-d", str(COMPILED_DIR), "-o", str(batch_out)],
        capture_output=True, text=True, timeout=600, cwd=str(PROJECT_DIR)
    )
    elapsed = time.time() - t0
    print(f"  {elapsed:.1f}s — 批量反编译完成")

    all_results = {}
    for fname in sorted(os.listdir(str(COMPILED_DIR))):
        if not fname.endswith('.pyc'):
            continue
        ver = None
        for v in VERSIONS:
            suffix = f'.{v}.pyc'
            if fname.endswith(suffix):
                ver = v
                base = fname[:-len(suffix)]
                break
        if ver is None:
            print(f"  ⚠ Unknown format: {fname}")
            continue
        source_file = base + '.py'
        rel = os.path.relpath(os.path.join(str(COMPILED_DIR), fname), str(PROJECT_DIR))
        batch_py = str(batch_out / (os.path.splitext(rel)[0] + '.py'))
        dest = str(DECOMPILED_DIR / ver_tag(ver) / source_file)
        success = os.path.exists(batch_py)
        if success:
            shutil.copy2(batch_py, dest)
            with open(dest) as f:
                source = f.read()
            orphans = count_orphans(source)
            syntax_ok, syntax_err = check_syntax(dest)
            runtime_ok, runtime_err = check_import(dest) if syntax_ok else (False, "Syntax error")
            patterns = scan_patterns(source)
            error_category = classify_error(syntax_ok, runtime_ok, patterns)
            for p in patterns:
                if p["type"] == "try_no_except_finally":
                    print(f"  ⚠ try_no_except_finally in {source_file} (Py {ver})")
                    for ex in p["examples"]:
                        print(f"    Example: {repr(ex[:100])}")
        else:
            orphans = 0
            syntax_ok = False
            syntax_err = None
            runtime_ok = False
            runtime_err = None
            patterns = []
            error_category = "decompile_failure"
        if base not in all_results:
            all_results[base] = {}
        all_results[base][ver] = {
            'source_file': source_file, 'dest': dest if success else None,
            'success': success, 'orphans': orphans,
            'lines': len(open(dest).read().split('\n')) if success else 0,
            'syntax_ok': syntax_ok, 'syntax_error': syntax_err,
            'runtime_ok': runtime_ok, 'runtime_error': runtime_err,
            'patterns': patterns, 'error_category': error_category
        }

    unique_files = len(all_results)
    shutil.rmtree(batch_out)

    print(f"\n{'='*60}")
    print(f"Phase 2: Diff 对比")
    print(f"{'='*60}")
    diffs = {v: {'ok': 0, 'fail': 0} for v in VERSIONS}
    cats = {v: {'A': 0, 'B': 0, 'C': 0, 'D': 0} for v in VERSIONS}
    key_diffs = {}
    total_orphans = 0
    total_diff_lines = 0

    for base in sorted(all_results.keys()):
        sf = all_results[base][list(all_results[base].keys())[0]]['source_file']
        original = load_original(sf)
        if original is None:
            continue
        orig_lines = len(original.split('\n'))
        orig_clean = strip_known_diffs(original)

        for ver in VERSIONS:
            if ver not in all_results[base]:
                continue
            r = all_results[base][ver]
            total_orphans += r.get('orphans', 0)
            if not r['success'] or r['dest'] is None:
                diffs[ver]['fail'] += 1
                continue
            try:
                with open(r['dest']) as f:
                    dec = f.read()
            except:
                diffs[ver]['fail'] += 1
                continue
            dec_clean = strip_known_diffs(dec)

            t1 = tempfile.NamedTemporaryFile(mode='w', suffix='.o', delete=False); t1.write(orig_clean); t1.close()
            t2 = tempfile.NamedTemporaryFile(mode='w', suffix='.d', delete=False); t2.write(dec_clean); t2.close()
            identical, dt = diff_u(t1.name, t2.name)
            os.unlink(t1.name); os.unlink(t2.name)

            added, removed = count_diff_lines(dt)
            total_diff_lines += (added + removed)
            diff_ratio = (added + removed) / max(orig_lines, 1)
            cat = classify(diff_ratio)
            cats[ver][cat] = cats[ver].get(cat, 0) + 1
            diffs[ver]['ok'] += 1

            if sf in KEY_FILES:
                if sf not in key_diffs:
                    key_diffs[sf] = {}
                key_diffs[sf][ver] = {
                    'identical': identical, 'added': added, 'removed': removed,
                    'cat': cat, 'orphans': r['orphans'],
                    'lines': r['lines'], 'orig_lines': orig_lines
                }

    for ver in VERSIONS:
        d = diffs[ver]
        c = cats[ver]
        total = d['ok'] + d['fail']
        ab = c.get('A', 0) + c.get('B', 0)
        print(f"  Py {ver}: {total} files | A={c.get('A',0)} B={c.get('B',0)} C={c.get('C',0)} D={c.get('D',0)} | "
              f"A+B={ab}/{total} ({ab/max(total,1)*100:.0f}%)")

    totals = {k: sum(cats[v].get(k, 0) for v in VERSIONS) for k in ['A','B','C','D']}
    total_ok = sum(d['ok'] for d in diffs.values())
    total_fail = sum(d['fail'] for d in diffs.values())
    total_all = total_ok + total_fail

    orphans_by_ver = {}
    orphan_files_by_ver = {}
    pattern_counts_by_ver = {}
    for base in all_results:
        for ver in VERSIONS:
            if ver in all_results[base] and all_results[base][ver].get('success'):
                o = all_results[base][ver].get('orphans', 0)
                if o > 0:
                    orphans_by_ver[ver] = orphans_by_ver.get(ver, 0) + o
                    if ver not in orphan_files_by_ver:
                        orphan_files_by_ver[ver] = set()
                    orphan_files_by_ver[ver].add(all_results[base][ver]['source_file'])
                patterns = all_results[base][ver].get('patterns', [])
                if ver not in pattern_counts_by_ver:
                    pattern_counts_by_ver[ver] = {}
                for p in patterns:
                    pattern_counts_by_ver[ver][p['type']] = pattern_counts_by_ver[ver].get(p['type'], 0) + p['count']

    file_orphans = []
    for base in all_results:
        total = sum(all_results[base][v].get('orphans', 0) for v in VERSIONS if v in all_results[base] and all_results[base][v].get('success'))
        if total > 0:
            file_orphans.append((base, total))
    file_orphans.sort(key=lambda x: -x[1])

    dclass = []
    for base in all_results:
        for ver in VERSIONS:
            if ver in all_results[base]:
                sf = all_results[base][ver]['source_file']
                orig = load_original(sf)
                if orig is None: continue
                r = all_results[base][ver]
                if not r.get('success') or not r.get('dest'): continue
                with open(r['dest']) as f:
                    dec = f.read()
                olen = len(strip_known_diffs(orig).split('\n'))
                t1 = tempfile.NamedTemporaryFile(mode='w', suffix='.o', delete=False); t1.write(strip_known_diffs(orig)); t1.close()
                t2 = tempfile.NamedTemporaryFile(mode='w', suffix='.d', delete=False); t2.write(strip_known_diffs(dec)); t2.close()
                _, dt = diff_u(t1.name, t2.name)
                os.unlink(t1.name); os.unlink(t2.name)
                a, r2 = count_diff_lines(dt)
                ratio = (a + r2) / max(olen, 1)
                if classify(ratio) == 'D':
                    dclass.append((base, ver, a + r2))
    dclass.sort(key=lambda x: -x[2])
    dclass = dclass[:15]

    version_error_counts = {}
    for ver in VERSIONS:
        version_error_counts[ver] = {
            'total': 0, 'ok': 0, 'syntax_error': 0, 'runtime_error': 0,
            'control_block_anomaly': 0, 'orphan_block': 0, 'decompile_failure': 0
        }

    for base in all_results:
        for ver in VERSIONS:
            if ver in all_results[base]:
                r = all_results[base][ver]
                version_error_counts[ver]['total'] += 1
                version_error_counts[ver][r['error_category']] += 1

    try:
        gc = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=str(PROJECT_DIR), timeout=5)
        git_commit = gc.stdout.strip()
    except:
        git_commit = "current"

    print(f"\n{'='*60}")
    print(f"Phase 3: 生成报告 → {REPORT_PATH}")
    print(f"{'='*60}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ab_total = total_ok - totals['C'] - totals['D']

    syntax_error_count = sum(version_error_counts[v]['syntax_error'] for v in VERSIONS)
    runtime_error_count = sum(version_error_counts[v]['runtime_error'] for v in VERSIONS)
    control_block_anomaly_count = sum(version_error_counts[v]['control_block_anomaly'] for v in VERSIONS)
    orphan_block_count = sum(version_error_counts[v]['orphan_block'] for v in VERSIONS)
    decompile_failure_count = sum(version_error_counts[v]['decompile_failure'] for v in VERSIONS)
    ok_count = sum(version_error_counts[v]['ok'] for v in VERSIONS)
    total_files_count = sum(version_error_counts[v]['total'] for v in VERSIONS)

    with open(REPORT_PATH, 'w') as f:
        f.write(f"""# PyRebuilderSharp 全量白盒测试报告

**生成时间**: {now}
**测试文件总数**: {total_files_count}
**Python 版本范围**: {', '.join(VERSIONS)}
**Commit**: `{git_commit}`

---

## 一、总体概览

### 1.1 版本分布

| Python 版本 | 文件数 | 完全通过 | 语法错误 | 运行时错误 | 控制块异常 | 孤儿块 | 反编译失败 |
|------------|--------|----------|----------|------------|------------|--------|------------|
""")
        for ver in VERSIONS:
            stats = version_error_counts[ver]
            f.write(f"| {ver} | {stats['total']} | {stats['ok']} | {stats['syntax_error']} | {stats['runtime_error']} | {stats['control_block_anomaly']} | {stats['orphan_block']} | {stats['decompile_failure']} |\n")

        f.write(f"""
### 1.2 总体通过率

- **完全通过**: {ok_count}/{total_files_count} ({ok_count/max(total_files_count,1)*100:.1f}%)
- **语法错误**: {syntax_error_count} ({syntax_error_count/max(total_files_count,1)*100:.1f}%)
- **运行时错误**: {runtime_error_count} ({runtime_error_count/max(total_files_count,1)*100:.1f}%)
- **控制块异常**: {control_block_anomaly_count} ({control_block_anomaly_count/max(total_files_count,1)*100:.1f}%)
- **孤儿块**: {orphan_block_count} ({orphan_block_count/max(total_files_count,1)*100:.1f}%)
- **反编译失败**: {decompile_failure_count} ({decompile_failure_count/max(total_files_count,1)*100:.1f}%)

### 1.3 Diff 质量分类

| 类别 | 含义 | 文件数 | 占比 |
|------|------|--------|------|
| A | 近乎完美 (≤3% diff) | {totals['A']} | {totals['A']/max(total_all,1)*100:.1f}% |
| B | 轻微差异 (≤15% diff) | {totals['B']} | {totals['B']/max(total_all,1)*100:.1f}% |
| C | 明显差异 (≤40% diff) | {totals['C']} | {totals['C']/max(total_all,1)*100:.1f}% |
| D | 高差异 (>40% diff) | {totals['D']} | {totals['D']/max(total_all,1)*100:.1f}% |
| **A+B** | **可接受输出** | **{ab_total}** | **{ab_total/max(total_all,1)*100:.1f}%** |

---

## 二、按优先级分类的问题分析

### 2.1 控制块异常（最高优先级）

**影响文件数**: {control_block_anomaly_count}

| 问题模式 | 出现次数 |
|----------|----------|
""")
        for ver in VERSIONS:
            if ver in pattern_counts_by_ver:
                for pattern_type, count in pattern_counts_by_ver[ver].items():
                    if pattern_type in ["try_no_except_finally", "for_empty", "empty_try"]:
                        f.write(f"| {pattern_type} (Py {ver}) | {count} |\n")

        f.write(f"""

### 2.2 指令缺失

**影响文件数**: {orphan_block_count}

| 问题模式 | 出现次数 |
|----------|----------|
""")
        for ver in VERSIONS:
            if ver in pattern_counts_by_ver:
                for pattern_type, count in pattern_counts_by_ver[ver].items():
                    if pattern_type in ["orphan_raise"]:
                        f.write(f"| {pattern_type} (Py {ver}) | {count} |\n")

        f.write(f"""

### 2.3 孤儿块

**影响文件数**: {orphan_block_count}

| 问题模式 | 出现次数 |
|----------|----------|
""")
        for ver in VERSIONS:
            if ver in pattern_counts_by_ver:
                for pattern_type, count in pattern_counts_by_ver[ver].items():
                    if pattern_type in ["bare_elem", "bare_list", "stray_pass"]:
                        f.write(f"| {pattern_type} (Py {ver}) | {count} |\n")

        f.write(f"""

### 2.4 语法错误

**影响文件数**: {syntax_error_count}

### 2.5 运行时错误

**影响文件数**: {runtime_error_count}

---

## 三、关键文件深度分析

| 文件 | 版本 | ± lines | 类别 | Orphans | 语法 | 运行 |
|------|------|---------|------|---------|------|------|
""")
        for fname in KEY_FILES:
            if fname not in key_diffs: continue
            for ver in VERSIONS:
                if ver not in key_diffs[fname]: continue
                d = key_diffs[fname][ver]
                tc = d['added'] + d['removed']
                emoji = {'A': '🟢', 'B': '🟡', 'C': '🟠', 'D': '🔴'}.get(d['cat'], '⚪')
                f.write(f"| {fname} | {ver} | +{d['added']}/−{d['removed']} | {emoji} {d['cat']} | {d['orphans']} | - | - |\n")

        f.write(f"""

---

## 四、Orphan 块分析

### 按版本统计

| Version | Orphans |
|:-------:|:-------:|
""")
        for ver in VERSIONS:
            o = orphans_by_ver.get(ver, 0)
            f.write(f"| {ver} | {o} |\n")

        f.write(f"""

### 按文件统计（Top 10）

| 文件 | Total Orphans |
|:-----|:-------------:|
""")
        for fn, count in file_orphans[:10]:
            f.write(f"| {fn} | {count} |\n")

        f.write(f"""

---

## 五、修复计划

### P0 - 紧急修复（影响面大）

1. **修复 Python 3.13/3.14 列表推导式和 for 循环重构**
   - 问题: `_repr_iterable` 等函数出现 `elem`, `[]`, `for _ in []` 等异常输出
   - 原因: `LOAD_FAST_AND_CLEAR` 和超级指令处理不完整
   - 影响: 3.13/3.14 的 reprlib 等核心库函数

2. **修复 try 块无 except/finally 问题**
   - 问题: 反编译输出包含 `try:` 但没有 except/finally
   - 原因: 异常表解析和控制流图重建不完整
   - 影响: 所有版本的异常处理

### P1 - 重要修复（控制块异常）

3. **修复 for 循环空迭代器问题**
   - 问题: `for _ in []:` 空循环
   - 原因: 列表推导式重构失败

4. **修复 CFG handler→class edge**
   - 问题: BlockScanner 将 handler 后的类/函数定义错误分类
   - 影响: ~50 个文件

### P2 - 次要修复（指令缺失/孤儿块）

5. **修复孤儿 raise 语句**
   - 问题: 独立的 `raise` 语句
   - 原因: 异常处理块重构不完整

6. **清理裸表达式** (`elem`, `[]`)
   - 原因: 栈机状态管理问题

7. **清理多余 pass 语句**

### P3 - 优化

8. **减少 orphan blocks** ({total_orphans})
   - 加强 `_processedBlockIds` 处理

9. **移除调试噪声** (`# orphan @` / `# [SUMMARY]`)
   - 改为 CLI 可选参数

10. **Docstring 格式优化** (`'text'` -> `\"\"\"text\"\"\"`)

---

*报告生成时间: {now}*
""")

    print(f"✅ 报告已生成: {REPORT_PATH}")
    print(f"\n{'='*60}")
    print(f"FINAL")
    print(f"{'='*60}")
    print(f"  完全通过: {ok_count}/{total_files_count} ({ok_count/max(total_files_count,1)*100:.1f}%)")
    print(f"  控制块异常: {control_block_anomaly_count}")
    print(f"  孤儿块: {orphan_block_count}")
    print(f"  语法错误: {syntax_error_count}")
    print(f"  A+B 可接受: {ab_total}/{total_all} ({ab_total/max(total_all,1)*100:.1f}%)")

if __name__ == '__main__':
    main()