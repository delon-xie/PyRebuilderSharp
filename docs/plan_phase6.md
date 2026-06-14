# Phase 6 — v3.11+ 完整反编译流水线（P2）

**版本**: v3.0
**日期**: 2026-06-14
**前提**: Phase 3 ✅ · Phase 4 ✅ · Phase 5 ✅ · Phase Fix ✅  全部关闭

---

## 一、已完成

| 项目 | 内容 | 文件 | 状态 |
|:-----|:------|:------|:------|
| Lv6a 操作码 | RESUME, COPY, SWAP, PRECALL, PUSH_EXC_INFO, PUSH_EXC_HANDLER, PULL_EXC_FROM_INFO, RERAISE, BINARY_OP, CALL, RETURN_CONST + match opcodes | `PycReader.cs`, `StackMachine.cs`, `Opcode.cs` | ✅ **全部完成** |
| Lv6b ExceptionTable | 异常表解析 + try 结构重建 | `BlockDecompiler.cs` | ✅ 完成 |
| Lv6c 异常处理 | 无 SETUP_FINALLY 的 3.11+ 模式 | `AstBuilder.cs` | ✅ 完成 |
| **Lv6d linetable** | 3.11+ `co_linetable` PEP 626 解析器 | `PycReader.cs` → `ParseLinetable311()` | ✅ **已完成** |
| Lv6e CACHE | `rawOp==0` 跳过 | `PycReader.cs` | ✅ 已修复 |
| Lv6f 版本矩阵 | 77 测试 2.7→3.14 | `VersionMatrixTests.cs` | ✅ |

## 二、已关闭的任务

以下任务已在 Phase Fix 中完成：

- `PULL_EXC_FROM_INFO_312` 操作码实现
- `RERAISE` 操作码实现
- `PUSH_EXC_HANDLER_312` 操作码实现
- `PUSH_EXC_INFO_312` 操作码实现
- `RETURN_CONST` 3.12 映射 (121=0x79)
- 3.12 cache 表修复（改为只跳过 `rawOp==0`）
- match/case 3.12 opcode 映射 (MATCH_CLASS=152, MATCH_MAPPING=31, MATCH_SEQUENCE=32, MATCH_KEYS=33)
- walrus `:=` NamedExpr + COPY+STORE 检测
- `except*` IsGroup 标志 + codegen
- linetable 解析 `ParseLinetable311()` 实现

## 三、Phase 6 总结

|lvLv6 全部 6 个子任务（Lv6a–Lv6f）已完成。实际实现与实际输出验证均通过。Phase 6 可以关闭。

## 四、后续工作

Phase 6 关闭后，剩余未完成工作已移入 Phase Fix：

| 项目 | 优先级 | 类型 |
|:-----|:-------|:------|
| `match/case` ExceptionTable CFG 重建 | 🔴 高 | 语法覆盖 |
| `except*` ExceptionTable → IsGroup 映射 | 🔴 高 | 语法覆盖 |
| walrus 控制流检测 | 🟢 低 | 语法覆盖 |
| AST 自动对比验证 | 🟡 中 | 工程增强 |
| CrashCollector Dashboard | 🟡 中 | 工程增强 |
| 批量反编译模式 | 🟢 低 | 工程增强 |
