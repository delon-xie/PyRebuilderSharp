# 文档三：Phase 3+ 反编译进阶与版本支持

**版本**: v1.1
**日期**: 2026-06-13
**项目**: PyRebuilderSharp
**状态**: 
- Lv0-Lv2 全版本通过 ✅ (21/21)
- 91 个真实 .py 反编译通过率 100% ✅ (454 总块, 0 失败块)
- v3.11/3.12 操作码映射 + 基本反编译 ✅
- Lv3 嵌套深度部分修复 ⏳
- 37 个嵌套 CodeObject Marshal 读取警告 ⚠️
- 测试矩阵待扩展至 3.11/3.12 ⏳

---

## 0. Phase 3 收敛计划（当前优先）

### 0.1 目标

在进入 Phase 4 语法覆盖之前，先确保 Phase 3 完全收敛：
1. 修复嵌套 CodeObject marshal 读取 → 37 个警告降为 0
2. 将 3.11/3.12 纳入测试矩阵
3. 建立 CrashCollector 运行时
4. Lv3 嵌套混合场景完全通过

### 0.2 收敛检查清单

| 序号 | 任务 | 依赖 | 预计工期 | 验收标准 |
|------|------|------|---------|---------|
| C1 | **Marshal 嵌套 CodeObject 修复**: 排查 `ReadMarshalCodeObject` 的 co_consts 读取失败根因。添加所有缺失的 marshal type code 处理 (TYPE_BYTES=0x7C 已加, 仍需排查流同步 0x64 问题) | 无 | 2-3 次会话 | 37 个警告 → 0; `test_data/compiled/*.3.12.pyc` 全部 91 个文件无 Warning |
| C2 | **编译矩阵扩展至 3.11/3.12**: `compile_pyc_matrix.py` 已包含 3.11.0/3.11.15/3.12.13；需要运行脚本生成 3.11/3.12 版本的 `test_data/compiled/*.3.11.pyc` 和 `tests/PyRebuilderSharp.Tests/TestData/compiled/` 中的版本矩阵 | C1 | 1 次会话 | pycdc 测试套件包含 3.11/3.12 版本的 .pyc 文件 |
| C3 | **CrashCollector 实现**: 在 `BlockDecompiler` 和 `StackMachine` 中插入收集点，生成 `CrashRecord` | 无 | 1 次会话 | 崩溃时输出结构化 CrashRecord（JSON），包含块 ID、指令索引、操作码序列 |
| C4 | **Lv3 嵌套混合修复**: 修复 `depth_5_try` 内层 handler pass vs result=-N；修复 `depth_5_while` orelse=[] vs Continue() 定位差；修复 `mixed_nested` orelse 跨块收集 | C1 | 2-3 次会话 | Lv3_NestedDepth + Lv3_NestedMixed 全版本通过 (14/14) |

### 0.3 阶段验收标准

```
反编译通过率: > 90% (当前: 100%) ✅
失败指令率:   < 10%  (当前: 0%)   ✅
Marshal 警告:   0    (当前: 37)    ❌ → ⏳
测试矩阵版本: 2.7, 3.5-3.12        (当前: 2.7-3.10) ⏳
CrashCollector: 已实现并集成        (当前: 未实现)    ⏳
Lv3 测试通过:  14/14               (当前: 0/14)     ❌ → ⏳
```

---

## 1. 添加新 Python 版本反编译支持的标准化流程

### 1.1 四层检查清单

当需要支持一个新的 Python 版本（如 3.13、3.14）时，按以下顺序检查：

```
Layer 1: PycReader (Marshal 读取)
Layer 2: Opcode 映射 (ParseInstructions)
Layer 3: StackMachine (指令处理)
Layer 4: AstBuilder (控制结构构建)
```

### 1.2 Layer 1 — Marshal 读取

**检查目标**: `PycReader.cs` 能否正确读取新版本的 .pyc 文件

| 检查项 | CPython 源文件 | 反编译对应文件 | 检查方法 |
|--------|---------------|--------------|---------|
| Magic Number | `Lib/importlib/_bootstrap_external.py` 搜索 `MAGIC_NUMBER` | `PycReader.cs` → `_magicBytes` | `python3 -c "import importlib; print(importlib.util.MAGIC_NUMBER.hex())"` |
| Header 大小 | 同上函数 `_code_to_timestamp_pyc` 等 | `PycReader.cs` → header size switch | 对比新版本 header bytes 长度 |
| TYPE_CODE 字段数 | `Python/marshal.c` → `w_complex_object` 中 TYPE_CODE 分支 | `PycReader.cs` → `ReadMarshalCodeObject` | 在 marshal.c 中数 field 数量 |
| TYPE_CODE_SIMPLE | `Python/marshal.c` → `r_object` 中 `TYPE_CODE_SIMPLE` | `ReadMarshalValue` 中 `TYPE_STRING(0x73)` 分支 | 检查 0x73 的赋值策略 |
| FLAG_REF 变化 | `Python/marshal.c` → `FLAG_REF` constant | `ReadMarshalObject` 中 FLAG_REF 处理 | 检查 ref 列表管理 |
| Localsplus 格式 | `Include/cpython/code.h` → `PyCodeObject` | `CodeObject.cs` → Varnames/Freevars/Cellvars | 检查字段名称和顺序 |
| ExceptionTable | `Python/ceval.c` → `co_exceptiontable` | `ParseExceptionTable` + `ExceptionTableEntry` | 检查条目格式（8字节 word 偏移） |

