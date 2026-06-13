using System.Text;
using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Readers;

/// <summary>
/// .pyc文件读取器。
/// 负责解析Python编译后的字节码文件。
/// </summary>
public class PycReader
{
    // Python各版本的Magic Number
    private static readonly Dictionary<byte[], string> KnownMagics = new()
    {
        { new byte[] { 0x03, 0xF3, 0x0D, 0x0A }, "Python 2.7" },
        { new byte[] { 0x17, 0x0D, 0x0D, 0x0A }, "Python 3.5" },
        { new byte[] { 0x33, 0x0D, 0x0D, 0x0A }, "Python 3.6" },
        { new byte[] { 0x42, 0x0D, 0x0D, 0x0A }, "Python 3.7" },
        { new byte[] { 0x55, 0x0D, 0x0D, 0x0A }, "Python 3.8" },
        { new byte[] { 0x61, 0x0D, 0x0D, 0x0A }, "Python 3.9" },
        { new byte[] { 0x6F, 0x0D, 0x0D, 0x0A }, "Python 3.10" },
        { new byte[] { 0xA0, 0x0D, 0x0D, 0x0A }, "Python 3.11" },
        { new byte[] { 0xA7, 0x0D, 0x0D, 0x0A }, "Python 3.11+" },
        { new byte[] { 0xCB, 0x0D, 0x0D, 0x0A }, "Python 3.12" },
        { new byte[] { 0xE7, 0x0D, 0x0D, 0x0A }, "Python 3.13" },
        { new byte[] { 0xF3, 0x0D, 0x0D, 0x0A }, "Python 3.14" },
    };

    private readonly List<object?> _refList = new();
    private readonly List<string> _internedStrings27 = new(); // Python 2.7 interned string table
    private string _pythonVersion = "Python 3.8";
    private byte[] _magicBytes = Array.Empty<byte>();

    /// <summary>
    /// 检查是否为 Python 2.7
    /// </summary>
    private bool IsPython27()
        => _magicBytes.Length >= 2 && _magicBytes[0] == 0x03 && _magicBytes[1] == 0xF3;

    /// <summary>
    /// 检查是否为 Python 3.10+（使用 word 偏移）
    /// </summary>
    private bool IsWordOffsetVersion()
        => _magicBytes.Length >= 2 && _magicBytes[0] >= 0x6F && _magicBytes[1] == 0x0D;

    /// <summary>
    /// 检查是否为 Python 3.8+（有 posOnlyArgCount）
    /// </summary>
    private bool IsPython38Plus()
        => _magicBytes.Length >= 2 && _magicBytes[0] >= 0x55 && _magicBytes[1] == 0x0D;

    /// <summary>
    /// 检查是否为 Python 3.2-3.6（12字节 header，无 flags 字段）
    /// Python 3.7+ 使用 PEP 552 的 16字节 header（含 flags）
    /// </summary>
    private bool IsPrePython37()
        => !IsPython27() && _magicBytes.Length >= 2 && _magicBytes[0] < 0x42 && _magicBytes[1] == 0x0D;

    /// <summary>
    /// 读取.pyc文件并解析为CodeObject。
    /// </summary>
    public CodeObject Read(byte[] data)
    {
        using var ms = new MemoryStream(data);
        using var br = new BinaryReader(ms);

        // Step 1: 验证Magic Number
        var magic = br.ReadBytes(4);
        _magicBytes = magic;
        var versionInfo = ValidateMagic(magic);
        _pythonVersion = versionInfo;

        // Step 2: 读取头部信息
        if (IsPython27())
        {
            // Python 2.7 header: magic(4) + timestamp(4) = 8 bytes, no flags/size
            var ts = br.ReadInt32(); // timestamp (unused)
            // 2.7 marshal data starts at offset 8
        }
        else if (IsPrePython37())
        {
            // Python 3.2-3.6 header: magic(4) + timestamp(4) + source_size(4) = 12 bytes (no flags)
            // PEP 552 (hash-based .pyc) was introduced in Python 3.7
            var timestamp = br.ReadInt32();
            var sourceSize = br.ReadInt32();
        }
        else
        {
            // Python 3.7+ header: magic(4) + flags(4) + timestamp(4) + source_size(4) = 16 bytes
            var flags = br.ReadInt32();
            var timestamp = br.ReadInt32();
            var size = br.ReadInt32();
        }

        // Step 3: 读取Marshal数据 — use ReadMarshalObject which handles FLAG_REF
        return (CodeObject?)ReadMarshalObject(br);
    }

    /// <summary>
    /// 验证Python Magic Number。
    /// </summary>
    private string ValidateMagic(byte[] magic)
    {
        foreach (var kvp in KnownMagics)
        {
            if (magic.SequenceEqual(kvp.Key))
                return kvp.Value;
        }
        throw new UnsupportedPythonVersionException(
            $"Unknown magic number: {BitConverter.ToString(magic)}");
    }

