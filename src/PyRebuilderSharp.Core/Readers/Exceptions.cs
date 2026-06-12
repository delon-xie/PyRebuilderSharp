namespace PyRebuilderSharp.Core.Readers;

/// <summary>无效的.pyc文件格式</summary>
public class InvalidPycFormatException : Exception
{
    public InvalidPycFormatException(string message) : base(message) { }
    public InvalidPycFormatException(string message, Exception inner)
        : base(message, inner) { }
}

/// <summary>不支持的Python版本</summary>
public class UnsupportedPythonVersionException : Exception
{
    public UnsupportedPythonVersionException(string message) : base(message) { }
}
