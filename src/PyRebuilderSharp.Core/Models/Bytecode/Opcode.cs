namespace PyRebuilderSharp.Core.Models.Bytecode;

/// <summary>
/// Python字节码操作码枚举。
/// 覆盖Python 2.7 + 3.5~3.14的所有操作码。
/// 所有版本统一的底层数值（带版本名称后缀的为别名）。
/// 
/// 各版本跳转指令值（2.7~3.10 一致）：
///   JUMP_IF_FALSE_OR_POP = 111
///   JUMP_IF_TRUE_OR_POP  = 112
///   POP_JUMP_IF_FALSE    = 114
///   POP_JUMP_IF_TRUE     = 115
/// 3.9+ 新增：
///   IS_OP      = 117
///   CONTAINS_OP = 118
/// </summary>
public enum Opcode
{
    // --- 栈操作 (0-99) ---
    POP_TOP = 1,
    ROT_TWO = 2,
    ROT_THREE = 3,
    DUP_TOP = 4,
    DUP_TOP_TWO = 5,
    NOP = 9,
    UNPACK_SEQUENCE = 92,  // 所有版本
    UNPACK_EX = 94,        // 所有版本

    // --- 一元运算 (11-15) ---
    UNARY_NEGATIVE = 11,
    UNARY_NOT = 12,
    UNARY_INVERT = 15,

    // --- 二元运算 (19-31) ---
    BINARY_POWER = 19,
    BINARY_MULTIPLY = 20,
    BINARY_DIVIDE = 21,       // Python 2 only (2.7)
    BINARY_MODULO = 22,
    BINARY_ADD = 23,
    BINARY_SUBTRACT = 24,
    BINARY_SUBSCR = 25,
    BINARY_FLOOR_DIVIDE = 26,
    BINARY_TRUE_DIVIDE = 27,
    BINARY_LSHIFT = 62,
    BINARY_RSHIFT = 63,
    BINARY_AND = 64,
    BINARY_XOR = 65,
    BINARY_OR = 66,

    // --- 原地运算 ---
    INPLACE_ADD = 55,
    INPLACE_SUBTRACT = 56,

    // --- 订阅操作 ---
    STORE_SUBSCR = 49,
    SLICE_0 = 30,       // Python 2: TOS = TOS[:]
    SLICE_1 = 31,       // Python 2: TOS = TOS1[TOS:]
    SLICE_2 = 32,       // Python 2: TOS = TOS1[:TOS]
    SLICE_3 = 33,       // Python 2: TOS = TOS2[TOS1:TOS]
    STORE_SLICE_0 = 40, // Python 2: TOS[TOS1] = TOS2 (TOS[:] = ...)
    STORE_SLICE_1 = 41, // Python 2: TOS1[TOS2:] = TOS
    STORE_SLICE_2 = 42, // Python 2: TOS1[:TOS2] = TOS
    STORE_SLICE_3 = 43, // Python 2: TOS2[TOS1:TOS] = TOS
    DELETE_SLICE_0 = 50,// Python 2: del TOS[:]
    DELETE_SLICE_1 = 51,// Python 2: del TOS1[TOS:]
    DELETE_SLICE_2 = 52,// Python 2: del TOS1[:TOS]
    DELETE_SLICE_3 = 53,// Python 2: del TOS2[TOS1:TOS]

    // --- 构建操作 (102-159) ---
    BUILD_TUPLE = 102,
    BUILD_LIST = 103,
    BUILD_SET = 104,
    BUILD_MAP = 105,
    BUILD_SLICE = 133,    // 3.5-3.10
    FORMAT_VALUE = 155,    // 3.6+: format value for f-string
    BUILD_STRING = 157,    // 3.6+: build f-string from formatted values

    // --- 导入 (108-109) ---
    IMPORT_NAME = 108,
    IMPORT_FROM = 109,
    IMPORT_STAR = 84,

    // --- 常量加载 (100) ---
    LOAD_CONST = 100,

    // --- 名称操作 ---
    LOAD_NAME = 101,
    STORE_NAME = 90,
    DELETE_NAME = 103,
    STORE_ATTR = 95,
    LOAD_ATTR = 106,
    DELETE_ATTR = 108,
    STORE_GLOBAL = 97,
    LOAD_GLOBAL = 116,
    DELETE_GLOBAL = 98,

    // --- 局部变量 ---
    LOAD_FAST = 124,
    STORE_FAST = 125,
    DELETE_FAST = 126,

