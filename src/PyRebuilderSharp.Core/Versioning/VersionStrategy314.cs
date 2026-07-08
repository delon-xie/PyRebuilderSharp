using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Versioning;

/// <summary>
/// Python 3.14 操作码映射策略。
/// 依据 CPython 3.14.3 (Lib/opcode.py + Include/opcode_ids.h) 精确对照。
/// HAVE_ARGUMENT = 43，opcodes 0-42 为无参指令，43+ 为有参指令。
/// </summary>
public class VersionStrategy314 : VersionStrategyBase
{
    public override PythonVersion Version => PythonVersion.Py314;
    public override string DisplayName => "Python 3.14";

    public override int HeaderSize => 16;
    public override int HaveArgument => 43;

    public override bool IsWordOffset => true;
    public override bool HasCaches => true;
    public override bool HasExceptionTable => true;
    public override bool HasQualname => true;
    public override bool SupportsCodeSimple => true;
    public override bool UseLocalsPlus => true;
    public override bool HasLinetable => true;
    public override bool HasPep552Header => true;
    public override bool HasPosOnlyArgCount => true;

    public override Opcode MapOpcode(byte rawOp)
    {
        return rawOp switch
        {
            // === 无参操作码 (0-42, HAVE_ARGUMENT=43) ===
            // 对照 CPython 3.14 opcode.py opmap
            0 => Models.Bytecode.Opcode.NOP,               // CACHE (解析器已跳过 raw 0)
            1 => Models.Bytecode.Opcode.BINARY_SLICE_313,
            2 => Models.Bytecode.Opcode.BEFORE_WITH_313,          // BEFORE_WITH (shared with 3.13)
            4 => Models.Bytecode.Opcode.CALL_FUNCTION_EX,
            5 => Models.Bytecode.Opcode.CHECK_EG_MATCH,
            6 => Models.Bytecode.Opcode.CHECK_EXC_MATCH,
            7 => Models.Bytecode.Opcode.CLEANUP_THROW_313,
            8 => Models.Bytecode.Opcode.DELETE_SUBSCR_313,
            9 => Models.Bytecode.Opcode.END_FOR_313,
            10 => Models.Bytecode.Opcode.END_SEND_313,
            11 => Models.Bytecode.Opcode.EXIT_INIT_CHECK_313,
            12 => Models.Bytecode.Opcode.FORMAT_SIMPLE_313,
            13 => Models.Bytecode.Opcode.FORMAT_WITH_SPEC_313,
            14 => Models.Bytecode.Opcode.GET_AITER_313,
            15 => Models.Bytecode.Opcode.GET_ANEXT_313,
            16 => Models.Bytecode.Opcode.GET_ITER,
            17 => Models.Bytecode.Opcode.RESERVED_313,     // RESERVED
            18 => Models.Bytecode.Opcode.GET_LEN_313,
            19 => Models.Bytecode.Opcode.GET_YIELD_FROM_ITER,
            20 => Models.Bytecode.Opcode.INTERPRETER_EXIT,
            21 => Models.Bytecode.Opcode.LOAD_BUILD_CLASS,
            22 => Models.Bytecode.Opcode.LOAD_LOCALS_313,
            23 => Models.Bytecode.Opcode.MAKE_FUNCTION,
            24 => Models.Bytecode.Opcode.MATCH_KEYS_313,    // 3.14 新位置
            25 => Models.Bytecode.Opcode.MATCH_MAPPING_313,
            26 => Models.Bytecode.Opcode.MATCH_SEQUENCE_313,
            27 => Models.Bytecode.Opcode.NOP,               // NOP
            28 => Models.Bytecode.Opcode.NOT_TAKEN_314,     // NOT_TAKEN
            29 => Models.Bytecode.Opcode.POP_EXCEPT,
            30 => Models.Bytecode.Opcode.POP_ITER_314,
            31 => Models.Bytecode.Opcode.POP_TOP,
            32 => Models.Bytecode.Opcode.PUSH_EXC_INFO_312,
            33 => Models.Bytecode.Opcode.PUSH_NULL,
            34 => Models.Bytecode.Opcode.RETURN_GENERATOR_313,
            35 => Models.Bytecode.Opcode.RETURN_VALUE,
            36 => Models.Bytecode.Opcode.SETUP_ANNOTATIONS,
            37 => Models.Bytecode.Opcode.STORE_SLICE_313,
            38 => Models.Bytecode.Opcode.STORE_SUBSCR,
            39 => Models.Bytecode.Opcode.TO_BOOL_313,
            40 => Models.Bytecode.Opcode.UNARY_INVERT,
            41 => Models.Bytecode.Opcode.UNARY_NEGATIVE,
            42 => Models.Bytecode.Opcode.UNARY_NOT,

            // === 有参操作码 (43+) ===
            43 => Models.Bytecode.Opcode.WITH_EXCEPT_START,
            44 => Models.Bytecode.Opcode.BINARY_OP,
            45 => Models.Bytecode.Opcode.BUILD_INTERPOLATION_314,
            46 => Models.Bytecode.Opcode.BUILD_LIST,
            47 => Models.Bytecode.Opcode.BUILD_MAP,
            48 => Models.Bytecode.Opcode.BUILD_SET,
            49 => Models.Bytecode.Opcode.BUILD_SLICE,
            50 => Models.Bytecode.Opcode.BUILD_STRING,
            51 => Models.Bytecode.Opcode.BUILD_TUPLE,
            52 => Models.Bytecode.Opcode.CALL,
            53 => Models.Bytecode.Opcode.CALL_INTRINSIC_1_313,
            54 => Models.Bytecode.Opcode.CALL_INTRINSIC_2_313,
            55 => Models.Bytecode.Opcode.CALL_KW_313,
            56 => Models.Bytecode.Opcode.COMPARE_OP,
            57 => Models.Bytecode.Opcode.CONTAINS_OP,
            58 => Models.Bytecode.Opcode.CONVERT_VALUE_313,
            59 => Models.Bytecode.Opcode.COPY,
            60 => Models.Bytecode.Opcode.COPY_FREE_VARS_313,
            61 => Models.Bytecode.Opcode.DELETE_ATTR,
            62 => Models.Bytecode.Opcode.DELETE_DEREF,
            63 => Models.Bytecode.Opcode.DELETE_FAST,
            64 => Models.Bytecode.Opcode.DELETE_GLOBAL,
            65 => Models.Bytecode.Opcode.DELETE_NAME,
            66 => Models.Bytecode.Opcode.DICT_MERGE,
            67 => Models.Bytecode.Opcode.DICT_UPDATE,
            68 => Models.Bytecode.Opcode.END_ASYNC_FOR_313,
            69 => Models.Bytecode.Opcode.EXTENDED_ARG,
            70 => Models.Bytecode.Opcode.FOR_ITER,
            71 => Models.Bytecode.Opcode.GET_AWAITABLE_313,
            72 => Models.Bytecode.Opcode.IMPORT_FROM,
            73 => Models.Bytecode.Opcode.IMPORT_NAME,
            74 => Models.Bytecode.Opcode.IS_OP,
            75 => Models.Bytecode.Opcode.JUMP_BACKWARD,
            76 => Models.Bytecode.Opcode.JUMP_BACKWARD_NO_INTERRUPT,
            77 => Models.Bytecode.Opcode.JUMP_FORWARD,
            78 => Models.Bytecode.Opcode.LIST_APPEND_313,
            79 => Models.Bytecode.Opcode.LIST_EXTEND,
            80 => Models.Bytecode.Opcode.LOAD_ATTR,
            81 => Models.Bytecode.Opcode.LOAD_COMMON_CONSTANT_314,
            82 => Models.Bytecode.Opcode.LOAD_CONST,
            83 => Models.Bytecode.Opcode.LOAD_DEREF,
            84 => Models.Bytecode.Opcode.LOAD_FAST,
            85 => Models.Bytecode.Opcode.LOAD_FAST_AND_CLEAR,
            86 => Models.Bytecode.Opcode.LOAD_FAST_BORROW_314,
            87 => Models.Bytecode.Opcode.LOAD_FAST_BORROW_LOAD_FAST_BORROW_314,
            88 => Models.Bytecode.Opcode.LOAD_FAST_CHECK,
            89 => Models.Bytecode.Opcode.LOAD_FAST_LOAD_FAST_313,
            90 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_DEREF,
            91 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_GLOBALS,
            92 => Models.Bytecode.Opcode.LOAD_GLOBAL,
            93 => Models.Bytecode.Opcode.LOAD_NAME,
            94 => Models.Bytecode.Opcode.LOAD_SMALL_INT_314,
            95 => Models.Bytecode.Opcode.LOAD_SPECIAL,
            96 => Models.Bytecode.Opcode.LOAD_SUPER_ATTR,
            97 => Models.Bytecode.Opcode.MAKE_CELL_313,          // 3.14: MAKE_CELL
            98 => Models.Bytecode.Opcode.MAP_ADD_313,            // 3.14: MAP_ADD
            99 => Models.Bytecode.Opcode.MATCH_CLASS_313,        // 3.14: MATCH_CLASS
            100 => Models.Bytecode.Opcode.POP_JUMP_IF_FALSE,
            101 => Models.Bytecode.Opcode.POP_JUMP_IF_NONE,
            102 => Models.Bytecode.Opcode.POP_JUMP_IF_NOT_NONE,
            103 => Models.Bytecode.Opcode.POP_JUMP_IF_TRUE,
            104 => Models.Bytecode.Opcode.RAISE_VARARGS,
            105 => Models.Bytecode.Opcode.RERAISE,
            106 => Models.Bytecode.Opcode.SEND,
            107 => Models.Bytecode.Opcode.SET_ADD_313,
            108 => Models.Bytecode.Opcode.SET_FUNCTION_ATTRIBUTE_313,
            109 => Models.Bytecode.Opcode.SET_UPDATE,
            110 => Models.Bytecode.Opcode.STORE_ATTR,
            111 => Models.Bytecode.Opcode.STORE_DEREF,
            112 => Models.Bytecode.Opcode.STORE_FAST,
            113 => Models.Bytecode.Opcode.STORE_FAST_LOAD_FAST_313,
            114 => Models.Bytecode.Opcode.STORE_FAST_STORE_FAST_313,
            115 => Models.Bytecode.Opcode.STORE_GLOBAL,
            116 => Models.Bytecode.Opcode.STORE_NAME,
            117 => Models.Bytecode.Opcode.SWAP,
            118 => Models.Bytecode.Opcode.UNPACK_EX,
            119 => Models.Bytecode.Opcode.UNPACK_SEQUENCE,
            120 => Models.Bytecode.Opcode.YIELD_VALUE_313,
            128 => Models.Bytecode.Opcode.RESUME_313,
            _ => (Models.Bytecode.Opcode)rawOp,
        };
    }

