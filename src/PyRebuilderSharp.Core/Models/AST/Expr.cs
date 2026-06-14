namespace PyRebuilderSharp.Core.Models.AST;

/// <summary>表达式节点基类</summary>
public abstract record Expr : AstNode;

// --- 字面量 ---
public record Constant(object? Value) : Expr;
public record Ellipsis() : Expr;

// --- 名称 ---
public record Name(string Id, ExpressionContext Ctx = ExpressionContext.Load) : Expr
{
    /// <summary>标记是否为 IMPORT_NAME 产生（用于 import/from 检测）</summary>
    public bool IsImport { get; init; }
}

/// <summary>星号表达式 *expr（用于展开赋值 a, *b = ... 或函数调用 f(*args)）</summary>
public record Starred(Expr Value, ExpressionContext Ctx = ExpressionContext.Load) : Expr;

public enum ExpressionContext { Load, Store, Del, AugLoad, AugStore, Param }

// --- 一元运算 ---
public record UnaryOp(UnaryOperator Op, Expr Operand) : Expr;
public enum UnaryOperator { Not, UAdd, USub, Invert }

// --- 二元运算 ---
public record BinOp(Expr Left, Operator Op, Expr Right) : Expr;
public enum Operator
{
    Add, Sub, Mul, Div, FloorDiv, Mod, Pow,
    LShift, RShift, BitOr, BitXor, BitAnd, MatMul
}

// --- 比较 ---
public record Compare(Expr Left, List<CmpOp> Ops, List<Expr> Comparators) : Expr;
public enum CmpOp { Eq, NotEq, Lt, LtE, Gt, GtE, Is, IsNot, In, NotIn }

// --- 函数调用 ---
public record Call(Expr Func, List<Expr> Args, List<Keyword> Keywords) : Expr;
public record Keyword(string? Arg, Expr Value);

// --- 属性/下标 ---
public record Attribute(Expr Value, string Attr, ExpressionContext Ctx) : Expr
{
    /// <summary>
    /// 标记是否为 IMPORT_FROM 产生。
    /// True 表示 from X import Y，False 表示 obj.attr。
    /// </summary>
    public bool IsImportFrom { get; init; }
}
public record Subscript(Expr Value, Expr Slice, ExpressionContext Ctx) : Expr;

// --- 切片 ---
public record Slice(Expr Lower, Expr Upper, Expr? Step) : Expr;

// --- 容器字面量 ---
public record ListLiteral(List<Expr> Elts, ContainerKind Kind) : Expr;
public record DictLiteral(List<(Expr Key, Expr Value)> Entries) : Expr;
public record SetLiteral(List<Expr> Elts) : Expr;
public enum ContainerKind { List, Tuple }

// --- Lambda ---
public record Lambda(List<Parameter> Args, Expr Body) : Expr;

// --- 推导式 ---
public record ListComp(Expr Elt, List<Comprehension> Generators) : Expr;
public record SetComp(Expr Elt, List<Comprehension> Generators) : Expr;
public record DictComp(Expr Key, Expr Value, List<Comprehension> Generators) : Expr;
public record GeneratorExp(Expr Elt, List<Comprehension> Generators) : Expr;

public record Comprehension(Expr Target, Expr Iter, List<Expr> Ifs, bool IsAsync = false);

// --- Formatted Value (用于f-string) ---
public record FormattedValue(Expr Value, int Conversion = -1, Expr? FormatSpec = null) : Expr;
public record JoinedStr(List<Expr> Values) : Expr;

// --- 函数引用（中间表示，用于Assign→FunctionDef转换） ---
public record FunctionRef(Bytecode.CodeObject? Code, string Name) : Expr;

// --- Walrus (NamedExpr) ---
public record NamedExpr(Expr Target, Expr Value) : Expr;