    // --- 比较 (3.8 及更早用 COMPARE_OP; 3.9+ 用 IS_OP / CONTAINS_OP) ---
    COMPARE_OP = 107,
    IS_OP = 117,           // 3.9+: 0=is, 1=is not
    CONTAINS_OP = 118,     // 3.9+: 0=in, 1=not in

    // --- 跳转 ---
    JUMP_FORWARD = 110,
    JUMP_IF_FALSE_OR_POP = 111,  // 所有版本（2.7~3.10）一致
    JUMP_IF_TRUE_OR_POP = 112,   // 所有版本（2.7~3.10）一致
    JUMP_ABSOLUTE = 113,
    JUMP_BACKWARD = 140,
    POP_JUMP_IF_FALSE = 114,     // 所有版本（2.7~3.10）一致
    POP_JUMP_IF_TRUE = 115,      // 所有版本（2.7~3.10）一致

    // 旧名称别名（兼容，值正确）
    POP_JUMP_IF_TRUE_PY38 = JUMP_IF_FALSE_OR_POP,   // 旧名，实际是 JUMP_IF_FALSE_OR_POP
    POP_JUMP_IF_FALSE_PY38 = JUMP_IF_TRUE_OR_POP,   // 旧名，实际是 JUMP_IF_TRUE_OR_POP

    // --- 循环 ---
    GET_ITER = 68,
    GET_YIELD_FROM_ITER = 69,  // Python 3.5+: yield from 迭代器包装
    FOR_ITER = 93,

    // --- 调用 ---
    CALL_FUNCTION = 131,     // 3.5-3.10: call function
    CALL_FUNCTION_KW = 141,  // 3.5-3.10: call with keyword args
    LOAD_METHOD = 160,       // 3.7-3.9: method call optimization
    CALL_METHOD = 161,       // 3.7-3.9: method call optimization

    // --- 返回 (83-87) ---
    RETURN_VALUE = 83,
    YIELD_VALUE = 86,
    POP_BLOCK = 87,         // Python 2.7 + 3.0-3.10；3.11+ 移除

    // --- Python 2.7 特有操作码（使用 200+ 范围避免与 v3.x 冲突）---
    PRINT_EXPR = 200,        // Python 2.7 only (raw 70)
    PRINT_ITEM = 201,        // Python 2.7 only (raw 71)
    PRINT_NEWLINE = 202,     // Python 2.7 only (raw 72)
    PRINT_ITEM_TO = 203,     // Python 2.7 only (raw 73)
    PRINT_NEWLINE_TO = 204,  // Python 2.7 only (raw 74)
    BREAK_LOOP = 205,        // Python 2.7 only (raw 80)
    CONTINUE_LOOP = 206,     // Python 2.7 only (raw 119)
    SETUP_LOOP = 207,        // Python 2.7 only (raw 120)
    SETUP_EXCEPT_27 = 211,   // Python 2.7 only (raw 121, 3.8+ = JUMP_IF_NOT_EXC_MATCH)
    IMPORT_STAR_27 = 208,    // Python 2.7 only (raw 84)
    EXEC_STMT = 209,         // Python 2.7 only (raw 85)
    BUILD_CLASS_27 = 210,    // Python 2.7 only (raw 89, but BUILD_CLASS was removed in 3.x)

    // --- Yield from ---
    YIELD_FROM = 87,        // Python 3.5-3.9: yield from (87)
    YIELD_FROM_PY310 = 72,  // Python 3.10: yield from 重编号为 72

    // --- 异常 ---
    SETUP_ANNOTATIONS = 85,
    END_FINALLY = 88,
    POP_EXCEPT = 89,
    SETUP_EXCEPT = 121,    // Python 3.5-3.7 (3.8+ 中被 JUMP_IF_NOT_EXC_MATCH 替代)
    SETUP_FINALLY = 122,   // Python 3.5-3.10 (3.11+ 中被 BINARY_OP 替代)
    RAISE_VARARGS = 130,
    RERAISE = 119,         // all versions (3.5-3.10 and 3.11+ share value 119)
    PUSH_EXC_INFO = 138,   // 3.5-3.10 (3.12+ changed to 35)
    JUMP_IF_NOT_EXC_MATCH = 121, // Python 3.8-3.10 (3.11+ 中被 RETURN_CONST 替代)
    SETUP_WITH = 143,      // Python 3.5-3.10 (3.11+ 中被 LOAD_FAST_AND_CLEAR 替代)
    BEFORE_WITH = 153,     // Python 3.7-3.10 (3.12+ 中改为 53)
    WITH_EXCEPT_START = 154, // Python 3.7-3.10 (3.12+ 中改为 49)

