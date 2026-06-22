def process_data_file(filename):
    """
    读取文件中的数字，计算平均值。
    演示嵌套的 try-except-else-finally 用法。
    """
    data = None
    
    try:  # 外层 try：负责文件操作
        print(f"[外层] 尝试打开文件: {filename}")
        file = open(filename, 'r')
        
        try:  # 内层 try：负责数据处理
            print("[内层] 开始读取数据...")
            lines = file.readlines()
            
            numbers = []
            for line in lines:
                line = line.strip()
                if not line:  # 跳过空行
                    continue
                    
                try:  # 最内层 try：逐行转换数字
                    num = int(line)
                    numbers.append(num)
                except ValueError:
                    print(f"[最内层 except] 无法转换为整数: '{line}'，已跳过")
                else:
                    print(f"[最内层 else] 成功解析数字: {num}")
                finally:
                    print(f"[最内层 finally] 行处理完毕: '{line}'")
            
            if numbers:
                average = sum(numbers) / len(numbers)
                return average
            else:
                raise ValueError("文件中没有有效的数字")
                
        except ValueError as ve:
            print(f"[内层 except] 数据处理失败: {ve}")
            return None
        else:
            print("[内层 else] 数据处理顺利完成，即将返回结果")
        finally:
            print("[内层 finally] 关闭文件")
            file.close()
            
    except FileNotFoundError:
        print(f"[外层 except] 文件不存在: {filename}")
        return None
    except PermissionError:
        print(f"[外层 except] 没有权限读取文件: {filename}")
        return None
    else:
        print("[外层 else] 文件操作成功完成")
    finally:
        print("[外层 finally] 程序结束")


# ---------- 测试用例 ----------

# 1. 正常情况
print("=" * 50)
print("测试1: 正常文件")
print("=" * 50)
with open("test_numbers.txt", "w") as f:
    f.write("10\n20\nabc\n30\n40\n")
result = process_data_file("test_numbers.txt")
print(f"最终结果: {result}\n")

# 2. 文件不存在
print("=" * 50)
print("测试2: 文件不存在")
print("=" * 50)
result = process_data_file("nonexistent.txt")
print(f"最终结果: {result}\n")

# 3. 文件为空（只有无效数据）
print("=" * 50)
print("测试3: 空文件")
print("=" * 50)
with open("empty_file.txt", "w") as f:
    f.write("abc\ndef\n")
result = process_data_file("empty_file.txt")
print(f"最终结果: {result}\n")