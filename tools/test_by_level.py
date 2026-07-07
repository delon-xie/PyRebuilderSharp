#!/usr/bin/env python3
"""
test_by_level.py — 分级基线测试，每次只测试一个级别

流程：
  1. 编译：将指定级别的所有 .py 编译为各版本 .pyc
  2. 反编译：用 PyRebuilderSharp CLI 批量反编译
  3. Displus 分析：用 tools/pyc2displus.py 生成每个 .pyc 的全信息 dump
  4. Diff 对比：原始 vs 反编译
  5. 评分 & 报告：生成该级别的测试报告 + 改进意见

用法：
  python tools/test_by_level.py <级别(1-10)> [--compile] [--raw]

选项：
  --compile   强制重新编译（默认跳过已存在的 .pyc）
  --raw       保留反编译的原始输出目录

级别定义：
  1  = level0/ + level1/   (# 控制流基础)
  2  = level2/             (# try/with/异常)
  3  = level3/             (# lambda)
  4  = level4/             (# 函数)
  5  = level5/             (# 类)
  6  = level6/             (# 推导式/async/yield)
  7  = level7/             (# 边界/语法)
  8  = level8/             (# 复杂)
  9  = level9/             (# 终极)
  10 = input/根目录 .py    (# 全部剩余)
"""

import os
import sys
import subprocess
import tempfile
import shutil
import time
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(PROJECT_DIR, "test_data/input")
COMPILED_DIR = os.path.join(PROJECT_DIR, "test_data/compiled", "levels")
DECOMPILED_DIR = os.path.join(PROJECT_DIR, "test_data/decompiled", "levels")
DISPLUS_DIR = os.path.join(PROJECT_DIR, "test_data/displus", "levels")
DOTNET_DLL = os.path.join(PROJECT_DIR, "bin/release/PyRebuilderSharp.Cli.dll")
PYC2DISPLUS = os.path.join(PROJECT_DIR, "tools/pyc2displus.py")
REPORT_DIR = os.path.join(PROJECT_DIR, "docs/level_reports")

VERSIONS = ["2.7", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]
PYENV_ROOT = os.path.expanduser("~/.pyenv/versions")

VERSION_PATHS = {
    "2.7":  f"{PYENV_ROOT}/2.7.18/bin/python2.7",
    "3.5":  f"{PYENV_ROOT}/3.5.10/bin/python3.5",
    "3.6":  f"{PYENV_ROOT}/3.6.15/bin/python3.6",
    "3.7":  f"{PYENV_ROOT}/3.7.17/bin/python3.7",
    "3.8":  f"{PYENV_ROOT}/3.8.20/bin/python3.8",
    "3.9":  f"{PYENV_ROOT}/3.9.25/bin/python3.9",
    "3.10": f"{PYENV_ROOT}/3.10.20/bin/python3.10",
    "3.11": f"{PYENV_ROOT}/3.11.15/bin/python3.11",
    "3.12": f"{PYENV_ROOT}/3.12.13/bin/python3.12",
    "3.13": f"{PYENV_ROOT}/3.13.12/bin/python3.13",
    "3.14": f"{PYENV_ROOT}/3.14.3/bin/python3.14",
}

LEVEL_DIRS = {
    1: ["level0", "level1"],
    2: ["level2"],
    3: ["level3"],
    4: ["level4"],
    5: ["level5"],
    6: ["level6"],
    7: ["level7"],
    8: ["level8"],
    9: ["level9"],
    10: [],
}

LEVEL_DESCRIPTIONS = {
    1: "基础控制流（if/else, for/while, break/continue, loop-else）",
    2: "异常与上下文管理（try/except/finally, with）",
    3: "Lambda 表达式",
    4: "函数定义与多函数",
    5: "类定义与继承",
    6: "推导式、async、yield、generator",
    7: "边界情况与语法特性",
    8: "复杂构造",
    9: "终极综合",
    10: "标准库及遗留测试文件",
}


# ── Helpers ────────────────────────────────────────────────────────────────

