using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Versioning;

/// <summary>
/// Python 3.14 版本策略。
/// 3.14 的操作码编号体系与 3.13 完全不同（HAVE_ARGUMENT=41）。
/// 新增多个操作码：LOAD_SMALL_INT, LOAD_FAST_BORROW, POP_ITER, NOT_TAKEN 等。
/// 
/// 来源: CPython main/Include/opcode_ids.h (2026-07-02)
/// </summary>
public class VersionStrategy314 : VersionStrategyBase
{
    public override PythonVersion Version => PythonVersion.Py314;
    public override string DisplayName => "Python 3.14";

    // 3.14 使用 16 字节头部（PEP 552）
    public override int HeaderSize => 16;
    // 3.14: HAVE_ARGUMENT=41 (opcodes 0-40 无参, 41+ 有参)
    public override int HaveArgument => 41;

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
    /// 来源: CPython main/Include/opcode_ids.h
    /// HAVE_ARGUMENT=41，操作码 0-40 无参数，41+ 有参数（含 RESUME=128）。
    /// </summary>
    public override Opcode MapOpcode(byte rawOp)
    {
        return rawOp switch
        {
            // --- 无参操作码 (0-40, HAVE_ARGUMENT=41) ---
            0 => Models.Bytecode.Opcode.NOP,                    // CACHE（已在前端跳过，映射为 NOP 无害）
            1 => Models.Bytecode.Opcode.BINARY_SLICE_313,       // BINARY_SLICE
            2 => Models.Bytecode.Opcode.BUILD_INTERPOLATION_314, // BUILD_TEMPLATE (3.14 新 f-string 操作)
            3 => Models.Bytecode.Opcode.BINARY_OP_INPLACE_ADD_UNICODE_314, // (3.14 new, 特化操作码)
            4 => Models.Bytecode.Opcode.CALL_FUNCTION_EX,       // CALL_FUNCTION_EX
            5 => Models.Bytecode.Opcode.CHECK_EG_MATCH,         // CHECK_EG_MATCH
            6 => Models.Bytecode.Opcode.CHECK_EXC_MATCH,        // CHECK_EXC_MATCH
            7 => Models.Bytecode.Opcode.CLEANUP_THROW_313,      // CLEANUP_THROW
            8 => Models.Bytecode.Opcode.DELETE_SUBSCR_313,      // DELETE_SUBSCR
            9 => Models.Bytecode.Opcode.END_FOR_313,            // END_FOR
            10 => Models.Bytecode.Opcode.END_SEND_313,           // END_SEND
            11 => Models.Bytecode.Opcode.EXIT_INIT_CHECK_313,    // EXIT_INIT_CHECK
            12 => Models.Bytecode.Opcode.FORMAT_SIMPLE_313,      // FORMAT_SIMPLE
            13 => Models.Bytecode.Opcode.FORMAT_WITH_SPEC_313,   // FORMAT_WITH_SPEC
            14 => Models.Bytecode.Opcode.GET_AITER_313,          // GET_AITER
            15 => Models.Bytecode.Opcode.GET_ANEXT_313,          // GET_ANEXT
            16 => Models.Bytecode.Opcode.GET_LEN_313,            // GET_LEN
            17 => Models.Bytecode.Opcode.RESERVED_313,           // RESERVED
            18 => Models.Bytecode.Opcode.INTERPRETER_EXIT,       // INTERPRETER_EXIT
            19 => Models.Bytecode.Opcode.LOAD_BUILD_CLASS,       // LOAD_BUILD_CLASS (71)
            20 => Models.Bytecode.Opcode.LOAD_LOCALS_313,        // LOAD_LOCALS
            21 => Models.Bytecode.Opcode.MAKE_FUNCTION,          // MAKE_FUNCTION (132)
            22 => Models.Bytecode.Opcode.MATCH_KEYS_313,         // MATCH_KEYS
            23 => Models.Bytecode.Opcode.MATCH_MAPPING_313,      // MATCH_MAPPING
            24 => Models.Bytecode.Opcode.MATCH_SEQUENCE_313,     // MATCH_SEQUENCE
            25 => Models.Bytecode.Opcode.NOP,                    // NOP (9)
            26 => Models.Bytecode.Opcode.NOT_TAKEN_314,          // NOT_TAKEN (3.14 new)
            27 => Models.Bytecode.Opcode.POP_EXCEPT,             // POP_EXCEPT (89)
            28 => Models.Bytecode.Opcode.POP_ITER_314,           // POP_ITER (3.14 new)
            29 => Models.Bytecode.Opcode.POP_TOP,                // POP_TOP (1)
            30 => Models.Bytecode.Opcode.PUSH_EXC_INFO_312,      // PUSH_EXC_INFO (179)
            31 => Models.Bytecode.Opcode.PUSH_NULL,              // PUSH_NULL (2)
            32 => Models.Bytecode.Opcode.RETURN_GENERATOR_313,   // RETURN_GENERATOR
            33 => Models.Bytecode.Opcode.RETURN_VALUE,           // RETURN_VALUE (83)
            34 => Models.Bytecode.Opcode.SETUP_ANNOTATIONS,      // SETUP_ANNOTATIONS (85)
            35 => Models.Bytecode.Opcode.STORE_SLICE_313,        // STORE_SLICE
            36 => Models.Bytecode.Opcode.STORE_SUBSCR,           // STORE_SUBSCR (49)
            37 => Models.Bytecode.Opcode.TO_BOOL_313,            // TO_BOOL (213)
            38 => Models.Bytecode.Opcode.UNARY_INVERT,           // UNARY_INVERT (15)
            39 => Models.Bytecode.Opcode.UNARY_NEGATIVE,         // UNARY_NEGATIVE (11)
            40 => Models.Bytecode.Opcode.UNARY_NOT,              // UNARY_NOT (12)

            // --- 有参操作码 (41+) ---
            41 => Models.Bytecode.Opcode.WITH_EXCEPT_START,      // WITH_EXCEPT_START (188)
            42 => Models.Bytecode.Opcode.BINARY_OP,              // BINARY_OP (191)
            43 => Models.Bytecode.Opcode.BUILD_INTERPOLATION_314, // BUILD_INTERPOLATION (3.14 new, 260)
            44 => Models.Bytecode.Opcode.BUILD_LIST,             // BUILD_LIST (103)
            45 => Models.Bytecode.Opcode.BUILD_MAP,              // BUILD_MAP (105)
            46 => Models.Bytecode.Opcode.BUILD_SET,              // BUILD_SET (104)
            47 => Models.Bytecode.Opcode.BUILD_SLICE,            // BUILD_SLICE (133)
            48 => Models.Bytecode.Opcode.BUILD_STRING,           // BUILD_STRING (157)
            49 => Models.Bytecode.Opcode.BUILD_TUPLE,            // BUILD_TUPLE (102)
            50 => Models.Bytecode.Opcode.CALL,                   // CALL (171)
            51 => Models.Bytecode.Opcode.CALL_INTRINSIC_1_313,   // CALL_INTRINSIC_1 (214)
            52 => Models.Bytecode.Opcode.CALL_INTRINSIC_2_313,   // CALL_INTRINSIC_2 (215)
            53 => Models.Bytecode.Opcode.CALL_KW_313,            // CALL_KW (216)
            54 => Models.Bytecode.Opcode.COMPARE_OP,             // COMPARE_OP (107)
            55 => Models.Bytecode.Opcode.CONTAINS_OP,            // CONTAINS_OP (118)
            56 => Models.Bytecode.Opcode.CONVERT_VALUE_313,      // CONVERT_VALUE (226)
            57 => Models.Bytecode.Opcode.COPY,                   // COPY (120)
            58 => Models.Bytecode.Opcode.COPY_FREE_VARS_313,     // COPY_FREE_VARS (227)
            59 => Models.Bytecode.Opcode.DELETE_ATTR,            // DELETE_ATTR (108)
            60 => Models.Bytecode.Opcode.DELETE_DEREF,           // DELETE_DEREF (139)
            61 => Models.Bytecode.Opcode.DELETE_FAST,            // DELETE_FAST (126)
            62 => Models.Bytecode.Opcode.DICT_MERGE,             // DICT_MERGE (164)
            63 => Models.Bytecode.Opcode.DICT_UPDATE,            // DICT_UPDATE (165)
            64 => Models.Bytecode.Opcode.END_ASYNC_FOR_313,      // END_ASYNC_FOR (243)
            65 => Models.Bytecode.Opcode.EXTENDED_ARG,           // EXTENDED_ARG (144)
            66 => Models.Bytecode.Opcode.FOR_ITER,               // FOR_ITER (93)
            67 => Models.Bytecode.Opcode.GET_AWAITABLE_313,      // GET_AWAITABLE (235)
            68 => Models.Bytecode.Opcode.GET_ITER,               // GET_ITER (68)
            69 => Models.Bytecode.Opcode.IMPORT_FROM,            // IMPORT_FROM (109)
            70 => Models.Bytecode.Opcode.IMPORT_NAME,            // IMPORT_NAME (108)
            71 => Models.Bytecode.Opcode.IS_OP,                  // IS_OP (117)
            72 => Models.Bytecode.Opcode.JUMP_BACKWARD,          // JUMP_BACKWARD (140)
            73 => Models.Bytecode.Opcode.JUMP_BACKWARD_NO_INTERRUPT, // JUMP_BACKWARD_NO_INTERRUPT (134)
            74 => Models.Bytecode.Opcode.JUMP_FORWARD,           // JUMP_FORWARD (110)
            75 => Models.Bytecode.Opcode.LIST_APPEND_313,        // LIST_APPEND (236)
            76 => Models.Bytecode.Opcode.LIST_EXTEND,            // LIST_EXTEND (162)
            77 => Models.Bytecode.Opcode.LOAD_ATTR,              // LOAD_ATTR (106)
            78 => Models.Bytecode.Opcode.LOAD_COMMON_CONSTANT_314, // LOAD_COMMON_CONSTANT (3.14 new, 259)
            79 => Models.Bytecode.Opcode.LOAD_CONST,             // LOAD_CONST (100)
            80 => Models.Bytecode.Opcode.LOAD_DEREF,             // LOAD_DEREF (137)
            81 => Models.Bytecode.Opcode.LOAD_FAST,              // LOAD_FAST (124)
            82 => Models.Bytecode.Opcode.LOAD_FAST_AND_CLEAR,    // LOAD_FAST_AND_CLEAR (192)
            83 => Models.Bytecode.Opcode.LOAD_FAST_BORROW_314,   // LOAD_FAST_BORROW (3.14 new, 255)
            84 => Models.Bytecode.Opcode.LOAD_FAST_BORROW_LOAD_FAST_BORROW_314, // (3.14 new, 256)
            85 => Models.Bytecode.Opcode.LOAD_FAST_CHECK,        // LOAD_FAST_CHECK (193)
            86 => Models.Bytecode.Opcode.LOAD_FAST_LOAD_FAST_313, // LOAD_FAST_LOAD_FAST (218)
            87 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_DEREF, // LOAD_FROM_DICT_OR_DEREF (176)
            88 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_GLOBALS, // LOAD_FROM_DICT_OR_GLOBALS (175)
            89 => Models.Bytecode.Opcode.LOAD_GLOBAL,            // LOAD_GLOBAL (116)
            90 => Models.Bytecode.Opcode.LOAD_NAME,              // LOAD_NAME (101)
            91 => Models.Bytecode.Opcode.LOAD_SMALL_INT_314,     // LOAD_SMALL_INT (3.14 new, 254)
            92 => Models.Bytecode.Opcode.LOAD_SPECIAL_314,       // LOAD_SPECIAL (3.14 new, 262)
            93 => Models.Bytecode.Opcode.LOAD_SUPER_ATTR,        // LOAD_SUPER_ATTR (141)
            94 => Models.Bytecode.Opcode.MAKE_CELL_313,          // MAKE_CELL (219)
            95 => Models.Bytecode.Opcode.MAP_ADD_313,            // MAP_ADD (237)
            96 => Models.Bytecode.Opcode.MATCH_CLASS_313,        // MATCH_CLASS (238)
            97 => Models.Bytecode.Opcode.POP_JUMP_IF_FALSE,      // POP_JUMP_IF_FALSE (114)
            98 => Models.Bytecode.Opcode.POP_JUMP_IF_NONE,       // POP_JUMP_IF_NONE (195)
            99 => Models.Bytecode.Opcode.POP_JUMP_IF_NOT_NONE,   // POP_JUMP_IF_NOT_NONE (194)
            100 => Models.Bytecode.Opcode.POP_JUMP_IF_TRUE,      // POP_JUMP_IF_TRUE (115)
            101 => Models.Bytecode.Opcode.RAISE_VARARGS,         // RAISE_VARARGS (130)
            102 => Models.Bytecode.Opcode.RERAISE,               // RERAISE (119)
            103 => Models.Bytecode.Opcode.SEND,                  // SEND (123)
            104 => Models.Bytecode.Opcode.SET_ADD_313,           // SET_ADD (239)
            105 => Models.Bytecode.Opcode.SET_FUNCTION_ATTRIBUTE_313, // SET_FUNCTION_ATTRIBUTE (220)
            106 => Models.Bytecode.Opcode.SET_UPDATE,            // SET_UPDATE (163)
            107 => Models.Bytecode.Opcode.STORE_ATTR,            // STORE_ATTR (95)
            108 => Models.Bytecode.Opcode.STORE_DEREF,           // STORE_DEREF (196)
            109 => Models.Bytecode.Opcode.STORE_FAST,            // STORE_FAST (125)
            110 => Models.Bytecode.Opcode.STORE_FAST_LOAD_FAST_313, // STORE_FAST_LOAD_FAST (221)
            111 => Models.Bytecode.Opcode.STORE_FAST_STORE_FAST_313, // STORE_FAST_STORE_FAST (222)
            112 => Models.Bytecode.Opcode.STORE_GLOBAL,          // STORE_GLOBAL (97)
            113 => Models.Bytecode.Opcode.STORE_NAME,            // STORE_NAME (90)
            114 => Models.Bytecode.Opcode.SWAP,                  // SWAP (99)
            115 => Models.Bytecode.Opcode.UNPACK_EX,             // UNPACK_EX (94)
            116 => Models.Bytecode.Opcode.UNPACK_SEQUENCE,       // UNPACK_SEQUENCE (92)
            117 => Models.Bytecode.Opcode.YIELD_VALUE_313,       // YIELD_VALUE (224)
            // 118-127: reserved/unused in 3.14 opcode_ids.h
            // 128: RESUME (特殊：有参无参分界之上但仍为 2 字节指令)
            128 => Models.Bytecode.Opcode.RESUME_313,            // RESUME (223, 3.14 raw=128)
            // 129+: super-instructions / instrumented opcodes — 不映射，使用原始值降级
            _ => (Models.Bytecode.Opcode)rawOp,
        };
    }

