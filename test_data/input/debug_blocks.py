import dis, marshal, types, struct

with open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)

for const in code.co_consts:
    if isinstance(const, types.CodeType) and const.co_name == 'depth_5_while':
        print('=== Block structure ===')
        instrs = list(dis.Bytecode(const))
        
        # Find leaders
        leaders = {0}
        for i, instr in enumerate(instrs):
            if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
                if instr.arg is not None:
                    leaders.add(instr.arg)
            elif instr.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER'):
                if instr.arg is not None:
                    leaders.add(instr.arg)
                if i + 1 < len(instrs):
                    leaders.add(instrs[i+1].offset)
        
        # Print blocks
        sorted_leaders = sorted(leaders)
        for i, start in enumerate(sorted_leaders):
            end = sorted_leaders[i+1] if i+1 < len(sorted_leaders) else instrs[-1].offset + 2
            block_instrs = [ins for ins in instrs if start <= ins.offset < end]
            print(f'Block [{start:3d}-{end-1:3d}]: {", ".join(f"{ins.opname}" for ins in block_instrs[:3])}...' if len(block_instrs) > 3 else f'Block [{start:3d}-{end-1:3d}]: {", ".join(f"{ins.opname}" for ins in block_instrs)}')
            if any(ins.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE') for ins in block_instrs):
                last = block_instrs[-1]
                print(f'  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].offset+2}')
            if any(ins.opname == 'JUMP_ABSOLUTE' for ins in block_instrs):
                for ins in block_instrs:
                    if ins.opname == 'JUMP_ABSOLUTE':
                        print(f'  → JUMP: offset={ins.offset}, target={ins.arg}')