**典型 marshal 变更模式**:

```
Python 2.7:  TYPE_CODE(4 fields) + TYPE_INTERNED + TYPE_STRINGREF
Python 3.4-3.7: TYPE_CODE(5 fields) + FLAG_REF
Python 3.8-3.10: TYPE_CODE(6 fields) + FLAG_REF
Python 3.11+: TYPE_CODE(5 fields, no nlocals) + TYPE_CODE_SIMPLE + CACHE + ExceptionTable
```

**调试命令**:
```python
# 检查 .pyc 结构
import struct, dis, marshal

with open('test.pyc', 'rb') as f:
    magic = f.read(4)           # Magic number
    header = f.read(12)         # 剩余 header
    code = marshal.load(f)      # 顶层 code object
    
print(f"Magic: {magic.hex()}")
print(f"co_argcount: {code.co_argcount}")
print(f"co_nlocals: {code.co_nlocals}")  # Python 3.11+ 不存在
print(f"co_stacksize: {code.co_stacksize}")
print(f"co_flags: {code.co_flags:#x}")
print(f"co_consts: {code.co_consts}")
print(f"co_names: {code.co_names}")
print(f"co_varnames: {code.co_varnames}")
print(f"co_code length: {len(code.co_code)}")
```

### 1.3 Layer 2 — Opcode 映射

**检查目标**: 新版本的 opcode 值与 3.12 是否相同

| 检查项 | CPython 源文件 | 方法 |
|--------|---------------|------|
| Opcode 数值表 | `Lib/opcode.py` → `def_op`/`name_op` 调用 | `python3 -c "import dis; print(dis.opmap)"` |
| CACHE 条目数 | `Lib/opcode.py` → `_cache_entries` 字典 | `python3 -c "import dis; print(dis._cache_entries)"` |
| HAVE_ARGUMENT 阈值 | `Include/opcode_ids.h` 或 `Lib/opcode.py` → `HAVE_ARGUMENT` | 通常 = 90 |
| EXTENDED_ARG | 同上 | 通常 = 144 |

**操作码映射的关键模式**:

```
在同一 Opcode 枚举中有多个名称时，它们共享字节值但适用于不同版本：
  121 = SETUP_EXCEPT (3.5-3.7) / JUMP_IF_NOT_EXC_MATCH (3.8-3.10) / RETURN_CONST (3.11+)
  122 = SETUP_FINALLY (3.5-3.10) / BINARY_OP (3.11+)
  143 = SETUP_WITH (3.5-3.10) / LOAD_FAST_AND_CLEAR (3.11+)
```

当同一字节值对应多个操作码时（如 122 在 3.10 为 SETUP_FINALLY，在 3.11+ 为 BINARY_OP）：
- **在 Opcode 枚举中**使用统一的数值（如字节值 122）
- **在 C# 的 switch 语句中**不能同时使用两个枚举名作为 case 标签 — 使用内部代理值（如 BINARY_OP = 191）

**CACHE 条目是关键** — 3.11 与 3.12 的缓存配置完全不同：

```csharp
// 3.11: 仅部分操作码有缓存（自适应字节码初期）
// 3.12: 所有操作码从初始就有固定 CACHE 条目
GetCacheCount311(byte rawOp)  // "稀疏"表格
GetCacheCount312(byte rawOp)  // "完整"表格
```

错误的 CACHE 计数会导致指令流错位——LOAD_NAME 的 CACHE 差异（3.11=0, 3.12=4）是最常见的 bug 来源。

### 1.4 Layer 3 — StackMachine

**检查目标**: 新操作码的处理能力

| 变更类型 | 示例 | 处理方法 |
|---------|------|---------|
| 新增操作码 | BINARY_OP 替代 BINARY_* | 在 Execute 中添加 case |
| 操作码删除 | POP_BLOCK 在 3.11+ 移除 | 在 3.11+ 映射中返回适当的替代 |
| 语义改变 | CALL 在 3.11+ 使用 PRECALL 协议 | 修改 CALL 处理逻辑 |
| 冗余操作码 | RESUME, NOP | 返回 null（忽略） |

**CALL 协议变更（3.11+）**:

```
3.10 及更早: CALL_FUNCTION N → 弹出 N 个参数 + 函数
3.11+: PUSH_NULL → LOAD func → LOAD args → UNPACK_SEQUENCE N → CALL N
```

