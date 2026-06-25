#!/usr/bin/env python3
"""
pyc_cache_analyzer.py — 分析 3.11+ .pyc 文件的 CACHE 条目布局

从原始字节码数据中精确定位每条指令，统计其后连续零字节的数量，
并与 VersionStrategy312 的 cache 表比对，找出差异。

用法: python3 tools/pyc_cache_analyzer.py [file.pyc]
"""
import struct, sys, os
from collections import defaultdict, Counter

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPILED_DIR = os.path.join(PROJECT_DIR, "test_data", "compiled")

# VersionStrategy312.GetCacheCount 当前表值
CACHE_TABLE_312 = {
    1:0,2:0,4:0,5:0,9:0, 11:1,12:0,15:0, 25:0,26:0,30:0,
    35:0,36:0,37:0, 40:0,41:0,42:0,43:0,47:0, 49:0,53:0,
    55:0,56:0,60:0,61:0, 68:0,69:0,71:0,72:0,73:0,74:0,75:0,
    79:0,80:0,81:0,83:0,84:0,85:0,86:0, 87:0,88:0,89:0,
    90:0,91:0,92:1,93:0,94:0,95:0, 96:0,97:0,98:0,99:0,
    100:1,101:4,102:4,103:4,104:4,105:4,106:4,107:4,
    108:0,109:0,110:0, 111:0,112:0,113:0,114:0,115:0,
    116:0,117:0,118:0,119:0, 120:0,121:0,122:1,123:1,
    124:1,125:1,126:1,127:1, 128:1,129:1,130:1,131:1,132:1,133:1,
    134:0,135:0,136:0,137:0,138:0,139:0, 140:0,141:0,142:0,143:1,
    144:0,145:0,146:0,147:0, 149:0, 150:0,151:0,152:0,
    155:0,156:0,157:0, 162:0,163:0,164:0,165:0,
    166:0,167:0, 170:0, 171:4, 172:0,173:0,174:0,175:0,176:0,
}

# CPython 3.12 已知 opcode 名称
OP_NAMES = {
    1:"POP_TOP",2:"PUSH_NULL",4:"DUP_TOP",5:"DUP_TOP_TWO",
    9:"NOP",11:"UNARY_NEGATIVE",12:"UNARY_NOT",15:"UNARY_INVERT",
    20:"PUSH_EXC_INFO",25:"BINARY_SUBSCR",26:"BINARY_SLICE",
    36:"CHECK_EXC_MATCH",37:"CHECK_EG_MATCH",
    49:"WITH_EXCEPT_START",53:"BEFORE_WITH",
    60:"STORE_SUBSCR",68:"GET_ITER",69:"GET_YIELD_FROM_ITER",
    71:"LOAD_BUILD_CLASS",83:"RETURN_VALUE",
    85:"SETUP_ANNOTATIONS",89:"POP_EXCEPT",90:"STORE_NAME",
    92:"UNPACK_SEQUENCE",93:"FOR_ITER",94:"UNPACK_EX",
    95:"STORE_ATTR",97:"STORE_GLOBAL",99:"SWAP",
    100:"LOAD_CONST",101:"LOAD_NAME",102:"BUILD_TUPLE",
    103:"BUILD_LIST",104:"BUILD_SET",105:"BUILD_MAP",
    106:"LOAD_ATTR",107:"COMPARE_OP",108:"IMPORT_NAME",
    109:"IMPORT_FROM",110:"JUMP_FORWARD",
    111:"POP_JUMP_IF_TRUE",112:"POP_JUMP_IF_FALSE",
    116:"LOAD_GLOBAL",117:"IS_OP",118:"CONTAINS_OP",
    119:"RERAISE",120:"COPY",121:"RETURN_CONST",122:"BINARY_OP",
    123:"SEND",124:"LOAD_FAST",125:"STORE_FAST",
    126:"DELETE_FAST",127:"LOAD_FAST_CHECK",
    128:"POP_JUMP_IF_NOT_NONE",129:"POP_JUMP_IF_NONE",
    130:"RAISE_VARARGS",132:"MAKE_FUNCTION",133:"BUILD_SLICE",
    134:"JUMP_BACKWARD_NO_INTERRUPT",140:"JUMP_BACKWARD",
    141:"LOAD_SUPER_ATTR",142:"CALL_FUNCTION_EX",
    143:"LOAD_FAST_AND_CLEAR",144:"EXTENDED_ARG",
    149:"COPY_FREE_VARS",151:"RESUME",
    171:"CALL",172:"KW_NAMES",
}

HAVE_ARG = 90  # threshold for instructions with arguments

def op_name(op):
    return OP_NAMES.get(op, f"OP_{op}")

def find_bytecodes(data):
    """Find all code objects in marshal data and extract their bytecodes"""
    bytecodes = []
    
    def scan_marshal(d, offset):
        """Scan for TYPE_CODE (0x63) in marshal data"""
        while offset < len(d):
            if d[offset] == 0x63:  # TYPE_CODE
                try:
                    bc = extract_code(d, offset)
                    if bc:
                        bytecodes.append(bc)
                except:
                    pass
            offset += 1
    
    scan_marshal(data, 0)
    return bytecodes

