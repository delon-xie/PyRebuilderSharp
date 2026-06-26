# PycReader 失效分析报告

## 概述

PycReader 是 PyRebuilderSharp 反编译器的核心组件，负责解析 CPython 编译生成的 `.pyc` 文件。其正确性直接决定后续反编译的成败。本报告系统分析 PycReader 在处理 Python 2.7~3.14 版本 pyc 文件时可能失效的场景和原因。

---

## 一、失效场景分类

### 1. Magic Number 识别失败（高风险）

**失效原因**：`VersionStrategyFactory.Create()` 仅支持预定义的魔数列表，未识别的魔数会直接抛出异常。

**影响范围**：整个 pyc 解析流程完全中断。

**具体场景**：

| 场景 | 风险等级 | 说明 |
|------|---------|------|
| Python 3.15+ 新魔数 | **极高** | CPython 每年都会改变魔数，当前只支持到 `2B0E0D0A` (3.14) |
| 3.14 魔数格式变化 | **高** | 3.14 魔数不再遵循 `value.to_bytes(2, 'little') + b'\r\n'` 模式，而是使用 `_imp.pyc_magic_number_token`，未来版本可能继续改变 |
| 未覆盖的 3.x 子版本 | **中** | 当前仅覆盖部分魔数（如 3.5 只覆盖 `170D0D0A`），某些小版本更新可能引入新魔数 |

**代码位置**：`VersionStrategyFactory.cs:19-36`

```csharp
// 当前魔数映射不完整，3.5-3.10 仅覆盖部分变体
"170D0D0A" or "1C0D0D0A" or "200D0D0A" or ... => new VersionStrategyPre311(...)
```

---

### 2. Header 解析失败（高风险）

**失效原因**：PycReader 根据版本策略解析不同长度的头部，但存在以下问题：

#### 2.1 3.14+ 头部格式变化

**风险场景**：3.14 魔数格式已改变，未来版本可能调整头部布局。

**代码位置**：`PycReader.cs:79-108`

```csharp
// 当前假设 3.11+ 头部结构固定，未考虑未来变化
if (_strategy.HasPep552Header)
{
    var flags = br.ReadInt32();
    bool isHashBased = (flags & 0x01) != 0;
    if (isHashBased)
        br.ReadBytes(8); // hash (64 bits)
    else
        br.ReadInt32(); // timestamp
    br.ReadInt32(); // source_size
}
```

#### 2.2 PEP 552 标志位扩展

**风险场景**：CPython 可能在 flags 字段中添加新的标志位，当前只处理了 bit 0（hash-based）。

---

### 3. Marshal 格式变化（高风险）

#### 3.1 TYPE_CODE_SIMPLE 处理缺陷

**失效场景**：Python 3.11+ 引入了 `TYPE_CODE_SIMPLE` (0x73)，与 `TYPE_STRING` 共享相同的类型字节。

**风险**：`ReadMarshalValue()` 中 `TYPE_STRING = 115` 被直接映射为字节数组，但在 3.11+ 的 CodeObject 上下文中，0x73 可能是 `TYPE_CODE_SIMPLE`。

**代码位置**：`PycReader.cs:1365`

```csharp
MarshalType.TYPE_STRING => ReadMarshalBytesDirect(br), // 115 = 0x73
```

**实际问题**：虽然代码中有特殊处理（`ReadRawMarshalBytes`），但在复杂嵌套场景下仍可能出错。

#### 3.2 FLAG_REF 机制的版本差异

**失效场景**：3.4-3.7 和 3.8+ 的 FLAG_REF 行为不一致。

**代码位置**：`pyc-format-reference.md:117-122` 记录了关键问题：

> 3.5-3.7 文件里 TYPE_CODE 后确实有 4 字节 ref_index；3.8+ 没有

**当前处理**：`ReadMarshalObject()` 使用统一的 FLAG_REF 处理逻辑，但没有区分 3.8 前后的差异。

#### 3.3 新的 Marshal 类型

**失效场景**：CPython 可能引入新的 marshal 类型（如未来版本的特殊对象类型）。

**代码位置**：`ReadMarshalValue()` 的 switch 语句缺少默认处理的扩展性。

---

### 4. CodeObject 字段变化（极高风险）

#### 4.1 字段数量和顺序变化

| Python 版本 | 字段数量 | 关键差异 |
|------------|---------|---------|
| 2.7 | 4 字段 | argcount, nlocals, stacksize, flags |
| 3.5-3.7 | 5 字段 | +kwonlyargcount |
| 3.8-3.10 | 6 字段 | +posonlyargcount |
| 3.11+ | 5 字段 | -nlocals（由 localsplus 派生） |

**失效场景**：

- **3.11+ 删除 nlocals**：当前通过 `_strategy.HasCaches` 判断，但如果未来版本重新引入 nlocals 会失效
- **新字段添加**：未来版本可能添加新的 CodeObject 字段

**代码位置**：`PycReader.cs:131-182`

#### 4.2 LocalsPlus 格式（3.11+）

**失效场景**：3.11+ 使用 `localsplusnames + localspluskinds` 替代独立的 `varnames/freevars/cellvars`。

