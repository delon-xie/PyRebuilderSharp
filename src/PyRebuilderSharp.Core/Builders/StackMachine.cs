using PyRebuilderSharp.Core.Models.AST;
using AstAttribute = PyRebuilderSharp.Core.Models.AST.Attribute;
using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Builders;

/// <summary>
/// 栈机模拟器。
/// 模拟Python虚拟机的栈操作，将字节码指令转为表达式树。
/// </summary>
public class StackMachine
{
    private readonly Stack<Expr> _exprStack = new();
    private readonly List<Expr> _results = new();
    private readonly CodeObject _code;
    private readonly HashSet<int> _loopHeaderOffsets;
    private bool _isForLoop;
    // v2.7 print 语句缓冲
    private readonly List<Expr> _printItems = new();

    public StackMachine(CodeObject code)
    {
        _code = code;
        _loopHeaderOffsets = new HashSet<int>();
        _isForLoop = false;
    }

    /// <summary>
    /// 设置循环头偏移集合，用于识别 continue/break。
    /// </summary>
    public void SetLoopHeaders(HashSet<int> headerOffsets)
    {
        _loopHeaderOffsets.Clear();
        foreach (var o in headerOffsets) _loopHeaderOffsets.Add(o);
    }

    /// <summary>
    /// 标记当前反编译的块是否为 for 循环体。
    /// for 循环中的 POP_TOP 应转为 break。
    /// </summary>
    public void SetIsForLoop(bool isFor)
    {
        _isForLoop = isFor;
    }

    /// <summary>重置栈状态</summary>
    private void Reset()
    {
        _exprStack.Clear();
        _results.Clear();
    }

    private Expr? SafePop()
    {
        if (_exprStack.Count > 0) return _exprStack.Pop();
        return null;
    }

    private Expr? SafePeek()
    {
        if (_exprStack.Count > 0) return _exprStack.Peek();
        return null;
    }

    /// <summary>是否有待处理的表达式</summary>
    public bool HasResults => _results.Count > 0;

    /// <summary>表达式栈大小</summary>
    public int ExprStackCount => _exprStack.Count;

    /// <summary>弹出表达式（从表达式栈，非_results）</summary>
    public Expr PopExpr()
    {
        return _exprStack.Pop();
    }

    /// <summary>弹出结果表达式</summary>
    public Expr PopResult()
    {
        var result = _results.Last();
        _results.RemoveAt(_results.Count - 1);
        return result;
    }

