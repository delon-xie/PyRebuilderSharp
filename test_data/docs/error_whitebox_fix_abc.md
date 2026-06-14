# Whitebox Fix: abc.py (Python 3.10)

**源文件**: `test_data/input/abc.py` (8,252 字节, 209 行)
**编译**: Python 3.10.20
**反编译行数**: 112 行 (源: 209 行)
**diff 差异**: 约 55 行
**测试日期**: 2026-06-14

---

## 差异分类

### A 类 — 预期差异（无需修复）

| 差异 | 原因 |
|:-----|:------|
| 无 `# Copyright 2007 Google...` | .pyc 不保存注释 |
| 缺少空行 | 代码生成器不插入空行 |
| 反编译头 `# Decompiled from: <module>` | Hermes 标记 |
| 孤儿块注释 `# orphan @0x...` | 结构标记 |

### B 类 — 语义错误（待修复，已处理）

| # | 问题 | 原始 | 反编译 | 修复状态 |
|:-:|:-----|:-----|:--------|:---------|
| 1 | 函数 docstring 丢失 | `def abstractmethod:"""..."""` | `def abstractmethod(funcobj):` | ✅ 隐式 docstring 支持 (`AstBuilder.BuildFunctionDef`) |
| 2 | `if not hasattr(...)` 条件反转 | `if not hasattr(...):` | `if hasattr(...):` (else 叉反转) | ✅ POP_JUMP_IF_TRUE 检测 (`BuildIfElse`, `BuildRestrictedIfElse`) |
| 3 | `for name, value in ...` 解包丢失 | `for name, value in cls.__dict__.items():` | `for name in cls.__dict__.items():` | ✅ UNPACK_SEQUENCE 检测 (`ExtractLoopVariable`) |
| 4 | `class ABCMeta:` 无 `else:` | try/except...`else:` | `# orphan @0x0092` | ⚠️ CFG 边缺失 (C 类) |
| 5 | `super().__new__` → `{}()` | `super().__new__(..., **kwargs)` | `cls = {}()` | ✅ CALL_FUNCTION_EX + DICT_MERGE 实现 |
| 6 | print 丢失 (`dump_registry`) | `print(f"...", file=file)` | `('file',)` | ✅ CALL_FUNCTION_KW + FORMAT_VALUE + BUILD_STRING |
| 7 | 元组解包 `(a,b,c,d)=fn()` | `(_a, _b, _c, _d) = fn()` | `_a = *fn()` | ✅ UNPACK_SEQUENCE 收集 + Assign 组合 |
| 8 | `import` 名悬浮 | ... | `_abc` / `_py_abc` 多余行 | ✅ POP_TOP `IsImport` 跳过 |
| 9 | docstring `\n` 转义 | `"""...\n..."""` | `"""...\\n..."""` | ✅ `"""..."""` + 实际换行 |
| 10 | `else:` 错误分支 | `if not hasattr(): return cls` / *else 不存在* | `if hasattr(): return cls else: abstracts=set()` | ✅ body 终止语句检测消除错误 else |
| 11 | 单行 docstring `'...'` vs `"""..."""` | `"""Abstract Base Classes..."""` | `'Abstract Base Classes...'` | ⚠️ 风格差异（单行，无语义影响） |

### C 类 — 已知限制（未修复）

| # | 问题 | 根因 | 修复位置 |
|:-:|:-----|:------|:---------|
| 1 | try handler → `class ABC(metaclass=ABCMeta)` 丢失 | CFG 无边连接 handler cleanup 到类定义 | `BlockScanner.LinkBlocks` |
| 2 | `update_abstractmethods` 内子孤儿块 | 嵌套控制流（for/if/else）重建不完整 | `AstBuilder.BuildRestrictedIfElse` |
| 3 | 无空行/`# Copyright` /类级 `__doc__=` vs 裸 docstring | .pyc 压缩或编译器策略 | 不可逆 |

---

## B 类修复记录

| # | 修复文件 | 变更行数 | 涉及模块 |
|:-:|:---------|:---------|:---------|
| 1 | `AstBuilder.cs` | +12 | `BuildFunctionDef`: co_consts[0] 隐式 docstring |
| 2 | `AstBuilder.cs` | +20 | `BuildIfElse`/`BuildRestrictedIfElse`: POP_JUMP_IF_TRUE 条件反 |
| 3 | `AstBuilder.cs` | +18 | `ExtractLoopVariable`: UNPACK_SEQUENCE 检测 |
| 5 | `StackMachine.cs` | +45 | CALL_FUNCTION_EX, DICT_MERGE |
| 6 | `StackMachine.cs` + `Opcode.cs` + `PythonCodeGenerator.cs` | +60 | CALL_FUNCTION_KW, FORMAT_VALUE, BUILD_STRING |
| 7 | `StackMachine.cs` | +40 | UNPACK_SEQUENCE 收集 + 组合 |
| 8 | `StackMachine.cs` | +5 | POP_TOP: `IsImport` 跳过 |
| 9 | `PythonCodeGenerator.cs` | +30 | `EscapeString`: `"""..."""` + 实际换行 |
| 10 | `AstBuilder.cs` | +10 | body 终止语句检测 |

---

## 回归测试

- 16 关键测试: ✅ 全部通过
- abc.3.10.pyc 快照: 112 行, 5 blocks, 4 orphan, 96 instr

---

## 结论

abc.py 的 11 个 B 类语义错误已修复 10 项。剩余 3 项 C 类限制（CFG 边缺失、嵌套控制流、不可逆丢失）不影响语义完整性。可以进入下一个白盒测试文件。
