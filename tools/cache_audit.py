#!/usr/bin/env python3
"""
cache_audit.py — 从 3.11+ .pyc 文件中提取指令的 cache 条目数

原理：在 wordcode 布局中，每条指令占 2 字节，CACHE 条目也是 2 字节。
CACHE 条目的 opcode 字节为 0（虽然 warmup 后可能非零）。
统计每条指令后连续非指令字节的数量来确定 cache 条目数。

用法: python3 tools/cache_audit.py [--all] [--verbose]
"""
import os, struct, sys
from collections import defaultdict, Counter

COMPILED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_data/compiled")

# CPython 3.11/3.12 已知 opcode -> name 映射（用于日志可读性）
OPCODE_NAMES_312 = {
    1: "POP_TOP", 2: "PUSH_NULL", 3: "INTERPRETER_EXIT", 4: "DUP_TOP",
    5: "DUP_TOP_TWO", 9: "NOP", 11: "UNARY_NEGATIVE", 12: "UNARY_NOT",
    15: "UNARY_INVERT", 20: "PULL_EXC_FROM_INFO_312", 25: "BINARY_SUBSCR",
    26: "BINARY_SLICE", 31: "MATCH_MAPPING_312", 32: "MATCH_SEQUENCE_312",
    33: "MATCH_KEYS_312", 34: "PUSH_EXC_HANDLER_312", 35: "PUSH_EXC_INFO_312",
    36: "CHECK_EXC_MATCH", 37: "CHECK_EG_MATCH", 49: "WITH_EXCEPT_START_312",
    53: "BEFORE_WITH_312", 60: "STORE_SUBSCR", 68: "GET_ITER",
    69: "GET_YIELD_FROM_ITER", 71: "LOAD_BUILD_CLASS", 83: "RETURN_VALUE",
    85: "SETUP_ANNOTATIONS", 89: "POP_EXCEPT", 90: "STORE_NAME",
    92: "UNPACK_SEQUENCE", 93: "FOR_ITER", 94: "UNPACK_EX",
    95: "STORE_ATTR", 97: "STORE_GLOBAL", 99: "SWAP",
    100: "LOAD_CONST", 101: "LOAD_NAME", 102: "BUILD_TUPLE",
    103: "BUILD_LIST", 104: "BUILD_SET", 105: "BUILD_MAP",
    106: "LOAD_ATTR", 107: "COMPARE_OP", 108: "IMPORT_NAME",
    109: "IMPORT_FROM", 110: "JUMP_FORWARD", 111: "POP_JUMP_IF_TRUE",
    112: "POP_JUMP_IF_FALSE", 114: "POP_JUMP_IF_FALSE",
    115: "POP_JUMP_IF_TRUE", 116: "LOAD_GLOBAL", 117: "IS_OP",
    118: "CONTAINS_OP", 119: "RERAISE", 120: "COPY",
    121: "RETURN_CONST", 122: "BINARY_OP", 123: "SEND",
    124: "LOAD_FAST", 125: "STORE_FAST", 126: "DELETE_FAST",
    127: "LOAD_FAST_CHECK", 128: "POP_JUMP_IF_NOT_NONE",
    129: "POP_JUMP_IF_NONE", 130: "RAISE_VARARGS", 132: "MAKE_FUNCTION",
    133: "BUILD_SLICE", 134: "JUMP_BACKWARD_NO_INTERRUPT",
    140: "JUMP_BACKWARD", 141: "LOAD_SUPER_ATTR", 142: "CALL_FUNCTION_EX",
    143: "LOAD_FAST_AND_CLEAR", 144: "EXTENDED_ARG", 149: "COPY_FREE_VARS",
    151: "RESUME", 152: "MATCH_CLASS_312", 156: "BUILD_CONST_KEY_MAP",
    162: "LIST_EXTEND", 163: "SET_UPDATE", 164: "DICT_MERGE",
    165: "DICT_UPDATE", 171: "CALL", 172: "KW_NAMES",
    173: "CALL_INTRINSIC_1", 174: "CALL_INTRINSIC_2",
    175: "LOAD_FROM_DICT_OR_GLOBALS", 176: "LOAD_FROM_DICT_OR_DEREF",
}

# Known HAVE_ARGUMENT threshold (same across 3.11+)
HAVE_ARGUMENT = 90

