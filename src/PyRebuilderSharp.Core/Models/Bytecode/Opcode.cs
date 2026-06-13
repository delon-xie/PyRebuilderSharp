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
public enum Opcode : byte
{
    // --- 栈操作 (0-99) ---
    POP_TOP = 1,
    ROT_TWO = 2,
    ROT_THREE = 3,
    DUP_TOP = 4,
    DUP_TOP_TWO = 5,
    NOP = 9,

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
    BUILD_STRING = 155,

    // --- 导入 (108-109) ---
    IMPORT_NAME = 108,
    IMPORT_FROM = 109,
    IMPORT_STAR = 84,

    // --- 其他 ---
    RESUME = 151,

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
    JUMP_BACKWARD_NO_INTERRUPT = 141,

    // 旧名称别名（兼容，值正确）
    POP_JUMP_IF_TRUE_PY38 = JUMP_IF_FALSE_OR_POP,   // 旧名，实际是 JUMP_IF_FALSE_OR_POP
    POP_JUMP_IF_FALSE_PY38 = JUMP_IF_TRUE_OR_POP,   // 旧名，实际是 JUMP_IF_TRUE_OR_POP

    // --- 循环 ---
    GET_ITER = 68,
    GET_YIELD_FROM_ITER = 69,  // Python 3.5+: yield from 迭代器包装
    FOR_ITER = 93,

    // --- 调用 ---
    CALL_FUNCTION = 131,
    CALL_FUNCTION_KW = 141,
    CALL_FUNCTION_EX = 142,
    LOAD_METHOD = 160,      // Python 3.7-3.9 method call optimization
    CALL_METHOD = 161,      // Python 3.7-3.9 method call optimization
    PRECALL = 156,
    CALL = 162,

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
    SEND = 123,

    // --- Yield from ---
    YIELD_FROM = 87,        // Python 3.5-3.9: yield from (87)
    YIELD_FROM_PY310 = 72,  // Python 3.10: yield from 重编号为 72

    // --- 异常 ---
    SETUP_ANNOTATIONS = 85,
    END_FINALLY = 88,
    POP_EXCEPT = 89,
    SETUP_EXCEPT = 121,    // Python 3.5-3.7 (3.8+ 中被 JUMP_IF_NOT_EXC_MATCH 替代)
    SETUP_FINALLY = 122,
    RAISE_VARARGS = 130,
    RERAISE = 119,
    PUSH_EXC_INFO = 138,
    JUMP_IF_NOT_EXC_MATCH = 121, // Python 3.8+ 替代 SETUP_EXCEPT
    SETUP_WITH = 143,
    BEFORE_WITH = 153,
    WITH_EXCEPT_START = 154,

    // --- 函数/类 ---
    LOAD_BUILD_CLASS = 71,
    MAKE_FUNCTION = 132,
    MAKE_CLOSURE = 134,    // 闭包函数：与MAKE_FUNCTION同但多弹出closure tuple

    // --- 特殊 ---
    EXTENDED_ARG = 144,   // 扩展参数

    // --- Python 3.11+ ---
    PRECALL_NEW = 156,
    CALL_NEW = 162,
    PUSH_NULL = 2,
}
