# Lv2 控制流评估测试

# for loop
for i in range(10):
    a = i

# for with list
for x in items:
    y = x

# break/continue
for n in range(5):
    if n == 3:
        break
    if n == 1:
        continue

# try/except
try:
    x = 1 / 0
except:
    x = 0

# try/except with specific exception
try:
    f = open("test.txt")
except IOError:
    f = None
