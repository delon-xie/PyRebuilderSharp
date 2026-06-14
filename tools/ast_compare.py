#!/usr/bin/env python3
"""
AST 自动对比验证工具

将反编译输出的 .py 文件与原 .py 文件进行 AST 语义比较。
用法: python ast_compare.py <original.py> <decompiled.py>
"""

import ast
import sys
import difflib


def normalize_ast(node):
    """将 AST 节点序列化为可比较的规范化形式，忽略格式/注释差异"""
    if node is None:
        return None
    if isinstance(node, ast.AST):
        fields = {}
        for field, value in ast.iter_fields(node):
            fields[field] = normalize_ast(value)
        return (type(node).__name__, fields)
    if isinstance(node, list):
        return [normalize_ast(item) for item in node]
    return node


def compare_asts(source_a, source_b):
    """比较两个 Python 源码的 AST 是否语义等价"""
    try:
        tree_a = ast.parse(source_a)
    except SyntaxError as e:
        return False, f"Syntax error in source A: {e}"
    try:
        tree_b = ast.parse(source_b)
    except SyntaxError as e:
        return False, f"Syntax error in source B: {e}"

    norm_a = normalize_ast(tree_a)
    norm_b = normalize_ast(tree_b)

    if norm_a == norm_b:
        return True, "AST 完全匹配"

    # 尝试查找差异
    from pprint import pformat
    str_a = pformat(norm_a)
    str_b = pformat(norm_b)

    diff = "\n".join(difflib.unified_diff(
        str_a.splitlines(), str_b.splitlines(),
        fromfile="original", tofile="decompiled",
        lineterm=""
    ))

    return False, f"AST 不匹配:\n{diff[:2000]}"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ast_compare.py <original.py> <decompiled.py>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        src_a = f.read()
    with open(sys.argv[2]) as f:
        src_b = f.read()

    match, message = compare_asts(src_a, src_b)
    print(f"{'PASS' if match else 'FAIL'}: {sys.argv[1]} vs {sys.argv[2]}")
    print(message)
    sys.exit(0 if match else 1)
