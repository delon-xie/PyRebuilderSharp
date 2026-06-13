# PyRebuilderSharp 阶段工作总结报告

**报告日期**: 2026-06-13 | **Version**: Phase 3+ | **测试基线**: 22/42 ✅ (+1 try nesting fix)

---

## 一、项目概览：从 PyRebuild → PyRebuilderSharp

### 1.1 立项背景

项目起源于对 Python 反编译器现状的不满：

- **pycdc (C++)**：功能最全但代码质量差 — 内存泄漏、全局变量满天飞、若出错则整体失败无兜底
- **pylingual**：ML 驱动在跨版本Python下的反编译效果良好,但在模型上进行迭代训练对系统环境的要求很高，时间复杂度更高，结果有很大不确定性（剩余30%不准确的反编译）
- **pycdc-studio / PyRebuild**：Python 版多引擎粘合层，受两个基础工具+ML兜底的思路，完全依赖外部工具的表现，不可控性太强。

**决策**：用 C# + .NET 10 + Avalonia 重写，以 pycdc 的 83 个测试文件为基线，以 PyRebuild 的多引擎块级兜底思路为架构设计参考，构建一个**原生跨平台**、**逐块容错**、**测试驱动**的 Python 字节码反编译器。

### 1.2 三阶段成果一览

| 阶段 | 范围 | 测试数 | 状态 | 核心文件 |
|------|------|--------|------|----------|
| Phase 1 — 单一控制块 | 表达式、顺序代码、if/while/for/try/break/continue | 7/7 (Lv0) | ✅ | StackMachine.cs |
| Phase 2 — 同类型嵌套 | 循环嵌套、if/elif/else 链、嵌套 try/except | 7/7 (Lv1) | ✅ | AstBuilder.cs |
| Phase 3 — 混合嵌套 | for-in-if, if-in-try, try-in-for, while-in-if, else clause 检测 | 7/7 (Lv2) + 1/21 (Lv3) | ✅ | AstBuilder.cs (10项修复) |

### 1.3 项目规模

```
-------------------------------------------------------------------------------
Language           Files    Total    Code  Comment  Blank    C/S  Comp%  Errs
-------------------------------------------------------------------------------
C#                    25    7523    6306     413    804   33.9   98.4     31
XML                    7     348     348       0      0    6.2   27.6      0
Markdown               3     446     446       0      0    2.0    0.0      0
Python                 7     278     209      24     45    0.3   84.3      0
Plain Text             7     145     145       0      0    0.7   24.1      0
JSON                   1      69      69       0      0    0.3   49.3      0
YAML                   1       8       8       0      0    0.0    0.0      0
-------------------------------------------------------------------------------
Total                 52    8817    7531     437    849   39.7   93.7     31
-------------------------------------------------------------------------------
```

---

## 二、做得好的地方 — 值得表扬 ✅

### 2.1 逐块兜底策略（核心创新）

**每个基本块独立反编译，失败输出注释块，绝不崩溃。** 这个策略让我们在 Phase 3 的 9 项修复过程中，始终保有 21 个通过测试的基线，不会因为一次修复失败而回归到 0。

```python
# 实际效果：即使 try 嵌套修复前只有 2 层，其他 if/for/while 测试完全不受影响
```

### 2.2 测试驱动开发（TDD）的红利

| 行为 | 结果 |
|------|------|
| 写测试先于写实现 | 每次重构都有安全网 |
| 版本矩阵 × 7 | 一个版本修好了，其他版本一起验证 |
| AST 比较 vs 文本比较 | 发现 pycdc 测试中的隐式 return None 问题 |

### 2.3 嵌套 try 修复的混合方法

**根因**：`BuildTryFromBlock` 用 BFS 从块后继收集 try body 块，在第一个 POP_BLOCK 处 BREAK。
- 嵌套的 SETUP_FINALLY 都在同一块内，handler 区域没有 CFG successor 边
- BFS 只收集到第一个 POP_BLOCK（最内层的），错过 3+ 层

