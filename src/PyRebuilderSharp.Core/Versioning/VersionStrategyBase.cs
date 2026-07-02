using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Versioning;

/// <summary>
/// 版本策略基类。大多数版本只需要重写 <see cref="MapOpcode"/> 和缓存相关属性。
/// </summary>
public abstract class VersionStrategyBase : IVersionStrategy
{
    public abstract PythonVersion Version { get; }
    public abstract string DisplayName { get; }

    // ---- 以下是各版本有差异的默认值 ----
    public virtual int HeaderSize => 12;   // magic(4)+timestamp(4)+size(4)
    public virtual int HaveArgument => 90;
    public virtual bool IsWordOffset => false;   // 3.10+
    public virtual bool HasCaches => false;       // 3.11+
    public virtual bool HasExceptionTable => false; // 3.11+
    public virtual bool HasQualname => false;      // 3.11+
    public virtual bool SupportsCodeSimple => false; // 3.11+
    public virtual bool UseLocalsPlus => false;    // 3.11+
    public virtual bool HasLinetable => false;     // 3.10+
    public virtual bool HasPep552Header => false;  // 3.8+
    public virtual bool HasPosOnlyArgCount => false; // 3.8+

    public virtual Opcode MapOpcode(byte rawOp)
    {
        // 默认：直接投射（适用于 3.6-3.10 统一编号）
        return (Opcode)rawOp;
    }

    public virtual int GetCacheCount(byte rawOp) => 0;

    public virtual bool RequiresArgument(byte rawOp)
    {
        return rawOp >= HaveArgument;
    }

    public virtual bool IsJumpInstruction(Opcode op) => op switch
    {
        Opcode.JUMP_FORWARD or Opcode.JUMP_BACKWARD
            or Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
            or Opcode.FOR_ITER or Opcode.JUMP_ABSOLUTE
            or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
            or Opcode.SETUP_EXCEPT or Opcode.SETUP_FINALLY
            or Opcode.SETUP_LOOP or Opcode.SETUP_WITH => true,
        _ => false
    };
}
