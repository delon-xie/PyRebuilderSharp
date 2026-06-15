using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Versioning;

/// <summary>
/// Python 2.7 版本策略。
/// 2.7 使用 8 字节头部（magic + timestamp，无 size/flags 字段），
/// 操作码映射与 3.x 完全不同。
/// </summary>
public class VersionStrategy27 : VersionStrategyBase
{
    public override PythonVersion Version => PythonVersion.Py27;
    public override string DisplayName => "Python 2.7";

    // 2.7 头部只有 magic(4) + timestamp(4)
    public override int HeaderSize => 8;
    public override int HaveArgument => 90;

    // 2.7 不支持任何新特性
    public override bool IsWordOffset => false;
    public override bool HasCaches => false;
    public override bool HasExceptionTable => false;
    public override bool HasQualname => false;
    public override bool SupportsCodeSimple => false;
    public override bool UseLocalsPlus => false;
    public override bool HasLinetable => false;
    public override bool HasPep552Header => false;
    public override bool HasPosOnlyArgCount => false;

    /// <summary>
    /// 将 Python 2.7 的原始 opcode 字节值映射到统一 Opcode 枚举。
    /// 2.7 的 opcode 值 70-89 与 3.x 完全不同：
    ///   70=PRINT_EXPR, 71=PRINT_ITEM, 72=PRINT_NEWLINE...
    ///   86=YIELD_VALUE, 87=POP_BLOCK, 88=END_FINALLY, 89=BUILD_CLASS
    /// </summary>
    public override Opcode MapOpcode(byte rawOp)
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
    /// 2.7 跳转指令检测。
    /// 包含 CONTINUE_LOOP, SETUP_LOOP, SETUP_EXCEPT_27, SETUP_FINALLY 等 2.7 特有跳转。
    /// </summary>
    public override bool IsJumpInstruction(Opcode op) => op switch
    {
        Models.Bytecode.Opcode.JUMP_FORWARD or Models.Bytecode.Opcode.JUMP_ABSOLUTE
            or Models.Bytecode.Opcode.POP_JUMP_IF_FALSE or Models.Bytecode.Opcode.POP_JUMP_IF_TRUE
            or Models.Bytecode.Opcode.JUMP_IF_TRUE_OR_POP or Models.Bytecode.Opcode.JUMP_IF_FALSE_OR_POP
            or Models.Bytecode.Opcode.FOR_ITER
            or Models.Bytecode.Opcode.CONTINUE_LOOP
            or Models.Bytecode.Opcode.SETUP_LOOP
            or Models.Bytecode.Opcode.SETUP_EXCEPT_27
            or Models.Bytecode.Opcode.SETUP_FINALLY => true,
        _ => false
    };
}
