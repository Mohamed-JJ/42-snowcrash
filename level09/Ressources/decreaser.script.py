import sys

if len(sys.argv) < 2:
    print("need more args")
    exit(1)

ret = ''

for i in range(0, len(sys.argv[1])):
    digit = ord(sys.argv[1][i])

    ret += chr(digit - i)
    # print(i, sys.argv[1][i])

print(ret)