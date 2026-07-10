# Step 2 总结文档

> 日期: 2026-07-10
> Phase 8 实施方案第二步完成
> 研读来源: `python-uncompyle6` (uncompyle6), `python-decompile3` (decompyle3), `pycdc` (pycdc)

---

## 成果清单

```
Step 2 → ✅
├── 研读①: COME_FROM 构建算法 ────────────────── ✅
│   ├── 来源: uncompyle6/scanner37base.py (314~363, 594~665)
│   ├── docs/research/research01_come_from_uncompyle6.md
│   └── 产出: ShouldGenerateComeFrom() + ComeFromType 分类
│
├── 研读②: 嵌套 CodeObject 递归 ──────────────── ✅
│   ├── 来源: pycdc/ASTree.cpp (85~120, 1649~1675, 3723~3760)
│   ├── docs/research/research02_nested_codeobject_pycdc.md
│   └── 产出: DecompileNestedCodeObjects() 设计 + 循环引用保护
│
├── 研读③: ExceptionTable 异常边 ────────────── ✅
│   ├── 来源: pycdc/pyc_code.cpp (148~171), pycdc/ASTree.cpp (2075~2092)
│   ├── docs/research/research03_exception_table_pycdc.md
│   └── 产出: ET→CFG 异常边严格映射 + 3.11+ 领先优势确认
│
├── 研读④: LIST_APPEND / 推导式 ─────────────── ✅
│   ├── 来源: uncompyle6/parsers/parse37.py, parse27.py
│   ├── docs/research/research04_list_append_uncompyle6.md
│   └── 产出: IsInComprehensionContext() + for-else 歧义解决
│
└── 研读⑤: Decorator 检测 ───────────────────── ✅
    ├── 来源: pycdc/ASTree.cpp (439~537 CALL_FUNCTION, 1649~1675 MAKE_FUNCTION)
    ├── docs/research/research05_decorator_pycdc.md
    └── 产出: TryExtractDecoratedFunction() + 多层装饰器递归
```

## 产出文件

| 文件 | 说明 |
|------|------|
| `docs/research/research01_come_from_uncompyle6.md` | COME_FROM 两步算法 + 跳转分类规则 |
| `docs/research/research02_nested_codeobject_pycdc.md` | pycdc 单一入口递归 + 循环引用检测 |
| `docs/research/research03_exception_table_pycdc.md` | ET 格式解析 + 块栈 vs 标注对比 |
| `docs/research/research04_list_append_uncompyle6.md` | 推导式语法规则 + BARE_EXPR 清理规则 |
| `docs/research/research05_decorator_pycdc.md` | CALL_FUNCTION decorator 检测 + FoldDecoratorCalls 算法 |

## 关键发现汇总

| # | 发现 | 来源 | 影响 |
|---|------|------|------|
| 1 | COME_FROM 是标注而非伪指令（全名分类由 SETUP_* 指令决定） | uncompyle6 | Step 4 ComeFromType 应继承此分类 |
| 2 | pycdc 不递归反编译嵌套 CodeObject（在代码生成阶段惰性处理） | pycdc | Step 5 的递归在 AST 构建阶段做，不同 |
| 3 | 3.11+ ExceptionTable 处理是 PyRebuilderSharp 的领先优势 | pycdc+对比 | Step 5: 只需微调 ET 映射 |
| 4 | LIST_APPEND 是语法结构而非独立指令 | uncompyle6 | Step 3: 安全的 B1/B2 删除规则 |
| 5 | Decorator 在 CALL_FUNCTION 时由栈上 NODE_FUNCTION 类型判定 | pycdc | Step 3: FoldDecoratorCalls 的后处理设计 |
| 6 | PyRebuilderSharp 的标注+模式目录结构优于 pycdc 的块栈 | 对比 | 保留现有架构，补充验证层 |
| 7 | pycdc 和 uncompyle6 都不支持 3.11+ ExceptionTable 正确反编译 | 多个源 | PyRebuilderSharp 在高版领域无直接竞争 |

## 错误发现汇总

| # | 研读中的假设 | ✅❌ | 实际 |
|---|------------|:---:|------|
| 1 | COME_FROM 在 scanner.py 中 | ❌ | 在 `scanner37base.py` 中，scanner.py 只是版本分发器 |
| 2 | pycdc 在 MAKE_FUNCTION 处递归 | ❌ | 发生在 CALL_FUNCTION 时 |
| 3 | uncompyle6 有独立的 try 语义处理 | ❌ | 都在语法规则中，语义层只是 default() |
| 4 | pycdc CALL_FUNCTION 通用逻辑 | ❌ | 内部包含 LOAD_BUILD_CLASS 的特殊处理 |

## 服务映射

```
研读成果 → Step 3 (BARE_EXPR)
├── research04 (LIST_APPEND) → B1/B2/B3 删除规则
└── research05 (decorator)   → FoldDecoratorCalls 算法

研读成果 → Step 4 (后支配树)
└── research01 (COME_FROM)   → ShouldGenerateComeFrom + ComeFromType

研读成果 → Step 5 (COME_FROM修复 + CodeObj + ET)
├── research02 (nested code) → DecompileNestedCodeObjects
└── research03 (ET)          → ET→CFG 严格映射
```
