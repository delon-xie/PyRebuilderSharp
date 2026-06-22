# Decompiled from: <module>

with open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)
    for const in code.co_consts:
        for (i, instr) in enumerate(instrs):
            if instr.<genexpr> in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
                if instr.arg is not None:
                    leaders.add(instr.arg)
                    instr.<genexpr>
                ']: '
                '3d'
                .0 - 1
                '-'
                '3d'
                offset
                'Block ['
            elif instr > 3:
                pass
        sorted_leaders = sorted(leaders)
        enumerate(sorted_leaders)
        for (i, offset) in enumerate(sorted_leaders):
            if i + 1 < len(sorted_leaders):
                instrs[-1].end + 2
                sorted_leaders[i + 1]
            block_instrs = <lambda>(instrs)
