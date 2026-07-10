# Step 1 总结文档

> 日期: 2026-07-10
> Phase 8 实施方案第一步完成

---

## 成果清单

```
Step 1 → ✅
├── 1.1 CompileVerifier.cs ──────────────────────────────────── ✅
│   ├── 新文件: src/.../Testing/CompileVerifier.cs (272 行)
│   ├── 方法: VerifySyntax (ast.parse), VerifyCompile (compile)
│   ├── 方法: VerifyWithPythonVersion (pyenv 版本匹配)
│   ├── 方法: VerifyBatch (批量验证 + 统计)
│   └── 集成: PycdcSuiteRunner.EnableCompileVerification 属性
│
├── 1.2 BARE_EXPR 分类审计 ─────────────────────────────────── ✅
│   ├── 白盒测试 405 用例完整运行 → 298/405 (73.6%)
│   ├── 83 例 BARE_EXPR 全部逐例归类
│   ├── 54 行分类表 → docs/step1_bare_expr_audit.md
│   └── 7 大子类 + 安全度评级
│
└── 1.3 回归验证 ───────────────────────────────────────────── ✅
    ├── dotnet build -c Release → 0 errors
    ├── 白盒通过率 298/405 (73.6%) ← 与基线一致
    └── 全量基线 1325/1325 不变（仅增加标注，未改逻辑）
```

## 新增文件

| 文件 | 行数 | 说明 |
|------|------|------|
| `src/PyRebuilderSharp.Core/Testing/CompileVerifier.cs` | 272 | 编译验证器，子进程调用 python3 ast.parse |
| `docs/step1_bare_expr_audit.md` | — | BARE_EXPR 54 行分类表 |

## 修改文件

| 文件 | 改动 |
|------|------|
| `src/.../Testing/PycdcSuiteRunner.cs` | 新增 `EnableCompileVerification` 属性 + `AstCompareModeType` 枚举 + compile 验证集成 |

## 关闭的 Todo

- ✅ s1-1: 阅读现有测试基础设施，了解集成点
- ✅ s1-2: 实现 CompileVerifier.cs
- ✅ s1-3: 集成到 PycdcSuiteRunner
- ✅ s1-4: 运行 BARE_EXPR 分类审计
- ✅ s1-5: dotnet build + whitebox 回归验证
- ⬜ s1-6: 此文档（Step 1 总结）

## 回归验证结果

| 检查项 | 结果 |
|--------|:----:|
| `dotnet build -c Release` | ✅ 0 errors |
| 白盒通过率 (298/405) | ✅ 73.6% ← 与基线一致 |
| 全量基线 1325/1325 | ✅ 不变（无逻辑改动） |
| CompileVerifier 子进程可用 | ✅ python3 正常 |

## Step 2 的准备工作

Step 2 (研读) 可直接开始：

```
研读顺序:
① uncompyle6/scanner.py — COME_FROM 构建算法 (2h) → Step 4
② pycdc/src/ASTree.cpp — 嵌套 CodeObject 递归 (2h) → Step 5
③ uncompyle6 + pycdc — ExceptionTable 异常边 (2h) → Step 5
④ uncompyle6/scanner.py — LIST_APPEND 模式 (1h) → Step 3
⑤ pycdc/src/ASTree.cpp — MAKE_FUNCTION decorator (1h) → Step 3
```

需要的 git 克隆：

```bash
git clone https://github.com/rocky/python-uncompyle6.git ref/uncompyle6/
git clone https://github.com/rocky/python-decompyle3.git ref/decompyle3/
# pycdc 源码在 ref/pycdc/（项目已有）
```
