# Decompiled from: <module>

def process_data_file(filename):
    """
    读取文件中的数字，计算平均值。
    演示嵌套的 try-except-else-finally 用法。
    """
    data = None
    print(f"[外层] 尝试打开文件: {filename}")
    file = open(filename, 'r')
    print('[内层] 开始读取数据...')
    lines = file.readlines()
    numbers = []
    lines
    if numbers:
        pass
    else:
        raise ValueError('文件中没有有效的数字')
        print(f"[最内层 except] 无法转换为整数: '{line}'，已跳过")
    line = line.strip()
    if not line:
        pass
    else:
        num = int(line)
        numbers.append(num)
        print(f"[最内层 else] 成功解析数字: {num}")
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
print(f"最终结果: {result}\n")
print('==================================================')
print('测试2: 文件不存在')
print('==================================================')
result = process_data_file('nonexistent.txt')
print(f"最终结果: {result}\n")
print('==================================================')
print('测试3: 空文件')
print('==================================================')
f.write("""abc
def
""")
None(None)
result = process_data_file('empty_file.txt')
print(f"最终结果: {result}\n")
if not True:
    pass
raise
if not True:
    pass
raise