    // --- 函数/类 ---
    LOAD_BUILD_CLASS = 71,
    MAKE_FUNCTION = 132,
    MAKE_CLOSURE = 134,    // 闭包函数：与MAKE_FUNCTION同但多弹出closure tuple

    // --- 特殊 ---
    EXTENDED_ARG = 144,   // 扩展参数

    // ==================== Python 3.11+ 操作码 ====================
    // 注：以下操作码值与 3.10 及更早版本有不同的语义。
    // 映射由 MapOpcodePy311/312 函数处理。

    PUSH_NULL = 2,           // 3.11+: push null to stack (call protocol)
    INTERPRETER_EXIT = 3,    // 3.12+: like RETURN_VALUE for None

    SWAP = 99,               // 3.11+: swap TOS and TOS1
    COPY = 120,              // 3.11+: duplicate TOS (not to be confused with COPY_FREE_VARS=149)
    // 注：以下 3.11+ 操作码与 3.10 版本值不同，使用 190+ 范围避免 byte 冲突
    RETURN_CONST = 190,      // 3.11+: LOAD_CONST + RETURN_VALUE (raw byte 121)
    BINARY_OP = 191,         // 3.11+: binary operation, arg selects op (raw byte 122)
    LOAD_FAST_AND_CLEAR = 192, // 3.11+: load + clear (raw byte 143)
    LOAD_FAST_CHECK = 193,   // 3.11+: load fast with unbound check (raw byte 127)
    POP_JUMP_IF_NOT_NONE = 194, // 3.11+ (raw byte 128)
    POP_JUMP_IF_NONE = 195,     // 3.11+ (raw byte 129)
    SEND = 123,              // 3.11+ already matches

    JUMP_BACKWARD_NO_INTERRUPT = 134, // 3.11+ (之前的 141 是错误的)

    // 闭包/自由变量 (3.11+)
    MAKE_CELL = 135,         // 3.11+: make cell
    LOAD_CLOSURE = 136,      // 3.11+: load closure cell
    LOAD_DEREF = 137,        // 3.11+: load deref cell
    STORE_DEREF = 138,       // 3.11+: store to deref cell
    DELETE_DEREF = 139,      // 3.11+: delete deref cell

    LOAD_SUPER_ATTR = 141,   // 3.11+: super attribute
    CALL_FUNCTION_EX = 142,  // 3.5-3.12: call with *args/**kwargs
    
    COPY_FREE_VARS = 149,    // 3.11+: copy free vars to closure
    RESUME = 151,            // 3.11+: resume at start of function/loop

    // 3.8+ function call expressions
    DICT_MERGE = 164,      // 3.8+: merge dict for **kwargs

    // 3.12: keyed/built operations
    BUILD_CONST_KEY_MAP = 156, // 3.12+
    LIST_EXTEND = 162,       // 3.12+: list extend inline
    SET_UPDATE = 163,        // 3.12+: set update inline
    DICT_UPDATE = 165,       // 3.12+: dict update inline

    // 3.11-specific (removed in 3.12)
    PRECALL_311 = 166,       // 3.11 only: prepare call
    CALL_311 = 167,          // 3.11 only: call function

    // 3.12+ call/name operations
    CALL = 171,              // 3.12+: call (replaces CALL_FUNCTION=131, CALL_311=167)
    KW_NAMES = 172,          // 3.11+: keyword names referenced by CALL
    CALL_INTRINSIC_1 = 173,  // 3.12+: intrinsic call type 1
    CALL_INTRINSIC_2 = 174,  // 3.12+: intrinsic call type 2
    LOAD_FROM_DICT_OR_GLOBALS = 175, // 3.12+
    LOAD_FROM_DICT_OR_DEREF = 176,   // 3.12+

    // 3.12+ exception/with renumbered
    PUSH_EXC_HANDLER_312 = 177, // 3.12+: push exception handler (raw byte 34)
    PULL_EXC_FROM_INFO_312 = 178, // 3.12+: pull exception info (raw byte 20)
    PUSH_EXC_INFO_312 = 179,   // 3.12+ (was 138 in 3.5-3.10, raw byte 35)
    CHECK_EXC_MATCH = 197,     // 3.12+ (raw byte 36)
    CHECK_EG_MATCH = 198,      // 3.12+ (raw byte 37)
    // 3.10+ match/case opcodes
    MATCH_MAPPING_312 = 180,   // 3.12+ (raw byte 31)
    MATCH_SEQUENCE_312 = 181,  // 3.12+ (raw byte 32)
    MATCH_KEYS_312 = 182,      // 3.12+ (raw byte 33)
    MATCH_CLASS_312 = 183,     // 3.12+ (raw byte 152)
    BEFORE_WITH_312 = 199,     // 3.12+ (was 153 in 3.7-3.10, raw byte 53)
    WITH_EXCEPT_START_312 = 188, // 3.12+ (was 154 in 3.7-3.10, raw byte 49)