def op_name(raw_op):
    return OPCODE_NAMES_312.get(raw_op, f"OP_{raw_op}")

def audit_pyc(path, verbose=False):
    """Analyze one .pyc file, return dict of opcode->cache_count_observations"""
    with open(path, 'rb') as f:
        data = f.read()
    
    # Determine version from magic
    magic = struct.unpack('<H', data[:2])[0]
    
    # Identify version from magic
    ver_map = {
        0x0d33: "3.6", 0x0d34: "3.6", 0x0d35: "3.6",
        0x0d36: "3.7", 0x0d37: "3.7", 0x0d38: "3.7",
        0x0d39: "3.8", 0x0d3a: "3.8",
        0x0d3b: "3.9", 0x0d3c: "3.9",
        0x0d6f: "3.10", 0x0da0: "3.10",
        0x0da7: "3.11", 0x0da8: "3.11", 0x0da9: "3.11",
        0x0dcb: "3.12", 0x0dcc: "3.12", 0x0dcd: "3.12",
    }
    version = ver_map.get(magic, f"0x{magic:04x}")
    
    # Skip header (16 bytes for 3.11+, 12 for 3.10-)
    header_size = 16 if magic >= 0x0da0 else 12
    code_start = header_size
    
    # Find the bytecode of the top-level code object
    # We need to parse marshal to get co_code
    # For simplicity, scan for bytecode in various code objects
    
    return audit_bytecode_in_marshal(data[code_start:], version, verbose)

def audit_bytecode_in_marshal(marshal_data, version, verbose):
    """Find and audit bytecode sections within marshal data"""
    results = defaultdict(list)
    total_instructions = 0
    
    # Find all code objects by scanning for CodeType markers
    # TYPE_CODE = 'c' (0x63) or TYPE_CODE2 = 0x63 in 3.8+
    pos = 0
    while pos < len(marshal_data) - 4:
        if marshal_data[pos] == 0x63:  # TYPE_CODE
            # Try to parse code object
            try:
                end, bc = extract_bytecode(marshal_data, pos)
                if bc and len(bc) > 10:
                    stats = count_cache_entries(bc, verbose)
                    for op, counts in stats.items():
                        results[op].extend(counts)
                    total_instructions += len(stats)
            except:
                pass
        pos += 1
    
    return results, total_instructions, version

def extract_bytecode(data, start):
    """Extract co_code from a code object starting at 'start'"""
    # TYPE_CODE format: 'c' argcount posonlyargcount ... co_code_size co_code_bytes ...
    # This is complex; for simplicity, just extract the raw bytecode after header
    # Skip TYPE_CODE byte
    pos = start + 1
    # Skip: argcount, posonlyargcount (3.8+), kwonlyargcount, nlocals, stacksize, flags
    # Each is a marshal int (variable length)
    for _ in range(6):
        pos = skip_marshal_int(data, pos)
    
    # Skip code (pascal string): size + content
    code_size, pos = read_marshal_int(data, pos)
    bc = data[pos:pos+code_size]
    pos += code_size
    
    # Skip consts, names, varnames, etc.
    return pos, bc

def skip_marshal_int(data, pos):
    """Skip one marshal integer (variable length)"""
    if pos >= len(data):
        return pos
    b = data[pos]
    if b <= 0x7e:  # SHORT int (1 byte)
        return pos + 1
    elif b == 0x7f:  # LONG int (5 bytes: type + 4 bytes)
        return pos + 5
    elif b == 0x69:  # TYPE_INT (1 byte) – older marshal format
        return pos + 5  # type + 4 bytes
    elif b == 0x6a:  # TYPE_INT64
        return pos + 9
    else:
        return pos + 1  # Unknown, skip

def read_marshal_int(data, pos):
    """Read marshal int, return (value, new_pos)"""
    if pos >= len(data):
        return 0, pos
    b = data[pos]
    if b == 0x7f:  # TYPE_INT
        return struct.unpack('<i', data[pos+1:pos+5])[0], pos + 5
    elif b == 0x69:  # TYPE_SHORT_ASCII_INTERNED or similar
        return data[pos+1], pos + 2
    else:
        return b, pos + 1

