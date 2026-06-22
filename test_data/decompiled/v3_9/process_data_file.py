# Decompiled from: <module>

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
