using System.Text;
using PyRebuilderSharp.Core.Models.AST;
using PyRebuilderSharp.Core.Models.Bytecode;
using AstAttribute = PyRebuilderSharp.Core.Models.AST.Attribute;

namespace PyRebuilderSharp.Core.Generators;

/// <summary>
/// Phase 4: Python代码生成器。
/// 将AST节点树转换为格式化的Python源代码。
/// 使用访问者模式遍历AST。
/// 支持 CommentBlock 兜底输出。
/// </summary>
public class PythonCodeGenerator : ICodeGenerator
{
    private readonly StringBuilder _output = new();
    private int _indentLevel;
    private readonly CodeGenOptions _options;

    public PythonCodeGenerator(CodeGenOptions? options = null)
    {
        _options = options ?? new CodeGenOptions();
    }

    public string Generate(AstNode root)
    {
        _output.Clear();
        _indentLevel = 0;
        Visit(root);
        return _output.ToString();
    }

    private void Visit(AstNode node)
    {
        switch (node)
        {
            case Module m:
                VisitModule(m);
                break;
            case FunctionDef f:
                VisitFunctionDef(f);
                break;
            case ClassDef c:
                VisitClassDef(c);
                break;
            case If i:
                VisitIf(i);
                break;
            case While w:
                VisitWhile(w);
                break;
            case For f:
                VisitFor(f);
                break;
            case Return r:
                VisitReturn(r);
                break;
            case Assign a:
                VisitAssign(a);
                break;
            case AugAssign aa:
                VisitAugAssign(aa);
                break;
            case ExprStmt e:
                WriteIndent();
                Visit(e.Value);
                _output.AppendLine();
                break;
            case Pass:
                WriteIndent();
                _output.AppendLine("pass");
                break;
            case Break:
                WriteIndent();
                _output.AppendLine("break");
                break;
            case Continue:
                WriteIndent();
                _output.AppendLine("continue");
                break;
            case Import imp:
                VisitImport(imp);
                break;
            case ImportFrom impf:
                VisitImportFrom(impf);
                break;
            case Try t:
                VisitTry(t);
                break;
            case Raise r:
                VisitRaise(r);
                break;
            case With w:
                VisitWith(w);
                break;
            case Assert a:
                VisitAssert(a);
                break;
            case Delete d:
                VisitDelete(d);
                break;
            case Global g:
                VisitGlobal(g);
                break;
            case Match m:
                VisitMatch(m);
                break;
            case Nonlocal n:
                VisitNonlocal(n);
                break;
            case Yield y:
                WriteIndent();
                VisitYield(y);
                _output.AppendLine();
                break;
            case YieldFrom yf:
                WriteIndent();
                VisitYieldFrom(yf);
                _output.AppendLine();
                break;

            // ❗ 核心：CommentBlock 兜底输出
            case CommentBlock cb:
                VisitCommentBlock(cb);
                break;

            // ---- 表达式 ----
            case Constant c:
                VisitConstant(c);
                break;
            case Name n:
                _output.Append(n.Id);
                break;
            case BinOp b:
                VisitBinOp(b);
                break;
            case UnaryOp u:
                VisitUnaryOp(u);
                break;
            case Compare c:
                VisitCompare(c);
                break;
            case BoolOp b:
                VisitBoolOp(b);
                break;
            case Call c:
                VisitCall(c);
                break;
            case AstAttribute a:
                VisitAttribute(a);
                break;
            case Subscript s:
                VisitSubscript(s);
                break;
            case ListLiteral l:
                VisitListLiteral(l);
                break;
            case Starred s:
                VisitStarred(s);
                break;
            case DictLiteral d:
                VisitDictLiteral(d);
                break;
            case Lambda l:
                VisitLambda(l);
                break;
            case FunctionRef fr:
                _output.Append(fr.Name);
                break;
            case Slice s:
                VisitSliceLiteral(s);
                break;
            case SetLiteral sl:
                VisitSetLiteral(sl);
                break;
            case NamedExpr ne:
                Visit(ne.Target);
                _output.Append(" := ");
                Visit(ne.Value);
                break;
            case FormattedValue fv:
                Visit(fv.Value);
                if (fv.Conversion > 0)
                {
                    _output.Append('!');
                    _output.Append((char)fv.Conversion);
                }
                if (fv.FormatSpec != null)
                {
                    _output.Append(':');
                    Visit(fv.FormatSpec);
                }
                break;
            case JoinedStr js:
                _output.Append('f');
                _output.Append('"');
                foreach (var part in js.Values)
                {
                    if (part is Constant c && c.Value is string s)
                        _output.Append(s);
                    else
                    {
                        _output.Append('{');
                        Visit(part);
                        _output.Append('}');
                    }
                }
                _output.Append('"');
                break;
            default:
                _output.Append($"# Unknown node: {node.GetType().Name}");
                break;
        }
    }