def get_source_files(level):
    """返回给定级别的所有 .py 源文件路径列表。"""
    sources = []
    dirs = LEVEL_DIRS.get(level)
    if dirs is None:
        return []
    if dirs:
        for d in dirs:
            dpath = os.path.join(INPUT_DIR, d)
            if not os.path.isdir(dpath):
                continue
            for f in sorted(os.listdir(dpath)):
                if f.endswith(".py"):
                    sources.append(os.path.join(dpath, f))
    else:
        for f in sorted(os.listdir(INPUT_DIR)):
            fpath = os.path.join(INPUT_DIR, f)
            if os.path.isfile(fpath) and f.endswith(".py"):
                sources.append(fpath)
    return sources


def get_pyc_files(level):
    """返回编译后该级别的所有 .pyc 文件路径列表。"""
    compiled_level = os.path.join(COMPILED_DIR, f"level{level}")
    if not os.path.isdir(compiled_level):
        return []
    result = []
    for root, _dirs, files in os.walk(compiled_level):
        for f in files:
            if f.endswith(".pyc"):
                result.append(os.path.join(root, f))
    return sorted(result)


def parse_pyc_name(pyc_path):
    """解析 .pyc 文件名 → (base_name, version)。"""
    fname = os.path.basename(pyc_path)
    # 格式: {name}.{ver}.pyc
    for v in VERSIONS:
        suffix = f".{v}.pyc"
        if fname.endswith(suffix):
            base = fname[:-len(suffix)]
            return base, v
    return None, None


def strip_known_diffs(text):
    """去除反编译输出中的辅助标记，只保留核心代码对比。"""
    lines = text.split('\n')
    filtered = []
    for line in lines:
        s = line.strip()
        if line.startswith('# Decompiled from:'):
            continue
        if s.startswith('# orphan @'):
            continue
        if s.startswith('# [SUMMARY]'):
            continue
        if s.startswith('# Copyright'):
            continue
        if s.startswith('# Licensed to'):
            continue
        filtered.append(line)
    # 去除末尾空行
    while filtered and filtered[-1].strip() == '':
        filtered.pop()
    return '\n'.join(filtered)


def count_diff_lines(diff_text):
    """统计 unified diff 中 +/- 行数（排除元数据头）。"""
    added = removed = 0
    for line in diff_text.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            added += 1
        elif line.startswith('-') and not line.startswith('---'):
            removed += 1
    return added, removed


def classify_diff(ratio):
    """根据 diff 比例分类。"""
    if ratio <= 0.03:
        return "A"
    if ratio <= 0.15:
        return "B"
    if ratio <= 0.40:
        return "C"
    return "D"


def count_orphans(source):
    return source.count('# orphan @')


def diff_files(path1, path2):
    """运行 diff -u，返回 (identical, diff_text)。"""
    try:
        r = subprocess.run(
            ["diff", "-u", path1, path2],
            capture_output=True, text=True, timeout=10,
        )
        return r.returncode == 0, r.stdout
    except subprocess.TimeoutExpired:
        return False, "[TIMEOUT]"


# ── Phase 1: 编译 ──────────────────────────────────────────────────────────

def phase_compile(level, force=False):
    """编译指定级别的 .py → .pyc。返回统计信息。"""
    sources = get_source_files(level)
    if not sources:
        print("  ⚠ 无源文件")
        return {"ok": 0, "fail": 0, "total": 0}

    available_vers = [v for v in VERSIONS if os.path.isfile(VERSION_PATHS.get(v, ""))]
    stats = {"ok": 0, "fail": 0, "total": 0}

    for src_path in sources:
        base = os.path.splitext(os.path.basename(src_path))[0]
        # 计算子目录（level0/ / level1/ ...）
        src_rel = os.path.relpath(os.path.dirname(src_path), INPUT_DIR)
        for ver in available_vers:
            python_bin = VERSION_PATHS[ver]
            dst_dir = os.path.join(COMPILED_DIR, f"level{level}")
            if src_rel != ".":
                dst_dir = os.path.join(dst_dir, src_rel)
            os.makedirs(dst_dir, exist_ok=True)
            dst_path = os.path.join(dst_dir, f"{base}.{ver}.pyc")

            # 跳过已存在的（除非 force）
            if not force and os.path.exists(dst_path):
                stats["ok"] += 1
                stats["total"] += 1
                continue

            stats["total"] += 1
            code = (
                "import py_compile, sys\n"
                f"src, dst = {repr(src_path)}, {repr(dst_path)}\n"
                "try:\n"
                "    py_compile.compile(src, cfile=dst, doraise=True)\n"
                "    print('OK')\n"
                "except py_compile.PyCompileError:\n"
                "    sys.exit(2)\n"
                "except Exception as e:\n"
                "    print(f'ERR: {e}')\n"
                "    sys.exit(3)\n"
            )
            try:
                r = subprocess.run(
                    [python_bin, "-c", code],
                    capture_output=True, text=True, timeout=30,
                )
                if "OK" in r.stdout:
                    stats["ok"] += 1
                else:
                    stats["fail"] += 1
            except Exception:
                stats["fail"] += 1

    return stats


