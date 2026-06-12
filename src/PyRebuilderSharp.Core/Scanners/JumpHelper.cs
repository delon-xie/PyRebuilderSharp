using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Scanners;

/// <summary>
/// 跳转指令辅助类。
/// 集中管理所有跳转相关的判断逻辑。
/// </summary>
public static class JumpHelper
{
    public static bool IsTerminal(Opcode op) => op switch
    {
        Opcode.RETURN_VALUE or Opcode.RAISE_VARARGS => true,
        _ => false
    };

    public static bool IsConditionalJump(Opcode op) => op switch
    {
        Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
            or Opcode.POP_JUMP_IF_TRUE_PY38 or Opcode.POP_JUMP_IF_FALSE_PY38
            or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
            or Opcode.FOR_ITER => true,
        _ => false
    };

    public static bool IsUnconditionalJump(Opcode op) => op switch
    {
        Opcode.JUMP_ABSOLUTE or Opcode.JUMP_FORWARD or Opcode.JUMP_BACKWARD => true,
        _ => false
    };

    public static bool IsJump(Opcode op)
        => IsConditionalJump(op) || IsUnconditionalJump(op);

    public static int? GetJumpTarget(Instruction instr)
    {
        if (IsJump(instr.Opcode) && instr.Argument.HasValue)
            return instr.Argument.Value;
        return null;
    }
}
