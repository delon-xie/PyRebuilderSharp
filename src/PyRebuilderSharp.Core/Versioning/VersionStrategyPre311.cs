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
    private readonly bool _is37;
    private readonly bool _is36;

    /// <summary>
    /// 初始化 3.5-3.10 版本策略。
    /// </summary>
    /// <param name="is310">是否为 Python 3.10（word offset + linetable）</param>
    /// <param name="is38plus">是否为 Python 3.8+（posonlyargcount）</param>
    /// <param name="is37">是否为 Python 3.7（PEP 552 header，但无 posonlyargcount）</param>
    /// <param name="is36">是否为 Python 3.6（3.5 与 3.6 魔数不同但构造参数相同）</param>
    public VersionStrategyPre311(bool is310, bool is38plus, bool is37 = false, bool is36 = false)
    {
        _is310 = is310;
        _is38plus = is38plus;
        _is37 = is37;
        _is36 = is36;
    }

    /// <summary>
    /// 根据 is310/is38plus/is37 标志确定版本。
    /// </summary>
    public override PythonVersion Version
    {
        get
        {
            if (_is310) return PythonVersion.Py310;
            if (_is38plus) return PythonVersion.Py38;
            if (_is37) return PythonVersion.Py37;
            if (_is36) return PythonVersion.Py36;
            return PythonVersion.Py35;
        }
    }

    public override string DisplayName
    {
        get
        {
            if (_is310) return "Python 3.10";
            if (_is38plus) return "Python 3.8";
            if (_is37) return "Python 3.7";
            if (_is36) return "Python 3.6";
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

    // 3.7+ 新增 (PEP 552 header), 3.8+ 新增 (posonlyargcount)
    public override bool HasPep552Header => _is37 || _is38plus;
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
