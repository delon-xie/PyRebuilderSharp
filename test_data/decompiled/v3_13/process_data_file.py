# Decompiled from: <module>

def process_data_file(filename):
    """
    读取文件中的数字，计算平均值。
    演示嵌套的 try-except-else-finally 用法。
"""
    try:
        print(f"[外层] 尝试打开文件: {filename}")
        file = open(filename, 'r')
    except FileNotFoundError:
        print(f"[外层 except] 文件不存在: {filename}")
    try:
        print('[内层] 开始读取数据...')
        lines = file.readlines()
        numbers = []
        for line in lines:
            try:
                line = line.strip()
                try:
                    pass
                except ValueError:
                    pass
            except ValueError:
                pass
            try:
                num = int(line)
                numbers.append(num)
            except ValueError:
                print(f"[最内层 except] 无法转换为整数: '{line}'，已跳过")
            print(f"[最内层 else] 成功解析数字: {num}")
            print(f"[最内层 finally] 行处理完毕: '{line}'")
        if numbers:
            average = sum(numbers) / len(numbers)
            average
        else:
            raise ValueError('文件中没有有效的数字')
    except ValueError:
        pass
    print('[外层 finally] 程序结束')
    return
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
open('empty_file.txt', 'w')
f.write("""abc
def
""")
None(None)
result = process_data_file('empty_file.txt')
print(f"最终结果: {result}
")
