#!/usr/bin/env python3
"""
compile_level.py — 编译指定级别（1-10）的所有 .py 源文件为 .pyc

级别定义：
  1  = level0/ + level1/    (# 最基础结构)
  2  = level2/              (# try/with/异常)
  3  = level3/              (# lambda)
  4  = level4/              (# 函数定义)
  5  = level5/              (# 类定义)
  6  = level6/              (# 推导式/async/yield)
  7  = level7/              (# 边界/语法)
  8  = level8/              (# 复杂)
  9  = level9/              (# 终极)
  10 = test_data/input/*.py (# 根目录所有 .py)

输出：test_data/compiled/levels/level{N}/{basename}.{ver}.pyc
"""

import os
import sys
import subprocess
import glob

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(PROJECT_DIR, "test_data/input")
COMPILED_DIR = os.path.join(PROJECT_DIR, "test_data/compiled", "levels")
PYENV_ROOT = os.path.expanduser("~/.pyenv/versions")

VERSIONS = ["2.7", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]

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

# 级别 → 目录映射
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
    10: [],  # root, handled specially
}


def get_source_files(level):
    """返回给定级别的所有 .py 源文件路径列表。"""
    sources = []
    dirs = LEVEL_DIRS.get(level)
    if dirs is None:
        print(f"❌ 无效级别: {level}（有效值 1-10）")
        sys.exit(1)

    if dirs:
        for d in dirs:
            dpath = os.path.join(INPUT_DIR, d)
            if not os.path.isdir(dpath):
                print(f"  ⚠ 目录不存在: {dpath}")
                continue
            for f in sorted(os.listdir(dpath)):
                if f.endswith(".py"):
                    sources.append(os.path.join(dpath, f))
    else:
        # Level 10: root files
        for f in sorted(os.listdir(INPUT_DIR)):
            fpath = os.path.join(INPUT_DIR, f)
            if os.path.isfile(fpath) and f.endswith(".py"):
                sources.append(fpath)

    return sources


def compile_file(src_path, ver, level):
    """用指定 Python 版本编译单个 .py → .pyc。返回 (ok, dst_path)"""
    python_bin = VERSION_PATHS.get(ver)
    if not python_bin or not os.path.isfile(python_bin):
        return False, None

    # 计算输出路径
    base = os.path.splitext(os.path.basename(src_path))[0]
    level_dir_rel = os.path.relpath(os.path.dirname(src_path), INPUT_DIR)
    if level_dir_rel == ".":
        level_dir_rel = "root"
    dst_dir = os.path.join(COMPILED_DIR, f"level{level}", level_dir_rel)
    os.makedirs(dst_dir, exist_ok=True)
    dst_path = os.path.join(dst_dir, f"{base}.{ver}.pyc")

    # 跳过已存在且更新的文件
    if os.path.exists(dst_path):
        src_mtime = os.path.getmtime(src_path)
        dst_mtime = os.path.getmtime(dst_path)
        if dst_mtime > src_mtime:
            return True, dst_path

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
        ok = "OK" in r.stdout
        return ok, dst_path if ok else None
    except subprocess.TimeoutExpired:
        print(f"    ⏱ 超时: {ver}")
        return False, None
    except FileNotFoundError:
        return False, None


def main():
    if len(sys.argv) < 2:
        print("用法: python tools/compile_level.py <级别(1-10)>")
        print()
        print("级别说明：")
        for lv in sorted(LEVEL_DIRS.keys()):
            dirs = LEVEL_DIRS[lv]
            if dirs:
                desc = f"目录 {', '.join(dirs)}/"
            else:
                desc = "input/ 根目录所有 .py"
            print(f"  {lv:2d} = {desc}")
        sys.exit(1)

    level = int(sys.argv[1])
    if level < 1 or level > 10:
        print(f"❌ 无效级别: {level}（有效值 1-10）")
        sys.exit(1)

    sources = get_source_files(level)
    if not sources:
        print(f"❌ 级别 {level} 没有找到 .py 源文件")
        sys.exit(1)

    # 检查可用 Python 版本
    available_vers = [v for v in VERSIONS if os.path.isfile(VERSION_PATHS.get(v, ""))]
    if not available_vers:
        print("❌ 未找到任何可用 Python 版本（检查 ~/.pyenv/versions/）")
        sys.exit(1)

    print(f"=== 编译级别 {level} ===")
    print(f"  源文件: {len(sources)} 个")
    print(f"  Python版本: {', '.join(available_vers)}")
    print(f"  输出目录: {COMPILED_DIR}/level{level}/")
    print()

    stats = {"ok": 0, "fail": 0, "skip": 0, "total": 0, "err_files": []}

    for src_path in sources:
        fname = os.path.basename(src_path)
        print(f"  📄 {fname}:")
        for ver in available_vers:
            stats["total"] += 1
            ok, dst_path = compile_file(src_path, ver, level)
            if ok and dst_path and os.path.exists(dst_path):
                print(f"    ✅ v{ver:>4s}  → {os.path.relpath(dst_path, COMPILED_DIR)}")
                stats["ok"] += 1
            elif ok:
                print(f"    ✅ v{ver:>4s}")
                stats["ok"] += 1
            else:
                print(f"    ❌ v{ver:>4s}  (语法不兼容或编译失败)")
                stats["fail"] += 1
                stats["err_files"].append((fname, ver))

    print()
    print(f"{'='*50}")
    print(f"编译完成:")
    print(f"  ✅ 成功: {stats['ok']}")
    print(f"  ❌ 失败: {stats['fail']}")
    print(f"  📊 总计: {stats['total']}")
    if stats["err_files"]:
        print(f"\n  失败详情（前10条）:")
        for fname, ver in stats["err_files"][:10]:
            print(f"    {fname} @ v{ver}")
    print()


if __name__ == "__main__":
    main()