# ── Phase 2: 反编译 ────────────────────────────────────────────────────────

def phase_decompile(level):
    """运行 PyRebuilderSharp CLI 批量反编译。返回成功/失败数。"""
    pyc_dir = os.path.join(COMPILED_DIR, f"level{level}")
    out_dir = os.path.join(DECOMPILED_DIR, f"level{level}")
    batch_out = os.path.join(out_dir, "_batch")

    if os.path.exists(batch_out):
        shutil.rmtree(batch_out)
    os.makedirs(batch_out, exist_ok=True)

    print(f"  CLI: dotnet exec {os.path.relpath(DOTNET_DLL, PROJECT_DIR)}")
    print(f"  输入: {os.path.relpath(pyc_dir, PROJECT_DIR)}")
    print(f"  输出: {os.path.relpath(batch_out, PROJECT_DIR)}")

    t0 = time.time()
    r = subprocess.run(
        ["dotnet", "exec", DOTNET_DLL, "-d", pyc_dir, "-o", batch_out],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        timeout=600, cwd=PROJECT_DIR,
    )
    elapsed = time.time() - t0
    print(f"  ⏱ {elapsed:.1f}s  (exit={r.returncode})")

    # 统计反编译结果
    dec_files = []
    for root, _dirs, files in os.walk(batch_out):
        for f in files:
            if f.endswith(".py"):
                dec_files.append(os.path.join(root, f))

    # 按版本归类
    result = {}  # {basename: {ver: source_code}}
    for dec_path in dec_files:
        rel = os.path.relpath(dec_path, batch_out)
        # rel 形如 "input_dir/basename.ver.py" 或 "subdir/basename.ver.py"
        parts = rel.replace(os.sep, "/").split("/")
        if len(parts) >= 2:
            # 最后部分是文件名
            pyc_name = os.path.splitext(parts[-1])[0]
            base, ver = parse_pyc_name(pyc_name + ".pyc")
            if base and ver:
                with open(dec_path) as f:
                    code = f.read()
                if base not in result:
                    result[base] = {}
                result[base][ver] = code

    # 清理 batch 输出（后续已归档）
    shutil.rmtree(batch_out)

    print(f"  反编译文件: {len(dec_files)}")
    print(f"  归类结果: {sum(len(v) for v in result.values())} (file×version)")

    # 归档到标准位置
    for base, ver_map in result.items():
        for ver, code in ver_map.items():
            dst_dir = os.path.join(out_dir, f"v{ver.replace('.', '_')}")
            os.makedirs(dst_dir, exist_ok=True)
            dst_path = os.path.join(dst_dir, f"{base}.py")
            with open(dst_path, 'w') as f:
                f.write(code)

    return result


# ── Phase 3: Displus 分析 ─────────────────────────────────────────────────

def phase_displus(level):
    """对每个 .pyc 运行 pyc2displus.py 生成全信息 dump。"""
    pyc_files = get_pyc_files(level)
    out_dir = os.path.join(DISPLUS_DIR, f"level{level}")
    os.makedirs(out_dir, exist_ok=True)

    count = 0
    for pyc_path in pyc_files:
        base, ver = parse_pyc_name(os.path.basename(pyc_path))
        if not base or not ver:
            continue
        # 保留子目录结构
        rel = os.path.relpath(os.path.dirname(pyc_path),
                              os.path.join(COMPILED_DIR, f"level{level}"))
        if rel == ".":
            dst_path = os.path.join(out_dir, f"{base}.{ver}.txt")
        else:
            d = os.path.join(out_dir, rel)
            os.makedirs(d, exist_ok=True)
            dst_path = os.path.join(d, f"{base}.{ver}.txt")

        try:
            r = subprocess.run(
                [sys.executable, PYC2DISPLUS, pyc_path],
                capture_output=True, text=True, timeout=60,
            )
            output = r.stdout + r.stderr
            with open(dst_path, 'w') as f:
                f.write(output)
            count += 1
        except subprocess.TimeoutExpired:
            with open(dst_path, 'w') as f:
                f.write("[TIMEOUT]\n")
        except Exception as e:
            with open(dst_path, 'w') as f:
                f.write(f"[ERROR] {e}\n")

    return count