    private void VisitModule(Module module)
    {
        // Module head comment (optional)
        if (_options.ShowHeader)
            _output.AppendLine($"# Decompiled from: {module.Name}");
        if (_options.ShowHeader)
            _output.AppendLine();

        foreach (var stmt in module.Body)
        {
            Visit(stmt);
            // Visit already appends newline, no need for extra blank line
        }
    }

    private void VisitFunctionDef(FunctionDef func)
    {
        if (func.Decorators?.Count > 0)
        {
            foreach (var decorator in func.Decorators)
            {
                WriteIndent();
                _output.Append("@");
                Visit(decorator);
                _output.AppendLine();
            }
        }

        WriteIndent();
        if (func.IsAsync)
            _output.Append("async ");
        _output.Append("def ");
        _output.Append(func.Name);
        _output.Append("(");

        for (int i = 0; i < func.Args.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            VisitParameter(func.Args[i]);
        }

        _output.Append(")");
        if (func.Returns != null)
        {
            _output.Append(" -> ");
            Visit(func.Returns);
        }
        _output.AppendLine(":");

        _indentLevel++;
        foreach (var stmt in func.Body)
            Visit(stmt);
        if (func.Body.Count == 0)
            EmitEmptyBodyPass();
        _indentLevel--;
    }

    private void VisitClassDef(ClassDef cls)
    {
        WriteIndent();

        if (cls.Decorators?.Count > 0)
        {
            foreach (var decorator in cls.Decorators)
            {
                WriteIndent();
                _output.Append("@");
                Visit(decorator);
                _output.AppendLine();
            }
        }

        _output.Append("class ");
        _output.Append(cls.Name);

        if (cls.Bases.Count > 0)
        {
            _output.Append("(");
            for (int i = 0; i < cls.Bases.Count; i++)
            {
                if (i > 0) _output.Append(", ");
                Visit(cls.Bases[i]);
            }
            _output.Append(")");
        }

        _output.AppendLine(":");

        _indentLevel++;
        foreach (var stmt in cls.Body)
            Visit(stmt);
        if (cls.Body.Count == 0)
            EmitEmptyBodyPass();
        _indentLevel--;
    }

    private void VisitIf(If ifStmt)
    {
        WriteIndent();
        _output.Append("if ");
        Visit(ifStmt.Test);
        _output.AppendLine(":");

        _indentLevel++;
        foreach (var stmt in ifStmt.Body)
            Visit(stmt);
        if (ifStmt.Body.Count == 0)
            EmitEmptyBodyPass();
        _indentLevel--;

        if (ifStmt.Orelse?.Count > 0)
        {
            if (ifStmt.Orelse.Count == 1 && ifStmt.Orelse[0] is If elifStmt)
            {
                RenderElif(elifStmt);
            }
            else
            {
                VisitElseClause(ifStmt.Orelse);
            }
        }
    }

    /// <summary>
    /// 渲染 elif 分支（支持 elif 链递归）
    /// </summary>
    private void RenderElif(If elifStmt)
    {
        WriteIndent();
        _output.Append("elif ");
        Visit(elifStmt.Test);
        _output.AppendLine(":");

        _indentLevel++;
        foreach (var stmt in elifStmt.Body)
            Visit(stmt);
        if (elifStmt.Body.Count == 0)
            EmitEmptyBodyPass();
        _indentLevel--;

        if (elifStmt.Orelse?.Count > 0)
        {
            if (elifStmt.Orelse.Count == 1 && elifStmt.Orelse[0] is If elifStmt2)
                RenderElif(elifStmt2); // next elif
            else
                VisitElseClause(elifStmt.Orelse); // final else
        }
    }

