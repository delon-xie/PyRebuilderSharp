# PyRebuilderSharp 阶段工作总结报告

**报告日期**: 2026-06-13 | **Version**: Phase 1-3 Complete | **测试基线**: 21/21 ✅

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
| Phase 3 — 混合嵌套 | for-in-if, if-in-try, try-in-for, while-in-if, else clause 检测 | 7/7 (Lv2) | ✅ | AstBuilder.cs (9项修复) |
| **总计** | **3 层级 × 7 版本 (2.7, 3.5-3.10)** | **21/21** | **✅** | |

### 1.3 项目规模

```
src/ 核心         42 个 .cs 文件, 7,220 SLOC
tests/ 测试       11 个 .cs 文件,   834 SLOC
测试数据           127 个 .py 源文件 → 550 个 .pyc 文件
测试基线           83 pycdc 测试集 × 7 版本 = 581 文件
```

### 1.4 架构四阶段流水线

```
.pyc → PycReader (Marshal) → BlockScanner (CFG) → AstBuilder (AST) → PythonCodeGenerator (源码)
       Phase 1 读取          Phase 2 分块            Phase 3 构建              Phase 4 生成
```

---

## 二、做得好的地方 — 值得表扬 ✅

### 2.1 逐块兜底策略（核心创新）

这是相比 pycdc 最大的设计差异，也是**本项目最具原创价值的设计决策**。

**pycdc 的问题**：全局状态 diff 驱动，一个 opcode 解析失败 → 整个函数体废掉，输出空 `pass`。

**PyRebuilderSharp 的做法**：
```
基本块 [B1, B2, B3, B4, B5]
  B1 ✅ → "x = a + b"
  B2 ✅ → "return x"
  B3 ❌ → "# [Block #3 Failed] offset=0x0040 Error: Unknown opcode"
  B4 ✅ → "y = 42"
  B5 ✅ → "print(y)"
```

**实现机制**：
- `BlockDecompiler.DecompileBlock()` 每个块独立 try/catch
- `BlockResult` 统一返回 Success / FallbackAsComment
- `CommentStmt` AST 节点使注释块与普通代码统一处理
- 输出格式包含偏移量、错误信息、原始字节码 — 便于调试

**效果**：即使部分块失败，整体输出仍包含最大可读代码。这对大型 .pyc 文件的实用价值远超 pycdc 的"全有或全无"模式。

### 2.2 测试驱动开发（TDD）的严格执行

这是项目**执行层面最值得表扬的地方** — 每次修改前先写测试，每次声称完成前跑验证：

- **版本矩阵测试**：3 层级 × 7 版本 = 21 个测试，每个版本独立编译 .pyc 文件
- **AST 语义比较**：对比 `ast.dump()` 输出而非字符串比较，忽略格式差异
- **pycdc 套件吸收**：83 个 pycdc 测试文件作为长期基线
- **每次迭代验证**：每个 bug 修复后跑 `dotnet test` 确认 21/21 不退化

### 2.3 文档先于代码

项目从开始就建立文档体系，设计文档在代码之前成型：
- `Python反编译总体设计.md` — 架构级决策（块隔离、阶段划分）
- `Python反编译详细设计.md` — 实现级细节（每 Opcode 的栈操作、AST 模型）
- `pyc-format-reference.md` — 从 CPython 源码推导的 .pyc 格式知识库（Magic Number、Header 布局、FLAG_REF 机制）
- `Phase1-ControlBlocks-Plan.md` — 17 种控制块的测试计划

**对 AI 辅助开发的启示**：清晰的文档让 AI 在每次对话时快速恢复上下文，不需要重复解释架构。

### 2.4 嵌套循环 StackOverflow 修复（关键发现）

这是 Phase 3 中**技术含量最高的修正**：

**问题**：C# 函数调用 `GetStructuredBlockStmts(bodyBlock, bodyVisited)` 中，`bodyVisited` 是独立新创建的 `HashSet`，内层循环的 body 块不在其中，导致外层循环迭代处理时无限递归。

**修复**：使用 `visited.Remove(bb)` 统一 managed visited 集

```csharp
// 旧：独立 bodyVisited → 嵌套 StackOverflow
var bodyVisited = new HashSet<BasicBlock>();
var stmts = GetStructuredBlockStmts(bodyBlock, bodyVisited);

// 新：同一 visited, Remove+Re-enter → 正确嵌套
foreach (var bb in bodyBlocks) visited.Remove(bb);
var stmts = GetStructuredBlockStmts(bodyBlock, visited);
```

**原理**：`CollectBodyBlocks` 把所有 body 块标记为 visited。先把它们移除，再用同一个 visited 集重入，内层循环自动把自己的 body 块重新标记进去。外层后续迭代正确跳过已处理块。

### 2.5 从 PyRebuild 中提取精华

