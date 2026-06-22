# PyRebuilderSharp — 3.6 函数缺失诊断报告

**日期**: 2026-06-22
**基线**: 997/997 100%, Diff: 71681, 孤儿: 0
**状态**: P0a 根因已定位，修复未完成

---

## 诊断链（从外到内）

| 层级 | 发现 | 结论 |
|:-----|:------|:------|
| `[BUILD] stmts count=1` | `PostProcessFunctionDefs` 仅收到 1 个语句 | `_blockResults[0]` 只有 1 个语句 |
| `[PP_ENTRY]` | 确实只有 1 个语句进入後处理器 | 函数定义不在 stmts 列表中 |
| `[STORE_NAME] val=FunctionRef` | 第一次反编译生成了正确的 `Assign` | ✅ StackMachine 工作正常 |
| `[STORE_NAME]` 出现两次 | 模块块被反编译**两次** | 第二次覆盖了第一次的结果 |
| `[MF_default] codeName=<module>` | 两次都是同一个模块代码 | 第二次来自 `BuildFunctionDef` → 子 `AstBuilder` |
| 单文件运行超时（15s+） | 第二次反编译导致死循环/超时 | 异常被 `DecompileBlock` 的 catch 捕获 |
| `ParseInstructionsWordcode` | 3.6 指令解析正确 | ✅ 不是解析器问题 |
| `MapOpcode(90) = STORE_NAME` | Opcode 映射正确 | ✅ 不是 opcode 问题 |

## 根因链

```
Build() 行 51: _blockResults = DecompileBlocks(...)    ← 第一次：正确（6+ 语句）
  ↓
Build() 行 447: stmts = PostProcessFunctionDefs(stmts)
  ↓     BuildFunctionDef() 行 4245: new AstBuilder(childCode)
  ↓        childBuilder.Build(cfg)
  ↓           child 块的 DecompileBlocks(...)            ← 第二次？
  ↓              子块处理崩溃/超时 → FallbackAsComment
  ↓                 但这是子 Builder，不影响父 Builder
  ↓
Build() 行 449: stmts = ConvertChildCodesToFunctionDefs(stmts)
```

## 真实原因推测

`AstBuilder` 构造函数（行 4245：`new AstBuilder(childCode)`）可能引用了全局状态，导致父子 `AstBuilder` 共享 `_blockResults`。当子 Builder 崩溃时，父的 `_blockResults` 被覆盖。

## 修复方向

**方案 A**: `BuildFunctionDef` 中使用独立的 `AstBuilder` 构造函数（不共享任何状态）。

**方案 B**: 在 `PostProcessFunctionDefs` 中缓存 `FunctionRef.Code` 的副本，不在 `BuildFunctionDef` 内创建子 `AstBuilder`，而是延迟到 `ConvertChildCodesToFunctionDefs` 处理。

**方案 C**: 在 `BuildFunctionDef` 中捕获所有异常并返回 `null`，确保不污染父 Builder 的 `_blockResults`。