# ── Phase 4: Diff 分析 ────────────────────────────────────────────────────

def phase_diff(level, decompiled_result):
    """对比原始源代码与反编译结果。返回分析和统计。"""
    sources = get_source_files(level)
    source_map = {}
    for sp in sources:
        base = os.path.splitext(os.path.basename(sp))[0]
        with open(sp) as f:
            source_map[base] = f.read()

    results = {}  # {base: {ver: {...}}}
    ver_stats = {v: {"ok": 0, "fail": 0, "A": 0, "B": 0, "C": 0, "D": 0}
                 for v in VERSIONS}
    total_orphans = 0
    total_diff_lines = 0

    for base, ver_map in decompiled_result.items():
        orig = source_map.get(base)
        if orig is None:
            # 可能是 root 文件但 source_map 里只有 basename
            for sp in sources:
                if os.path.splitext(os.path.basename(sp))[0] == base:
                    with open(sp) as f:
                        orig = f.read()
                    break
        if orig is None:
            continue

        orig_clean = strip_known_diffs(orig)
        orig_lines = len(orig_clean.split('\n'))

        results[base] = {}
        for ver, dec_code in ver_map.items():
            if ver not in ver_stats:
                ver_stats[ver] = {"ok": 0, "fail": 0, "A": 0, "B": 0, "C": 0, "D": 0}

            dec_clean = strip_known_diffs(dec_code)
            orphans = count_orphans(dec_code)

            # 临时文件 diff
            t1 = tempfile.NamedTemporaryFile(mode='w', suffix='.o', delete=False)
            t1.write(orig_clean)
            t1.close()
            t2 = tempfile.NamedTemporaryFile(mode='w', suffix='.d', delete=False)
            t2.write(dec_clean)
            t2.close()

            identical, dt = diff_files(t1.name, t2.name)
            os.unlink(t1.name)
            os.unlink(t2.name)

            added, removed = count_diff_lines(dt)
            total_diff_lines += (added + removed)
            diff_ratio = (added + removed) / max(orig_lines, 1)
            cat = classify_diff(diff_ratio)

            ver_stats[ver]["ok"] += 1
            ver_stats[ver][cat] = ver_stats[ver].get(cat, 0) + 1
            total_orphans += orphans

            results[base][ver] = {
                "identical": identical,
                "added": added,
                "removed": removed,
                "ratio": diff_ratio,
                "cat": cat,
                "orphans": orphans,
                "orig_lines": orig_lines,
                "dec_lines": len(dec_clean.split('\n')),
            }

    # 跨版本统计顶级D类文件
    dclass = []
    for base, ver_map in results.items():
        for ver, d in ver_map.items():
            if d["cat"] == "D":
                dclass.append((base, ver, d["added"] + d["removed"]))
    dclass.sort(key=lambda x: -x[2])

    return {
        "results": results,
        "ver_stats": ver_stats,
        "total_orphans": total_orphans,
        "total_diff_lines": total_diff_lines,
        "dclass": dclass[:15],  # top 15
    }


# ── Phase 5: 报告生成 ─────────────────────────────────────────────────────

