# Decompiled from: <module>

def process_data_file(filename):
    """
    读取文件中的数字，计算平均值。
    演示嵌套的 try-except-else-finally 用法。
    """
    data = None
    try:
        print(f"[外层] 尝试打开文件: {filename}")
        file = open(filename, 'r')
    finally:
        print(f"[外层 except] 文件不存在: {filename}")
    print('[外层 finally] 程序结束')
print('==================================================')
print('测试1: 正常文件')
print('==================================================')
try:
    f.write("""10
20
abc
30
40
""")
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
None(None)
