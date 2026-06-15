# Python .pyc 格式版本参考 (v1.0)

> 铁律：Python 跨版本的 .pyc 格式**不向后兼容**。每个版本都是独立的。
> 所有知识来源于 CPython 源码（Python/marshal.c, Python/compile.c, Lib/opcode.py）。
> 当 PyRebuilderSharp 的行为与本文档冲突时，以 CPython 源码为准。

---

## 1. 魔数与版本检测

| 版本 | 魔数 (小端) | `_pythonMinorVersion` | 备注 |
|:----:|:----------|:---------------------:|:-----|
| 2.7 | `03 F3 0D 0A` | — | 8字节头部 |
| 3.5 | `17 0D 0D 0A` | — | wordcode前 |
| 3.6 | `33 0D 0D 0A` | — | wordcode开始 |
| 3.7 | `42 0D 0D 0A` | — | |
| 3.8 | `55 0D 0D 0A` | — | PEP 552 header |
| 3.9 | `61 0D 0D 0A` | — | |
| 3.10 | `6F 0D 0D 0A` | — | linetable 开始 |
| 3.11 | `A0 0D 0D 0A` 或 `A7 0D 0D 0A` | 11 | TYPE_CODE_SIMPLE |
| 3.12 | `CB 0D 0D 0A` | 12 | 完整cache表 |
| 3.13 | `E7 0D 0D 0A` | 13 | 操作码全面重编号 |
| 3.14 | `F3 0D 0D 0A` 或 `2B 0E 0D 0A` | 14 | HAVE_ARGUMENT=43, 另一套编号 |

> ⚠️ `F3 0D 0D 0A` 是 **3.14** 的魔数，不是 3.13！
> 见 Python/importlib/_bootstrap_external.py 的 _set_filesize_magic_table。

---

## 2. 头部格式

### 2.7
```
magic(4) + timestamp(4) = 8字节
```

### 3.5-3.7
```
magic(4) + timestamp(4) + source_size(4) = 12字节
```

### 3.8-3.10 (PEP 552)
```
magic(4) + flags(4) + [hash(8) if flags&1 else timestamp(4)] + source_size(4)
```
- `flags & 1`: hash-based .pyc（8字节hash）vs timestamp-based（4字节timestamp）
- `flags & 2`: source_size 存在（3.8+ 总是存在）
- 最小头部 = 16字节, 最大 = 20字节

### 3.11-3.14
```
magic(4) + bitfield(4) + [hash(8) if bitfield&1 else timestamp(4)] + source_size(4)
```
- 与 3.8-3.10 相同布局
- 3.11 新增 bitfield 位2: `0x04` = 支持 TYPE_CODE_SIMPLE

---

## 3. Marshal 对象格式

### 2.7
```
TYPE_CODE (0x63) [+ FLAG_REF (0x80)]
  argcount(int32)
  nlocals(int32)
  stacksize(int32)
  flags(int32)
  code(TYPE_STRING)
  consts(TUPLE)
  names(TUPLE-of-string)
  varnames(TUPLE-of-string)
  freevars(TUPLE-of-string)
  cellvars(TUPLE-of-string)
  filename(STRING)
  name(STRING)
  firstlineno(int32)
  lnotab(TYPE_STRING)
```

### 3.5-3.10
和 2.7 类似但：
- `names`, `varnames`, `freevars`, `cellvars` 使用 interned string 格式
- 3.8+: 新增 `posonlyargcount` 字段（在 argcount 之后）

### 3.11+ (TYPE_CODE, non-simple)
```
[FLAG_REF] TYPE_CODE (0x63)
  argcount(int32)
  posonlyargcount(int32)        # ← 新增
  kwonlyargcount(int32)
  stacksize(int32)
  flags(int32)
  code(TYPE_STRING              # 0x73 with ref tracking)
  consts(TUPLE)
  localsplusnames(TUPLE)        # ← 替代 names+varnames+freevars+cellvars
  localspluskinds(TYPE_STRING)  # ← 新增
  filename(STRING)
  name(STRING)
  qualname(STRING)              # ← 新增
  firstlineno(int32)
  lnotab(TYPE_STRING 或 linetable TYPE_STRING)
  exceptiontable(TYPE_STRING)   # ← 新增
```

