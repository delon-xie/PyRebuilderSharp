#!/usr/bin/env python3
"""
orphan_analysis.py — 对 enum.py 和 functools.py 的孤儿块进行分类分析
"""
import os, re, subprocess, tempfile
from collections import Counter, defaultdict

DECOMPILED_DIR = "test_data/decompiled"
INPUT_DIR = "test_data/input"

def strip_known(text):
    lines = text.split('\n')
    out = []
    for line in lines:
        sl = line.strip()
        if line.startswith('# Decompiled from:'): continue
        if sl.startswith('# orphan @'): continue
        if sl.startswith('# [SUMMARY]'): continue
        if sl.startswith('# [WARN]'): continue
        if sl.startswith('# Unknown node'): continue
        if sl.startswith('# Copyright'): continue
        out.append(line)
    return '\n'.join(out)

def diff_u(p1, p2):
    r = subprocess.run(["diff", "-u", p1, p2], capture_output=True, text=True, timeout=10)
    return r.returncode == 0, r.stdout

targets = ["enum.py", "functools.py"]
versions_seen = set()

for root, dirs, files in os.walk(DECOMPILED_DIR):
    vt = os.path.basename(root)
    for fn in files:
        if fn in targets:
            versions_seen.add((fn, vt))

# Group by file, version
for fn in targets:
    print(f"\n{'='*70}")
    print(f"  {fn} — 孤儿块分析")
    print(f"{'='*70}")
    
    all_orphans_by_ver = {}
    
    for root, dirs, files in os.walk(DECOMPILED_DIR):
        vt = os.path.basename(root)
        if fn not in files: continue
        
        path = os.path.join(root, fn)
        with open(path) as f:
            content = f.read()
        
        # Count orphans
        orphans = re.findall(r'# orphan @(0x[0-9A-F]+)', content)
        if not orphans:
            continue
        
        print(f"\n  {vt}: {len(orphans)} orphans")
        
        # Get lines around each orphan
        lines = content.split('\n')
        orphan_positions = []
        for i, line in enumerate(lines):
            m = re.search(r'# orphan @(0x[0-9A-F]+)', line)
            if m:
                offset = m.group(1)
                # What follows the orphan?
                following = []
                for j in range(i+1, min(i+6, len(lines))):
                    s = lines[j].strip()
                    if s and not s.startswith('# orphan @') and not s.startswith('# [SUMMARY]'):
                        following.append(s)
                        break
                orphan_positions.append((offset, following[0] if following else "(empty)"))
        
        # Classify by context (what function/class are they in?)
        current_def = "module-level"
        orphans_by_def = Counter()
        orphans_near = defaultdict(list)
        
        for i, line in enumerate(lines):
            s = line.strip()
            if s.startswith('def ') or s.startswith('class '):
                name_part = s.split('(')[0].split(' ')[1] if ' ' in s else s
                current_def = name_part
            m = re.search(r'# orphan @(0x[0-9A-F]+)', line)
            if m:
                orphans_by_def[current_def] += 1
                # Get the statement right after this orphan
                for j in range(i+1, min(i+4, len(lines))):
                    ns = lines[j].strip()
                    if ns and not ns.startswith('#') and not ns.startswith('def ') and not ns.startswith('class '):
                        orphans_near[current_def].append(ns[:80])
                        break
        
        print(f"  By function/class:")
        for name, count in orphans_by_def.most_common(10):
            sample = ""
            if name in orphans_near and orphans_near[name]:
                sample = f"  e.g. `{orphans_near[name][0]}`"
            print(f"    {name}: {count} {sample}")
        
        all_orphans_by_ver[vt] = {
            'count': len(orphans),
            'by_def': orphans_by_def,
        }
    
    # Cross-version analysis
    print(f"\n  --- 跨版本孤儿模式 ---")
    if fn == "enum.py":
        # Show orphan distribution across versions
        for vt_data in sorted(all_orphans_by_ver.keys(), key=lambda x: x):
            v = all_orphans_by_ver[vt_data]
            top3 = v['by_def'].most_common(3)
            top3_str = ', '.join(f"{n}({c})" for n, c in top3)
            print(f"    {vt_data}: {v['count']} orphans, top: {top3_str}")

