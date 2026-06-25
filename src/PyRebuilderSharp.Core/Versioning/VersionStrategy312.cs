using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Versioning;

/// <summary>
/// Python 3.12 版本策略。
/// 3.12 的操作码与 3.11 部分不同（CALL=171, RESUME=151, POP_JUMP_IF at 114/115 等）。
/// cache 为完整模式（几乎所有有参操作码都有固定 cache 条目）。
/// </summary>
public class VersionStrategy312 : VersionStrategyBase
{
    public override PythonVersion Version => PythonVersion.Py312;
    public override string DisplayName => "Python 3.12";

    // 3.12 使用 16 字节头部（PEP 552）
    public override int HeaderSize => 16;
    public override int HaveArgument => 90;

    // 3.11+ 特性全部开启
    public override bool IsWordOffset => true;
    public override bool HasCaches => true;
    public override bool HasExceptionTable => true;
    public override bool HasQualname => true;
    public override bool SupportsCodeSimple => true;
    public override bool UseLocalsPlus => true;
    public override bool HasLinetable => true;
    public override bool HasPep552Header => true;
    public override bool HasPosOnlyArgCount => true;

    /// <summary>
    /// 将 Python 3.12 的原始 opcode 字节值映射到统一 Opcode 枚举。
    /// 3.12 特有的值：CALL=171, RESUME=151, POP_JUMP_IF at 114/115,
    /// PUSH_EXC_HANDLER_312=177, PUSH_EXC_INFO_312=179 等。
    /// </summary>
    public override Opcode MapOpcode(byte rawOp)
    {
        return rawOp switch
        {
            // --- 所有版本一致的 (3.12) ---
            1 => Models.Bytecode.Opcode.POP_TOP,
            9 => Models.Bytecode.Opcode.NOP,
            11 => Models.Bytecode.Opcode.UNARY_NEGATIVE,
            12 => Models.Bytecode.Opcode.UNARY_NOT,
            15 => Models.Bytecode.Opcode.UNARY_INVERT,
            25 => Models.Bytecode.Opcode.BINARY_SUBSCR,
            26 => Models.Bytecode.Opcode.BINARY_SLICE_313,
            60 => Models.Bytecode.Opcode.STORE_SUBSCR,
            68 => Models.Bytecode.Opcode.GET_ITER,
            69 => Models.Bytecode.Opcode.GET_YIELD_FROM_ITER,
            71 => Models.Bytecode.Opcode.LOAD_BUILD_CLASS,
            83 => Models.Bytecode.Opcode.RETURN_VALUE,
            85 => Models.Bytecode.Opcode.SETUP_ANNOTATIONS,
            89 => Models.Bytecode.Opcode.POP_EXCEPT,
            92 => Models.Bytecode.Opcode.UNPACK_SEQUENCE,
            93 => Models.Bytecode.Opcode.FOR_ITER,
            94 => Models.Bytecode.Opcode.UNPACK_EX,
            95 => Models.Bytecode.Opcode.STORE_ATTR,
            97 => Models.Bytecode.Opcode.STORE_GLOBAL,
            100 => Models.Bytecode.Opcode.LOAD_CONST,
            101 => Models.Bytecode.Opcode.LOAD_NAME,
            102 => Models.Bytecode.Opcode.BUILD_TUPLE,
            103 => Models.Bytecode.Opcode.BUILD_LIST,
            104 => Models.Bytecode.Opcode.BUILD_SET,
            105 => Models.Bytecode.Opcode.BUILD_MAP,
            106 => Models.Bytecode.Opcode.LOAD_ATTR,
            107 => Models.Bytecode.Opcode.COMPARE_OP,
            108 => Models.Bytecode.Opcode.IMPORT_NAME,
            109 => Models.Bytecode.Opcode.IMPORT_FROM,
            110 => Models.Bytecode.Opcode.JUMP_FORWARD,
            116 => Models.Bytecode.Opcode.LOAD_GLOBAL,
            117 => Models.Bytecode.Opcode.IS_OP,
            118 => Models.Bytecode.Opcode.CONTAINS_OP,
            119 => Models.Bytecode.Opcode.RERAISE,
            124 => Models.Bytecode.Opcode.LOAD_FAST,
            125 => Models.Bytecode.Opcode.STORE_FAST,
            126 => Models.Bytecode.Opcode.DELETE_FAST,
            130 => Models.Bytecode.Opcode.RAISE_VARARGS,
            132 => Models.Bytecode.Opcode.MAKE_FUNCTION,
            133 => Models.Bytecode.Opcode.BUILD_SLICE,
            140 => Models.Bytecode.Opcode.JUMP_BACKWARD,
            142 => Models.Bytecode.Opcode.CALL_FUNCTION_EX,
            144 => Models.Bytecode.Opcode.EXTENDED_ARG,

            // --- 3.11+ 新值 ---
            2 => Models.Bytecode.Opcode.PUSH_NULL,
            3 => Models.Bytecode.Opcode.INTERPRETER_EXIT,
            4 => Models.Bytecode.Opcode.DUP_TOP,
            5 => Models.Bytecode.Opcode.DUP_TOP_TWO,
            99 => Models.Bytecode.Opcode.SWAP,
            120 => Models.Bytecode.Opcode.COPY,
            121 => Models.Bytecode.Opcode.RETURN_CONST,
            122 => Models.Bytecode.Opcode.BINARY_OP,
            123 => Models.Bytecode.Opcode.SEND,
            127 => Models.Bytecode.Opcode.LOAD_FAST_CHECK,
            128 => Models.Bytecode.Opcode.POP_JUMP_IF_NOT_NONE,
            129 => Models.Bytecode.Opcode.POP_JUMP_IF_NONE,
            134 => Models.Bytecode.Opcode.JUMP_BACKWARD_NO_INTERRUPT,
            141 => Models.Bytecode.Opcode.LOAD_SUPER_ATTR,
            143 => Models.Bytecode.Opcode.LOAD_FAST_AND_CLEAR,
            149 => Models.Bytecode.Opcode.COPY_FREE_VARS,
            172 => Models.Bytecode.Opcode.KW_NAMES,

            // --- 3.12 特有的值 ---
            20 => Models.Bytecode.Opcode.PULL_EXC_FROM_INFO_312,
            34 => Models.Bytecode.Opcode.PUSH_EXC_HANDLER_312,
            35 => Models.Bytecode.Opcode.PUSH_EXC_INFO_312,
            36 => Models.Bytecode.Opcode.CHECK_EXC_MATCH,
            37 => Models.Bytecode.Opcode.CHECK_EG_MATCH,
            31 => Models.Bytecode.Opcode.MATCH_MAPPING_312,
            32 => Models.Bytecode.Opcode.MATCH_SEQUENCE_312,
            33 => Models.Bytecode.Opcode.MATCH_KEYS_312,
            152 => Models.Bytecode.Opcode.MATCH_CLASS_312,
            49 => Models.Bytecode.Opcode.WITH_EXCEPT_START_312,
            53 => Models.Bytecode.Opcode.BEFORE_WITH_312,

            90 => Models.Bytecode.Opcode.STORE_NAME,
            111 => Models.Bytecode.Opcode.POP_JUMP_IF_TRUE,
            112 => Models.Bytecode.Opcode.POP_JUMP_IF_FALSE,
            114 => Models.Bytecode.Opcode.POP_JUMP_IF_FALSE,
            115 => Models.Bytecode.Opcode.POP_JUMP_IF_TRUE,
            151 => Models.Bytecode.Opcode.RESUME,
            156 => Models.Bytecode.Opcode.BUILD_CONST_KEY_MAP,
            162 => Models.Bytecode.Opcode.LIST_EXTEND,
            163 => Models.Bytecode.Opcode.SET_UPDATE,
            164 => Models.Bytecode.Opcode.DICT_MERGE,
            165 => Models.Bytecode.Opcode.DICT_UPDATE,
            171 => Models.Bytecode.Opcode.CALL,
            173 => Models.Bytecode.Opcode.CALL_INTRINSIC_1,
            174 => Models.Bytecode.Opcode.CALL_INTRINSIC_2,
            175 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_GLOBALS,
            176 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_DEREF,

            // Fallback: treat as raw value
            _ => (Models.Bytecode.Opcode)rawOp,
        };
    }

