using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Versioning;

public static class VersionStrategyFactory
{
    /// <summary>
    /// 根据魔数字节创建对应的版本策略。
    /// 魔数格式与 Python/importlib/_bootstrap_external.py 一致。
    /// </summary>
    public static IVersionStrategy Create(byte[] magic)
    {
        if (magic.Length < 4)
            throw new ArgumentException("Magic bytes must be at least 4 bytes", nameof(magic));
        
        var magicHex = BitConverter.ToString(magic, 0, 4).Replace("-", "");
        
        return magicHex switch
        {
            "03F30D0A" => new VersionStrategy27(),
            
            // 3.5-3.10.0 魔数范围
            "170D0D0A" or "1C0D0D0A" or "200D0D0A" or "260D0D0A" or "2B0D0D0A" or "300D0D0A" 
                => new VersionStrategyPre311(is310: false, is38plus: false),
            "330D0D0A" or "3B0D0D0A" or "400D0D0A" => new VersionStrategyPre311(is310: false, is38plus: false),
            "420D0D0A" or "450D0D0A" or "4D0D0D0A" => new VersionStrategyPre311(is310: false, is38plus: false),
            "550D0D0A" or "5D0D0D0A" or "600D0D0A" => new VersionStrategyPre311(is310: false, is38plus: true),
            "610D0D0A" or "660D0D0A" or "6A0D0D0A" => new VersionStrategyPre311(is310: false, is38plus: true),
            "6F0D0D0A" => new VersionStrategyPre311(is310: true, is38plus: true),
            
            "A00D0D0A" or "A70D0D0A" => new VersionStrategy311(),
            "CB0D0D0A" => new VersionStrategy312(),
            "E70D0D0A" => new VersionStrategy313(),
            "F30D0D0A" or "2B0E0D0A" => new VersionStrategy314(),
            
            _ => throw new NotSupportedException($"Unknown Python magic: 0x{magicHex}")
        };
    }
}