    private void VisitElseClause(List<Stmt> orelse)
    {
        WriteIndent();
        _output.AppendLine("else:");
        _indentLevel++;
        foreach (var stmt in orelse)
            Visit(stmt);
        if (orelse.Count == 0)
            EmitEmptyBodyPass();
        _indentLevel--;
    }

    private void VisitWhile(While whileStmt)
    {
        WriteIndent();
        _output.Append("while ");
        Visit(whileStmt.Test);
        _output.AppendLine(":");

        _indentLevel++;
        foreach (var stmt in whileStmt.Body)
            Visit(stmt);
        if (whileStmt.Body.Count == 0)
            EmitEmptyBodyPass();
        _indentLevel--;

        if (whileStmt.Orelse?.Count > 0)
            VisitElseClause(whileStmt.Orelse);
    }

    private void VisitFor(For forStmt)
    {
        WriteIndent();
        _output.Append("for ");
        Visit(forStmt.Target);
        _output.Append(" in ");
        Visit(forStmt.Iter);
        _output.AppendLine(":");

        _indentLevel++;
        foreach (var stmt in forStmt.Body)
            Visit(stmt);
        if (forStmt.Body.Count == 0)
            EmitEmptyBodyPass();
        _indentLevel--;

        if (forStmt.Orelse?.Count > 0)
            VisitElseClause(forStmt.Orelse);
    }

    private void VisitTry(Try tryStmt)
    {
        WriteIndent();
        _output.AppendLine("try:");

        _indentLevel++;
        foreach (var stmt in tryStmt.Body)
            Visit(stmt);
        if (tryStmt.Body.Count == 0)
            EmitEmptyBodyPass();
        _indentLevel--;

        foreach (var handler in tryStmt.Handlers)
        {
            WriteIndent();
            _output.Append(handler.IsGroup ? "except*" : "except");
            if (handler.Type != null)
            {
                _output.Append(" ");
                Visit(handler.Type);
                if (handler.Name != null)
                {
                    _output.Append(" as ");
                    _output.Append(handler.Name);
                }
            }
            _output.AppendLine(":");

            _indentLevel++;
            foreach (var stmt in handler.Body)
                Visit(stmt);
            if (handler.Body.Count == 0)
                EmitEmptyBodyPass();
            _indentLevel--;
        }

        if (tryStmt.Orelse?.Count > 0)
            VisitElseClause(tryStmt.Orelse);

        if (tryStmt.Finalbody?.Count > 0)
        {
            WriteIndent();
            _output.AppendLine("finally:");
            _indentLevel++;
            foreach (var stmt in tryStmt.Finalbody)
                Visit(stmt);
            if (tryStmt.Finalbody.Count == 0)
                EmitEmptyBodyPass();
            _indentLevel--;
        }
    }

    /// <summary>
    /// 当控制体为空时输出 pass（如 for/while/try 的空 body）
    /// </summary>
    private void EmitEmptyBodyPass()
    {
        WriteIndent();
        _output.AppendLine("pass");
    }

    private void VisitWith(With withStmt)
    {
        WriteIndent();
        _output.Append("with ");
        for (int i = 0; i < withStmt.Items.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            var item = withStmt.Items[i];
            Visit(item.ContextExpr);
            if (item.OptionalVars != null)
            {
                _output.Append(" as ");
                Visit(item.OptionalVars);
            }
        }
        _output.AppendLine(":");

        _indentLevel++;
        foreach (var stmt in withStmt.Body)
            Visit(stmt);
        if (withStmt.Body.Count == 0)
            EmitEmptyBodyPass();
        _indentLevel--;
    }