    /// <summary>
    /// 读取Marshal格式的CodeObject。
    /// </summary>
    private CodeObject ReadMarshalCodeObject(BinaryReader br, bool isSimple = false)
    {
        var code = new CodeObject();
        var startPos = br.BaseStream.Position;

        // 设置版本信息
        code.IsPython38Plus = IsPython38Plus();

        try
        {
            if (IsPython27())
                return ReadMarshalCodeObject27(br);

            // 读取CodeObject的各个字段
            code.ArgCount = br.ReadInt32();
            if (IsPython38Plus() && !isSimple)
            {
                // Python 3.8+: argcount, posonlyargcount, kwonlyargcount, nlocals, stacksize, flags
                var posOnlyArgCount = br.ReadInt32();
                code.KwOnlyArgCount = br.ReadInt32();
                var nlocals = br.ReadInt32();
                var stacksize = br.ReadInt32();
                var flags = br.ReadInt32();
                code.IsGenerator = (flags & 0x20) != 0;
                code.IsCoroutine = (flags & 0x80) != 0;
                code.IsAsyncGenerator = (flags & 0xC0) == 0xC0;
            }
            else if (isSimple)
            {
                // TYPE_CODE_SIMPLE: argcount, nlocals, stacksize, flags
                // （无 posonlyargcount/kwonlyargcount，即使 3.11+ 也是如此）
                var nlocals = br.ReadInt32();
                var stacksize = br.ReadInt32();
                var flags = br.ReadInt32();
                code.KwOnlyArgCount = 0;
                code.IsGenerator = (flags & 0x20) != 0;
                code.IsCoroutine = (flags & 0x80) != 0;
                code.IsAsyncGenerator = (flags & 0xC0) == 0xC0;
            }
            else
            {
                // Python 3.5-3.7: argcount, kwonlyargcount, nlocals, stacksize, flags
                code.KwOnlyArgCount = br.ReadInt32();
                var nlocals = br.ReadInt32();
                var stacksize = br.ReadInt32();
                var flags = br.ReadInt32();
                code.IsGenerator = (flags & 0x20) != 0;
                code.IsCoroutine = false;
                code.IsAsyncGenerator = false;
            }

            // 读取字节码 — 通过 ReadMarshalObject 以正确处理 FLAG_REF
            var bytecodeObj = ReadMarshalObject(br);
            byte[]? bcBytes = bytecodeObj as byte[];
            if (bcBytes != null)
                code.Instructions = ParseInstructions(bcBytes);

            code.Constants = ReadMarshalDictSafe(br, code);

            // names/varnames/freevars/cellvars — 通过 ReadMarshalObject 以正确处理 FLAG_REF
            code.Names = ReadMarshalObjectAsStrList(br);
            code.Varnames = ReadMarshalObjectAsStrList(br);
            code.Freevars = ReadMarshalObjectAsStrList(br);
            code.Cellvars = ReadMarshalObjectAsStrList(br);

            // filename/name — 通过 ReadMarshalObject 以正确处理 FLAG_REF
            var filenameObj = ReadMarshalObject(br);
            code.Filename = filenameObj?.ToString() ?? "<unknown>";
            var nameObj = ReadMarshalObject(br);
            code.Name = nameObj?.ToString() ?? "<module>";

            // Python 3.11+: 读取 qualname（仅 TYPE_CODE，非 TYPE_CODE_SIMPLE）
            if (IsPython311Plus() && !isSimple)
            {
                try { var _ = ReadMarshalObject(br); } catch { }
            }

            // first line number (int32) — 3.8+ 的字段
            try { code.FirstLineNumber = br.ReadInt32(); } catch { }

            // lnotab — 通过 ReadMarshalObject 以正确处理 FLAG_REF
            var lnotabObj = ReadMarshalObject(br);
            byte[]? lnotab = lnotabObj as byte[];
            if (lnotab != null)
                code.LineNumberTable = ParseLineNumberTable(lnotab, code.Instructions);

            // Python 3.11+: 读取 co_exceptiontable（仅 TYPE_CODE，非 TYPE_CODE_SIMPLE）
            if (IsPython311Plus() && !isSimple && br.BaseStream.Position < br.BaseStream.Length)
            {
                try
                {
                    var excTblObj = ReadMarshalObject(br);
                    if (excTblObj is byte[] excBytes && excBytes.Length > 0)
                        code.ExceptionTable = ParseExceptionTable(excBytes);
                }
                catch { }
            }
        }
        catch (EndOfStreamException)
        {
        }

        return code;
    }

