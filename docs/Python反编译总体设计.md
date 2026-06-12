# 文档一：Python反编译总体设计.md

## Python字节码反编译器总体设计文档

**版本**: v2.1
**日期**: 2026-06-13
**项目**: PyRebuilderSharp
**状态**: 开发阶段 — Lv0 表达式 ✅ · Lv1 顺序代码块 ✅ · Lv2 控制流 ✅ · Lv3 嵌套矩阵 ✅

---

## 1. 项目概述

### 1.1 背景与目标

**PyRebuilderSharp** 是一个基于 C#(.NET 10) 的 Python 字节码反编译器，对标 pycdc，以 Avalonia UI 提供跨平台 GUI。核心目标：

- **多版本兼容**: 支持 Python 2.7 + 3.5~3.10（3.11+ 暂缓）
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

## 2. 四阶段流水线架构

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

## 3. 解决方案结构

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

## 4. 核心组件详解

### 4.1 BlockDecompiler — 逐块反编引擎

```csharp
// 每个基本块独立反编译，捕获异常→注释兜底
var result = BlockDecompiler.DecompileBlock(
    instructions, codeObject, blockId, loopHeaders, isForLoop);

if (result.IsSuccess)
    // result.Statements → AST 节点列表
else
    // result.CommentFallback → "# [Block #{id} Decompilation Failed]..."
```

### 4.2 BlockResult — 成功/失败统一返回

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

### 4.3 StackMachine — 栈机模拟

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

### 4.4 AstBuilder — 控制结构识别

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

## 5. 版本支持矩阵

| 版本 | Magic Number | Header | ref_index | 状态 |
|------|-------------|--------|-----------|------|
| 2.7 | 03 F3 0D 0A | 8B | 不读取 | ✅ Lv0-Lv3 |
| 3.5 | 0D 17 0D 0A | 12B | 跳过 | ✅ Lv0-Lv3 |
| 3.6 | 0D 33 0D 0A | 12B | 跳过 | ✅ Lv0-Lv3 |
| 3.7 | 0D 42 0D 0A | 16B | 跳过 | ✅ Lv0-Lv3 |
| 3.8 | 0D 55 0D 0A | 16B | 读取 | ✅ Lv0-Lv3 |
| 3.9 | 0D 61 0D 0A | 16B | 读取 | ✅ Lv0-Lv3 |
| 3.10 | 0D 6F 0D 0A | 16B | 读取 | ✅ Lv0-Lv3 |
| 3.11+ | 0D A0+ | 16B+CACHE | 读取 | ⏳ 暂缓 |

---

## 6. 测试策略

### 6.1 版本矩阵测试（核心）

```
42 tests = 6 层级 × 7 版本
  └─ Lv0_Expressions:  2.7, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10 ✅
  └─ Lv1_Sequential:   2.7, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10 ✅
  └─ Lv2_ControlFlow:  2.7, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10 ✅
  └─ Lv3_NestedDepth:  2.7, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10 ✅  ← 新增
  └─ Lv3_NestedMixed:  2.7, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10 ✅  ← 新增
  └─ Lv3_NestedMatrix: 2.7, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10 ✅  ← 新增
```

比较方式（按优先级）：
1. **AST 语义比较**（首选）— `python3 -c "import ast; print(ast.dump(ast.parse(...)))"`
2. **Token 比较**（回退）— 当 .py 源文件不存在时

### 6.2 编译矩阵

`compile_pyc_matrix.py` 使用 pyenv 多版本 Python 编译测试文件：
```bash
VERSIONS=("2.7.18" "3.5.10" "3.6.15" "3.7.17" "3.8.18" "3.9.18" "3.10.14")
for v in "${VERSIONS[@]}"; do
    pyenv local $v && python3 -m py_compile "$file"
done
```

---

## 7. 已知限制与计划

### 7.1 当前版本的已知问题（P0）

| 问题 | 影响 | 计划修复 |
|------|------|---------|
| except handler body 尾部 POP_EXCEPT 处理 | except 体尾部 | Phase 5 细化 |
| AugAssign 转换（`i = i + 1` → `i += 1`） | 已实现基础模式 | Phase 5 细化 |

### 7.2 下一阶段计划

| 层级 | 内容 | 优先级 |
|------|------|--------|
| Lv3 | **嵌套控制块（深度5+矩阵对偶）** | **已完成** |
| Lv4 | 函数/方法（def、lambda、class） | P0 |
| Lv5 | 异常处理增强（with、finally、raise from） | P1 |
| Lv6 | 生成器与协程（yield/async/match） | P2 |
| GUI | 完善 UI（语法高亮、块级注释着色、批量反编译） | P1 |
| 3.11+ | CACHE 条目、RESUME、BINARY_OP 统一 | P2 |

### 7.3 GUI 功能规划

- [x]  Avalonia 跨平台窗口
- [x]  .pyc 文件选择（FilePicker）
- [x]  反编译流水线执行
- [ ]  语法高亮（AvaloniaEdit）
- [ ]  注释块高亮着色（红色背景）
- [ ]  块级成功率统计
- [ ]  批量反编译（文件夹模式）
- [ ]  Python 版本选择
- [ ]  源码保存