    /// <summary>
    /// 执行单条指令。
    /// </summary>
    public Stmt? Execute(Instruction instr)
    {
        switch (instr.Opcode)
        {
            // ---- 常量加载 ----
            case Opcode.LOAD_CONST:
                var value = _code.Constants.TryGetValue(instr.Argument ?? 0, out var v) ? v : null;
                _exprStack.Push(new Constant(value));
                return null;

            // ---- 名称操作 ----
            case Opcode.LOAD_NAME:
                var name = GetName(instr);
                _exprStack.Push(new Name(name, ExpressionContext.Load));
                return null;

            case Opcode.LOAD_FAST:
                var localName = GetVarname(instr);
                _exprStack.Push(new Name(localName, ExpressionContext.Load));
                return null;

            case Opcode.LOAD_GLOBAL:
                var globalName = GetName(instr);
                _exprStack.Push(new Name(globalName, ExpressionContext.Load));
                return null;

            case Opcode.STORE_NAME:
            {
                var storeName = GetName(instr);
                var val = SafePop();
                if (val == null) return null;
                return new Assign(new List<Expr> { new Name(storeName, ExpressionContext.Store) }, val);
            }

            case Opcode.STORE_FAST:
            {
                var storeLocal = GetVarname(instr);
                var val = SafePop();
                if (val == null) return null;
                return new Assign(new List<Expr> { new Name(storeLocal, ExpressionContext.Store) }, val);
            }

            case Opcode.STORE_GLOBAL:
            {
                var global = GetName(instr);
                var val = SafePop();
                if (val == null) return null;
                return new Assign(new List<Expr> { new Name(global, ExpressionContext.Store) }, val);
            }

            case Opcode.DELETE_FAST:
                return null;

            case Opcode.STORE_ATTR:
            {
                var attrName = GetName(instr);
                // Python 3.10: stack = [value, object]; TOS=object, TOS1=value
                var obj = SafePop();       // TOS = 对象
                var attrValue = SafePop(); // TOS1 = 值
                if (attrValue == null || obj == null) return null;
                return new Assign(new List<Expr> { new AstAttribute(obj, attrName, ExpressionContext.Store) }, attrValue);
            }

            case Opcode.LOAD_ATTR:
            {
                var attr = GetName(instr);
                var obj = SafePop();
                if (obj == null) return null;
                _exprStack.Push(new AstAttribute(obj, attr, ExpressionContext.Load));
                return null;
            }

            // ---- 构建操作 ----
            case Opcode.BUILD_TUPLE:
            case Opcode.BUILD_LIST:
            {
                var count = instr.Argument ?? 0;
                var items = new List<Expr>();
                for (int i = 0; i < count && _exprStack.Count > 0; i++)
                {
                    var item = SafePop();
                    if (item != null) items.Insert(0, item);
                }
                var kind = instr.Opcode == Opcode.BUILD_TUPLE ? ContainerKind.Tuple : ContainerKind.List;
                _exprStack.Push(new ListLiteral(items, kind));
                return null;
            }

            case Opcode.BUILD_MAP:
            {
                var count = instr.Argument ?? 0;
                var entries = new List<(Expr Key, Expr Value)>();
                for (int i = 0; i < count && _exprStack.Count >= 2; i++)
                {
                    var val = SafePop();
                    var key = SafePop();
                    if (key != null && val != null) entries.Insert(0, (key, val));
                }
                _exprStack.Push(new DictLiteral(entries));
                return null;
            }

            case Opcode.BUILD_SET:
            {
                var count = instr.Argument ?? 0;
                var items = new List<Expr>();
                for (int i = 0; i < count && _exprStack.Count > 0; i++)
                {
                    var item = SafePop();
                    if (item != null) items.Insert(0, item);
                }
                _exprStack.Push(new SetLiteral(items));
                return null;
            }

            // ---- 二元运算 ----
            case Opcode.BINARY_ADD: return HandleBinaryOp(Operator.Add);
            case Opcode.BINARY_SUBTRACT: return HandleBinaryOp(Operator.Sub);
            case Opcode.BINARY_MULTIPLY: return HandleBinaryOp(Operator.Mul);
            case Opcode.BINARY_DIVIDE: return HandleBinaryOp(Operator.Div);  // Python 2 only
            case Opcode.BINARY_TRUE_DIVIDE: return HandleBinaryOp(Operator.Div);
            case Opcode.BINARY_POWER: return HandleBinaryOp(Operator.Pow);
            case Opcode.BINARY_FLOOR_DIVIDE: return HandleBinaryOp(Operator.FloorDiv);
            case Opcode.BINARY_MODULO: return HandleBinaryOp(Operator.Mod);
            case Opcode.BINARY_LSHIFT: return HandleBinaryOp(Operator.LShift);
            case Opcode.BINARY_RSHIFT: return HandleBinaryOp(Operator.RShift);
            case Opcode.BINARY_AND: return HandleBinaryOp(Operator.BitAnd);
            case Opcode.BINARY_OR: return HandleBinaryOp(Operator.BitOr);
            case Opcode.BINARY_XOR: return HandleBinaryOp(Operator.BitXor);
            case Opcode.INPLACE_ADD: return HandleBinaryOp(Operator.Add);
            case Opcode.INPLACE_SUBTRACT: return HandleBinaryOp(Operator.Sub);

            // ---- BINARY_SUBSCR (a[b]) and Python 2 SLICE opcodes ----
            case Opcode.BINARY_SUBSCR:
            {
                var idx = SafePop();
                var obj = SafePop();
                if (idx == null || obj == null) return null;
                _exprStack.Push(new Subscript(obj, idx, ExpressionContext.Load));
                return null;
            }

            // Python 2.7 SLICE opcodes — these bundle Subscript+Slice
            case Opcode.SLICE_0: // TOS = TOS[:]
            {
                var c0 = SafePop();
                if (c0 == null) return null;
                var none0 = new Constant(null);
                _exprStack.Push(new Subscript(c0, new Slice(none0, none0, null), ExpressionContext.Load));
                return null;
            }
            case Opcode.SLICE_1: // TOS = TOS1[TOS:]
            {
                var lower1 = SafePop();
                var container1 = SafePop();
                if (lower1 == null || container1 == null) return null;
                var none1 = new Constant(null);
                _exprStack.Push(new Subscript(container1, new Slice(lower1, none1, null), ExpressionContext.Load));
                return null;
            }
            case Opcode.SLICE_2: // TOS = TOS1[:TOS]
            {
                var upper2 = SafePop();
                var container2 = SafePop();
                if (upper2 == null || container2 == null) return null;
                var none2 = new Constant(null);
                _exprStack.Push(new Subscript(container2, new Slice(none2, upper2, null), ExpressionContext.Load));
                return null;
            }
            case Opcode.SLICE_3: // TOS = TOS2[TOS1:TOS]
            {
                var upper3 = SafePop();
                var lower3 = SafePop();
                var container3 = SafePop();
                if (upper3 == null || lower3 == null || container3 == null) return null;
                _exprStack.Push(new Subscript(container3, new Slice(lower3, upper3, null), ExpressionContext.Load));
                return null;
            }
            case Opcode.STORE_SLICE_0: // TOS[TOS1] = TOS2 → store slice
            case Opcode.STORE_SLICE_1:
            case Opcode.STORE_SLICE_2:
            case Opcode.STORE_SLICE_3:
            case Opcode.DELETE_SLICE_0: // del slice
            case Opcode.DELETE_SLICE_1:
            case Opcode.DELETE_SLICE_2:
            case Opcode.DELETE_SLICE_3:
                // Skip for now — consume stack items to avoid leaking
                SafePop(); SafePop(); SafePop();
                return null;

            // ---- BUILD_SLICE (3.5-3.10: items[1:10]) ----
            case Opcode.BUILD_SLICE:
            {
                var arg = instr.Argument ?? 0;
                // BUILD_SLICE arg=2: [lower, upper]  arg=3: [lower, upper, step]
                Expr? step = null;
                if (arg >= 3)
                    step = SafePop();
                var upper = SafePop();
                var lower = SafePop();
                if (lower == null) lower = new Constant(null);
                if (upper == null) upper = new Constant(null);
                var slice = new Slice(lower, upper, step);
                _exprStack.Push(slice);
                return null;
            }

            // ---- 一元运算 ----
            case Opcode.UNARY_NEGATIVE:
            {
                var op = SafePop();
                if (op == null) return null;
                _exprStack.Push(new UnaryOp(UnaryOperator.USub, op));
                return null;
            }
            case Opcode.UNARY_NOT:
            {
                var op = SafePop();
                if (op == null) return null;
                _exprStack.Push(new UnaryOp(UnaryOperator.Not, op));
                return null;
            }
            case Opcode.UNARY_INVERT:
            {
                var op = SafePop();
                if (op == null) return null;
                _exprStack.Push(new UnaryOp(UnaryOperator.Invert, op));
                return null;
            }

            // ---- 返回 ----
            case Opcode.RETURN_VALUE:
            {
                var retValue = SafePop();
                return new Return(retValue);
            }

            // ---- 栈操作 ----
            case Opcode.POP_TOP:
            {
                var popped = SafePop();
                // for 循环体中的 POP_TOP = break（即使栈为空）
                if (_isForLoop)
                    return new Break();
                if (popped != null)
                    return new ExprStmt(popped);
                return null;
            }

            case Opcode.DUP_TOP:
            {
                var top = SafePeek();
                if (top != null) _exprStack.Push(top);
                return null;
            }
 
            // ---- 比较 ----
            case Opcode.COMPARE_OP:
            {
                var cmpRight = SafePop();
                var cmpLeft = SafePop();
                if (cmpLeft == null || cmpRight == null) return null;
                // CPython 比较码：0=<, 1=<=, 2===, 3=!=, 4=>, 5=>=, 6=in, 7=not in, 8=is, 9=is not
                var pyOp = instr.Argument ?? 0;
                var cmpOp = pyOp switch
                {
                    0 => CmpOp.Lt,
                    1 => CmpOp.LtE,
                    2 => CmpOp.Eq,
                    3 => CmpOp.NotEq,
                    4 => CmpOp.Gt,
                    5 => CmpOp.GtE,
                    6 => CmpOp.In,
                    7 => CmpOp.NotIn,
                    8 => CmpOp.Is,
                    9 => CmpOp.IsNot,
                    _ => CmpOp.Eq
                };
                _exprStack.Push(new Compare(cmpLeft, new List<CmpOp> { cmpOp }, new List<Expr> { cmpRight }));
                return null;
            }

            // ---- IS_OP (3.9+) — 非跳转，相当于 COMPARE_OP is/is not ----
            case Opcode.IS_OP:
            {
                // Stack: ... value1, value2 → pop both, push boolean
                var right = SafePop();
                var left = SafePop();
                if (left == null || right == null) return null;
                var arg = instr.Argument ?? 0;
                var isOp = arg == 0 ? CmpOp.Is : CmpOp.IsNot;
                _exprStack.Push(new Compare(left, new List<CmpOp> { isOp }, new List<Expr> { right }));
                return null;
            }

            // ---- CONTAINS_OP (3.9+) — 非跳转，相当于 COMPARE_OP in/not in ----
            case Opcode.CONTAINS_OP:
            {
                var right = SafePop(); // container
                var left = SafePop();  // element
                if (left == null || right == null) return null;
                var arg = instr.Argument ?? 0;
                var containsOp = arg == 0 ? CmpOp.In : CmpOp.NotIn;
                _exprStack.Push(new Compare(left, new List<CmpOp> { containsOp }, new List<Expr> { right }));
                return null;
            }

            // ---- 函数调用 ----
            case Opcode.CALL_FUNCTION:
            {
                var argCount = instr.Argument ?? 0;
                var args = new List<Expr>();
                for (int i = 0; i < argCount && _exprStack.Count > 0; i++)
                {
                    var a = SafePop();
                    if (a != null) args.Insert(0, a);
                }
                var func = SafePop();
                if (func == null) return null;
                _exprStack.Push(new Call(func, args, new List<Keyword>()));
                return null;
            }

            case Opcode.CALL_METHOD:
            {
                // Python 3.7-3.9: CALL_METHOD pops method, self, then args
                // Stack: [method, self, arg0, arg1, ...] → pop argCount+2 elements total
                var callArgCount = instr.Argument ?? 0;
                var callArgs = new List<Expr>();
                for (int i = 0; i < callArgCount && _exprStack.Count > 0; i++)
                {
                    var a = SafePop();
                    if (a != null) callArgs.Insert(0, a);
                }
                SafePop(); // self (not needed for the call expression)
                var method = SafePop();
                if (method == null) return null;
                _exprStack.Push(new Call(method, callArgs, new List<Keyword>()));
                return null;
            }

            case Opcode.LOAD_METHOD:
            {
                // Python 3.7-3.9: pops obj, pushes (method, self)
                // Stack after: [method_expr, self_obj]
                // CALL_METHOD will consume: pop self, pop method, pop args
                var methodName = GetName(instr);
                var obj = SafePop();
                if (obj == null) return null;
                var attr = new Models.AST.Attribute(obj, methodName, ExpressionContext.Load);
                // Push method expression first (top of stack for CALL_METHOD)
                _exprStack.Push(attr);
                // Push self reference below (so CALL_METHOD pops it first as "self")
                _exprStack.Push(obj);
                return null;
            }
            case Opcode.CALL_FUNCTION_EX:
                return null; // Skip for now

            // ---- Print（Python 2.7）----
            case Opcode.PRINT_ITEM:
            {
                var val = SafePop();
                if (val != null)
                    _printItems.Add(val);
                return null;
            }
            case Opcode.PRINT_NEWLINE:
            {
                if (_printItems.Count > 0)
                {
                    var items = new List<Expr>(_printItems);
                    _printItems.Clear();
                    var printCall = new Call(new Name("print", ExpressionContext.Load), items, new());
                    return new ExprStmt(printCall);
                }
                return new ExprStmt(new Call(new Name("print", ExpressionContext.Load), new(), new()));
            }
            case Opcode.PRINT_EXPR:
            {
                var val = SafePop();
                if (val != null)
                    return new ExprStmt(val);
                return null;
            }
            case Opcode.PRINT_ITEM_TO:
            {
                // print >> dest, val — 重定向输出到 dest
                var val = SafePop();
                var dest = SafePop(); // dest 在 val 下面
                if (val != null && dest != null)
                    _printItems.Add(val);
                if (dest != null)
                    _printItems.Insert(0, dest); // dest 作为第一个参数（便于print调用）
                return null;
            }
            case Opcode.PRINT_NEWLINE_TO:
            {
                // print >> expr — 重定向输出结束，忽略 dest
                SafePop(); // pop destination
                if (_printItems.Count > 0)
                {
                    var items = new List<Expr>(_printItems);
                    _printItems.Clear();
                    var printCall = new Call(new Name("print", ExpressionContext.Load), items, new());
                    return new ExprStmt(printCall);
                }
                return null;
            }

            // ---- NOP and safe-to-skip opcodes ----
            case Opcode.NOP:
            case Opcode.RESUME:
            case Opcode.YIELD_FROM_PY310:
            case Opcode.YIELD_FROM:
            {
                // Python 3.5-3.10: YIELD_FROM
                // 栈: [... iter_expr, initial_send_value(None)]
                // pop TOS (initial send value, 通常是 None, 丢弃)
                // pop TOS1 (迭代器表达式)
                // 输出: yield from <iter_expr>
                var initialSend = SafePop();  // 丢弃
                var iterExpr = SafePop();
                if (iterExpr != null)
                    return new YieldFrom(iterExpr);
                return null;
            }
            case Opcode.POP_EXCEPT:
            case Opcode.SETUP_ANNOTATIONS:
            case Opcode.SETUP_FINALLY:
            case Opcode.BEFORE_WITH:
            case Opcode.WITH_EXCEPT_START:
            case Opcode.PUSH_EXC_INFO:
            case Opcode.PUSH_NULL:
            case Opcode.SETUP_WITH:
            case Opcode.SEND:
                return null;
            case Opcode.RAISE_VARARGS:
            {
                var oparg = instr.Argument ?? 0;
                if (oparg == 0)
                    return new Raise();  // bare raise
                if (oparg == 1)
                {
                    var exc = SafePop();
                    return new Raise(exc);
                }
                // oparg == 2: raise X from Y
                var cause = SafePop();
                var exc2 = SafePop();
                return new Raise(exc2, cause);
            }

            // ---- Jump opcodes (handled by BlockScanner) ----
            case Opcode.JUMP_FORWARD:
            case Opcode.JUMP_BACKWARD:
            case Opcode.JUMP_BACKWARD_NO_INTERRUPT:
            case Opcode.JUMP_IF_TRUE_OR_POP:
            case Opcode.JUMP_IF_FALSE_OR_POP:
                return null;

            case Opcode.JUMP_ABSOLUTE:
                // 跳转到循环头 → continue
                if (instr.Argument.HasValue && _loopHeaderOffsets.Contains(instr.Argument.Value))
                    return new Continue();
                return null;

            case Opcode.POP_JUMP_IF_TRUE:
            case Opcode.POP_JUMP_IF_FALSE:
                return null;

            case Opcode.FOR_ITER:
                return null;

            // ---- Import ----
            case Opcode.IMPORT_NAME:
            {
                SafePop(); // fromlist
                SafePop(); // level
                var modName = GetName(instr);
                _exprStack.Push(new Name(modName, ExpressionContext.Load));
                return null;
            }

            case Opcode.IMPORT_FROM:
            {
                var impName = GetName(instr);
                var mod = SafePeek();
                if (mod == null) return null;
                _exprStack.Push(new AstAttribute(mod, impName, ExpressionContext.Load) { IsImportFrom = true });
                return null;
            }

            case Opcode.GET_ITER:
                return null;

            case Opcode.GET_YIELD_FROM_ITER:
                // GET_YIELD_FROM_ITER: TOS = iter(TOS)，对 AST 透明
                return null;

            case Opcode.MAKE_FUNCTION:
            {
                // v2.7: 栈顶只有 code object（无 qualname）
                // v3.3+: 栈顶 → [defaults?, kwdefaults?, annotations?, closure?, qualname, code]
                string funcName = "<lambda>";
                CodeObject? childCode = null;

                if (_code.IsPython27)
                {
                    // v2.7: 只有 code object
                    var codeExpr = SafePop();
                    if (codeExpr is Constant c && c.Value is CodeObject co)
                        childCode = co;
                    funcName = childCode?.Name ?? "<lambda>";
                }
                else
                {
                    // v3.3+: pop qualname + code
                    var qualNameExpr = SafePop();
                    var codeExpr = SafePop();

                    funcName = qualNameExpr switch
                    {
                        Constant c when c.Value is string s => s,
                        _ => "<lambda>"
                    };

                    if (codeExpr is Constant c2 && c2.Value is CodeObject co)
                        childCode = co;
                }

                _exprStack.Push(new FunctionRef(childCode, funcName));
                return null;
            }

            case Opcode.LOAD_BUILD_CLASS:
                _exprStack.Push(new Name("__build_class__", ExpressionContext.Load));
                return null;

            case Opcode.YIELD_VALUE:
            {
                var yielded = SafePop();
                return new Yield(yielded);
            }

            case Opcode.BUILD_STRING:
            {
                var count = instr.Argument ?? 0;
                var parts = new List<Expr>();
                for (int i = 0; i < count && _exprStack.Count > 0; i++)
                {
                    var p = SafePop();
                    if (p != null) parts.Insert(0, p);
                }
                _exprStack.Push(new JoinedStr(parts));
                return null;
            }

            // ---- STORE_SUBSCR (a[b] = c) ----
            case Opcode.STORE_SUBSCR:
            {
                SafePop(); // value
                SafePop(); // key/index
                SafePop(); // object
                return null;
            }

            default:
                // Instead of crashing, create a comment to preserve surrounding block
                return null; // Skip unknown opcodes — block becomes partial output
        }
    }

    private Stmt? HandleBinaryOp(Operator op)
    {
        if (_exprStack.Count < 2) return null;
        var right = _exprStack.Pop();
        var left = _exprStack.Pop();
        _exprStack.Push(new BinOp(left, op, right));
        return null;
    }

    private string GetName(Instruction instr)
    {
        var idx = instr.Argument ?? 0;
        if (idx < _code.Names.Count)
        {
            var name = _code.Names[idx];
            if (!string.IsNullOrEmpty(name)) return name;
        }
        // Try child code object names as fallback
        foreach (var child in _code.ChildCodes)
        {
            if (idx < child.Names.Count && !string.IsNullOrEmpty(child.Names[idx]))
                return child.Names[idx];
        }
        return $"name_{idx}";
    }

    private string GetVarname(Instruction instr)
    {
        var idx = instr.Argument ?? 0;
        if (idx < _code.Varnames.Count)
        {
            var name = _code.Varnames[idx];
            if (!string.IsNullOrEmpty(name)) return name;
        }
        foreach (var child in _code.ChildCodes)
        {
            if (idx < child.Varnames.Count && !string.IsNullOrEmpty(child.Varnames[idx]))
                return child.Varnames[idx];
        }
        return $"var_{idx}";
    }
}
