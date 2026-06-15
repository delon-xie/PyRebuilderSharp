namespace PyRebuilderSharp.Core.Versioning;

/// <summary>
/// Python 版本枚举。每个版本独立编号——.pyc 格式不向后兼容。
/// 见 docs/pyc_format_reference.md 获取完整的格式差异参考。
/// </summary>
public enum PythonVersion
{
    Unknown = 0,
    Py27,       // Python 2.7
    Py35,       // Python 3.5
    Py36,       // Python 3.6
    Py37,       // Python 3.7
    Py38,       // Python 3.8
    Py39,       // Python 3.9
    Py310,      // Python 3.10
    Py311,      // Python 3.11 — 首个 cache/exceptiontable/localsplus/qualname 版本
    Py312,      // Python 3.12 — 完整 cache 表, CALL=171
    Py313,      // Python 3.13 — HAVE_ARGUMENT=44, 操作码全面重编
    Py314,      // Python 3.14 — HAVE_ARGUMENT=43, 再次重编

    // 版本分组（用于策略共用）
    PreWordcode = Py27,     // 2.7, 3.5
    Wordcode = Py36,        // 3.6-3.10
    CacheCode = Py311,      // 3.11+
    Renumbered = Py313,     // 3.13-3.14 (独立编号)
}
