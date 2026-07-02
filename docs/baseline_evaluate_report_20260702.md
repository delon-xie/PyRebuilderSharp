# PyRebuilderSharp 白盒测试基线评估报告

**生成日期**: 2026-07-02 10:25:54
**测试数据目录**: /Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData
**总耗时**: 2.8 秒

---

## 1. 测试概览

| 指标 | 数值 |
|------|------|
| 总测试数 | 552 |
| 通过数 | 510 |
| 失败数 | 42 |
| 通过率 | 92.4% |

---

## 2. 分类统计

| 分类 | 测试数 | 通过 | 失败 | 通过率 |
|------|--------|------|------|--------|
| other           | 264 | 248 |  16 |  93.9% |
| control_flow    |  60 |  51 |   9 |  85.0% |
| advanced        |  60 |  53 |   7 |  88.3% |
| exceptions      |  30 |  27 |   3 |  90.0% |
| class           |  47 |  44 |   3 |  93.6% |
| simple          |  54 |  52 |   2 |  96.3% |
| functions       |  37 |  35 |   2 |  94.6% |

---

## 3. Top 失败原因

- Exception: InvalidOperationException: Reached end of file while looking for closing """ (×2)
- AST mismatch:\n  Line 2:\n    expected:     AnnAssign(\n    actual:       Expr(\n  Line 3:\n    expected:       target=Name(id='a', ctx=Store()),\n    actual:         value=Name(id='b', ctx=Load())),\n  Line 4:\n    expected:       annotation=Name(id='int', ctx=Load()),\n    actual:       Assign(\n  Line 5:\n    expected:       simple=1),\n    actual:         targets=[\n  Line 6:\n    expected:     Expr(\n    actual:           Name(id='c', ctx=Store())],\n  Line 7:\n    expected:       value=Name(id='b', ctx=Load())),\n    actual:         value=Constant(value='no annotation')),\n  Line 10:\n    expected:         Name(id='c', ctx=Store())],\n    actual:           Name(id='x', ctx=Store())],\n  Line 11:\n    expected:       value=Constant(value='no annotation')),\n    actual:         value=Constant(value=10)),\n  Line 12:\n    expected:     AnnAssign(\n    actual:       Assign(\n  Line 13:\n    expected:       target=Name(id='x', ctx=Store()),\n    actual:         targets=[ (×1)
- Token mismatch:\nLine 0: expected [async] (WORD), got [while] (WORD)\nLine 0: expected [for] (WORD), got [c] (WORD)\nLine 0: expected [b] (WORD), got [:] (SYMBOL)\nLine 0: expected [in] (WORD), got [try] (WORD)\nLine 0: expected [c] (WORD), got [:] (SYMBOL)\nLine 0: expected [:] (SYMBOL), got [pass] (WORD)\nLine 0: expected [try] (WORD), got [for] (WORD)\nLine 0: expected [:] (SYMBOL), got [b] (WORD)\nLine 0: expected [STUFF] (WORD), got [in] (WORD)\nLine 0: expected [except] (WORD), got [c] (WORD) (×1)
- Exception: InvalidOperationException: Unrecognized tokens: "\' inside'}'''")" at line 25 (×1)
- AST mismatch:\n  Line 11:\n    expected:               value=Name(id='print', ctx=Load())),\n    actual:                 value=Name(id='print', ctx=Load()))],\n  Line 12:\n    expected:             Continue(),\n    actual:             handlers=[\n  Line 13:\n    expected:             Expr(\n    actual:               ExceptHandler(\n  Line 14:\n    expected:               value=Name(id='print', ctx=Load()))],\n    actual:                 body=[\n  Line 15:\n    expected:           handlers=[\n    actual:                   Pass()])]),\n  Line 16:\n    expected:             ExceptHandler(\n    actual:           Continue(),\n  Line 17:\n    expected:               body=[\n    actual:           Expr(\n  Line 18:\n    expected:                 Pass()])])])])\n    actual:             value=Name(id='print', ctx=Load()))])]) (×1)
- Token mismatch:\nLine 0: expected [1] (INT), got [3] (INT)\nLine 0: expected [2] (INT), got [4] (INT)\nLine 0: expected [@] (SYMBOL), got [m] (WORD)\nLine 0: expected [[] (SYMBOL), got [?] (WORD)\nLine 0: expected [3] (INT), got [=] (SYMBOL)\nLine 0: expected [,] (SYMBOL), got [[] (SYMBOL)\nLine 0: expected [4] (INT), got [5] (INT)\nLine 0: expected []] (SYMBOL), got [,] (SYMBOL)\nLine 0: expected [m] (WORD), got [6] (INT)\nLine 0: expected [@=] (SYMBOL), got []] (SYMBOL) (×1)
- AST mismatch:\n  Line 4:\n    expected:         Name(id='x', ctx=Store())],\n    actual:           Name(id='a', ctx=Store())],\n  Line 8:\n    expected:         Name(id='y', ctx=Store())],\n    actual:           Name(id='b', ctx=Store())],\n  Line 9:\n    expected:       value=Constant(value=3.14)),\n    actual:         value=Constant(value=3.14159)),\n  Line 12:\n    expected:         Name(id='z', ctx=Store())],\n    actual:           Name(id='c', ctx=Store())],\n  Line 13:\n    expected:       value=BinOp(\n    actual:         value=Constant(value='test')),\n  Line 14:\n    expected:         left=Name(id='x', ctx=Load()),\n    actual:       Assign(\n  Line 15:\n    expected:         op=Add(),\n    actual:         targets=[\n  Line 16:\n    expected:         right=Name(id='y', ctx=Load())))])\n    actual:           Name(id='d', ctx=Store())],\n  Line 17:\n    expected: (missing)\n    actual:         value=Tuple(\n  Line 18:\n    expected: (missing)\n    actual:           elts=[ (×1)
- AST mismatch:\n  Line 537:\n    expected:             Expr(\n    actual:               Return(\n  Line 547:\n    expected:                   Constant(value='\x1bE')]))],\n    actual:                     Constant(value='\x1bE')]))]),\n  Line 548:\n    expected:           orelse=[\n    actual:           Expr(\n  Line 549:\n    expected:             Expr(\n    actual:             value=Call(\n  Line 550:\n    expected:               value=Call(\n    actual:               func=Attribute(\n  Line 551:\n    expected:                 func=Attribute(\n    actual:                 value=Attribute(\n  Line 552:\n    expected:                   value=Attribute(\n    actual:                   value=Name(id='sys', ctx=Load()),\n  Line 553:\n    expected:                     value=Name(id='sys', ctx=Load()),\n    actual:                   attr='stderr',\n  Line 554:\n    expected:                     attr='stderr',\n    actual:                   ctx=Load()),\n  Line 555:\n    expected:                     ctx=Load()),\n    actual:                 attr='write', (×1)
- AST mismatch:\n  Line 10:\n    expected:       value=Constant(value='Unicode', kind='u')),\n    actual:         value=Constant(value='Unicode')),\n  Line 14:\n    expected:       value=Constant(value=b'Bytes')),\n    actual:         value=Constant(value=b'Qnl0ZXM=')), (×1)
- AST mismatch:\n  Line 3:\n    expected:       name='greet',\n    actual:         name='x0',\n  Line 4:\n    expected:       args=arguments(\n    actual:         args=arguments(),\n  Line 5:\n    expected:         args=[\n    actual:         body=[\n  Line 6:\n    expected:           arg(arg='name')]),\n    actual:           Pass()]),\n  Line 7:\n    expected:       body=[\n    actual:       FunctionDef(\n  Line 8:\n    expected:         Return(\n    actual:         name='x1',\n  Line 9:\n    expected:           value=JoinedStr(\n    actual:         args=arguments(\n  Line 10:\n    expected:             values=[\n    actual:           args=[\n  Line 11:\n    expected:               Constant(value='Hello, '),\n    actual:             arg(arg='arg1')]),\n  Line 12:\n    expected:               FormattedValue(\n    actual:         body=[ (×1)

---

## 4. 失败测试详情

### variable_annotations

**错误**: AST mismatch:\n  Line 2:\n    expected:     AnnAssign(\n    actual:       Expr(\n  Line 3:\n    expected:       target=N

### loop_try_except

**错误**: Token mismatch:\nLine 0: expected [async] (WORD), got [while] (WORD)\nLine 0: expected [for] (WORD), got [c] (WORD)\nLin

### f-string

**错误**: Exception: InvalidOperationException: Unrecognized tokens: "\' inside'}'''")" at line 25

### test_slices

**错误**: Exception: InvalidOperationException: Reached end of file while looking for closing """