    /// <summary>
    /// Python 2.7 CodeObject 读取。
    /// 字段顺序：argcount, nlocals, stacksize, flags
    /// （无 posOnlyArgCount/kwOnlyArgCount）
    /// </summary>
    private CodeObject ReadMarshalCodeObject27(BinaryReader br)
    {
        var code = new CodeObject();
        try
        {
            code.ArgCount = br.ReadInt32();
            code.KwOnlyArgCount = 0;
            var nlocals = br.ReadInt32();
            var stacksize = br.ReadInt32();
            var flags = br.ReadInt32();

            code.IsGenerator = (flags & 0x20) != 0;
            code.IsCoroutine = false;
            code.IsAsyncGenerator = false;

            // 读取字节码 — 通过 ReadMarshalObject 以正确处理 FLAG_REF
            var bytecodeObj = ReadMarshalObject(br);
            byte[]? bcBytes = bytecodeObj as byte[];
            if (bcBytes != null)
                code.Instructions = ParseInstructions(bcBytes);

            code.Constants = ReadMarshalDictSafe(br, code);

            code.Names = ReadMarshalListSafe27(br)?.Select(x => x?.ToString() ?? "").ToList() ?? new();
            code.Varnames = ReadMarshalListSafe27(br)?.Select(x => x?.ToString() ?? "").ToList() ?? new();
            code.Freevars = ReadMarshalListSafe27(br)?.Select(x => x?.ToString() ?? "").ToList() ?? new();
            code.Cellvars = ReadMarshalListSafe27(br)?.Select(x => x?.ToString() ?? "").ToList() ?? new();

            code.Filename = ReadMarshalString27(br) ?? "<unknown>";
            code.Name = ReadMarshalString27(br) ?? "<module>";

            // Python 2.7 有 firstlineno
            try { code.FirstLineNumber = br.ReadInt32(); } catch { }

            var lnotab = ReadMarshalBytesSafe(br);
            if (lnotab != null)
                code.LineNumberTable = ParseLineNumberTable(lnotab, code.Instructions);
        }
        catch (EndOfStreamException) { }
        return code;
    }

    /// <summary>
    /// Python 2.7 安全的 Marshal 列表读取。
    /// 在 2.7 中，names/varnames/freevars/cellvars 是 tuple。
    /// 同时收集 interned string 用于 TYPE_STRINGREF 解析。
    /// </summary>
    private List<object?>? ReadMarshalListSafe27(BinaryReader br)
    {
        if (br.BaseStream.Position >= br.BaseStream.Length)
            return null;
        try
        {
            var rawType = br.ReadByte();
            var type = rawType; // 2.7 不使用 FLAG_REF

            if (type == MarshalType.TYPE_REF) // 2.7 TYPE_STRINGREF = 0x7a, but for lists handle TYPE_REF
            {
                var refIdx = br.ReadInt32();
                if (refIdx >= 0 && refIdx < _refList.Count && _refList[refIdx] is List<object?> refList)
                    return refList;
                return new List<object?>();
            }

            // 只接受 tuple 类型
            if (type != MarshalType.TYPE_TUPLE && type != MarshalType.TYPE_SMALL_TUPLE)
                return new List<object?>();

            int count = type == MarshalType.TYPE_SMALL_TUPLE ? br.ReadByte() : br.ReadInt32();
            var items = new List<object?>();
            for (int i = 0; i < count; i++)
            {
                items.Add(ReadMarshalValue27(br));
            }
            return items;
        }
        catch { return null; }
    }

    /// <summary>
    /// Python 2.7 marshal 值读取 — 处理 TYPE_INTERNED(0x74) 和 TYPE_STRINGREF(0x7a)。
    /// </summary>
    private object? ReadMarshalValue27(BinaryReader br)
    {
        var type = br.ReadByte();
        return type switch
        {
            78 => null,             // 'N' TYPE_NONE
            105 => br.ReadInt32(),  // 'i' TYPE_INT
            84 => true,             // 'T' TYPE_TRUE
            70 => false,            // 'F' TYPE_FALSE
            115 or 116 => ReadMarshalString27FromType(br, type), // 's' TYPE_STRING, 't' TYPE_INTERNED
            122 => ReadStringRef27(br), // 'z' TYPE_STRINGREF
            40 or 41 => ReadMarshalList27(br, type), // '(' TYPE_TUPLE, ')' TYPE_SMALL_TUPLE
            46 => new object(),     // '.' TYPE_ELLIPSIS
            _ => SkipUnknown27(br, type),
        };
    }

    private string ReadMarshalString27(BinaryReader br)
    {
        var type = br.ReadByte();
        return ReadMarshalString27FromType(br, type);
    }

    private string ReadMarshalString27FromType(BinaryReader br, byte type)
    {
        if (type == 115) // 's' TYPE_STRING — raw bytes
        {
            var len = br.ReadInt32();
            var bytes = br.ReadBytes(len);
            return System.Text.Encoding.UTF8.GetString(bytes);
        }
        if (type == 116) // 't' TYPE_INTERNED — interned string
        {
            var len = br.ReadInt32();
            var bytes = br.ReadBytes(len);
            var str = System.Text.Encoding.UTF8.GetString(bytes);
            _internedStrings27.Add(str);
            return str;
        }
        if (type == 122) // 'z' TYPE_STRINGREF
        {
            return ReadStringRef27(br);
        }
        return "";
    }

    /// <summary>
    /// Python 2.7 TYPE_STRINGREF (0x7a) — 引用之前出现过的 interned string。
    /// </summary>
    private string ReadStringRef27(BinaryReader br)
    {
        var idx = br.ReadInt32();
        if (idx >= 0 && idx < _internedStrings27.Count)
            return _internedStrings27[idx];
        return $"strref_{idx}";
    }