PyRebuild (Python) 项目失败于性能瓶颈，但其设计思路非常出色，我们选择性地继承：
- **多引擎顺序兜底** → 简化为单引擎 + 注释兜底（当前阶段）
- **纯代码块(Block)** 的概念 → 完整继承，作为反编译的最小单位
- **JSON 中间表示** → 采用 AST record 类型 + 模式匹配
- **pycdc 测试集** → 完整复制，作为兼容性基线

---

## 三、中间出现的问题 — 经验教训 ⚠️

### 3.1 Phase 2 同类型嵌套的 4 个 P0/P1 bug

| Bug | 症状 | 根因 | 修复 |
|-----|------|------|------|
| YIELD_FROM opcode 缺失 | `yield from` 认作 `yield` | 3.10 中 YIELD_FROM=72 | 添加字节大小表 |
| STORE_ATTR 栈顺序反转 | `obj.attr = val` → 反了 | TOS=obj 误作 TOS=val | 交换弹栈顺序 |
| FLAG_REF 读取缺失 | 3.8+ .pyc 乱码 | CodeObject 字段未走 ReadMarshalObject | 全部统一走 ReadMarshalObject |
| except handler 误识别 | typed/bare except 区分失败 | DUP_TOP / POP_TOP×3 检测 | 检查 DUP_TOP 指令 |

### 3.2 Phase 3 混合嵌套的 9 项修复

| 问题 | 症状 | 修复 |
|------|------|------|
| for-in-if | for 循环被 while 拦截器捕获 | `!isForLoop` 过滤 |
| try body 为空 | SETUP_FINALLY 只扫当前块 | 按后继遍历收集所有 body 块 |
| spurious 内层 for | FOR_ITER 走 IsConditionBranch | FOR_ITER 检测前置 |
| 循环变量 `_` | SafePop() 跨块返回 null | 剥离无效 Assign |
| 空体缺 `pass` | if/for/try 空体空白 | EmitEmptyBodyPass() |
| 函数定义重复 | bodyVisited 不同步 | sync afterBranch → visited |
| while 变 if | BuildRestrictedIfElse 误判 LoopHeader | LoopHeader 检查 |
| if-in-try 消失 | POP_JUMP_IF_* 在 preBodyInstrs | preBodyInstrs 分支检测 |
| else 子句丢失 | 无 JUMP_FORWARD skip 时 else 认不出 | Predecessor+终端+BuildBlockOnly 三合一启发式 |

**教训**：控制块识别是"按特征猜结构"的启发式过程，每个新嵌套模式都需要新增检测规则。这是反编译器最难的地方，但**逐块兜底确保了每次修复都不影响已有功能**。

### 3.3 pycdc 的已知问题（印证我们的设计思路）

研究 pycdc 的 BUG 修复报告（2025-07 至 2026-06）发现 8 个正式合并的修复和 5 个本地修改：

**正式修复（Git 提交）**：
- RAISE_VARARGS bug、空栈保护、循环引用保护、EOF 检查、null dereference
- Python 3.11+ 异常表支持、SLICE opcodes、JUMP_BACKWARD、CO_ASYNC_GENERATOR
- FORMAT_VALUE f-string 修复、Long Numeric 表示修复

**本地修改（未合并）**：
- `ASTMap::m_unpack` 字典解包
- `ASTCondBlock::m_exceptVar` except as 语法
- `ASTIterBlock::m_compType` 推导式类型区分

**启示**：pycdc 团队也在不断修复问题，但 C++ 的复杂性使得每次修复都有引入新 bug 的风险。我们选择 C# + record 类型 + 模式匹配，从根本上降低了代码复杂度。

---

## 四、执行过程评价

### 4.1 "AI 驱动开发"的高效模式

本项目完全是在 AI 辅助下完成的，**整个项目 42 个源文件 7,220 SLOC 由 AI 生成，人工审查错误修复**。这种模式的关键成功因素：

1. **文档先行** — 设计文档作为 AI 的"北极星"，每次对话开始时加载，确保 AI 不偏离架构
2. **测试驱动** — 21 个版本矩阵测试作为"质量门禁"，AI 的每次修改必须通过全部测试
3. **小步迭代** — 每次只做一件事（一个控制块类型），测试通过后再推进
4. **记忆系统** — Hermes 的 MEMORY.md 和 Holographic Memory 让跨会话上下文保持

### 4.2 "9 步修复法"的经验

Phase 3 的 9 项修复展示了反编译器开发的典型模式：

```
发现失败测试 → 运行验证确认 → 阅读源码理解 → 定位根因 → 
设计修复方案 → 实施修复 → 运行所有测试确认不退化 → 记录问题 → 进入下一个
```

这个循环中**最关键的是 "确认不退化" 这一步** — 21 个测试确保每次修复不引入新问题。

### 4.3 值得改进的地方

