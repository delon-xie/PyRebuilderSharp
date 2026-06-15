# Version Isolation Architecture Plan (v1.0)

> 目标：消除 PyRebuilderSharp 中散布的 `if (IsPythonX())` 魔数条件，
> 将每个 Python 版本的 marshal 格式、字节码格式、操作码映射封装为独立模块。
> 基于 `docs/pyc_format_reference.md` 中 CPython 源码验证的知识。

---

## 问题现状

当前代码中有 30+ 处版本条件判断散布在 PycReader.cs 中：
```csharp
if (IsPython27()) { ... }
if (IsPython311Plus()) { ... }
if (_pythonMinorVersion == 13) { ... } else { ... }
```

这种方式的问题：
1. **添加新版本需要改 5+ 处**（版本检测、操作码映射、cache 表、字节码解析、异常表解析）
2. **条件嵌套导致逻辑路径爆炸**（3.11×3.12×3.13×3.14 的组合数）
3. **延续性假设错误**（例如 3.13 的 `MapOpcodePy313` 代码和 3.14 的 `MapOpcodePy314` 应该完全独立，但当前通过 `MapOpcodePy311` 的 `is312` 分支处理 3.12）

---

## 架构设计

### 核心：`PythonVersion` 枚举 + `IVersionStrategy` 接口

```csharp
public enum PythonVersion {
    Py27, Py35, Py36, Py37, Py38, Py39, Py310,
    Py311, Py312, Py313, Py314
}

public interface IVersionStrategy {
    PythonVersion Version { get; }
    int HeaderSize { get; }
    int HaveArgument { get; }
    bool IsWordOffset { get; }
    bool HasCaches { get; }
    bool HasExceptionTable { get; }
    bool HasLinetable { get; }
    bool HasQualname { get; }
    bool IsCodeSimple { get; }
    bool UseLocalsPlus { get; }
    
    Opcode MapOpcode(byte rawOp);
    int GetCacheCount(byte rawOp);
    int GetHaveArgument();
    bool IsJumpInstruction(Opcode op);
}
```

### 版本工厂
```csharp
public static class VersionStrategyFactory {
    public static IVersionStrategy Create(byte[] magic) { ... }
}
```

### 各版本策略类
```
VersionStrategy27   — Python 2.7 特殊处理
VersionStrategy35_36_37 — 3.5-3.7, 可变长字节码
VersionStrategy38_39_310 — 3.8-3.10, wordcode
VersionStrategy311  — 3.11, 稀疏 cache
VersionStrategy312  — 3.12, 全量 cache
VersionStrategy313  — 3.13, HAVE_ARGUMENT=44
VersionStrategy314  — 3.14, HAVE_ARGUMENT=43
```

---

## 迁移步骤

### Phase 1：策略接口定义 + 版本分发
1. 定义 `PythonVersion` 枚举 + `IVersionStrategy` 接口
2. `VersionStrategyFactory.Create(magic)` 根据魔数决定版本
3. 在 `PycReader.Read()` 入口处创建策略并注入

### Phase 2：逐版本迁移（从后往前）
按 3.14 → 3.13 → 3.12 → 3.11 → 3.8-3.10 → 3.5-3.7 → 2.7 顺序：

1. **移出 MapOpcodePy314 → VersionStrategy314.MapOpcode()**
2. **移出 GetCacheCount314 → VersionStrategy314.GetCacheCount()**
3. **移出 IsJumpInstruction314 → VersionStrategy314.IsJumpInstruction()**
4. **移出字节码解析差异 → VersionStrategy314 的方法或属性**
5. **移出 marshal 读取差异 → 在 ReadCodeObject 中使用策略的格式属性**

### Phase 3：重构 PycReader
- `ReadCodeObject()` 使用 `_strategy.HeaderSize` 替代魔数硬编码
- `ParseInstructions()` 使用 `_strategy.IsWordOffset` 替代 `IsWordOffsetVersion()`
- `ParseInstructions311Plus()` 使用 `_strategy.MapOpcode()` + `_strategy.GetCacheCount()`
- Exception table 解析使用 `_strategy.HasExceptionTable`

### Phase 4：文档 + 测试
- 更新 `docs/pyc_format_reference.md`
- 每个版本独立的回归测试
- 验证所有 2.7-3.14 的 abc.py 白盒测试

---

## 风险与缓解

| 风险 | 缓解 |
|:-----|:------|
| 重构期间 3.14 功能退化 | 每步 dotnet build + abc.3.14 回归 |
| 接口设计过度工程化 | 先从 3.14 需要的最小接口开始 |
| AstBuilder/CodeGenerator 也有版本依赖 | Phase 2 只动 PycReader, Phase 3 再扩展 |
