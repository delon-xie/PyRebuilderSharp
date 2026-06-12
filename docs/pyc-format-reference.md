# .pyc 文件格式知识库

来源：CPython 各版本 `Lib/py_compile.py` + `Lib/importlib/_bootstrap_external.py`。
涵盖 Python 2.7 ~ 3.14。

---

## 一、写入流程

### Python 2.7 (`Lib/py_compile.py`)
```python
MAGIC = imp.get_magic()  # 4 bytes
f.write(MAGIC)           # 4 bytes MAGIC
wr_long(f, timestamp)    # 4 bytes mtime (int32 LE)
marshal.dump(codeobject, f)
```

### Python 3.0-3.6 (`Lib/py_compile.py` → `_code_to_bytecode`)
```python
data = bytearray(MAGIC_NUMBER)   # 4 bytes
data.extend(_w_long(mtime))      # 4 bytes timestamp
data.extend(_w_long(source_size))# 4 bytes source size
data.extend(marshal.dumps(code))
```

### Python 3.7+ — Timestamp-based (`_code_to_timestamp_pyc`)
```python
data = bytearray(MAGIC_NUMBER)   # 4 bytes
data.extend(_pack_uint32(0))     # 4 bytes flags=0
data.extend(_pack_uint32(mtime)) # 4 bytes timestamp
data.extend(_pack_uint32(source_size)) # 4 bytes source size
data.extend(marshal.dumps(code))
```

### Python 3.7+ — Hash-based (`_code_to_hash_pyc`, PEP 552)
```python
data = bytearray(MAGIC_NUMBER)    # 4 bytes
flags = 0b1 | (checked << 1)     # 4 bytes (bit0=hash, bit1=unchecked)
data.extend(_pack_uint32(flags))
data.extend(source_hash)          # 8 bytes blake2b hash
data.extend(marshal.dumps(code))
```

---

## 二、Header 布局

| Python 版本 | 头部大小 | 布局 |
|-------------|---------|------|
| 2.7 | **8** 字节 | MAGIC(4) + mtime(4) |
| 3.0 - 3.6 | **12** 字节 | MAGIC(4) + mtime(4) + source_size(4) |
| 3.7+ (timestamp) | **16** 字节 | MAGIC(4) + flags(4) + mtime(4) + source_size(4) |
| 3.7+ (hash) | **16** 字节 | MAGIC(4) + flags(4) + source_hash(8) |

**检测策略**：
```python
if data[0]==0x03 and data[1]==0xF3:  # 2.7
    header_size = 8
elif data[0] < 0x42:  # 3.0-3.6 (magic < 0x0D42)
    header_size = 12
else:
    header_size = 16  # 3.7+
```

---

## 三、Flags 字段语义 (3.7+, offset 4-7)

```
Bit 0: 0 = timestamp-based .pyc
       1 = hash-based .pyc
Bit 1: 0 = checked hash (每次 import 重新计算并比较)
       1 = unchecked hash (信任已有 hash，仅存验证)
```

读取方式：`int.from_bytes(data[4:8], 'little')` / `_unpack_uint32(data[4:8])`

---

## 四、Magic Number 对照表

| 版本 | Magic 整数值 | Magic 字节 (LE) |
|------|-------------|-----------------|
| 2.7 | 0x03F3 | `03 F3 0D 0A` |
| 3.0 | 0x0D0B | `0B 0D 0D 0A` |
| 3.1 | 0x0D1A | `1A 0D 0D 0A` |
| 3.2 | 0x0D2F | `2F 0D 0D 0A` |
| 3.3 | 0x0D3E | `3E 0D 0D 0A` |
| 3.4 | 0x0D41 | `41 0D 0D 0A` |
| 3.5 | 0x0D17 | `17 0D 0D 0A` |
| 3.6 | 0x0D33 | `33 0D 0D 0A` |
| 3.7 | 3394 (0x0D42) | `42 0D 0D 0A` |
| 3.8 | 3413 (0x0D55) | `55 0D 0D 0A` |
| 3.9 | 3425 (0x0D61) | `61 0D 0D 0A` |
| 3.10 | 3439 (0x0D6F) | `6F 0D 0D 0A` |
| 3.11 | 3495 (0x0DA7) | `A7 0D 0D 0A` |
| 3.12 | 3531 (0x0DCB) | `CB 0D 0D 0A` |
| 3.13 | 3571 (0x0DE7) | `E7 0D 0D 0A` |
| 3.14 | `_imp.pyc_magic_number_token` | 4 字节整 LE (不再 0D 0A 固定后缀) |