    /// <summary>
    /// 3.14 的缓存条目数（CPython 3.14 main/Lib/opcode.py _cache_format）。
    /// 使用 3.14 原始操作码字节值。
    /// 来源: CPython main/Lib/opcode.py _inline_cache_entries (2026-07-02)
    /// </summary>
    public override bool RequiresArgument(byte rawOp)
    {
        // HAVE_ARGUMENT=41 意味着 raw >= 41 都有参数
        if (rawOp >= HaveArgument)
            return true;
        // 少数无参区域中的例外：CALL_FUNCTION_EX(4) 也需要参数
        return rawOp switch
        {
            4 => true,   // CALL_FUNCTION_EX (flags)
            _ => false,
        };
    }

    public override int GetCacheCount(byte rawOp)
    {
        return rawOp switch
        {
            // _cache_format entries from CPython 3.14 main
            36 => 1,  // STORE_SUBSCR
            37 => 3,  // TO_BOOL (counter=1, version=2)
            42 => 5,  // BINARY_OP (counter=1, descr=4)
            50 => 3,  // CALL (counter=1, func_version=2)
            53 => 3,  // CALL_KW (counter=1, func_version=2)
            54 => 1,  // COMPARE_OP
            55 => 1,  // CONTAINS_OP
            66 => 1,  // FOR_ITER
            68 => 1,  // GET_ITER (3.14 new cache!)
            72 => 1,  // JUMP_BACKWARD
            77 => 9,  // LOAD_ATTR (counter=1, version=2, keys_version=2, descr=4)
            89 => 4,  // LOAD_GLOBAL (counter=1, index=1, module_keys=1, builtin_keys=1)
            93 => 1,  // LOAD_SUPER_ATTR
            97 => 1,  // POP_JUMP_IF_FALSE
            98 => 1,  // POP_JUMP_IF_NONE
            99 => 1,  // POP_JUMP_IF_NOT_NONE
            100 => 1, // POP_JUMP_IF_TRUE
            103 => 1, // SEND
            107 => 4, // STORE_ATTR (counter=1, version=2, index=1)
            116 => 1, // UNPACK_SEQUENCE
            128 => 1, // RESUME (3.14 new: counter=1)
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