    private void VisitMatch(Match match)
    {
        WriteIndent();
        _output.Append("match ");
        Visit(match.Subject);
        _output.AppendLine(":");
        _indentLevel++;
        foreach (var mc in match.Cases)
        {
            WriteIndent();
            _output.Append("case ");
            VisitMatchPattern(mc.Pattern);
            if (mc.Guard != null)
            {
                _output.Append(" if ");
                Visit(mc.Guard);
            }
            _output.AppendLine(":");
            _indentLevel++;
            foreach (var stmt in mc.Body)
                Visit(stmt);
            if (mc.Body.Count == 0)
                EmitEmptyBodyPass();
            _indentLevel--;
        }
        _indentLevel--;
    }

    private void VisitMatchPattern(MatchPattern pattern)
    {
        switch (pattern)
        {
            case MatchValue mv:
                Visit(mv.Value);
                break;
            case MatchSingleton ms:
                Visit(ms.Value);
                break;
            case MatchWildcard:
                _output.Append("_");
                break;
            case MatchSequence seq:
                _output.Append("[");
                for (int i = 0; i < seq.Patterns.Count; i++)
                {
                    if (i > 0) _output.Append(", ");
                    VisitMatchPattern(seq.Patterns[i]);
                }
                if (seq.Rest != null)
                {
                    if (seq.Patterns.Count > 0) _output.Append(", ");
                    _output.Append("*");
                    VisitMatchPattern(seq.Rest);
                }
                _output.Append("]");
                break;
            case MatchMapping mm:
                _output.Append("{");
                for (int i = 0; i < mm.Keys.Count; i++)
                {
                    if (i > 0) _output.Append(", ");
                    Visit(mm.Keys[i]);
                    _output.Append(": ");
                    VisitMatchPattern(mm.Patterns[i]);
                }
                if (mm.Rest != null)
                {
                    if (mm.Keys.Count > 0) _output.Append(", ");
                    _output.Append("**");
                    VisitMatchPattern(mm.Rest);
                }
                _output.Append("}");
                break;
            case MatchClass mc:
                Visit(mc.Cls);
                _output.Append("(");
                for (int i = 0; i < mc.Patterns.Count; i++)
                {
                    if (i > 0) _output.Append(", ");
                    if (mc.KwdNames != null && i >= mc.Patterns.Count - mc.KwdNames.Count)
                    {
                        int kwIdx = mc.KwdNames.Count - (mc.Patterns.Count - i);
                        _output.Append(mc.KwdNames[kwIdx]);
                        _output.Append("=");
                    }
                    VisitMatchPattern(mc.Patterns[i]);
                }
                _output.Append(")");
                break;
            case MatchAs ma:
                if (ma.Pattern != null)
                {
                    VisitMatchPattern(ma.Pattern);
                    _output.Append(" as ");
                }
                _output.Append(ma.Name ?? "_");
                break;
            case MatchOr mo:
                for (int i = 0; i < mo.Patterns.Count; i++)
                {
                    if (i > 0) _output.Append(" | ");
                    VisitMatchPattern(mo.Patterns[i]);
                }
                break;
            case MatchStar ms:
                _output.Append("*");
                _output.Append(ms.Name ?? "_");
                break;
            default:
                _output.Append("# Unknown pattern");
                break;
        }
    }

    private void VisitReturn(Return ret)
    {
        WriteIndent();
        _output.Append("return");
        if (ret.Value != null)
        {
            _output.Append(" ");
            Visit(ret.Value);
        }
        _output.AppendLine();
    }

    private void VisitAssign(Assign assign)
    {
        WriteIndent();
        for (int i = 0; i < assign.Targets.Count; i++)
        {
            if (i > 0) _output.Append(" = ");
            Visit(assign.Targets[i]);
        }
        _output.Append(" = ");
        Visit(assign.Value);
        _output.AppendLine();
    }

    private void VisitAugAssign(AugAssign aug)
    {
        WriteIndent();
        Visit(aug.Target);
        _output.Append($" {GetAugOpSymbol(aug.Op)} ");
        Visit(aug.Value);
        _output.AppendLine();
    }

    private void VisitImport(Import imp)
    {
        WriteIndent();
        _output.Append("import ");
        for (int i = 0; i < imp.Names.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            _output.Append(imp.Names[i].Name);
            if (imp.Names[i].Asname != null)
            {
                _output.Append(" as ");
                _output.Append(imp.Names[i].Asname);
            }
        }
        _output.AppendLine();
    }

