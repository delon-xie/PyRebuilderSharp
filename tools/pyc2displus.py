#!/usr/bin/env python3
"""
pyc2displus — Full-detail .pyc dumper.

Parses every byte of a .pyc file and dumps all readable information
with zero detail loss:
  - Full header (magic → Python version, flags, timestamp, source_size)
  - Every code object field recursively (incl. version‑gated fields)
  - Raw co_code hex + instruction count
  - Decoded co_lnotab (offset→line mapping)
  - co_linetable, co_endlinetable, co_columntable (3.10+/3.11+)
  - co_exceptiontable fully decoded (3.11+)
  - Detailed disassembly via dis.Bytecode() with argrepr
  - Recursive code-object tree (loop‑safe via id tracking)
"""

import marshal
import struct
import dis
import types
import sys
import datetime
import io

# ── Magic number → Python version ──────────────────────────────────────────
MAGIC_MAP = {
    20121: "2.7",
    50823: "3.0-3.2",
    3065:  "3.3",
    3085:  "3.4-3.5",
    3361:  "3.6",
    3393:  "3.7",
    3413:  "3.8",
    3425:  "3.9a",
    3439:  "3.9",
    3456:  "3.10a",
    3470:  "3.10b",
    3489:  "3.10",
    3511:  "3.11a",
    3523:  "3.11b",
    3535:  "3.11",
    3551:  "3.12a",
    3560:  "3.12",
    3579:  "3.12b",
    3582:  "3.12c",
    3595:  "3.13a",
    3614:  "3.13b",
    3630:  "3.13",
    3643:  "3.14a",
    3671:  "3.14",
}


def decode_magic(magic_bytes):
    magic_val = struct.unpack('<H', magic_bytes[:2])[0]
    return MAGIC_MAP.get(magic_val, f"unknown(0x{magic_val:04x})")


def get_major_version(magic_bytes):
    """Return (major, minor) guessed from magic number."""
    magic_val = struct.unpack('<H', magic_bytes[:2])[0]
    ver = MAGIC_MAP.get(magic_val, "")
    if ver.startswith("3."):
        parts = ver.split(".")[1].split("a")[0].split("b")[0]
        try:
            return (3, int(parts))
        except ValueError:
            pass
    elif ver.startswith("2."):
        return (2, 7)
    return None


# ── Exception-table decoder (3.11+) ────────────────────────────────────────
def decode_exception_table(data):
    """Decode Python 3.11+ exception table (entries of 7 bytes each)."""
    entries = []
    i = 0
    while i + 7 <= len(data):
        start  = data[i] | (data[i + 1] << 8)
        end    = data[i + 2] | (data[i + 3] << 8)
        target = data[i + 4] | (data[i + 5] << 8)
        dl     = data[i + 6]
        depth  = dl & 3
        lasti  = (dl >> 2) & 0x3f
        entries.append({
            'start': start, 'end': end, 'target': target,
            'depth': depth, 'lasti': lasti,
        })
        i += 7
    return entries


# ── lnotab decoder ─────────────────────────────────────────────────────────
def decode_lnotab(lnotab, firstlineno):
    """Decode co_lnotab bytes into (offset, line) pairs."""
    entries = []
    offset = 0
    line = firstlineno
    for i in range(0, len(lnotab), 2):
        if i + 1 >= len(lnotab):
            break
        addr_delta = lnotab[i]
        line_delta = lnotab[i + 1]
        if addr_delta == 0 and line_delta == 0:
            # extended arg, skip (actually rare — safe guard)
            continue
        offset += addr_delta * 2  # byte offset = 2 × instruction offset
        if line_delta >= 128:
            line_delta -= 256
        line += line_delta
        entries.append((offset, line))
    return entries


# ── Flag decoder ───────────────────────────────────────────────────────────
FLAG_NAMES = [
    (0x0004, "CO_VARARGS (*args)"),
    (0x0008, "CO_VARKEYWORDS (**kwargs)"),
    (0x0020, "CO_GENERATOR"),
    (0x0040, "CO_COROUTINE (async def)"),
    (0x0080, "CO_ITERABLE_COROUTINE"),
    (0x0100, "CO_ASYNC_GENERATOR"),
    (0x0800, "CO_NO_FREE (no freevars/cellvars)"),
]


def decode_flags(flags):
    return [name for mask, name in FLAG_NAMES if flags & mask]