    /// <summary>
    /// 3.12 的缓存条目数（完整 cache 表）。
    /// </summary>
    public override int GetCacheCount(byte rawOp)
    {
        return rawOp switch
        {
            1 => 0, 2 => 0, 4 => 0, 5 => 0, 9 => 0,
            11 => 1, 12 => 0, 15 => 0,
            25 => 0, 26 => 0, 30 => 0,
            35 => 0, 36 => 0, 37 => 0,
            40 => 0, 41 => 0, 42 => 0, 43 => 0, 47 => 0,
            49 => 0, 53 => 0,
            55 => 0, 56 => 0, 60 => 0, 61 => 0,
            68 => 0, 69 => 0, 71 => 0, 72 => 0, 73 => 0, 74 => 0, 75 => 0,
            79 => 0, 80 => 0, 81 => 0, 83 => 0, 84 => 0, 85 => 0, 86 => 0,
            87 => 0, 88 => 0, 89 => 0,
            90 => 0, 91 => 0, 92 => 1, 93 => 0, 94 => 0, 95 => 0,
            96 => 0, 97 => 0, 98 => 0, 99 => 0,
            100 => 1, // LOAD_CONST
            101 => 4, // LOAD_NAME
            102 => 4, 103 => 4, 104 => 4, 105 => 4,
            106 => 4, 107 => 4,
            108 => 0, 109 => 0, 110 => 0,
            111 => 0, 112 => 0, 113 => 0, 114 => 0, 115 => 0,
            116 => 0, // LOAD_GLOBAL
            117 => 0, 118 => 0, 119 => 0,
            120 => 0, 121 => 0, 122 => 1, 123 => 1,
            124 => 1, 125 => 1, 126 => 1, 127 => 1,
            128 => 1, 129 => 1, 130 => 1, 131 => 1, 132 => 1, 133 => 1,
            134 => 0, 135 => 0, 136 => 0, 137 => 0, 138 => 0, 139 => 0,
            140 => 0, 141 => 0, 142 => 0, 143 => 1,
            144 => 0, 145 => 0, 146 => 0, 147 => 0,
            149 => 0,
            150 => 0, 151 => 0, 152 => 0,
            155 => 0, 156 => 0, 157 => 0,
            162 => 0, 163 => 0, 164 => 0, 165 => 0,
            166 => 0, 167 => 0,
            170 => 0,
            171 => 4, // CALL
            172 => 0, 173 => 0, 174 => 0, 175 => 0, 176 => 0,
            _ => 0,
        };
    }

    /// <summary>
    /// 3.11+ 跳转指令检测。
    /// </summary>
    public override bool IsJumpInstruction(Opcode op) => op switch
    {
        Models.Bytecode.Opcode.JUMP_FORWARD or Models.Bytecode.Opcode.JUMP_BACKWARD
            or Models.Bytecode.Opcode.POP_JUMP_IF_FALSE or Models.Bytecode.Opcode.POP_JUMP_IF_TRUE
            or Models.Bytecode.Opcode.POP_JUMP_IF_NOT_NONE or Models.Bytecode.Opcode.POP_JUMP_IF_NONE
            or Models.Bytecode.Opcode.FOR_ITER or Models.Bytecode.Opcode.JUMP_BACKWARD_NO_INTERRUPT
            or Models.Bytecode.Opcode.JUMP_ABSOLUTE or Models.Bytecode.Opcode.JUMP_IF_TRUE_OR_POP
            or Models.Bytecode.Opcode.JUMP_IF_FALSE_OR_POP or Models.Bytecode.Opcode.TO_BOOL_313
            or Models.Bytecode.Opcode.POP_ITER_314
            or Models.Bytecode.Opcode.SEND => true,
        _ => false
    };
}
