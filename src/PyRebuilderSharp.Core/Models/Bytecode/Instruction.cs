namespace PyRebuilderSharp.Core.Models.Bytecode;

/// <summary>
/// 表示一条Python字节码指令。
/// 使用readonly record struct保证不可变性。
/// </summary>
public readonly record struct Instruction(
    int Offset,           // 指令在字节码中的偏移量
    Opcode Opcode,        // 操作码
    int? Argument = null  // 参数（可选，仅带参数的指令有值）
);
