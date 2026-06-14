# Phase Log FX — 日志驱动的反编译修复管道

**版本**: v1.0
**日期**: 2026-06-14
**前置**: Phase 1–6 + Phase Fix 全关闭 · 错误日志框架就位 ✅

---

## 一、核心理念

**不再用上帝视角修改代码**。改为日志驱动的工作流：

1. 全量基准测试 → 生成 `~/.pyrebuilder/crashes/*.json`
2. 日志分析工具 `crash_report.py` → 去重、分类、排序
3. 根据日志反馈 → 单次修复一个异常类型
4. 重新基准测试 → 验证修复 → 循环

---

## 二、工作流

```
                 ┌──────────────────────┐
                 │ 全矩阵基准测试 (938)    │
                 │ `dotnet run MarshalDiag` │
                 └────────┬─────────────┘
                          ↓
                 ┌──────────────────────┐
                 │ 生成 crash JSON 文件    │
                 │ ~/.pyrebuilder/crashes/ │
                 └────────┬─────────────┘
                          ↓
                 ┌──────────────────────┐
                 │ crash_report.py 分析   │
                 │ → 去重异常类型          │
                 │ → 按文件数排序          │
                 │ → 输出报告              │
                 └────────┬─────────────┘
                          ↓
                 ┌──────────────────────┐
                 │ 选择 #1 异常 → 修复      │
                 │ (根据日志反馈定位问题)    │
                 └────────┬─────────────┘
                          ↓
                 ┌──────────────────────┐
                 │ 重新基准测试 → 验证      │
                 │ crash 减少则修复有效     │
                 └────────┬─────────────┘
                          ↓
                 ┌──────────────────────┐
                 │ 回到第二步 → 下一异常    │
                 │ 直至 0 crash            │
                 └──────────────────────┘
```

---

## 三、工具 — crash_report.py

```bash
python tools/crash_report.py
```

输出格式：

```
=== Crash Report ===
Total crash files: 142
Unique exception types: 3

#1 [98 files] NullReferenceException
  Message: Object reference not set to an instance of an object
  Files: test_nested.3.8.pyc, test_match.3.10.pyc, ...
  First file instructions: RESUME, LOAD_CONST, LOAD_NAME, ...
  Source summary: block_47 in PycReader.ReadMarshalCodeObject

#2 [32 files] IndexOutOfRangeException
  Message: Index was outside the bounds of the array
  Files: test_loops.3.12.pyc, ...
  First file instructions: ...
  Source summary: ...

#3 [12 files] InvalidOperationException
  Message: ...
```

---

## 四、日志增强

如果 crash_report.py 的输出不够定位问题（例如只有异常类型没有上下文），则增强 CrashCollector 的报告内容：

| 字段 | 当前 | 增强 |
|:-----|:------|:------|
| `FileName` | block_47 | 完整文件名 + 偏移 |
| `SourceSnippet` | RESUME... | 前 5 条指令 |
| `PythonVersion` | ? | 从 magic 读取的版本 |
| `Offsets` | (无) | 块偏移范围 |
| `BlockCount` | (无) | 总块数 / 失败块数 |

---

## 五、修复原则

1. **单次修复一个异常类型** — 不要同时修复多个
2. **验证方式**：重新基准测试 → crash 文件数减少
3. **回归测试**：16 个关键测试必须 100% 通过
4. **日志即文档**：crash 减少记录在 crash_report 中

---

## 六、基线数据

| 指标 | 基准 | 目标 |
|:-----|:-----|:-----|
| 关键测试 | 16/16 | 16/16 |
| Marsha 警告 | 0/938 | 0/938 |
| Crash 文件数 | TBD (运行基准) | 0 |
| 语法覆盖 | 15 项 | 15 项 |
