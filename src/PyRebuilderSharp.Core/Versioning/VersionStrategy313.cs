using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Versioning;

/// <summary>
/// Python 3.13 版本策略。
/// 3.13 的操作码编号体系与 3.12 完全不同（HAVE_ARGUMENT=44）。
/// 几乎所有操作码都被重新编号，引入了多个新的 super-instruction。
/// </summary>
public class VersionStrategy313 : VersionStrategyBase
{
    public override PythonVersion Version => PythonVersion.Py313;
    public override string DisplayName => "Python 3.13";

    // 3.13 使用 16 字节头部（PEP 552）
    public override int HeaderSize => 16;
    public override int HaveArgument => 44;  // 3.13 特有

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
    /// 将 Python 3.13+ 的原始 opcode 字节值映射到统一 Opcode 枚举。
    /// 3.13 的操作码编号体系与 3.12 完全不同（HAVE_ARGUMENT=44, 插入/删除了多个操作码）。
    /// 完整映射表来源于 CPython 3.13 Lib/opcode.py opname[]。
    /// </summary>
    public override Opcode MapOpcode(byte rawOp)
    {
        return rawOp switch
        {
            // 3.13 opname 完整映射（raw byte -> Opcode enum）
            1 => Models.Bytecode.Opcode.BEFORE_ASYNC_WITH_313,
            2 => Models.Bytecode.Opcode.BEFORE_WITH_313,
            4 => Models.Bytecode.Opcode.BINARY_SLICE_313,
            5 => Models.Bytecode.Opcode.BINARY_SUBSCR,      // enum=25
            6 => Models.Bytecode.Opcode.CHECK_EG_MATCH,     // enum=198
            7 => Models.Bytecode.Opcode.CHECK_EXC_MATCH,    // enum=197
            8 => Models.Bytecode.Opcode.CLEANUP_THROW_313,
            9 => Models.Bytecode.Opcode.DELETE_SUBSCR_313,
            10 => Models.Bytecode.Opcode.END_ASYNC_FOR_313,
            11 => Models.Bytecode.Opcode.END_FOR_313,
            12 => Models.Bytecode.Opcode.END_SEND_313,
            13 => Models.Bytecode.Opcode.EXIT_INIT_CHECK_313,
            14 => Models.Bytecode.Opcode.FORMAT_SIMPLE_313,
            15 => Models.Bytecode.Opcode.FORMAT_WITH_SPEC_313,
            16 => Models.Bytecode.Opcode.GET_AITER_313,
            17 => Models.Bytecode.Opcode.RESERVED_313,
            18 => Models.Bytecode.Opcode.GET_ANEXT_313,
            19 => Models.Bytecode.Opcode.GET_ITER,          // enum=68
            20 => Models.Bytecode.Opcode.GET_LEN_313,
            21 => Models.Bytecode.Opcode.GET_YIELD_FROM_ITER, // enum=69
            22 => Models.Bytecode.Opcode.INTERPRETER_EXIT,  // enum=3
            23 => Models.Bytecode.Opcode.LOAD_ASSERTION_ERROR_313,
            24 => Models.Bytecode.Opcode.LOAD_BUILD_CLASS,  // enum=71
            25 => Models.Bytecode.Opcode.LOAD_LOCALS_313,
            26 => Models.Bytecode.Opcode.MAKE_FUNCTION,     // enum=132
            27 => Models.Bytecode.Opcode.MATCH_KEYS_313,
            28 => Models.Bytecode.Opcode.MATCH_MAPPING_313,
            29 => Models.Bytecode.Opcode.MATCH_SEQUENCE_313,
            30 => Models.Bytecode.Opcode.NOP,               // enum=9
            31 => Models.Bytecode.Opcode.POP_EXCEPT,         // enum=89
            32 => Models.Bytecode.Opcode.POP_TOP,            // enum=1
            33 => Models.Bytecode.Opcode.PUSH_EXC_INFO,      // -> PUSH_EXC_INFO_312=179
            34 => Models.Bytecode.Opcode.PUSH_NULL,          // enum=2
            35 => Models.Bytecode.Opcode.RETURN_GENERATOR_313,
            36 => Models.Bytecode.Opcode.RETURN_VALUE,       // enum=83
            37 => Models.Bytecode.Opcode.SETUP_ANNOTATIONS,  // enum=85
            38 => Models.Bytecode.Opcode.STORE_SLICE_313,
            39 => Models.Bytecode.Opcode.STORE_SUBSCR,       // enum=49
            40 => Models.Bytecode.Opcode.TO_BOOL_313,        // 3.13+ new (raw 40)
            41 => Models.Bytecode.Opcode.UNARY_INVERT,       // enum=15
            42 => Models.Bytecode.Opcode.UNARY_NEGATIVE,     // enum=11
            43 => Models.Bytecode.Opcode.UNARY_NOT,          // enum=12
            44 => Models.Bytecode.Opcode.WITH_EXCEPT_START,  // -> WITH_EXCEPT_START_312=188
            45 => Models.Bytecode.Opcode.BINARY_OP,          // enum 191 (raw 122 in 3.12)
            46 => Models.Bytecode.Opcode.BUILD_CONST_KEY_MAP,// enum=156
            47 => Models.Bytecode.Opcode.BUILD_LIST,         // enum=103
            48 => Models.Bytecode.Opcode.BUILD_MAP,          // enum=105
            49 => Models.Bytecode.Opcode.BUILD_SET,          // enum=104
            50 => Models.Bytecode.Opcode.BUILD_SLICE,        // enum=133
            51 => Models.Bytecode.Opcode.BUILD_STRING,       // enum=157
            52 => Models.Bytecode.Opcode.BUILD_TUPLE,        // enum=102
            53 => Models.Bytecode.Opcode.CALL,               // enum=171
            54 => Models.Bytecode.Opcode.CALL_FUNCTION_EX,   // enum=142
            55 => Models.Bytecode.Opcode.CALL_INTRINSIC_1_313, // 3.13+ (raw 55)
            56 => Models.Bytecode.Opcode.CALL_INTRINSIC_2_313, // 3.13+ (raw 56)
            57 => Models.Bytecode.Opcode.CALL_KW_313,        // 3.13+ (raw 57)
            58 => Models.Bytecode.Opcode.COMPARE_OP,         // enum=107
            59 => Models.Bytecode.Opcode.CONTAINS_OP,        // enum=118
            60 => Models.Bytecode.Opcode.CONVERT_VALUE_313,  // 3.13+ (raw 60)
            61 => Models.Bytecode.Opcode.COPY,               // enum=120
            62 => Models.Bytecode.Opcode.COPY_FREE_VARS_313, // 3.13+ (was 149 in 3.12)
            63 => Models.Bytecode.Opcode.DELETE_ATTR,
            64 => Models.Bytecode.Opcode.DELETE_DEREF,       // enum=139
            65 => Models.Bytecode.Opcode.DELETE_FAST,        // enum=126
            66 => Models.Bytecode.Opcode.DELETE_GLOBAL,
            67 => Models.Bytecode.Opcode.DELETE_NAME,
            68 => Models.Bytecode.Opcode.DICT_MERGE,         // enum=164
            69 => Models.Bytecode.Opcode.DICT_UPDATE,        // enum=165
            70 => Models.Bytecode.Opcode.ENTER_EXECUTOR_313, // 3.13+ new
            71 => Models.Bytecode.Opcode.EXTENDED_ARG,        // enum=144
            72 => Models.Bytecode.Opcode.FOR_ITER,           // enum=93
            73 => Models.Bytecode.Opcode.GET_AWAITABLE_313,
            74 => Models.Bytecode.Opcode.IMPORT_FROM,        // enum=109
            75 => Models.Bytecode.Opcode.IMPORT_NAME,        // enum=108
            76 => Models.Bytecode.Opcode.IS_OP,              // enum=117
            77 => Models.Bytecode.Opcode.JUMP_BACKWARD,      // enum=140
            78 => Models.Bytecode.Opcode.JUMP_BACKWARD_NO_INTERRUPT, // enum=134
            79 => Models.Bytecode.Opcode.JUMP_FORWARD,       // enum=110
            80 => Models.Bytecode.Opcode.LIST_APPEND_313,
            81 => Models.Bytecode.Opcode.LIST_EXTEND,        // enum=162
            82 => Models.Bytecode.Opcode.LOAD_ATTR,          // enum=106
            83 => Models.Bytecode.Opcode.LOAD_CONST,         // enum=100
            84 => Models.Bytecode.Opcode.LOAD_DEREF,         // enum=137
            85 => Models.Bytecode.Opcode.LOAD_FAST,          // enum=124
            86 => Models.Bytecode.Opcode.LOAD_FAST_AND_CLEAR, // enum=192 (raw 143 in 3.12)
            87 => Models.Bytecode.Opcode.LOAD_FAST_CHECK,    // enum=193 (raw 127 in 3.12)
            88 => Models.Bytecode.Opcode.LOAD_FAST_LOAD_FAST_313, // 3.13+ new (raw 88)
            89 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_DEREF, // enum=176
            90 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_GLOBALS, // enum=175
            91 => Models.Bytecode.Opcode.LOAD_GLOBAL,        // enum=116
            92 => Models.Bytecode.Opcode.LOAD_NAME,          // enum=101
            93 => Models.Bytecode.Opcode.LOAD_SUPER_ATTR,    // enum=141
            94 => Models.Bytecode.Opcode.MAKE_CELL_313,      // 3.13+ (was 135 in 3.11)
            95 => Models.Bytecode.Opcode.MAP_ADD_313,
            96 => Models.Bytecode.Opcode.MATCH_CLASS_313,    // -> MATCH_CLASS_312=183
            97 => Models.Bytecode.Opcode.POP_JUMP_IF_FALSE,  // enum=114
            98 => Models.Bytecode.Opcode.POP_JUMP_IF_NONE,   // enum=195 (raw 129 in 3.12)
            99 => Models.Bytecode.Opcode.POP_JUMP_IF_NOT_NONE, // enum=194 (raw 128 in 3.12)
            100 => Models.Bytecode.Opcode.POP_JUMP_IF_TRUE,  // enum=115
            101 => Models.Bytecode.Opcode.RAISE_VARARGS,     // enum=130
            102 => Models.Bytecode.Opcode.RERAISE,           // enum=119
            103 => Models.Bytecode.Opcode.RETURN_CONST_313,  // 3.13+ (was 190 alias for raw 121 in 3.12)
            104 => Models.Bytecode.Opcode.SEND,              // enum=123
            105 => Models.Bytecode.Opcode.SET_ADD_313,
            106 => Models.Bytecode.Opcode.SET_FUNCTION_ATTRIBUTE_313, // 3.13+ new
            107 => Models.Bytecode.Opcode.SET_UPDATE,        // enum=163
            108 => Models.Bytecode.Opcode.STORE_ATTR,        // enum=95
            109 => Models.Bytecode.Opcode.STORE_DEREF,       // enum=138
            110 => Models.Bytecode.Opcode.STORE_FAST,        // enum=125
            111 => Models.Bytecode.Opcode.STORE_FAST_LOAD_FAST_313, // 3.13+ new
            112 => Models.Bytecode.Opcode.STORE_FAST_STORE_FAST_313, // 3.13+ new
            113 => Models.Bytecode.Opcode.STORE_GLOBAL,      // enum=97
            114 => Models.Bytecode.Opcode.STORE_NAME,        // enum=90
            115 => Models.Bytecode.Opcode.SWAP,              // enum=99
            116 => Models.Bytecode.Opcode.UNPACK_EX,         // enum=94
            117 => Models.Bytecode.Opcode.UNPACK_SEQUENCE,   // enum=92
            118 => Models.Bytecode.Opcode.YIELD_VALUE_313,   // 3.13+ (was 86 in 3.10)
            // RESUME at raw 149 (was 151 in 3.12, 90 in 3.11)
            149 => Models.Bytecode.Opcode.RESUME_313,
            // Fallback: cast raw value directly (some may still decode correctly)
            _ => (Models.Bytecode.Opcode)rawOp,
        };
    }