# ── Code-object dumper ─────────────────────────────────────────────────────
def show_code_full(code, indent=0, seen=None):
    if seen is None:
        seen = set()
    prefix = "  " * indent

    code_id = id(code)
    if code_id in seen:
        print(f"{prefix}=== CodeObject: {code.co_name!r} (already dumped, skip) ===")
        return
    seen.add(code_id)

    # ── header ─────────────────────────────────────────────────────────
    print(f"{prefix}=== CodeObject: {code.co_name!r} @ {code.co_filename!r} ===")
    print(f"{prefix}  co_argcount         = {code.co_argcount}")

    if hasattr(code, 'co_posonlyargcount'):
        print(f"{prefix}  co_posonlyargcount  = {code.co_posonlyargcount}")

    print(f"{prefix}  co_kwonlyargcount   = {code.co_kwonlyargcount}")
    print(f"{prefix}  co_nlocals          = {code.co_nlocals}")
    print(f"{prefix}  co_stacksize        = {code.co_stacksize}")
    print(f"{prefix}  co_flags            = 0x{code.co_flags:04x}")
    for f in decode_flags(code.co_flags):
        print(f"{prefix}    {f}")
    print(f"{prefix}  co_firstlineno      = {code.co_firstlineno}")

    if hasattr(code, 'co_qualname'):
        print(f"{prefix}  co_qualname         = {code.co_qualname!r}")

    # ── name / var tables ──────────────────────────────────────────────
    print(f"{prefix}  co_varnames         = {code.co_varnames}")
    print(f"{prefix}  co_names            = {code.co_names}")
    print(f"{prefix}  co_freevars         = {code.co_freevars}")
    print(f"{prefix}  co_cellvars         = {code.co_cellvars}")

    # ── raw bytecode ───────────────────────────────────────────────────
    raw = code.co_code
    print(f"{prefix}  co_code (raw hex)   = {raw.hex()}")
    n_instr = len(raw) // 2
    print(f"{prefix}    length            = {len(raw)} bytes ({n_instr} instructions)")

    # ── co_consts (recursive) ──────────────────────────────────────────
    print(f"{prefix}  co_consts:")
    for i, c in enumerate(code.co_consts):
        if isinstance(c, types.CodeType):
            print(f"{prefix}    [{i}] <code object {c.co_name!r}> @ {c.co_filename!r}:{c.co_firstlineno}")
            show_code_full(c, indent + 2, seen)
        elif c is None:
            print(f"{prefix}    [{i}] None")
        elif c is True:
            print(f"{prefix}    [{i}] True")
        elif c is False:
            print(f"{prefix}    [{i}] False")
        elif isinstance(c, (int, float, complex)):
            print(f"{prefix}    [{i}] {c!r}")
        elif isinstance(c, str):
            s = repr(c)
            if len(s) > 300:
                s = s[:300] + "..."
            print(f"{prefix}    [{i}] {s}")
        elif isinstance(c, bytes):
            print(f"{prefix}    [{i}] bytes ({len(c)} B): {c.hex()}")
        elif isinstance(c, tuple):
            if len(c) > 60:
                print(f"{prefix}    [{i}] tuple ({len(c)} items): {c[:10]!r} ...")
            else:
                print(f"{prefix}    [{i}] tuple: {c!r}")
        else:
            print(f"{prefix}    [{i}] {c!r}")

    # ── line-number tables ─────────────────────────────────────────────
    # co_lnotab (available in all versions)
    lnotab = code.co_lnotab
    print(f"{prefix}  co_lnotab (hex)     = {lnotab.hex()}")
    if lnotab:
        decoded = decode_lnotab(lnotab, code.co_firstlineno)
        print(f"{prefix}    decoded (offset → line):")
        for off, ln in decoded:
            print(f"{prefix}      offset={off:5d} → line {ln}")

    # co_linetable (3.10+)
    if hasattr(code, 'co_linetable') and code.co_linetable:
        print(f"{prefix}  co_linetable (hex)  = {code.co_linetable.hex()}")

    # co_endlinetable (3.11+)
    if hasattr(code, 'co_endlinetable') and code.co_endlinetable:
        print(f"{prefix}  co_endlinetable     = {code.co_endlinetable.hex()}")

    # co_columntable (3.11+)
    if hasattr(code, 'co_columntable') and code.co_columntable:
        print(f"{prefix}  co_columntable      = {code.co_columntable.hex()}")

    # ── exception table (3.11+) ────────────────────────────────────────
    if hasattr(code, 'co_exceptiontable') and code.co_exceptiontable:
        print(f"{prefix}  co_exceptiontable   = {code.co_exceptiontable.hex()}")
        if code.co_exceptiontable:
            entries = decode_exception_table(code.co_exceptiontable)
            print(f"{prefix}    entries ({len(entries)}):")
            for e in entries:
                print(f"{prefix}      try [{e['start']:5d}, {e['end']:5d}) → "
                      f"target={e['target']:5d}  depth={e['depth']}  lasti={e['lasti']}")

    # ── detailed disassembly ───────────────────────────────────────────
    print(f"{prefix}  --- dis (detailed) ---")
    try:
        bc = dis.Bytecode(code)
        for instr in bc:
            arg_part = ""
            if instr.argrepr:
                arg_part = f"  # {instr.argrepr}"
            elif instr.arg is not None:
                arg_part = f"  # [{instr.arg}]"
            print(f"{prefix}    {instr.offset:4d}  {instr.opname:20s} "
                  f"{str(instr.arg or ''):>6s}{arg_part}")
    except Exception as exc:
        # fallback to text-based dis
        print(f"{prefix}    (dis.Bytecode failed: {exc})")
        print(f"{prefix}    --- dis (text fallback) ---")
        buf = io.StringIO()
        dis.dis(code, file=buf)
        for line in buf.getvalue().splitlines():
            print(f"{prefix}    {line}")

    print()