def count_cache_entries(bytecode, verbose=False):
    """
    Parse bytecode and count cache entries after each instruction.
    Returns dict: raw_opcode -> list of (cache_count, offset)
    """
    stats = defaultdict(list)
    offset = 0
    prev_op = None
    prev_offset = None
    
    while offset + 1 < len(bytecode):
        raw_op = bytecode[offset]
        
        if raw_op == 0:
            # Cache entry or unused byte
            if prev_op is not None:
                # Count consecutive cache entries
                cache_start = offset
                count = 0
                while offset + 1 < len(bytecode) and bytecode[offset] == 0:
                    count += 1
                    offset += 2
                offset -= 2  # will advance by 2 at loop end
            offset += 2
            continue
        
        # Process instruction
        if prev_op is not None and prev_op >= HAVE_ARGUMENT:
            # Count cache entries after previous instruction
            cache_count = (offset - (prev_offset + 2)) // 2
            if cache_count > 0:
                stats[prev_op].append(cache_count)
        
        prev_op = raw_op
        prev_offset = offset
        offset += 2  # each instruction is 2 bytes
    
    # Handle last instruction
    if prev_op is not None and prev_op >= HAVE_ARGUMENT and prev_offset is not None:
        cache_count = (offset - (prev_offset + 2)) // 2
        if cache_count > 0:
            stats[prev_op].append(cache_count)
    
    return stats

def main():
    verbose = '--verbose' in sys.argv
    only_latest = '--latest' in sys.argv
    
    pyc_files = sorted([f for f in os.listdir(COMPILED_DIR) if f.endswith('.pyc')])
    
    # Aggregate per-opcode cache counts
    all_stats = defaultdict(list)
    all_instructions = 0
    file_count = 0
    
    for fname in pyc_files:
        path = os.path.join(COMPILED_DIR, fname)
        try:
            results, instr_count, version = audit_pyc(path, verbose)
            if instr_count > 0:
                file_count += 1
                all_instructions += instr_count
                for op, counts in results.items():
                    all_stats[op].extend(counts)
        except Exception as e:
            if verbose:
                print(f"  ERROR {fname}: {e}")
    
    print(f"=== Cache Entry Audit ===")
    print(f"Audited {file_count} .pyc files, {all_instructions} total instructions")
    print()
    print(f"{'Opcode':>8} {'Name':25s} {'Obs':>5} {'Cache':>8} {'Min':>3} {'Max':>3} {'Mode':>3}")
    print("-" * 65)
    
    # Sort by opcode
    for op in sorted(all_stats.keys()):
        counts = all_stats[op]
        if not counts:
            continue
        # Get most common cache count (mode)
        counter = Counter(counts)
        mode = counter.most_common(1)[0][0]
        c_min = min(counts)
        c_max = max(counts)
        name = op_name(op)
        
        print(f"  {op:>4}  {name:25s} {len(counts):>5}  variations: {set(counts)}  mode={mode}")
        
        # Check if cache count is consistent
        if c_min != c_max and verbose:
            print(f"         INCONSISTENT! Range {c_min}-{c_max}")
    
    print()
    print("=== Current GetCacheCount values (VersionStrategy312) ===")
    # Known cache counts from VersionStrategy312 (correct ones)
    known = {
        11: 1, 25: 0, 60: 0, 92: 1, 93: 0, 94: 0, 95: 0,
        100: 1, 101: 4, 102: 4, 103: 4, 104: 4, 105: 4,
        106: 4, 107: 4, 108: 0, 109: 0, 110: 0,
        111: 0, 112: 0, 113: 0, 114: 0, 115: 0,
        116: 0, 117: 0, 118: 0, 119: 0,
        120: 0, 121: 0, 122: 1, 123: 1,
        124: 1, 125: 1, 126: 1, 127: 1,
        128: 1, 129: 1, 130: 1, 131: 1, 132: 1, 133: 1,
        134: 0, 140: 0, 141: 0, 142: 0, 143: 1,
        144: 0, 149: 0, 151: 0,
        152: 0, 156: 0, 162: 0, 163: 0, 164: 0, 165: 0,
        171: 4, 172: 0, 173: 0, 174: 0, 175: 0, 176: 0,
    }
    
    for op in sorted(all_stats.keys()):
        counts = all_stats[op]
        observed = set(counts)
        expected = known.get(op, 0)
        match = "✅" if len(observed) == 1 and list(observed)[0] == expected else "❌"
        details = f"obs={observed}, tbl={expected}"
        print(f"  {match} op={op:>3} ({op_name(op):25s}) {details}")

if __name__ == '__main__':
    main()
