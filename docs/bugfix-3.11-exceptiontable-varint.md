# Bugfix: ExceptionTable Varint Parsing (3.11+)

**Commit**: `a6fbd10`
**Date**: 2026-06-16

## Symptom

Python 3.11+ `.pyc` files had incorrect try/except handler ranges. ExceptionTable offsets were read using a fixed 8-byte format, producing garbage ranges.

## Root Cause

CPython 3.11+ uses a **base-64 varint encoding** (6 bits per byte, bit 6 = continuation flag) for ExceptionTable entries, not a fixed 8-byte format.

**Reference**: CPython 3.11 `Python/marshal.c`:
```c
// Exception table entries are stored as base-128 varints
// Each entry: try_start, try_end, handler_start, target_depth
```

Actually it's base-64: each byte has 6 data bits + 1 continuation bit, big-endian. The `>>= 1` shift comes from CPython's implementation where the continuation bit is stored in bit 6.

## Fix Applied

Replaced fixed 8-byte format with base-64 varint decoder:

```csharp
// Base-64 varint: bit 6 = continuation, big-endian
// Reference: CPython 3.11 Python/marshal.c read_exception_table()
private static (bool hasNext, int value, int bytesRead) ReadVarint(byte[] data, int offset)
{
    int value = 0;
    int bytesRead = 0;
    while (offset + bytesRead < data.Length)
    {
        byte b = data[offset + bytesRead];
        bytesRead++;
        bool hasNext = (b & 0x40) != 0;  // bit 6 = continuation
        value = (value << 6) | (b & 0x3F);  // 6 data bits
        if (!hasNext)
            return (false, value, bytesRead);
    }
    return (false, value, bytesRead);  // fallback if malformed
}
```

## Affected Code

- `src/PyRebuilderSharp.Core/Readers/PycReader.cs` — ExceptionTable varint parser

## Regression

938/938 succeeded, 0 failed, 0 crashes ✅
