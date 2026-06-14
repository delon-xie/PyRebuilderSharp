# Phase 6 — v3.11+ 完整反编译流水线（P2）

**版本**: v2.0
**日期**: 2026-06-14
**前提**: Phase 3 ✅ · Phase 4 ✅ · Phase 5 ✅ · Phase Fix ✅  全部关闭

---

## 一、已完成

| 项目 | 内容 | 文件 | 状态 |
|:-----|:------|:------|:------|
| Lv6a 操作码 | RESUME, COPY, SWAP, PRECALL, PUSH_EXC_INFO, PUSH_EXC_HANDLER, PULL_EXC_FROM_INFO, RERAISE, BINARY_OP, CALL, RETURN_CONST | `PycReader.cs`, `StackMachine.cs` | ✅ **全部完成** |
| Lv6b ExceptionTable | 异常表解析 + try 结构重建 | `BlockDecompiler.cs` | ✅ Phase 3 完成 |
| Lv6c 异常处理 | 无 SETUP_FINALLY 的 3.11+ 模式 | `AstBuilder.cs` | ✅ Phase 3 完成 |
| Lv6e CACHE | `rawOp==0` 跳过 | `PycReader.cs` | ✅ 已修复 |
| Lv6f 版本矩阵 | 77 测试 2.7→3.14 | `VersionMatrixTests.cs` | ✅ |

## 二、待完成

### Lv6d — linetable/co_lines 解析（下一优先级）

`co_linetable` 为 3.11+ 新增的字节码行号表，替换旧的 `co_lnotab`。当前作为 raw bytes 读取但未解析。

| 子任务 | 难度 | 优先级 |
|:-------|:-----|:-------|
| linetable 解析算法 | 🟡 中 | P1 |
| co_lines() API 暴露 | 🟢 低 | P2 |

## 三、已关闭的任务

以下任务已在 Phase Fix 中完成，不再保留在 Phase 6：

- `PULL_EXC_FROM_INFO_312` 操作码实现
- `RERAISE` 操作码实现
- `PUSH_EXC_HANDLER_312` 操作码实现
- `PUSH_EXC_INFO_312` 操作码实现
- `RETURN_CONST` 3.12 映射 (121=0x79)
- 3.12 cache 表修复（改为只跳过 `rawOp==0`）

## 四、建议执行的优先级

1. **Lv6d linetable 解析** — 🟡 中优先级，修复后影响行号显示而非输出正确性
2. **Phase Fix 6 项** — 按 `docs/plan_phase_fix.md` 执行
