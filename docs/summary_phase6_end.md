# Phase 6 收尾总结 — PyRebuilderSharp

**版本**: v1.0
**日期**: 2026-06-14
**项目**: PyRebuilderSharp (.NET 10 + Avalonia GUI)

---

## 一、Phase 6 目标

Phase 6 的目标是完成 v3.11+ 完整反编译流水线，包括：新操作码适配、ExceptionTable 驱动的控制流、无 SETUP_FINALLY 的异常处理、linetable 解析、CACHE 字节对齐、以及版本矩阵全覆盖。

---

## 二、完成清单

| Lv6 | 内容 | 文件 | 状态 |
|:----|:------|:------|:------|
| **Lv6a** | v3.11+ 操作码适配（RESUME, COPY, SWAP, PRECALL, PUSH_EXC_INFO, PUSH_EXC_HANDLER, PULL_EXC_FROM_INFO, RERAISE, BINARY_OP, CALL, RETURN_CONST, MATCH_CLASS, MATCH_MAPPING, MATCH_SEQUENCE, MATCH_KEYS） | `PycReader.cs` MapOpcodePy311, `StackMachine.cs` handlers, `Opcode.cs` enum | ✅ **全部完成** |
| **Lv6b** | ExceptionTable 解析 + try 结构重建 | `PycReader.cs` ParseExceptionTable, `BlockDecompiler.cs` | ✅ Phase 3 完成 |
| **Lv6c** | 无 SETUP_FINALLY 的异常处理（3.11+ 模式） | `AstBuilder.cs` BuildTryFromBlock | ✅ Phase 3 完成 |
| **Lv6d** | **linetable 解析**（PEP 626 格式，替代 lnotab） | `PycReader.cs` ParseLinetable311() | ✅ **本阶段完成** |
| **Lv6e** | CACHE 条目处理（`rawOp==0` 跳过，不依赖 cache 表） | `PycReader.cs` ParseInstructions311Plus | ✅ **本阶段修复** |
| **Lv6f** | v3.11+ 版本矩阵测试（2.7→3.14 全覆盖） | `VersionMatrixTests.cs` | ✅ |

---

## 三、本阶段新增功能

### Lv6d — linetable 解析器 (`ParseLinetable311`)

实现 Python 3.11+ `co_linetable`（PEP 626 格式）解码器：

| 编码类型 | 字节数 | 字段 |
|:---------|:-------|:-----|
| 短条目 (code 0) | 2 字节 | line delta (4b) + end delta (6b) |
| 中条目 (code 1) | 3 字节 | line delta (8b) + end delta (6b) |
| 长条目 (code 2) | 4+ 字节 | line delta (6b) + column + end delta |
| 哨兵 (code 3) | 2 字节 | 终止标记 |

已集成到 `CodeObject`：新增 `LineNumberBytes`、`HasLinetable` 字段。

### Lv6e — CACHE 修复

移除不可信的 `GetCacheCount312` 表（LOAD_CONST=1、LOAD_NAME=4 等与实际编译输出不一致）。改为 `ParseInstructions311Plus` 只跳过 `rawOp==0` 字节。

---

## 四、跨阶段修复（Phase 3–6 联动）

| 修复 | 来源 | 影响 |
|:-----|:------|:------|
| `ReadRawMarshalBytes` 新增 TYPE_REF 处理 | Phase 3 | co_names 正确 |
| ROT_TWO=2 ↔ PUSH_NULL=2 枚举冲突 | Phase 4 | class 定义输出 |
| cache 表 → `rawOp==0` 跳过 | Phase 6 | CALL/指令正确解析 |
| `ParseLinetable311()` | Phase 6 | 行号表可用 |
| match opcode 映射 | Phase 6 | match/case 不崩溃 |
| walrus NamedExpr + 检测 | Phase Fix | `:=` 基础支持 |
| `except*` IsGroup + codegen | Phase Fix | `except*` 渲染 |

---

## 五、Phase 6 关闭后完成的工作

Phase 6 全部 6 个子任务已完成。额外完成：

| 项目 | 优先级 | 完成状态 |
|:-----|:-------|:---------|
| `except*` ExceptionTable → IsGroup 映射 | 🔴 高 | ✅ `BuildTryFromExceptionTable` + CHECK_EG_MATCH |
| walrus 控制流检测 | 🟢 低 | ✅ NamedExpr + COPY+STORE 检测 |
| AST 自动对比验证 | 🟡 中 | ✅ `tools/ast_compare.py` |
| CrashCollector Dashboard | 🟡 中 | ✅ Avalonia 崩溃日志面板 |
| 批量反编译模式 | 🟢 低 | ✅ CLI `-d <dir>`, `--stats` |

### 剩余工作（1 项）

| 项目 | 优先级 | 说明 |
|:-----|:-------|:------|
| `match/case` ExceptionTable CFG 重建 + AST | 🔴 高 | 需要 Match/MatchCase/MatchPattern 节点 + 代码生成器 |

---

## 六、项目总览

| 阶段 | 内容 | 状态 |
|:------|:------|:------|
| Phase 1–2 | CLI + Avalonia GUI 基础设施 | ✅ 关闭 |
| Phase 3 | marshal 收敛 + Lv3 嵌套 + 交叉嵌套修复 | ✅ 关闭 |
| Phase 4 | def/class/yield/@decorator/async + 展开赋值 | ✅ 关闭 |
| Phase 5 | 编译脚本全覆盖 + 工程增强基础 | ✅ 关闭 |
| Phase Fix | 9 项已知问题 + walrus + except* + match opcode | ✅ 关闭 |
| **Phase 6** | **v3.11+ 完整反编译流水线（Lv6a–Lv6f）** | ✅ **关闭** |