PUSH_NULL 会在栈上留下一个 null 标记（sentinel），CALL 需要检测并弹出它：
```csharp
var peeked = SafePeek();
if (peeked is Constant { Value: null })
    _exprStack.Pop(); // 抛弃 null sentinel
```

### 1.5 Layer 4 — AstBuilder

**检查目标**: 控制流构建是否需要适配

| 变更 | 影响 | 处理方法 |
|------|------|---------|
| 异常表格式 | ExceptionTable 替代 SETUP_FINALLY | 解析 ExceptionTable → try 体范围 |
| 块分裂规则 | 3.11+ 块边界判断 | 检查 CACHE 对齐 |
| 跳转指令变化 | JUMP_BACKWARD 替代 JUMP_ABSOLUTE | 更新 IsJump 检测 |
| 行号表 | lnotab vs linetable | 解析新的行号编码格式 |

---

## 2. CPython 源码定位与问题排查方法论

### 2.1 核心源文件速查表

| 问题域 | 首要源文件 | 次要源文件 |
|--------|----------|----------|
| 字节码行为 | `Python/ceval.c` → `_PyEval_EvalFrameDefault` | `Python/bytecodes.c` |
| 编译过程 | `Python/compile.c` → `compiler_*` | `Python/symtable.c` |
| Marshal 格式 | `Python/marshal.c` → `r_object` / `w_complex_object` | `Python/importlib_external.py` |
| Opcode 定义 | `Lib/opcode.py` | `Include/opcode_ids.h` |
| CodeObject 结构 | `Include/cpython/code.h` | `Objects/codeobject.c` |
| AST 定义 | `Python/ast.c` → AST 节点创建 | `Parser/asdl.py` |
| 异常处理 | `Python/ceval.c` → 异常处理循环 | `Python/errors.c` |
| .pyc 格式 | `Lib/importlib/_bootstrap_external.py` | `Python/import.c` |

### 2.2 搜索策略

**场景 A：遇到未知操作码**

```
1. 获取操作码字节值（如 122）
2. 在 CPython 中搜索：
   #define 122  → Include/opcode_ids.h
   case 122:   → Python/ceval.c 或 Python/bytecodes.c
   
3. 判断使用场景：从 ceval.c 的 case 注释中了解操作码用途
   （如 BINARY_OP: "Implement binary operator"）
   
4. 验证：用 dis 模块反汇编含有该操作码的 .pyc
```

**场景 B：Marshal 读取出错**

```
1. 确定异常类型（stream end / unknown type code / type mismatch）
2. 定位到出错的 marshal 字节位置
3. 在 marshal.c 中搜索 TYPE_ 常量：
   grep "TYPE_" Include/marshal.h
   或搜索 r_object 函数中的 type 字节处理
4. PycReader.cs 中的 ReadMarshalValue 需要与 marshal.c 的 r_object 一一对应
```

**场景 C：控制流结构异常**

```
1. 用 dis 模块查看反编译目标的字节码
   dis.dis(code)
   
2. 记录所有跳转指令（JUMP_FORWARD, POP_JUMP_IF_*, JUMP_ABSOLUTE/BACKWARD）
   
3. 在 compile.c 中搜索对应的编译函数：
   compiler_if  → if 语句的字节码生成
   compiler_while → while 语句的字节码生成
   
4. 理解编译器的块分裂策略：哪些指令导致块分裂？
   - JUMP/FOR_ITER → 无条件分裂
   - POP_JUMP_IF_* → 条件分裂（两个后继）
```

### 2.3 版本差异定位方法论

当反编译在版本 A 正常但在版本 B 失败时：

```
Step 1: 确认 marshal 读取成功（Phase 1）
- 输出 `# Decompiled from:` 表示 Phase 1 成功
- 检查 CodeObject.Instructions.Count 是否合理

Step 2: 检查操作码映射（Phase 2）
- 在 PycReader.cs 的 MapOpcodePy311 中确认该版本的操作码值
- 检查 GetCacheCount311/312 是否正确

Step 3: 检查分块结果
- 确认基本块数量和边界
- 检查 LoopHeader/LoopBody 标记

Step 4: 逐块追踪
- 检查每个块的 BlockDecompiler 结果
- 确定失败的块及原因
```

### 2.4 跨版本对比工具

```python
# 跨版本对比同一源文件的字节码
import dis, marshal, sys

files = {
    '3.10': 'test_foo.3.10.pyc',
    '3.11': 'test_foo.3.11.pyc',
    '3.12': 'test_foo.3.12.pyc',
}

for ver, path in files.items():
    with open(path, 'rb') as f:
        magic = f.read(4)
        f.seek(16)  # 3.7+ header size
        code = marshal.load(f)
    
    print(f"\n=== {ver} ===")
    print(f"Instructions: {len(list(dis.get_instructions(code)))}")
    dis.dis(code)