    private void VisitImportFrom(ImportFrom impf)
    {
        WriteIndent();
        _output.Append("from ");
        if (impf.Level > 0)
            _output.Append(new string('.', impf.Level));
        if (impf.Module != null)
            _output.Append(impf.Module);
        _output.Append(" import ");

        for (int i = 0; i < impf.Names.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            _output.Append(impf.Names[i].Name);
            if (impf.Names[i].Asname != null)
            {
                _output.Append(" as ");
                _output.Append(impf.Names[i].Asname);
            }
        }
        _output.AppendLine();
    }

    private void VisitRaise(Raise raise)
    {
        WriteIndent();
        _output.Append("raise");
        if (raise.Exc != null)
        {
            _output.Append(" ");
            Visit(raise.Exc);
            if (raise.Cause != null)
            {
                _output.Append(" from ");
                Visit(raise.Cause);
            }
        }
        _output.AppendLine();
    }

    private void VisitAssert(Assert assert)
    {
        WriteIndent();
        _output.Append("assert ");
        Visit(assert.Test);
        if (assert.Msg != null)
        {
            _output.Append(", ");
            Visit(assert.Msg);
        }
        _output.AppendLine();
    }

    private void VisitDelete(Delete del)
    {
        WriteIndent();
        _output.Append("del ");
        for (int i = 0; i < del.Targets.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            Visit(del.Targets[i]);
        }
        _output.AppendLine();
    }

    private void VisitGlobal(Global global)
    {
        WriteIndent();
        _output.Append("global ");
        _output.AppendLine(string.Join(", ", global.Names));
    }

    private void VisitNonlocal(Nonlocal nonlocal)
    {
        WriteIndent();
        _output.Append("nonlocal ");
        _output.AppendLine(string.Join(", ", nonlocal.Names));
    }

    // ❗ 核心：注释块兜底输出
    // 每行以当前缩进级别的 # 开头
    private void VisitCommentBlock(CommentBlock comment)
    {
        foreach (var line in comment.Comment.Split('\n'))
        {
            if (line.Trim().Length == 0 && line.Length == 0)
                continue;
            WriteIndent();
            _output.AppendLine(line);
        }
    }

    // ---- 表达式处理方法 ----

    private void VisitConstant(Constant constant)
    {
        if (constant.Value == null)
        {
            _output.Append("None");
        }
        else
        {
            switch (constant.Value)
            {
                case bool b:
                    _output.Append(b ? "True" : "False");
                    break;
                case int i:
                    _output.Append(i.ToString());
                    break;
                case long l:
                    _output.Append(l.ToString());
                    break;
                case double d:
                    _output.Append(d.ToString("G"));
                    break;
                case double[] dc when dc.Length == 2:
                    // Python complex number: real+imagj
                    _output.Append($"({dc[0]} + {dc[1]}j)");
                    break;
                case string s:
                    _output.Append(EscapeString(s));
                    break;
                case byte[] bytes:
                    _output.Append($"b'{Convert.ToBase64String(bytes)}'");
                    break;
                case System.Collections.IList list:
                    if (list is PyRebuilderSharp.Core.Models.Bytecode.PyTuple pyTup)
                        VisitConstantTuple(pyTup);
                    else
                        VisitConstantList(list);
                    break;
                default:
                    _output.Append(constant.Value.ToString());
                    break;
            }
        }
    }

    private void VisitConstantList(System.Collections.IList list)
    {
        // Lists are rendered as [...] 
        _output.Append("[");
        for (int i = 0; i < list.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            var item = list[i];
            if (item is Constant c)
                VisitConstant(c);
            else
                VisitConstant(new Constant(item));
        }
        _output.Append("]");
    }

