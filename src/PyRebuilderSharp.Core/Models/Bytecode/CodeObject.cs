using PyRebuilderSharp.Core.Versioning;

namespace PyRebuilderSharp.Core.Models.Bytecode;

/// <summary>
/// Python代码对象，对应CPython的PyCodeObject。
/// </summary>
public class CodeObject
{
    // ---- 标识信息 ----
    public string Name { get; set; } = "<module>";
    public string QualifiedName { get; set; } = "";
    public string Filename { get; set; } = "<unknown>";
    public int FirstLineNumber { get; set; } = 1;

    // ---- 字节码 ----
    public List<Instruction> Instructions { get; set; } = new();

    // ---- 常量表 ----
    public Dictionary<int, object?> Constants { get; set; } = new();

    // ---- 符号表 ----
    public List<string> Names { get; set; } = new();
    public List<string> Varnames { get; set; } = new();
    public List<string> Freevars { get; set; } = new();
    public List<string> Cellvars { get; set; } = new();

    // ---- 子代码对象 ----
    public List<CodeObject> ChildCodes { get; set; } = new();

    // ---- 函数签名 ----
    public int ArgCount { get; set; }
    public int KwOnlyArgCount { get; set; }
    public bool HasVarargs { get; set; }
    public bool HasVarkw { get; set; }

    // ---- 属性标志 ----
    public bool IsGenerator { get; set; }
    public bool IsCoroutine { get; set; }
    public bool IsAsyncGenerator { get; set; }

    // ---- 版本信息 ----
    /// <summary>
    /// 显式 Python 版本枚举，用于 switch/case 版本分支。
    /// 每个 case 必须附带 CPython 源码引用注释（参见 Include/opcode.h, Python/ceval.c, Python/compile.c）。
    /// </summary>
    public PythonVersion Version { get; set; } = PythonVersion.Unknown;

    /// <summary>Python 2.7（opcode 布局/MAKE_FUNCTION 值不同）</summary>
    public bool IsPython27 { get; set; }
    /// <summary>Python 3.8+（opcode 121 是 JUMP_IF_NOT_EXC_MATCH 而非 SETUP_EXCEPT）</summary>
    public bool IsPython38Plus { get; set; }
    /// <summary>Python 3.10+ word offset（指令arg已 ×2 转为字节偏移）</summary>
    public bool IsWordOffset { get; set; }

    // ---- 行号表 ----
    public Dictionary<int, int> LineNumberTable { get; set; } = new();
    /// <summary>原始 lnotab/linetable 字节</summary>
    public byte[]? LineNumberBytes { get; set; }
    /// <summary>指示行号表是否是 3.11+ linetable 格式</summary>
    public bool HasLinetable { get; set; }

    // ---- 异常表 (Python 3.10+) ----
    public List<ExceptionTableEntry> ExceptionTable { get; set; } = new();

    // ---- 反编译追踪 ----
    /// <summary>已被 StackMachine 执行/反编译的指令偏移集合</summary>
    public HashSet<int> DecompiledInstructionOffsets { get; set; } = new();

    public override string ToString()
        => $"CodeObject: {Name} ({Instructions.Count} instrs)";
}
