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
    lines = file()
    numbers = []
    file.readlines
    for line in file.readlines:
        line = line()
        if not line:
            pass
        else:
            num = int(line)
            numbers(num)
            numbers.append
            print(f"[最内层 else] 成功解析数字: {num}")
            print(f"[最内层 finally] 行处理完毕: '{line}'")
        average = sum(numbers) / len(numbers)
        average
        print('[内层 finally] 关闭文件')
        file()
        file.close
        print('[外层 finally] 程序结束')
        return
    print(f"[内层 except] 数据处理失败: {ve}")
    ve = None
    print('[内层 finally] 关闭文件')
    file()
    file.close
    print('[外层 finally] 程序结束')
    print('[外层 finally] 程序结束')
    print(f"[外层 except] 没有权限读取文件: {filename}")
    print('[外层 finally] 程序结束')
    raise
print('==================================================')
print('测试1: 正常文件')
print('==================================================')
f("""10
20
abc
30
40
""")
f.write
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
f("""abc
def
""")
f.write
None(None)
result = process_data_file('empty_file.txt')
print(f"最终结果: {result}
")
