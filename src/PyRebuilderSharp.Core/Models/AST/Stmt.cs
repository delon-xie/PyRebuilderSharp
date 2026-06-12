namespace PyRebuilderSharp.Core.Models.AST;

/// <summary>语句节点基类</summary>
public abstract record Stmt : AstNode;

// --- 简单语句 ---
public record Pass() : Stmt;
public record Break() : Stmt;
public record Continue() : Stmt;
public record ExprStmt(Expr Value) : Stmt;

// --- 赋值 ---
public record Assign(List<Expr> Targets, Expr Value) : Stmt;
public record AnnAssign(Expr Target, Expr Annotation, Expr? Value = null) : Stmt;
public record AugAssign(Expr Target, Operator Op, Expr Value) : Stmt;

// --- 删除 ---
public record Delete(List<Expr> Targets) : Stmt;

// --- 返回/Yield ---
public record Return(Expr? Value) : Stmt;
public record Yield(Expr? Value) : Stmt;
public record YieldFrom(Expr Value) : Stmt;

// --- 控制流 ---
public record If(Expr Test, List<Stmt> Body, List<Stmt>? Orelse = null) : Stmt;
public record While(Expr Test, List<Stmt> Body, List<Stmt>? Orelse = null) : Stmt;
public record For(Expr Target, Expr Iter, List<Stmt> Body, List<Stmt>? Orelse = null) : Stmt;

// --- 异常 ---
public record Try(
    List<Stmt> Body,
    List<ExceptHandler> Handlers,
    List<Stmt>? Orelse = null,
    List<Stmt>? Finalbody = null
) : Stmt;

public record ExceptHandler(Expr? Type, string? Name, List<Stmt> Body) : Stmt;
public record Raise(Expr? Exc = null, Expr? Cause = null) : Stmt;
public record Assert(Expr Test, Expr? Msg = null) : Stmt;

// --- With ---
public record With(List<WithItem> Items, List<Stmt> Body) : Stmt;
public record WithItem(Expr ContextExpr, Expr? OptionalVars);

// --- 函数/类 ---
public record FunctionDef(
    string Name,
    List<Parameter> Args,
    List<Stmt> Body,
    List<Expr>? Decorators = null,
    Expr? Returns = null,
    bool IsGenerator = false,
    bool IsAsync = false
) : Stmt;

public record AsyncFunctionDef(
    string Name,
    List<Parameter> Args,
    List<Stmt> Body,
    List<Expr>? Decorators = null,
    Expr? Returns = null
) : Stmt;

public record ClassDef(
    string Name,
    List<Expr> Bases,
    List<Stmt> Body,
    List<Expr>? Decorators = null
) : Stmt;

public record Parameter(string Name, Expr? Annotation = null, Expr? Default = null);

// --- 模块 ---
public record Module(List<Stmt> Body, string Name = "<module>") : AstNode;

// --- Import ---
public record Import(List<Alias> Names) : Stmt;
public record ImportFrom(string? Module, List<Alias> Names, int Level = 0) : Stmt;
public record Alias(string Name, string? Asname);

// --- 声明 ---
public record Global(List<string> Names) : Stmt;
public record Nonlocal(List<string> Names) : Stmt;
public record TypeAlias(Expr Name, Expr Value) : Stmt;

// --- 注释块（兜底） ---
public record CommentBlock(string Comment) : Stmt;