**修复**：替换为混合扫描器 `ProcessTryBodyHybrid`
- 指令级递归：在当前块中检测内层 SETUP_FINALLY，递归构建 inner Try
- 块级 BFS：对后继块用 GetStructuredBlockStmts 处理 if/for/while
- Handler 隔离：`IsBlockInsideHandlerRegion` 过滤 handler 块
- 6 个新辅助方法：ExtractHandlerInstrs, DecompileHandlerInstrs, DetectIsExceptHandler, ExtractExceptType, FindPastHandlerEnd, FindHandlerEndOffset

**结果**：5 层纯 try 嵌套 ✅ | 混合嵌套仍 WIP

---

## 三、问题与教训 ⚠️

### 3.1 本次修复中的"坑"

| 坑 | 现象 | 修复 |
|----|------|------|
| BFS 在 POP_BLOCK 处 break | 只收集到最内层 try 的 POP_BLOCK | 移除 break，改用混合方法 |
| FindPastHandlerEnd 从 i+1 扫描 | 扫到内层 handler 的 POP_EXCEPT | 改为从 handlerAbs 开始扫描 |
| 指令级扫描无法处理 if/for/while | 混合嵌套丢失结构 | 增加块级 BFS 作为第三遍 |

### 3.2 已知问题（Phase 3 遗留）

| 问题 | 影响版本 | 根因 | 难度 |
|------|---------|------|------|
| args 为空 | v3.5-3.7 | PycReader marshal 中 kwonlyargcount 偏移 | 🔴 |
| while-orelse | v3.8-3.9 | while 循环的 else 子句生成 Pass() | ⚠️ |
| 混合嵌套排序 | v3.10+ | Try 和 If 的 AST 先后顺序 | ⚠️ |
| AST 解析 | v2.7 | Python 2 语法不被 Python 3 ast.parse 接受 | ❌ 暂缓 |

### 3.3 设计模式

**控制块识别的本质**：反编译器本质是"按特征猜结构"的启发式过程。每个新嵌套模式都需要新的检测规则。Pycdc 有大把 P0/P1 bug 始终修不完的根本原因就在于此。

**我们的应对**：逐块容错机制确保即使某个块猜错了，其他块仍然正确。混合方法将指令级（精准）和块级（结构化）扫描结合，兼顾精确度和完整性。

---

## 四、技术细节

### 4.1 文件结构

```
src/PyRebuilderSharp.Core/
├── Builders/
│   ├── AstBuilder.cs       ← Phase 2-3 核心，10 项嵌套修复（本文件）
│   ├── BlockDecompiler.cs   ← 逐块反编译引擎
│   └── StackMachine.cs      ← Phase 1 核心，表达式级反编译
├── Readers/
│   └── PycReader.cs         ← .pyc 文件读取（v3.5-3.7 已知问题）
├── Generators/
│   └── PythonCodeGenerator.cs ← AST → Python 代码
├── Models/
│   └── AST/CFG/Bytecode/
└── Testing/
    └── PycdcSuiteRunner.cs
```

---

## 五、Phase 3 修复清单

| # | 修复 | 日期 | 效果 |
|---|------|------|------|
| 1 | for-in-if 补全 | 6/12 | for 循环体如果有多个 if/while，补全缺失的结尾体 |
| 2 | try body 块收集 | 6/12 | 优化 try body 的块收集范围，支持复杂循环嵌套 |
| 3 | FOR_ITER 检查 | 6/12 | 在 IsConditionBranch 前检查，防止 for 循环被误判为 if |
| 4 | 移除无效 Assign | 6/12 | BuildForLoop 中 strip 无效的 Assign（如 i=i） |
| 5 | EmitEmptyBodyPass | 6/12 | 空循环体输出 pass |
| 6 | afterBranch visited 同步 | 6/12 | function def 块被重复处理的修复 |
| 7 | while-LoopHeader | 6/12 | while 循环的 LoopHeader 标记问题 |
| 8 | if-in-try 条件跳转 | 6/12 | try body 中 POP_JUMP_IF_* 的精确检测 |
| 9 | else 子句检测 | 6/12 | 精确的 else 子句检测规则 |
| 10 | **嵌套 try 递归修复** | **6/13** | **纯 5 层 try nesting ✅ | 详见下面 |**

