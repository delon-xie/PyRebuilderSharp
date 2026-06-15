using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Versioning;

/// <summary>
/// 版本策略接口——封装特定 Python 版本的 .pyc 格式差异。
/// 每个 Python 版本的 marshal 格式、操作码编号、字节码布局、cache 配置都是独立的。
/// 实现类不应假定任何跨版本的兼容性。
/// </summary>
public interface IVersionStrategy
{
    /// <summary>版本标识。</summary>
    PythonVersion Version { get; }

    /// <summary>展示名称（如 "Python 3.14"）。</summary>
    string DisplayName { get; }

    /// <summary>.pyc 头部字节数（魔数+flags+timestamp+size 等）。</summary>
    int HeaderSize { get; }

    /// <summary>HAVE_ARGUMENT 阈值：rawOp >= 此值则指令带参数。</summary>
    int HaveArgument { get; }

    /// <summary>跳转偏移是否为 word 偏移（×2）。3.10+ 是。</summary>
    bool IsWordOffset { get; }

    /// <summary>字节码中是否有 CACHE 条目（opcode=0）。3.11+ 是。</summary>
    bool HasCaches { get; }

    /// <summary>code 对象是否有 exceptiontable。3.11+ 是。</summary>
    bool HasExceptionTable { get; }

    /// <summary>code 对象是否有 qualname 字段。3.11+ 是。</summary>
    bool HasQualname { get; }

    /// <summary>头部是否有 FLAG_REF 支持的 TYPE_CODE_SIMPLE。3.11+ 是。</summary>
    bool SupportsCodeSimple { get; }

    /// <summary>marshal 格式是否使用 localsplusnames/localspluskinds。3.11+ 是。</summary>
    bool UseLocalsPlus { get; }

    /// <summary>代码对象是否使用 linetable（替代 lnotab）。3.10+ 是。</summary>
    bool HasLinetable { get; }

    /// <summary>头部是否有 PEP 552 flags 字段。3.8+ 是。</summary>
    bool HasPep552Header { get; }

    /// <summary>marshal 中 code 对象是否有 posonlyargcount 字段。3.8+ 是。</summary>
    bool HasPosOnlyArgCount { get; }

    /// <summary>
    /// 将原始字节值映射到统一 <see cref="Opcode"/> 枚举。
    /// </summary>
    Opcode MapOpcode(byte rawOp);

    /// <summary>
    /// 获取指定操作码的 cache 条目数（每条 2 字节）。仅在 HasCaches=true 时有效。
    /// </summary>
    int GetCacheCount(byte rawOp);

    /// <summary>
    /// 判断操作码是否为跳转指令（用于 word offset 转换）。
    /// </summary>
    bool IsJumpInstruction(Opcode op);
}