    private List<object?> ReadMarshalList27(BinaryReader br, byte type)
    {
        int count = type == 41 ? br.ReadByte() : br.ReadInt32(); // ')' SMALL_TUPLE
        var items = new List<object?>();
        for (int i = 0; i < count; i++)
            items.Add(ReadMarshalValue27(br));
        return items;
    }

    private object? SkipUnknown27(BinaryReader br, byte type)
    {
        try
        {
            if (br.BaseStream.Position < br.BaseStream.Length)
            {
                // Try to skip: assume 4-byte length prefix
                var skipped = br.ReadBytes(Math.Min(4, (int)(br.BaseStream.Length - br.BaseStream.Position)));
            }
        }
        catch { }
        return null;
    }

    /// <summary>
    /// 安全的 Marshal Bytes 读取。
    /// </summary>
    private byte[]? ReadMarshalBytesSafe(BinaryReader br)
    {
        if (br.BaseStream.Position >= br.BaseStream.Length)
            return null;
        try { return ReadMarshalBytes(br); }
        catch { return null; }
    }

    /// <summary>
    /// 安全的 Marshal Dict 读取 — 同时提取子代码对象到 ChildCodes
    /// </summary>
    private Dictionary<int, object?> ReadMarshalDictSafe(BinaryReader br, CodeObject parentCode = null)
    {
        if (br.BaseStream.Position >= br.BaseStream.Length)
            return new();
        try 
        { 
            var startPos = br.BaseStream.Position;
            var dict = ReadMarshalDict(br);
            // 提取常量中的 CodeObject 到 ChildCodes 列表
            if (parentCode != null)
            {
                foreach (var kvp in dict)
                {
                    if (kvp.Value is CodeObject childCode)
                        parentCode.ChildCodes.Add(childCode);
                }
            }
            return dict;
        }
        catch (Exception ex) 
        { 
            System.Console.Error.WriteLine($"WARNING: Constants read failed at pos {br.BaseStream.Position}: {ex.Message}");
            return new(); 
        }
    }

    /// <summary>
    /// 安全的 Marshal List 读取。
    /// </summary>
    private List<object?>? ReadMarshalListSafe(BinaryReader br)
    {
        if (br.BaseStream.Position >= br.BaseStream.Length)
            return null;
        try { return ReadMarshalList(br); }
        catch { return null; }
    }

    /// <summary>
    /// 安全的 Marshal String 读取。
    /// </summary>
    private string? ReadMarshalStringSafe(BinaryReader br)
    {
        if (br.BaseStream.Position >= br.BaseStream.Length)
            return null;
        try { return ReadMarshalString(br); }
        catch { return null; }
    }

    /// <summary>
    /// 解析字节码为指令列表。
    /// Python 2.7/3.5: 可变长度格式（无参指令1字节，有参【>=90】指令3字节）
    /// Python 3.6-3.10: 2字节 wordcode [opcode, arg]
    /// Python 3.11+: 2字节 wordcode + CACHE 条目
    /// EXTENDED_ARG 链式组合参数。
    /// </summary>
    private List<Instruction> ParseInstructions(byte[] bytecode)
    {
        if (IsPython27())
            return ParseInstructionsPre36(bytecode);
        if (IsPython311Plus())
            return ParseInstructions311Plus(bytecode);
        // Python 3.5: pre-wordcode format
        if (_magicBytes.Length >= 2 && _magicBytes[0] < 0x33)
            return ParseInstructionsPre36(bytecode);
        // Python 3.6-3.10: wordcode (2 bytes per instruction)
        return ParseInstructionsWordcode(bytecode);
    }

    /// <summary>
    /// 解析 Python 2.7/3.5 字节码（可变长度格式）。
    /// opcode < 90 (HAVE_ARGUMENT): 1 字节
    /// opcode >= 90: 1 字节 opcode + 2 字节 arg（小端） = 3 字节
    /// </summary>
    private List<Instruction> ParseInstructionsPre36(byte[] bytecode)
    {
        var instructions = new List<Instruction>();
        int offset = 0;
        int extArg = 0;

        while (offset < bytecode.Length)
        {
            var op = (Models.Bytecode.Opcode)bytecode[offset];
            offset += 1;

            // Handle EXTENDED_ARG chain
            if (op == Models.Bytecode.Opcode.EXTENDED_ARG)
            {
                // In pre-3.6 format, EXTENDED_ARG has a 2-byte arg (little-endian)
                if (offset + 2 <= bytecode.Length)
                {
                    var argLow = bytecode[offset];
                    var argHigh = bytecode[offset + 1];
                    extArg = (extArg << 16) | (argHigh << 8) | argLow;
                    offset += 2;
                }
                continue;
            }

            int? arg = null;
            if ((byte)op >= 90) // HAVE_ARGUMENT
            {
                if (offset + 2 <= bytecode.Length)
                {
                    var argLow = bytecode[offset];
                    var argHigh = bytecode[offset + 1];
                    arg = (extArg << 16) | (argHigh << 8) | argLow;
                    offset += 2;
                }
                else
                {
                    break;
                }
            }
            extArg = 0;

            int instrSize = (byte)op >= 90 ? 3 : 1;
            instructions.Add(new Instruction(offset - instrSize, op, arg));
        }

        return instructions;
    }

