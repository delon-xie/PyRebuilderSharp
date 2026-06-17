namespace PyRebuilderSharp.Core.Readers;

/// <summary>
/// Python Marshal格式的类型常量。
/// 对应CPython的marshal.c中的类型定义。
/// 全部常量值已与 CPython v2.7.18-v3.14.3 的 marshal.c 逐版本交叉验证。
/// </summary>
internal static class MarshalType
{
    // --- 基础类型 ---
    public const byte TYPE_NONE = 78;           // 'N'
    public const byte TYPE_INT = 105;            // 'i'
    public const byte TYPE_LONG = 108;           // 'l'
    public const byte TYPE_INT64 = 73;           // 'I' (Python 2.7, 3.6+)
    public const byte TYPE_FLOAT = 102;          // 'f'
    public const byte TYPE_BINARY_FLOAT = 103;   // 'g'
    public const byte TYPE_COMPLEX = 120;        // 'x'
    public const byte TYPE_BINARY_COMPLEX = 121; // 'y'

    // --- 字符串类型 ---
    public const byte TYPE_STRING = 115;         // 's' — bytes对象 (Python 2遗留命名)
    public const byte TYPE_BYTES = 124;          // '|' (Python 3+)
    public const byte TYPE_SHORT_ASCII = 122;    // 'z' — 短ASCII (1字节长度)
    public const byte TYPE_SHORT_ASCII_INTERNED = 90; // 'Z'
    public const byte TYPE_ASCII = 97;           // 'a' — 长ASCII (4字节长度)
    public const byte TYPE_ASCII_INTERNED = 65;  // 'A' (注意: 不是 116/'t'!)
    public const byte TYPE_UNICODE = 117;        // 'u' — UTF-8编码
    public const byte TYPE_INTERNED = 116;       // 't' — UTF-8编码, interned (v3.4+)
    public const byte TYPE_STRINGREF = 82;       // 'R' — Python 2.7 interned string ref

    // --- 容器类型 ---  
    public const byte TYPE_TUPLE = 40;           // '('
    public const byte TYPE_SMALL_TUPLE = 41;     // ')' (v4+)
    public const byte TYPE_LIST = 91;            // '['
    public const byte TYPE_DICT = 123;           // '{'
    public const byte TYPE_SET = 60;             // '<'
    public const byte TYPE_FROZENSET = 62;       // '>'

    // --- 特殊对象 ---
    public const byte TYPE_CODE = 99;            // 'c'
    public const byte TYPE_REF = 114;            // 'r'
    public const byte TYPE_TRUE = 84;            // 'T'
    public const byte TYPE_FALSE = 70;           // 'F'
    public const byte TYPE_ELLIPSIS = 46;        // '.'
    public const byte TYPE_NULL = 48;            // '0'
    public const byte TYPE_STOPITER = 83;        // 'S'
    public const byte TYPE_UNKNOWN = 63;         // '?' (注意: 不是 33/'!'!)
    public const byte TYPE_SLICE = 58;           // ':' (Python 3.14+)

    // --- 非标准/内部类型 ---
    public const byte TYPE_CODE_SIMPLE = 115;    // 's' — 与 TYPE_STRING 冲突, 仅用于 Python 3.11+ 的 isSimple 参数

    /// <summary>
    /// Flag bit for reference tracking in marshal format (Python 3.4+).
    /// ORed with type codes to indicate the object is stored in the reference list.
    /// </summary>
    public const byte TYPE_FLAG_REF = 0x80;

    public static bool IsNumericType(byte type) => type switch
    {
        TYPE_INT or TYPE_LONG or TYPE_INT64 or TYPE_FLOAT or TYPE_COMPLEX => true,
        _ => false
    };

    public static bool IsStringType(byte type) => type switch
    {
        TYPE_STRING or TYPE_SHORT_ASCII or TYPE_SHORT_ASCII_INTERNED
            or TYPE_ASCII or TYPE_UNICODE or TYPE_ASCII_INTERNED
            or TYPE_INTERNED or TYPE_STRINGREF => true,
        _ => false
    };

    public static bool IsContainerType(byte type) => type switch
    {
        TYPE_TUPLE or TYPE_SMALL_TUPLE or TYPE_LIST
            or TYPE_DICT or TYPE_SET or TYPE_FROZENSET => true,
        _ => false
    };
}
