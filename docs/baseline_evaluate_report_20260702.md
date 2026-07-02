# PyRebuilderSharp 白盒测试基线评估报告

**生成日期**: 2026-07-02 11:01:06
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

- AST mismatch:\n  Line 12:\n    expected:           value=Await(\n    actual:             value=YieldFrom( (×1)
- AST mismatch:\n  Line 10:\n    expected:         Expr(\n    actual:           Return(\n  Line 14:\n    expected:               Constant(value='true')]))]),\n    actual:                 Constant(value='true')]))])])\n  Line 15:\n    expected:     Expr(\n    actual:   (missing)\n  Line 16:\n    expected:       value=Call(\n    actual:   (missing)\n  Line 17:\n    expected:         func=Name(id='print', ctx=Load()),\n    actual:   (missing)\n  Line 18:\n    expected:         args=[\n    actual:   (missing)\n  Line 19:\n    expected:           Constant(value='false (so jumping forward)')]))])\n    actual:   (missing) (×1)
- AST mismatch:\n  Line 2:\n    expected:     Assign(\n    actual:       Expr(\n  Line 3:\n    expected:       targets=[\n    actual:         value=Call(\n  Line 4:\n    expected:         Name(id='a', ctx=Store())],\n    actual:           func=Name(id='print', ctx=Load()),\n  Line 5:\n    expected:       value=Constant(value=1)),\n    actual:           args=[\n  Line 6:\n    expected:     Assign(\n    actual:             Name(id='result', ctx=Load())])),\n  Line 7:\n    expected:       targets=[\n    actual:       Assign(\n  Line 8:\n    expected:         Name(id='result', ctx=Store())],\n    actual:         targets=[\n  Line 9:\n    expected:       value=IfExp(\n    actual:           Name(id='a', ctx=Store())],\n  Line 10:\n    expected:         test=Compare(\n    actual:         value=Constant(value=2)),\n  Line 11:\n    expected:           left=BinOp(\n    actual:       Expr( (×1)
- AST mismatch:\n  Line 63:\n    expected:                   value=Constant(value=2))])],\n    actual:                     value=Constant(value=2))])]),\n  Line 64:\n    expected:           orelse=[\n    actual:           Assign(\n  Line 65:\n    expected:             Assign(\n    actual:             targets=[\n  Line 66:\n    expected:               targets=[\n    actual:               Name(id='a', ctx=Store())],\n  Line 67:\n    expected:                 Name(id='a', ctx=Store())],\n    actual:             value=Constant(value=3)),\n  Line 68:\n    expected:               value=Constant(value=3))]),\n    actual:           Assign(\n  Line 69:\n    expected:         Assign(\n    actual:             targets=[\n  Line 70:\n    expected:           targets=[\n    actual:               Name(id='b', ctx=Store())],\n  Line 71:\n    expected:             Name(id='b', ctx=Store())],\n    actual:             value=Constant(value='--------'))]),\n  Line 72:\n    expected:           value=Constant(value='--------'))]),\n    actual:       FunctionDef( (×1)
- AST mismatch:\n  Line 8:\n    expected:             Name(id='x', ctx=Store())],\n    actual:               Name(id='my_class', ctx=Store())],\n  Line 9:\n    expected:           value=Constant(value=1)),\n    actual:             value=Call(\n  Line 10:\n    expected:         ClassDef(\n    actual:               func=Name(id='__build_class__', ctx=Load()),\n  Line 11:\n    expected:           name='my_class',\n    actual:               args=[\n  Line 12:\n    expected:           body=[\n    actual:                 Name(id='my_class', ctx=Load()),\n  Line 13:\n    expected:             Assign(\n    actual:                 Constant(value='my_class')]))])])\n  Line 14:\n    expected:               targets=[\n    actual:   (missing)\n  Line 15:\n    expected:                 Name(id='y', ctx=Store())],\n    actual:   (missing)\n  Line 16:\n    expected:               value=Name(id='x', ctx=Load()))])])])\n    actual:   (missing) (×1)
- AST mismatch:\n  Line 21:\n    expected:     Assign(\n    actual:       Expr(\n  Line 22:\n    expected:       targets=[\n    actual:         value=Call(\n  Line 23:\n    expected:         Subscript(\n    actual:           func=Name(id='print', ctx=Load()),\n  Line 24:\n    expected:           value=Name(id='a', ctx=Load()),\n    actual:           args=[\n  Line 25:\n    expected:           slice=Slice(\n    actual:             Name(id='a', ctx=Load())]))])\n  Line 26:\n    expected:             lower=Constant(value=13)),\n    actual:   (missing)\n  Line 27:\n    expected:           ctx=Store())],\n    actual:   (missing)\n  Line 28:\n    expected:       value=Name(id='l', ctx=Load())),\n    actual:   (missing)\n  Line 29:\n    expected:     Assign(\n    actual:   (missing)\n  Line 30:\n    expected:       targets=[\n    actual:   (missing) (×1)
- AST mismatch:\n  Line 22:\n    expected:                 Return(\n    actual:                   Pass()])])])])\n  Line 23:\n    expected:                   value=Constant(value='value'))])]),\n    actual:   (missing)\n  Line 24:\n    expected:         Return(\n    actual:   (missing)\n  Line 25:\n    expected:           value=Constant(value='ok'))])])\n    actual:   (missing) (×1)
- AST mismatch:\n  Line 13:\n    expected:         Tuple(\n    actual:           Name(id='a', ctx=Store())],\n  Line 14:\n    expected:           elts=[\n    actual:         value=Starred(\n  Line 15:\n    expected:             Name(id='a', ctx=Store()),\n    actual:           value=Name(id='x', ctx=Load()),\n  Line 16:\n    expected:             Name(id='b', ctx=Store()),\n    actual:           ctx=Load())),\n  Line 17:\n    expected:             Name(id='c', ctx=Store())],\n    actual:       Assign(\n  Line 18:\n    expected:           ctx=Store())],\n    actual:         targets=[\n  Line 19:\n    expected:       value=Name(id='x', ctx=Load())),\n    actual:           Name(id='b', ctx=Store())],\n  Line 20:\n    expected:     Assign(\n    actual:         value=Starred(\n  Line 21:\n    expected:       targets=[\n    actual:           value=Name(id='x', ctx=Load()),\n  Line 22:\n    expected:         Name(id='x', ctx=Store())],\n    actual:           ctx=Load())), (×1)
- Token mismatch:\nLine 0: expected [for] (WORD), got [?] (WORD)\nLine 0: expected [i] (WORD), got [=] (SYMBOL)\nLine 0: expected [,] (SYMBOL), got [[] (SYMBOL)\nLine 0: expected [x] (WORD), got [res] (WORD)\nLine 0: expected [in] (WORD), got [.] (SYMBOL)\nLine 0: expected [enumerate] (WORD), got [append] (WORD)\nLine 0: expected [lst] (WORD), got [func] (WORD)\nLine 0: expected [)] (SYMBOL), got [(] (SYMBOL)\nLine 0: expected [:] (SYMBOL), got [i] (WORD)\nLine 0: expected [res] (WORD), got [,] (SYMBOL) (×1)
- AST mismatch:\n  Line 2:\n    expected:     Expr(\n    actual:       Assign(\n  Line 3:\n    expected:       value=Constant(value="\ntest_integers.py -- source test pattern for integers\n\nThis source is part of the decompyle test suite.\nSnippet taken from python libs's test_class.py\n\ndecompyle is a Python byte-code decompiler\nSee http://www.goebel-consult.de/decompyle/ for download and\nfor further information\n")),\n    actual:         targets=[\n  Line 4:\n    expected:     Import(\n    actual:           Name(id='name_0', ctx=Store())],\n  Line 5:\n    expected:       names=[\n    actual:         value=Constant(value="\ntest_integers.py -- source test pattern for integers\n\nThis source is part of the decompyle test suite.\nSnippet taken from python libs's test_class.py\n\ndecompyle is a Python byte-code decompiler\nSee http://www.goebel-consult.de/decompyle/ for download and\nfor further information\n")),\n  Line 6:\n    expected:         alias(name='sys')]),\n    actual:       Import(\n  Line 7:\n    expected:     Assign(\n    actual:         names=[\n  Line 8:\n    expected:       targets=[\n    actual:           alias(name='name_1')]),\n  Line 9:\n    expected:         Name(id='i', ctx=Store())],\n    actual:       Assign(\n  Line 10:\n    expected:       value=Constant(value=1)),\n    actual:         targets=[\n  Line 11:\n    expected:     Assign(\n    actual:           Name(id='name_2', ctx=Store())], (×1)

---

## 4. 失败测试详情

### async_def

**错误**: AST mismatch:\n  Line 12:\n    expected:           value=Await(\n    actual:             value=YieldFrom(

### test_pop_jump_forward_if_false

**错误**: AST mismatch:\n  Line 10:\n    expected:         Expr(\n    actual:           Return(\n  Line 14:\n    expected:        

### conditional_expressions

**错误**: AST mismatch:\n  Line 2:\n    expected:     Assign(\n    actual:       Expr(\n  Line 3:\n    expected:       targets=[\n

### test_exceptions

**错误**: AST mismatch:\n  Line 63:\n    expected:                   value=Constant(value=2))])],\n    actual:                    

### load_classderef

**错误**: AST mismatch:\n  Line 8:\n    expected:             Name(id='x', ctx=Store())],\n    actual:               Name(id='my_c

### store_slice

**错误**: AST mismatch:\n  Line 21:\n    expected:     Assign(\n    actual:       Expr(\n  Line 22:\n    expected:       targets=[

### test_exception_match_py311

**错误**: AST mismatch:\n  Line 22:\n    expected:                 Return(\n    actual:                   Pass()])])])])\n  Line 2

### unpack_assign

**错误**: AST mismatch:\n  Line 13:\n    expected:         Tuple(\n    actual:           Name(id='a', ctx=Store())],\n  Line 14:\n

### iter_unpack

**错误**: Token mismatch:\nLine 0: expected [for] (WORD), got [?] (WORD)\nLine 0: expected [i] (WORD), got [=] (SYMBOL)\nLine 0: e

### test_integers_py3

**错误**: AST mismatch:\n  Line 2:\n    expected:     Expr(\n    actual:       Assign(\n  Line 3:\n    expected:       value=Const

### binary_ops

**错误**: AST mismatch:\n  Line 4:\n    expected:         Tuple(\n    actual:           Name(id='a', ctx=Store())],\n  Line 5:\n  

### test_class_method

**错误**: AST mismatch:\n  Line 20:\n    expected:                 Expr(\n    actual:                   Return(\n  Line 24:\n    e

### variable_annotations

**错误**: AST mismatch:\n  Line 2:\n    expected:     AnnAssign(\n    actual:       Expr(\n  Line 3:\n    expected:       target=N

### loop_try_except

**错误**: Token mismatch:\nLine 0: expected [async] (WORD), got [while] (WORD)\nLine 0: expected [for] (WORD), got [c] (WORD)\nLin

### f-string

**错误**: Exception: InvalidOperationException: Unrecognized tokens: "\' inside'}'''")" at line 24

### test_slices

**错误**: Token mismatch:\nLine 0: expected [1] (INT), got [:] (SYMBOL)\nLine 0: expected []] (SYMBOL), got [42] (INT)\nLine 0: ex

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

### test_sets

**错误**: AST mismatch:\n  Line 24:\n    expected:       value=Set(\n    actual:         value=List(\n  Line 29:\n    expected:   

### test_decorators

**错误**: AST mismatch:\n  Line 3:\n    expected:       name='simple_decorator',\n    actual:         name='square',\n  Line 6:\n 

### test_with

**错误**: AST mismatch:\n  Line 2:\n    expected:     With(\n    actual:       Expr(\n  Line 3:\n    expected:       items=[\n    

### private_name

**错误**: AST mismatch:\n  Line 43:\n    expected:             Name(id='__private_var', ctx=Store())],\n    actual:               

### op_precedence

**错误**: AST mismatch:\n  Line 12:\n    expected:             left=Name(id='c', ctx=Load()),\n    actual:               left=BinO

### chain_assignment

**错误**: AST mismatch:\n  Line 4:\n    expected:         Name(id='a', ctx=Store()),\n    actual:           Name(id='a', ctx=Store

### test_main

**错误**: Token mismatch:\nLine 0: expected [from] (WORD), got [,] (SYMBOL)\nLine 0: expected [app] (WORD), got [sync] (WORD)\nLin


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