    /// <summary>
    /// 检查是否为 Python 3.11+（有 CACHE 条目）
    /// </summary>
    private bool IsPython311Plus()
        => _magicBytes.Length >= 2 && _magicBytes[0] >= 0xA0 && _magicBytes[1] == 0x0D;

    /// <summary>
    /// 3.11+ 的缓存条目数（每个缓存条目 = 2 字节）
    /// 来源：CPython Lib/opcode.py _cache_entries
    /// </summary>
    private static int GetCacheCount(byte opcode)
    {
        // 3.12 cache entries
        return opcode switch
        {
            1 => 0,    // POP_TOP
            2 => 0,    // PUSH_NULL
            4 => 0,    // DUP_TOP
            5 => 0,    // DUP_TOP_TWO
            9 => 0,    // NOP
            11 => 1,   // UNARY_NEGATIVE
            12 => 0,   // UNARY_NOT
            15 => 0,   // UNARY_INVERT
            20 => 0,   // BINARY_OP (result)
            26 => 0,   // BINARY_SUBSCR
            30 => 0,   // STORE_SUBSCR
            35 => 0,   // UNPACK_SEQUENCE
            36 => 0,   // UNPACK_EX
            40 => 0,   // BUILD_TUPLE
            41 => 0,   // BUILD_LIST
            42 => 0,   // BUILD_SET
            43 => 0,   // BUILD_MAP
            47 => 0,   // BUILD_STRING
            48 => 0,   // BUILD_TUPLE_UNPACK
            55 => 0,   // INPLACE_ADD etc (now removed in 3.12)
            56 => 0,   // INPLACE_SUBTRACT
            61 => 0,   // LOAD_BUILD_CLASS
            68 => 0,   // GET_ITER
            69 => 0,   // GET_YIELD_FROM_ITER
            70 => 0,   // PRINT_EXPR
            71 => 0,   // LOAD_BUILD_CLASS
            72 => 0,   // YIELD_FROM
            73 => 0,   // GET_AWAITABLE
            74 => 0,   // LOAD_ASSERTION_ERROR
            75 => 0,   // RETURN_GENERATOR
            79 => 0,   // SETUP_WITH
            80 => 0,   // SETUP_CLEANUP
            81 => 0,   // SETUP_FINALLY
            83 => 0,   // POP_EXCEPT
            84 => 0,   // POP_FINALLY
            86 => 0,   // PUSH_EXC_INFO
            87 => 0,   // LOAD_LOCALS
            88 => 0,   // LOAD_FROM_DICT
            89 => 0,   // LOAD_BUILD_CLASS
            90 => 1,   // RESUME
            91 => 0,   // MATCH_CLASS
            92 => 0,   // MATCH_MAPPING
            93 => 0,   // MATCH_SEQUENCE
            94 => 0,   // MATCH_KEYS
            95 => 0,   // MATCH_KEY
            96 => 0,   // PUSH_EXC_INFO
            97 => 0,   // CHECK_EXC_MATCH
            98 => 0,   // CHECK_EG_MATCH
            99 => 0,   // PREP_RERAISE
            100 => 1,  // LOAD_CONST
            101 => 4,  // LOAD_NAME
            102 => 4,  // BUILD_TUPLE
            103 => 4,  // BUILD_LIST
            104 => 4,  // BUILD_SET
            105 => 4,  // BUILD_MAP
            106 => 4,  // LOAD_ATTR
            107 => 4,  // COMPARE_OP
            108 => 0,  // IMPORT_NAME
            109 => 0,  // IMPORT_FROM
            110 => 0,  // JUMP_FORWARD
            112 => 0,  // IS_OP
            113 => 0,  // CONTAINS_OP
            114 => 0,  // CONTAINS_OP
            115 => 0,  // POP_JUMP_IF_FALSE (3.11+)
            116 => 0,  // POP_JUMP_IF_TRUE (3.11+)
            117 => 0,  // JUMP_IF_TRUE_OR_POP
            118 => 0,  // JUMP_IF_FALSE_OR_POP
            119 => 0,  // JUMP_ABSOLUTE (3.11+ renamed)
            120 => 0,  // JUMP_BACKWARD
            121 => 0,  // JUMP_BACKWARD_NO_INTERRUPT
            122 => 1,  // BINARY_OP
            123 => 1,  // UNARY_OP
            124 => 1,  // LOAD_FAST
            125 => 1,  // STORE_FAST
            126 => 1,  // DELETE_FAST
            127 => 1,  // LOAD_FAST_CHECK
            128 => 1,  // LOAD_FAST_AND_CLEAR
            129 => 1,  // LOAD_DEREF
            130 => 1,  // STORE_DEREF
            131 => 1,  // LOAD_CLOSURE
            132 => 1,  // LOAD_CLASSDEREF
            133 => 1,  // LOAD_SUPER_ATTR
            135 => 0,  // STORE_ATTR
            136 => 0,  // DELETE_ATTR
            137 => 0,  // STORE_GLOBAL
            138 => 0,  // DELETE_GLOBAL
            140 => 0,  // LOAD_GLOBAL
            141 => 0,  // LOAD_FROM_DICT
            142 => 0,  // LOAD_METHOD (removed in 3.12, kept for compat)
            150 => 0,  // LIST_APPEND
            151 => 0,  // SET_ADD
            152 => 0,  // MAP_ADD
            153 => 0,  // LOAD_ATTR
            154 => 3,  // PRECALL (3.11) or 0 (3.12→CALL)
            155 => 0,  // CALL (3.11)
            156 => 0,  // KW_NAMES
            157 => 0,  // LOAD_LOCALS
            160 => 0,  // LOAD_METHOD (3.11)
            162 => 0,  // CALL_INTRINSIC_1
            163 => 0,  // CALL_INTRINSIC_2
            164 => 0,  // LOAD_FROM_DICT
            165 => 0,  // LOAD_BUILD_CLASS
            166 => 0,  // PRECALL (3.11)
            167 => 0,  // CALL (3.11)
            170 => 0,  // PUSH_EXC_INFO
            _ => 0,
        };
    }

