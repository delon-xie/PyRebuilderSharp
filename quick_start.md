# PyRebuilderSharp 快速入门

## 环境要求

| 依赖 | 最低版本 | 备注 |
|:-----|:---------|:----|
| [.NET SDK](https://dotnet.microsoft.com/download) | 10.0 | 必须 .NET 10+（使用的 C# 13 特性） |
| OS | — | macOS / Windows / Linux 均可 |
| Git | 可选 | 用于克隆代码 |

**支持 Python 版本**：2.7, 3.5 ~ 3.14

### 验证安装

```bash
dotnet --version
# 应输出: 10.0.x
```

---

## 克隆与构建

### 1. 克隆仓库

```bash
git clone https://github.com/yourorg/PyRebuilderSharp.git
cd PyRebuilderSharp
```

### 2. 构建全部项目

```bash
dotnet build -c Release
```

**预期输出**：`0 个错误`（警告不影响运行）

### 3. 构建并启动 GUI

```bash
dotnet run --project src/PyRebuilderSharp.Gui -c Release
```

将弹出暗色主题的 Avalonia 窗口。

### 4. 运行命令行

```bash
dotnet run --project src/PyRebuilderSharp.Cli -c Release -- input.pyc -o output.py
```

参数说明：

| 参数 | 说明 |
|:-----|:-----|
| `input.pyc` | 要反编译的 .pyc 文件（必需） |
| `-o`, `--output <file>` | 输出文件（可选，缺省输出到 stdout） |

示例：

```bash
# 输出到终端
dotnet run --project src/PyRebuilderSharp.Cli -c Release -- example.pyc

# 保存到文件
dotnet run --project src/PyRebuilderSharp.Cli -c Release -- example.pyc -o restored.py

# 批量处理
for f in *.pyc; do
  dotnet run --project src/PyRebuilderSharp.Cli -c Release -- "$f" -o "${f%.pyc}_decomp.py"
done
```

---

## 运行测试

### 单元测试

```bash
dotnet test tests/PyRebuilderSharp.Tests -c Release
```

测试分类：

| 分类 | 内容 | 当前通过 |
|:-----|:-----|:--------:|
| Lv0_Expressions | 算术/比较/逻辑表达式 | ✅ 7/7 |
| Lv1_Sequential | 赋值/调用/返回 | ✅ 7/7 |
| Lv2_ControlFlow | if/for/while/try/with | ✅ 7/7 |
| Lv3_NestedDepth | 嵌套控制流混合 | ⏳ 0/7 |
| VersionMatrix | 跨版本反编译矩阵 | ⏳ 部分 |

### 基准测试（全部 .pyc 文件）

```bash
cd tools/QuickBenchmark
dotnet run -c Release -- ../../test_data/compiled
```

遍历 `test_data/compiled/` 下所有 .pyc 文件，输出每个文件的块数、失败数和耗时。

---

## 使用 GUI 进行反编译

### 基本操作

1. **启动 GUI**：`dotnet run --project src/PyRebuilderSharp.Gui -c Release`
2. **打开文件**：点击「📂 打开 .pyc」按钮，选择一个或多个 .pyc 文件
3. **拖放**：将 .pyc 文件从 Finder/资源管理器拖入窗口
4. **选择文件**：在左侧文件列表点击任意文件，自动反编译
5. **查看结果**：右侧编辑区显示带行号的源码
6. **保存**：点击「💾 保存」按钮，选择输出路径

### GUI 界面说明

```
┌─────────────────────────────────────────────────┐
│ 📂 打开 .pyc  💾 保存  │  🐍 3.12  │ ✅ 12块成功 │  ← 工具栏
├────────────┬────────────────────────────────────┤
│ 📄 .pyc 列表 │    反编译结果（带行号 + 语法高亮）    │
│             │                                    │
│ abc.3.12    │   1│ import sys                     │
│  8 KB 🐍3.12│   2│ import os                      │
│             │   3│                                │
│ test_for    │   4│ def test():                     │
│  2 KB 🐍3.10│   5│     for i in range(10):         │
│             │   6│         print(i)                │
│             │                                    │
├────────────┴────────────────────────────────────┤
│ ✅ 完成 — 3 个函数, 12 基本块, 5ms    [===]     │  ← 状态栏
└─────────────────────────────────────────────────┘
```

### 重要提示

- 反编译结果中的 **注释块**（`# ═══ [Block N Decompilation Failed] ═══`）表示该基本块反编译失败，已转为注释兜底。这是**正常行为**——其他块保持不变。
- 状态栏显示成功/失败统计。如果有失败块，请参考下方「报告异常」章节。

---

## 构建测试文件

### 从 .py 编译 .pyc

使用项目内置脚本：

```bash
# Python 3.12
python3 -c "
import py_compile, sys
for f in test_data/input/*.py:
    try:
        py_compile.compile(f, cfile=f.replace('input/', 'compiled/').replace('.py', '.3.12.pyc'))
    except py_compile.PyCompileError as e:
        print(f'Skip {f}: {e}')
"

# Python 3.11（需 pyenv 切换）
pyenv shell 3.11.15
python3 tools/compile_311.py
```

### 使用 compile_pyc_matrix.py

```bash
# 编译全部版本（需安装对应 pyenv Python 版本）
python3 tests/PyRebuilderSharp.Tests/TestData/scripts/compile_pyc_matrix.py
```

该脚本自动扫描本机安装的 Python 版本，编译全部 `test_data/input/*.py` 到 `test_data/compiled/*.{version}.pyc`。

---

## 如何报告异常

### 提供的信息

在 GitHub Issues 中提供以下内容（越多越容易定位）：

```markdown
**环境**:
- OS: macOS 14.5 / Windows 11 / Ubuntu 24.04
- .NET 版本: 10.0.x
- 构建配置: Release / Debug

**异常文件**:
- 文件名: abc.3.12.pyc
- Python 版本: 3.12
- 文件大小: 8839 bytes
- Magic: 0xC00D0D0A

**复现步骤**:
1. 打开 PyRebuilderSharp GUI
2. 拖入 abc.3.12.pyc
3. 观察状态栏或输出

**异常信息**:
（粘贴终端的错误输出或 GUI 状态栏的错误信息）

**原始 .pyc 文件**:
（或提供可复现的最小 .py 文件和对应 Python 版本）
```

### 使用调试工具

```bash
# 查看 .pyc 的指令序列和分块
dotnet run --project tools/DebugBlocks.csproj -- problem.pyc

# 运行基准测试（定位是否所有文件都失败还是仅个别）
cd tools/QuickBenchmark && dotnet run -c Release -- ../../test_data/compiled
```

### 异常发生时的自助排查

如果反编译结果中出现注释块（`# [Block N Decompilation Failed]`）：

1. **查看注释块内容**：注释块中包含偏移范围、错误类型和原始字节码
2. **确认 Python 版本**：3.11+/3.8-3.10/2.7 使用不同的操作码映射
3. **检查已知问题**：参见 docs/summary_Phase3_plus.md 的「已知问题」章节
4. **提供 .pyc 文件**：最小的可复现文件最有用

---

## 文档索引

| 文档 | 说明 |
|:-----|:------|
| [Python反编译总体设计.md](docs/Python反编译总体设计.md) | 架构设计、核心原则、与 pycdc 对比 |
| [Python反编译详细设计.md](docs/Python反编译详细设计.md) | 模块设计、数据模型、API 参考 |
| [summary_Phase3_plus.md](docs/summary_Phase3_plus.md) | Phase 3 收敛计划、异常收集、已知问题、新版本支持流程 |
| [README.md](README.md) | 项目概览与成就 |

---

## 安装依赖的参考命令

### macOS (Homebrew)

```bash
# 安装 .NET 10 SDK
brew install dotnet-sdk

# 验证
dotnet --version
```

### Ubuntu/Debian

```bash
# 添加 Microsoft 包源
wget https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt update
sudo apt install dotnet-sdk-10.0

# 验证
dotnet --version
```

### Windows

从 [dotnet.microsoft.com](https://dotnet.microsoft.com/download/dotnet/10.0) 下载 .NET 10 SDK 安装包，运行安装程序后重启终端。

---

> **开发建议**：开发时使用 `dotnet watch run --project src/PyRebuilderSharp.Gui` 实现热重载，修改代码后自动刷新 GUI。
