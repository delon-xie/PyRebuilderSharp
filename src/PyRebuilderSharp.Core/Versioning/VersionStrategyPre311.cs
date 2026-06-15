using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Versioning;

/// <summary>
/// Python 3.5-3.10 版本策略（3.11 之前的统一编号时代）。
/// 使用 is310/is38plus 构造函数参数来配置 3.10/3.8 新增的特性。
/// 所有 3.5-3.10 版本使用相同的操作码编号体系，可直接投射。
/// </summary>
public class VersionStrategyPre311 : VersionStrategyBase
{
    private readonly bool _is310;
    private readonly bool _is38plus;

    /// <summary>
    /// 初始化 3.5-3.10 版本策略。
    /// </summary>
    /// <param name="is310">是否为 Python 3.10（word offset + linetable）</param>
    /// <param name="is38plus">是否为 Python 3.8+（PEP 552 header + posonlyargcount）</param>
    public VersionStrategyPre311(bool is310, bool is38plus)
    {
        _is310 = is310;
        _is38plus = is38plus;
    }

    /// <summary>
    /// 根据 is310/is38plus 标志确定版本。
    /// </summary>
    public override PythonVersion Version
    {
        get
        {
            if (_is310) return PythonVersion.Py310;
            if (_is38plus) return PythonVersion.Py38;
            // For versions before 3.8, we approximate with Py35
            // (caller can refine with specific version if needed)
            return PythonVersion.Py35;
        }
    }

    public override string DisplayName
    {
        get
        {
            if (_is310) return "Python 3.10";
            if (_is38plus) return "Python 3.8";
            return "Python 3.5";
        }
    }

    public override int HaveArgument => 90;
    public override bool HasCaches => false;
    public override bool HasExceptionTable => false;
    public override bool HasQualname => false;
    public override bool SupportsCodeSimple => false;
    public override bool UseLocalsPlus => false;

    // 3.10 新增
    public override bool IsWordOffset => _is310;
    public override bool HasLinetable => _is310;

    // 3.8 新增
    public override bool HasPep552Header => _is38plus;
    public override bool HasPosOnlyArgCount => _is38plus;

    /// <summary>
    /// 3.5-3.10 的操作码编号体系统一，可直接投射。
    /// </summary>
    public override Opcode MapOpcode(byte rawOp)
    {
        return (Opcode)rawOp;
    }

    // IsJumpInstruction 继承自基类的默认实现
}