    /// <summary>
    /// 解析 3.11+ 字节码（跳 CACHE 条目）
    /// </summary>
    private List<Instruction> ParseInstructions311Plus(byte[] bytecode)
    {
        var instructions = new List<Instruction>();
        int offset = 0;
        int extArg = 0;

        while (offset + 1 < bytecode.Length)
        {
            byte rawOp = bytecode[offset];
            var rawArg = bytecode[offset + 1];

            // Skip cache entries (opcode 0)
            if (rawOp == 0)
            {
                offset += 2;
                continue;
            }

            var op = (Models.Bytecode.Opcode)rawOp;

            // 3.11+: RESUME (opcode 90) 与旧版 STORE_NAME 冲突，需要修正
            if (IsPython311Plus() && rawOp == 90)
                op = Models.Bytecode.Opcode.RESUME;

            // Handle EXTENDED_ARG chain
            if (op == Models.Bytecode.Opcode.EXTENDED_ARG)
            {
                extArg = (extArg << 8) | rawArg;
                offset += 2;
                continue;
            }

            // Instructions with arguments: rawOp >= 90 (HAVE_ARGUMENT threshold)
            int? arg = null;
            if (rawOp >= 90)
                arg = (extArg << 8) | rawArg;
            extArg = 0;

            // Python 3.10+ 使用 word 偏移 — 3.11+ 沿用此规则
            // 需要区分绝对值跳转和相对值跳转
            if (IsWordOffsetVersion() && arg.HasValue && IsJumpInstruction(op))
                arg = arg.Value * 2;

            instructions.Add(new Instruction(offset, op, arg));

            // Skip cache entries after this instruction
            int cacheEntries = GetCacheCount(rawOp);
            offset += 2 + cacheEntries * 2;
        }

        return instructions;
    }

    /// <summary>
    /// 解析 3.10 及更早的字节码（无 CACHE）
    /// </summary>
    private List<Instruction> ParseInstructionsWordcode(byte[] bytecode)
    {
        var instructions = new List<Instruction>();
        int offset = 0;
        int extArg = 0;

        while (offset + 1 < bytecode.Length)
        {
            var op = (Models.Bytecode.Opcode)bytecode[offset];
            var rawArg = bytecode[offset + 1];

            // Handle EXTENDED_ARG chain
            if (op == Models.Bytecode.Opcode.EXTENDED_ARG)
            {
                extArg = (extArg << 8) | rawArg;
                offset += 2;
                continue;
            }

            // Instructions with arguments use the combined value
            int? arg = null;
            // HAVE_ARGUMENT = 90 threshold
            if ((byte)op >= 90)
                arg = (extArg << 8) | rawArg;
            extArg = 0;

            // Python 3.10+ 使用 word 偏移（每个指令2字节）
            if (IsWordOffsetVersion() && arg.HasValue && IsJumpInstruction(op))
                arg = arg.Value * 2;

            instructions.Add(new Instruction(offset, op, arg));
            offset += 2;
        }

        return instructions;
    }

    private static bool IsJumpInstruction(Opcode op) => op switch
    {
        Opcode.JUMP_ABSOLUTE or Opcode.JUMP_FORWARD or Opcode.JUMP_BACKWARD
            or Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
            or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
            or Opcode.FOR_ITER or Opcode.JUMP_BACKWARD_NO_INTERRUPT
            or Opcode.SETUP_FINALLY => true,
        _ => false
    };

    // ---- Marshal读取辅助方法 ----

    private List<string> ReadMarshalObjectAsStrList(BinaryReader br)
    {
        var obj = ReadMarshalObject(br);
        if (obj is System.Collections.IList list)
        {
            var result = new List<string>(list.Count);
            foreach (var item in list)
                result.Add(item?.ToString() ?? "");
            return result;
        }
        return new List<string>();
    }

