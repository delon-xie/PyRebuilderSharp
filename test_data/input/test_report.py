import subprocess
import os

# 获取所有测试文件
result = subprocess.run(['python3', 'tests/run_tests.py'], capture_output=True, text=True)
output = result.stdout + result.stderr

# 按测试组整理结果
test_groups = {}
current_group = None

for line in output.split('\n'):
    if line.startswith('***'):
        parts = line.split(':')
        if len(parts) >= 2:
            current_group = parts[0].strip().replace('*** ', '')
            status = parts[1].strip()
            test_groups[current_group] = {'status': status, 'files': []}
    elif current_group and line.strip().endswith('.3.10.pyc'):
        test_groups[current_group]['files'].append(line.strip())

# 输出报告
print('=' * 60)
print('Python 3.10 版本测试报告')
print('=' * 60)

passed_groups = []
failed_groups = []

for group, info in test_groups.items():
    if info['files']:
        if 'PASS' in info['status']:
            passed_groups.append(group)
        elif 'FAIL' in info['status']:
            failed_groups.append(group)

print(f'\n通过的测试组 ({len(passed_groups)}):')
print('-' * 40)
for group in passed_groups:
    print(f'  ✓ {group}')

print(f'\n失败的测试组 ({len(failed_groups)}):')
print('-' * 40)
for group in failed_groups:
    print(f'  ✗ {group}')
    for f in test_groups[group]['files']:
        print(f'    - {f}')

print(f'\n总计: {len(passed_groups)} 组通过, {len(failed_groups)} 组失败')
