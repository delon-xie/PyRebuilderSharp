using PyRebuilderSharp.Core.Models.AST;
using AstAttribute = PyRebuilderSharp.Core.Models.AST.Attribute;
using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Versioning;

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

    private int _pendingCopyDepth = -1; // 用于 walrus := 检测
    private Expr? _pendingUnpackContainer; // 待处理的元组解包容器
    private List<Expr>? _pendingUnpackTargets; // 待处理的元组解包目标列表

    public StackMachine(CodeObject code)
    {
        _code = code;
        _loopHeaderOffsets = new HashSet<int>();
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
        _code.DecompiledInstructionOffsets.Add(instr.Offset);
        switch (instr.Opcode)
        {
            // ---- 常量加载 ----
            case Opcode.LOAD_CONST:
                var value = _code.Constants.TryGetValue(instr.Argument ?? 0, out var v) ? v : null;
                _exprStack.Push(new Constant(value));
                return null;

            // ---- 3.14 新操作码 ----
            case Opcode.LOAD_SMALL_INT_314:
                // LOAD_SMALL_INT: arg 本身就是小整数值（0-255）
                _exprStack.Push(new Constant((long)(instr.Argument ?? 0)));
                return null;

            case Opcode.LOAD_COMMON_CONSTANT_314:
                // LOAD_COMMON_CONSTANT: arg 映射到常见常量
                // CPython 3.14: 0=None, 1=True, 2=False, 3=Ellipsis
                var commonIdx = instr.Argument ?? 0;
                object? commonVal;
                switch (commonIdx)
                {
                    case 0: commonVal = null; break;
                    case 1: commonVal = true; break;
                    case 2: commonVal = false; break;
                    default: commonVal = null; break;
                }
                _exprStack.Push(new Constant(commonVal));
                return null;

            case Opcode.LOAD_SPECIAL_314:
                // LOAD_SPECIAL: arg 映射到特殊名称
                // CPython 3.14: 0=__name__, 1=__module__, 2=__qualname__
                var specialName = (instr.Argument ?? 0) switch
                {
                    0 => "__name__",
                    1 => "__module__",
                    2 => "__qualname__",
                    _ => $"__special_{instr.Argument}__"
                };
                _exprStack.Push(new Name(specialName, ExpressionContext.Load));
                return null;

            case Opcode.LOAD_FAST_BORROW_314:
                // LOAD_FAST_BORROW: 同 LOAD_FAST（借用引用，语义等价）
                var borrowName = GetVarname(instr);
                _exprStack.Push(new Name(borrowName, ExpressionContext.Load));
                return null;

            case Opcode.LOAD_FAST_BORROW_LOAD_FAST_BORROW_314:
                // 双 borrow-load: 连续加载两个局部变量
                // CPython 3.14 wordcode: 1-byte arg packs two 4-bit indices
                //   arg & 0x0F = var1 index (low 4 bits)
                //   arg >> 4   = var2 index (high 4 bits)
                var packedArg = instr.Argument ?? 0;
                int idxA = packedArg & 0x0F;
                int idxB = packedArg >> 4;
                var nameA = idxA < _code.Varnames.Count ? _code.Varnames[idxA] : $"v_{idxA}";
                var nameB = idxB < _code.Varnames.Count ? _code.Varnames[idxB] : $"v_{idxB}";
                _exprStack.Push(new Name(nameA, ExpressionContext.Load));
                _exprStack.Push(new Name(nameB, ExpressionContext.Load));
                return null;

            case Opcode.POP_ITER_314:
                // POP_ITER: 弹出 for 循环迭代器的栈条目
                SafePop();
                return null;

            case Opcode.NOT_TAKEN_314:
                // NOT_TAKEN: JIT 提示标记，无栈效果
                return null;

            case Opcode.BUILD_INTERPOLATION_314:
                // BUILD_INTERPOLATION: f-string 插值构建
                // 当前不构建具体的 f-string AST，后续可扩展
                var interpCount = instr.Argument ?? 0;
                for (int _ = 0; _ < interpCount; _++)
                    SafePop();
                _exprStack.Push(new Constant("<f-string>"));
                return null;

            case Opcode.BINARY_OP_INPLACE_ADD_UNICODE_314:
                // BINARY_OP_INPLACE_ADD_UNICODE: 原地 Unicode 加法
                var rhs = SafePop();
                var lhs = SafePop();
                if (lhs != null && rhs != null)
                    _exprStack.Push(new BinOp(lhs, Models.AST.Operator.Add, rhs));
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

            case Opcode.LOAD_DEREF:
            {
                var idx = instr.Argument ?? 0;
                string cellName;
                if (idx < _code.Cellvars.Count)
                    cellName = _code.Cellvars[idx];
                else if (idx - _code.Cellvars.Count < _code.Freevars.Count)
                    cellName = _code.Freevars[idx - _code.Cellvars.Count];
                else
                    cellName = $"cell_{idx}";
                _exprStack.Push(new Name(cellName, ExpressionContext.Load));
                return null;
            }

            case Opcode.STORE_NAME:
            {
                var storeName = GetName(instr);
                var val = SafePop();
                if (val == null) return null;
                // walrus := detected: COPY followed by STORE_NAME
                if (_pendingCopyDepth >= 0)
                {
                    _pendingCopyDepth = -1;
                    _exprStack.Push(new NamedExpr(new Name(storeName, ExpressionContext.Store), val));
                    return null;
                }
                return new Assign(new List<Expr> { new Name(storeName, ExpressionContext.Store) }, val);
            }

            case Opcode.STORE_FAST:
            {
                var storeLocal = GetVarname(instr);
                var val = SafePop();
                if (val == null) return null;
                // walrus := detected: COPY followed by STORE_FAST
                if (_pendingCopyDepth >= 0)
                {
                    _pendingCopyDepth = -1;
                    _exprStack.Push(new NamedExpr(new Name(storeLocal, ExpressionContext.Store), val));
                    return null;
                }
                // If there's a pending unpack, accumulate this STORE_FAST as a target
                if (_pendingUnpackContainer != null)
                {
                    _pendingUnpackTargets!.Add(new Name(storeLocal, ExpressionContext.Store));
                    
                    // Check if more Starred items remain
                    bool hasMoreStarred = false;
                    foreach (var e in _exprStack)
                    {
                        if (e is Starred s && s.Value == _pendingUnpackContainer && s.Ctx == ExpressionContext.Load)
                        { hasMoreStarred = true; break; }
                    }
                    if (!hasMoreStarred)
                    {
                        var container = _pendingUnpackContainer;
                        var allTargets = _pendingUnpackTargets;
                        _pendingUnpackContainer = null;
                        _pendingUnpackTargets = null;
                        return new Assign(
                            new List<Expr> { new ListLiteral(allTargets!, ContainerKind.Tuple) }, container);
                    }
                    return null; // Still waiting
                }
                
                // UNPACK_SEQUENCE with Starred: start collecting tuple targets
                if (val is Starred starred && starred.Ctx == ExpressionContext.Load)
                {
                    var targets = new List<Expr> { new Name(storeLocal, ExpressionContext.Store) };
                    _pendingUnpackContainer = starred.Value;
                    _pendingUnpackTargets = targets;
                    
                    // Check if more Starred items remain
                    bool hasMoreStarred = false;
                    foreach (var e in _exprStack)
                    {
                        if (e is Starred s && s.Value == starred.Value && s.Ctx == ExpressionContext.Load)
                        { hasMoreStarred = true; break; }
                    }
                    if (!hasMoreStarred)
                    {
                        // Single-item unpack — emit immediately
                        _pendingUnpackContainer = null;
                        _pendingUnpackTargets = null;
                        return new Assign(
                            new List<Expr> { new ListLiteral(targets, ContainerKind.Tuple) }, starred.Value);
                    }
                    return null; // Wait for more STORE_FAST instructions
                }
                
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
                // 3.10-: stack = [value, object]; TOS=object (conventional LOAD order)
                // 3.13+: stack = [object, value]; TOS=value (LOAD_FAST_BORROW dual-load order)
                // See CPython Python/generated_cases.c.h: POP()=value, POP()=owner
                Expr? attrValue, obj;
                if (_code.Version >= PythonVersion.Py313)
                {
                    attrValue = SafePop();  // TOS = value (3.13+ convention)
                    obj = SafePop();        // TOS1 = object
                }
                else
                {
                    obj = SafePop();        // TOS = object (3.10- convention)
                    attrValue = SafePop();  // TOS1 = value
                }
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

            // ---- f-string: FORMAT_VALUE + BUILD_STRING ----
            case Opcode.FORMAT_VALUE:
            {
                var conversion = (instr.Argument ?? 0) & 0x03;
                int conv = conversion switch { 1 => 's', 2 => 'r', 3 => 'a', _ => -1 };
                var fval = SafePop();
                if (fval == null) return null;
                _exprStack.Push(new FormattedValue(fval, conv));
                return null;
            }

            case Opcode.BUILD_STRING:
            {
                var count = instr.Argument ?? 0;
                var parts = new List<Expr>();
                for (int i = 0; i < count && _exprStack.Count > 0; i++)
                {
                    var part = SafePop();
                    if (part != null) parts.Insert(0, part);
                }
                _exprStack.Push(new JoinedStr(parts));
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
            case Opcode.INPLACE_MULTIPLY: return HandleBinaryOp(Operator.Mul);
            case Opcode.INPLACE_MODULO: return HandleBinaryOp(Operator.Mod);
            case Opcode.INPLACE_POWER: return HandleBinaryOp(Operator.Pow);
            case Opcode.INPLACE_FLOOR_DIVIDE: return HandleBinaryOp(Operator.FloorDiv);
            case Opcode.INPLACE_TRUE_DIVIDE: return HandleBinaryOp(Operator.Div);
            case Opcode.INPLACE_AND: return HandleBinaryOp(Operator.BitAnd);
            case Opcode.INPLACE_OR: return HandleBinaryOp(Operator.BitOr);
            case Opcode.INPLACE_XOR: return HandleBinaryOp(Operator.BitXor);
            case Opcode.INPLACE_LSHIFT: return HandleBinaryOp(Operator.LShift);
            case Opcode.INPLACE_RSHIFT: return HandleBinaryOp(Operator.RShift);
            case Opcode.INPLACE_MATRIX_MULTIPLY: return HandleBinaryOp(Operator.MatMul);

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
                // for 循环体中的 POP_TOP：仅当栈为空时才生成 Break。
                // 若有表达式（如 `abstracts.add(name)` 的返回值），则作为正常 ExprStmt。
                // 参考 CPython 3.10: POP_TOP 在 for 循环体尾部用于丢弃循环变量值，
                // 但调用表达式的返回值的 POP_TOP 属于语句体的一部分。
                if (_isForLoop && popped == null)
                    return new Break();
                if (popped != null)
                {
                    // import-from 产生的模块名是中间值，不是有效语句
                    if (popped is Name n && n.IsImport)
                        return null;
                    return new ExprStmt(popped);
                }
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
                var pyOp = instr.Argument ?? 0;

                // 3.12+ encodes comparison type in upper bits, flags in lower bits:
                //   3.12: oparg >> 4 = comparison index
                //   3.13+: oparg >> 5 = comparison index
                // 3.11-: oparg is the comparison index directly (0-9)
                int cmpIdx;
                if (_code.Version is PythonVersion.Py312)
                    cmpIdx = pyOp >> 4;
                else if (_code.Version >= PythonVersion.Py313)
                    cmpIdx = pyOp >> 5;
                else
                    cmpIdx = pyOp;

                // Standard comparison indices:
                //   0=Lt, 1=LtE, 2=Eq, 3=NotEq, 4=Gt, 5=GtE, 6=In, 7=NotIn, 8=Is, 9=IsNot
                // Note: IS_OP and CONTAINS_OP are separate opcodes in 3.9+;
                // for 3.8- they are encoded as indices 6-9 in COMPARE_OP.
                var cmpOp = cmpIdx switch
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
                    _ => CmpOp.Eq,
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
            {
                var flags = instr.Argument ?? 0;
                var args = new List<Expr>();
                var keywords = new List<Keyword>();
                
                // CPython 3.10 implementation (ceval.c):
                // Stack: [func, args, kwargs]  — kwargs TOS, args TOS1, func TOS2
                // flags & 0x01 = kwargs dict is present (dict on TOS)
                // flags & 0x02 = args tuple is present (tuple on TOS1)
                // Even when a flag is 0, the corresponding value IS on the stack,
                // it just means kwargs=None or args=empty_tuple.
                // But for decompilation: always pop both then func.
                
                var kwargsExpr = SafePop(); // TOS = kwargs dict or None
                var argsExpr = SafePop();   // TOS1 = args tuple
                var func = SafePop();       // TOS2 = func
                if (func == null) return null;
                
                if (argsExpr is ListLiteral listLit)
                    args.AddRange(listLit.Elts);
                
                if (kwargsExpr != null)
                {
                    if (kwargsExpr is Name kn)
                        keywords.Add(new Keyword(null, kn));
                    else
                        keywords.Add(new Keyword(null, kwargsExpr));
                }
                
                var call = new Call(func, args, keywords);
                _exprStack.Push(call);
                return null;
            }

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

            // ---- 3.11+ no-ops (safe to skip) ----
            case Opcode.NOP:
            case Opcode.RESUME:
            case Opcode.INTERPRETER_EXIT:
            case Opcode.COPY_FREE_VARS:
            case Opcode.SETUP_ANNOTATIONS:
                return null;

            // ---- 3.11+ BINARY_OP (arg 指定操作类型) ----
            // 注意: CPython 3.13+ 扩展了 BINARY_OP, arg=26 = subscript ([])
            case Opcode.BINARY_OP:
            {
                var opType = instr.Argument ?? 0;

                // CPython 3.13+: BINARY_OP arg=26 is subscript (a[b])
                // See Python/bytecodes.c: BINARY_OP with oparg 26 = BINARY_SUBSCR
                if (opType == 26)
                {
                    var idx = SafePop();
                    var obj = SafePop();
                    if (idx == null || obj == null) return null;
                    _exprStack.Push(new Subscript(obj, idx, ExpressionContext.Load));
                    return null;
                }

                // pop TOS, TOS1 → push BinOp(TOS1, op, TOS)
                var right = SafePop();
                var left = SafePop();
                if (left == null || right == null) return null;
                var binOp = MapBinaryOpArg(opType);
                _exprStack.Push(new BinOp(left, binOp, right));
                return null;
            }

            // ---- 3.13+ BINARY_SLICE: name[start:end] (replaces BUILD_SLICE+BINARY_SUBSCR) ----
            // CPython 3.13+: pops (container, start, end) from stack, pushes subscript-slice
            // See Python/bytecodes.c: BINARY_SLICE = 'obj[slice(start, end)]'
            case Opcode.BINARY_SLICE_313:
            {
                var end = SafePop();
                var start = SafePop();
                var container = SafePop();
                if (container == null) return null;
                if (start == null) start = new Constant(null);
                if (end == null) end = new Constant(null);
                _exprStack.Push(new Subscript(container, new Slice(start, end, null), ExpressionContext.Load));
                return null;
            }

            // ---- 3.11+ RETURN_CONST: LOAD_CONST + RETURN_VALUE combined ----
            case Opcode.RETURN_CONST:
            case Opcode.RETURN_CONST_313:
            {
                var constIdx = instr.Argument ?? 0;
                var retConst = _code.Constants.TryGetValue(constIdx, out var cv) ? cv : null;
                return new Return(new Constant(retConst));
            }

            // ---- 3.11+ PUSH_NULL: call protocol marker ----
            // NOTE: ROT_TWO and PUSH_NULL share enum value 2 (same raw byte 02 in 3.11+)
            // In 3.11+, raw byte 02 = PUSH_NULL. In 3.10-, raw byte 02 = ROT_TWO.
            // Since both are 2 in the enum, only ROT_TWO appears in the switch.
            // For 3.11+, treat as PUSH_NULL (push null sentinel for call protocol).
            // For 3.10-: ROT_TWO was never handled (fell through to default → null),
            // which broke SEND/JUMP_BACKWARD patterns. For now, still return null.
            case Opcode.ROT_TWO:
                // 在 3.12+ 调用协议中，PUSH_NULL 标记"我需要一个函数对象"
                // 参考 CPython 3.12: Include/internal/pycore_opcode.h PUSH_NULL=2
                // 3.11: PRECALL_311/CALL_311 协议，CALL opcode (171) 不存在
                // 3.12+: CALL opcode (171) 引入，PUSH_NULL 在调用前压入 null 哨兵
                if (_code.Version is PythonVersion.Py312 or PythonVersion.Py313 or PythonVersion.Py314)
                {
                    _exprStack.Push(new Constant(null));  // sentinel null
                    return null;
                }
                // Fall through to default for pre-3.11 (ROT_TWO not supported)
                return null;

            // ---- 3.11+ COPY: duplicate TOS[n] ----
            case Opcode.COPY:
            case Opcode.COPY_FREE_VARS_313:
            {
                var depth = instr.Argument ?? 0;
                // COPY n: duplicate the element n positions below TOS
                // In Python 3.12, COPY n copies stack[-1-n]. For walrus := pattern,
                // COPY 1 is used with only 1 element on stack — copy TOS.
                if (depth == 0 || depth > _exprStack.Count)
                {
                    var top = SafePeek();
                    if (top != null) _exprStack.Push(top);
                    _pendingCopyDepth = (int)depth;
                }
                else
                {
                    // COPY n: push stack[-n], where stack[-1]=TOS.
                    // In reversed array: TOS is at lastIdx, TOS1 at lastIdx-1.
                    var arr = _exprStack.ToArray();
                    Array.Reverse(arr);
                    int lastIdx = arr.Length - 1;
                    int idx = lastIdx - (int)depth + 1;
                    if (idx >= 0 && idx < arr.Length)
                        _exprStack.Push(arr[idx]);
                    _pendingCopyDepth = (int)depth;
                }
                return null;
            }

            // ---- 3.11+ SWAP: swap TOS and TOS[n] ----
            case Opcode.SWAP:
            {
                var depth = instr.Argument ?? 0;
                // SWAP n: swap TOS with item at depth n below TOS
                // depth=1: swap TOS and TOS1 (standard two-item swap)
                // depth=2: swap TOS and TOS2 (e.g., SWAP 2 in 3.13+)
                if (depth >= 1 && depth <= _exprStack.Count)
                {
                    // Convert stack to array, reverse (bottom→top), swap positions
                    var arr = _exprStack.ToArray();
                    Array.Reverse(arr);
                    int lastIdx = arr.Length - 1;
                    // CPython: SWAP n swaps TOS (reversed[lastIdx]) with stack[-n]
                    // where stack[-1]=TOS, stack[-2]=TOS1, etc.
                    // In reversed array: TOS is at lastIdx, TOS1 at lastIdx-1, etc.
                    // So swap TOS with reversed[lastIdx - depth + 1]
                    int swapIdx = lastIdx - (int)depth + 1;
                    if (swapIdx >= 0 && swapIdx < arr.Length)
                    {
                        (arr[lastIdx], arr[swapIdx]) = (arr[swapIdx], arr[lastIdx]);
                        _exprStack.Clear();
                        Array.Reverse(arr);
                        for (int i = 0; i < arr.Length; i++)
                            _exprStack.Push(arr[i]);
                    }
                }
                return null;
            }

            // ---- 3.11+ CALL / CALL_311: new call protocol ----
            case Opcode.CALL:
            case Opcode.CALL_311:
            case Opcode.CALL_KW_313:
            {
                var argCount = instr.Argument ?? 0;
                // In 3.11+: stack = [..., PUSH_NULL?, func, arg0, arg1, ...]
                // For 3.12: CALL arg = number of positional args
                // For 3.11: CALL_311 arg = same, PRECALL_311 handled separately
                var args = new List<Expr>();
                for (int i = 0; i < argCount && _exprStack.Count > 0; i++)
                {
                    var a = SafePop();
                    if (a != null) args.Insert(0, a);
                }
                
                var func = SafePop();
                // 3.14+: PUSH_NULL 可能在函数之后（栈: [func, NULL, ...]），
                // 而非 3.12-3.13 的之前（栈: [NULL, func, ...]）。
                // 参考 CPython 3.14 调用协议变化。
                if (func is Constant { Value: null })
                {
                    // PUSH_NULL sentinel was on top — pop the real function
                    if (_exprStack.Count > 0)
                        func = SafePop();
                    else
                        return null;
                }
                else if (func == null)
                {
                    return null;
                }

                // If TOS is a null sentinel (PUSH_NULL), pop it
                var peeked = SafePeek();
                if (peeked is Constant { Value: null })
                {
                    _exprStack.Pop(); // discard null sentinel
                }
                
                // Create a dummy Call to capture the null sentinel issue
                // If the null sentinel exists, wrap as call; otherwise just treat as func(args)
                var call = new Call(func, args, new List<Keyword>());
                _exprStack.Push(call);
                return null;
            }

            // ---- 3.5-3.10 CALL_FUNCTION_KW: call with keyword args ----
            case Opcode.CALL_FUNCTION_KW:
            {
                // Stack: [func, arg0, arg1, ..., argN-1, keyword_names_tuple]
                // keyword_names_tuple = (kw_name0, kw_name1, ...)
                // arg = total number of arguments (positional + keyword)
                var totalArgs = instr.Argument ?? 0;
                var keywordNames = SafePop(); // TOS = keyword names tuple
                var args = new List<Expr>();
                var keywords = new List<Keyword>();
                
                // Pop all arguments
                var argValues = new List<Expr>();
                for (int i = 0; i < totalArgs && _exprStack.Count > 0; i++)
                {
                    var a = SafePop();
                    if (a != null) argValues.Insert(0, a);
                }
                var func = SafePop();
                if (func == null) return null;
                
                // Determine which args are positional vs keyword using keyword_names tuple
                if (keywordNames is Constant kn && kn.Value is System.Collections.IList nameList)
                {
                    int kwCount = nameList.Count;
                    int posCount = totalArgs - kwCount;
                    for (int i = 0; i < posCount && i < argValues.Count; i++)
                        args.Add(argValues[i]);
                    for (int i = 0; i < kwCount && posCount + i < argValues.Count; i++)
                    {
                        var kwName = nameList[i]?.ToString() ?? "";
                        keywords.Add(new Keyword(kwName, argValues[posCount + i]));
                    }
                }
                else
                {
                    // Fallback: all args are positional
                    args.AddRange(argValues);
                }
                
                _exprStack.Push(new Call(func, args, keywords));
                return null;
            }

            // ---- DICT_MERGE: merge dict for **kwargs ----
            case Opcode.DICT_MERGE:
            {
                // Stack: [..., target_dict, source_dict]
                // TOS = source_dict (kwargs), TOS1 = target_dict (empty BUILD_MAP)
                var source = SafePop(); // kwargs dict
                SafePop(); // empty dict from BUILD_MAP
                if (source != null)
                    _exprStack.Push(source);
                return null;
            }

            // ---- 3.11 PRECALL_311: prepare call (3.11 only) ----
            case Opcode.PRECALL_311:
            {
                // PRECALL marks the boundary between args and function on stack.
                // In 3.11, CALL follows and actually executes.
                // For decompilation: PRECALL is a no-op because CALL_311 handles the actual args.
                // The arg is the number of positional args (same as CALL's arg).
                return null;
            }

            // ---- 3.11+ KW_NAMES: keyword arg names for CALL ----
            case Opcode.KW_NAMES:
            {
                // KW_NAMES stores keyword argument name tuple index.
                // The actual keyword values are on the stack after positional args.
                // For now: skip — keywords are handled via simplifications
                return null;
            }

            // ---- 3.11+ LOAD_FAST_AND_CLEAR: load var then clear it (try/except) ----
            case Opcode.LOAD_FAST_AND_CLEAR:
            {
                var varName = GetVarname(instr);
                _exprStack.Push(new Name(varName, ExpressionContext.Load));
                return null;
            }

            // ---- 3.11+ LOAD_FAST_CHECK: like LOAD_FAST with error on unbound ----
            case Opcode.LOAD_FAST_CHECK:
            {
                var checkName = GetVarname(instr);
                _exprStack.Push(new Name(checkName, ExpressionContext.Load));
                return null;
            }

            // ---- 3.11+ SEND: generator send ----
            case Opcode.SEND:
            {
                // SEND pops two: generator, send_value
                // For AST: treat like yield from
                var sendValue = SafePop();
                var genExpr = SafePop();
                if (genExpr != null)
                    _exprStack.Push(genExpr);  // SEND pushes result; keep gen for now
                return null;
            }

            // ---- 3.11+ POP_JUMP_IF_NOT_NONE / POP_JUMP_IF_NONE ----
            case Opcode.POP_JUMP_IF_NOT_NONE:
            case Opcode.POP_JUMP_IF_NONE:
                // Conditional jumps — handled by BlockScanner/CFG building
                // Pop the condition for stack hygiene
                SafePop();
                return null;

            // ---- 3.12+ BUILD_CONST_KEY_MAP ----
            case Opcode.BUILD_CONST_KEY_MAP:
            {
                // Build map from keys tuple + values
                // Stack: ..., keys_tuple, value0, value1, ..., valueN-1
                // where keys_tuple is a tuple constant with N key names
                var count = instr.Argument ?? 0;
                var entries = new List<(Expr Key, Expr Value)>();
                var keysExpr = SafePop();  // keys tuple
                for (int i = 0; i < count && _exprStack.Count > 0; i++)
                {
                    var val = SafePop();
                    if (val != null && keysExpr != null)
                    {
                        // Extract key name from tuple
                        Expr key;
                        if (keysExpr is Constant c && c.Value is System.Collections.IList list && i < list.Count)
                            key = new Constant(list[i]);
                        else
                            key = new Constant($"key_{i}");
                        entries.Insert(0, (key, val));
                    }
                }
                _exprStack.Push(new DictLiteral(entries));
                return null;
            }

            // ---- 3.12+ exception/with renumbered opcodes ----
            case Opcode.BEFORE_WITH_312:
            case Opcode.WITH_EXCEPT_START_312:
            case Opcode.PUSH_EXC_HANDLER_312:
            case Opcode.PULL_EXC_FROM_INFO_312:
            case Opcode.PUSH_EXC_INFO_312:
            case Opcode.CHECK_EXC_MATCH:
            case Opcode.CHECK_EG_MATCH:
            // 3.10+ match/case: runtime pattern matching, no AST generation
            case Opcode.MATCH_MAPPING_312:
            case Opcode.MATCH_SEQUENCE_312:
            case Opcode.MATCH_KEYS_312:
            case Opcode.MATCH_CLASS_312:
                return null;

            // ---- 3.5-3.10 opcodes that carry through ----
            case Opcode.YIELD_FROM_PY310:
            case Opcode.YIELD_FROM:
            {
                // Python 3.5-3.10: YIELD_FROM
                var initialSend = SafePop();  // 丢弃
                var iterExpr = SafePop();
                if (iterExpr != null)
                    return new YieldFrom(iterExpr);
                return null;
            }

            // ---- UNPACK_SEQUENCE: 展开序列到栈 ----
            case Opcode.UNPACK_SEQUENCE:
            {
                var count = instr.Argument ?? 0;
                var container = SafePop();
                if (container == null) return null;

                for (int i = count - 1; i >= 0; i--)
                    _exprStack.Push(new Starred(container, ExpressionContext.Load));
                return null;
            }

            case Opcode.UNPACK_EX:
            {
                // UNPACK_EX: arg = (num_required_before << 8) | num_required_after
                var rawArg = instr.Argument ?? 0;
                var beforeCount = rawArg >> 8;
                var afterCount = rawArg & 0xFF;
                var container = SafePop();
                if (container == null) return null;
                
                // Push required-before first (will be stored from the right)
                // Then push starred container for the middle
                // Then push required-after 
                for (int i = 0; i < beforeCount; i++)
                    _exprStack.Push(new Starred(container, ExpressionContext.Load));
                // Push the *rest marker as Starred with a special flag
                _exprStack.Push(new Starred(container, ExpressionContext.Store));
                for (int i = 0; i < afterCount; i++)
                    _exprStack.Push(new Starred(container, ExpressionContext.Load));
                return null;
            }

            case Opcode.POP_EXCEPT:
            case Opcode.SETUP_FINALLY:
            case Opcode.BEFORE_WITH:
            case Opcode.WITH_EXCEPT_START:
            case Opcode.PUSH_EXC_INFO:
            case Opcode.SETUP_WITH:
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
                if (oparg == 2)
                {
                    var cause = SafePop();
                    var exc = SafePop();
                    return new Raise(exc, cause);
                }
                return null;
            }
            case Opcode.RERAISE:
                return new Raise();
            
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
                _exprStack.Push(new Name(modName, ExpressionContext.Load) { IsImport = true });
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

            // Python 2.7: from X import *
            case Opcode.IMPORT_STAR_27:
            {
                // IMPORT_STAR 本身没有栈效果 — 只是标记"所有名字都导入"
                return null;
            }

            case Opcode.GET_ITER:
                return null;

            case Opcode.GET_YIELD_FROM_ITER:
                // GET_YIELD_FROM_ITER: TOS = iter(TOS)，对 AST 透明
                return null;

            case Opcode.MAKE_FUNCTION:
            {
                // MAKE_FUNCTION 的栈布局因 Python 版本而异。
                // 参考 CPython:
                //   - 2.7: 栈顶只有 code object（无 qualname）— Python/ceval.c 2.7 make_function
                //   - 3.3-3.11: 栈顶 → defaults?, kwdefaults?, annotations?, closure?, [qualname,] code
                //     3.11 中 qualname 来自 co_qualname，但依旧出现在栈上
                //   - 3.12+: qualname 来自 co_qualname，栈上只有 code object
                //     参见 CPython 3.12: Python/compile.c compiler_make_function
                //     及 Python/ceval.c CALL 协议重构
                string funcName = "<lambda>";
                CodeObject? childCode = null;

                switch (_code.Version)
                {
                    case PythonVersion.Py27:
                        // v2.7: 只有 code object（无 qualname/freevars/cellvars 等复杂栈）
                        // 参考 CPython 2.7: Python/ceval.c line ~2034 MAKE_FUNCTION
                    {
                        var codeExpr = SafePop();
                        if (codeExpr is Constant c && c.Value is CodeObject co)
                            childCode = co;
                        funcName = childCode?.Name ?? "<lambda>";
                        break;
                    }

                    case PythonVersion.Py311:
                    case PythonVersion.Py312:
                    case PythonVersion.Py313:
                    case PythonVersion.Py314:
                        // Python 3.11+: MAKE_FUNCTION pops only code object
                        // 参考 CPython 3.11: Python/ceval.c TARGET(MAKE_FUNCTION)
                        //     ONLY pops code object. qualname no longer on stack.
                        //     PyFunction_New() reads co_qualname from code object.
                    {
                        var codeExpr = SafePop();
                        if (codeExpr is Constant c2 && c2.Value is CodeObject co)
                        {
                            childCode = co;
                            funcName = co.Name ?? "<lambda>";
                        }
                        break;
                    }

                    default:
                        // v3.3-3.11: pop qualname + code
                        // 参考 CPython 3.11: Python/ceval.c MAKE_FUNCTION
                        //     "Pops a code object and a qualified name from the stack."
                    {
                        var qualNameExpr = SafePop();
                        var codeExpr = SafePop();

                        if (qualNameExpr is Constant c3 && c3.Value is string s)
                            funcName = s;

                        if (codeExpr is Constant c2 && c2.Value is CodeObject co)
                            childCode = co;
                        break;
                    }
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

            // ---- STORE_SUBSCR (a[b] = c) ----
            case Opcode.STORE_SUBSCR:
            {
                SafePop(); // value
                SafePop(); // key/index
                SafePop(); // object
                return null;
            }

            // 3.13+ TO_BOOL: convert TOS to boolean (no-op for decompiler, expression unchanged)
            case Opcode.TO_BOOL_313:
                return null;

            // 3.13+ SET_FUNCTION_ATTRIBUTE: set function attribute (closure/defaults/annotations)
            // Pops one value from stack. StackMachine: just skip — output unaffected.
            case Opcode.SET_FUNCTION_ATTRIBUTE_313:
                return null;

            // 3.13+ FORMAT_SIMPLE: f-string simple format (no-op, expression unchanged)
            case Opcode.FORMAT_SIMPLE_313:
                return null;

            // 3.13+ CONVERT_VALUE: convert to repr/str/ascii (no-op for decompiler)
            case Opcode.CONVERT_VALUE_313:
                return null;

            // ---- 3.11+ LIST_APPEND: TOS → append to list at TOS[n] ----
            case Opcode.LIST_APPEND_313:
            {
                var depth = instr.Argument ?? 0;
                // LIST_APPEND n: pop TOS (item), append to list at stack[-n]
                // arg=1: pop item, append to list at TOS1 (the list below the item)
                var item = SafePop();
                if (item == null) return null;
                // The list at stack[-depth] should be a ListLiteral from BUILD_LIST
                // Since records can't be cast/mutated in-place, we pop, modify, push back
                if (_exprStack.Count >= depth && _exprStack.Peek() is ListLiteral listLit)
                {
                    // Only modify if we can find the list — BUILD_LIST already pushed it
                    // ListLiteral.Elts is a mutable List<Expr>; add the new item
                    var elts = listLit.Elts;
                    elts.Add(item);
                }
                return null;
            }

            // 3.13+ CALL_INTRINSIC_1: intrinsic function call type 1
            case Opcode.CALL_INTRINSIC_1_313:
                return null;

            // 3.13+ CALL_INTRINSIC_2: intrinsic function call type 2
            case Opcode.CALL_INTRINSIC_2_313:
                return null;

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

    /// <summary>
    /// 将 3.11+ BINARY_OP 的参数映射到我们统一的 Operator 枚举。
    /// CPython 3.11+ _nb_ops 表：
    ///   0=add, 1=and, 2=floor_div, 3=lshift, 5=mul, 6=mod, 7=or,
    ///   8=pow, 9=rshift, 10=sub, 11=truediv, 12=xor
    ///   13-25 = in-place variants
    /// </summary>
    private static Operator MapBinaryOpArg(int arg)
    {
        return arg switch
        {
            0 => Operator.Add,
            1 => Operator.BitAnd,
            2 => Operator.FloorDiv,
            3 => Operator.LShift,
            5 => Operator.Mul,
            6 => Operator.Mod,
            7 => Operator.BitOr,
            8 => Operator.Pow,
            9 => Operator.RShift,
            10 => Operator.Sub,
            11 => Operator.Div,
            12 => Operator.BitXor,
            // In-place (13-25): same operator, mark as in-place if needed
            >= 13 and <= 25 => MapBinaryOpArg(arg - 13),
            _ => Operator.Add,
        };
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
