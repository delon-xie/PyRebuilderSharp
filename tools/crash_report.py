#!/usr/bin/env python3
"""
crash_report.py — 日志驱动的反编译修复管道

从 ~/.pyrebuilder/crashes/ 读取 crash JSON，去重、分类、排序。
输出可操作的修复报告。

用法:
  ./crash_report.py              # 分析全部 crash
  ./crash_report.py --summary    # 仅汇总
  ./crash_report.py --json       # JSON 格式输出 (供 CI 使用)
  ./crash_report.py --clear      # 清除所有 crash (修复后)
"""

import os, json, glob, sys
from collections import Counter, defaultdict
from datetime import datetime


CRASH_DIR = os.path.expanduser("~/.pyrebuilder/crashes")


def load_crashes():
    """加载所有 crash JSON 文件"""
    if not os.path.isdir(CRASH_DIR):
        return []
    crashes = []
    for f in sorted(glob.glob(os.path.join(CRASH_DIR, "crash_*.json"))):
        try:
            with open(f) as fh:
                data = json.load(fh)
                data["_file"] = f
                crashes.append(data)
        except (json.JSONDecodeError, OSError):
            pass
    return crashes


def analyze(crashes):
    """去重、分类、排序"""
    if not crashes:
        return {
            "total": 0,
            "unique_exceptions": {},
            "by_type": {},
            "by_message": {},
            "top_files": []
        }

    # 按异常类型分组
    by_type = defaultdict(list)
    for c in crashes:
        et = c.get("ExceptionType", "Unknown")
        by_type[et].append(c)

    # 按异常消息分组
    by_message = defaultdict(list)
    for c in crashes:
        em = c.get("ExceptionMessage", "?")[:120]
        by_message[em].append(c)

    # 按文件分组
    by_file = defaultdict(list)
    for c in crashes:
        fn = c.get("FileName", "anonymous")
        by_file[fn].append(c)

    # 每个类型取一个样本
    unique = {}
    for et, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
        sample = items[0]
        unique[et] = {
            "count": len(items),
            "pct": f"{len(items) / len(crashes) * 100:.1f}%",
            "message": sample.get("ExceptionMessage", "?")[:200],
            "example_file": sample.get("FileName", "?"),
            "stacktrace": sample.get("StackTrace", "").split("\\n")[0] if "\\n" in sample.get("StackTrace", "") else sample.get("StackTrace", "")[:200],
            "source_snippet": sample.get("SourceSnippet", "?")[:100],
        }

    return {
        "total": len(crashes),
        "unique_exceptions": unique,
        "by_type": dict(by_type),
        "by_message": dict(by_message),
        "top_files": sorted(by_file.items(), key=lambda x: -len(x[1]))[:10],
    }


def print_report(result):
    """打印可读报告"""
    print("=" * 60)
    print("  Crash Report — Phase Log FX")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    if result["total"] == 0:
        print("🎉 0 crash files — all clean!")
        return

    print(f"Total crash files: {result['total']}")
    print(f"Unique exception types: {len(result['unique_exceptions'])}")
    print()

    for rank, (et, info) in enumerate(result["unique_exceptions"].items(), 1):
        print(f"─── #{rank} [{info['count']} files, {info['pct']}] {et} ───")
        print(f"  Message: {info['message']}")
        print(f"  Example file: {info['example_file']}")
        if info['source_snippet']:
            print(f"  Source: {info['source_snippet']}")
        if info['stacktrace']:
            print(f"  Stack: {info['stacktrace']}")
        print()

    print("─── Top crashed files ───")
    for fn, crashes_list in result["top_files"]:
        types = Counter(c.get("ExceptionType", "?") for c in crashes_list)
        type_str = ", ".join(f"{t}({c})" for t, c in types.most_common(2))
        print(f"  [{len(crashes_list)} crashes] {fn} → {type_str}")

    print()
    print(f"Recommendation: fix #{list(result['unique_exceptions'].keys())[0]}")
    print(f"  Re-run: ./crash_report.py (should show fewer crashes)")


def main():
    args = set(sys.argv[1:])

    if "--clear" in args:
        count = 0
        for f in glob.glob(os.path.join(CRASH_DIR, "crash_*.json")):
            os.remove(f)
            count += 1
        print(f"Cleared {count} crash files")
        return

    crashes = load_crashes()
    result = analyze(crashes)

    if "--json" in args:
        print(json.dumps(result, indent=2, default=str))
        return

    print_report(result)


if __name__ == "__main__":
    main()