    private byte[] ReadMarshalBytes(BinaryReader br)
    {
        var rawType = br.ReadByte();
        var type = (byte)(rawType & ~MarshalType.TYPE_FLAG_REF);

        int length;
        if (type == MarshalType.TYPE_SHORT_ASCII || type == MarshalType.TYPE_SHORT_ASCII_INTERNED)
            length = br.ReadByte();
        else
            length = br.ReadInt32();
        return br.ReadBytes(length);
    }

    private string ReadMarshalString(BinaryReader br)
    {
        var rawType = br.ReadByte();
        var type = (byte)(rawType & ~MarshalType.TYPE_FLAG_REF);
        bool hasRef = (rawType & MarshalType.TYPE_FLAG_REF) != 0;

        string result;
        // Handle direct string types
        if (type == MarshalType.TYPE_SHORT_ASCII || type == MarshalType.TYPE_SHORT_ASCII_INTERNED)
            result = ReadMarshalShortString(br);
        else if (type == MarshalType.TYPE_ASCII || type == MarshalType.TYPE_ASCII_INTERNED || type == MarshalType.TYPE_UNICODE)
            result = ReadMarshalLongString(br);
        else if (type == MarshalType.TYPE_STRING)
        {
            var data = ReadMarshalBytesDirect(br);
            result = Encoding.UTF8.GetString(data);
        }
        else if (type == MarshalType.TYPE_REF)
        {
            var refIdx = br.ReadInt32();
            if (refIdx >= 0 && refIdx < _refList.Count && _refList[refIdx] is string refStr)
                return refStr;
            return "";
        }
        else
            throw new InvalidPycFormatException($"Unexpected string type: {rawType} (0x{rawType:X2})");

        // 如果带 FLAG_REF，加入 _refList 供后续 TYPE_REF 引用
        if (hasRef)
        {
            var refIndex = _refList.Count;
            _refList.Add(result);
        }

        return result;
    }

    /// <summary>
    /// Read marshal bytes directly (already consumed the type byte).
    /// </summary>
    private byte[] ReadMarshalBytesDirect(BinaryReader br)
    {
        var length = br.ReadInt32();
        return br.ReadBytes(length);
    }

    private List<object?> ReadMarshalList(BinaryReader br)
    {
        var rawType = br.ReadByte();
        var type = (byte)(rawType & ~MarshalType.TYPE_FLAG_REF);

        // Handle TYPE_REF: return previously stored list from ref list
        if (type == MarshalType.TYPE_REF)
        {
            var refIdx = br.ReadInt32();
            if (refIdx >= 0 && refIdx < _refList.Count && _refList[refIdx] is List<object?> refList)
                return refList;
            return new List<object?>();
        }

        if (type != MarshalType.TYPE_LIST && type != MarshalType.TYPE_TUPLE && type != MarshalType.TYPE_SMALL_TUPLE)
        {
            throw new InvalidPycFormatException($"Expected list/tuple, got {rawType}");
        }

        int count;
        if (type == MarshalType.TYPE_SMALL_TUPLE)
            count = br.ReadByte();
        else
            count = br.ReadInt32();

        bool isTuple = (type == MarshalType.TYPE_TUPLE || type == MarshalType.TYPE_SMALL_TUPLE);
        var items = isTuple ? new PyTuple() : new List<object?>();
        for (int i = 0; i < count; i++)
        {
            items.Add(ReadMarshalObject(br));
        }
        return items;
    }

    private Dictionary<int, object?> ReadMarshalDict(BinaryReader br)
    {
        var dict = new Dictionary<int, object?>();
        if (IsPython38Plus())
        {
            // 3.8+: 通过 ReadMarshalObject 正确处理 FLAG_REF
            var obj = ReadMarshalObject(br);
            if (obj is System.Collections.IList list)
            {
                for (int i = 0; i < list.Count; i++)
                    dict[i] = list[i];
            }
        }
        else
        {
            // 2.7/3.5-3.7: FLAG_REF 不存在，直接读 marshal list
            var list = ReadMarshalList(br);
            for (int i = 0; i < list.Count; i++)
            {
                dict[i] = list[i];
            }
        }
        return dict;
    }

    private object? ReadMarshalObject(BinaryReader br)
    {
        var rawType = br.ReadByte();
        var type = (byte)(rawType & ~MarshalType.TYPE_FLAG_REF);
        
        object? result;
        if ((rawType & MarshalType.TYPE_FLAG_REF) != 0)
        {
            var refIndex = _refList.Count;
            _refList.Add(null);
            result = ReadMarshalValue(br, type);
            _refList[refIndex] = result;
        }
        else
        {
            result = ReadMarshalValue(br, type);
        }

        return result;
    }

    /// <summary>
    /// 读取类型字节，如果 FLAG_REF 被设置则跳过 4 字节的引用索引。
    /// Python 3.4+ marshal 格式：FLAG_REF 类型字节后紧跟引用索引（4字节）。
    /// </summary>
    private (byte rawType, byte type) ReadTypeAndSkipRef(BinaryReader br)
    {
        var rawType = br.ReadByte();
        var type = (byte)(rawType & ~MarshalType.TYPE_FLAG_REF);
        if ((rawType & MarshalType.TYPE_FLAG_REF) != 0)
        {
            // FLAG_REF 类型字节后有一个 4 字节引用索引需要跳过
            br.ReadInt32();
        }
        return (rawType, type);
    }