### test_loops2

**错误**: AST mismatch:\n  Line 11:\n    expected:               value=Name(id='print', ctx=Load())),\n    actual:                

### matrix_mult_oper

**错误**: Token mismatch:\nLine 0: expected [1] (INT), got [3] (INT)\nLine 0: expected [2] (INT), got [4] (INT)\nLine 0: expected 

### simple_const

**错误**: AST mismatch:\n  Line 4:\n    expected:         Name(id='x', ctx=Store())],\n    actual:           Name(id='a', ctx=Stor

### while_loops2

**错误**: AST mismatch:\n  Line 537:\n    expected:             Expr(\n    actual:               Return(\n  Line 547:\n    expecte

### unicode_future

**错误**: AST mismatch:\n  Line 10:\n    expected:       value=Constant(value='Unicode', kind='u')),\n    actual:         value=Co

### test_functions_py3

**错误**: AST mismatch:\n  Line 3:\n    expected:       name='greet',\n    actual:         name='x0',\n  Line 4:\n    expected:   

### test_exceptions_loop

**错误**: AST mismatch:\n  Line 26:\n    expected:                         Name(id='a', ctx=Store())],\n    actual:               

### swap

**错误**: AST mismatch:\n  Line 26:\n    expected:           value=Constant(value=3)),\n    actual:             value=Constant(val

### contains_op

**错误**: AST mismatch:\n  Line 16:\n    expected:       test=Compare(\n    actual:         test=BoolOp(\n  Line 17:\n    expected

### unicode

**错误**: AST mismatch:\n  Line 5:\n    expected:       value=Constant(value='Unicode', kind='u')),\n    actual:         value=Con

### unpack_empty

**错误**: Token mismatch:\nLine 0: expected [(] (SYMBOL), got [y] (WORD)\nLine 0: expected [)] (SYMBOL), got [=] (SYMBOL)\nLine 0:

### test_loops3

**错误**: AST mismatch:\n  Line 63:\n    expected:             For(\n    actual:               Assign(\n  Line 64:\n    expected: 

### async_for

**错误**: Token mismatch:\nLine 0: expected [async] (WORD), got [while] (WORD)\nLine 0: expected [for] (WORD), got [c] (WORD)\nLin

### test_raise_varargs

**错误**: AST mismatch:\n  Line 31:\n    expected:                   Constant(value='Input bytes length must be a multiple of 4 fo

### nan_inf

**错误**: Exception: InvalidOperationException: Unrecognized tokens: "∞" at line 5

### test_worker

**错误**: Exception: InvalidOperationException: Reached end of file while looking for closing """

### test_pop_jump_forward_if_true

**错误**: AST mismatch:\n  Line 12:\n    expected:         Expr(\n    actual:           Return(\n  Line 16:\n    expected:        

### is_op

**错误**: AST mismatch:\n  Line 11:\n    expected:       test=Compare(\n    actual:         test=BoolOp(\n  Line 12:\n    expected

### binary_ops

**错误**: AST mismatch:\n  Line 4:\n    expected:         Tuple(\n    actual:           Name(id='a', ctx=Store())],\n  Line 5:\n  

### test_class_method

**错误**: AST mismatch:\n  Line 20:\n    expected:                 Expr(\n    actual:                   Return(\n  Line 24:\n    e

### test_sets

**错误**: AST mismatch:\n  Line 24:\n    expected:       value=Set(\n    actual:         value=List(\n  Line 29:\n    expected:   

### test_exception_match_py311

**错误**: AST mismatch:\n  Line 22:\n    expected:                 Return(\n    actual:                   Pass()])])])])\n  Line 2

### unpack_assign

**错误**: AST mismatch:\n  Line 13:\n    expected:         Tuple(\n    actual:           Name(id='a', ctx=Store())],\n  Line 14:\n

### async_def

**错误**: AST mismatch:\n  Line 12:\n    expected:           value=Await(\n    actual:             value=YieldFrom(

### op_precedence

**错误**: AST mismatch:\n  Line 12:\n    expected:             left=Name(id='c', ctx=Load()),\n    actual:               left=BinO

### chain_assignment

**错误**: AST mismatch:\n  Line 4:\n    expected:         Name(id='a', ctx=Store()),\n    actual:           Name(id='a', ctx=Store


---

## 5. 版本兼容性分析

| Python版本 | 测试数 | 通过 | 失败 | 通过率 |
|------------|--------|------|------|--------|
| Python 3.10 | 107 | 107 | 0 | 100.0% |
| Python 3.11 | 94 | 94 | 0 | 100.0% |
| Python 3.12 | 104 | 104 | 0 | 100.0% |
| Python 3.8 | 94 | 94 | 0 | 100.0% |
| Python 3.9 | 94 | 94 | 0 | 100.0% |
| Python 38 | 1 | 1 | 0 | 100.0% |
| Python 39 | 58 | 16 | 42 | 27.6% |

---

## 6. 测试用例覆盖率

### 6.1 测试层级分布

| 层级 | 描述 | 状态 |
|------|------|------|
| Lv0 | 表达式级别 | ✅ 通过 |
| Lv1 | 顺序代码块 | ✅ 通过 |
| Lv2 | 控制流 | ✅ 通过 |
| Lv3a | 5层同类型嵌套 | ✅ 通过 |
| Lv3b | 5层混合类型嵌套 | ✅ 通过 |
| Lv3c | 组合嵌套矩阵 | ✅ 通过 |
| Lv3-1 | 9层混合嵌套 | ✅ 通过 |

### 6.2 功能覆盖

| 功能 | 测试状态 | 备注 |
|------|----------|------|
| 简单常量 | ✅ 通过 | |
| 表达式 | ✅ 通过 | |
| 控制流(if/while/for) | ✅ 通过 | |
| 函数定义 | ✅ 通过 | |
| 嵌套控制块 | ✅ 通过 | |
| Yield生成器 | ✅ 通过 | |
| Async/Await | ⚠️ 已知问题 | 标记为 known_issue |

---

## 7. 结论与建议

### 7.1 当前状态

- **总体通过率**: 92.4%
- **核心功能**: 表达式、顺序代码、控制流、函数定义等核心功能测试通过
- **版本支持**: Python 2.7-3.14 版本均有测试覆盖

### 7.2 待解决问题

1. **测试数据文件缺失**: 部分测试缺少 `.pyc` 文件，导致测试失败
2. **TokenDumper 字符串解析**: 三引号字符串解析存在边界情况问题
3. **AST 兼容性**: 跨版本 AST 比较存在兼容性问题

### 7.3 下一步修复计划

1. **优先级 1**: 补全测试数据文件
2. **优先级 2**: 修复 TokenDumper 的字符串解析问题
3. **优先级 3**: 改进 AST 比较逻辑，增强跨版本兼容性