```

### 2.5 常用调试命令速查

```bash
# 查看 .pyc 文件的 magic number
python3 -c "with open('test.pyc','rb') as f: print(f.read(4).hex())"

# 查看 Python 版本的 opcode 映射
python3 -c "import dis; print('\n'.join(f'{v:3d} = {k}' for k,v in sorted(dis.opmap.items(), key=lambda x:x[1])))"

# 获取 Python 版本的 cache 条目
python3 -c "import dis; print(dis._cache_entries if hasattr(dis,'_cache_entries') else 'N/A')"

# 反汇编 .pyc 文件
python3 -c "
import dis, marshal
with open('test.pyc','rb') as f:
    f.read(16)
    code = marshal.load(f)
    dis.dis(code)
"

# Python 版本号 → magic number
python3 -c "
import importlib.util, sys
print(f'Python {sys.version}: magic={importlib.util.MAGIC_NUMBER.hex()}')
"

# 查看代码对象的调试信息
python3 -c "
import dis, marshal
with open('test.pyc','rb') as f:
    f.read(16)
    code = marshal.load(f)
    show_code = getattr(dis, 'show_code', None)
    if show_code:
        show_code(code)
    else:
        # Python 3.12+ 的代码信息
        print(f'name={code.co_name}, args={code.co_argcount}, stack={code.co_stacksize}')
"
```

---

## 3. 异常收集与 Bug 复现机制（设计方案）

### 3.1 当前缺陷

当前反编译器在 Phase 3 (BlockDecompiler) 中捕获异常并输出注释块，但异常信息是"一次性"的——无法在后续运行时复用：

- 异常信息写入最终输出的注释块中，不会被结构化保存
- 无法自动生成复现测试
- 无法统计哪些文件/版本/操作码最容易失败
- 无法从大量顺序块中快速定位导致崩溃的最小指令集

### 3.2 核心原则：逐块隔离 → 最小复现

因为 `BlockDecompiler` 的每个基本块**独立反编译**（逐块调用 `StackMachine.Execute()`），一个块的失败与其他块完全无关。这天然允许我们：

```
完整.pyc → Phase1读取 → Phase2分块 → [Block1, Block2, ..., BlockN]
                                          │
                                     BlockK 反编译失败
                                          │
                                     CrashRecord 记录了:
                                     - 失败块 BlockK 的指令序列
                                     - 失败时的栈机状态上下文
                                     - 所属函数/代码对象信息
                                          │
                                     ┌────▼─────────────────────┐
                                     │ 最小复现 = 仅 BlockK 指令 │
                                     │ + 必要的前导 SETUP 指令   │
                                     │ (无关块全部丢弃)          │
                                     └─────────────────────────┘
```

**为什么可以丢弃无关块？** 因为每个基本块在 Python 字节码中是"平坦指令序列"——没有跳转，只有顺序执行。BlockK 的指令可以独立于 Block1..K-1 单独喂给 StackMachine。

### 3.3 复现管道总览

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     异常发生时的完整链路                                    │
│                                                                         │
│  1. StackMachine.Execute(instr) ── 对第 N 条指令抛出异常                   │
│     │                                                                   │
│     ▼                                                                   │
│  2. BlockDecompiler 的 catch 拦截                                        │
│     │                                                                   │
│     ▼                                                                   │
│  3. CrashCollector.Record()                                             │
│     ├── 记录: 异常类型 + 消息 + 栈追踪                                   │
│     ├── 记录: 异常发生的块 BlockId                                       │
│     ├── 记录: 异常时刻的指令索引 (InstructionIndex)                       │
│     ├── 记录: 指令总数                                                   │
│     ├── 记录: 栈机当前 _exprStack 深度/内容（如果有）                      │
│     └── 记录: 所属的代码对象名 + 函数签名                                │
│     │                                                                   │
│     ▼                                                                   │
│  4. ContextExtractor 提取最小上下文                                       │
│     ├── 从 BlockK 提取所有指令 → Instructions                             │
│     ├── 识别必要的常量和符号表依赖 (Constants/Names/Varnames)              │
│     ├── 从完整 CodeObject 中拷贝这些依赖                                  │
│     └── 生成 MinimalContext (最小可独立反编译的上下文)                     │
│     │                                                                   │
│     ▼                                                                   │
│  5a. StackMachineTestGenerator                                          │
│      └── 生成 xUnit 测试方法:                                            │
│          直接创建 StackMachine, 投入 MinimalContext 的指令               │
│          验证特定指令第 N 条抛出异常类型 T                                 │
│                                                                         │
│  5b. MinimalPycBuilder (可选)                                           │
│      └── 从 MinimalContext 构建一个最小可执行的 .pyc 文件                  │
│          完全跳过 BlockScanner/AstBuilder,                                │
│          直接用 BlockDecompiler 反编译一个单块                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.4 CrashRecord 增强版

```csharp
/// <summary>
/// 反编译失败的完整记录 —— 精确到指令级别。
/// </summary>
public class CrashRecord
{
    // ── 文件标识 ──
    /// <summary>.pyc 文件的 SHA256 哈希</summary>
    public string FileHash { get; init; } = "";
    /// <summary>Python 版本标识（如 "3.11.5"）</summary>
    public string PythonVersion { get; init; } = "";
    /// <summary>Magic number 十六进制</summary>
    public string MagicHex { get; init; } = "";