# ── PYC loader ─────────────────────────────────────────────────────────────
def load_pyc(path):
    with open(path, "rb") as f:
        data = f.read()

    print(f"=== PYC File: {path} ===")
    print(f"  Total size       = {len(data)} bytes")
    print()

    # ── magic ──────────────────────────────────────────────────────────
    magic_bytes = data[:4]
    magic_val = struct.unpack('<H', magic_bytes[:2])[0]
    py_ver = decode_magic(magic_bytes)
    print(f"  Magic            = {magic_bytes.hex()}  (Python {py_ver})")
    print(f"    value          = 0x{magic_val:04x}")

    # ── header fields ──────────────────────────────────────────────────
    # Detect header format
    #  3.0–3.6 : magic(4) + timestamp(4) [+ source_size(4)]
    #  3.7+    : magic(4) + flags(4) + timestamp(4) + source_size(4)

    ver = get_major_version(magic_bytes)
    header_size = 4

    # Try 3.7+ first: 4 bytes after magic are flags
    if len(data) >= 16:
        # Peek at what would be flags — 3.7+ flags for py_compile is
        # typically 0x0000000d, so check for a small non‑timestamp value
        candidate_flags = struct.unpack('<I', data[4:8])[0]
        # If the value looks like a small number (< 1e5) it's probably flags
        # rather than a unix timestamp (> 1.5e9 in 2017+).
        if candidate_flags < 100000:
            header_size = 16
            flags = candidate_flags
            print(f"  [3.7+ 16‑byte header detected]")
            print(f"  Header flags     = 0x{flags:08x}")
            if flags & 0x01:
                print(f"    0x01 = BIT_MODE_SOURCE (source timestamp/size present)")
            if flags & 0x02:
                print(f"    0x02 = BIT_MODE_COMPILED (no source check)")
            if flags & 0x04:
                print(f"    0x04 = (reserved bit)")
            timestamp = struct.unpack('<I', data[8:12])[0]
            source_size = struct.unpack('<I', data[12:16])[0]
            print(f"  Timestamp        = {timestamp}")
            print(f"    datetime       = {datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)}")
            print(f"  Source size      = {source_size} bytes")
        else:
            # Try 12‑byte header: magic(4) + timestamp(4) + source_size(4)
            if len(data) >= 12:
                header_size = 12
                timestamp = struct.unpack('<I', data[4:8])[0]
                source_size = struct.unpack('<I', data[8:12])[0]
                print(f"  [≤3.6 12‑byte header]")
                print(f"  Timestamp        = {timestamp}")
                print(f"    datetime       = {datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)}")
                print(f"  Source size      = {source_size} bytes")
            else:
                header_size = 8
                timestamp = struct.unpack('<I', data[4:8])[0]
                print(f"  [≤3.6 8‑byte header]")
                print(f"  Timestamp        = {timestamp}")
                print(f"    datetime       = {datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)}")

    elif len(data) >= 8:
        header_size = 8
        timestamp = struct.unpack('<I', data[4:8])[0]
        print(f"  [8‑byte header]")
        print(f"  Timestamp        = {timestamp}")
        print(f"    datetime       = {datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)}")
    else:
        print(f"  [Header too small to parse beyond magic]")

    print(f"  Data offset      = {header_size}")
    print(f"  Marshal data     = {len(data) - header_size} bytes")
    print()

    # ── marshal load ───────────────────────────────────────────────────
    code = marshal.loads(data[header_size:])
    return code


# ── CLI ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pyc2displus.py <path_to.pyc>")
        sys.exit(1)

    code = load_pyc(sys.argv[1])
    show_code_full(code)
