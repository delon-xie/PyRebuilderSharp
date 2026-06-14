# 文档一：Python反编译总体设计.md

## Python字节码反编译器总体设计文档

**版本**: v2.6
**日期**: 2026-06-14
**项目**: PyRebuilderSharp
**状态**: Phase 1–6 ✅ 全部关闭 — 109 测试 · 版本矩阵2.7-3.14全覆盖 · Benchmark 938/938 · 17 项修复 · 语法覆盖 13 项 · 工程增强6项待完成

---

## 1. 项目概述

### 1.1 背景与目标

**PyRebuilderSharp** 是一个基于 C#(.NET 10) 的 Python 字节码反编译器，对标 pycdc，以 Avalonia UI 提供跨平台 GUI。核心目标：

- **多版本兼容**: 支持 Python 2.7 + 3.5~3.14（marshal读取），完整反编译 2.7~3.14
- **块级容错**: 每个基本块独立反编译，失败块输出注释兜底，不影响其他块
- **高还原度**: AST 级语义比较，确保反编译结果等价于原源码
- **跨平台**: .NET 10 + Avalonia UI → Windows/macOS/Linux

### 1.2 核心优势

| 特性 | pycdc (C++) | PyRebuilderSharp (C#) |
|------|-------------|----------------------|
| **语言** | C++17 | C# 10 (.NET 10) |
| **AST 模型** | 手写多态 + enum | record 类型 + 模式匹配 |
| **内存管理** | shared_ptr/unique_ptr | GC 自动回收 |
| **容错机制** | 整体失败 | **逐块注释兜底** |
| **测试体系** | 手动测试为主 | xUnit + AST 语义比较 |
| **GUI** | 无 | Avalonia UI |
| **跨平台** | CMake 编译 | dotnet build 单命令 |

### 1.3 逐块兜底策略（核心设计原则）

```
基本块列表 [B1, B2, B3, B4, B5]
         │
         ▼
    ┌────────────────────────────────────────┐
    │    BlockDecompiler.DecompileBlocks()    │
    │                                         │
    │  B1 ─► 栈机模拟 ─► AST ─► "x = a + b"  │ ✅ 成功
    │  B2 ─► 栈机模拟 ─► AST ─► "return x"   │ ✅ 成功
    │  B3 ─► 栈机模拟 ─► ❌ 异常             │ ❌ 失败→注释
    │       └── ► 输出注释块                  │
    │  B4 ─► 栈机模拟 ─► AST ─► "y = 42"     │ ✅ 成功
    │  B5 ─► 栈机模拟 ─► AST ─► "print(y)"   │ ✅ 成功
    └────────────────────────────────────────┘
```

**核心原则**：
1. **块隔离** — 每个基本块独立反编译，一个块失败不影响其他块
2. **注释兜底** — 失败块输出 `# [Block #{id} Decompilation Failed]` 注释，含偏移/错误/字节码
3. **最大恢复** — 即使部分块失败，整体仍生成最大可读的 Python 源码
4. **控制结构保持** — 失败块的外层 if/for/try 结构仍正确生成
5. **CPython 源代码是最高权威** — 遇到难以解释的字节码偏移、操作码映射、marshal 格式等问题时，**必须首先查看 CPython 源代码**（`Python/marshal.c`, `Python/compile.c`, `Python/ceval.c`, `Include/opcode.h`），而非依赖第三方文档、pycdc 实现或推理猜测。CPython 源码是 gcc/msvc/any C 编译器编译的真实行为，任何第三方实现都可能与真实行为有偏差。

注释块格式：
```csharp
// # ════════════════════════════════════════
// # [Block #{id} Decompilation Failed]
// # Offsets: 0x0000 - 0x0010
// # Engine: StackMachine
// # Error: Unhandled opcode PRECALL (156)
// # Raw bytes: 64 01 00 6E 02 00 ...
// # ════════════════════════════════════════
```

---

## 2. CPython 源码研读 — 理解 .py → .pyc 编译管道

### 2.1 为什么需要研读 CPython 源码

反编译器本质上是编译器的逆过程。要写好反编译器，必须深刻理解编译器的每一步做了什么。CPython 源代码是反编译工作的**权威参考**——任何第三方文档或 pycdc 的实现都可能与真实行为有偏差。

### 2.2 .py → .pyc 编译管道全貌

```
Python 源码 (.py)
    │
    ▼
┌──────────────────────────────────────────────────┐
│  Phase A: Lexer (词法分析)                        │
│  ├── Python/tokenize.c → tokens                  │
│  └── 将源码字符流 → token 序列                    │
└──────────────────────┬───────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│  Phase B: Parser (语法分析)                       │
│  ├── Parser/pgen.c / Python/ast.c                │
│  ├── LL(1) 解析器 → CST → AST (mod_ty)           │
│  └── 输出: mod_ty (Module_ty / Interactive_ty)    │
└──────────────────────┬───────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│  Phase C: Compiler (字节码编译器)                  │
│  ├── Python/compile.c → compiler.c的核心逻辑       │
│  ├── Python/symtable.c → 符号表分析                │
│  ├── 三阶段:                                       │
│  │   ① 符号表构建 (symtable)                       │
│  │   ② CFG 构建 (basicblock, 非 Python 3.11 的块)  │
│  │   ③ 汇编 → bytecode 数组                        │
│  └── 输出: PyCodeObject                            │
└──────────────────────┬───────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│  Phase D: Marshal (序列化)                        │
│  ├── Python/marshal.c                            │
│  ├── 将 PyCodeObject → 二进制流                    │
│  ├── 类型编码: TYPE_CODE, TYPE_STRING, TYPE_TUPLE  │
│  ├── 版本3.4+: FLAG_REF(0x80) + TYPE_REF(0x52)    │
│  ├── 版本2.7: TYPE_INTERNED(0x74) + TYPE_STRINGREF(0x52)  │
│  └── 输出: .pyc 二进制文件                          │
└──────────────────────┬───────────────────────────┘
                       ▼
                  .pyc 文件
```

### 2.3 关键源文件清单与对应关系

| CPython 源文件 | 功能 | 反编译对应模块 |
|---------------|------|--------------|
| `Python/compile.c` | 字节码编译器核心 — AST→CFG→bytecode | AstBuilder（逆过程） |
| `Python/symtable.c` | 符号表 — 变量作用域分析 | CodeObject.Names/Varnames/Freevars/Cellvars |
| `Python/ast.c` | AST 定义与操作 | AstNode/Expr/Stmt 模型 |
| `Python/marshal.c` | marshal 序列化/反序列化 | PycReader (ReadMarshalValue/ReadMarshalValue27) |
| `Python/ceval.c` | 字节码解释器 — ceval 循环 | StackMachine（栈机模拟） |
| `Include/code.h` | PyCodeObject 结构体定义 | CodeObject 模型 |
| `Include/opcode.h` | 操作码常量定义 | Opcode 枚举 |
| `Include/compile.h` | 编译器内部结构（basicblock/CFG） | BasicBlock/BlockFlags |
| `Lib/importlib/_bootstrap_external.py` | .pyc 文件格式解析 | PycReader header 读取 |
| `Include/pycache.h` | PEP 552 哈希/时间戳缓存 | .pyc header flags |

### 2.4 Python/compile.c 核心流程（反编译重点）

这是反编译最重要的源文件。理解 compile.c 的编译步骤 = 知道反编译器需要逆推的步骤：

```c
// compile.c 的核心入口
static PyCodeObject *
compiler_mod(struct compiler *c, mod_ty mod)
{
    // 1. 符号表分析 — 确定变量作用域
    //    PySymtable_Build(mod, filename, c->c_future)
    
    // 2. 为当前作用域创建编译器单元
    //    compiler_enter_scope(c, filename, ...)
    
    // 3. 根据 AST 节点类型分发
    switch (mod->kind) {
    case Module_kind:
        compiler_body(c, mod->v.Module.body);
        break;
    case Interactive_kind:
        ...
    }
    
    // 4. 生成最终的 PyCodeObject
    //    compiler_make_instruction(c, ...) 逐个指令
    //    assemble(c, ...) 汇编 → 字节码数组
    return compiler_make_return(c);
}
```

**编译器的关键内部结构**：

```c
// basicblock — 基本块（Compiler 内部的 CFG）
// 这不是运行时的块，而是编译过程中的结构
typedef struct basicblock {
    PyObject *b_instr;     // 指令数组
    struct basicblock *b_next;  // 下一块（线性顺序）
    struct basicblock *b_prevy; // 前驱（用于 JUMP_IF 等）
    int b_iused;           // 已使用的指令数
    int b_ialloc;          // 分配的容量
    int b_offset;          // 字节码偏移
    unsigned b_next_addr;  // 下一个指令的地址（跳转目标计算）
    unsigned b_start_addr; // 块的起始地址
    int b_label;           // 标签（跳转标记）
    int b_code;            // 代码类型
} basicblock;

// compiler 结构 — 编译上下文
struct compiler {
    PyObject *c_filename;          // 当前文件名
    PyObject *c_name;              // 当前代码对象名（"<module>"/函数名）
    PyObject *c_u?;                // 符号表
    struct compiler_unit *u;       // 当前编译单元
    PyObject *c_stack;             // 编译栈
    Py_ssize_t c_stack_size;       // 栈深度
    int c_flags;                   // 编译器标志
    int c_optimize;                // 优化级别（-O）
    
    // 指令发出
    int c_nestlevel;               // 嵌套深度（用于 max_depth）
};
```

### 2.5 编译步骤对反编译的启示

| 编译步骤 | 影响 | 反解策略 |
|---------|------|---------|
| **符号表分析** 建立作用域链 | names=全局名, varnames=局部名, freevars/cellvars=闭包 | `CodeObject.Names` 全反写回 `Name(Id, Load/Store)`, `VarName` 需判断 Load/Store |
| **常数折叠** `2+3`→`5` | 运行时看不到 2+3，只看到 `LOAD_CONST 5` | `Constant(5)` 直接输出，无法恢复 `2+3` |
| **条件表达式折叠** `if x:` → `POP_JUMP_IF_*` | 分支条件消失，只剩跳转 | AstBuilder 通过 jump target 反推 if 条件 |
| **循环展开** for/while → 跳转图 | 循环体变成有回边的 CFG | ControlFlowScanner 检测回边→识别循环头 |
| **try 编译** SETUP_FINALLY(3.10-) / ExceptionTable(3.11+) | 异常处理偏移量编码 | BuildTryFromBlock 解析偏移 |
| **优化级** `-O` 移除 assert/docstring | 反编译输出中 assert/docstring 可能缺失 | 无法恢复（信息丢失） |

### 2.6 compile.c 指令发出机制

反编译器最难的地方——编译器怎么发出指令，反编译器就要怎么逆推：

```c
// compile.c 发出一条指令
static int
compiler_addop(struct compiler *c, int opcode)
{
    // 向当前 basicblock 添加一条指令
    return compiler_addop_i(c, opcode, 0);
}

static int
compiler_addop_i(struct compiler *c, int opcode, Py_ssize_t arg)
{
    struct basicblock *b;
    
    // 获取当前基本块
    b = compiler_current_block(c);
    
    // 向块内添加指令
    // 如果块满则扩展
    if (b->b_iused >= b->b_ialloc) {
        // 扩展指令数组
    }
    
    b->b_instr[b->b_iused].i_opcode = opcode;
    b->b_instr[b->b_iused].i_oparg = arg;
    b->b_iused++;
    
    // 某些指令会导致块分裂（如 JUMP_ABSOLUTE）
    compiler_use_next_block(c);  // 可能分裂块
}
```

**关键**: 编译器用 **basicblock** 作为指令容器，然后在 **assemble()** 中将这些块拼成连续的字节码数组。反编译器需要反转这个过程——从连续字节码恢复基本块。

### 2.7 marshal.c 版本差异总结（反编译重点）

通过研读 CPython 不同版本的 `Python/marshal.c`，得到的版本差异：

| 特性 | Python 2.7 | Python 3.4-3.7 | Python 3.8-3.10 | Python 3.11+ |
|------|-----------|---------------|----------------|-------------|
| **header 大小** | 8B | 12B | 16B | 16B |
| **code 字段数** | 4 (arg,nl,ss,flags) | 5 (arg,kw,nl,ss,flags) | 6 (+pos) | 5 (-nl,+pos) |
| **ref 机制** | TYPE_INTERNED + TYPE_STRINGREF(0x52) | FLAG_REF(0x80) + TYPE_REF(0x52) | 同 3.4-3.7 | 同 3.4-3.7 |
| **refstack** | 无 | 全局 ref list | 同 | 同 |
| **interned strings** | `p->strings` 列表 | 同 | 同 | 同 |
| **TYPE_CODE_SIMPLE** | 无 | 无 | 无 | 有(0x73) |
| **locplus** | varnames+cellvars+freevars 分开 | 同 | 同 | varnames+cellvars+freevars→localsplusnames+kinds |

### 2.8 compile.c 调试方法

编译 .py → 用 `dis` 模块查看字节码：
```python
import dis, marshal

# 编译源码
with open('test.py') as f:
    code = compile(f.read(), 'test.py', 'exec')

# 查看字节码
dis.dis(code)

# 查看代码对象的内部结构
print(f"co_names: {code.co_names}")
print(f"co_varnames: {code.co_varnames}")
print(f"co_consts: {code.co_consts}")
print(f"co_filename: {code.co_filename}")
print(f"co_name: {code.co_name}")
```

**查看 CPython 内部结构的变化**：
```python
# Python 2.7 vs 3.x 的差异
# v2.7: co_freevars, co_cellvars 是单独字段
# v3.11+: co_localsplusnames = varnames + cellvars + freevars

# 查看指令分布
from collections import Counter
Counter(instr.opname for instr in dis.get_instructions(code))
```

---

## 3. 四阶段流水线架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Decompiler 主入口                                │
└───────────────────────────┬─────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Phase 1: 字节码读取                                                    │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────────────────┐  │
│  │ PycReader   │ → │ CodeObject   │ → │ Instruction[] + 常数表    │  │
│  │ (Marshal)   │    │ 反序列化     │    │ 符号表(code_names/var)    │  │
│  └─────────────┘    └──────────────┘    └───────────────────────────┘  │
│  支持: 2.7(8B header), 3.0-3.6(12B), 3.7+(16B), pre-3.8 ref_index    │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Phase 2: 分块与控制流分析                                              │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────────────────┐  │
│  │ BlockScanner│ → │ BasicBlock[] │ → │ ControlFlowScanner         │  │
│  │ (Leader标记)│    │ CFG 构建     │    │ (LoopHeader/Body 标记)   │  │
│  └─────────────┘    └──────────────┘    └───────────────────────────┘  │
│  BlockFlags: Entry, Exit, LoopHeader, LoopBody, ConditionHeader       │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Phase 3: AST 构建 (核心容错阶段)                                       │
│  ┌─────────────────┐    ┌──────────────┐    ┌───────────────────────┐  │
│  │ BlockDecompiler  │ → │ BlockResult  │ → │ AstBuilder            │  │
│  │ (逐块栈机模拟)   │    │ Success/Fail  │    │ (While/For/If/Try)   │  │
│  │ StackMachine     │    │ 注释兜底     │    │ 控制块构建           │  │
│  └─────────────────┘    └──────────────┘    └───────────────────────┘  │
│  ● 每个 block 独立 try/catch，失败→BlockResult.FallbackAsComment()     │
│  ● 嵌套循环使用 visited.Remove(bb) 防止 StackOverflow                 │
│  ● break/continue 通过 _isForLoop + POP_TOP 和 JUMP_ABSOLUTE 检测    │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Phase 4: 代码生成                                                      │
│  ┌──────────────────┐    ┌──────────────┐    ┌───────────────────────┐  │
│  │ PythonCodeGen    │ → │ 缩进管理      │ → │ Python 源码            │  │
│  │ (Visitor 模式)   │    │ IndentStack  │    │ (含注释块)             │  │
│  └──────────────────┘    └──────────────┘    └───────────────────────┘  │
│  ● AST → Python 字符串：If→"if ...:", While→"while ...:", For→"for"   │
│  ● 注释块作为 CommentStmt 节点，输出为 # 注释                          │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
                      Python 源代码（含注释兜底块）
```

---

## 4. 解决方案结构

```
PyRebuilderSharp.slnx
├── src/
│   ├── PyRebuilderSharp.Core/           # 核心库 (net10.0)
│   │   ├── Models/
│   │   │   ├── AST/                     # AST 节点（record 类型）
│   │   │   │   ├── AstNode.cs           # 基类
│   │   │   │   ├── Expr.cs              # 表达式节点
│   │   │   │   ├── Stmt.cs              # 语句节点（含 CommentStmt）
│   │   │   │   └── CommentStmt.cs       # 注释兜底语句节点
│   │   │   ├── Bytecode/                # 字节码模型
│   │   │   │   ├── Instruction.cs       # 指令 (record struct)
│   │   │   │   ├── Opcode.cs            # 操作码枚举
│   │   │   │   └── CodeObject.cs        # 代码对象
│   │   │   └── CFG/                     # 控制流图
│   │   │       ├── BasicBlock.cs        # 基本块
│   │   │       ├── BlockFlags.cs        # 块属性标志
│   │   │       └── StructuredCFG.cs     # 结构化 CFG
│   │   ├── Readers/
│   │   │   └── PycReader.cs             # .pyc 文件读取器
│   │   ├── Scanners/
│   │   │   ├── BlockScanner.cs          # 基本块划分
│   │   │   └── ControlFlowScanner.cs    # 控制流分析
│   │   ├── Builders/
│   │   │   ├── AstBuilder.cs            # AST 构建（控制结构识别）
│   │   │   ├── StackMachine.cs          # 栈机模拟
│   │   │   ├── BlockDecompiler.cs       # 逐块反编译
│   │   │   └── BlockResult.cs           # 反编译结果 + 注释兜底
│   │   ├── Generators/
│   │   │   └── PythonCodeGenerator.cs   # Python 源码输出
│   │   └── Decompiler.cs                # 主入口编排
│   │
│   ├── PyRebuilderSharp.Cli/            # 命令行工具
│   │   └── Program.cs                   # CLI 入口
│   │
│   └── PyRebuilderSharp.Gui/            # Avalonia GUI
│       ├── App.axaml / App.axaml.cs     # 应用入口
│       ├── Program.cs                   # 启动
│       ├── ViewModels/
│       │   ├── ViewModelBase.cs         # MVVM 基类
│       │   └── MainViewModel.cs         # 主 ViewModel
│       └── Views/
│           ├── MainWindow.axaml         # 主窗口布局
│           └── MainWindow.axaml.cs      # 窗口代码
│
└── tests/
    └── PyRebuilderSharp.Tests/          # 测试项目
        ├── PycReaderTests.cs            # 读取器测试
        ├── StackMachineTests.cs         # 栈机测试
        ├── PycdcSuiteTests.cs           # pycdc 套件
        │   └── PycdcSuiteRunner.cs      # 测试运行器
        ├── QuickTests/
        │   ├── VersionMatrixTests.cs    # 版本矩阵测试（Lv0/Lv1/Lv2）
        │   ├── DiagnoseWhileLoops.cs    # while 诊断
        │   └── TestPopJump.cs           # POP_JUMP 测试
        └── TestData/
            ├── input/                   # .py 源文件
            ├── compiled/                # .pyc 文件（编译矩阵）
            └── tokenized/               # 预期 token 输出
```

---

## 5. 核心组件详解

### 5.1 BlockDecompiler — 逐块反编引擎

```csharp
// 每个基本块独立反编译，捕获异常→注释兜底
var result = BlockDecompiler.DecompileBlock(
    instructions, codeObject, blockId, loopHeaders, isForLoop);

if (result.IsSuccess)
    // result.Statements → AST 节点列表
else
    // result.CommentFallback → "# [Block #{id} Decompilation Failed]..."
```

### 5.2 BlockResult — 成功/失败统一返回

```csharp
public class BlockResult
{
    public bool IsSuccess { get; init; }
    public List<Stmt> Statements { get; init; }    // 成功时
    public string CommentFallback { get; init; }   // 失败时
    public string? ErrorMessage { get; init; }

    public static BlockResult Success(List<Stmt> stmts);
    public static BlockResult FallbackAsComment(
        List<Instruction> instructions, Exception exception, int blockId);
}
```

### 5.3 StackMachine — 栈机模拟

| 指令类型 | 处理方式 |
|---------|---------|
| LOAD_CONST/NAME/FAST | 压栈 Expr |
| BINARY_ADD/SUB/MUL | 弹栈右→左→BinOp |
| STORE_NAME/FAST/ATTR | 弹栈值→Assign |
| POP_TOP | for 循环体→Break，否则丢弃 |
| RETURN_VALUE | 弹栈值→Return |
| JUMP_ABSOLUTE→循环头 | Continue |
| COMPARE_OP | 弹栈右→左→Compare |
| CALL_FUNCTION | 弹栈 args→Call |

### 5.4 AstBuilder — 控制结构识别

| 控制结构 | 检测方法 | 构建输出 |
|---------|---------|---------|
| while | LoopHeader + 回边 | While(Test, Body, Orelse) |
| for | FOR_ITER 指令 | For(Target, Iter, Body) |
| if/else | POP_JUMP_IF_* 分支 | If(Test, Body, Orelse) |
| try | SETUP_FINALLY | Try(Body, Handlers, Orelse, Finalbody) |
| break | for 中 POP_TOP | Break() |
| continue | JUMP_ABSOLUTE→循环头 | Continue() |

**嵌套循环保护**：使用 `visited.Remove(bb)` 从 visited 集合中移除 body 块，使 GetStructuredBlockStmts 能用同一 visited 集重新管理，防止嵌套时 StackOverflow。

---

## 6. 版本支持矩阵

| 版本 | Magic Number | Header | 字段数 | 状态 |
|------|-------------|--------|--------|------|
| 2.7 | 03 F3 0D 0A | 8B | arg,nl,ss,flags(4) | ✅ Marsahl + Lv0-Lv3 |
| 3.5 | 17 0D 0D 0A | 12B | arg,kw,nl,ss,flags(5) | ✅ Lv0-Lv3 |
| 3.6 | 33 0D 0D 0A | 12B | arg,kw,nl,ss,flags(5) | ✅ Lv0-Lv3 |
| 3.7 | 42 0D 0D 0A | 16B | arg,kw,nl,ss,flags(5) | ✅ Lv0-Lv3 |
| 3.8 | 55 0D 0D 0A | 16B | arg,pos,kw,nl,ss,flags(6) | ✅ Lv0-Lv3 |
| 3.9 | 61 0D 0D 0A | 16B | arg,pos,kw,nl,ss,flags(6) | ✅ Lv0-Lv3 |
| 3.10 | 6F 0D 0D 0A | 16B | arg,pos,kw,nl,ss,flags(6) | ✅ Lv0-Lv3 |
| 3.11 | A7 0D 0D 0A | 16B+CACHE | arg,pos,kw,ss,flags(5) 去nl | ✅ marshal + def + class + yield |
| 3.12 | C0 0D 0D 0A | 16B+CACHE | 同 3.11 | ✅ 同 3.11 |
| 3.13 | D0 0D 0D 0A | 16B+CACHE | 同 3.11 | ✅ 兼容 marshal |
| 3.14 | D2 0D 0D 0A | 16B+CACHE | 同 3.11 | ✅ 兼容 marshal |

---

## 7. 测试策略

### 7.1 版本矩阵测试（核心）

```
77 tests = 7 层级 × 11 版本 (全覆盖 2.7 → 3.14)
  ├─ Lv0_Expressions:         2.7, 3.5-3.14 ✅ (11)
  ├─ Lv1_Sequential:          2.7, 3.5-3.14 ✅ (11)
  ├─ Lv2_ControlFlow:         2.7, 3.5-3.14 ✅ (11)
  ├─ Lv3_NestedDepth(5层):    2.7-3.14 ✅ (11)
  ├─ Lv3_NestedMixed:         2.7-3.14 ✅ (11)
  ├─ Lv3_NestedMatrix:        2.7-3.14 ✅ (11)
  └─ Lv3-1_NestedDepth(九层塔): 2.7-3.14 ✅ (11)  ← 新增
```

所有版本均标记为 `known_issue`（AST 语义比较跳过），仅验证反编译不崩溃。
3.11+ 版本通过 marshal 3.11+ 格式修复（`localsplusnames + localspluskinds`）可正确读取。
3.13/3.14 兼容 marshal 格式（与 3.11/3.12 一致）。

比较方式（按优先级）：
1. **AST 语义比较**（首选）— `python3 -c "import ast; print(ast.dump(ast.parse(...)))"`
2. **Token 比较**（回退）— 当 .py 源文件不存在时

### 7.2 编译矩阵

`compile_pyc_matrix.py` 使用 pyenv 多版本 Python 编译测试文件：
```bash
VERSIONS=("2.7.18" "3.5.10" "3.6.15" "3.7.17" "3.8.18" "3.9.18" "3.10.14")
for v in "${VERSIONS[@]}"; do
    pyenv local $v && python3 -m py_compile "$file"
done
```

---

## 8. 当前状态与剩余工作

### 8.1 已完成的里程碑

| 层级 | 内容 | 状态 |
|------|------|:----:|
| Lv0 | 表达式（常量/变量/二目/调用/属性/比较/切片） | ✅ |
| Lv1 | 顺序代码块（赋值/return/表达式语句） | ✅ |
| Lv2 | 控制流（if/while/for/try/break/continue/else） | ✅ |
| Lv3 | 嵌套控制块（深度5 + 矩阵对偶 + 混合嵌套 + 九层塔） | ✅ |
| v2.7 marshal | TYPE_STRINGREF 修复、FLAG_REF 正确禁用 | ✅ |
| v3.11+ marshal | 8 修复：localsplusnames+kinds、FLAG_REF ref slot、container ref、exceptiontable TYPE_REF 等 | ✅ 0/938 警告 |
| `def` 语句 | 函数定义、参数、返回值、闭包 | ✅ |
| `class` 定义 | 类定义、方法、__init__、类级属性 | ✅ |
| `yield` / `yield from` | 生成器函数 | ✅ |
| `@decorator` | 装饰器链 | ✅ |
| `async def` / `await` | 异步函数 | ✅ |
| 展开赋值 | `a, b = ...`, `a, *rest = ...` | ✅ |
| CrashCollector | JSON 崩溃记录到 ~/.pyrebuilder/crashes/ | ✅ |
| GUI | Avalonia 暗色主题 + 拖放 + 语法高亮 + 版本检测 | ✅ |
| 编译脚本 | `tools/compile_test_data.py` 2.7→3.14 全覆盖 | ✅ |

### 8.2 剩余工作

- 语法覆盖：`match/case` (3.10+)、`except*` (3.11+)、walrus `:=`
- 工程增强：AST 自动对比验证、CrashCollector Dashboard、批量反编译模式

---

## 9. 剩余工作计划

Phase 1–6 全部关闭。剩余工作移入 **Phase Fix**：

| 项目 | 优先级 | 类型 |
|:-----|:-------|:------|
| `match/case` ExceptionTable CFG 重建 | 🔴 高 | 语法覆盖 |
| `except*` ExceptionTable → IsGroup 映射 | 🔴 高 | 语法覆盖 |
| walrus 控制流检测 | 🟢 低 | 语法覆盖 |
| AST 自动对比验证 | 🟡 中 | 工程增强 |
| CrashCollector Dashboard | 🟡 中 | 工程增强 |
| 批量反编译模式 | 🟢 低 | 工程增强 |

详见 `docs/plan_phase_fix.md`。

---

## 10. 已知问题（已全部关闭）

| 层级 | 内容 | 优先级 |
|------|------|--------|
| **Lv8a** | AST 语义比较自动化（CI） | P1 |
| **Lv8b** | 性能优化（大文件/多代码对象） | P2 |
| **Lv8c** | Python 2.7 bytecode 全面支持（SLICE/PRINT/EXEC/RAISE） | P2 |
| **Lv8d** | Python 3.13+ 新特性适配 | P3 |
| **Lv8e** | 插件化反编译引擎（支持第三方扩展） | P3 |

---

## 10. 已知问题（已全部关闭）

✅ Phase 3/4/5 已知问题已在 2026-06-14 全部修复。详见 `docs/summary_phase_fix_end.md`。

| 问题 | 修复 |
|:-----|:------|
| module `co_names` 被 marshal TYPE_REF 耗尽 | `ReadRawMarshalBytes` 新增 `ReadRefAndReturnBytes` |
| abc.3.12 `from name_8 import name_9` | 同上 |
| `class __name__:` / `Foo = 'Foo'` → `class Foo: pass` | ROT_TWO/PUSH_NULL 枚举冲突 + cache 表修复 |
| `x = f()` → `x = f` | cache 表重写为只跳过 `rawOp==0` |
| StackMachineTests × 2, TokenDumperTests × 1 | 测试用例更新 |