    // ── 精确崩溃位置 ──
    /// <summary>失败的基本块 ID</summary>
    public int BlockId { get; init; }
    /// <summary>失败块在原始字节码中的偏移范围</summary>
    public (int Start, int End) BlockOffsetRange { get; init; }
    /// <summary>崩溃发生的指令索引（在 BlockK 的指令列表内）</summary>
    public int InstructionIndex { get; init; }
    /// <summary>崩溃指令的操作码名称</summary>
    public string FailingOpcode { get; init; } = "";
    /// <summary>崩溃指令的完整信息</summary>
    public string? FailingInstruction { get; init; }

    // ── 异常的完整上下文 ──
    /// <summary>异常类型全名</summary>
    public string ExceptionType { get; init; } = "";
    /// <summary>异常消息</summary>
    public string ExceptionMessage { get; init; } = "";
    /// <summary>异常栈追踪（包含 StackMachine.Execute 的行号）</summary>
    public string? StackTrace { get; init; }

    // ── 崩溃块的指令全景 ──
    /// <summary>失败块的所有指令（用于最小复现）</summary>
    public List<Instruction> BlockInstructions { get; init; } = new();
    /// <summary>栈机在执行到崩溃点之前的 _exprStack 快照</summary>
    public int ExprStackDepthBeforeCrash { get; init; }

    // ── 所属代码对象信息 ──
    /// <summary>代码对象名称（"<module>" 或函数名）</summary>
    public string CodeObjectName { get; init; } = "";
    /// <summary>是否为函数体</summary>
    public bool IsFunctionBody { get; init; }

    // ── 时间戳 ──
    public DateTime Timestamp { get; init; }
}
```

**关键字段说明**：

| 字段 | 用途 | 获取来源 |
|------|------|---------|
| `InstructionIndex` | 精确到第几条指令崩溃 | `BlockDecompiler` 的 `foreach` 循环中记录当前索引 |
| `BlockInstructions` | 所有指令的完整拷贝 | 在 catch 块中从 `instructions` 参数复制 |
| `ExprStackDepthBeforeCrash` | 栈深度快照 | 崩溃前一刻从 `stackMachine.ExprStackCount` 读取 |
| `FailingOpcode` | 崩溃的操作码 | 崩溃指令的 `instr.Opcode.ToString()` |

### 3.5 ContextExtractor — 提取最小上下文

```csharp
/// <summary>
/// 从 CrashRecord 提取最小可独立反编译的上下文。
/// 丢弃所有无关块，仅保留失败块所需的 CLR/符号表依赖。
/// </summary>
public class ContextExtractor
{
    /// <summary>
    /// 生成最小反编译上下文。
    /// 只包含失败块的指令 + 该块需要的常量/名称/变量。
    /// </summary>
    public MinimalContext ExtractMinimal(CrashRecord record, CodeObject originalCode)
    {
        // 1. 收集该块涉及的所有常量索引
        var usedConsts = new HashSet<int>();
        var usedNames = new HashSet<int>();
        var usedVarnames = new HashSet<int>();
        
        foreach (var instr in record.BlockInstructions)
        {
            if (instr.Opcode == Opcode.LOAD_CONST && instr.Argument.HasValue)
                usedConsts.Add(instr.Argument.Value);
            if (instr.Opcode == Opcode.LOAD_NAME && instr.Argument.HasValue)
                usedNames.Add(instr.Argument.Value);
            if (instr.Opcode == Opcode.STORE_NAME && instr.Argument.HasValue)
                usedNames.Add(instr.Argument.Value);
            if (instr.Opcode is Opcode.LOAD_FAST or Opcode.STORE_FAST && instr.Argument.HasValue)
                usedVarnames.Add(instr.Argument.Value);
        }

        // 2. 从原始 CodeObject 拷贝依赖
        var miniCode = new CodeObject
        {
            Name = originalCode.Name,
            IsPython27 = originalCode.IsPython27,
            IsPython38Plus = originalCode.IsPython38Plus,
            Instructions = record.BlockInstructions.ToList(),
            Constants = originalCode.Constants
                .Where(kv => usedConsts.Contains(kv.Key))
                .ToDictionary(kv => kv.Key, kv => kv.Value),
            Names = originalCode.Names
                .Where((_, i) => usedNames.Contains(i))
                .ToList(),
            Varnames = originalCode.Varnames
                .Where((_, i) => usedVarnames.Contains(i))
                .ToList(),
        };

        return new MinimalContext(miniCode, record);
    }
}

