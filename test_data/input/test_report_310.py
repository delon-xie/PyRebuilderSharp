import subprocess
import re

# 运行测试并保存输出
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True, cwd='/Users/admin/codes/Tools/PyRebuild/ref/pycdc')

lines = result.stdout.split('\n')

print('=' * 60)
print('Python 3.10 版本测试报告')
print('=' * 60)

passed = 0
failed = 0
current_test = None
current_test_fail = False

# 移除 ANSI 转义序列的函数
def remove_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

for line in lines:
    # 移除 ANSI 转义序列
    clean_line = remove_ansi(line)
    line_stripped = clean_line.strip()
    
    if line_stripped.startswith('*** '):
        # 新的测试组
        if current_test:
            # 输出上一个测试的结果
            if current_test_fail:
                print(f'✗ {current_test}')
                failed += 1
            else:
                print(f'✓ {current_test}')
                passed += 1
        
        # 开始新测试
        current_test = line_stripped[4:].split(':')[0]
        current_test_fail = False
        
        # 检查这一行是否有 FAIL
        if 'FAIL' in line_stripped:
            current_test_fail = True
    
    elif current_test:
        # 检查是否是 3.10.pyc 文件
        if '3.10.pyc' in clean_line:
            # 如果测试行有 FAIL，标记为失败
            if 'FAIL' in clean_line or 'Unsupported' in clean_line or 'Bad MAGIC' in clean_line:
                current_test_fail = True

# 输出最后一个测试的结果
if current_test:
    if current_test_fail:
        print(f'✗ {current_test}')
        failed += 1
    else:
        print(f'✓ {current_test}')
        passed += 1

print('=' * 60)
print(f'总计: {passed} PASS, {failed} FAIL')
print('=' * 60)