**风险点**：
- `localspluskinds` 的 kind 值定义可能变化（当前假设 0=var, 1=cell, 2=free）
- 未来可能引入新的 kind 类型

**代码位置**：`PycReader.cs:224-230`

```csharp
switch (kind)
{
    // localspluskinds uses bit flags matching CPython's CO_FAST_* constants:
    // CO_FAST_LOCAL=0x20, CO_FAST_CELL=0x40, CO_FAST_FREE=0x80
    // NOT simple 0/1/2 values!
    if ((kind & 0x80) != 0)        // CO_FAST_FREE
        freevars.Add(localsplusnames[i]);
    else if ((kind & 0x40) != 0)   // CO_FAST_CELL
        cellvars.Add(localsplusnames[i]);
    else                            // CO_FAST_LOCAL (0x20) or HIDDEN
        varnames.Add(localsplusnames[i]);
}
```

#### 4.3 Qualname 字段（3.11+）

**失效场景**：3.11+ 所有代码对象都有 qualname 字段，但解析逻辑在异常时静默跳过。

**风险**：qualname 读取失败会导致后续字段错位。

**代码位置**：`PycReader.cs:252-257`

---

### 5. 字节码格式变化（极高风险）

#### 5.1 操作码编号体系重构

**3.13 重大变更**：HAVE_ARGUMENT 从 90 变为 44，几乎所有操作码重新编号。

**3.14 变更**：HAVE_ARGUMENT 变为 43，继续调整操作码编号。

**失效场景**：

- **MapOpcode 映射缺失**：每个版本策略的 `MapOpcode()` 必须覆盖所有操作码，遗漏会导致错误的操作码映射
- **新操作码未映射**：如 3.14 的 `LOAD_SMALL_INT_314`, `LOAD_FAST_BORROW_314` 等
- **Super-instructions**：3.14 引入的超级指令（如 `CALL_PY_EXACT_ARGS`）未被映射，直接 fallback 为原始字节值

**代码位置**：各 `VersionStrategyXxx.MapOpcode()`

#### 5.2 CACHE 条目处理

**3.11**：稀疏模式（仅部分操作码有 cache）
**3.12+**：完整模式（几乎所有有参操作码都有固定 cache 条目）

**失效场景**：
- `GetCacheCount()` 返回值不正确会导致 CACHE 跳过错误
- 未来版本可能改变 cache 策略

**代码位置**：各 `VersionStrategyXxx.GetCacheCount()`

#### 5.3 EXTENDED_ARG 链式参数

**失效场景**：3.11+ 的 EXTENDED_ARG 编码方式变化。

**3.6-3.10**：每次 EXTENDED_ARG 贡献 8 位，合并为 `(extArg << 8) | rawArg`
**3.11+**：保持相同逻辑，但 CACHE 条目影响偏移计算

**代码位置**：`PycReader.cs:821-826`

#### 5.4 特殊指令编码

**LOAD_GLOBAL 编码**（3.12+）：
```
arg = (name_idx << 1) | push_null_bit
```

**LOAD_ATTR 编码**（3.12+）：
```
arg = (name_idx << 1) | self_or_null_bit
```

**失效场景**：未来版本可能改变这些编码规则。

**代码位置**：`PycReader.cs:838-852`

---

### 6. Linetable 格式变化（中风险）

#### 6.1 PEP 626 Linetable（3.11+）

**失效场景**：3.11+ 使用新的 linetable 格式，解析逻辑复杂。

**风险点**：
- Sentinel 码处理不完整（当前只处理了简单情况）
- 未来可能扩展 linetable 格式

**代码位置**：`PycReader.cs:1546-1599`

---

### 7. ExceptionTable 格式变化（中风险）

#### 7.1 3.11+ 变长编码

**失效场景**：3.11+ 使用 base-64 varint 编码的异常表。

**风险点**：
- 字段数量或编码方式可能变化
- 当前假设每条记录固定 4 个字段

**代码位置**：`PycReader.cs:1606-1631`

---

### 8. 字节码解析偏移计算（高风险）

#### 8.1 Word Offset vs Byte Offset

**3.10+**：跳转偏移使用 word 偏移（需 ×2 转换为字节偏移）

**失效场景**：
- `IsJumpInstruction()` 判断不准确会导致跳转目标计算错误
- 未来版本可能改变偏移单位

**代码位置**：`PycReader.cs:835-836`, `900-901`

---

## 二、失效影响分析

| 失效层级 | 影响 | 示例 |
|---------|------|------|
| **致命** | 解析完全失败，抛出异常 | Magic Number 未识别 |
| **严重** | CodeObject 结构破坏，后续分析全部错误 | 字段错位（如漏读 qualname） |
| **中等** | 部分指令解析错误，反编译结果不准确 | 操作码映射错误 |
| **轻微** | 元数据丢失，不影响核心逻辑 | 行号表解析失败 |

---

## 三、当前代码的防护机制

### 3.1 安全限制

```csharp
private const int MaxMarshalDepth = 100000;  // 递归深度限制
private const int MaxMarshalCalls = 50000;    // 调用次数限制
private const int MaxReadSeconds = 15;        // 读取超时
```