/// <summary>
/// 最小上下文 —— 可独立反编译的最小指令集 + 所有依赖。
/// </summary>
public record MinimalContext(
    CodeObject Code,
    CrashRecord SourceRecord
);
```

### 3.6 StackMachineTestGenerator — 生成精确到指令的测试

```csharp
/// <summary>
/// 从 CrashRecord 生成 xUnit 测试方法。
/// 测试直接创建 StackMachine 并逐条执行到出错的指令，验证崩溃。
/// </summary>
public class StackMachineTestGenerator
{
    public string GenerateTestCode(MinimalContext ctx)
    {
        var r = ctx.SourceRecord;
        var instrLines = new List<string>();
        for (int i = 0; i < ctx.Code.Instructions.Count; i++)
        {
            var ins = ctx.Code.Instructions[i];
            var argStr = ins.Argument.HasValue ? ins.Argument.Value.ToString() : "null";
            instrLines.Add($"            new Instruction({ins.Offset}, Opcode.{ins.Opcode}, {argStr})");
        }

        return $@"
/// <summary>
/// 复现: {r.ExceptionType} — Block#{r.BlockId}
/// 文件: {r.FileHash}
/// 版本: {r.PythonVersion}
/// 崩溃指令索引: #{r.InstructionIndex} ({r.FailingOpcode})
/// 栈机深度: {r.ExprStackDepthBeforeCrash}
/// </summary>
[Fact]
public void Repro_Block{r.BlockId}_{r.ExceptionType}()
{{
    // Arrange
    var code = new CodeObject
    {{
        Name = ""{r.CodeObjectName}"",
        Constants = new Dictionary<int, object?>(),
        Names = new List<string>(),
        Varnames = new List<string>(),
        Instructions = new List<Instruction>
        {{
{string.Join(",\n", instrLines)}
        }}
    }};

    var machine = new StackMachine(code);

    // Act & Assert
    var ex = Assert.Throws<{r.ExceptionType}>(() =>
    {{
        foreach (var instr in code.Instructions)
        {{
            machine.Execute(instr);
        }}
    }});

    // 验证是预期的那条指令导致的崩溃
    Assert.Contains(""{r.FailingOpcode}"", ex.Message);
}}
";
    }
}
```

### 3.7 MinimalPycBuilder — 构建最小可复现 .pyc

当需要完整的 .pyc 文件（而非仅 StackMachine 测试）进行调试时：

```csharp
/// <summary>
/// 从 MinimalContext 构建一个最小可反编译的 .pyc 文件。
/// 
/// 原理：
///   将失败块的指令包装为一个顶层模块或单函数。
///   写入标准的 .pyc header + marshal 格式的 CodeObject。
///   只包含该块需要的常量/名称/变量。
///   
/// 构建结果可以被 Decompiler.Decompile() 直接复用，
/// 经过完整的 Phase1→Phase2→Phase3 流水线。
/// </summary>
public class MinimalPycBuilder
{
    /// <summary>
    /// 从 MinimalContext 构建 .pyc 文件。
    /// </summary>
    public byte[] BuildPyc(MinimalContext ctx, string pythonVersion)
    {
        // 1. 选择 magic number
        var magic = pythonVersion switch
        {
            "3.10" => new byte[] { 0x6F, 0x0D, 0x0D, 0x0A },
            "3.11" => new byte[] { 0xA7, 0x0D, 0x0D, 0x0A },
            "3.12" => new byte[] { 0xC0, 0x0D, 0x0D, 0x0A },
            _ => new byte[] { 0x6F, 0x0D, 0x0D, 0x0A }, // default 3.10
        };

        using var ms = new MemoryStream();
        using var bw = new BinaryWriter(ms);

        // 2. 写入 header (16B for 3.7+)
        bw.Write(magic);
        bw.Write(0L);  // 填充时间戳等 (不影响反编译)

        // 3. 以 marshal TYPE_CODE 格式写入最小 CodeObject
        WriteMinimalCodeObject(bw, ctx.Code, magic);

        return ms.ToArray();
    }