def extract_code(data, start):
    """Extract bytecode from a TYPE_CODE at position start"""
    pos = start + 1  # skip 'c'
    
    # Skip count fields (variable-length marshal ints)
    for _ in range(6):
        pos = skip_int(data, pos)
    
    # Bytecode: size + content
    size = read_uint(data, pos)
    pos += 4
    bc = data[pos:pos+size]
    return bc

def skip_int(data, pos):
    if pos >= len(data):
        return pos
    b = data[pos]
    if b == 0x7f or b == 0x69:  # TYPE_INT or TYPE_CODE
        return pos + 5
    elif b <= 0x7e:  # small int
        return pos + 1
    return pos + 1

def read_uint(data, pos):
    return struct.unpack('<I', data[pos:pos+4])[0]

class Instruction:
    __slots__ = ('offset', 'opcode', 'arg', 'cache_count')
    def __init__(self, offset, opcode, arg, cache_count=0):
        self.offset = offset
        self.opcode = opcode
        self.arg = arg
        self.cache_count = cache_count

def parse_bytecode(bc):
    """Parse 3.11+ wordcode: 2 bytes per instruction, skip zero cache entries"""
    instrs = []
    offset = 0
    
    while offset + 1 < len(bc):
        op = bc[offset]
        
        # Skip cache entries (opcode=0)
        if op == 0:
            offset += 2
            continue
        
        arg = bc[offset + 1] if op >= HAVE_ARG else None
        instr = Instruction(offset, op, arg)
        
        # Advance past instruction
        offset += 2
        
        # Count zero cache entries
        cache_count = 0
        while offset + 1 < len(bc) and bc[offset] == 0:
            offset += 2
            cache_count += 1
        
        instr.cache_count = cache_count
        instrs.append(instr)
    
    return instrs

def analyze_file(path):
    with open(path, 'rb') as f:
        data = f.read()
    
    magic = struct.unpack('<H', data[:2])[0]
    header_size = 16 if magic >= 0x0da0 else 12
    
    # Find bytecodes by skipping header and scanning marshal
    bc_list = find_bytecodes(data[header_size:])
    
    all_stats = defaultdict(list)
    func_count = 0
    
    for bc in bc_list:
        if len(bc) < 10:
            continue
        instrs = parse_bytecode(bc)
        func_count += 1
        
        for instr in instrs:
            if instr.cache_count > 0:
                all_stats[instr.opcode].append(instr.cache_count)
    
    return all_stats, func_count, magic

def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else [
        os.path.join(COMPILED_DIR, f) for f in sorted(os.listdir(COMPILED_DIR))
        if f.endswith('.pyc')
    ]
    
    all_stats = defaultdict(list)
    total_funcs = 0
    total_files = 0
    
    for path in files:
        try:
            stats, funcs, magic = analyze_file(path)
            for op, counts in stats.items():
                all_stats[op].extend(counts)
            total_funcs += funcs
            total_files += 1
        except Exception as e:
            print(f"  SKIP {os.path.basename(path)}: {e}")
    
    print(f"=== PyRebuilderSharp Cache Entry Analysis ===")
    print(f"Audited {total_files} files, {total_funcs} code objects")
    print()
    print(f"{'Op':>4} {'Name':25s} {'Tbl':>3} {'Obs':>6} {'Samples':>8} {'Verdict':>12}")
    print("-" * 65)
    
    for op in sorted(all_stats.keys()):
        counts = all_stats[op]
        if not counts:
            continue
        tbl = CACHE_TABLE_312.get(op, 0)
        counter = Counter(counts)
        most_common = counter.most_common(1)[0][0]
        samples = sum(counter.values())
        
        # Determine verdict
        if most_common == tbl:
            verdict = "✅ match"
        elif most_common < tbl:
            verdict = "❌ table > actual"
        else:
            verdict = "❌ table < actual"
        
        # Show distribution
        if len(counter) > 1:
            dist = ", ".join(f"{k}({v})" for k, v in sorted(counter.items()))
            print(f"  {op:>3} {op_name(op):25s} {tbl:>3}  {most_common:>3}  {samples:>8}  {verdict:>12}")
            print(f"       dist: [{dist}]")
        else:
            print(f"  {op:>3} {op_name(op):25s} {tbl:>3}  {most_common:>3}  {samples:>8}  {verdict:>12}")
    
    # Summary of mismatches
    print()
    print("=== Mismatches (table != observed mode) ===")
    for op in sorted(all_stats.keys()):
        counts = all_stats[op]
        if not counts:
            continue
        tbl = CACHE_TABLE_312.get(op, 0)
        counter = Counter(counts)
        mode = counter.most_common(1)[0][0]
        if mode != tbl:
            print(f"  op={op:>3} ({op_name(op):25s}) tbl={tbl} → obs={mode} (samples={sum(counter.values())})")

if __name__ == '__main__':
    main()
