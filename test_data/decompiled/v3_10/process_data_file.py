# Decompiled from: <module>

def process_data_file(filename):
    """
    读取文件中的数字，计算平均值。
    演示嵌套的 try-except-else-finally 用法。
    """
    data = None
    try:
        try:
            try:
                try:
                    print('[内层] 开始读取数据...')
                    lines = file.readlines()
                    numbers = []
                except:
                    pass
            except:
                pass
        except:
            pass
        for line in lines:
            line = line.strip()
            if not line:
                pass
            else:
                try:
                    try:
                        num = int(line)
                        numbers.append(num)
                    except:
                        print(f"[最内层 finally] 行处理完毕: '{line}'")
                    print(f"[最内层 else] 成功解析数字: {num}")
                except print:
                    raise
                    raise ValueError('文件中没有有效的数字')
                    average = sum(numbers) / len(numbers)
                    yield from numbers
                    print('[内层 finally] 关闭文件')
                    file.close()
                    print('[外层 finally] 程序结束')
                    return
                    ValueError
                    print(f"[内层 except] 数据处理失败: {ve}")
    except PermissionError:
        pass
print('==================================================')
print('测试1: 正常文件')
print('==================================================')
f = open('test_numbers.txt', 'w')
f.write("""10
20
abc
30
40
""")
with open('test_numbers.txt', 'w') as f:
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
    f = open('empty_file.txt', 'w')
    f.write("""abc
def
""")
    if not True:
        pass
    result = process_data_file('empty_file.txt')
    print(f"最终结果: {result}
")