    private object? ReadMarshalValue(BinaryReader br, byte type)
    {
        return type switch
        {
            MarshalType.TYPE_NONE => null,
            MarshalType.TYPE_INT => br.ReadInt32(),
            MarshalType.TYPE_LONG => br.ReadInt64(),
            MarshalType.TYPE_FLOAT => br.ReadDouble(),
            MarshalType.TYPE_BINARY_FLOAT => br.ReadDouble(),
            MarshalType.TYPE_COMPLEX => (br.ReadDouble(), br.ReadDouble()),
            // 115 = TYPE_CODE_SIMPLE (3.11+) 或 TYPE_STRING (旧版)
            MarshalType.TYPE_STRING when IsPython311Plus() && !IsPython27()
                => ReadMarshalCodeObject(br, isSimple: true),
            MarshalType.TYPE_STRING => ReadMarshalBytesDirect(br),
            MarshalType.TYPE_SHORT_ASCII => ReadMarshalShortString(br),
            MarshalType.TYPE_SHORT_ASCII_INTERNED => ReadMarshalShortString(br),
            MarshalType.TYPE_ASCII => ReadMarshalLongString(br),
            MarshalType.TYPE_ASCII_INTERNED => ReadMarshalLongString(br),
            MarshalType.TYPE_UNICODE => ReadMarshalLongString(br),
            MarshalType.TYPE_SMALL_TUPLE => ReadSmallTuple(br),
            MarshalType.TYPE_CODE => ReadMarshalCodeObject(br, isSimple: false),
            MarshalType.TYPE_TRUE => true,
            MarshalType.TYPE_FALSE => false,
            MarshalType.TYPE_ELLIPSIS => new object(),
            MarshalType.TYPE_REF => ReadRef(br),
            MarshalType.TYPE_SET => new List<object?>(), // Skip set content for now
            MarshalType.TYPE_FROZENSET => new List<object?>(),
            _ => HandleUnknownMarshalType(br, type),
        };
    }

    private object? HandleUnknownMarshalType(BinaryReader br, byte type)
    {
        // Try to skip: assume it's a value with a 4-byte length prefix
        try
        {
            if (br.BaseStream.Position < br.BaseStream.Length)
            {
                var length = Math.Min(br.ReadInt32(), br.BaseStream.Length - br.BaseStream.Position);
                br.BaseStream.Position += length;
            }
        }
        catch { }
        return null;
    }

    private object? ReadRef(BinaryReader br)
    {
        var index = br.ReadInt32();
        if (index >= 0 && index < _refList.Count)
            return _refList[index];
        return null;
    }

    private string ReadMarshalShortString(BinaryReader br)
    {
        var len = br.ReadByte();
        return Encoding.UTF8.GetString(br.ReadBytes(len));
    }

    private string ReadMarshalLongString(BinaryReader br)
    {
        var len = br.ReadInt32();
        return Encoding.UTF8.GetString(br.ReadBytes(len));
    }

    private PyTuple ReadSmallTuple(BinaryReader br)
    {
        var count = br.ReadByte();
        var items = new PyTuple();
        for (int i = 0; i < count; i++)
        {
            items.Add(ReadMarshalObject(br));
        }
        return items;
    }

    private Dictionary<int, int> ParseLineNumberTable(byte[] lnotab, List<Instruction> instructions)
    {
        var table = new Dictionary<int, int>();
        int line = instructions.Count > 0 ? 1 : 0;
        int addr = 0;

        for (int i = 0; i < lnotab.Length; i += 2)
        {
            if (i + 1 >= lnotab.Length) break;
            addr += lnotab[i];
            line += (sbyte)lnotab[i + 1];
            table[addr] = line;
        }

        return table;
    }

    /// <summary>
    /// 解析 Python 3.10+ co_exceptiontable。
    /// 每个条目 8 字节（4 个 word offset，每个 2 字节，小端序）：
    ///   [start(2B)][end(2B)][target(2B)][depth+lasti(2B)]
    /// word offset → byte offset = word * 2
    /// </summary>
    private List<ExceptionTableEntry> ParseExceptionTable(byte[] data)
    {
        var entries = new List<ExceptionTableEntry>();
        for (int i = 0; i + 7 < data.Length; i += 8)
        {
            int start = (data[i] | (data[i + 1] << 8)) * 2;
            int end = (data[i + 2] | (data[i + 3] << 8)) * 2;
            int target = (data[i + 4] | (data[i + 5] << 8)) * 2;
            int depthLasti = data[i + 6] | (data[i + 7] << 8);
            int depth = depthLasti & 0x3;
            bool lasti = (depthLasti & 0x4) != 0;

            entries.Add(new ExceptionTableEntry
            {
                StartOffset = start,
                EndOffset = end,
                TargetOffset = target,
                Depth = depth,
                Lasti = lasti
            });
        }
        return entries;
    }
}