    /// <summary>
    /// Visit a PyTuple constant, always output as parenthesized tuple.
    /// </summary>
    private void VisitConstantTuple(PyRebuilderSharp.Core.Models.Bytecode.PyTuple tuple)
    {
        _output.Append("(");
        for (int i = 0; i < tuple.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            var item = tuple[i];
            if (item is Constant c)
                VisitConstant(c);
            else
                VisitConstant(new Constant(item));
        }
        if (tuple.Count == 1)
            _output.Append(",)");  // Ensures (3,) not (3)
        else
            _output.Append(")");
    }

    private void VisitBinOp(BinOp binOp)
    {
        bool leftParens = binOp.Left is BinOp leftBin
            && GetOperatorPriority(leftBin.Op) > GetOperatorPriority(binOp.Op);
        bool rightParens = binOp.Right is BinOp rightBin
            && GetOperatorPriority(rightBin.Op) > GetOperatorPriority(binOp.Op);

        if (leftParens) _output.Append("(");
        Visit(binOp.Left);
        if (leftParens) _output.Append(")");
        _output.Append($" {GetOpSymbol(binOp.Op)} ");
        if (rightParens) _output.Append("(");
        Visit(binOp.Right);
        if (rightParens) _output.Append(")");
    }

    private void VisitUnaryOp(UnaryOp unaryOp)
    {
        var opSymbol = unaryOp.Op switch
        {
            UnaryOperator.Not => "not ",
            UnaryOperator.USub => "-",
            UnaryOperator.UAdd => "+",
            UnaryOperator.Invert => "~",
            _ => "?"
        };
        _output.Append(opSymbol);

        if (unaryOp.Operand is BinOp)
        {
            _output.Append("(");
            Visit(unaryOp.Operand);
            _output.Append(")");
        }
        else
        {
            Visit(unaryOp.Operand);
        }
    }

    private void VisitBoolOp(BoolOp boolOp)
    {
        string opStr = boolOp.Op switch
        {
            BoolOperator.And => " and ",
            BoolOperator.Or => " or ",
            _ => " ? "
        };
        for (int i = 0; i < boolOp.Values.Count; i++)
        {
            if (i > 0) _output.Append(opStr);
            // Wrap sub-expressions in parens if needed
            if (boolOp.Values[i] is BinOp or Compare)
            {
                _output.Append("(");
                Visit(boolOp.Values[i]);
                _output.Append(")");
            }
            else
            {
                Visit(boolOp.Values[i]);
            }
        }
    }

    private void VisitCompare(Compare compare)
    {
        Visit(compare.Left);
        for (int i = 0; i < compare.Ops.Count; i++)
        {
            _output.Append($" {GetCmpOpSymbol(compare.Ops[i])} ");
            Visit(compare.Comparators[i]);
        }
    }

    private void VisitCall(Call call)
    {
        Visit(call.Func);
        _output.Append("(");

        for (int i = 0; i < call.Args.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            Visit(call.Args[i]);
        }

        foreach (var kw in call.Keywords)
        {
            if (call.Args.Count > 0 || call.Keywords.IndexOf(kw) > 0)
                _output.Append(", ");
            if (kw.Arg != null)
            {
                _output.Append(kw.Arg);
                _output.Append("=");
            }
            else
            {
                _output.Append("**");  // **kwargs dict unpacking
            }
            Visit(kw.Value);
        }

        _output.Append(")");
    }

    private void VisitAttribute(AstAttribute attr)
    {
        Visit(attr.Value);
        _output.Append(".");
        _output.Append(attr.Attr);
    }

    private void VisitSubscript(Subscript sub)
    {
        Visit(sub.Value);
        _output.Append("[");
        if (sub.Slice is Slice slice)
        {
            // Output as slice: items[lower:upper:step]
            VisitSliceLiteral(slice);
        }
        else if (sub.Slice is Constant { Value: PySliceData ps })
        {
            // Pre-computed slice constant: items[start:stop:step]
            VisitSliceConstantLiteral(ps);
        }
        else if (sub.Slice is Constant c)
        {
            // Non-slice constant index (e.g., name[2])
            Visit(c);
        }
        else
        {
            // Fallback: unknown index type
            Visit(sub.Slice);
        }
        _output.Append("]");
    }