**3.7-3.13 公式**：`value.to_bytes(2, 'little') + b'\r\n'`
**3.14+ 公式**：`_imp.pyc_magic_number_token.to_bytes(4, 'little')`

---

## 五、Marshal 数据

所有版本的 marshal 数据均由 `marshal.dumps(code)` 生成，marshal version = 4 (Python 3.4+)。

**FLAG_REF 机制 (3.4+)**:
- 类型字节高位 (`0x80`) 表示该对象被引用追踪
- `w_ref()` 流程（`marshal.c`）:
  1. `mark_object(v, p)` → 首次→返回 `-1`; 已存在→返回索引
  2. 首次: `*flag |= FLAG_REF` → `W_TYPE` 写入 `type|0x80` → 调用 `w_complex_object` 写入对象数据 **(无 ref_index)**
  3. 重复: `W_TYPE(TYPE_REF, p)` → `w_long(idx, p)` → return **不写对象**

**关键坑 — ref_index 不一致性**:
- CPython 的 `r_object` 读取 FLAG_REF 类型字节后调用 `r_long(p)` 读取 ref_index
- 但 `w_complex_object` 中 `W_TYPE` 写 type|FLAG_REF 后 **不写 ref_index**
- 实际文件里有 4 字节是因为 `mark_object()` 在 `w_ref` 中写入了 `TYPE_REF (0x72|0x80) + ref_index`... 但只对非首次对象
- **验证结论**：3.5-3.7 文件里 TYPE_CODE 后确实有 4 字节 ref_index；3.8+ 没有
- 原因推测：3.7 的 `w_ref` 实现中，首次 `mark_object` 返回 0 (非 -1)，导致写入 TYPE_REF；3.8+ 改为返回 -1，不再写入

**2.7 marshal 差异**:
- 无 FLAG_REF 机制
- TYPE_INTERNED = `0x74` ('t') — 4 字节长度 + UTF-8 bytes，用于 names/varnames
- TYPE_STRINGREF = `0x7A` ('z') — 4 字节索引，引用之前出现过的 interned string
- TYPE_STRING = `0x73` ('s') — 4 字节长度 + raw bytes，用于 filename/name/code/lnotab

---

## 六、对反编译器的影响

| 影响点 | 需处理的版本差异 |
|--------|----------------|
| Header 解析 | 2.7=8B, 3.0-3.6=12B, 3.7+=16B |
| CodeObject 字段 | 2.7: 4字段; 3.0-3.7: 4字段; 3.8+: 6字段(含posOnly) |
| 指令格式 | 2.7/3.5: 可变长(1或3B); 3.6+: 2B wordcode; 3.11+: 有CACHE |
| 跳转偏移 | 3.10+: 字节偏移 \*2; 3.9-: 字偏移 |
| Slice | 2.7: SLICE_0-3 独立 opcode; 3.x: BUILD_SLICE+ BINARY_SUBSCR |
| 比较运算 | 3.8-: COMPARE_OP; 3.9+: IS_OP/CONTAINS_OP |
| 函数调用 | 3.7-3.9: CALL_METHOD/LOAD_METHOD; 3.11+: PRECALL/CALL |
| 异常表 | 3.10+: 异常表条目; 3.9-: 无 |

---

## 七、关键源文件

- `Lib/py_compile.py` — 编译入口
- `Lib/importlib/_bootstrap_external.py` — 格式定义、验证、MAGIC_NUMBER
- `Python/marshal.c` — marshal 序列化/反序列化
- `Objects/codeobject.c` — CodeObject 构造
- `Python/compile.c` — Python 源码→字节码
- `Include/opcode_ids.h` / `Lib/opcode.py` — opcode 定义
