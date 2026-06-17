using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Versioning;

/// <summary>
/// Python 3.14 版本策略。
/// 3.14 的操作码编号体系与 3.13 完全不同（HAVE_ARGUMENT=43）。
/// 新增多个操作码：LOAD_SMALL_INT_314, LOAD_FAST_BORROW_314, POP_ITER_314 等。
/// </summary>
public class VersionStrategy314 : VersionStrategyBase
{
    public override PythonVersion Version => PythonVersion.Py314;
    public override string DisplayName => "Python 3.14";

    // 3.14 使用 16 字节头部（PEP 552）
    public override int HeaderSize => 16;
    public override int HaveArgument => 43;  // 3.14 特有

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
    /// 将 Python 3.14 的原始 opcode 字节值映射到统一 Opcode 枚举。
    /// 3.14 的操作码编号体系与 3.13 完全不同（HAVE_ARGUMENT=43 vs 44）。
    /// 完整映射表来源于 CPython 3.14 Lib/opcode.py opname[]。
    /// 仅映射通用操作码（super-instruction 如 CALL_PY_EXACT_ARGS 等不映射——通常不会出现在
    /// py_compile 生成的字节码中，直接以原始字节值 fallback 为 Opcode 枚举）。
    /// </summary>
    public override Opcode MapOpcode(byte rawOp)
    {
        return rawOp switch
        {
            // --- 无参操作码 (0-42, HAVE_ARGUMENT=43) ---
            0 => Models.Bytecode.Opcode.NOP,                  // CACHE -> NOP（CACHE 已在前端跳过）
            1 => Models.Bytecode.Opcode.BINARY_SLICE_313,     // BINARY_SLICE
            2 => Models.Bytecode.Opcode.BEFORE_WITH_313,      // BUILD_TEMPLATE -> BEFORE_WITH
            3 => Models.Bytecode.Opcode.BINARY_OP_INPLACE_ADD_UNICODE_314, // (3.14 new)
            4 => Models.Bytecode.Opcode.CALL_FUNCTION_EX,     // CALL_FUNCTION_EX (enum=142)
            5 => Models.Bytecode.Opcode.CHECK_EG_MATCH,       // CHECK_EG_MATCH (enum=198)
            6 => Models.Bytecode.Opcode.CHECK_EXC_MATCH,      // CHECK_EXC_MATCH (enum=197)
            7 => Models.Bytecode.Opcode.CLEANUP_THROW_313,    // CLEANUP_THROW
            8 => Models.Bytecode.Opcode.DELETE_SUBSCR_313,    // DELETE_SUBSCR
            9 => Models.Bytecode.Opcode.END_FOR_313,          // END_FOR (3.14 raw=9)
            10 => Models.Bytecode.Opcode.END_SEND_313,        // END_SEND
            11 => Models.Bytecode.Opcode.EXIT_INIT_CHECK_313, // EXIT_INIT_CHECK
            12 => Models.Bytecode.Opcode.FORMAT_SIMPLE_313,   // FORMAT_SIMPLE
            13 => Models.Bytecode.Opcode.FORMAT_WITH_SPEC_313,// FORMAT_WITH_SPEC
            14 => Models.Bytecode.Opcode.GET_AITER_313,       // GET_AITER
            15 => Models.Bytecode.Opcode.GET_ANEXT_313,       // GET_ANEXT
            16 => Models.Bytecode.Opcode.GET_ITER,            // GET_ITER (enum=68)
            17 => Models.Bytecode.Opcode.RESERVED_313,        // RESERVED
            18 => Models.Bytecode.Opcode.GET_LEN_313,         // GET_LEN
            19 => Models.Bytecode.Opcode.GET_YIELD_FROM_ITER, // (enum=69)
            20 => Models.Bytecode.Opcode.INTERPRETER_EXIT,    // (enum=3)
            21 => Models.Bytecode.Opcode.LOAD_BUILD_CLASS,    // (enum=71)
            22 => Models.Bytecode.Opcode.LOAD_LOCALS_313,     // LOAD_LOCALS
            23 => Models.Bytecode.Opcode.MAKE_FUNCTION,       // (enum=132)
            24 => Models.Bytecode.Opcode.MATCH_KEYS_313,      // MATCH_KEYS
            25 => Models.Bytecode.Opcode.MATCH_MAPPING_313,   // MATCH_MAPPING
            26 => Models.Bytecode.Opcode.MATCH_SEQUENCE_313,  // MATCH_SEQUENCE
            27 => Models.Bytecode.Opcode.NOP,                 // NOP (enum=9)
            28 => Models.Bytecode.Opcode.NOT_TAKEN_314,       // NOT_TAKEN (3.14 new)
            29 => Models.Bytecode.Opcode.POP_EXCEPT,          // POP_EXCEPT (enum=89)
            30 => Models.Bytecode.Opcode.POP_ITER_314,        // POP_ITER (3.14 new)
            31 => Models.Bytecode.Opcode.POP_TOP,             // POP_TOP (enum=1)
            32 => Models.Bytecode.Opcode.PUSH_EXC_INFO_312,   // PUSH_EXC_INFO (enum=179)
            33 => Models.Bytecode.Opcode.PUSH_NULL,           // PUSH_NULL (enum=2)
            34 => Models.Bytecode.Opcode.RETURN_GENERATOR_313,// RETURN_GENERATOR
            35 => Models.Bytecode.Opcode.RETURN_VALUE,        // (enum=83)
            36 => Models.Bytecode.Opcode.SETUP_ANNOTATIONS,   // (enum=85)
            37 => Models.Bytecode.Opcode.STORE_SLICE_313,     // STORE_SLICE
            38 => Models.Bytecode.Opcode.STORE_SUBSCR,        // (enum=49)
            39 => Models.Bytecode.Opcode.TO_BOOL_313,         // TO_BOOL (enum=213)
            40 => Models.Bytecode.Opcode.UNARY_INVERT,        // (enum=15)
            41 => Models.Bytecode.Opcode.UNARY_NEGATIVE,      // (enum=11)
            42 => Models.Bytecode.Opcode.UNARY_NOT,           // (enum=12)

            // --- 有参操作码 (43+) ---
            43 => Models.Bytecode.Opcode.WITH_EXCEPT_START,   // -> WITH_EXCEPT_START_312=188
            44 => Models.Bytecode.Opcode.BINARY_OP,           // BINARY_OP (enum=191)
            45 => Models.Bytecode.Opcode.BUILD_INTERPOLATION_314, // BUILD_INTERPOLATION (3.14 new)
            46 => Models.Bytecode.Opcode.BUILD_LIST,          // (enum=103)
            47 => Models.Bytecode.Opcode.BUILD_MAP,           // (enum=105)
            48 => Models.Bytecode.Opcode.BUILD_SET,           // (enum=104)
            49 => Models.Bytecode.Opcode.BUILD_SLICE,         // (enum=133)
            50 => Models.Bytecode.Opcode.BUILD_STRING,        // (enum=157)
            51 => Models.Bytecode.Opcode.BUILD_TUPLE,         // (enum=102)
            52 => Models.Bytecode.Opcode.CALL,                // CALL (enum=171)
            53 => Models.Bytecode.Opcode.CALL_INTRINSIC_1_313,// CALL_INTRINSIC_1 (enum=214)
            54 => Models.Bytecode.Opcode.CALL_INTRINSIC_2_313,// CALL_INTRINSIC_2 (enum=215)
            55 => Models.Bytecode.Opcode.CALL_KW_313,         // CALL_KW (enum=216)
            56 => Models.Bytecode.Opcode.COMPARE_OP,          // (enum=107)
            57 => Models.Bytecode.Opcode.CONTAINS_OP,         // (enum=118)
            58 => Models.Bytecode.Opcode.CONVERT_VALUE_313,   // CONVERT_VALUE (enum=226)
            59 => Models.Bytecode.Opcode.COPY,                // COPY (enum=120)
            60 => Models.Bytecode.Opcode.COPY_FREE_VARS_313,  // COPY_FREE_VARS (enum=227)
            61 => Models.Bytecode.Opcode.DELETE_ATTR,         // (enum=108)
            62 => Models.Bytecode.Opcode.DELETE_DEREF,        // (enum=139)
            63 => Models.Bytecode.Opcode.DELETE_FAST,         // (enum=126)
            64 => Models.Bytecode.Opcode.DELETE_GLOBAL,       // (enum=98)
            65 => Models.Bytecode.Opcode.DELETE_NAME,         // (enum=103)
            66 => Models.Bytecode.Opcode.DICT_MERGE,          // DICT_MERGE (enum=164)
            67 => Models.Bytecode.Opcode.DICT_UPDATE,         // DICT_UPDATE (enum=165)
            68 => Models.Bytecode.Opcode.END_ASYNC_FOR_313,   // END_ASYNC_FOR (enum=243)
            69 => Models.Bytecode.Opcode.EXTENDED_ARG,         // EXTENDED_ARG (enum=144)
            70 => Models.Bytecode.Opcode.FOR_ITER,            // FOR_ITER (enum=93)
            71 => Models.Bytecode.Opcode.GET_AWAITABLE_313,   // GET_AWAITABLE (enum=235)
            72 => Models.Bytecode.Opcode.IMPORT_FROM,         // (enum=109)
            73 => Models.Bytecode.Opcode.IMPORT_NAME,         // (enum=108)
            74 => Models.Bytecode.Opcode.IS_OP,               // (enum=117)
            75 => Models.Bytecode.Opcode.JUMP_BACKWARD,       // (enum=140)
            76 => Models.Bytecode.Opcode.JUMP_BACKWARD_NO_INTERRUPT, // (enum=134)
            77 => Models.Bytecode.Opcode.JUMP_FORWARD,        // (enum=110)
            78 => Models.Bytecode.Opcode.LIST_APPEND_313,     // LIST_APPEND (enum=236)
            79 => Models.Bytecode.Opcode.LIST_EXTEND,         // LIST_EXTEND (enum=162)
            80 => Models.Bytecode.Opcode.LOAD_ATTR,           // (enum=106)
            81 => Models.Bytecode.Opcode.LOAD_COMMON_CONSTANT_314, // LOAD_COMMON_CONSTANT (3.14 new)
            82 => Models.Bytecode.Opcode.LOAD_CONST,          // (enum=100)
            83 => Models.Bytecode.Opcode.LOAD_DEREF,          // (enum=137)
            84 => Models.Bytecode.Opcode.LOAD_FAST,           // (enum=124)
            85 => Models.Bytecode.Opcode.LOAD_FAST_AND_CLEAR, // (enum=192)
            86 => Models.Bytecode.Opcode.LOAD_FAST_BORROW_314,  // LOAD_FAST_BORROW (3.14 new)
            87 => Models.Bytecode.Opcode.LOAD_FAST_BORROW_LOAD_FAST_BORROW_314, // (3.14 new)
            88 => Models.Bytecode.Opcode.LOAD_FAST_CHECK,     // LOAD_FAST_CHECK (enum=193)
            89 => Models.Bytecode.Opcode.LOAD_FAST_LOAD_FAST_313, // (enum=218)
            90 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_DEREF, // (enum=176)
            91 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_GLOBALS, // (enum=175)
            92 => Models.Bytecode.Opcode.LOAD_GLOBAL,         // (enum=116)
            93 => Models.Bytecode.Opcode.LOAD_NAME,           // (enum=101)
            94 => Models.Bytecode.Opcode.LOAD_SMALL_INT_314,     // LOAD_SMALL_INT (3.14 new)
            95 => Models.Bytecode.Opcode.LOAD_SPECIAL_314,     // (3.14 new)
            96 => Models.Bytecode.Opcode.LOAD_SUPER_ATTR,     // LOAD_SUPER_ATTR (enum=141)
            97 => Models.Bytecode.Opcode.MAKE_CELL_313,       // MAKE_CELL (enum=219)
            98 => Models.Bytecode.Opcode.MAP_ADD_313,         // MAP_ADD (enum=237)
            99 => Models.Bytecode.Opcode.MATCH_CLASS_313,     // MATCH_CLASS (enum=238)
            100 => Models.Bytecode.Opcode.POP_JUMP_IF_FALSE,  // (enum=114)
            101 => Models.Bytecode.Opcode.POP_JUMP_IF_NONE,   // (enum=195)
            102 => Models.Bytecode.Opcode.POP_JUMP_IF_NOT_NONE, // (enum=194)
            103 => Models.Bytecode.Opcode.POP_JUMP_IF_TRUE,   // (enum=115)
            104 => Models.Bytecode.Opcode.RAISE_VARARGS,      // (enum=130)
            105 => Models.Bytecode.Opcode.RERAISE,            // (enum=119)
            106 => Models.Bytecode.Opcode.SEND,               // (enum=123)
            107 => Models.Bytecode.Opcode.SET_ADD_313,        // SET_ADD (enum=239)
            108 => Models.Bytecode.Opcode.SET_FUNCTION_ATTRIBUTE_313, // (enum=220)
            109 => Models.Bytecode.Opcode.SET_UPDATE,         // SET_UPDATE (enum=163)
            110 => Models.Bytecode.Opcode.STORE_ATTR,         // (enum=95)
            111 => Models.Bytecode.Opcode.STORE_DEREF,        // (enum=138)
            112 => Models.Bytecode.Opcode.STORE_FAST,         // (enum=125)
            113 => Models.Bytecode.Opcode.STORE_FAST_LOAD_FAST_313, // (enum=221)
            114 => Models.Bytecode.Opcode.STORE_FAST_STORE_FAST_313, // (enum=222)
            115 => Models.Bytecode.Opcode.STORE_GLOBAL,       // (enum=97)
            116 => Models.Bytecode.Opcode.STORE_NAME,         // (enum=90)
            117 => Models.Bytecode.Opcode.SWAP,               // SWAP (enum=99)
            118 => Models.Bytecode.Opcode.UNPACK_EX,          // (enum=94)
            119 => Models.Bytecode.Opcode.UNPACK_SEQUENCE,    // (enum=92)
            120 => Models.Bytecode.Opcode.YIELD_VALUE_313,    // YIELD_VALUE (enum=224)
            // 121-127: reserved (unnamed in 3.14 opname)
            128 => Models.Bytecode.Opcode.RESUME_313,         // RESUME (enum=223, 3.14 raw=128)
            // 129+: super-instructions (not mapped, use raw value as fallback)
            _ => (Models.Bytecode.Opcode)rawOp,
        };
    }

