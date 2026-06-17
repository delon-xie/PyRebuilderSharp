using System.Text;
using PyRebuilderSharp.Core.Versioning;
using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Readers;

/// <summary>
/// .pyc文件读取器。
/// 负责解析Python编译后的字节码文件。
/// </summary>
public class PycReader
{
    /// <summary>版本策略——封装当前 .pyc 版本的所有格式差异。</summary>
    private IVersionStrategy _strategy = null!;

    private readonly List<object?> _refList = new();
    private readonly List<string> _internedStrings27 = new(); // Python 2.7 interned string table
    private byte[] _magicBytes = Array.Empty<byte>();
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
    /// 读取.pyc文件并解析为CodeObject。
    /// </summary>
    public CodeObject Read(byte[] data)
    {
        using var ms = new MemoryStream(data);
        using var br = new BinaryReader(ms);
        
        _marshalDepth = 0;
        _marshalCalls = 0;
        _readTimer = System.Diagnostics.Stopwatch.StartNew();
        
        // Step 1: 验证Magic Number → 创建版本策略
        var magic = br.ReadBytes(4);
        _magicBytes = magic;
        _strategy = VersionStrategyFactory.Create(magic);

        // Step 2: 读取头部信息
        if (_strategy.Version == PythonVersion.Py27)
        {
            // Python 2.7 header: magic(4) + timestamp(4) = 8 bytes, no flags/size
            var ts = br.ReadInt32(); // timestamp (unused)
            // 2.7 marshal data starts at offset 8
        }
        else if (!_strategy.HasPep552Header)
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
    /// 读取Marshal格式的CodeObject。
    /// </summary>
    private CodeObject ReadMarshalCodeObject(BinaryReader br, bool isSimple = false)
    {
        var code = new CodeObject();

        // 设置版本信息
        code.Version = _strategy.Version;
        code.IsPython38Plus = _strategy.HasPosOnlyArgCount;
        code.IsWordOffset = _strategy.IsWordOffset;

        try
        {
            if (_strategy.Version == PythonVersion.Py27)
                return ReadMarshalCodeObject27(br);

            // 读取CodeObject的各个字段
            code.ArgCount = br.ReadInt32();
            if (_strategy.HasCaches && !isSimple)
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
            else if (_strategy.HasPosOnlyArgCount && !isSimple)
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
            if (_strategy.HasCaches)
            {
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
            if (_strategy.UseLocalsPlus)
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
            if (_strategy.HasQualname)
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
            if (_strategy.HasCaches)
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
                code.HasLinetable = _strategy.HasLinetable;
                code.LineNumberTable = ParseLineNumberTable(lnotab, code.Instructions, _strategy.HasLinetable);
            }

            // co_exceptiontable（3.11+ 的所有代码对象都有）
            if (_strategy.HasExceptionTable && br.BaseStream.Position < br.BaseStream.Length)
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
        code.Version = PythonVersion.Py27;
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
        if (_strategy.Version == PythonVersion.Py27)
            return ParseInstructionsPre36(bytecode);
        if (_strategy.HasCaches)
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
            var op = _strategy.MapOpcode(rawOp);
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

            // Map raw opcode to our unified enum via version strategy
            var op = _strategy.MapOpcode(rawOp);

            // Handle EXTENDED_ARG chain
            if (op == Models.Bytecode.Opcode.EXTENDED_ARG)
            {
                extArg = (extArg << 8) | rawArg;
                offset += 2;
                continue;
            }

            // Instructions with arguments: HAVE_ARGUMENT threshold
            int? arg = null;
            if (rawOp >= _strategy.HaveArgument)
                arg = (extArg << 8) | rawArg;
            extArg = 0;

            // Python 3.10+ 使用 word 偏移
            if (_strategy.IsWordOffset && arg.HasValue && _strategy.IsJumpInstruction(op))
                arg = arg.Value * 2;

            // Python 3.12+ wordcode: LOAD_GLOBAL 编码 (name_idx << 1) | push_null
            // 需要提取实际的 name index: arg >> 1
            if (_strategy.HasCaches && arg.HasValue && op == Models.Bytecode.Opcode.LOAD_GLOBAL
                && (arg.Value & 1) != 0)  // push_null bit set
            {
                arg = arg.Value >> 1;
            }

            // Python 3.12+ wordcode: LOAD_ATTR 编码 (name_idx << 1) | self_or_null
            // 始终需要 >> 1 提取真实 name index
            if (_strategy.HasCaches && arg.HasValue
                && op is Models.Bytecode.Opcode.LOAD_ATTR or Models.Bytecode.Opcode.LOAD_SUPER_ATTR)
            {
                arg = arg.Value >> 1;
            }

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
            if (_strategy.IsWordOffset && arg.HasValue && _strategy.IsJumpInstruction(op))
                arg = arg.Value * 2;

            instructions.Add(new Instruction(offset, op, arg));
            offset += 2;
        }

        return instructions;
    }

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
                if (idx >= 0 && idx < _refList.Count)
                {
                    if (_refList[idx] is List<string> cached)
                        return cached;
                    if (_refList[idx] is List<object?> objList)
                        return objList.Where(x => x != null).Select(x => x.ToString() ?? "").ToList();
                }
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

    /// <summary>
    /// 读取 TYPE_SLICE (0x2D) 对象 — start, stop, step 三个 marshal 对象。
    /// </summary>
    private object? ReadMarshalSlice(BinaryReader br)
    {
        ReadMarshalObject(br);
        ReadMarshalObject(br);
        ReadMarshalObject(br);
        return null;
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
        if (_strategy.HasPosOnlyArgCount)
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
            MarshalType.TYPE_SLICE => ReadMarshalSlice(br),
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
        // 3.11+ 异常表：统一使用变长 base-64 varint 编码（bit6=延续标记）
        // 适用于 3.11, 3.12, 3.13, 3.14
        return ParseExceptionTableVarint(data);
    }

    /// <summary>
    /// 3.11+ 异常表：变长 6-bit/字节编码（base-64 varint）。
    /// CPython 3.11+ 统一使用此格式。见 Lib/dis.py → _parse_varint：
    ///   val = byte & 63 (6 bits data)
    ///   while byte & 64: (bit 6 = continuation)
    ///       val <<= 6; val |= next_byte & 63
    /// 每条 4 个字段：start(word), size(word), target(word), depth_lasti
    /// 所有偏移都是 WORD 偏移（字节偏移/2），读取后 *2。
    /// depth = dl >> 1, lasti = dl & 1
    /// </summary>
    private List<ExceptionTableEntry> ParseExceptionTableVarint(byte[] data)
    {
        var entries = new List<ExceptionTableEntry>();
        int i = 0;
        while (i < data.Length)
        {
            // Read 4 variable-length fields (base-64, bit-6 continuation)
            int start = ReadExceptionTableVarint(data, ref i);
            int size = ReadExceptionTableVarint(data, ref i);
            int target = ReadExceptionTableVarint(data, ref i);
            int depthLasti = ReadExceptionTableVarint(data, ref i);

            if (i > data.Length) break; // overflow guard

            int end = start + size;
            int depth = depthLasti >> 1;
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
    /// 读取异常表的变长字段：6 位数据/字节，bit6=延续标记。
    /// 大端序（高位在前）。对应 CPython 的 _parse_varint。
    /// </summary>
    private static int ReadExceptionTableVarint(byte[] data, ref int offset)
    {
        if (offset >= data.Length) throw new IndexOutOfRangeException();
        int value = data[offset++] & 0x3f; // bits 0-5 = first 6 bits
        while (offset < data.Length && (data[offset - 1] & 0x40) != 0)
        {
            value = (value << 6) | (data[offset] & 0x3f);
            offset++;
        }
        return value;
    }
}
