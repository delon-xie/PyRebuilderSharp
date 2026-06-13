# 代码查看器设计文档

**版本**: v2.0
**日期**: 2026-06-14
**状态**: Phase 1 ✅ · Phase 2 ⏸️ · Phase 3 📋

## 概述

PyRebuilderSharp 的代码查看器采用**分阶段迭代**策略，逐步实现从基础显示到高级联动的完整功能。

---

## Phase 1 — 基础显示（已完成 ✅）

### 目标
左侧文件树 + 右侧 split 双栏（dis | py），VS Code Dark+ 语法高亮。

### 实现

| 功能 | 方案 |
|:-----|:------|
| 代码显示 | `SelectableTextBlock` + `Inlines` |
| 语法高亮 | `PythonSyntaxHighlight`（纯 Inline，0 第三方） |
| 反汇编 | `DisassemblyGenerator`（自研，不依赖 python3 -m dis） |
| 文件树 | `TreeView` + `FileTreeNode` 模型 |
| 拖放 | 支持 .pyc 文件和文件夹递归遍历 |
| 主题 | VS Code Dark+ 配色（`#1e1e1e` / `#252526` / `#323233`） |

---

## Phase 2 — 锁定滚动同步（📋 后续）

### 布局

```
┌─────────── 260px ──────────┬──── 4 ────┬────────── * ───────────┐
│ 📂 字节码文件               │          │                         │
│ ┌────────────────────────┐ │  分割线   │ ┌──────────┬──────────┐ │
│ │ 📁 test_data/          │ │          │ │ 🔍dis    │ 🔍source │ │
│ │  ├─ 📄 abc.3.12.pyc   │ │          │ │ ┌───────┐│ ┌───────┐│ │
│ │  ├─ 📄 test_for.pyc   │ │          │ │ │LOAD   ││ │import ││ │
│ │  └─ 📄 my_module.pyc   │ │          │ │ │CALL   ││ │def .. ││ │
│ │                        │ │          │ │ │...    ││ │...    ││ │
│ │                        │ │          │ │ └───────┘│ └───────┘│ │
│ │                        │ │          │ └──────────┴──────────┘ │
│ └────────────────────────┘ │          │                         │
└────────────────────────────┴──────────┴─────────────────────────┘
```

### 技术方案

| 组件 | 实现 |
|:-----|:------|
| 左侧文件树 | Avalonia `TreeView` + 自定义 `TreeViewItem` 模板 |
| 右栏 dis 编辑器 | `AvaloniaEdit.TextEditor`，纯文本，等宽字体 |
| 右栏 py 编辑器 | `AvaloniaEdit.TextEditor`，Python 语法高亮（TextMate） |
| 反编译触发 | 点击文件树中的 .pyc 节点，或点击「▶ 反编译」按钮 |
| dis 生成 | 调用 `python3 -m dis <pyc>` 进程 |
| 语法高亮 | `AvaloniaEdit.TextMate` + `TextMateSharp.Grammars` ThemeName.DarkPlus |

### 文件树数据模型

```csharp
public class FileTreeNode
{
    public string Name { get; set; }
    public string? FullPath { get; set; }    // null = 目录节点
    public bool IsDirectory { get; set; }
    public ObservableCollection<FileTreeNode> Children { get; set; }
}
```

### ViewModel 接口

```csharp
// 当前选中文件
FileTreeNode? SelectedNode { get; set; }

// 展开的文件树根节点列表
ObservableCollection<FileTreeNode> FileTree { get; }

// 添加文件到树中（自动按路径分目录）
void AddToFileTree(string filePath);
```

### 验收标准

1. ✅ 打开 .pyc 后左侧出现文件树
2. ✅ 相同目录的文件自动归入同一文件夹节点
3. ✅ 点击文件节点 → 右侧显示 dis + py
4. ✅ dis 和 py 代码正常渲染，非空白
5. ✅ 语法高亮生效（至少右侧 Python 有颜色）

---

## Phase 2 — 锁定滚动（后续）

### 目标
双栏滚动同步，一个滚动时另一侧按比例同步。

### 技术方案

```csharp
// 使用 DispatcherTimer 轮询 VerticalOffset（80ms 间隔）
// 等比映射：ratio = source.Offset / (source.Extent - source.Viewport)
// target.ScrollToVerticalOffset(ratio * (target.Extent - target.Viewport))
```

### 注意事项
- 需要处理递归同步（A→B 时 B 触发事件→A，用 _isSyncing 标志防循环）
- 行数差异大时等比映射会有视觉偏差，但功能可用

---

## Phase 3 — 行号映射（后续）

### 目标
将 dis 输出的行号与源码行号建立映射，实现精确同步。

### 技术方案

```csharp
// 从 dis 输出中解析源码行号前缀
// dis 格式： "  行号    偏移量  指令..."
var match = Regex.Match(line.Trim(), @"^(\d+)");
int srcLine = int.Parse(match.Groups[1].Value);
// 建立 BytecodeLine → SourceLine 映射表
```

---

## NuGet 包依赖

```xml
<!-- 已安装 -->
Avalonia.AvaloniaEdit 12.0.0     — 代码编辑器
AvaloniaEdit.TextMate 12.0.0     — TextMate 语法高亮
TextMateSharp.Grammars           — TextMate 语法定义
```

---

## 历史

| 版本 | 日期 | 说明 |
|:-----|:------|:------|
| v1.0 | 2026-06-13 | 初始设计（含锁定滚动） |
| v2.0 | 2026-06-13 | 分阶段迭代计划（Phase 1 基础显示） |