    /// <summary>
    /// 3.13+ 的缓存条目数（CPython 3.13 Lib/opcode.py _inline_cache_entries）。
    /// 注意：使用 3.13 的原始操作码字节值，因为 3.13 的操作码编号体系与 3.12 完全不同。
    /// </summary>
    public override int GetCacheCount(byte rawOp)
    {
        return rawOp switch
        {
            5 => 1,   // BINARY_SUBSCR
            39 => 1,  // STORE_SUBSCR
            40 => 3,  // TO_BOOL
            45 => 1,  // BINARY_OP
            53 => 3,  // CALL
            58 => 1,  // COMPARE_OP
            59 => 1,  // CONTAINS_OP
            72 => 1,  // FOR_ITER
            77 => 1,  // JUMP_BACKWARD
            82 => 9,  // LOAD_ATTR
            91 => 4,  // LOAD_GLOBAL
            93 => 1,  // LOAD_SUPER_ATTR
            97 => 1,  // POP_JUMP_IF_FALSE
            98 => 1,  // POP_JUMP_IF_NONE
            99 => 1,  // POP_JUMP_IF_NOT_NONE
            100 => 1, // POP_JUMP_IF_TRUE
            104 => 1, // SEND
            108 => 4, // STORE_ATTR
            117 => 1, // UNPACK_SEQUENCE
            _ => 0,
        };
    }

    /// <summary>
    /// 3.11+ 跳转指令检测（含 TO_BOOL_313）。
    /// </summary>
    public override bool IsJumpInstruction(Opcode op) => op switch
    {
        Models.Bytecode.Opcode.JUMP_FORWARD or Models.Bytecode.Opcode.JUMP_BACKWARD
            or Models.Bytecode.Opcode.POP_JUMP_IF_FALSE or Models.Bytecode.Opcode.POP_JUMP_IF_TRUE
            or Models.Bytecode.Opcode.POP_JUMP_IF_NOT_NONE or Models.Bytecode.Opcode.POP_JUMP_IF_NONE
            or Models.Bytecode.Opcode.FOR_ITER or Models.Bytecode.Opcode.JUMP_BACKWARD_NO_INTERRUPT
            or Models.Bytecode.Opcode.JUMP_ABSOLUTE or Models.Bytecode.Opcode.JUMP_IF_TRUE_OR_POP
            or Models.Bytecode.Opcode.JUMP_IF_FALSE_OR_POP
            or Models.Bytecode.Opcode.SEND => true,
        _ => false
    };
}