    /// <summary>
    /// Render a Slice AST node as [lower:upper:step] slice literal.
    /// </summary>
    private void VisitSliceLiteral(Slice slice)
    {
        // Strip trailing None for cleaner output: items[1:] instead of items[1:None]
        Visit(slice.Lower);
        _output.Append(":");
        bool hasUpper = !(slice.Upper is Constant { Value: null }); // None
        bool hasStep = slice.Step != null && !(slice.Step is Constant { Value: null });
        if (hasUpper)
            Visit(slice.Upper);
        if (hasStep || hasUpper)
        {
            // Still need an empty upper if step is present but upper is None
            if (!hasUpper && hasStep)
            {
                // items[1::2] → lower is provided, upper is empty
            }
            if (hasStep)
            {
                _output.Append(":");
                Visit(slice.Step);
            }
        }
    }

    /// <summary>
    /// Render a pre-computed PySliceData constant as [start:stop:step] slice literal.
    /// Python's slice(None, 2, None) → [:2]
    /// </summary>
    private void VisitSliceConstantLiteral(PySliceData ps)
    {
        bool hasStart = ps.Start != null && !(ps.Start is int i && i == 0 && ps.Stop == null);
        bool hasStop = ps.Stop != null;
        bool hasStep = ps.Step != null && !(ps.Step is int step && step == 1);

        if (hasStart)
            _output.Append(FormatSliceValue(ps.Start));
        _output.Append(":");
        if (hasStop)
            _output.Append(FormatSliceValue(ps.Stop));
        if (hasStep)
        {
            _output.Append(":");
            _output.Append(FormatSliceValue(ps.Step));
        }
    }

    private string FormatSliceValue(object? val)
    {
        if (val == null) return "";
        if (val is bool b) return b ? "True" : "False";
        if (val is int i) return i.ToString();
        if (val is long l) return l.ToString();
        if (val is string s) return EscapeString(s);
        return val.ToString() ?? "";
    }

    private void VisitSetLiteral(SetLiteral set)
    {
        _output.Append("{");
        for (int i = 0; i < set.Elts.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            Visit(set.Elts[i]);
        }
        _output.Append("}");
    }

    private void VisitListLiteral(ListLiteral list)
    {
        string open = list.Kind == ContainerKind.Tuple ? "(" : "[";
        string close = list.Kind == ContainerKind.Tuple ? ")" : "]";

        _output.Append(open);
        for (int i = 0; i < list.Elts.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            Visit(list.Elts[i]);
        }
        _output.Append(close);
    }

    private void VisitStarred(Starred star)
    {
        _output.Append('*');
        Visit(star.Value);
    }

    private void VisitDictLiteral(DictLiteral dict)
    {
        _output.Append("{");
        for (int i = 0; i < dict.Entries.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            Visit(dict.Entries[i].Key);
            _output.Append(": ");
            Visit(dict.Entries[i].Value);
        }
        _output.Append("}");
    }

    private void VisitLambda(Lambda lambda)
    {
        _output.Append("lambda ");
        for (int i = 0; i < lambda.Args.Count; i++)
        {
            if (i > 0) _output.Append(", ");
            VisitParameter(lambda.Args[i]);
        }
        _output.Append(": ");
        Visit(lambda.Body);
    }

    private void VisitYield(Yield yield)
    {
        _output.Append("yield");
        if (yield.Value != null)
        {
            _output.Append(" ");
            Visit(yield.Value);
        }
    }

    private void VisitYieldFrom(YieldFrom yieldFrom)
    {
        _output.Append("yield from ");
        Visit(yieldFrom.Value);
    }

    private void VisitParameter(Parameter param)
    {
        _output.Append(param.Name);
        if (param.Annotation != null)
        {
            _output.Append(": ");
            Visit(param.Annotation);
        }
        if (param.Default != null)
        {
            _output.Append(" = ");
            Visit(param.Default);
        }
    }

    // ---- 辅助方法 ----

    private void WriteIndent()
    {
        _output.Append(new string(' ', _indentLevel * 4));
    }

