namespace PyRebuilderSharp.Core;

/// <summary>反编译过程中的异常</summary>
public class DecompilationException : Exception
{
    public DecompilationException(string message) : base(message) { }
    public DecompilationException(string message, Exception inner)
        : base(message, inner) { }
}
