# Decompiled from: <module>

def process_data_file(filename):
    """
    读取文件中的数字，计算平均值。
    演示嵌套的 try-except-else-finally 用法。
    """
    print('[外层 finally] 程序结束')
    return
print('==================================================')
print('测试1: 正常文件')
print('==================================================')
f.write("""10
20
abc
30
40
""")
None(None)
result = process_data_file('test_numbers.txt')
print(f"最终结果: {result}
")
print('==================================================')
print('测试2: 文件不存在')
print('==================================================')
result = process_data_file('nonexistent.txt')
print(f"最终结果: {result}
")
print('==================================================')
print('测试3: 空文件')
print('==================================================')
f.write("""abc
def
""")
None(None)
result = process_data_file('empty_file.txt')
print(f"最终结果: {result}
")
