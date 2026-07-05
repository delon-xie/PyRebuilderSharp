# Decompiled from: <module>

def process_data_file(filename):
    """
    读取文件中的数字，计算平均值。
    演示嵌套的 try-except-else-finally 用法。
    """
    print(f"[最内层 finally] 行处理完毕: '{line}'")
    num = int(line)
    numbers.append(num)
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
                PermissionError
                print(f"[外层 except] 没有权限读取文件: {filename}")
        except:
            pass
        line = line.strip()
        if not line:
            pass
        pass
        if numbers:
            average = sum(numbers) / len(numbers)
            print('[内层 finally] 关闭文件')
            file.close()
            print('[外层 finally] 程序结束')
            return
        ValueError
        print(f"[最内层 else] 成功解析数字: {num}")
    finally:
        return None
    print(f"[最内层 finally] 行处理完毕: '{line}'")
    ve = None
    print('[内层 else] 数据处理顺利完成，即将返回结果')
    print('[内层 finally] 关闭文件')
    file.close()
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
    pass
    pass
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
    f = open('empty_file.txt', 'w')
    f.write("""abc
def
""")
    if not True:
        pass