    /// <summary>
    /// 3.14 中 CALL_FUNCTION_EX (raw 4) 位于 HAVE_ARGUMENT=43 之下，无参数。
    /// </summary>
    public override bool RequiresArgument(byte rawOp)
    {
        return rawOp >= HaveArgument;
    }

    /// <summary>
    /// 内联缓存数量，对照 CPython 3.14 _inline_cache_entries。
    /// 每条 cache entry 占 2 字节（1 word）。
    /// </summary>
    public override int GetCacheCount(byte rawOp)
    {
        return rawOp switch
        {
            38 => 1,   // STORE_SUBSCR
            39 => 3,   // TO_BOOL
            44 => 5,   // BINARY_OP
            52 => 3,   // CALL
            55 => 3,   // CALL_KW
            56 => 1,   // COMPARE_OP
            57 => 1,   // CONTAINS_OP
            70 => 1,   // FOR_ITER
            75 => 1,   // JUMP_BACKWARD
            80 => 9,   // LOAD_ATTR
            92 => 4,   // LOAD_GLOBAL
            96 => 1,   // LOAD_SUPER_ATTR
            100 => 1,  // POP_JUMP_IF_FALSE
            101 => 1,  // POP_JUMP_IF_NONE
            102 => 1,  // POP_JUMP_IF_NOT_NONE
            103 => 1,  // POP_JUMP_IF_TRUE
            106 => 1,  // SEND
            110 => 4,  // STORE_ATTR
            119 => 1,  // UNPACK_SEQUENCE
            128 => 0,   // RESUME (3.14 无 CACHE 条目)
            _ => 0,
        };
    }

    public override bool IsJumpInstruction(Opcode op) => op switch
    {
        Models.Bytecode.Opcode.JUMP_FORWARD or Models.Bytecode.Opcode.JUMP_BACKWARD
            or Models.Bytecode.Opcode.POP_JUMP_IF_FALSE or Models.Bytecode.Opcode.POP_JUMP_IF_TRUE
            or Models.Bytecode.Opcode.POP_JUMP_IF_NOT_NONE or Models.Bytecode.Opcode.POP_JUMP_IF_NONE
            or Models.Bytecode.Opcode.FOR_ITER or Models.Bytecode.Opcode.JUMP_BACKWARD_NO_INTERRUPT
            or Models.Bytecode.Opcode.JUMP_ABSOLUTE or Models.Bytecode.Opcode.JUMP_IF_TRUE_OR_POP
            or Models.Bytecode.Opcode.JUMP_IF_FALSE_OR_POP
            or Models.Bytecode.Opcode.SEND => true,
        _ => false,
    };
}