    // ==================== Python 3.13+ 操作码 ====================
    // 3.13 重新编号了几乎所有操作码，以下别名对应 3.13 的原始字节值。
    BEFORE_ASYNC_WITH_313 = 212,   // 3.13+ (raw byte 1)
    TO_BOOL_313 = 213,             // 3.13+ (raw byte 40)
    CALL_INTRINSIC_1_313 = 214,    // 3.13+ (raw byte 55)
    CALL_INTRINSIC_2_313 = 215,    // 3.13+ (raw byte 56)
    CALL_KW_313 = 216,             // 3.13+ (raw byte 57)
    ENTER_EXECUTOR_313 = 217,      // 3.13+ (raw byte 70)
    LOAD_FAST_LOAD_FAST_313 = 218, // 3.13+ (raw byte 88)
    MAKE_CELL_313 = 219,           // 3.13+ (raw byte 94, 3.11 的 MAKE_CELL=135)
    SET_FUNCTION_ATTRIBUTE_313 = 220, // 3.13+ (raw byte 106)
    STORE_FAST_LOAD_FAST_313 = 221,// 3.13+ (raw byte 111)
    STORE_FAST_STORE_FAST_313 = 222, // 3.13+ (raw byte 112)
    RESUME_313 = 223,              // 3.13+ (raw byte 149, 3.12=151)
    YIELD_VALUE_313 = 224,         // 3.13+ (raw byte 118)
    BEFORE_WITH_313 = 225,         // 3.13+ (raw byte 2)
    CONVERT_VALUE_313 = 226,       // 3.13+ (raw byte 60)
    COPY_FREE_VARS_313 = 227,      // 3.13+ (raw byte 62, was 149 in 3.11-3.12)
    RETURN_CONST_313 = 228,        // 3.13+ (raw byte 103)
    // 以下 3.13 映射所需别名（不常用的操作码）
    LOAD_LOCALS_313 = 229,
    MATCH_KEYS_313 = 230,
    MATCH_MAPPING_313 = 231,
    MATCH_SEQUENCE_313 = 232,
    RETURN_GENERATOR_313 = 233,
    STORE_SLICE_313 = 234,
    GET_AWAITABLE_313 = 235,
    LIST_APPEND_313 = 236,
    MAP_ADD_313 = 237,
    MATCH_CLASS_313 = 238,
    SET_ADD_313 = 239,
    // 余下 3.13 映射所用别名
    BINARY_SLICE_313 = 240,
    CLEANUP_THROW_313 = 241,
    DELETE_SUBSCR_313 = 242,
    END_ASYNC_FOR_313 = 243,
    END_FOR_313 = 244,
    END_SEND_313 = 245,
    EXIT_INIT_CHECK_313 = 246,
    FORMAT_SIMPLE_313 = 247,
    FORMAT_WITH_SPEC_313 = 248,
    GET_AITER_313 = 249,
    GET_ANEXT_313 = 250,
    GET_LEN_313 = 251,
    LOAD_ASSERTION_ERROR_313 = 252,
    RESERVED_313 = 253,

    // ==================== Python 3.14 新增操作码 ====================
    // 3.14 操作码体系与 3.13 完全不同（HAVE_ARGUMENT=43, 新增/移动了多个操作码）。
    // 以下条目仅用于 MapOpcodePy314 映射，原始字节值见方法注释。
    LOAD_SMALL_INT_314 = 254,         // 3.14 raw=94: 加载小整数（取代 LOAD_CONST+小int）
    LOAD_FAST_BORROW_314 = 255,       // 3.14 raw=86: borrow-load local（不增加引用计数）
    LOAD_FAST_BORROW_LOAD_FAST_BORROW_314 = 256, // 3.14 raw=87: 双 borrow-load
    NOT_TAKEN_314 = 257,              // 3.14 raw=28: 紧随条件跳转后的标记（提示 JIT 该分支未执行）
    POP_ITER_314 = 258,              // 3.14 raw=30: pop iterator after for-loop
    LOAD_COMMON_CONSTANT_314 = 259,  // 3.14 raw=81: 加载常见常量（None/True/False/Ellipsis）
    BUILD_INTERPOLATION_314 = 260,   // 3.14 raw=45: build interpolation for f-string
    BINARY_OP_INPLACE_ADD_UNICODE_314 = 261, // 3.14 raw=3
    LOAD_SPECIAL_314 = 262,          // 3.14 raw=95
}
