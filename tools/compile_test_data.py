#!/usr/bin/env python3
"""PyRebuilderSharp 测试文件编译脚本"""
import importlib.util
import struct
import marshal
import os
import sys

PY_ROOT = os.path.expanduser("~/.pyenv/versions")

VERSIONS = {
    "3.11": ("3.11.15", f"{PY_ROOT}/3.11.15/bin/python3.11"),
    "3.12": ("3.12.13", f"{PY_ROOT}/3.12.13/bin/python3.12"),
    "3.13": ("3.13.12", f"{PY_ROOT}/3.13.12/bin/python3.13"),
    "3.14": ("3.14.3",  f"{PY_ROOT}/3.14.3/bin/python3.14"),
}

TARGET_DIR = "/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData"

def compile_with_version(version, py_path, out_path):
    """用子进程调用特定版本的 Python 编译"""
    _, python_bin = VERSIONS[version]
    if not os.path.exists(python_bin):
        return False

    # 使用 subprocess 而不是 os.system 避免 shell 转义问题
    import subprocess
    code = (
        "import py_compile\n"
        f"py_compile.compile({py_path!r}, cfile={out_path!r}, dfile={os.path.basename(py_path)!r})\n"
        "print('OK')\n"
    )
    result = subprocess.run([python_bin, "-c", code], capture_output=True, text=True, timeout=30)
    return "OK" in result.stdout

def main():
    os.makedirs(os.path.join(TARGET_DIR, "compiled"), exist_ok=True)
    input_dir = os.path.join(TARGET_DIR, "input")
    py_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".py")])

    print(f"找到 {len(py_files)} 个 .py 文件\n")

    ok, skip, fail = 0, 0, 0
    for py_file in py_files:
        py_path = os.path.join(input_dir, py_file)
        for version, (ver_dir, py_bin) in VERSIONS.items():
            base = py_file[:-3]
            out_path = os.path.join(TARGET_DIR, "compiled", f"{base}.{version}.pyc")
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                skip += 1
                continue
            print(f"  {py_file:40s} → v{version} ... ", end="", flush=True)
            ok_ = compile_with_version(version, py_path, out_path)
            if ok_:
                print("OK")
                ok += 1
            else:
                print("FAIL")
                fail += 1

    print(f"\n完成: {ok} 编译, {skip} 跳过, {fail} 失败")

if __name__ == "__main__":
    main()
