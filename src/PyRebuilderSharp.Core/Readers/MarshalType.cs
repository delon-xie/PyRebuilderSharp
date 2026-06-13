namespace PyRebuilderSharp.Core.Readers;

/// <summary>
/// Python Marshal格式的类型常量。
/// 对应CPython的marshal.c中的类型定义。
/// </summary>
internal static class MarshalType
{
    public const byte TYPE_NONE = 78;           // 'N'
    public const byte TYPE_INT = 105;            // 'i'
    public const byte TYPE_LONG = 108;           // 'l'
    public const byte TYPE_FLOAT = 102;           // 'f'
    public const byte TYPE_BINARY_FLOAT = 103;    // 'g'
    public const byte TYPE_COMPLEX = 120;        // 'x'
    public const byte TYPE_STRING = 115;         // 's'
    public const byte TYPE_SHORT_ASCII = 122;    // 'z'
    public const byte TYPE_SHORT_ASCII_INTERNED = 90;    // 'Z'
    public const byte TYPE_ASCII = 116;          // 't'
    public const byte TYPE_UNICODE = 117;        // 'u'
    public const byte TYPE_ASCII_INTERNED = 65;  // 'A'
    public const byte TYPE_TUPLE = 40;           // '('
    public const byte TYPE_SMALL_TUPLE = 41;     // ')'
    public const byte TYPE_LIST = 91;            // '['
    public const byte TYPE_DICT = 123;           // '{'
    public const byte TYPE_SET = 60;             // '<'
    public const byte TYPE_FROZENSET = 62;       // '>'
    public const byte TYPE_CODE = 99;            // 'c'
    public const byte TYPE_CODE_SIMPLE = 115;   // 's' (Python 3.11+ only — conflicts with TYPE_STRING in older versions)
    public const byte TYPE_REF = 114;            // 'r'
    public const byte TYPE_REF_FLAG = 82;        // 'R'
    public const byte TYPE_BINARY_COMPLEX = 121;  // 'y'
    public const byte TYPE_FALSE = 70;           // 'F'
    public const byte TYPE_TRUE = 84;            // 'T'
    public const byte TYPE_ELLIPSIS = 46;        // '.'
    public const byte TYPE_STOPITERATION = 63;   // '?'
    public const byte TYPE_UNKNOWN = 33;         // '!'
    public const byte TYPE_INTERNAL_REF = 73;    // 'I'
    public const byte TYPE_INTERNAL_STR_REF = 74; // 'J'

    /// <summary>
    /// Flag bit for reference tracking in marshal format (Python 3.4+).
    /// ORed with type codes to indicate the object is stored in the reference list.
    /// </summary>
    public const byte TYPE_FLAG_REF = 0x80;

    public static bool IsNumericType(byte type) => type switch
    {
        TYPE_INT or TYPE_LONG or TYPE_FLOAT or TYPE_COMPLEX => true,
        _ => false
    };

    public static bool IsStringType(byte type) => type switch
    {
        TYPE_STRING or TYPE_SHORT_ASCII or TYPE_SHORT_ASCII_INTERNED
            or TYPE_ASCII or TYPE_UNICODE or TYPE_ASCII_INTERNED => true,
        _ => false
    };

    public static bool IsContainerType(byte type) => type switch
    {
        TYPE_TUPLE or TYPE_SMALL_TUPLE or TYPE_LIST
            or TYPE_DICT or TYPE_SET or TYPE_FROZENSET => true,
        _ => false
    };
}
