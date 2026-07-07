# Level 7 诊断结果

> Level 7：边界情况与语法特性
> 4 文件 × 34 测试点，7011 diff lines（~7000 来自 test_syntax.py）

---

## 核心文件问题分析

**l7_edge.py** (24 diff lines, 全部是已知问题的重现):

| 问题 | 说明 | 对应 Level | 难度 |
|:-----|:------|:-----------|:----:|
| continue/break in while 丢失 | l7_9/10 — `continue` 在循环体尾部被消除 | — | 🟢 |
| `return None`→`pass` | l7_11/15 — `StripTrailingReturnNone` 未覆盖内层函数 | l4_13 | 🟢 |
| if-elif→三元 | l7_12 — `isSimpleAndExpr` 对多条件 if 的误判 | l1_2 | 🟢 |
| `return total` 丢失 | l7_13 — 嵌套 for 的 `return total` 被死代码消除 | l1_4 | 🟡 |
| tuple 括号 `(a, b)` | l7_5/19/20 — 返回值带括号 | known | 🟢 |
| 常量折叠 `1+2`→`3` | l7_5/14 — 编译期常量已求值，反编译无法恢复 | by design | — |
| def→class | l7_17 — `global` 关键字触发 `PostProcessFunctionDefs` 中 `ClassDef` 误判 | l1_6 | 🟡 |
| nonlocal 变量丢失 | l7_18 — `x = 10` 和 `nonlocal x; x = 20` 消失 | l4_6 | 🟡 |
| 链式赋值 `a=b=c=1`→`c=b:=a:=1` | l7_20 — walrus 检测对链式赋值的过度匹配 | l6_7 | 🟢 |

**test_syntax.py** (108KB CPython 测试，≈7000 diff lines) — 不是反编译目标测试文件，应跳过。

---

## 建议

Level 7 不包含新的反编译问题——所有问题都在 Level 1-6 中出现过。建议在下一轮迭代中：
1. 将 `test_syntax.py` 移出 Level 7（非反编译测试目标）
2. 聚焦 Level 1 (l1_4/7/9)、Level 2 (try/except)、Level 5 (`__build_class__`)、Level 6 (推导式) 的深层修复

这些深层修复完成后，Level 7 的对应问题自然解决。