print(f"\n{'='*70}")
print(f"  孤儿块成因分类")
print(f"{'='*70}")
print("""
类型 A: Handler 前导块 (DUP_TOP/POP_TOP/END_FINALLY)
  - 已被 Phase 10 P1 过滤，残余的语义内容已包含在 try/except AST 中
  - 继续过滤的条件：块中包含 handler 前导指令

类型 B: Handler 链遗漏块 (JUMP_IF_NOT_EXC_MATCH 后继)
  - try/except 链条中第二/第三个 except 的块
  - ExtractExceptHandlerFromOffset 的 BFS 未能遍历到
  - 在 3.6-3.9 中常见（SETUP_FINALLY 模式）

类型 C: 嵌套 for-loop 体边界块
  - 3.11+ 中 for-loop 体末尾的 JUMP_BACKWARD 未被消费
  - Phase 10 P2 已过滤 JUMP_BACKWARD，但循环体内有其他指令块残留

类型 D: 纯常量/Name 表达式 (如 `cls.__bases__`, `()`)
  - StackMachine 处理的平铺语句未关联到上层结构
  - 通常出现在函数开头，是 for-loop/if 的前置计算块

类型 E: 空块或仅含 Pass 的块
  - 指令数 0 或仅产生 Pass
  - 已在 Phase 9b 中跳过
""")

# Detailed analysis for top orphan functions in enum.py
print(f"{'='*70}")
print(f"  enum.py 深度分析 (v3_8 为样本)")
print(f"{'='*70}")

with open("test_data/decompiled/v3_8/enum.py") as f:
    lines = f.readlines()

# Find orphans in __new__ (95 orphans - largest)
current_func = None
func_orphans = defaultdict(list)
func_lines = {}

for i, line in enumerate(lines):
    s = line.strip()
    if s.startswith('def ') or s.startswith('class '):
        name_part = s.split('(')[0].split(' ')[1] if ' ' in s else s
        current_func = name_part
        func_lines[current_func] = []
    elif current_func and '# orphan @' in s:
        m = re.search(r'# orphan @(0x[0-9A-F]+)', s)
        if m:
            off = m.group(1)
            # Get next non-empty, non-comment line
            for j in range(i+1, min(i+5, len(lines))):
                ns = lines[j].strip()
                if ns and not ns.startswith('#') and not ns.startswith('def') and not ns.startswith('class'):
                    func_orphans[current_func].append((off, ns))
                    break
            else:
                func_orphans[current_func].append((off, "(empty)"))

# Show top orphan functions with detail
for func_name, orphans in sorted(func_orphans.items(), key=lambda x: -len(x[1]))[:5]:
    print(f"\n  【{func_name}】({len(orphans)} orphans)")
    # Group by statement type
    stmt_types = Counter()
    for off, stmt in orphans:
        # Classify the statement
        if stmt in ("(empty)", ""):
            typ = "空"
        elif stmt.startswith('pass') or stmt.startswith('if not True'):
            typ = "pass/未达"
        elif stmt.startswith('return'):
            typ = "return"
        elif stmt.startswith('break') or stmt.startswith('continue'):
            typ = "break/continue"
        elif stmt.startswith('raise'):
            typ = "raise"
        elif stmt.startswith('('):
            typ = "元组常量"
        elif stmt.startswith("'") or stmt.startswith('"'):
            typ = "字符串常量"
        elif stmt.startswith('if ') or stmt.startswith('elif '):
            typ = "if判断头"
        elif stmt.startswith('for ') or stmt.startswith('while '):
            typ = "循环头"
        else:
            typ = "表达式语句"
        stmt_types[typ] += 1
    
    for typ, cnt in stmt_types.most_common():
        print(f"    {typ}: {cnt}")
    # Show samples
    print(f"    样本:")
    for off, stmt in orphans[:5]:
        print(f"      @{off}: `{stmt}`")
