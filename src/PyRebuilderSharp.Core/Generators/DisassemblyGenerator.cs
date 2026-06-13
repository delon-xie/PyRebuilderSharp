using System.Text;
using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Generators;

public static class DisassemblyGenerator
{
    public static string Generate(CodeObject code)
    {
        var sb = new StringBuilder();
        WriteCodeObject(sb, code, "");
        return sb.ToString();
    }

    private static void WriteCodeObject(StringBuilder sb, CodeObject code, string indent)
    {
        if (code.Name != "<module>")
        {
            sb.AppendLine($"\n{indent}Disassembly of {code.Name}:");
            sb.AppendLine($"{indent}  (filename: {code.Filename}, first line: {code.FirstLineNumber})");
        }

        int? prevLine = null;
        foreach (var ins in code.Instructions)
        {
            if (code.LineNumberTable.TryGetValue(ins.Offset, out int line))
            {
                if (line != prevLine)
                {
                    if (prevLine != null)
                        sb.AppendLine();
                    prevLine = line;
                }
            }

            var opName = GetOpcodeName(ins.Opcode);
            var argStr = ins.Argument?.ToString() ?? "";
            var argRepr = GetArgRepr(ins, code);

            var lineStr = prevLine?.ToString()?.PadLeft(4) ?? "    ";
            sb.AppendLine($"{indent}{lineStr}   {ins.Offset,-8}{opName,-24}{argStr,-4}{argRepr}");
        }

        foreach (var child in code.ChildCodes)
            WriteCodeObject(sb, child, indent);
    }

    private static string GetOpcodeName(Opcode op)
    {
        var name = op.ToString();
        int underscoreIdx = name.LastIndexOf('_');
        if (underscoreIdx > 0 && name.Length - underscoreIdx <= 3)
        {
            var suffix = name[(underscoreIdx + 1)..];
            if (suffix.All(char.IsDigit))
                name = name[..underscoreIdx];
        }
        return name;
    }

    private static string GetArgRepr(Instruction ins, CodeObject code)
    {
        if (ins.Argument == null) return "";
        int arg = ins.Argument.Value;
        var op = ins.Opcode;

        // ---- 常量操作 ----
        if (op == Opcode.LOAD_CONST)
        {
            if (code.Constants.TryGetValue(arg, out var cv))
                return $"({FormatConst(cv)})";
            return "";
        }

        // ---- 名称操作（Names 表）----
        if (op is Opcode.LOAD_NAME or Opcode.STORE_NAME or Opcode.DELETE_NAME
            or Opcode.LOAD_GLOBAL or Opcode.STORE_GLOBAL or Opcode.DELETE_GLOBAL
            or Opcode.LOAD_ATTR or Opcode.STORE_ATTR or Opcode.DELETE_ATTR
            or Opcode.IMPORT_NAME or Opcode.IMPORT_FROM or Opcode.LOAD_METHOD)
        {
            if (arg >= 0 && arg < code.Names.Count)
                return $"({code.Names[arg]})";
            return "";
        }

        // ---- 局部变量（Varnames 表）----
        if (op is Opcode.LOAD_FAST or Opcode.STORE_FAST or Opcode.DELETE_FAST)
        {
            if (arg >= 0 && arg < code.Varnames.Count)
                return $"({code.Varnames[arg]})";
            return "";
        }

        // ---- 闭包变量（Cellvars/Freevars）----
        if (op is Opcode.LOAD_DEREF or Opcode.STORE_DEREF or Opcode.DELETE_DEREF)
        {
            if (arg >= 0 && arg < code.Cellvars.Count)
                return $"({code.Cellvars[arg]})";
            arg -= code.Cellvars.Count;
            if (arg >= 0 && arg < code.Freevars.Count)
                return $"({code.Freevars[arg]})";
            return "";
        }

        // ---- 比较操作 ----
        if (op == Opcode.COMPARE_OP)
        {
            return arg switch
            {
                0 => "(<)", 1 => "(<=)", 2 => "(==)", 3 => "(!=)",
                4 => "(>)", 5 => "(>=)", 6 => "(in)", 7 => "(not in)",
                8 => "(is)", 9 => "(is not)", 10 => "(EXCEPTION_MATCH)",
                _ => $"({arg})"
            };
        }

        // ---- 函数调用 ----
        if (op is Opcode.CALL_FUNCTION or Opcode.CALL_FUNCTION_KW
            or Opcode.CALL_FUNCTION_EX or Opcode.CALL_METHOD
            or Opcode.CALL or Opcode.CALL_311)
        {
            return $"({arg} args)";
        }

        // ---- 跳转指令 ----
        if (op is Opcode.JUMP_FORWARD or Opcode.JUMP_ABSOLUTE or Opcode.JUMP_BACKWARD
            or Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE)
        {
            return $"(to 0x{arg * 2:X4})";
        }

        // ---- 构建容器 ----
        if (op is Opcode.BUILD_TUPLE or Opcode.BUILD_LIST or Opcode.BUILD_SET
            or Opcode.BUILD_MAP or Opcode.BUILD_STRING)
        {
            return arg == 1 ? "(1 elem)" : $"({arg} elems)";
        }

        // ---- MAKE_FUNCTION ----
        if (op == Opcode.MAKE_FUNCTION)
        {
            return arg switch
            {
                0 => "",
                1 => "(defaults)",
                2 => "(annotation)",
                3 => "(defaults, annotation)",
                4 => "(closure)",
                8 => "(annotation)",
                _ => ""
            };
        }

        return "";
    }

    private static string FormatConst(object? v)
    {
        return v switch
        {
            null => "None",
            bool b => b ? "True" : "False",
            int i => i.ToString(),
            long l => l.ToString(),
            double d => d.ToString("G"),
            string s => $"'{EscapeString(s)}'",
            CodeObject c => $"<code {c.Name}>",
            _ => v.ToString() ?? "?"
        };
    }

    private static string EscapeString(string s)
    {
        return s.Replace("\\", "\\\\")
                .Replace("\n", "\\n")
                .Replace("\r", "\\r")
                .Replace("\t", "\\t")
                .Replace("'", "\\'");
    }
}