1. **早期缺少 .pyc 编译矩阵自动化脚本** — 初期手动编译 7 个版本的 .pyc，后来才写了 `compile_pyc_matrix.py`
2. **C# 异步处理未使用** — `async`/`await` 模式在整个代码库中缺失，后续 GUI 可能需要
3. **pycdc 基线测试尚未全通** — 420/581 个 pycdc 测试文件因不支持的操作码而失败（预期内，但可以作为进度指标）

---

## 五、后续推进计划

### 5.1 Phase 4: 函数/类/模块（P0 优先级）

| 功能 | 描述 | 测试 |
|------|------|------|
| `def` 函数定义 | MAKE_FUNCTION + 压栈 = 函数签名的 AST | test_def_base.py |
| 默认参数 | MAKE_FUNCTION oparg > 0 → pop 默认值元组 | def f(x=10) |
| `class` 类定义 | LOAD_BUILD_CLASS + CALL_FUNCTION | test_class_base.py |
| `lambda` | MAKE_FUNCTION 简化版 | test_lambda_base.py |
| `return` / `yield` | RETURN_VALUE 外的返回形式 | test_yield_base.py |
| `import` | IMPORT_NAME + STORE | test_import_base.py |

### 5.2 Phase 5: 异常处理增强（P1）

| 功能 | 现状 | 目标 |
|------|------|------|
| `with` 语句 | 未实现 | SETUP_WITH + BEFORE_WITH 检测 |
| typed except | 基础版已实现 | 增强 ExceptHandler.Type/Name 提取 |
| `raise ... from` | 未实现 | RAISE_VARARGS + CAUSE |
| `finally` | 未实现 | SETUP_FINALLY + END_FINALLY 配对 |

### 5.3 Phase 6: 高级特性（P2）

- `LOAD_DEREF` / `STORE_DEREF` — 闭包变量的栈机模拟
- `async def` / `await` — async 函数支持
- `async for` / `async with` — 异步上下文
- `match` / `case` — Python 3.10+ 模式匹配（需要 CACHE 条目处理）
- `while` / `for` 的 `else` 子句 — 当前已部分支持，需要完整测试

### 5.4 GUI 完善（持续）

| 功能 | 优先级 | 状态 |
|------|--------|------|
| 语法高亮 (AvaloniaEdit) | P1 | ⏳ |
| 注释块高亮着色（红色背景） | P1 | ⏳ |
| 块级成功率统计 | P2 | ⏳ |
| 批量反编译（文件夹模式） | P2 | ⏳ |
| Python 版本选择器 | P2 | ⏳ |
| 源码保存对话框 | P2 | ⏳ |

### 5.5 Python 3.11+（暂缓，P3）

```
主要障碍：CACHE 条目（1-4B/opcode）、RESUME=90（与 STORE_NAME 冲突）、
BINARY_OP 统一、异常表替换指令编码。
目前 3.5-3.10 稳定后再推进。
```

### 5.6 版本矩阵测试升级

```
当前: 3 层级 × 7 版本 = 21 测试
Phase 4 后: 7 层级 × 7 版本 = 49 测试
完成后: 功能层级 × 7 版本 = ~60 测试
```

---

## 六、关键指标仪表板

```
📊 项目健康度
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
测试通过率   ■■■■■■■■■■ 21/21 (100%) ✅
代码质量     ■■■■■■■■■■ 0 error, 0 warning ✅
文档覆盖率   ■■■■■■■□□□ 4/6 份文档 ⚠️
GUI 完成度   ■□□□□□□□□□ 基础框架 ✅, 功能缺失
pycdc 兼容   ■□□□□□□□□□ ~30% 操作码覆盖 ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 代码规模趋势
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 0 (骨架)      ~2,000 SLOC
Phase 1 (单一)      ~4,500 SLOC  + 4 docs
Phase 2 (同类型)     ~5,800 SLOC  + 测试
Phase 3 (混合)       ~7,220 SLOC  + 21 tests ✅
Phase 4 (函数)       预计 ~9,000 SLOC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 七、总结

**PyRebuilderSharp 从一个实验性的 C# 移植尝试起步**，经过 3 个阶段的迭代，已发展为一个 42 文件、7,220 SLOC 的 Python 字节码反编译器，21 个版本矩阵测试全部通过。

**最大的成就不是反编译器的功能——而是确立了一套可复用的反编译器开发方法论**：
1. **逐块容错** — 让反编译器不再"全有或全无"
2. **测试驱动** — 版本矩阵测试确保 7 个 Python 版本的一致性
3. **文档先行** — 设计文档让 AI 驱动的开发保持方向
4. **小步迭代** — 每次只做一个控制块类型，测试通过再推进

**最大的教训**：控制块识别是"按特征猜结构"的启发式过程，每个新嵌套模式都意味着新的检测规则。这也是为什么 pycdc 有大把 P0/P1 bug 始终修不完——但我们的逐块兜底机制确保了：**即使某个块猜错了，其他块仍然正确**。

**下一个目标**：进入 Phase 4 — 函数/类/模块，这是从"玩具反编译器"到"实用反编译器"的关键一步。