    private void WriteMinimalCodeObject(BinaryWriter bw, CodeObject code, byte[] magic)
    {
        // 按版本写入 TYPE_CODE
        // v3.8+: argcount, posonlyargcount, kwonlyargcount, nlocals, stacksize, flags
        bw.Write((byte)0x63);  // TYPE_CODE (99)
        bw.Write(code.ArgCount);     // int: argcount
        if (IsPython38Plus(magic))
            bw.Write(0);             // int: posonlyargcount
        bw.Write(0);                 // int: kwonlyargcount
        bw.Write(code.Varnames.Count); // int: nlocals
        bw.Write(2);                 // int: stacksize
        bw.Write(0x40);             // int: flags (CO_NOFREE = 0x40)

        // bytecodes
        WriteMarshalBytes(bw, SerializeInstructions(code.Instructions));
        
        // consts tuple
        WriteMarshalTuple(bw, code.Constants.Values.ToList());
        
        // names tuple
        WriteMarshalTuple(bw, code.Names.Cast<object>().ToList());
        
        // varnames tuple
        WriteMarshalTuple(bw, code.Varnames.Cast<object>().ToList());
        
        // freevars / cellvars (empty for minimal repro)
        WriteMarshalTuple(bw, new List<object>());
        WriteMarshalTuple(bw, new List<object>());
        
        // filename, name, firstlineno, lnotab
        bw.Write((byte)0x7A);  // TYPE_SHORT_ASCII_INTERNED
        bw.Write((byte)"<minimal>".Length);
        bw.Write(System.Text.Encoding.UTF8.GetBytes("<minimal>"));
        
        bw.Write((byte)0x7A);
        bw.Write((byte)code.Name.Length);
        bw.Write(System.Text.Encoding.UTF8.GetBytes(code.Name));
        
        bw.Write(1);  // firstlineno
        
        // lnotab (empty)
        bw.Write((byte)0x73);  // TYPE_STRING
        bw.Write(0);           // length 0
    }

    private byte[] SerializeInstructions(List<Instruction> instructions)
    {
        using var ms = new MemoryStream();
        foreach (var ins in instructions)
        {
            ms.WriteByte((byte)ins.Opcode);
            ms.WriteByte((byte)(ins.Argument ?? 0));
        }
        return ms.ToArray();
    }
}
```

### 3.8 复现流程速查

```
用户报告异常
    │
    ▼
┌─────────────────────────────────────────┐
│  CrashRecord 包含:                        │
│  - .pyc 文件哈希 → 定位原文件              │
│  - 崩溃块 ID → 确定失败位置                │
│  - 崩溃指令索引 → 精确到哪条指令            │
│  - 块指令序列 → 最小复现集                 │
└─────────────────┬───────────────────────┘
                  │
       ┌──────────┴──────────┐
       ▼                     ▼
  StackMachine测试         Minimal .pyc
  (秒级运行)             (完整流水线调试)
       │                     │
       ▼                     ▼