    /// <summary>
    /// 3.14 的缓存条目数（CPython 3.14 Lib/opcode.py _cache_format）。
    /// 使用 3.14 原始操作码字节值，因为 3.14 的操作码编号与 3.13 完全不同。
    /// </summary>
    public override int GetCacheCount(byte rawOp)
    {
        return rawOp switch
        {
            38 => 1,  // STORE_SUBSCR (raw 0x26)
            39 => 3,  // TO_BOOL (raw 0x27)
            44 => 5,  // BINARY_OP (raw 0x2c)
            52 => 3,  // CALL (raw 0x34)
            55 => 3,  // CALL_KW (raw 0x37)
            56 => 1,  // COMPARE_OP (raw 0x38)
            57 => 1,  // CONTAINS_OP (raw 0x39)
            70 => 1,  // FOR_ITER (raw 0x46)
            75 => 1,  // JUMP_BACKWARD (raw 0x4b)
            80 => 9,  // LOAD_ATTR (raw 0x50)
            92 => 4,  // LOAD_GLOBAL (raw 0x5c)
            96 => 1,  // LOAD_SUPER_ATTR (raw 0x60)
            100 => 1, // POP_JUMP_IF_FALSE (raw 0x64)
            101 => 1, // POP_JUMP_IF_NONE (raw 0x65)
            102 => 1, // POP_JUMP_IF_NOT_NONE (raw 0x66)
            103 => 1, // POP_JUMP_IF_TRUE (raw 0x67)
            106 => 1, // SEND (raw 0x6a)
            110 => 4, // STORE_ATTR (raw 0x6e)
            119 => 1, // UNPACK_SEQUENCE (raw 0x77)
            _ => 0,
        };
    }

    /// <summary>
    /// 3.11+ 跳转指令检测（含 TO_BOOL_313 和 POP_ITER_314）。
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