### 3.11+ (TYPE_CODE_SIMPLE, 0x73 with FLAG_REF clear)
```
[FLAG_REF] TYPE_STRING (0x73) [When bitfield & 0x04 is set]
  → 实际上是 TYPE_CODE_SIMPLE，字段少一些：
  argcount(int32)
  nlocals(int32)
  stacksize(int32)
  flags(int32)
  code(TYPE_STRING)
  consts(TUPLE)
  ... 同上
```

### 3.14 特有的 marshal 行为
- marshal 格式本身未变（与 3.11-3.13 相同）
- TYPE_CODE_SIMPLE 继续使用
- 唯一差异在字节码（操作码编号 + cache 配置）

---

## 4. 字节码格式

| 版本 | 格式 | 每指令字节 | CACHE | HAVE_ARGUMENT |
|:----:|:----:|:--------:|:----:|:------------:|
| 2.7 | 可变长 | 1 或 3 | 无 | 90 |
| 3.5 | 可变长 | 1 或 3 | 无 | 90 |
| 3.6-3.10 | wordcode | 2 | 无 | 90 |
| 3.11 | wordcode+cache | 2+@ | 稀疏 | 90 |
| 3.12 | wordcode+cache | 2+@ | 全量 | 90 |
| 3.13 | wordcode+cache | 2+@ | 全量(重编) | **44** |
| 3.14 | wordcode+cache | 2+@ | 全量(重设计) | **43** |

### 可变长格式 (2.7/3.5)
```
if rawop >= HAVE_ARGUMENT (90):
    opcode(1) + arg_le16(2) = 3字节
else:
    opcode(1) = 1字节
```

### Wordcode (3.6+)
```
instruction = opcode(1) + arg(1) = 2字节
arg = (extended_arg << 8) | raw_arg
```

### CACHE 格式 (3.11+)
每个 cache 条目 = 2字节，opcode 字段 = 0
```
instruction(2) + [cache(2)]*N
```
3.12+ 中 cache 在编译时预分配，所以即使从未使用的 cache 槽也存在。
3.14 的 cache 格式由 `opcode._cache_format` 定义（每个字段名→字节数）。

### 跳转偏移量编码
- **3.9 及更早**: 字节偏移（目标是绝对字节位置）
- **3.10+**: word 偏移（目标是 instruction index × 2）
- PyRebuilderSharp 中 `IsWordOffsetVersion()` 处理此转换

---

## 5. 操作码编号

### 2.7 (独立编号)
- 2.7 的操作码 70-89 与 3.x 完全不同（PRINT_EXPR=70, BREAK_LOOP=80 等）
- 需 `MapOpcode27()` 映射

### 3.5-3.10 (统一编号)
- 所有版本共用一套编号（少量增减）
- 3.9 新增: IS_OP=117, CONTAINS_OP=118
- 3.10 新增: YIELD_FROM=72（从 87 重编号），GEN_START=71

### 3.11-3.12 (大重构编号)
- `HAVE_ARGUMENT` 仍为 90，但操作码值大量改变
- 新增: PUSH_NULL=2, SWAP=99, COPY=120, RETURN_CONST=121→190(内部), BINARY_OP=122→191(内部)
- 3.12 新增: CALL=171, KW_NAMES=172 等
- 3.11 特有: PRECALL_311=166, CALL_311=167
- 3.12 新增: PUSH_EXC_HANDLER_312=177, PULL_EXC_FROM_INFO_312=178 等

### 3.13 (完全重编号)
- `HAVE_ARGUMENT` = **44**（从 90 改变）
- 所有操作码按字母/功能重新编号
- 新增 3.13 特定操作码（TO_BOOL_313=40 等）

### 3.14 (再次重编号)
- `HAVE_ARGUMENT` = **43**（从 44 改变）
- 编号体系与 3.13 **完全不同**
- `RESUME` = 128（3.13 中 = 149, 3.12 中 = 151, 3.11 中 = 90）
- 新增: LOAD_SMALL_INT=94, LOAD_FAST_BORROW=86, NOT_TAKEN=28, POP_ITER=30
- super-instruction 区域: 129-255（BINARY_OP_ADD_FLOAT=129, CALL_PY_EXACT_ARGS=161 等）

---

## 6. CACHE 配置对照