    private string EscapeString(string s)
    {
        var sb = new StringBuilder();
        bool isMultiLine = s.Contains('\n');
        if (isMultiLine)
            sb.Append("\"\"\"");
        else
            sb.Append('\'');
        foreach (char c in s)
        {
            if (isMultiLine)
            {
                switch (c)
                {
                    case '\n': sb.Append('\n'); break;  // """内直接换行
                    case '\r': sb.Append("\\r"); break;
                    case '\t': sb.Append('\t'); break;  // """内直接制表符
                    case '\\': sb.Append("\\\\"); break;
                    case '"':
                        if (sb.Length >= 2 && sb[^1] == '"' && sb[^2] == '"')
                            sb.Append('\\');
                        sb.Append('"');
                        break;
                    default:
                        if (c < 0x20 || c == 0x7F)
                            sb.Append($"\\x{(int)c:x2}");
                        else
                            sb.Append(c);
                        break;
                }
            }
            else
            {
                switch (c)
                {
                    case '\\': sb.Append("\\\\"); break;
                    case '\n': sb.Append("\\n"); break;
                    case '\r': sb.Append("\\r"); break;
                    case '\t': sb.Append("\\t"); break;
                    case '\'':
                    case '"': sb.Append("\\'"); break;
                    default:
                        if (c < 0x20 || c == 0x7F)
                            sb.Append($"\\x{(int)c:x2}");
                        else
                            sb.Append(c);
                        break;
                }
            }
        }
        if (isMultiLine)
            sb.Append("\"\"\"");
        else
            sb.Append('\'');
        return sb.ToString();
    }

    private string GetOpSymbol(Operator op) => op switch
    {
        Operator.Add => "+",
        Operator.Sub => "-",
        Operator.Mul => "*",
        Operator.Div => "/",
        Operator.FloorDiv => "//",
        Operator.Mod => "%",
        Operator.Pow => "**",
        Operator.LShift => "<<",
        Operator.RShift => ">>",
        Operator.BitOr => "|",
        Operator.BitXor => "^",
        Operator.BitAnd => "&",
        Operator.MatMul => "@",
        _ => "?"
    };

    private string GetAugOpSymbol(Operator op) => op switch
    {
        Operator.Add => "+=",
        Operator.Sub => "-=",
        Operator.Mul => "*=",
        Operator.Div => "/=",
        Operator.FloorDiv => "//=",
        Operator.Mod => "%=",
        Operator.Pow => "**=",
        Operator.LShift => "<<=",
        Operator.RShift => ">>=",
        Operator.BitOr => "|=",
        Operator.BitXor => "^=",
        Operator.BitAnd => "&=",
        _ => "?="
    };

    private string GetCmpOpSymbol(CmpOp op) => op switch
    {
        CmpOp.Eq => "==",
        CmpOp.NotEq => "!=",
        CmpOp.Lt => "<",
        CmpOp.LtE => "<=",
        CmpOp.Gt => ">",
        CmpOp.GtE => ">=",
        CmpOp.Is => "is",
        CmpOp.IsNot => "is not",
        CmpOp.In => "in",
        CmpOp.NotIn => "not in",
        _ => "?"
    };

    private bool NeedsParentheses(BinOp binOp)
    {
        var parentPriority = GetOperatorPriority(binOp.Op);

        if (binOp.Left is BinOp leftBin)
        {
            // 左子节点优先级更低（数字更大）时，需要括号
            // 例如：(a - b) / c → a - b / c 会解析为 a - (b/c)，错了
            if (GetOperatorPriority(leftBin.Op) > parentPriority) return true;
        }

        if (binOp.Right is BinOp rightBin)
        {
            // 右子节点优先级不高于父节点时（即更低或相等），需要括号
            if (GetOperatorPriority(rightBin.Op) <= parentPriority) return true;
        }

        return false;
    }

    private int GetOperatorPriority(Operator op) => op switch
    {
        Operator.Pow => 1,
        Operator.MatMul => 2,
        Operator.Mul or Operator.Div or Operator.FloorDiv or Operator.Mod => 3,
        Operator.Add or Operator.Sub => 4,
        Operator.LShift or Operator.RShift => 5,
        Operator.BitAnd => 6,
        Operator.BitXor => 7,
        Operator.BitOr => 8,
        _ => 9
    };
}