┌─────────────────────────────────────────┐
│  修复 StackMachine.Execute()             │
│  └─ 添加缺失的 case                      │
│  └─ 修复参数处理逻辑                      │
│  └─ 添加 SafePop() 保护                  │
│                                         │
│  验证: StackMachineTest 通过             │
│  验证: Minimal .pyc 完整反编译成功        │
└─────────────────────────────────────────┘
```

---

## 4. 已知问题清单

### 4.1 Lv3 嵌套深度测试失败

| 问题 | Severity | 影响版本 | 根因 | 解决方案 |
|------|---------|---------|------|---------|
| depth_5_try 内层 handler 显示 pass 而非 result=-N | Medium | 2.7, 3.5-3.10 | `ExtractExceptHandlerFromOffset` 收集 handler 块时边界判断过于宽松 — 同一基本块内 5 层 SETUP_FINALLY 的 handler 偏移共享相同的 RETURN_VALUE 后继块，导致最内层 handler 被最外层覆盖 | 在 handler 收集中增加偏移边界约束（`succ.StartOffset < nextHandlerOffset`），只收集当前 handler 范围内的块 |
| depth_5_while 期望 orelse=[] 而实际有 Continue() | Low | 3.8+ | WHILE 循环末尾的 JUMP_ABSOLUTE（跳回循环头）在 BlockDecompiler 中被剥离后，BuildWhileLoopBody 的 `GetStructuredBlockStmts` 未再次过滤冗余 Continue | 已在 `BuildWhileLoopBody` 末尾添加 `while(simpleStmts[^1] is Continue) simpleStmts.RemoveAt(...)` 修复 |
| depth_5_if 中 return None 出现在 if-body 内 | Low | 2.7, 3.5-3.10 | 函数末尾的 LOAD_CONST None + RETURN_VALUE 被分解为 Return(None) 并保留在 if-body 中，未从函数体弹出 | 已添加 `StripTrailingReturnNone` 递归剥离所有控制结构体中的末尾 return None |
| mixed 嵌套中 orelse 被跨块收集 | Medium | 2.7, 3.5-3.10 | `BuildTryFromBlock` 的 else 体收集从 `FindBlocksFromOffset(elseJumpTarget)` 开始，指向 handler 之后的 after_all 块而非 else 体本身 | 已修复：从 POP_BLOCK 块的后继中找 offset < handlerAbs 的块作为 else 体 |

### 4.2 v3.11+ 操作码相关问题

| 问题 | Severity | 根因 | 解决方案 |
|------|---------|------|---------|
| UNPACK_SEQUENCE 在 call-prep 与 tuple-unpack 双语义 | High | 3.11+ 调用协议中 UNPACK_SEQUENCE 有双重角色：a) 实际序列解包（a,b = ...）, b) 调用参数准备标记（print(a+b)）。StackMachine 无法区分两者 | 需要上下文感知处理：检测后续指令（CALL vs STORE）或模拟 PUSH_NULL sentinel 检测。当前作为 no-op，函数调用正确但 tuple 解包显示完整元组 |
|| 部分 3.11 .pyc 文件 "Constants read failed" | Medium | 3.11 marshal 嵌套 code object 的 _refList 管理差异 | ReadMarshalCodeObject 的 ref 索引需正确管理 |
|| 3.12 嵌套 CodeObject marshal 流同步 (0x64) | High | 读取嵌套 CodeObject 的 co_consts 时遇到未知 type 0x64，流已偏移。根因为部分字段尺寸计算错误导致后续 type byte 位置不对齐 | 用 Python marshal.dumps() 对比预期结构，定位 reader 何处多读/少读字节 |

### 4.3 控制流构建问题

| 问题 | Severity | 根因 | 解决方案 |
|------|---------|------|---------|
| depth_5_for 循环最后一层变量未被有效使用 | Low | FOR_ITER 的循环变量（`e`）从迭代器正确弹出，但嵌套太深时某些赋值被死代码消除删除 | 暂不影响输出正确性，后续在死代码消除中增加赋值保护 |
| while 循环头检测在条件分支块中偶尔误判 | Medium | `IsConditionBranch` 同时检测 POP_JUMP_IF_* 和 JUMP_BACKWARD，回边与条件分支共享检测路径 | 在 `GetStructuredBlockStmts` 中添加向后跳转检测，优先判定为循环继续而非 if/else |
| 嵌套 try 在 3.11+（ExceptionTable）尚未实现 | High | 3.11+ 的异常处理使用 ExceptionTable（try 范围表）替代 SETUP_FINALLY/POP_BLOCK 模式，AstBuilder 还未解析 ExceptionTable 来构建 try 结构 | 在 Phase 6 中实现，需要解析 `CodeObject.ExceptionTable` 的 [start, end, target, depth] 条目 |

### 4.4 代码生成质量问题

| 问题 | Severity | 根因 | 解决方案 |
|------|---------|------|---------|
| `a, b = (10, 3)` 显示为 `a = (10, 3)` | Low | 3.11+ 的 UNPACK_SEQUENCE 在 call-prep 模式中作为 no-op，在 tuple-unpack 模式下也应 no-op。导致 STORE_NAME 消费整个 tuple 而非解包后的元素 | 需要 UNPACK_SEQUENCE 的上下文检测修复（见 4.2） |
| `print()` 显示为 `print` | Low | print() 的零参数调用在字节码中表现为 LOAD_NAME 'print' + POP_TOP，POP_TOP 弹出 Name('print') 并生成 ExprStmt(Name('print'))，最终输出未格式化的 | 代码生成器中为 Call(Name('print'), [], []) 特殊处理输出 `print()`，但零参数 case 在 POP_TOP 分支中未覆盖 |
| `return None` 在函数末尾被剥离 | Low(预期行为) | 隐式 `return None` 被 `StripTrailingReturnNone` 剥离，但显式 `return None` 也会被剥离 | 需要区分：显式 return（在源码中有 return 关键字）vs 编译器隐式注入的 return。目前无法区分，均为剥离 |
| module-level `return None` 被剥离 | Low(预期行为) | `Build()` 方法中 strip 逻辑已处理 | 在 ClassDef body 中也做了类似剥离 |

### 4.5 测试框架问题

| 问题 | Severity | 根因 | 解决方案 |
|------|---------|------|---------|
| AST 比较过于严格 | Medium | 使用 pycdc 的 tokenized AST dump 作为预期 | 增加语义等价比较 |
| 测试编译矩阵不含 3.11/3.12 版本矩阵 | Medium | compile_pyc_matrix.py 未对整个套件运行 | 已编译 91 个 3.11 + 91 个 3.12 文件 |

---

## 5. 附录：CPython 版本 Magic Number 速查

| Python 版本 | Magic 2B(LE) | 文件首字节 | Header大小 | 说明 |
|-----------|-------------|-----------|-----------|------|
| 2.7 | `03F3` | `0x03` | 8B | 最长支持版本，marshal 格式差异最大 |
| 3.5 | `170D` | `0x17` | 12B | 引入 wordcode |
| 3.6 | `330D` | `0x33` | 12B | 小的字节码变化 |
| 3.7 | `420D` | `0x42` | 16B | header 增加至 16B |
| 3.8 | `550D` | `0x55` | 16B | JUMP_IF_NOT_EXC_MATCH |
| 3.9 | `610D` | `0x61` | 16B | IS_OP/CONTAINS_OP |
| 3.10 | `6F0D` | `0x6F` | 16B | YIELD_FROM 重编号 |
| 3.11 | `A70D` | `0xA7` | 16B+CACHE | 操作码全面重编号，CACHE 引入 |
| 3.12 | `C00D` | `0xC0` | 16B+CACHE | CALL 重编号(167→171) |
| 3.13 | (待查) | — | — | 待支持 |