### 3.2 异常捕获和日志

```csharp
// 多处 try-catch + LogCatch 记录位置信息
try { code.FirstLineNumber = br.ReadInt32(); }
catch (Exception ex) { LogCatch(br, "ReadMarshalCodeObject.firstlineno", ex); }
```

### 3.3 版本策略隔离

通过 `IVersionStrategy` 接口隔离版本差异，每个版本有独立的策略实现。

---

## 四、潜在失效的触发条件

### 4.1 版本升级触发

| 触发事件 | 失效类型 | 严重程度 |
|---------|---------|---------|
| Python 3.15 发布 | Magic Number 未识别 | 致命 |
| 新操作码引入 | MapOpcode 映射缺失 | 严重 |
| HAVE_ARGUMENT 阈值变化 | 参数解析错误 | 严重 |
| CodeObject 字段变化 | 字段错位 | 致命 |

### 4.2 编译选项触发

| 编译选项 | 失效类型 | 说明 |
|---------|---------|------|
| `--with-lto` | Marshal 格式变化 | LTO 优化可能改变字节码结构 |
| 调试模式 | 额外元数据 | 可能包含调试信息 |
| 特殊构建配置 | 自定义魔数 | 非标准 Python 发行版 |

### 4.3 平台差异触发

| 平台 | 失效类型 | 说明 |
|------|---------|------|
| 32 位系统 | 整数大小 | 某些字段可能使用不同大小 |
| 大端序系统 | 字节序 | 当前假设小端序 |

---

## 五、失效检测和定位方法

### 5.1 运行时检测

```csharp
// 现有的日志机制
private void LogCatch(BinaryReader br, string context, Exception ex)
{
    System.Console.Error.WriteLine(
        $"[WARN] PycReader.{context}: offset={br.BaseStream.Position}/{br.BaseStream.Length} " +
        $"marshalDepth={_marshalDepth} elapsed={_readTimer?.Elapsed.TotalSeconds:F1}s " +
        $"ex={ex.GetType().Name}: {ex.Message}");
}
```

### 5.2 检测指标

| 指标 | 异常值 | 可能原因 |
|------|-------|---------|
| `marshalDepth` 突增 | > 1000 | 循环引用或格式错误 |
| `offset` 跳跃 | 非预期的位置变化 | 字段长度错误 |
| `_refList` 越界 | 引用索引超出范围 | FLAG_REF 处理错误 |

---

## 六、代码优化建议

### 6.1 Magic Number 动态识别

**问题**：当前使用硬编码的魔数映射，无法应对新版本。

**优化方案**：
```csharp
// 基于魔数格式特征动态判断版本
public static IVersionStrategy Create(byte[] magic)
{
    // 3.14+ 魔数不再遵循 b'\r\n' 后缀模式
    if (magic[2] != 0x0D || magic[3] != 0x0A)
    {
        // 3.14+ 新格式，需要解析 token
        return DetectModernVersion(magic);
    }
    
    // 传统格式：前两字节 + \r\n
    ushort magicValue = BitConverter.ToUInt16(magic, 0);
    
    if (magicValue >= 0x0DA7) // 3.11+
    {
        if (magicValue >= 0x0E2B) return new VersionStrategy314();
        if (magicValue >= 0x0DE7) return new VersionStrategy313();
        if (magicValue >= 0x0DCB) return new VersionStrategy312();
        return new VersionStrategy311();
    }
    // ... 其他版本判断
}
```

### 6.2 字段解析的健壮性

**问题**：当前按固定顺序读取字段，一旦字段数量变化就会错位。

**优化方案**：使用基于字段描述符的解析方式。

### 6.3 Marshal 类型扩展机制

**问题**：`ReadMarshalValue()` 的 switch 语句难以扩展。

**优化方案**：使用策略模式或字典映射处理 Marshal 类型。

---

## 七、总结

### 失效风险矩阵

| 风险类别 | 风险等级 | 概率 | 影响 |
|---------|---------|------|------|
| Magic Number 未识别 | **极高** | 高（每年一次） | 致命 |
| 操作码映射缺失 | **高** | 中 | 严重 |
| CodeObject 字段变化 | **高** | 中 | 致命 |
| CACHE 条目变化 | **中** | 中 | 严重 |
| Marshal 格式变化 | **中** | 低 | 严重 |
| Linetable 变化 | **低** | 低 | 中等 |

### 核心结论

1. **最大风险来自版本升级**：每次 Python 主版本发布都可能引入破坏性变化
2. **3.13+ 是重灾区**：操作码编号体系重构，几乎每个版本都有重大调整
3. **防护机制有限**：当前的 try-catch 只能捕获异常，无法修复格式错误
4. **扩展能力不足**：硬编码的版本策略难以应对未来变化

### 建议措施

1. **建立版本检测自动化**：定期从 CPython 源码提取魔数和操作码定义
2. **增强容错能力**：实现更灵活的字段解析和错误恢复机制
3. **完善测试覆盖**：为每个版本添加完整的测试用例
4. **文档化版本差异**：维护详细的版本差异文档