def generate_report(level, compile_stats, decompiled_result, diff_analysis, elapsed):
    """生成该级别的测试报告 + 改进建议。"""
    os.makedirs(REPORT_DIR, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_date = datetime.now().strftime("%Y%m%d")
    report_path = os.path.join(REPORT_DIR,
                               f"level{level}_report_{report_date}.md")

    try:
        gc = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=PROJECT_DIR, timeout=5,
        )
        git_commit = gc.stdout.strip()
    except Exception:
        git_commit = "current"

    vs = diff_analysis["ver_stats"]
    rs = diff_analysis["results"]
    total_attempts = sum(v["ok"] + v["fail"] for v in vs.values())
    total_ok = sum(v["ok"] for v in vs.values())
    total_fail = sum(v["fail"] for v in vs.values())
    totals_cat = {k: sum(v.get(k, 0) for v in vs.values())
                  for k in ["A", "B", "C", "D"]}
    ab_total = totals_cat["A"] + totals_cat["B"]
    unique_files = len(rs)
    source_count = len(get_source_files(level))

    # 找出每个文件最差版本
    worst_by_file = {}
    for base, ver_map in rs.items():
        worst_cat = "A"
        worst_d = None
        for ver, d in ver_map.items():
            cat_rank = {"A": 0, "B": 1, "C": 2, "D": 3}
            if cat_rank.get(d["cat"], 0) > cat_rank.get(worst_cat, 0):
                worst_cat = d["cat"]
                worst_d = d
        worst_by_file[base] = (worst_cat, worst_d)

    # 按难度排序文件
    cat_order = {"D": 0, "C": 1, "B": 2, "A": 3}
    file_by_difficulty = sorted(worst_by_file.items(),
                                key=lambda x: cat_order.get(x[1][0], 4))
    hard_files = [(b, c, d) for b, (c, d) in file_by_difficulty
                  if c in ("C", "D")]

    content = f"""# Level {level} Baseline Test Report

**Level**: {level} — {LEVEL_DESCRIPTIONS.get(level, "")}
**Date**: {now}
**Source files**: {source_count}
**Unique files in test**: {unique_files}
**Versions**: {len(VERSIONS)} ({', '.join(VERSIONS)})
**Engine**: PyRebuilderSharp ({git_commit})
**Total time**: {elapsed:.1f}s

---

## 1. Executive Summary

| Metric | Value | Status |
|:-------|:-----:|:------:|
| Source files | {source_count} | |
| Unique decompiled results | {len(rs)} | |
| Total (file × version) | {total_attempts} | |
| Compile OK | {compile_stats.get('ok', 0)} | ✅ |
| Compile FAIL (syntax inc.) | {compile_stats.get('fail', 0)} | ⚠️ |
| Decompile OK | {total_ok} | ✅ |
| Decompile FAIL | {total_fail} | ❌ |
| **A class (≤3% diff)** | **{totals_cat['A']}** | ✅ |
| **B class (≤15% diff)** | **{totals_cat['B']}** | ✅ |
| C class (≤40% diff) | {totals_cat['C']} | ⚠️ |
| D class (>40% diff) | {totals_cat['D']} | ⚠️ |
| **A+B acceptable** | **{ab_total} ({ab_total / max(total_attempts, 1) * 100:.0f}%)** | |
| Total orphan blocks | {diff_analysis['total_orphans']} | ⚠️ |
| Total diff lines | {diff_analysis['total_diff_lines']} | |

---

## 2. Per-Version Breakdown

| Version | OK | Fail | A | B | C | D | A+B% | Orphans |
|:-------:|:--:|:----:|:-:|:-:|:-:|:-:|:----:|:-------:|
"""
    for ver in VERSIONS:
        s = vs.get(ver, {"ok": 0, "fail": 0, "A": 0, "B": 0, "C": 0, "D": 0})
        total = s["ok"]
        ab = s.get("A", 0) + s.get("B", 0)
        content += f"| {ver} | {s['ok']} | {s['fail']} | {s.get('A',0)} | {s.get('B',0)} | {s.get('C',0)} | {s.get('D',0)} | {ab/max(total,1)*100:.0f}% | — |\n"

    content += f"""

---

## 3. File-Level Detail

| File | #Ver | Best | Worst | Orphans | Detail |
|:-----|:----:|:----:|:-----:|:-------:|:-------|
"""
    for base, (worst_cat, worst_d) in file_by_difficulty:
        ver_count = len(rs[base])
        best_cat = min((d["cat"] for d in rs[base].values()),
                       key=lambda x: {"A": 0, "B": 1, "C": 2, "D": 3}.get(x, 4))
        total_ords = sum(d["orphans"] for d in rs[base].values())
        # Detail summary per version
        parts = []
        for ver in VERSIONS:
            if ver in rs[base]:
                d = rs[base][ver]
                parts.append(f"{ver}:{d['cat']}(+{d['added']}/-{d['removed']})")
        detail = ", ".join(parts[:5])
        if len(parts) > 5:
            detail += "…"
        emoji_worst = {"A": "🟢", "B": "🟡", "C": "🟠", "D": "🔴"}.get(worst_cat, "⚪")
        emoji_best = {"A": "🟢", "B": "🟡", "C": "🟠", "D": "🔴"}.get(best_cat, "⚪")
        content += f"| {base}.py | {ver_count} | {emoji_best}{best_cat} | {emoji_worst}{worst_cat} | {total_ords} | {detail} |\n"

    if hard_files:
        content += f"""

---

## 4. Hardest Files (C/D class)

| File | Version | Diff Lines | Ratio | Orphans | Core Issue |
|:-----|:-------:|:----------:|:-----:|:-------:|:-----------|
"""
        for base, ver, _ in diff_analysis["dclass"][:10]:
            if ver in rs.get(base, {}):
                d = rs[base][ver]
                content += f"| {base}.py | {ver} | +{d['added']}/-{d['removed']} | {d['ratio']:.1%} | {d['orphans']} | (see displus) |\n"

    # 生成改进建议
    content += f"""

---

## 5. Improvement Analysis

### 5.1 Orphan Block Analysis
"""
    orphan_files = [(b, sum(d["orphans"] for d in vm.values()))
                    for b, vm in rs.items()
                    if sum(d["orphans"] for d in vm.values()) > 0]
    orphan_files.sort(key=lambda x: -x[1])
    if orphan_files:
        content += """| File | Total Orphans | Suspect |
|:-----|:-------------:|:--------|
"""
        for b, o in orphan_files[:10]:
            content += f"| {b}.py | {o} | ⚠️ 未解析的 CFG 块 |\n"
    else:
        content += "✅ 无 orphan 块\n"

    # 跨版本一致的D类文件模式
    consistent_d = {}
    for base, vm in rs.items():
        d_vers = [v for v, d in vm.items() if d["cat"] == "D"]
        if len(d_vers) >= len(VERSIONS) // 2:
            consistent_d[base] = d_vers
    if consistent_d:
        content += f"""
### 5.2 跨版本一致问题（{len(consistent_d)} 个文件在大多数版本中为 D 类）

| File | Affected Versions |
|:-----|:-----------------|
"""
        for b, vers in sorted(consistent_d.items())[:10]:
            content += f"| {b}.py | {', '.join(vers)} |\n"
        content += """
这些文件在所有版本中表现一致，说明是**反编译器固有缺陷**而非版本特定问题。
查阅 displus 输出找共性 pattern。
"""

    content += f"""

### 5.3 按版本降级检查

| Version | C+D Ratio | Assessment |
|:-------:|:---------:|:-----------|
"""
    for ver in VERSIONS:
        s = vs.get(ver, {"ok": 0, "C": 0, "D": 0})
        total = max(s["ok"], 1)
        cd = s.get("C", 0) + s.get("D", 0)
        cd_ratio = cd / total * 100
        if cd_ratio < 10:
            assessment = "✅ 良好"
        elif cd_ratio < 30:
            assessment = "⚠️ 需关注"
        else:
            assessment = "🔴 突出问题"
        content += f"| {ver} | {cd_ratio:.0f}% | {assessment} |\n"

    content += """

### 5.4 推荐修复优先级

| Priority | Issue | Level Impact | Suggested Approach |
|:--------:|:------|:------------:|:-------------------|
"""
    # 自动推导改进建议
    suggestions = []
    if diff_analysis["total_orphans"] > 0:
        suggestions.append(
            ("P1", f"减少 orphan 块 ({diff_analysis['total_orphans']})",
             f"{diff_analysis['total_orphans']} orphans",
             "强化 _processedBlockIds 追踪，检查 CFG 孤块链接"))
    worst_ver = min(vs.items(), key=lambda x: x[1].get("A", 0) / max(x[1]["ok"], 1))
    if worst_ver[1]["ok"] > 0:
        suggestions.append(
            ("P1", f"修复 v{worst_ver[0]} 质量问题（{worst_ver[1].get('D',0)} 个 D 类）",
             f"{worst_ver[1].get('D',0)} D-class",
             "检查该版本特有的 opcode/ET 处理"))
    if consistent_d:
        suggestions.append(
            ("P2", f"解决 {len(consistent_d)} 个跨版本 D 类文件的共性问题",
             f"{len(consistent_d)} files",
             "对比 displus 输出定位共性 pattern"))
    if not suggestions:
        suggestions.append(
            ("P3", "持续优化 B→A 转换",
             "cosmetic diffs",
             "docstring 格式、空行保留"))

    for pri, issue, impact, approach in suggestions:
        content += f"| {pri} | {issue} | {impact} | {approach} |\n"

    # 反编译结果示例
    content += f"""

---

## 6. Sample: Worst File at Displus Detail

See `test_data/displus/level{level}/` for full per-file per-version pyc2displus dumps.
These contain complete bytecode, exception tables, lnotab, and code object details.

---

## 7. Next Steps

| Priority | Action |
|:--------:|:-------|
| P0 | Fix hardest file(s) in this level |
| P1 | Run test again to verify fix |
| P2 | Move to next level |
| P3 | Track per-level convergence across iterations |

---

*Report generated by `tools/test_by_level.py` on {now}*
"""

    with open(report_path, 'w') as f:
        f.write(content)

    return report_path


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(1 if len(sys.argv) < 2 else 0)

    level = int(sys.argv[1])
    if level < 1 or level > 10:
        print(f"❌ 无效级别: {level}")
        sys.exit(1)

    force_compile = "--compile" in sys.argv
    keep_raw = "--raw" in sys.argv

    t_start = time.time()
    print(f"\n{'='*60}")
    print(f"  Level {level} Baseline Test")
    print(f"  {LEVEL_DESCRIPTIONS.get(level, '')}")
    print(f"{'='*60}")
    print()

    # Phase 1: 编译
    print(f"[Phase 1/5] 编译 .py → .pyc")
    print(f"{'-'*40}")
    compile_stats = phase_compile(level, force=force_compile)
    print(f"  OK={compile_stats.get('ok', 0)}  FAIL={compile_stats.get('fail', 0)}")
    print()

    # Phase 2: 反编译
    print(f"[Phase 2/5] 反编译 .pyc → .py")
    print(f"{'-'*40}")
    decompiled_result = phase_decompile(level)
    dec_count = sum(len(v) for v in decompiled_result.values())
    print(f"  结果: {len(decompiled_result)} files × {dec_count} (file×ver)")
    print()

    # Phase 3: Displus
    print(f"[Phase 3/5] 生成 displus 全信息 dump")
    print(f"{'-'*40}")
    displus_count = phase_displus(level)
    print(f"  生成: {displus_count} 个 .txt")
    print()

    # Phase 4: Diff 分析
    print(f"[Phase 4/5] Diff 对比分析")
    print(f"{'-'*40}")
    diff_analysis = phase_diff(level, decompiled_result)
    vs = diff_analysis["ver_stats"]
    for ver in VERSIONS:
        s = vs.get(ver, {})
        if s.get("ok", 0) > 0:
            ab = s.get("A", 0) + s.get("B", 0)
            print(f"  Py {ver}: {s['ok']} files | A={s.get('A',0)} B={s.get('B',0)} "
                  f"C={s.get('C',0)} D={s.get('D',0)} | A+B={ab}/{s['ok']} ({ab/max(s['ok'],1)*100:.0f}%)")
    print(f"  Orphans: {diff_analysis['total_orphans']}")
    print(f"  Diff lines: {diff_analysis['total_diff_lines']}")
    print()

    # Phase 5: 报告
    elapsed = time.time() - t_start
    print(f"[Phase 5/5] 生成测试报告")
    print(f"{'-'*40}")
    report_path = generate_report(level, compile_stats, decompiled_result,
                                  diff_analysis, elapsed)
    print(f"  📄 {report_path}")
    print()

    print(f"{'='*60}")
    total_s = sum(v["ok"] for v in vs.values())
    total_a = sum(v.get("A", 0) for v in vs.values())
    total_b = sum(v.get("B", 0) for v in vs.values())
    print(f"  ✅ Level {level} 测试完成 ({elapsed:.1f}s)")
    print(f"  📊 Total: {total_s} | A={total_a} B={total_b}")
    print(f"  📁 Displus: test_data/displus/level{level}/")
    print(f"{'='*60}")
    print()


if __name__ == "__main__":
    main()