### 嵌套 try 修复详解

**字节码结构**（depth_5_try, 3.10）：
```
 4: SETUP_FINALLY to 100   (最外层)
 6: SETUP_FINALLY to 82    (第4层)
 8: SETUP_FINALLY to 54    (第3层)
10: SETUP_FINALLY to 38    (第2层)
12: SETUP_FINALLY to 22    (最内层)
14: LOAD_CONST 42; 16: STORE_FAST result
18: POP_BLOCK; 20: JUMP_FORWARD to 34  (跳过最内层 handler)
22: POP_TOP×3, -1, POP_EXCEPT          (最内层 except: result=-1)
34: POP_BLOCK; 36: JUMP_FORWARD to 50
38: POP_TOP×3, -2, POP_EXCEPT          (第2层)
50: POP_BLOCK; 52: JUMP_FORWARD to 74
54: POP_TOP×3, -3, POP_EXCEPT          (第3层)
66: POP_BLOCK×2, RETURN                (第3层清理)
74: POP_BLOCK×2, RETURN                (第4/5层清理)
82: POP_TOP×3, -4, POP_EXCEPT          (第4层)
94: POP_BLOCK, RETURN                  (第4层清理)
100: POP_TOP×3, -5, POP_EXCEPT         (最外层)
```

**修复前输出**：
```python
try: result = 42
except: result = -5
```

**修复后输出**：
```python
try:
    try:
        try:
            try:
                try:
                    result = 42
                except:
                    result = -1
            except:
                result = -2
        ... (3 层) ...
    except:
        result = -4
except:
    result = -5
```

---

## 六、测试状态

| 测试方法 | 类型 | 用例数 | 状态 |
|----------|------|--------|------|
| Lv0_BasicBlocks | Lv0 | 7 | ✅ |
| Lv1_SameTypeNesting | Lv1 | 7 | ✅ |
| Lv2_MixedNesting | Lv2 | 7 | ✅ |
| Lv3_NestedDepth | Lv3 | 7 | ❌ **1/7** (v3.10 ✅) |
| Lv3_NestedMixed | Lv3 | 7 | ❌ 0/7 |
| Lv3_NestedMatrix | Lv3 | 7 | ❌ 0/7 |
| **总计** | | **42** | **22/22 ✅ / 20 ❌** |

---

## 七、总结

**PyRebuilderSharp 从一个实验性的 C# 移植尝试起步**，经过 3 个阶段的迭代，已发展为一个 52 文件、8,817 SLOC 的 Python 字节码反编译器，22 个版本矩阵测试通过。

**嵌套 try 修复是 Phase 3 最后的 P1 问题**。混合扫描方法解决了纯 try 嵌套问题，但混合嵌套（try+if/for/while）仍需改进。

**最大的成就不是反编译器的功能——而是确立了一套可复用的反编译器开发方法论**：
1. **逐块容错** — 让反编译器不再"全有或全无"
2. **测试驱动** — 版本矩阵测试确保 7 个 Python 版本的一致性
3. **文档先行** — 设计文档让 AI 驱动的开发保持方向
4. **小步迭代** — 每次只做一个控制块类型，测试通过再推进

**下一个目标**：进入 Phase 4 — 函数/类/模块，这是从"玩具反编译器"到"实用反编译器"的关键一步。同时处理 Lv3 遗留问题：混合嵌套排序、v3.5-3.7 marshal、while-orelse。
