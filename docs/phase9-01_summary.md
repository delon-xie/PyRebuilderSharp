# Phase 9-01 总结文档

> 日期: 2026-07-10
> 修复: CFG handler→class edge 误分类

---

## 变更文件

| 文件 | 改动 |
|------|------|
| `src/.../Scanners/BlockScanner.cs` | +89 行 (CleanHandlerSuccessors + IsClassOrFuncDefinition + Scan 集成 + ExceptionTable 过滤) |

## 回归验证

| 指标 | 修复前 | 修复后 | 变化 |
|------|:------:|:------:|:----:|
| 全量基线 | 1325/1325 | 1325/1325 | → ✅ |
| 孤儿块 | 0 | 0 | → ✅ |
| A+B 可接受 | 52 (4%) | 52 (4%) | → |
| Diff lines | 146007 | 146007 | → |
| 白盒通过 | 299 | 299 | → ✅ |
| `dotnet build` | 0 errors | 0 errors | → ✅ |

## 修复内容

### 1. ExceptionTable handler 边过滤（3.11+）

`LinkBlocks()` 中 ExceptionTable handler 边现在排除 class/func 定义块（`IsClassOrFuncDefinition`），防止 ET handler 边连接到 LOAD_BUILD_CLASS / MAKE_FUNCTION 块。

### 2. 后处理清理（全版本）

新增 `CleanHandlerSuccessors()` 方法，处理 3.10- 版本中通过 RAISE_VARARGS fallthrough 或其他路径产生的 handler→class/func 错误边：
- 检测 handler 块（`BlockFlags.ExceptionHandler`）的后继中的 class/func 定义
- 移除错误边，自动重新连接最近的非 handler 前驱

### 3. 检测规则

```csharp
IsClassOrFuncDefinition(block):
  - LOAD_BUILD_CLASS → class 定义
  - LOAD_CONST/LOAD_CLOSURE + MAKE_FUNCTION/MAKE_CLOSURE → 函数定义
```

## 实施中的问题

1. **`AddSuccessor` 是实例方法** — `CleanHandlerSuccessors` 原设计为 `static`，但调用实例方法失败。改为实例方法。
2. **Opcode 名不存在** — `LOAD_CLOSURE_313`, `MAKE_CLOSURE_312` 等命名不存在于 Opcode 枚举。仅用 `LOAD_CLOSURE`, `MAKE_FUNCTION`, `MAKE_CLOSURE`。
