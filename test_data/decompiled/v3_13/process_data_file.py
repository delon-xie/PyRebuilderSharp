# Decompiled from: <module>

def process_data_file(filename):
    """
    读取文件中的数字，计算平均值。
    演示嵌套的 try-except-else-finally 用法。
"""
    data = None
    pass
    print('[内层] 开始读取数据...')
    lines = file.readlines()
    numbers = []
    lines
    average = [line.strip() for line in lines if not line]
print('==================================================')
print('测试1: 正常文件')
print('==================================================')
open('test_numbers.txt', 'w')
f.write("""10
20
abc
30
40
""")
None
result = process_data_file('test_numbers.txt')
print(f"最终结果: {result}\n")
print('==================================================')
print('测试2: 文件不存在')
print('==================================================')
result = process_data_file('nonexistent.txt')
print(f"最终结果: {result}\n")
print('==================================================')
print('测试3: 空文件')
print('==================================================')
open('empty_file.txt', 'w')
f.write("""abc
def
""")
None
result = process_data_file('empty_file.txt')
print(f"最终结果: {result}\n")
pass
pass
