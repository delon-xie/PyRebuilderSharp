// Diagnostic: trace marshal positions through nested code object reading
using PyRebuilderSharp.Core.Readers;

var root = "/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled";
var file = Path.Combine(root, "abc.3.12.pyc");
var data = File.ReadAllBytes(file);

// Use reflection to access private methods for tracing
// Alternatively, add guard positions in ReadMarshalCodeObject

// Let's just use the Public API and check result
using var ms = new MemoryStream(data);
using var br = new BinaryReader(ms);

// Skip header
br.ReadBytes(16); // header

var readerType = typeof(PycReader);
var reader = Activator.CreateInstance(readerType, nonPublic: true);

var readMethod = readerType.GetMethod("Read", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance);
var code = readMethod.Invoke(reader, new object[] { data });

var codeType = code.GetType();
var nameProp = codeType.GetProperty("Name");
var instrsProp = codeType.GetProperty("Instructions");
var childCodesProp = codeType.GetProperty("ChildCodes");
var constantsProp = codeType.GetProperty("Constants");

System.Console.WriteLine($"Code: {nameProp.GetValue(code)}");
System.Console.WriteLine($"Instructions: {((System.Collections.ICollection)instrsProp.GetValue(code)).Count}");

// Count child codes recursively
System.Func<object, int, int> countChildren = null;
countChildren = (obj, depth) => {
    var children = (System.Collections.IList)childCodesProp.GetValue(obj);
    var consts = (System.Collections.IDictionary)constantsProp.GetValue(obj);
    int total = 0;
    foreach (var c in children)
    {
        var cname = c.GetType().GetProperty("Name").GetValue(c);
        var ccount = c.GetType().GetProperty("Instructions")?.GetValue(c);
        System.Console.WriteLine($"  Child: {cname} (instrs={(ccount != null ? ((System.Collections.ICollection)ccount).Count : 0)})");
        total += 1 + countChildren(c, depth + 1);
    }
    return total;
};

var childCount = countChildren(code, 0);
System.Console.WriteLine($"Total child codes found: {childCount}");
System.Console.WriteLine($"Expected based on Python: 17 nested code objects");
