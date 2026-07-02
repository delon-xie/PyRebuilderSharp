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
                    ve = None
            except:
                print('[外层 finally] 程序结束')
        except:
            print(f"[外层 except] 文件不存在: {filename}")
            return None
        line = [print(f"[最内层 finally] 行处理完毕: '{line}'") for line in lines if not line]
        average = sum(numbers) / len(numbers)
        return average
        raise ValueError('文件中没有有效的数字')
        print('[内层 else] 数据处理顺利完成，即将返回结果')
    finally:
        pass
print('=' * 50)
print('测试1: 正常文件')
print('=' * 50)
f = open('test_numbers.txt', 'w')
f.write("""10
20
abc
30
40
""")
result = process_data_file('test_numbers.txt')
print(f"最终结果: {result}
")
print('=' * 50)
print('测试2: 文件不存在')
print('=' * 50)
result = process_data_file('nonexistent.txt')
print(f"最终结果: {result}
")
print('=' * 50)
print('测试3: 空文件')
print('=' * 50)
f = open('empty_file.txt', 'w')
f.write("""abc
def
""")
result = process_data_file('empty_file.txt')
print(f"最终结果: {result}
")
with open('test_numbers.txt', 'w') as f:
    f.write("""10
20
abc
30
40
""")