### 3.11 (稀疏)
仅少数操作码有 cache:
- UNPACK_SEQUENCE(92): 1
- COMPARE_OP(107): 2
- BINARY_OP(122): 1
- UNARY_OP(123): 1
- CALL(171): 4
等。多数基础操作码（LOAD_CONST, LOAD_NAME, STORE_NAME）无 cache。

### 3.12 (全量预分配)
几乎每个有参操作码都有固定 cache 条目表。
参考 `GetCacheCount312()`。

### 3.13 (重编号)
cache 配置对应 3.13 的原始操作码字节值。
参考 `GetCacheCount313()`。

### 3.14 (重新设计)
cache 由 `_cache_format` dict 定义，每个操作码有命名字段配置：
| 操作码 | raw | 总cache条目 | 字段 |
|:-------|:---:|:----------:|:----|
| STORE_SUBSCR | 38 | 1 | counter |
| TO_BOOL | 39 | 3 | counter+version |
| BINARY_OP | 44 | 5 | counter+descr |
| CALL | 52 | 3 | counter+func_version |
| CALL_KW | 55 | 3 | counter+func_version |
| COMPARE_OP | 56 | 1 | counter |
| CONTAINS_OP | 57 | 1 | counter |
| FOR_ITER | 70 | 1 | counter |
| JUMP_BACKWARD | 75 | 1 | counter |
| LOAD_ATTR | 80 | 9 | counter+version+keys_version+descr |
| LOAD_GLOBAL | 92 | 4 | counter+index+module_keys+builtin_keys |
| LOAD_SUPER_ATTR | 96 | 1 | counter |
| POP_JUMP_IF_FALSE | 100 | 1 | counter |
| POP_JUMP_IF_NONE | 101 | 1 | counter |
| POP_JUMP_IF_NOT_NONE | 102 | 1 | counter |
| POP_JUMP_IF_TRUE | 103 | 1 | counter |
| SEND | 106 | 1 | counter |
| STORE_ATTR | 110 | 4 | counter+version+index |
| UNPACK_SEQUENCE | 119 | 1 | counter |

---

## 7. 关键版本分界点

| 分界 | 触发条件 | 变更内容 |
|:----|:---------|:---------|
| 2.7 | `IsPython27()` | 特殊操作码映射 + 8字节头部 |
| pre-3.6 | magic < 0x33 | 可变长字节码格式 |
| 3.6+ | magic >= 0x33 | wordcode 格式 |
| 3.8+ | magic >= 0x55 | PEP 552 header |
| 3.10+ | magic >= 0x6F | linetable, word offsets |
| 3.11+ | IsPython311Plus() | cache, exceptiontable, qualname, localsplus, TYPE_CODE_SIMPLE |
| 3.12 | _pythonMinorVersion == 12 | 完整 cache 表, CALL=171 |
| 3.13 | _pythonMinorVersion == 13 | HAVE_ARGUMENT=44, 操作码全面重编 |
| 3.14 | _pythonMinorVersion == 14 | HAVE_ARGUMENT=43, 再次重编 |

---

## 8. 已知坑点

1. **`F30D0D0A` 不是 3.13**。字节顺序 `F3 0D 0D 0A` 是 3.14 的魔数（第 2 个）。
2. **3.12 的 CALL 操作码** 在字节码中 arg 是 cache offset，不是函数参数数量。
3. **3.13/3.14 的 `EXTENDED_ARG` 链** 在 wordcode 中 `extArg = (extArg << 8) | rawArg`，但 3.13+ 的 HAVE_ARGUMENT 是 44/43，所以 rawOp >= 44/43 才组合参数。
4. **3.14 的 `LOADS_SMALL_INT`** 直接编码小整数 arg，不是 LOAD_CONST+co_consts 索引。
5. **3.14 的 `NOT_TAKEN`** 紧随条件跳转指令，提示 JIT 该分支未执行，不是独立指令。
6. **3.14 的 `POP_ITER`** 在 for 循环结束后弹出迭代器，替代 `POP_TOP`。
7. **3.11+ 的 TYPE_CODE_SIMPLE** 在字节码层面与 TYPE_CODE 有相同的剩余字段，但 marshal 编码更紧凑。
8. **3.12+ 删除的 PRECALL** 3.11 的 PRECALL+CALL 序列在 3.12 中被合并为单个 CALL。
