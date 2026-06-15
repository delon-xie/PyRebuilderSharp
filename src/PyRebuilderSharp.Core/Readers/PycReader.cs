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
        { new byte[] { 0x2B, 0x0E, 0x0D, 0x0A }, "Python 3.14" },
    };

    // 3.11+ magic bytes 集合（用于 IsPython311Plus 快速查找）
    private static readonly HashSet<string> _py311PlusMagicHex = new()
    {
        "A00D0D0A", "A70D0D0A",  // 3.11
        "CB0D0D0A",               // 3.12
        "E70D0D0A",               // 3.13
        "F30D0D0A", "2B0E0D0A",  // 3.14
    };

    private readonly List<object?> _refList = new();
    private readonly List<string> _internedStrings27 = new(); // Python 2.7 interned string table
    private string _pythonVersion = "Python 3.8";
    private byte[] _magicBytes = Array.Empty<byte>();
    /// <summary>检测到的 Python 次版本号（11=3.11, 12=3.12, 13=3.13, 14=3.14, 0=未知）。</summary>
    private int _pythonMinorVersion;
    private int _marshalDepth = 0;
    private const int MaxMarshalDepth = 100000;
    private int _marshalCalls = 0;
    private const int MaxMarshalCalls = 50000;
    private System.Diagnostics.Stopwatch? _readTimer;
    private const int MaxReadSeconds = 15;
    private void CheckReadTimeout(BinaryReader? br = null)
    {
        if (_readTimer == null) return;
        if (_readTimer.Elapsed.TotalSeconds > MaxReadSeconds)
        {
            System.Console.Error.WriteLine($"[TIMEOUT] CheckReadTimeout fires at {_readTimer.Elapsed.TotalSeconds:F1}s, offset={br?.BaseStream.Position}, calls={_marshalCalls}");
            System.Console.Error.Flush();
            throw new TimeoutException(
                $"PycReader timed out after {MaxReadSeconds}s at offset {br?.BaseStream.Position}/{br?.BaseStream.Length}, " +
                $"marshalDepth={_marshalDepth}, calls={_marshalCalls}.");
        }
    }
    
    /// <summary>
    /// 记录警告日志（含流位置、marshal深度、上下文方法名）。
    /// 用于所有异常捕获点，方便后续排查 marshal 格式问题。
    /// </summary>
    private void LogCatch(BinaryReader br, string context, Exception ex)
    {
        System.Console.Error.WriteLine(
            $"[WARN] PycReader.{context}: offset={br.BaseStream.Position}/{br.BaseStream.Length} " +
            $"marshalDepth={_marshalDepth} elapsed={_readTimer?.Elapsed.TotalSeconds:F1}s " +
            $"ex={ex.GetType().Name}: {ex.Message}");
    }
    
    /// <summary>
    /// 无 BinaryReader 时的重载。
    /// </summary>
    private void LogCatch(string context, Exception ex, string? extraInfo = null)
    {
        System.Console.Error.WriteLine(
            $"[WARN] PycReader.{context}: marshalDepth={_marshalDepth} " +
            $"elapsed={_readTimer?.Elapsed.TotalSeconds:F1}s " +
            $"ex={ex.GetType().Name}: {ex.Message}{(extraInfo != null ? " " + extraInfo : "")}");
    }

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
        
        _marshalDepth = 0;
        _marshalCalls = 0;
        _readTimer = System.Diagnostics.Stopwatch.StartNew();
        
        // Step 1: 验证Magic Number
        var magic = br.ReadBytes(4);
        _magicBytes = magic;
        var versionInfo = ValidateMagic(magic);
        _pythonVersion = versionInfo;
        // 检测次版本号用于 3.11+/3.12/3.13+ 的分派
        var magicHex = BitConverter.ToString(magic, 0, 4).Replace("-", "");
        _pythonMinorVersion = magicHex switch
        {
            "A00D0D0A" or "A70D0D0A" => 11,
            "CB0D0D0A" => 12,
            "E70D0D0A" => 13,
            "F30D0D0A" or "2B0E0D0A" => 14,
            _ => 0,
        };

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
            // Python 3.11+: flags & 0x01 → hash-based .pyc (PEP 552)
            //   magic(4) + flags(4) + hash(8) + source_size(4) = 20 bytes
            var flags = br.ReadInt32();
            bool isHashBased = (flags & 0x01) != 0;
            if (isHashBased)
            {
                br.ReadBytes(8); // hash (64 bits, PEP 552)
            }
            else
            {
                br.ReadInt32(); // timestamp
            }
            br.ReadInt32(); // source_size
        }

        // Step 3: 读取Marshal数据
        _marshalDepth = 0;
        _marshalCalls = 0;
        _readTimer = System.Diagnostics.Stopwatch.StartNew();
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

        // 设置版本信息
        code.IsPython38Plus = IsPython38Plus();

        try
        {
            if (IsPython27())
                return ReadMarshalCodeObject27(br);

            // 读取CodeObject的各个字段
            code.ArgCount = br.ReadInt32();
            if (IsPython311Plus() && !isSimple)
            {
                // Python 3.11+ TYPE_CODE: argcount, posonlyargcount, kwonlyargcount, stacksize, flags
                // （无 nlocals — 由 localsplusnames+kinds 派生）
                var posOnlyArgCount = br.ReadInt32();
                code.KwOnlyArgCount = br.ReadInt32();
                var stacksize = br.ReadInt32();
                var flags = br.ReadInt32();
                code.IsGenerator = (flags & 0x20) != 0;
                code.IsCoroutine = (flags & 0x80) != 0;
                code.IsAsyncGenerator = (flags & 0xC0) == 0xC0;
            }
            else if (IsPython38Plus() && !isSimple)
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
            // v3.11+: TYPE_STRING(0x73) 是字节码（非 TYPE_CODE_SIMPLE），用 ReadRawMarshalBytes
            byte[]? bcBytes;
            if (IsPython311Plus())
            {
                var bcStart = br.BaseStream.Position;
                bcBytes = ReadRawMarshalBytes(br);
            }
            else
            {
                var bytecodeObj = ReadMarshalObject(br);
                bcBytes = bytecodeObj as byte[];
            }
            if (bcBytes != null)
                code.Instructions = ParseInstructions(bcBytes);

            code.Constants = ReadMarshalDictSafe(br, code);
            
            // names/varnames/freevars/cellvars
            if (IsPython311Plus())
            {
                // Python 3.11+: marshal 格式改为单个 localsplusnames + localspluskinds
                // co_names 仍然独立存储
                code.Names = ReadMarshalObjectAsStrList(br);
                var localsplusnames = ReadMarshalObjectAsStrList(br);
                
                // localspluskinds = 字节数组
                byte[]? localspluskinds = null;
                try
                {
                    localspluskinds = ReadRawMarshalBytes(br);
                }
                catch (Exception ex) { LogCatch(br, "ReadMarshalCodeObject.localspluskinds", ex); }
                
                // 按类型拆分为 varnames/cellvars/freevars
                var varnames = new List<string>();
                var cellvars = new List<string>();
                var freevars = new List<string>();
                for (int i = 0; i < localsplusnames.Count; i++)
                {
                    var kind = (localspluskinds != null && i < localspluskinds.Length) ? localspluskinds[i] : (byte)0;
                    switch (kind)
                    {
                        case 2: freevars.Add(localsplusnames[i]); break;
                        case 1: cellvars.Add(localsplusnames[i]); break;
                        default:
                        case 0: varnames.Add(localsplusnames[i]); break;
                    }
                }
                code.Varnames = varnames;
                code.Freevars = freevars;
                code.Cellvars = cellvars;
            }
            else
            {
                // Pre-3.11: 独立的 varnames/freevars/cellvars
                code.Names = ReadMarshalObjectAsStrList(br);
                code.Varnames = ReadMarshalObjectAsStrList(br);
                code.Freevars = ReadMarshalObjectAsStrList(br);
                code.Cellvars = ReadMarshalObjectAsStrList(br);
            }

            // filename/name — 通过 ReadMarshalObject 以正确处理 FLAG_REF
            var filenameObj = ReadMarshalObject(br);
            code.Filename = filenameObj?.ToString() ?? "<unknown>";
            var nameObj = ReadMarshalObject(br);
            code.Name = nameObj?.ToString() ?? "<module>";

            // qualname (3.11+ 的所有代码对象都有)
            if (IsPython311Plus())
            {
                if (code.Name == "<module>") System.Console.Error.WriteLine($"[DIAG] before qualname: pos={br.BaseStream.Position}");
                try { var qualObj = ReadMarshalObject(br); if (code.Name == "<module>") System.Console.Error.WriteLine($"[DIAG] qualname={qualObj} len={qualObj?.ToString()?.Length} pos={br.BaseStream.Position}"); }
                catch (Exception ex) { LogCatch(br, "ReadMarshalCodeObject.qualname", ex); }
            }

            // first line number (int32) — 3.8+ 的字段
            try { code.FirstLineNumber = br.ReadInt32(); if (code.Name == "<module>") System.Console.Error.WriteLine($"[DIAG] firstline={code.FirstLineNumber} pos={br.BaseStream.Position}"); }
            catch (Exception ex) { LogCatch(br, "ReadMarshalCodeObject.firstlineno", ex); }

            // lnotab/linetable
            byte[]? lnotab;
            if (IsPython311Plus())
            {
                if (code.Name == "<module>") System.Console.Error.WriteLine($"[DIAG] before lnotab: pos={br.BaseStream.Position}");
                lnotab = ReadRawMarshalBytes(br);
                if (code.Name == "<module>") System.Console.Error.WriteLine($"[DIAG] lnotab: len={lnotab?.Length} pos={br.BaseStream.Position}");
            }
            else
            {
                var lnotabObj = ReadMarshalObject(br);
                lnotab = lnotabObj as byte[];
            }
            if (lnotab != null)
            {
                code.LineNumberBytes = lnotab;
                code.HasLinetable = IsPython311Plus();
                code.LineNumberTable = ParseLineNumberTable(lnotab, code.Instructions, IsPython311Plus());
            }

            // co_exceptiontable（3.11+ 的所有代码对象都有）
            if (IsPython311Plus() && br.BaseStream.Position < br.BaseStream.Length)
            {
                try
                {
                    // 先 peek 类型字节，只有是 string/bytes/ref 类型才读取
                    var peekByte = br.ReadByte();
                    br.BaseStream.Position--;
                    var peekType = (byte)(peekByte & ~MarshalType.TYPE_FLAG_REF);
                    if (code.Name == "<module>")
                        System.Console.Error.WriteLine($"[DIAG] exc table offset={br.BaseStream.Position} peek=0x{peekByte:X2} type=0x{peekType:X2} flag_ref={(peekByte & MarshalType.TYPE_FLAG_REF) != 0}");
                    if (peekType == MarshalType.TYPE_STRING || peekType == MarshalType.TYPE_BYTES
                        || peekType == MarshalType.TYPE_SHORT_ASCII || peekType == MarshalType.TYPE_ASCII
                        || peekType == MarshalType.TYPE_UNICODE)
                    {
                        var excBytes = ReadRawMarshalBytes(br);
                        if (excBytes != null && excBytes.Length > 0)
                        {
                            System.Console.Error.WriteLine($"[DIAG] ExceptionTable raw bytes ({excBytes.Length} bytes): {BitConverter.ToString(excBytes)}");
                            code.ExceptionTable = ParseExceptionTable(excBytes);
                        }
                    }
                    else if (peekType == MarshalType.TYPE_REF)
                    {
                        // Exception table is a reference to previously stored bytes
                        var excObj = ReadMarshalObject(br);
                        if (excObj is byte[] excBytes && excBytes.Length > 0)
                            code.ExceptionTable = ParseExceptionTable(excBytes);
                    }
                }
                catch (Exception ex) { LogCatch(br, "ReadMarshalCodeObject.exceptiontable", ex); }
            }
        }
        catch (EndOfStreamException eos)
        {
            LogCatch(br, "ReadMarshalCodeObject.outer", eos);
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
        code.IsPython27 = true;
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

            // 读取字节码 — 使用 ReadRawMarshalBytes（v2.7 TYPE_STRING 格式）
            var bcBytes = ReadRawMarshalBytes(br);
            if (bcBytes != null)
                code.Instructions = ParseInstructions(bcBytes);

            code.Constants = ReadMarshalDictSafe27(br, code);

            code.Names = ReadMarshalListSafe27(br)?.Select(x => x?.ToString() ?? "").ToList() ?? new();
            code.Varnames = ReadMarshalListSafe27(br)?.Select(x => x?.ToString() ?? "").ToList() ?? new();
            code.Freevars = ReadMarshalListSafe27(br)?.Select(x => x?.ToString() ?? "").ToList() ?? new();
            code.Cellvars = ReadMarshalListSafe27(br)?.Select(x => x?.ToString() ?? "").ToList() ?? new();

            code.Filename = ReadMarshalString27(br) ?? "<unknown>";
            code.Name = ReadMarshalString27(br) ?? "<module>";

            // Python 2.7 有 firstlineno
            try { code.FirstLineNumber = br.ReadInt32(); }
            catch (Exception ex) { LogCatch(br, "ReadMarshalCodeObject27.firstlineno", ex); }

            var lnotab = ReadMarshalBytes27(br);
            if (lnotab != null)
                code.LineNumberTable = ParseLineNumberTable(lnotab, code.Instructions);
        }
        catch (EndOfStreamException eos)
        {
            LogCatch(br, "ReadMarshalCodeObject27.outer", eos);
        }
        return code;
    }

    /// <summary>
    /// Python 2.7 安全的 Marshal 列表读取。
    /// 在 2.7 中，names/varnames/freevars/cellvars 是 tuple。
    /// v2.7 没有 FLAG_REF/TYPE_REF 机制。
    /// </summary>
    private List<object?>? ReadMarshalListSafe27(BinaryReader br)
    {
        if (br.BaseStream.Position >= br.BaseStream.Length)
            return null;
        try
        {
            var type = br.ReadByte(); // v2.7: 无 FLAG_REF，原始类型字节

            // 只接受 tuple 类型
            if (type != MarshalType.TYPE_TUPLE && type != MarshalType.TYPE_SMALL_TUPLE)
                return new List<object?>();

            int count = type == MarshalType.TYPE_SMALL_TUPLE ? br.ReadByte() : br.ReadInt32();
            var items = new List<object?>();
            for (int i = 0; i < count; i++)
            {
                try
                {
                    items.Add(ReadMarshalValue27(br));
                }
                catch (Exception ex)
                {
                    LogCatch(br, "ReadMarshalListSafe27.element", ex);
                    break;
                }
            }
            return items;
        }
        catch (Exception ex) { LogCatch(br, "ReadMarshalListSafe27.outer", ex); return null; }
    }

    private object? ReadMarshalValue27(BinaryReader br)
    {
        var type = br.ReadByte();
        
        // Handle TYPE_STRINGREF (0x52 = 'R'): references an interned string by index
        if (type == 0x52)
        {
            var refIdx = br.ReadInt32();
            if (refIdx >= 0 && refIdx < _internedStrings27.Count)
                return _internedStrings27[refIdx];
            return $"strref_{refIdx}";
        }
        
        return type switch
        {
            78 => null,             // 'N' TYPE_NONE
            105 => br.ReadInt32(),  // 'i' TYPE_INT
            108 => ReadMarshalLong27(br), // 'l' TYPE_LONG (v2.7: count + shorts)
            102 => double.Parse(System.Text.Encoding.UTF8.GetString(br.ReadBytes(br.ReadInt32()))), // 'f' TYPE_FLOAT
            103 => br.ReadDouble(), // 'g' TYPE_BINARY_FLOAT
            121 => new double[] { br.ReadDouble(), br.ReadDouble() }, // 'y' TYPE_BINARY_COMPLEX [real, imag]
            84 => true,             // 'T' TYPE_TRUE
            70 => false,            // 'F' TYPE_FALSE
            115 or 116 => ReadMarshalString27FromType(br, type), // 's' TYPE_STRING, 't' TYPE_INTERNED
            117 => ReadMarshalUnicode27(br), // 'u' TYPE_UNICODE — Python 2.7 unicode string
            122 => ReadStringRef27_7a(br), // 'z' TYPE_STRINGREF (v3.x compat, v2.7 中不出现在此处)
            40 or 41 or 91 => ReadMarshalList27(br, type), // '(' TYPE_TUPLE, ')' TYPE_SMALL_TUPLE, '[' TYPE_LIST
            60 or 62 => ReadMarshalSetOrFrozenset27(br, type), // '<' TYPE_SET, '>' TYPE_FROZENSET
            46 => new object(),     // '.' TYPE_ELLIPSIS
            99 => ReadMarshalCodeObject27(br), // 'c' TYPE_CODE (nested functions/lambdas)
            _ => SkipUnknown27(br, type),
        };
    }

    private string ReadMarshalString27(BinaryReader br)
    {
        var type = br.ReadByte();
        // v2.7: 0x52 = TYPE_STRINGREF — reference to previously interned string
        if (type == 0x52)
        {
            var refIdx = br.ReadInt32();
            if (refIdx >= 0 && refIdx < _internedStrings27.Count)
                return _internedStrings27[refIdx];
            return $"strref_{refIdx}";
        }
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
            return ReadStringRef27_7a(br);
        }
        if (type == 117) // 'u' TYPE_UNICODE
        {
            var len = br.ReadInt32();
            var bytes = br.ReadBytes(len);
            return System.Text.Encoding.UTF8.GetString(bytes);
        }
        return "";
    }

    /// <summary>
    /// Python 2.7 TYPE_UNICODE (0x75 = 'u') — UTF-8 encoded unicode string。
    /// 4字节长度 + UTF-8 内容字节。
    /// </summary>
    private string ReadMarshalUnicode27(BinaryReader br)
    {
        var len = br.ReadInt32();
        var bytes = br.ReadBytes(len);
        return System.Text.Encoding.UTF8.GetString(bytes);
    }

    /// <summary>
    /// Python 2.7 lnotab 读取 — 正确处理 TYPE_STRINGREF (0x52)。</summary>
    private byte[]? ReadMarshalBytes27(BinaryReader br)
    {
        if (br.BaseStream.Position >= br.BaseStream.Length)
            return null;
        try
        {
            var rawType = br.ReadByte();
            // v2.7 TYPE_STRINGREF (0x52): reference to interned string
            if (rawType == 0x52)
            {
                var refIdx = br.ReadInt32();
                if (refIdx >= 0 && refIdx < _internedStrings27.Count)
                {
                    var interned = _internedStrings27[refIdx];
                    return System.Text.Encoding.UTF8.GetBytes(interned);
                }
                return null;
            }
            // v2.7 TYPE_STRING (0x73) or TYPE_INTERNED (116): 4-byte length + data
            if (rawType == 0x73 || rawType == 116)
            {
                var len = br.ReadInt32();
                return br.ReadBytes(len);
            }
            // TYPE_SHORT_ASCII (0x7a): 1-byte length + data
            if (rawType == 0x7a)
            {
                var len = br.ReadByte();
                return br.ReadBytes(len);
            }
            return null;
        }
        catch (Exception ex) { LogCatch(br, "ReadMarshalBytes27", ex); return null; }
    }

    /// <summary>
    /// Python 2.7 TYPE_LONG (0x6c = 'l') — 长整数，格式为 count(int32) + count*2字节的shorts。
    /// </summary>
    private object? ReadMarshalLong27(BinaryReader br)
    {
        try
        {
            var size = br.ReadInt32(); // digit count
            if (size <= 0 || size > 256) return 0L;
            var digits = new short[size];
            for (int i = 0; i < size; i++)
                digits[i] = br.ReadInt16();
            // Convert back: Python uses base 2^15 digits
            long result = 0;
            for (int i = size - 1; i >= 0; i--)
                result = (result << 15) + (digits[i] & 0x7FFF);
            // Last digit sign bit
            if ((digits[size - 1] & 0x8000) != 0)
                result = -result;
            return result;
        }
        catch (Exception ex) { LogCatch(br, "ReadMarshalLong27", ex); return 0L; }
    }

    /// <summary>
    /// Python TYPE_SET (0x3c = '&lt;') 或 TYPE_FROZENSET (0x3e = '&gt;')。
    /// 格式：count(int32) + count 个 marshal 值。返回 List。
    /// v2.7 和 v3.x 通用。
    /// </summary>
    private List<object?> ReadMarshalSetOrFrozenset27(BinaryReader br, byte type)
    {
        var count = br.ReadInt32();
        var items = new List<object?>();
        for (int i = 0; i < count; i++)
        {
            if (i >= 10000) { LogCatch($"ReadMarshalSetOrFrozenset27.count={count}", new InvalidOperationException($"Safety limit at {i}")); break; }
            items.Add(ReadMarshalValue27(br));
        }
        return items;
    }

    /// <summary>
    /// v3.x 的 TYPE_SET / TYPE_FROZENSET 读取。
    /// </summary>
    private List<object?> ReadMarshalSetOrFrozenset(BinaryReader br)
    {
        var count = br.ReadInt32();
        var items = new List<object?>();
        for (int i = 0; i < count; i++)
        {
            if (i >= 10000) { LogCatch($"ReadMarshalSetOrFrozenset.count={count}", new InvalidOperationException($"Safety limit at {i}")); break; }
            items.Add(ReadMarshalObject(br));
        }
        return items;
    }

    /// <summary>
    /// Python 2.7 TYPE_STRINGREF (0x7a) — v3.x 兼容，引用 interned string。
    /// 纯 v2.7 文件中几乎不出现（v2.7 的 TYPE_STRINGREF 是 0x52）。
    /// </summary>
    private string ReadStringRef27_7a(BinaryReader br)
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
        {
            if (i >= 10000) { LogCatch($"ReadMarshalList27.count={count}", new InvalidOperationException($"Safety limit at {i}")); break; }
            items.Add(ReadMarshalValue27(br));
        }
        return items;
    }

    /// <summary>
    /// Python 2.7 常量表读取 — 使用 ReadMarshalValue27 确保 TYPE_INTERNED/TYPE_STRINGREF 正确处理。
    /// </summary>
    private Dictionary<int, object?> ReadMarshalDictSafe27(BinaryReader br, CodeObject? parentCode = null)
    {
        if (br.BaseStream.Position >= br.BaseStream.Length)
            return new();
        try
        {
            var list = ReadMarshalListSafe27(br);
            if (list == null) return new();
            var dict = new Dictionary<int, object?>();
            for (int i = 0; i < list.Count; i++)
            {
                dict[i] = list[i];
                if (list[i] is CodeObject childCode && parentCode != null)
                    parentCode.ChildCodes.Add(childCode);
            }
            return dict;
        }
        catch (Exception ex) { LogCatch(br, "ReadMarshalDictSafe27", ex); return new(); }
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
        catch (Exception ex) { LogCatch(br, "SkipUnknown27", ex); }
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
        catch (Exception ex) { LogCatch(br, "ReadMarshalBytesSafe", ex); return null; }
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
            LogCatch(br, $"ReadMarshalDictSafe(offset={br.BaseStream.Position})", ex);
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
        catch (Exception ex) { LogCatch(br, "ReadMarshalListSafe", ex); return null; }
    }

    /// <summary>
    /// 安全的 Marshal String 读取。
    /// </summary>
    private string? ReadMarshalStringSafe(BinaryReader br)
    {
        if (br.BaseStream.Position >= br.BaseStream.Length)
            return null;
        try { return ReadMarshalString(br); }
        catch (Exception ex) { LogCatch(br, "ReadMarshalStringSafe", ex); return null; }
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
            var rawOp = bytecode[offset];
            // v2.7: map opcodes 70-89 to v2.7-specific enum values
            var op = IsPython27() && rawOp is >= 70 and <= 89
                ? MapOpcode27(rawOp)
                : (Models.Bytecode.Opcode)rawOp;
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
    /// 将 Python 2.7 的原始 opcode 映射到正确的枚举值。
    /// v2.7 opcodes 70-89 与 v3.x 完全不同：
    ///   70=PRINT_EXPR, 71=PRINT_ITEM, 72=PRINT_NEWLINE...
    ///   86=YIELD_VALUE, 87=POP_BLOCK, 88=END_FINALLY, 89=BUILD_CLASS
    /// </summary>
    private static Models.Bytecode.Opcode MapOpcode27(byte rawOp)
    {
        return rawOp switch
        {
            70 => Models.Bytecode.Opcode.PRINT_EXPR,
            71 => Models.Bytecode.Opcode.PRINT_ITEM,
            72 => Models.Bytecode.Opcode.PRINT_NEWLINE,
            73 => Models.Bytecode.Opcode.PRINT_ITEM_TO,
            74 => Models.Bytecode.Opcode.PRINT_NEWLINE_TO,
            80 => Models.Bytecode.Opcode.BREAK_LOOP,
            84 => Models.Bytecode.Opcode.IMPORT_STAR_27,
            85 => Models.Bytecode.Opcode.EXEC_STMT,
            86 => Models.Bytecode.Opcode.YIELD_VALUE,
            87 => Models.Bytecode.Opcode.POP_BLOCK,
            88 => Models.Bytecode.Opcode.END_FINALLY,
            89 => Models.Bytecode.Opcode.BUILD_CLASS_27,
            _ => (Models.Bytecode.Opcode)rawOp,
        };
    }

    /// <summary>
    /// 检查是否为 Python 3.11+（有 CACHE 条目）
    /// </summary>
    private bool IsPython311Plus()
        => _magicBytes.Length >= 4 && _py311PlusMagicHex.Contains(
            BitConverter.ToString(_magicBytes, 0, 4).Replace("-", ""));

    /// <summary>检查是否为 Python 3.13+（操作码完全重新编号，3.13 和 3.14 编号不同）</summary>
    private bool IsPython313Plus() => _pythonMinorVersion == 13;
    /// <summary>检查是否为 Python 3.14（操作码编号与 3.13 不同，HAVE_ARGUMENT=43 vs 44）</summary>
    private bool IsPython314() => _pythonMinorVersion == 14;

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
    /// 解析 3.11+ 字节码（跳 CACHE 条目 + opcode 映射）
    /// </summary>
    private List<Instruction> ParseInstructions311Plus(byte[] bytecode)
    {
        var instructions = new List<Instruction>();
        int offset = 0;
        int extArg = 0;
        int safety = 0;

        while (offset + 1 < bytecode.Length)
        {
            if (++safety > 1000000)
                throw new InvalidOperationException(
                    $"Infinite loop in ParseInstructions311Plus at offset {offset}/{bytecode.Length}");

            byte rawOp = bytecode[offset];
            var rawArg = bytecode[offset + 1];

            // Skip cache entries (opcode 0)
            if (rawOp == 0)
            {
                offset += 2;
                continue;
            }

            // Map raw 3.11+/3.12/3.13/3.14 opcode to our unified enum
            var op = _pythonMinorVersion switch
            {
                13 => MapOpcodePy313(rawOp),
                14 => MapOpcodePy314(rawOp),
                _ => MapOpcodePy311(rawOp),
            };

            // Handle EXTENDED_ARG chain
            if (op == Models.Bytecode.Opcode.EXTENDED_ARG)
            {
                extArg = (extArg << 8) | rawArg;
                offset += 2;
                continue;
            }

            // Instructions with arguments: HAVE_ARGUMENT threshold
            // 3.12: HAVE_ARGUMENT=90; 3.13: HAVE_ARGUMENT=44; 3.14: HAVE_ARGUMENT=43
            int? arg = null;
            int haveArgThreshold = _pythonMinorVersion switch
            {
                13 => 44,
                14 => 43,
                _ => 90,
            };
            if (rawOp >= haveArgThreshold)
                arg = (extArg << 8) | rawArg;
            extArg = 0;

            // Python 3.10+ 使用 word 偏移
            if (IsWordOffsetVersion() && arg.HasValue && IsJumpInstruction311Plus(op))
                arg = arg.Value * 2;

            instructions.Add(new Instruction(offset, op, arg));

            // Advance past this instruction (2 bytes) and any cache entries
            // NOTE: don't trust the cache table — only skip actual CACHE markers (opcode=0)
            offset += 2;
            while (offset + 1 < bytecode.Length && bytecode[offset] == 0)
                offset += 2;
        }

        return instructions;
    }

    /// <summary>
    /// 将 3.11+/3.12 的原始 opcode 字节值映射到统一 Opcode 枚举。
    /// 3.11 和 3.12 许多 opcode 值与 3.10 及更早版本不同。
    /// </summary>
    private Models.Bytecode.Opcode MapOpcodePy311(byte rawOp)
    {
        // 3.12-specific: some opcodes renumbered from 3.11
        // 3.11: CALL=167, PRECALL=166, RESUME=90, POP_JUMP_IF_{TRUE,FALSE}=111/112
        // 3.12: CALL=171, no PRECALL, RESUME=151, POP_JUMP_IF_{TRUE,FALSE}=114/115
        // 3.14: uses 3.12-like numbering (RESUME=128, CALL=52)
        bool is312 = _pythonMinorVersion == 12 || (_pythonMinorVersion == 0 && _magicBytes[0] >= 0xB0);

        return rawOp switch
        {
            // --- 所有版本一致的 (3.10 和 3.11/12 值相同) ---
            1 => Models.Bytecode.Opcode.POP_TOP,
            9 => Models.Bytecode.Opcode.NOP,
            11 => Models.Bytecode.Opcode.UNARY_NEGATIVE,
            12 => Models.Bytecode.Opcode.UNARY_NOT,
            15 => Models.Bytecode.Opcode.UNARY_INVERT,
            25 => Models.Bytecode.Opcode.BINARY_SUBSCR,
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

            // --- 3.11+ 新值 (与 3.10 不同) ---
            2 => Models.Bytecode.Opcode.PUSH_NULL,
            3 => Models.Bytecode.Opcode.INTERPRETER_EXIT,
            4 => Models.Bytecode.Opcode.DUP_TOP,
            5 => Models.Bytecode.Opcode.DUP_TOP_TWO,
            99 => Models.Bytecode.Opcode.SWAP,
            120 => Models.Bytecode.Opcode.COPY,
            121 => Models.Bytecode.Opcode.RETURN_CONST,  // internal value 190
            122 => Models.Bytecode.Opcode.BINARY_OP,     // internal value 191
            123 => Models.Bytecode.Opcode.SEND,
            127 => Models.Bytecode.Opcode.LOAD_FAST_CHECK,  // internal value 193
            128 => Models.Bytecode.Opcode.POP_JUMP_IF_NOT_NONE,  // internal value 194
            129 => Models.Bytecode.Opcode.POP_JUMP_IF_NONE,     // internal value 195
            134 => Models.Bytecode.Opcode.JUMP_BACKWARD_NO_INTERRUPT,
            141 => Models.Bytecode.Opcode.LOAD_SUPER_ATTR,
            143 => Models.Bytecode.Opcode.LOAD_FAST_AND_CLEAR,  // internal value 192
            149 => Models.Bytecode.Opcode.COPY_FREE_VARS,
            172 => Models.Bytecode.Opcode.KW_NAMES,

            // --- 3.11 ↔ 3.12 有差异的值 ---
            90 when is312 => Models.Bytecode.Opcode.STORE_NAME,
            90 => Models.Bytecode.Opcode.STORE_NAME,  // Both 3.11 and 3.12: 90 = STORE_NAME
            111 when is312 => Models.Bytecode.Opcode.POP_JUMP_IF_TRUE,
            111 => Models.Bytecode.Opcode.POP_JUMP_IF_TRUE,  // 3.11: same value
            112 when is312 => Models.Bytecode.Opcode.POP_JUMP_IF_FALSE,
            112 => Models.Bytecode.Opcode.POP_JUMP_IF_FALSE,  // 3.11: same value

            // 3.12 特有的值
            20 when is312 => Models.Bytecode.Opcode.PULL_EXC_FROM_INFO_312,
            34 when is312 => Models.Bytecode.Opcode.PUSH_EXC_HANDLER_312,
            35 when is312 => Models.Bytecode.Opcode.PUSH_EXC_INFO_312,
            36 when is312 => Models.Bytecode.Opcode.CHECK_EXC_MATCH,
            37 when is312 => Models.Bytecode.Opcode.CHECK_EG_MATCH,
            // 3.10+ match/case opcodes (3.12 raw byte values)
            31 when is312 => Models.Bytecode.Opcode.MATCH_MAPPING_312,
            32 when is312 => Models.Bytecode.Opcode.MATCH_SEQUENCE_312,
            33 when is312 => Models.Bytecode.Opcode.MATCH_KEYS_312,
            152 when is312 => Models.Bytecode.Opcode.MATCH_CLASS_312,
            49 when is312 => Models.Bytecode.Opcode.WITH_EXCEPT_START_312,
            53 when is312 => Models.Bytecode.Opcode.BEFORE_WITH_312,
            114 when is312 => Models.Bytecode.Opcode.POP_JUMP_IF_FALSE,
            115 when is312 => Models.Bytecode.Opcode.POP_JUMP_IF_TRUE,
            151 when is312 => Models.Bytecode.Opcode.RESUME,
            156 when is312 => Models.Bytecode.Opcode.BUILD_CONST_KEY_MAP,
            162 when is312 => Models.Bytecode.Opcode.LIST_EXTEND,
            163 when is312 => Models.Bytecode.Opcode.SET_UPDATE,
            164 when is312 => Models.Bytecode.Opcode.DICT_MERGE,
            165 when is312 => Models.Bytecode.Opcode.DICT_UPDATE,
            171 when is312 => Models.Bytecode.Opcode.CALL,
            173 when is312 => Models.Bytecode.Opcode.CALL_INTRINSIC_1,
            174 when is312 => Models.Bytecode.Opcode.CALL_INTRINSIC_2,
            175 when is312 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_GLOBALS,
            176 when is312 => Models.Bytecode.Opcode.LOAD_FROM_DICT_OR_DEREF,

            // 3.11 特有的值
            166 when !is312 => Models.Bytecode.Opcode.PRECALL_311,
            167 when !is312 => Models.Bytecode.Opcode.CALL_311,

            // 3.11: POP_JUMP_IF_* at same values as 3.12 naming
            114 when !is312 => Models.Bytecode.Opcode.STORE_NAME,   // 3.11: 114 is different
            115 when !is312 => Models.Bytecode.Opcode.DELETE_NAME,  // 3.11: 115 is different

            // Fallback: treat as raw value (some may be 3.12-specific that we haven't mapped)
            _ => (Models.Bytecode.Opcode)rawOp,
        };
    }

    /// <summary>
    /// 将 Python 3.13+ 的原始 opcode 字节值映射到统一 Opcode 枚举。
    /// 3.13 的操作码编号体系与 3.12 完全不同（HAVE_ARGUMENT=44, 插入/删除了多个操作码）。
    /// 完整映射表来源于 CPython 3.13 Lib/opcode.py opname[]。
    /// </summary>
    private Models.Bytecode.Opcode MapOpcodePy313(byte rawOp)
    {
        return rawOp switch
        {
            // 3.13 opname 完整映射（raw byte → Opcode enum）
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
            33 => Models.Bytecode.Opcode.PUSH_EXC_INFO,      // → PUSH_EXC_INFO_312=179
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
            44 => Models.Bytecode.Opcode.WITH_EXCEPT_START,  // → WITH_EXCEPT_START_312=188
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
            96 => Models.Bytecode.Opcode.MATCH_CLASS_313,        // → MATCH_CLASS_312=183
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
    /// 3.11+ 跳转指令检测（含 JUMP_BACKWARD）。
    /// 3.14 新增：JUMP_IF_FALSE/TRUE（伪指令）、POP_ITER（结束循环）。
    /// </summary>
    private static bool IsJumpInstruction311Plus(Opcode op) => op switch
    {
        Opcode.JUMP_FORWARD or Opcode.JUMP_BACKWARD
            or Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
            or Opcode.POP_JUMP_IF_NOT_NONE or Opcode.POP_JUMP_IF_NONE
            or Opcode.FOR_ITER or Opcode.JUMP_BACKWARD_NO_INTERRUPT
            or Opcode.JUMP_ABSOLUTE or Opcode.JUMP_IF_TRUE_OR_POP
            or Opcode.JUMP_IF_FALSE_OR_POP or Opcode.TO_BOOL_313
            or Opcode.POP_ITER_314
            or Opcode.SEND => true,
        _ => false
    };

    /// <summary>
    /// 3.11+ 的缓存条目数。
    /// 3.11, 3.12, 3.13, 3.14 的缓存配置完全不同：
    /// - 3.11: 自适应字节码初期，只有部分 opcode 有 cache（未特化的 opcode 无 cache）
    /// - 3.12: 所有 opcode 从初始就有固定 cache 条目
    /// - 3.13: 操作码重新编号，cache 配置对应新的 raw byte 值
    /// - 3.14: HAVE_ARGUMENT=43, cache 配置重新设计
    /// </summary>
    private int GetCacheCount311Plus(byte rawOp)
    {
        if (IsPython314())
            return GetCacheCount314(rawOp);
        if (IsPython313Plus())
            return GetCacheCount313(rawOp);
        bool is312 = _pythonMinorVersion == 12 || _magicBytes[0] >= 0xB0;
        if (is312)
            return GetCacheCount312(rawOp);
        else
            return GetCacheCount311(rawOp);
    }

    /// <summary>
    /// 3.11 的缓存条目数（从实际字节码观察得到）。
    /// 关键差异：LOAD_NAME/LOAD_CONST/STORE_NAME 等基础操作码无 cache。
    /// </summary>
    private static int GetCacheCount311(byte rawOp)
    {
        return rawOp switch
        {
            1 => 0, 2 => 0, 4 => 0, 5 => 0, 9 => 0,
            11 => 0, 12 => 0, 15 => 0,
            25 => 0, 30 => 0, 31 => 0,
            35 => 0, 36 => 0, 37 => 0,
            40 => 0, 41 => 0, 42 => 0, 43 => 0, 47 => 0,
            49 => 0, 53 => 0,
            55 => 0, 56 => 0, 60 => 0, 61 => 0,
            68 => 0, 69 => 0, 71 => 0, 72 => 0, 73 => 0, 74 => 0, 75 => 0,
            79 => 0, 80 => 0, 81 => 0, 83 => 0, 84 => 0, 85 => 0, 86 => 0,
            87 => 0, 88 => 0, 89 => 0,
            90 => 0, 91 => 0, 92 => 1,  // UNPACK_SEQUENCE
            93 => 0, 94 => 0, 95 => 0, 96 => 0, 97 => 0, 98 => 0, 99 => 0,
            100 => 0, // LOAD_CONST (no cache in 3.11)
            101 => 0, // LOAD_NAME (no cache in 3.11)
            102 => 0, 103 => 0, 104 => 0, 105 => 0,
            106 => 0, // LOAD_ATTR (no cache in 3.11)
            107 => 2, // COMPARE_OP
            108 => 0, 109 => 0, 110 => 0,
            111 => 0, 112 => 0, 113 => 0, 114 => 0, 115 => 0,
            116 => 0, // LOAD_GLOBAL (no cache in 3.11)
            117 => 0, 118 => 0, 119 => 0,
            120 => 0, 121 => 0, 122 => 1,  // BINARY_OP
            123 => 1,  // UNARY_OP
            124 => 0, 125 => 0, 126 => 0, 127 => 0,
            128 => 0, 129 => 0, 130 => 0, 131 => 0, 132 => 0, 133 => 0,
            134 => 0, 135 => 0, 136 => 0, 137 => 0, 138 => 0, 139 => 0,
            140 => 0, 141 => 0, 142 => 0, 143 => 0,
            144 => 0, 145 => 0, 146 => 0, 147 => 0,
            149 => 0,
            150 => 0, 151 => 0, 152 => 0,
            155 => 0, 156 => 0, 157 => 0,
            162 => 0, 163 => 0, 164 => 0, 165 => 0,
            166 => 0, // PRECALL_311 (doesn't appear in bytecodes, but safe)
            167 => 0, // CALL_311
            170 => 0,
            171 => 4, // CALL
            172 => 0, 173 => 0, 174 => 0, 175 => 0, 176 => 0,
            _ => 0,
        };
    }

    /// <summary>
    /// 3.12 的缓存条目数（完整 cache 表）。
    /// </summary>
    private static int GetCacheCount312(byte rawOp)
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
    /// 3.13+ 的缓存条目数（CPython 3.13 Lib/opcode.py _inline_cache_entries）。
    /// 注意：使用 3.13 的原始操作码字节值，因为 3.13 的操作码编号体系与 3.12 完全不同。
    /// </summary>
    private static int GetCacheCount313(byte rawOp)
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
    /// 3.14 的缓存条目数（CPython 3.14 Lib/opcode.py _cache_format）。
    /// 使用 3.14 原始操作码字节值，因为 3.14 的操作码编号与 3.13 完全不同。
    /// </summary>
    private static int GetCacheCount314(byte rawOp)
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
    /// 将 Python 3.14 的原始 opcode 字节值映射到统一 Opcode 枚举。
    /// 3.14 的操作码编号体系与 3.13 完全不同（HAVE_ARGUMENT=43 vs 44）。
    /// 完整映射表来源于 CPython 3.14 Lib/opcode.py opname[]。
    /// 仅映射通用操作码（super-instruction 如 CALL_PY_EXACT_ARGS 等不映射——通常不会出现在
    /// py_compile 生成的字节码中，直接以原始字节值 fallback 为 Opcode 枚举）。
    /// </summary>
    private Models.Bytecode.Opcode MapOpcodePy314(byte rawOp)
    {
        return rawOp switch
        {
            // --- 无参操作码 (0-42, HAVE_ARGUMENT=43) ---
            0 => Models.Bytecode.Opcode.NOP,                  // CACHE → NOP（CACHE 已在前端跳过）
            1 => Models.Bytecode.Opcode.BINARY_SLICE_313,     // BINARY_SLICE
            2 => Models.Bytecode.Opcode.BEFORE_WITH_313,      // BUILD_TEMPLATE → BEFORE_WITH
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
            43 => Models.Bytecode.Opcode.WITH_EXCEPT_START,   // → WITH_EXCEPT_START_312=188
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
    /// 解析 3.10 及更早的字节码（无 CACHE）
    /// </summary>
    private List<Instruction> ParseInstructionsWordcode(byte[] bytecode)
    {
        var instructions = new List<Instruction>();
        int offset = 0;
        int extArg = 0;
        int safety = 0;

        while (offset + 1 < bytecode.Length)
        {
            if (++safety > 1000000)
                throw new InvalidOperationException(
                    $"Infinite loop in ParseInstructionsWordcode at offset {offset}/{bytecode.Length}");
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
        var result = new List<string>();
        try
        {
            var rawType = br.ReadByte();
            var type = (byte)(rawType & ~MarshalType.TYPE_FLAG_REF);

            if (type == MarshalType.TYPE_REF)
            {
                var idx = br.ReadInt32();
                if (idx >= 0 && idx < _refList.Count && _refList[idx] is List<string> cached)
                    return cached;
                return result;
            }

            // Container (tuple) FLAG_REF: reserve ref slot + fill after reading elements
            bool containerHasRef = (rawType & MarshalType.TYPE_FLAG_REF) != 0;
            int containerRefIdx = -1;
            if (containerHasRef)
            {
                containerRefIdx = _refList.Count;
                _refList.Add(null);
            }

            int count;
            if (type == MarshalType.TYPE_SMALL_TUPLE)
                count = br.ReadByte();
            else if (type == MarshalType.TYPE_TUPLE)
                count = br.ReadInt32();
            else
            {
                // Single string (non-tuple)
                // Handle 0x73 (TYPE_STRING) directly to avoid TYPE_CODE_SIMPLE confusion.
                // For other types, use ReadMarshalObject for correct ref list alignment.
                var str = ReadOneMarshalString(br, rawType);
                if (str != null) result.Add(str);
                return result;
            }

            for (int i = 0; i < count; i++)
            {
                if (i >= 10000)
                {
                    Console.Error.WriteLine($"[WARN] ReadMarshalObjectAsStrList: aborting at {i} items (safety limit)");
                    break;
                }
                // Peek: if TYPE_STRING(0x73), read directly; else use ReadMarshalObject
                var peek = br.ReadByte();
                br.BaseStream.Position--;
                var peekType = (byte)(peek & ~MarshalType.TYPE_FLAG_REF);

                string? str;
                if (peekType == MarshalType.TYPE_STRING)
                {
                    // 0x73 = TYPE_STRING in names context, NOT TYPE_CODE_SIMPLE
                    str = ReadOneMarshalString(br, null);
                }
                else
                {
                    // For all other types, use ReadMarshalObject for correct ref list
                    var obj = ReadMarshalObject(br);
                    str = obj?.ToString();
                }
                if (str != null) result.Add(str);
            }
            
            // Fill container ref slot
            if (containerRefIdx >= 0)
                _refList[containerRefIdx] = result;
        }
        catch (Exception ex) { LogCatch(br, "ReadMarshalObjectAsStrList", ex); }
        return result;
    }

    /// <summary>
    /// 读取单个 marshal 字符串值，保持 ref list 对齐。
    /// 处理 0x73 为 TYPE_STRING（非 TYPE_CODE_SIMPLE）。
    /// 不通过 ReadMarshalValue dispatch，避免 0x73 误判。
    /// </summary>
    private string? ReadOneMarshalString(BinaryReader br, byte? preReadRawType)
    {
        byte rawType;
        if (preReadRawType.HasValue)
            rawType = preReadRawType.Value;
        else
            rawType = br.ReadByte();

        var type = (byte)(rawType & ~MarshalType.TYPE_FLAG_REF);

        // TYPE_REF: lookup in ref list
        if (type == MarshalType.TYPE_REF)
        {
            var refIdx = br.ReadInt32();
            if (refIdx >= 0 && refIdx < _refList.Count && _refList[refIdx] is string refStr)
                return refStr;
            return null;
        }

        // For FLAG_REF strings: reserve ref slot BEFORE reading (like ReadMarshalObject)
        bool hasRef = (rawType & MarshalType.TYPE_FLAG_REF) != 0;
        int flagRefIdx = -1;
        if (hasRef)
        {
            flagRefIdx = _refList.Count;
            _refList.Add(null);
        }

        string? result = type switch
        {
            MarshalType.TYPE_STRING => ReadLongString(br),
            MarshalType.TYPE_SHORT_ASCII => ReadShortString(br),
            MarshalType.TYPE_SHORT_ASCII_INTERNED => ReadShortString(br),
            MarshalType.TYPE_ASCII => ReadLongString(br),
            MarshalType.TYPE_ASCII_INTERNED => ReadLongString(br),
            MarshalType.TYPE_UNICODE => ReadLongString(br),
            _ => null,
        };

        if (flagRefIdx >= 0 && result != null)
            _refList[flagRefIdx] = result;

        return result;
    }

    /// <summary>
    /// 读取一个 marshal 字符串值。
    /// 不通过 ReadMarshalValue（避免 TYPE_STRING 0x73 与 TYPE_CODE_SIMPLE 混淆）。
    /// 如果 preReadType 不为 null，表示类型字节已读。
    /// </summary>
    private string? ReadMarshalStringValue(BinaryReader br, byte? preReadType = null)
    {
        try
        {
            byte rawType;
            if (preReadType.HasValue)
                rawType = preReadType.Value;
            else
                rawType = br.ReadByte();

            var type = (byte)(rawType & ~MarshalType.TYPE_FLAG_REF);
            bool hasRef = (rawType & MarshalType.TYPE_FLAG_REF) != 0;
            
            // TYPE_REF (0x72) — reference to a previously stored string
            if (type == MarshalType.TYPE_REF)
            {
                var refIdx = br.ReadInt32();
                if (refIdx >= 0 && refIdx < _refList.Count && _refList[refIdx] is string refStr)
                    return refStr;
                return null;
            }
            
            // If FLAG_REF is set, pre-reserve a ref list slot (like ReadMarshalObject does)
            // so later TYPE_REF references find the correct entry.
            int flagRefIdx = -1;
            if (hasRef)
            {
                flagRefIdx = _refList.Count;
                _refList.Add(null);
            }
            
            string? result = type switch
            {
                MarshalType.TYPE_STRING => ReadLongString(br),
                MarshalType.TYPE_SHORT_ASCII => ReadShortString(br),
                MarshalType.TYPE_SHORT_ASCII_INTERNED => ReadShortString(br),
                MarshalType.TYPE_ASCII => ReadLongString(br),
                MarshalType.TYPE_ASCII_INTERNED => ReadLongString(br),
                MarshalType.TYPE_UNICODE => ReadLongString(br),
                _ => null,
            };
            
            // Fill the reserved ref slot with the actual string value
            if (flagRefIdx >= 0 && result != null)
            {
                _refList[flagRefIdx] = result;
            }
            
            return result;
        }
        catch (Exception ex) { LogCatch(br, "ReadMarshalStringValue", ex); return null; }
    }

    private string ReadShortString(BinaryReader br)
    {
        var len = br.ReadByte();
        return Encoding.UTF8.GetString(br.ReadBytes(len));
    }

    private string ReadLongString(BinaryReader br)
    {
        var len = br.ReadInt32();
        return Encoding.UTF8.GetString(br.ReadBytes(len));
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

    private List<object?> ReadMarshalList(BinaryReader br, bool typeByteRead = false, bool forceList = false)
    {
        int count;
        bool isTuple;
        
        if (!typeByteRead)
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

            if (type == MarshalType.TYPE_SMALL_TUPLE)
                count = br.ReadByte();
            else
                count = br.ReadInt32();

            isTuple = (type == MarshalType.TYPE_TUPLE || type == MarshalType.TYPE_SMALL_TUPLE);
        }
        else
        {
            // type byte already consumed by ReadMarshalValue — read count directly
            count = br.ReadInt32();
            isTuple = !forceList;  // default tuple, forceList → false
        }
        var items = isTuple ? new PyTuple() : new List<object?>();
        for (int i = 0; i < count; i++)
        {
            CheckReadTimeout(br);
            if (i >= 10000)
            {
                LogCatch($"ReadMarshalList.count={count}", new InvalidOperationException($"Safety limit 10000 hit at item {i}"));
                break;
            }
            try
            {
                items.Add(ReadMarshalObject(br));
            }
            catch (Exception ex)
            {
                LogCatch(br, $"ReadMarshalList.item[{i}]", ex);
                items.Add(null);
            }
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

    /// <summary>
    /// 读取 Python marshal TYPE_DICT (0x7B = '{')。
    /// 格式：key-value 对 + TYPE_NONE 终止符。
    /// 类型字节已被 ReadMarshalValue 消费，只需读 key-value 对。
    /// </summary>
    private Dictionary<object?, object?> ReadMarshalDictObject(BinaryReader br)
    {
        var dict = new Dictionary<object?, object?>();
        try
        {
            int maxEntries = 100000;
            int entries = 0;
            while (br.BaseStream.Position < br.BaseStream.Length)
            {
                CheckReadTimeout(br);
                if (++entries > maxEntries)
                    throw new InvalidOperationException(
                        $"Infinite loop in dictionary reading at offset {br.BaseStream.Position}. " +
                        $"Last key: {dict.Keys.LastOrDefault()}");
                // PEEK next type byte
                var peekByte = br.ReadByte();
                br.BaseStream.Position--; // unread

                if ((peekByte & ~MarshalType.TYPE_FLAG_REF) == MarshalType.TYPE_NONE)
                {
                    br.ReadByte(); // consume TYPE_NONE
                    break;
                }

                var key = ReadMarshalObject(br);
                var val = ReadMarshalObject(br);
                if (key != null)
                    dict[key] = val;
            }
        }
        catch (Exception ex) { LogCatch(br, "ReadMarshalDictObject", ex); }
        return dict;
    }

    private object? ReadMarshalObject(BinaryReader br)
    {
        CheckReadTimeout(br);
        if (++_marshalCalls > MaxMarshalCalls)
            throw new InvalidOperationException(
                $"Marshal calls exceeded {MaxMarshalCalls} at offset {br.BaseStream.Position}. " +
                "Possible infinite loop in marshal parsing.");
        if (++_marshalDepth > MaxMarshalDepth)
            throw new InvalidOperationException(
                $"Marshal recursion depth exceeded {MaxMarshalDepth} at offset {br.BaseStream.Position}. " +
                "Possible infinite loop in .pyc reading.");
        
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
            MarshalType.TYPE_BINARY_COMPLEX => new double[] { br.ReadDouble(), br.ReadDouble() },
            MarshalType.TYPE_BYTES => ReadMarshalBytesDirect(br),
            // 115 = TYPE_STRING — 永远是 bytes 对象（CPython 中所有代码对象都用 TYPE_CODE 'c'）
            MarshalType.TYPE_STRING => ReadMarshalBytesDirect(br),
            MarshalType.TYPE_SHORT_ASCII => ReadMarshalShortString(br),
            MarshalType.TYPE_SHORT_ASCII_INTERNED => ReadMarshalShortString(br),
            MarshalType.TYPE_ASCII => ReadMarshalLongString(br),
            MarshalType.TYPE_ASCII_INTERNED => ReadMarshalLongString(br),
            MarshalType.TYPE_UNICODE => ReadMarshalLongString(br),
            MarshalType.TYPE_SMALL_TUPLE => ReadSmallTuple(br),
            MarshalType.TYPE_TUPLE => ReadMarshalList(br, typeByteRead: true),
            MarshalType.TYPE_LIST => ReadMarshalList(br, typeByteRead: true, forceList: true),
            MarshalType.TYPE_DICT => ReadMarshalDictObject(br),
            MarshalType.TYPE_CODE => ReadMarshalCodeObject(br, isSimple: false),
            MarshalType.TYPE_TRUE => true,
            MarshalType.TYPE_FALSE => false,
            MarshalType.TYPE_ELLIPSIS => new object(),
            MarshalType.TYPE_REF => ReadRef(br),
            MarshalType.TYPE_SET => ReadMarshalSetOrFrozenset(br),
            MarshalType.TYPE_FROZENSET => ReadMarshalSetOrFrozenset(br),
            _ => HandleUnknownMarshalType(br, type),
        };
    }

    private object? HandleUnknownMarshalType(BinaryReader br, byte type)
    {
        // If the type byte is very small (< 4), it's likely padding or
        // a non-marshal byte between fields. Don't skip any data.
        if (type < 4)
            return null;
        
        // Try to skip: assume it's a value with a 4-byte length prefix
        try
        {
            if (br.BaseStream.Position < br.BaseStream.Length)
            {
                var length = Math.Min(br.ReadInt32(), br.BaseStream.Length - br.BaseStream.Position);
                br.BaseStream.Position += length;
            }
        }
        catch (Exception ex) { LogCatch(br, $"HandleUnknownMarshalType type=0x{type:X2}", ex); }
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

    /// <summary>
    /// 从 marshal 流中读取原始字节数据。
    /// 支持 TYPE_STRING, TYPE_SHORT_ASCII, TYPE_SHORT_ASCII_INTERNED,
    /// TYPE_ASCII, TYPE_ASCII_INTERNED, TYPE_UNICODE。
    /// </summary>
    private byte[]? ReadRawMarshalBytes(BinaryReader br)
    {
        var rawType = br.ReadByte();
        var type = (byte)(rawType & ~MarshalType.TYPE_FLAG_REF);

        // FLAG_REF: reserve ref list slot (matching CPython's r_object behavior)
        bool hasRef = (rawType & MarshalType.TYPE_FLAG_REF) != 0;
        int refIdx = -1;
        if (hasRef)
        {
            refIdx = _refList.Count;
            _refList.Add(null);
        }

        byte[]? result = type switch
        {
            MarshalType.TYPE_SHORT_ASCII_INTERNED or MarshalType.TYPE_SHORT_ASCII
                => ReadShortStringBytes(br),
            MarshalType.TYPE_ASCII_INTERNED or MarshalType.TYPE_ASCII
                or MarshalType.TYPE_STRING or MarshalType.TYPE_UNICODE
                or 116
                => ReadLongStringBytes(br),
            MarshalType.TYPE_BYTES => ReadLongStringBytes(br),
            MarshalType.TYPE_REF => ReadRefAndReturnBytes(br),
            _ => null,
        };

        if (refIdx >= 0 && result != null)
            _refList[refIdx] = result;

        return result;
    }

    private byte[] ReadShortStringBytes(BinaryReader br)
    {
        var len = br.ReadByte();
        return br.ReadBytes(len);
    }

    /// <summary>
    /// 读取 TYPE_REF (0x72) + 4字节索引，从 ref list 中获取已存储的字节数组。
    /// 3.11+ 的 localspluskinds/linetable/exceptiontable 可能用 TYPE_REF 引用已存储数据。
    /// </summary>
    private byte[]? ReadRefAndReturnBytes(BinaryReader br)
    {
        var idx = br.ReadInt32();
        if (idx >= 0 && idx < _refList.Count)
        {
            if (_refList[idx] is byte[] bytes)
                return bytes;
            if (_refList[idx] is string str)
                return System.Text.Encoding.ASCII.GetBytes(str);
        }
        return null;
    }

    private byte[] ReadLongStringBytes(BinaryReader br)
    {
        var len = br.ReadInt32();
        // 防止过读：如果 len 超过文件剩余字节，只读取到文件末尾
        long remaining = br.BaseStream.Length - br.BaseStream.Position;
        if (len > remaining)
            len = (int)Math.Max(0, remaining);
        return br.ReadBytes(len);
    }

    private PyTuple ReadSmallTuple(BinaryReader br)
    {
        var count = br.ReadByte();
        var items = new PyTuple();
        for (int i = 0; i < count; i++)
        {
            if (i >= 10000)
            {
                LogCatch($"ReadSmallTuple.count={count}", new InvalidOperationException($"Safety limit 10000 hit at item {i}"));
                break;
            }
            try
            {
                items.Add(ReadMarshalObject(br));
            }
            catch (Exception ex)
            {
                LogCatch(br, $"ReadSmallTuple.item[{i}]", ex);
                items.Add(null);
            }
        }
        return items;
    }

    private Dictionary<int, int> ParseLineNumberTable(byte[] lnotab, List<Instruction> instructions, bool isLinetable = false)
    {
        if (isLinetable)
            return ParseLinetable311(lnotab);
        
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
    /// 解析 Python 3.11+ co_linetable（PEP 626 格式）。
    /// 使用 Python 的 co_lines() 语义提取 (start_offset, line) 映射。
    /// </summary>
    private Dictionary<int, int> ParseLinetable311(byte[] data)
    {
        var table = new Dictionary<int, int>();
        int line = 1;
        int start = 0;
        int i = 0;
        while (i < data.Length)
        {
            int code = (data[i] >> 6) & 3;
            switch (code)
            {
                case 0: // short: 1-3 bytes
                    if (i + 1 >= data.Length) return table;
                    int lineDeltaShort = (data[i] >> 2) & 0xF;
                    int endDeltaShort = ((data[i] & 3) << 2) | (data[i + 1] & 3);
                    line += lineDeltaShort;
                    start += endDeltaShort;
                    i += 2;
                    break;
                case 1: // medium: 3 bytes
                    if (i + 2 >= data.Length) return table;
                    int lineDeltaMed = ((data[i] & 0x3F) << 2) | ((data[i + 1] >> 6) & 3);
                    int endDeltaMed = data[i + 1] & 0x3F;
                    line += (sbyte)(lineDeltaMed > 31 ? lineDeltaMed - 64 : lineDeltaMed);
                    start += endDeltaMed;
                    i += 3;
                    break;
                case 2: // long: 4+ bytes
                    if (i + 3 >= data.Length) return table;
                    int lineDeltaLong = data[i] & 0x3F;
                    int column = data[i + 2];
                    int endDeltaLong = data[i + 3];
                    line += (sbyte)(lineDeltaLong > 31 ? lineDeltaLong - 64 : lineDeltaLong);
                    start += endDeltaLong;
                    i += 4;
                    break;
                case 3: // sentinel
                    int entryCode = (data[i] >> 3) & 7;
                    switch (entryCode)
                    {
                        case 0: break; // end of entries
                        case 1: // simple no-line entry (skip)
                            i += 2;
                            continue;
                        default:
                            // skip 2 bytes per entry code 3+ 
                            i += 2;
                            continue;
                    }
                    return table;
            }
            table[start] = line;
        }
        return table;
    }

    /// <summary>
    /// 解析 3.13+ 异常表（变长 6-bit 编码，每条记录 4 个字段）。
    /// 3.12 及更早使用固定 8 字节/条目的格式。
    /// </summary>
    private List<ExceptionTableEntry> ParseExceptionTable(byte[] data)
    {
        // 3.13+ exception table uses variable-length 6-bit encoding
        if (_pythonMinorVersion == 13)
            return ParseExceptionTable313(data);
        return ParseExceptionTable312(data);
    }

    /// <summary>
    /// 3.12 及更早：固定 8 字节/条目的异常表格式。
    /// 每条：start(u16)*2, end(u16)*2, target(u16)*2, depth|lasti(u16)。
    /// </summary>
    private List<ExceptionTableEntry> ParseExceptionTable312(byte[] data)
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

    /// <summary>
    /// 3.13+ 异常表：变长 6-bit/字节编码。
    /// 每条记录 4 个字段：start, size(end-start), target, depth_lasti。
    /// 每个字段用变长编码，6 位数据/字节，bit7=延续标记。
    /// 所有偏移都是 WORD 偏移（字节偏移/2）。
    /// </summary>
    private List<ExceptionTableEntry> ParseExceptionTable313(byte[] data)
    {
        var entries = new List<ExceptionTableEntry>();
        int i = 0;
        while (i < data.Length)
        {
            if (i + 1 >= data.Length) break; // need at least start + size
            
            // Read 4 variable-length fields
            int start = ReadBase128_6bit(data, ref i);
            int size = ReadBase128_6bit(data, ref i);
            int target = ReadBase128_6bit(data, ref i);
            int depthLasti = ReadBase128_6bit(data, ref i);

            if (i > data.Length) break; // overflow guard

            int end = start + size;
            int depth = (depthLasti >> 1) & 0x3;
            bool lasti = (depthLasti & 1) != 0;

            entries.Add(new ExceptionTableEntry
            {
                StartOffset = start * 2,
                EndOffset = end * 2,
                TargetOffset = target * 2,
                Depth = depth,
                Lasti = lasti
            });
        }
        return entries;
    }

    /// <summary>
    /// 读取变长 6-bit 编码的值。每字节：bits 0-5=数据，bit7=延续标记（1=还有后续字节）。
    /// 数据以高 6 位在前、低 6 位在后的顺序存储。
    /// </summary>
    private static int ReadBase128_6bit(byte[] data, ref int offset)
    {
        int value = 0;
        while (offset < data.Length)
        {
            byte b = data[offset++];
            value = (value << 6) | (b & 0x3f);
            if ((b & 0x80) == 0)
                break;
            if ((value >> 30) != 0) break; // safety: prevent overflow
        }
        return value;
    }
}
