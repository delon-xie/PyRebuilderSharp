/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Builders/BlockDecompiler.cs(25,42): warning CS8625: 无法将 null 字面量转换为非 null 的引用类型。 [/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/PyRebuilderSharp.Core.csproj]
/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Readers/PycReader.cs(379,99): warning CS8625: 无法将 null 字面量转换为非 null 的引用类型。 [/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/PyRebuilderSharp.Core.csproj]
/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Models/CFG/ControlStructure.cs(34,16): warning CS8907: 参数“Header”未读。是否忘记通过它来使用该名称初始化属性? [/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/PyRebuilderSharp.Core.csproj]
/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Readers/PycReader.cs(96,16): warning CS8603: 可能返回 null 引用。 [/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/PyRebuilderSharp.Core.csproj]
/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Models/CFG/ControlStructure.cs(24,16): warning CS8907: 参数“Header”未读。是否忘记通过它来使用该名称初始化属性? [/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/PyRebuilderSharp.Core.csproj]
/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Models/CFG/ControlStructure.cs(17,16): warning CS8907: 参数“Header”未读。是否忘记通过它来使用该名称初始化属性? [/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/PyRebuilderSharp.Core.csproj]
/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Models/CFG/ControlStructure.cs(14,44): warning CS8907: 参数“Header”未读。是否忘记通过它来使用该名称初始化属性? [/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/PyRebuilderSharp.Core.csproj]
/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Models/AST/AstNode.cs(9,27): warning CS8618: 在退出构造函数时，不可为 null 的 属性 "Location" 必须包含非 null 值。请考虑添加 "required" 修饰符或将该 属性 声明为可为 null。 [/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/PyRebuilderSharp.Core.csproj]
/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Generators/PythonCodeGenerator.cs(752,27): warning CS8604: “void PythonCodeGenerator.Visit(AstNode node)”中的形参“node”可能传入 null 引用实参。 [/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/PyRebuilderSharp.Core.csproj]
/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Builders/AstBuilder.cs(540,54): warning CS0219: 变量“isFinally”已被赋值，但从未使用过它的值 [/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/PyRebuilderSharp.Core.csproj]
/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/Builders/AstBuilder.cs(979,49): warning CS8604: “List<Stmt> AstBuilder.GetStructuredBlockStmts(BasicBlock block, HashSet<BasicBlock> visited)”中的形参“block”可能传入 null 引用实参。 [/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Core/PyRebuilderSharp.Core.csproj]
# Decompiled from: <module>

def depth_5_if(x0, x1, x2, x3, x4):
    if x0 > 0:
        if x1 > 1:
            pass
        else:
            result = 20
            return result
    else:
        result = 10
        return result
def depth_5_for():
    total = 0
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    for e in range(2):
                        total += 1
    return total
def depth_5_while():
    total = 0
    a = 2
    while a > 0:
        a -= 1
        b = 2
        while b > 0:
            b -= 1
            c = 2
            while c > 0:
                c -= 1
                d = 2
                while d > 0:
                    d -= 1
                    e = 2
                    while e > 0:
                        e -= 1
                        total += 1
    return total
def depth_5_try():
    result = 0
    try:
        result = 42
    except:
        result = -5

